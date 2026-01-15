#!/usr/bin/env python3
# MMS 0.5.0 — Matrix Export (Demo)

import argparse, json, sys
from pathlib import Path
from collections import defaultdict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--problem-id", default=None)
    args = ap.parse_args()

    rows = defaultdict(lambda: {"by_source": defaultdict(list)})
    with Path(args.facts).open("r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if args.problem_id and r.get("problem_id") != args.problem_id:
                continue
            key = r.get("problem_id","_")
            src = r["source"]["source_id"]
            rows[key]["by_source"][src].append({
                "record_id": r["record_id"],
                "claim": r["claim"]["text"],
                "language": r["claim"]["language"],
                "status": r["status"]
            })

    out = []
    for pid, data in rows.items():
        out.append({
            "record_type": "mms.matrix_row",
            "problem_id": pid,
            "by_source": data["by_source"]
        })

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())

