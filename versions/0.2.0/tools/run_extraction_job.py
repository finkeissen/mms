#!/usr/bin/env python3
"""
MMS Tool: run_extraction_job.py

Runs a single extraction job in a hardened way:
- loads a prompt template
- fills placeholders with a job payload
- calls an LLM via a pluggable adapter (stdout stub by default)
- validates output against schema + hardening checks
- if invalid: runs repair mode up to N retries (by printing the repair prompt)
- writes the final JSON result to an output file

IMPORTANT:
This file ships with a NO-NETWORK default adapter.
Integrate your own LLM adapter in `call_llm()`.

Usage example (no network; you paste model output manually):
  python mms/0.2.0/tools/run_extraction_job.py \
    --prompt mms/0.2.0/prompts/extraction/domain.generate.prompt.md \
    --schema mms/0.2.0/schemas/extraction-job-result.schema.json \
    --job-type domain \
    --seed-topics '["Medizin","Jura","Ökonomie"]' \
    --max-items 20 \
    --language de \
    --model gpt-5 \
    --out out/job-domain.json

Exit codes:
  0 = success
  5 = validation failed after retries
  4 = IO/unexpected error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from validate_extraction_job import (
    compute_input_hash,
    hardening_checks,
    read_schema,
    validate_schema,
)

PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fill_placeholders(template: str, mapping: Dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        key = m.group(1)
        if key not in mapping:
            raise KeyError(f"Missing placeholder value for: {key}")
        return mapping[key]

    return PLACEHOLDER_RE.sub(repl, template)


def make_job_payload(
    job_type: str,
    seed_topics_json: str,
    max_items: int,
    language: str,
    parent_domain_id: Optional[str],
    parent_domain_title: Optional[str],
) -> Dict[str, Any]:
    inputs: Dict[str, Any] = {}
    constraints: Dict[str, Any] = {}

    if job_type == "domain":
        inputs["seed_topics"] = json.loads(seed_topics_json) if seed_topics_json else []
        constraints["max_items"] = max_items
        constraints["language"] = language
        constraints["style"] = "neutral"
        constraints["allow_overlap"] = True

    elif job_type == "subdomain":
        if not parent_domain_id or not parent_domain_title:
            raise ValueError("subdomain requires --parent-domain-id and --parent-domain-title")
        inputs["parent_domain"] = {"id": parent_domain_id, "title": parent_domain_title}
        constraints["max_items"] = max_items
        constraints["language"] = language
        constraints["style"] = "neutral"
        constraints["allow_overlap"] = True

    else:
        # placeholders for later job types
        inputs["parent"] = {"id": parent_domain_id, "title": parent_domain_title}
        constraints["max_items"] = max_items
        constraints["language"] = language

    job = {
        "job_id": f"job::{job_type}::{int(time.time())}",
        "job_type": job_type,
        "version": "0.1",
        "inputs": inputs,
        "constraints": constraints,
    }
    return job


def call_llm(prompt_text: str, model: str) -> str:
    """
    Default adapter: NO NETWORK.
    Prints the prompt and reads JSON from stdin.

    Replace this function with your real model call. It must return the raw model output string.
    """
    print("\n" + "=" * 80)
    print("PROMPT TO SEND TO MODEL")
    print("=" * 80)
    print(prompt_text)
    print("=" * 80)
    print("PASTE MODEL JSON OUTPUT BELOW. End with EOF (Ctrl-D on Unix, Ctrl-Z Enter on Windows).")
    print("=" * 80)

    data = sys.stdin.read()
    return data.strip()


def validate(doc: Any, schema: Dict[str, Any], strict: bool = False) -> Optional[str]:
    schema_issues = validate_schema(doc, schema)
    if schema_issues:
        return "\n".join(f"[ERROR] {i.path}: {i.message}" for i in schema_issues)

    if not isinstance(doc, dict):
        return "[ERROR] /: Top-level must be an object."

    hard_issues = hardening_checks(doc)
    errors = [i for i in hard_issues if i.level == "error"]
    warnings = [i for i in hard_issues if i.level == "warning"]

    if errors:
        return "\n".join(f"[ERROR] {i.path}: {i.message}" for i in errors)
    if strict and warnings:
        return "\n".join(f"[WARNING] {i.path}: {i.message}" for i in warnings)
    return None


def build_prompt_mapping(
    job: Dict[str, Any],
    run_id: str,
    model: str,
    prompt_id: str,
    created_at_iso: str,
    input_hash: str,
    seed_topics_json: str,
    max_items: int,
    language: str,
    parent_domain_id: Optional[str],
    parent_domain_title: Optional[str],
) -> Dict[str, str]:
    # Keep values as strings (templates are plain text).
    mapping: Dict[str, str] = {
        "job_id": job["job_id"],
        "run_id": run_id,
        "model": model,
        "created_at_iso": created_at_iso,
        "input_hash": input_hash,
        "seed_topics_json": seed_topics_json if seed_topics_json else "[]",
        "max_items": str(max_items),
        "language": language,
        "parent_domain_id": parent_domain_id or "",
        "parent_domain_title": json.dumps(parent_domain_title or "", ensure_ascii=False),
        # Note: parent_domain_title is injected as JSON string to preserve quotes safely.
        "invalid_output_text": "",  # used only by repair prompt
    }
    return mapping


def extract_prompt_id(prompt_text: str) -> str:
    # expects a line like: "# prompt_id: ..."
    for line in prompt_text.splitlines():
        if line.strip().lower().startswith("# prompt_id:"):
            return line.split(":", 1)[1].strip()
    return "unknown-prompt-id"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Run a hardened MMS extraction job.")
    p.add_argument("--prompt", required=True, help="Prompt template path (md).")
    p.add_argument("--repair-prompt", default="mms/0.2.0/prompts/extraction/repair-json.prompt.md")
    p.add_argument("--schema", required=True, help="Schema path (json).")
    p.add_argument("--job-type", required=True, choices=["domain", "subdomain"], help="Job type.")
    p.add_argument("--seed-topics", default="[]", help="JSON array string for domain seed topics.")
    p.add_argument("--max-items", type=int, default=25)
    p.add_argument("--language", default="en", choices=["de", "en"])
    p.add_argument("--model", required=True, help="Model name for provenance.")
    p.add_argument("--parent-domain-id", default=None)
    p.add_argument("--parent-domain-title", default=None)
    p.add_argument("--out", required=True, help="Output JSON file path.")
    p.add_argument("--strict", action="store_true", help="Treat warnings as errors.")
    p.add_argument("--max-repairs", type=int, default=2)
    args = p.parse_args(argv)

    try:
        prompt_path = Path(args.prompt)
        repair_path = Path(args.repair_prompt)
        schema_path = Path(args.schema)
        out_path = Path(args.out)

        schema = read_schema(schema_path)

        job = make_job_payload(
            job_type=args.job_type,
            seed_topics_json=args.seed_topics,
            max_items=args.max_items,
            language=args.language,
            parent_domain_id=args.parent_domain_id,
            parent_domain_title=args.parent_domain_title,
        )

        run_id = f"run::{int(time.time())}"
        created_at_iso = utc_now_iso()
        input_hash = compute_input_hash(job["inputs"], job["constraints"])

        prompt_text = load_text(prompt_path)
        prompt_id = extract_prompt_id(prompt_text)

        mapping = build_prompt_mapping(
            job=job,
            run_id=run_id,
            model=args.model,
            prompt_id=prompt_id,
            created_at_iso=created_at_iso,
            input_hash=input_hash,
            seed_topics_json=args.seed_topics,
            max_items=args.max_items,
            language=args.language,
            parent_domain_id=args.parent_domain_id,
            parent_domain_title=args.parent_domain_title,
        )

        filled_prompt = fill_placeholders(prompt_text, mapping)
        raw = call_llm(filled_prompt, model=args.model)

        for attempt in range(args.max_repairs + 1):
            raw_str = raw.strip()
            try:
                doc = json.loads(raw_str)
            except json.JSONDecodeError as e:
                err_msg = f"[ERROR] invalid JSON: {e}"
                doc = None

            if doc is not None:
                v = validate(doc, schema, strict=args.strict)
                if v is None:
                    write_json(out_path, doc)
                    print(f"OK: wrote {out_path}")
                    return 0
                err_msg = v

            # If we are out of repair attempts, fail.
            if attempt >= args.max_repairs:
                print("FAILED: validation after repairs.", file=sys.stderr)
                print(err_msg, file=sys.stderr)
                return 5

            # Repair step: fill repair prompt with invalid output and re-run.
            repair_template = load_text(repair_path)
            mapping["invalid_output_text"] = json.dumps(raw_str, ensure_ascii=False)
            repair_prompt = fill_placeholders(repair_template, mapping)

            raw = call_llm(repair_prompt, model=args.model)

        return 5

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())

