#!/usr/bin/env python3
"""
MMS Tool: chain_extract.py

Runs the extraction chain step-by-step and persists results to a JSONL store.

Current implemented chain:
1) domain
2) subdomain (for each produced domain)

Next levels (problem_area, atomic_problem, problem_detail) are intentionally
left for the next steps to avoid premature complexity.

This tool uses:
- mms/0.2.0/tools/run_extraction_job.py
- mms/0.2.0/tools/persist_extraction_job.py

By default, run_extraction_job.py uses a NO-NETWORK adapter:
it prints the prompt and you paste the model output JSON via stdin.

Usage:
  python mms/0.2.0/tools/chain_extract.py \
    --store mms/0.2.0/store \
    --model gpt-5 \
    --language de \
    --seed-topics '["Medizin","Jura","Ökonomie","Politik","Psychologie","Physik"]' \
    --max-domains 25 \
    --max-subdomains 25 \
    --dedupe

Exit codes:
  0 = success
  7 = upstream tool failed
  4 = IO/unexpected error
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def run_cmd(cmd: List[str]) -> Tuple[int, str, str]:
    """
    Runs a command interactively (inherits stdin for paste flows).
    Captures stdout/stderr for logging.
    """
    proc = subprocess.Popen(
        cmd,
        stdin=sys.stdin,  # important: allow interactive paste in run_extraction_job.py
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate()
    return proc.returncode, out, err


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_title(x: Any) -> str:
    if isinstance(x, str):
        return x
    return ""


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Run MMS extraction chain (domain -> subdomain) and persist results.")
    p.add_argument("--store", required=True, help="Store directory (runs.jsonl + artifacts.jsonl).")
    p.add_argument("--model", required=True, help="Model name for provenance (e.g. gpt-5).")
    p.add_argument("--language", default="en", choices=["de", "en"])
    p.add_argument("--seed-topics", default="[]", help="JSON array string, used for domain generation.")
    p.add_argument("--max-domains", type=int, default=25)
    p.add_argument("--max-subdomains", type=int, default=25)
    p.add_argument("--dedupe", action="store_true", help="Skip persisting duplicate artifacts (by key).")
    p.add_argument("--strict", action="store_true", help="Treat validator warnings as errors.")
    args = p.parse_args(argv)

    try:
        store_dir = Path(args.store)
        store_dir.mkdir(parents=True, exist_ok=True)

        # Paths
        schema_path = "mms/0.2.0/schemas/extraction-job-result.schema.json"

        prompt_domain = "mms/0.2.0/prompts/extraction/domain.generate.prompt.md"
        prompt_subdomain = "mms/0.2.0/prompts/extraction/subdomain.generate.prompt.md"

        runner = "mms/0.2.0/tools/run_extraction_job.py"
        persister = "mms/0.2.0/tools/persist_extraction_job.py"

        out_dir = store_dir / "out"
        out_dir.mkdir(parents=True, exist_ok=True)

        # -------------------------
        # Step 1: Domains
        # -------------------------
        domain_out = out_dir / f"job-domain-{int(time.time())}.json"

        cmd = [
            sys.executable,
            runner,
            "--prompt", prompt_domain,
            "--schema", schema_path,
            "--job-type", "domain",
            "--seed-topics", args.seed_topics,
            "--max-items", str(args.max_domains),
            "--language", args.language,
            "--model", args.model,
            "--out", str(domain_out),
        ]
        if args.strict:
            cmd.append("--strict")

        rc, out, err = run_cmd(cmd)
        sys.stdout.write(out)
        sys.stderr.write(err)
        if rc != 0:
            print("FAILED: domain extraction job failed.", file=sys.stderr)
            return 7

        cmd = [
            sys.executable,
            persister,
            "--input", str(domain_out),
            "--schema", schema_path,
            "--store", str(store_dir),
        ]
        if args.dedupe:
            cmd.append("--dedupe")

        rc, out, err = run_cmd(cmd)
        sys.stdout.write(out)
        sys.stderr.write(err)
        if rc != 0:
            print("FAILED: persisting domain job failed.", file=sys.stderr)
            return 7

        domain_doc = read_json(domain_out)
        status = domain_doc["result"]["status"]
        if status != "ok":
            print(f"STOP: domain job ended with status={status}. No subdomain jobs will run.")
            return 0

        domains = domain_doc["result"].get("items", [])
        if not isinstance(domains, list) or len(domains) == 0:
            print("STOP: no domains returned. No subdomain jobs will run.")
            return 0

        # -------------------------
        # Step 2: Subdomains per Domain
        # -------------------------
        for d in domains:
            if not isinstance(d, dict):
                continue
            dom_id = d.get("id")
            dom_title = d.get("title")
            if not isinstance(dom_id, str) or not dom_id.strip():
                continue

            sub_out = out_dir / f"job-subdomain-{dom_id.replace(':', '_')}-{int(time.time())}.json"

            cmd = [
                sys.executable,
                runner,
                "--prompt", prompt_subdomain,
                "--schema", schema_path,
                "--job-type", "subdomain",
                "--max-items", str(args.max_subdomains),
                "--language", args.language,
                "--model", args.model,
                "--parent-domain-id", dom_id,
                "--parent-domain-title", safe_title(dom_title),
                "--out", str(sub_out),
            ]
            if args.strict:
                cmd.append("--strict")

            rc, out, err = run_cmd(cmd)
            sys.stdout.write(out)
            sys.stderr.write(err)
            if rc != 0:
                print(f"FAILED: subdomain extraction failed for {dom_id}", file=sys.stderr)
                return 7

            cmd = [
                sys.executable,
                persister,
                "--input", str(sub_out),
                "--schema", schema_path,
                "--store", str(store_dir),
            ]
            if args.dedupe:
                cmd.append("--dedupe")

            rc, out, err = run_cmd(cmd)
            sys.stdout.write(out)
            sys.stderr.write(err)
            if rc != 0:
                print(f"FAILED: persisting subdomain job failed for {dom_id}", file=sys.stderr)
                return 7

        print("OK: completed chain (domain -> subdomain).")
        print("Next: add problem_area, atomic_problem, problem_detail job types with the same pattern.")
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())

