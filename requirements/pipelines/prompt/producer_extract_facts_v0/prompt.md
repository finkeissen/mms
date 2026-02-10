# Prompt: Extract Facts / Claims (v0)

**Profile:** PRODUCER  
**Stage:** 2 (Candidate Extraction)  
**Goal:** Produce candidate claims with explicit provenance and scope, without truth judgments.

---

## Instructions (for the model)

You will be given:
- a source excerpt (from a frozen snapshot)
- optional context/scope

Your task:
- extract atomic claims as explicit assertions
- do not evaluate truth
- do not resolve contradictions
- keep competing/alternative statements as separate claims

Output format:
- a list of candidate claims, each with:
  - assertion text
  - brief scope/context
  - source pointer (locator)
  - temporal binding (if stated; otherwise omit)

Forbidden:
- scoring, ranking, “most likely”
- harmonizing contradictions
- removing alternatives

---

## Notes

This prompt is conceptually inspired by the historical pilot prompt:
`modes/0.5.0 … (LLM-pilot)/pilot/prompts/extract-facts.v0.2.md`
but must remain contract-aligned with:
- `docs/10_kernel-contract.md`
- `docs/20_logical-process.md`
- `docs/30_profiles-and-modes.md`

