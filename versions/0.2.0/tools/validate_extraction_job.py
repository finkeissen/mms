#!/usr/bin/env python3
"""
MMS Tool: validate_extraction_job.py

Validates an MMS Extraction Job Result (JSON) against the canonical schema:
- mms/0.2.0/schemas/extraction-job-result.schema.json

Optionally enforces additional "hardening" rules beyond JSON Schema, e.g.:
- job_type-specific constraints (domain parent_id must be null, etc.)
- deterministic ID format checks
- STOP semantics checks

This tool does NOT call an LLM.
If you want auto-repair, integrate this validator with your runner that can
invoke the repair prompt and then re-run validation.

Usage:
  python mms/0.2.0/tools/validate_extraction_job.py \
    --input path/to/job-result.json \
    --schema mms/0.2.0/schemas/extraction-job-result.schema.json

Exit codes:
  0 = valid
  2 = schema validation failed
  3 = hardening checks failed
  4 = IO or unexpected error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import jsonschema
except ImportError as e:
    print("ERROR: Missing dependency 'jsonschema'. Install it first.", file=sys.stderr)
    raise


ID_PATTERNS = {
    "domain": re.compile(r"^dom::[a-z0-9-]+$"),
    "subdomain": re.compile(r"^sub::[a-z0-9-]+::[a-z0-9-]+$"),
    "problem_area": re.compile(r"^area::[a-z0-9-]+::[a-z0-9-]+$"),
    "atomic_problem": re.compile(r"^ap::[a-z0-9-]+::[a-z0-9-]+$"),
    "problem_detail": re.compile(r"^pd::[a-z0-9-]+::[a-z0-9-]+$"),
}

JOB_TYPES = ("domain", "subdomain", "problem_area", "atomic_problem", "problem_detail")
STATUSES = ("ok", "stop", "error")


@dataclass
class ValidationIssue:
    level: str  # "error" or "warning"
    path: str
    message: str


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_schema(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def canonicalize_for_hash(obj: Any) -> str:
    """
    Canonical JSON serialization for stable hashing.
    """
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def compute_input_hash(job_inputs: Dict[str, Any], job_constraints: Dict[str, Any]) -> str:
    """
    Computes the input_hash the same way MMS should: from canonicalized inputs+constraints.
    """
    payload = {"inputs": job_inputs, "constraints": job_constraints}
    canon = canonicalize_for_hash(payload).encode("utf-8")
    return hashlib.sha256(canon).hexdigest()


def validate_schema(instance: Any, schema: Dict[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(instance), key=str):
        path = "/" + "/".join(str(p) for p in err.absolute_path)
        issues.append(ValidationIssue(level="error", path=path, message=err.message))
    return issues


def hardening_checks(doc: Dict[str, Any]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []

    # Basic top-level expectations (schema already covers structure, but keep defensive checks)
    job = doc.get("job", {})
    result = doc.get("result", {})
    prov = doc.get("provenance", {})

    job_type = job.get("job_type")
    status = result.get("status")

    if job_type not in JOB_TYPES:
        issues.append(ValidationIssue("error", "/job/job_type", f"Unknown job_type: {job_type!r}"))
        return issues  # further checks depend on job_type

    if status not in STATUSES:
        issues.append(ValidationIssue("error", "/result/status", f"Unknown status: {status!r}"))
        return issues

    # STOP semantics (beyond schema: errors must be empty on stop)
    if status == "stop":
        if result.get("items") not in ([], None) and len(result.get("items", [])) != 0:
            issues.append(ValidationIssue("error", "/result/items", "STOP requires items to be empty."))
        sr = result.get("stop_reason")
        if not isinstance(sr, str) or not sr.strip():
            issues.append(ValidationIssue("error", "/result/stop_reason", "STOP requires non-empty stop_reason."))
        errs = result.get("errors", [])
        if isinstance(errs, list) and len(errs) != 0:
            issues.append(ValidationIssue("error", "/result/errors", "STOP requires errors to be empty."))

    # OK semantics (ensure stop_reason is null)
    if status == "ok":
        if result.get("stop_reason", None) is not None:
            issues.append(ValidationIssue("error", "/result/stop_reason", "OK requires stop_reason to be null."))

    # ERROR semantics (must include errors, schema enforces minItems but double check)
    if status == "error":
        errs = result.get("errors", [])
        if not isinstance(errs, list) or len(errs) < 1:
            issues.append(ValidationIssue("error", "/result/errors", "ERROR requires at least one error entry."))

    # Provenance sanity: created_at parse
    created_at = prov.get("created_at")
    if isinstance(created_at, str):
        try:
            # Accept ISO 8601 with timezone (preferred). datetime.fromisoformat handles many forms.
            datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except Exception:
            issues.append(ValidationIssue("warning", "/provenance/created_at", "created_at is not ISO-8601 parseable."))

    # Input hash consistency (warning by default because runners may evolve)
    try:
        inputs = job.get("inputs", {})
        constraints = job.get("constraints", {})
        expected_hash = compute_input_hash(inputs, constraints)
        actual_hash = prov.get("input_hash")
        if isinstance(actual_hash, str) and actual_hash != expected_hash:
            issues.append(
                ValidationIssue(
                    "warning",
                    "/provenance/input_hash",
                    "input_hash does not match sha256(canonical(inputs+constraints)).",
                )
            )
    except Exception:
        issues.append(ValidationIssue("warning", "/provenance/input_hash", "Could not recompute input_hash."))

    # Per-item checks (only if status ok)
    if status == "ok":
        items = result.get("items", [])
        if not isinstance(items, list):
            issues.append(ValidationIssue("error", "/result/items", "items must be an array."))
            return issues

        id_re = ID_PATTERNS[job_type]

        for i, item in enumerate(items):
            pfx = f"/result/items/{i}"

            # required keys should exist by schema; still check types and domain-specific constraints
            _id = item.get("id")
            parent_id = item.get("parent_id")
            title = item.get("title")
            summary = item.get("summary")

            if not isinstance(_id, str) or not _id.strip():
                issues.append(ValidationIssue("error", f"{pfx}/id", "id must be a non-empty string."))
            else:
                if not id_re.match(_id):
                    issues.append(
                        ValidationIssue(
                            "error",
                            f"{pfx}/id",
                            f"id does not match required pattern for {job_type}: {id_re.pattern}",
                        )
                    )

            if job_type == "domain":
                if parent_id is not None:
                    issues.append(ValidationIssue("error", f"{pfx}/parent_id", "domain items require parent_id = null."))
            else:
                if not isinstance(parent_id, str) or not parent_id.strip():
                    issues.append(ValidationIssue("error", f"{pfx}/parent_id", f"{job_type} items require parent_id."))

            if not isinstance(title, str) or not title.strip():
                issues.append(ValidationIssue("error", f"{pfx}/title", "title must be a non-empty string."))

            if not isinstance(summary, str) or not summary.strip():
                issues.append(ValidationIssue("error", f"{pfx}/summary", "summary must be a non-empty string."))

            scope = item.get("scope")
            tags = item.get("tags")
            if not isinstance(scope, list):
                issues.append(ValidationIssue("error", f"{pfx}/scope", "scope must be an array of strings."))
            if not isinstance(tags, list):
                issues.append(ValidationIssue("error", f"{pfx}/tags", "tags must be an array of strings."))

    return issues


def format_issues(issues: List[ValidationIssue]) -> str:
    lines = []
    for iss in issues:
        lines.append(f"[{iss.level.upper()}] {iss.path}: {iss.message}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate MMS extraction job result JSON.")
    parser.add_argument("--input", required=True, type=str, help="Path to extraction job result JSON file.")
    parser.add_argument(
        "--schema",
        required=True,
        type=str,
        help="Path to extraction-job-result.schema.json",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors.",
    )
    args = parser.parse_args(argv)

    try:
        input_path = Path(args.input)
        schema_path = Path(args.schema)

        doc = read_json(input_path)
        schema = read_schema(schema_path)

        schema_issues = validate_schema(doc, schema)
        if schema_issues:
            print(format_issues(schema_issues), file=sys.stderr)
            return 2

        if not isinstance(doc, dict):
            print("[ERROR] /: Top-level JSON must be an object.", file=sys.stderr)
            return 2

        hard_issues = hardening_checks(doc)
        if hard_issues:
            errors = [i for i in hard_issues if i.level == "error"]
            warnings = [i for i in hard_issues if i.level == "warning"]

            if errors or (args.strict and warnings):
                print(format_issues(hard_issues), file=sys.stderr)
                return 3

            # warnings only
            print(format_issues(warnings), file=sys.stderr)

        print("OK: extraction job result is valid.")
        return 0

    except FileNotFoundError as e:
        print(f"ERROR: file not found: {e}", file=sys.stderr)
        return 4
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"ERROR: unexpected failure: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())

