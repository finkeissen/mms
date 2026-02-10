# tools/

This directory contains small, human-readable tooling for MMS.

Current tools:

- `validate_run.py`
  - validates a flat run directory against the canonical schemas in `schemas/`
  - validates:
    - `manifest.json` (run-manifest schema)
    - JSONL artifacts referenced in the manifest (`claims`, `relations`, `conflicts`)

Design goals:
- minimal dependencies
- clear error messages
- deterministic behavior
- no implicit fixes ("fail loud")

---

## Usage

From repo root:

```bash
python tools/validate_run.py runs/examples/run_2026-01-15T10-00-00Z_producer_extract_facts_v0
python tools/validate_run.py runs/examples/run_2026-01-15T10-05-00Z_enricher_link_and_conflict_v0

