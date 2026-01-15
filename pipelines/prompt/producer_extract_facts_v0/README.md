# producer_extract_facts_v0 (Prompt Producer)

**Profile:** PRODUCER  
**Primary stage:** Stage 2 — Candidate Extraction  
**Target artifacts:** Claim candidates → (after gate) canonical `mms.claim.v0.1` records  
**Status:** Draft (canonical reference producer)

---

## Purpose

This pipeline is the **canonical reference Producer** for MMS 0.2.x.

It extracts candidate claims from a frozen source snapshot using a prompt-based approach.

This is derived conceptually from the historical pilot:
- `modes/0.5.0 … (LLM-pilot)/pilot/prompts/extract-facts.v0.2.md`
but rebuilt under the new MMS kernel/process/profile model.

---

## What This Producer May Do (Producer profile)

This producer may:
- read declared frozen sources
- generate candidate claim statements
- attach extraction metadata

This producer may not:
- resolve conflicts
- rank truth or validity
- rewrite existing claims
- merge/split claim identities silently

---

## Inputs

- a frozen source snapshot (declared in the run manifest)
- a problem/context scope (optional but recommended)

---

## Outputs

This producer produces a candidate set which is passed to Stage 3 (Kernel Gate).

In early versions, the producer may directly emit schema-conforming records,
but acceptance into the canonical Matrix is defined by Stage 3.

---

## Next Steps

1. Add prompt file (`prompt.md`)
2. Add mapping file (`mapping.md`) from extracted fields → `mms.claim.v0.1`
3. Add a flat example run under `runs/examples/` using this producer

