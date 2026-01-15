# Mapping: Producer Output → `mms.claim.v0.1`

This document maps the producer’s extracted candidate fields to the canonical
claim record schema.

Target schema:
- `schemas/claim.schema.json` (`mms.claim.v0.1`)

---

## Candidate → Canonical Field Mapping

### Required Fields

- `claim_id`
  - created at acceptance time (Stage 3)
  - stable identity, never rewritten

- `run_id`
  - from run manifest

- `assertion.text`
  - extracted assertion text (atomic claim)

- `provenance.sources[].source_id`
  - from manifest input source snapshot id

- `provenance.sources[].locator`
  - pointer into the frozen source (page/section/offset)

- `context.scope`
  - extracted or minimal scope (“as stated in source excerpt”)

- `temporal.asserted_at`
  - run time or source-provided time if explicit

- `status`
  - default `ASSERTED` for accepted claims
  - do not encode truth; conflicts are handled separately

- `created_at`
  - record creation time

---

## Acceptance Rule

A candidate becomes a canonical claim only after passing Stage 3 (Kernel Gate):
- schema validation
- provenance completeness
- scope present
- no silent merges/splits

