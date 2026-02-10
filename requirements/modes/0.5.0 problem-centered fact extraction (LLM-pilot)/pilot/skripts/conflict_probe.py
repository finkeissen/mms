#!/usr/bin/env python3
# MMS 0.5.0 — Conflict Probe Runner (hardened)

from __future__ import annotations
import argparse, json, sys, time, datetime as dt
from pathlib import Path
from typing import Any, Dict, List
from providers.llm_provider import build_provider

def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00","Z")

def read_json(p: Path) -> Dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def write_json(p: Path, o: Dict[str, Any]):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")

def load_prompt(path: Path, **kv) -> str:
    t = path.read_text(encoding="utf-8")
    for k,v in kv.items():
        t = t.replace("{{"+k+"}}", v)
    return t

def call_with_retries(client, text, n, backoff):
    for i in range(n+1):
        try: return client.complete(text)
        except Exception:
            if i>=n: raise
            time.sleep(backoff[min(i, len(backoff)-1)])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--problem", required=True)
    ap.add_argument("--candidate-claim", required=True)
    ap.add_argument("--existing-claims", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-retries", type=int, default=2)
    ap.add_argument("--backoff", default="5,30")
    args = ap.parse_args()

    client = build_provider(provider=args.provider, model=args.model, temperature=args.temperature)
    problem = read_json(Path(args.problem))
    cand = read_json(Path(args.candidate_claim))
    exist = json.loads(Path(args.existing_claims).read_text(encoding="utf-8"))

    rendered = load_prompt(
        Path(args.prompt),
        PROBLEM_JSON=json.dumps(problem, ensure_ascii=False, sort_keys=True),
        CANDIDATE_CLAIM_JSON=json.dumps(cand, ensure_ascii=False),
        EXISTING_CLAIMS_JSON=json.dumps(exist, ensure_ascii=False)
    )
    backoff = [int(x) for x in args.backoff.split(",") if x.strip()]
    raw = call_with_retries(client, rendered, args.max_retries, backoff)
    out = json.loads(raw.strip())
    out["_meta"] = {"generated_at": utc_now()}
    write_json(Path(args.out), out)
    return 0

if __name__ == "__main__":
    sys.exit(main())

