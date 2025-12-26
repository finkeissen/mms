#!/usr/bin/env python3
"""
MMS Tool: persist_extraction_job.py

Takes a validated Extraction Job Result JSON and persists:
1) run record -> runs.jsonl (one line per job run)
2) each extracted item -> artifacts.jsonl (one line per item, append-only)

Design goals:
- Append-only JSONL for scalability
- Deterministic de-duplication (optional)
- No epistemic claims (system records only)
- STOP and ERROR runs are still persisted (as run records)

Input must already conform to:
mms/0.2.0/schemas/extraction-job-result.schema.json

Usage:
  python mms/0.2.0/tools/persist_extraction_job.py \
    --input out/job-domain.json \
    --store mms/0.2.0/store \
    --dedupe

Outputs:
  <store>/runs.jsonl
  <store>/artifacts.jsonl

Exit codes:
  0 = success
  6 = invalid input file / schema mismatch / semantic mismatch
  4 = IO/unexpected error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Set, Tuple

from validate_extraction_job import read_schema, validate_schema, hardening_checks


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def stable_item_key(job_type: str, item: Dict[str, Any]) -> str:
    """
    Deterministic key used for de-duplication across runs.
    We base this on job_type + id. (Id is expected to be stable.)
    """
    _id = item.get("id", "")
    return f"{job_type}::{_id}"


def load_existing_keys(artifacts_path: Path) -> Set[str]:
    """
    Loads existing keys from artifacts.jsonl for dedupe.
    For large stores, replace with an index. This is the minimal hardened version.
    """
    keys: Set[str] = set()
    if not artifacts_path.exists():
        return keys

    with artifacts_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                k = obj.get("_key")
                if isinstance(k, str):
                    keys.add(k)
            except Exception:
                # ignore malformed historical lines; store is append-only
                continue
    return keys


def make_run_record(doc: Dict[str, Any], store_version: str = "0.1") -> Dict[str, Any]:
    job = doc["job"]
    result = doc["result"]
    prov = doc["provenance"]

    return {
        "_type": "mms.run",
        "_version": store_version,
        "created_at": utc_now_iso(),
        "job": job,
        "result_meta": {
            "status": result.get("status"),
            "items_count": len(result.get("items", [])) if isinstance(result.get("items"), list) else 0,
            "stop_reason": result.get("stop_reason"),
            "errors_count": len(result.get("errors", [])) if isinstance(result.get("errors"), list) else 0,
        },
        "provenance": prov,
    }


def make_artifact_record(
    doc: Dict[str, Any],
    item: Dict[str, Any],
    store_version: str = "0.1",
) -> Dict[str, Any]:
    job = doc["job"]
    prov = doc["provenance"]

    # System-level record; still preserves job + provenance
    record: Dict[str, Any] = {
        "_type": "mms.artifact",
        "_version": store_version,
        "created_at": utc_now_iso(),
        "level": job["job_type"],  # domain|subdomain|...
        "item": item,
        "job_ref": {
            "job_id": job["job_id"],
            "job_type": job["job_type"],
            "job_version": job["version"],
        },
        "provenance": prov,
    }
    record["_key"] = stable_item_key(job["job_type"], item)
    return record


def validate_input(doc: Any, schema: Dict[str, Any]) -> Tuple[bool, str]:
    if not isinstance(doc, dict):
        return False, "Top-level JSON must be an object."

    schema_issues = validate_schema(doc, schema)
    if schema_issues:
        msg = "\n".join(f"[SCHEMA] {i.path}: {i.message}" for i in schema_issues)
        return False, msg

    hard_issues = hardening_checks(doc)
    errors = [i for i in hard_issues if i.level == "error"]
    if errors:
        msg = "\n".join(f"[HARDEN] {i.path}: {i.message}" for i in errors)
        return False, msg

    return True, "OK"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Persist MMS extraction job output to JSONL store.")
    p.add_argument("--input", required=True, help="Path to validated extraction job result JSON.")
    p.add_argument("--schema", default="mms/0.2.0/schemas/extraction-job-result.schema.json")
    p.add_argument("--store", required=True, help="Store directory (will contain runs.jsonl + artifacts.jsonl).")
    p.add_argument("--runs-file", default="runs.jsonl")
    p.add_argument("--artifacts-file", default="artifacts.jsonl")
    p.add_argument("--dedupe", action="store_true", help="Skip items already present (by stable key).")
    args = p.parse_args(argv)

    try:
        input_path = Path(args.input)
        schema_path = Path(args.schema)
        store_dir = Path(args.store)

        runs_path = store_dir / args.runs_file
        artifacts_path = store_dir / args.artifacts_file

        schema = read_schema(schema_path)
        doc = read_json(input_path)

        ok, msg = validate_input(doc, schema)
        if not ok:
            print("INVALID INPUT:", file=sys.stderr)
            print(msg, file=sys.stderr)
            return 6

        # Always write run record (even if STOP/ERROR)
        run_rec = make_run_record(doc)
        append_jsonl(runs_path, run_rec)

        status = doc["result"]["status"]
        if status != "ok":
            print(f"OK: persisted run ({status}), no items written.")
            return 0

        items = doc["result"].get("items", [])
        if not isinstance(items, list):
            print("INVALID INPUT: result.items must be an array.", file=sys.stderr)
            return 6

        existing_keys: Set[str] = set()
        if args.dedupe:
            existing_keys = load_existing_keys(artifacts_path)

        written = 0
        skipped = 0

        for item in items:
            if not isinstance(item, dict):
                continue
            rec = make_artifact_record(doc, item)
            k = rec["_key"]
            if args.dedupe and k in existing_keys:
                skipped += 1
                continue
            append_jsonl(artifacts_path, rec)
            written += 1
            if args.dedupe:
                existing_keys.add(k)

        print(f"OK: persisted run + {written} items (skipped {skipped}).")
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

