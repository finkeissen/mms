# MMS 0.5.0 — Next Steps (Pilot Runs)

## Intent
In the next days we will run small/local LLM test runs to populate the knowledge base
and validate whether the current MMS design works in practice.

This is a practical validation phase for:
- problem-centered extraction
- strict JSON outputs
- record schema conformance
- fail-closed error handling
- reproducibility via prompt_hash and run logs

---

## What we will do
1) Create a small pilot set of `mms.problem` records (10–100).
2) Run extraction with small/local LLMs (LM Studio) using:
   - `pilot/scripts/run_pilot.py`
   - `pilot/prompts/extract-facts.v0.1.md`
3) Validate outputs:
   - schema validation of `facts.jsonl`
   - run-report auditing
4) Iterate only on:
   - prompts (new versions, never overwrite)
   - provider settings (model/temperature)
   - operational scripts (bugfixes + hardening)

---

## What we will NOT do (yet)
- no scaling to 100k/10M problems
- no ontology or synonym unification
- no conflict resolution
- no truth ranking / trust scoring
- no “complete matrix”

---

## Deliverables
- `pilot/outputs/facts.jsonl` (append-only; validated)
- `pilot/outputs/run-report.json` (auditable)
- `notes/lessons-learned.md` (observations + failure modes)
- optional: `pilot/outputs/matrix-demo.json` (demo export)

---

## Decision gates
After initial runs we decide:
- whether schemas hold without changes
- whether prompt contract is sufficient
- whether error handling is adequate
- what must be added for 0.6.0

---

## Working rules
- Never overwrite prompts; bump version (v0.1 → v0.2).
- Always keep `prompt_hash` and `run_id`.
- Fail closed: if unsure, produce `unknown` / write no record.
- Keep MMS core small; bulk data goes to datasets/storage later.

