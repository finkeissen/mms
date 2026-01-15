#!/usr/bin/env python3
"""
MMS 0.5.0 Pilot Runner — problem-centered LLM extraction (hardened)

- Reads mms.problem JSON files
- Calls LLMs via provider plugins (openai, lmstudio)
- Enforces strict JSON output
- Validates against record.schema.json
- Writes mms.fact_record JSONL
- Produces auditable run-report.json

Fail-closed by default.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import jsonschema

from providers.llm_provider import build_provider


# ---------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------

def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def is_problem_record(obj: Dict[str, Any]) -> bool:
    return obj.get("record_type") == "mms.problem" and isinstance(obj.get("problem_id"), str)


def prompt_hash(prompt_text: str) -> str:
    return "sha256:" + sha256_hex(prompt_text)


# ---------------------------------------------------------------------
# error model
# ---------------------------------------------------------------------

@dataclass
class ErrorEvent:
    timestamp: str
    error_code: str
    problem_id: Optional[str]
    prompt_id: Optional[str]
    provider: Optional[str]
    model: Optional[str]
    message: str
    raw_response_hash: Optional[str] = None


class ErrorCodes:
    E1_TRANSPORT = "E1_TRANSPORT"
    E2_PARSE = "E2_PARSE"
    E2_SCHEMA = "E2_SCHEMA"
    E4_PROVENANCE = "E4_PROVENANCE"
    E5_INPUT = "E5_INPUT"


# ---------------------------------------------------------------------
# schema validation
# ---------------------------------------------------------------------

class SchemaValidator:
    def __init__(self, record_schema_path: Path):
        self.schema = read_json(record_schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    def validate(self, record: Dict[str, Any]) -> None:
        errors = sorted(self.validator.iter_errors(record), key=lambda e: e.path)
        if errors:
            msg = "; ".join(
                f"{'/'.join(map(str, e.path))}: {e.message}"
                for e in errors[:5]
            )
            raise ValueError(msg)


# ---------------------------------------------------------------------
# prompt handling
# ---------------------------------------------------------------------

def load_prompt_text(path: Path, *, problem_json: str, context: str) -> str:
    template = path.read_text(encoding="utf-8")
    return (
        template.replace("{{PROBLEM_JSON}}", problem_json)
                .replace("{{CONTEXT}}", context)
    )


def parse_strict_json(text: str) -> Dict[str, Any]:
    s = text.strip()
    if s.startswith("```"):
        raise ValueError("Markdown fences not allowed")
    if not (s.startswith("{") and s.endswith("}")):
        raise ValueError("Not a single JSON object")
    return json.loads(s)


def validate_extract_output(obj: Dict[str, Any]):
    if obj.get("status") not in ("asserted", "unknown", "no-claim"):
        raise ValueError("Invalid status")
    claims = obj.get("claims", [])
    if obj["status"] == "asserted" and not claims:
        raise ValueError("asserted requires claims")
    if obj["status"] != "asserted" and claims:
        raise ValueError("non-asserted must not contain claims")
    for c in claims:
        if not isinstance(c.get("text"), str) or not isinstance(c.get("language"), str):
            raise ValueError("Invalid claim")
    return obj["status"], claims


# ---------------------------------------------------------------------
# fact record
# ---------------------------------------------------------------------

def new_record_id() -> str:
    return uuid.uuid4().hex


def build_fact_record(
    *,
    mms_version: str,
    rp_version: str,
    claim_text: str,
    claim_language: str,
    problem_id: str,
    provider: str,
    model: str,
    temperature: float,
    prompt_id: str,
    prompt_hash_value: str,
    run_id: str
) -> Dict[str, Any]:
    return {
        "record_type": "mms.fact_record",
        "record_id": new_record_id(),
        "mms_version": mms_version,
        "rp_version": rp_version,
        "created_at": utc_now_iso(),
        "status": "asserted",
        "claim": {
            "text": claim_text,
            "language": claim_language
        },
        "source": {
            "source_id": f"llm:{provider}:{model}",
            "source_type": "llm",
            "llm": {
                "provider": provider,
                "model": model,
                "temperature": temperature,
                "prompt_id": prompt_id,
                "prompt_hash": prompt_hash_value
            }
        },
        "provenance": {
            "run_id": run_id,
            "pipeline_id": "mms.0.5.0.pilot"
        },
        "problem_id": problem_id
    }


# ---------------------------------------------------------------------
# retry
# ---------------------------------------------------------------------

def call_with_retries(client, prompt_text: str, max_retries: int, backoff: List[int]) -> str:
    for i in range(max_retries + 1):
        try:
            return client.complete(prompt_text)
        except Exception:
            if i >= max_retries:
                raise
            time.sleep(backoff[min(i, len(backoff) - 1)])


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

def run() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--mms-version", default="0.5.0")
    ap.add_argument("--rp-version", default="0.4.0")

    ap.add_argument("--problems-dir", required=True)
    ap.add_argument("--contexts-dir", default="")
    ap.add_argument("--outputs-dir", required=True)

    ap.add_argument("--record-schema", required=True)
    ap.add_argument("--extract-prompt", required=True)
    ap.add_argument("--prompt-id", default="mms.pilot.extract_facts.v0.1")

    ap.add_argument("--max-retries", type=int, default=2)
    ap.add_argument("--backoff", default="5,30")

    args = ap.parse_args()

    problems_dir = Path(args.problems_dir)
    contexts_dir = Path(args.contexts_dir) if args.contexts_dir else None
    outputs_dir = Path(args.outputs_dir)

    facts_jsonl = outputs_dir / "facts.jsonl"
    report_path = outputs_dir / "run-report.json"

    validator = SchemaValidator(Path(args.record_schema))
    provider_client = build_provider(
        provider=args.provider,
        model=args.model,
        temperature=args.temperature
    )

    run_id = f"run-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%SZ')}"

    report = {
        "run_id": run_id,
        "started_at": utc_now_iso(),
        "ended_at": None,
        "errors": [],
        "counters": {
            "problems_processed": 0,
            "fact_records_written": 0,
            "errors": 0
        }
    }

    backoff = [int(x) for x in args.backoff.split(",") if x.strip()]
    prompt_path = Path(args.extract_prompt)

    for pfile in sorted(problems_dir.glob("*.json")):
        try:
            problem = read_json(pfile)
            if not is_problem_record(problem):
                raise ValueError("Invalid problem record")
        except Exception as e:
            report["errors"].append(ErrorEvent(
                utc_now_iso(), ErrorCodes.E5_INPUT, None,
                args.prompt_id, args.provider, args.model, str(e)
            ).__dict__)
            report["counters"]["errors"] += 1
            continue

        report["counters"]["problems_processed"] += 1
        problem_id = problem["problem_id"]

        context = ""
        if contexts_dir:
            cfile = contexts_dir / (pfile.stem + ".txt")
            if cfile.exists():
                context = cfile.read_text(encoding="utf-8")

        rendered = load_prompt_text(
            prompt_path,
            problem_json=json.dumps(problem, ensure_ascii=False, sort_keys=True),
            context=context
        )
        phash = prompt_hash(rendered)

        try:
            raw = call_with_retries(provider_client, rendered, args.max_retries, backoff)
            out = parse_strict_json(raw)
            status, claims = validate_extract_output(out)
        except Exception as e:
            report["errors"].append(ErrorEvent(
                utc_now_iso(), ErrorCodes.E2_PARSE, problem_id,
                args.prompt_id, args.provider, args.model, str(e)
            ).__dict__)
            report["counters"]["errors"] += 1
            continue

        if status != "asserted":
            continue

        for c in claims:
            rec = build_fact_record(
                mms_version=args.mms_version,
                rp_version=args.rp_version,
                claim_text=c["text"],
                claim_language=c["language"],
                problem_id=problem_id,
                provider=args.provider,
                model=args.model,
                temperature=args.temperature,
                prompt_id=args.prompt_id,
                prompt_hash_value=phash,
                run_id=run_id
            )
            try:
                validator.validate(rec)
                append_jsonl(facts_jsonl, rec)
                report["counters"]["fact_records_written"] += 1
            except Exception as e:
                report["errors"].append(ErrorEvent(
                    utc_now_iso(), ErrorCodes.E4_PROVENANCE, problem_id,
                    args.prompt_id, args.provider, args.model, str(e)
                ).__dict__)
                report["counters"]["errors"] += 1

    report["ended_at"] = utc_now_iso()
    write_json(report_path, report)
    return 0


if __name__ == "__main__":
    sys.exit(run())

