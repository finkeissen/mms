# MMS 0.4.0
## JSONL Output Specification & Reproducible Artifact Records

**Version:** 0.4.0 (work-in-progress spec)  
**Status:** System artifact output layer (Experimental)  
**Authority:** None

---

### Goal of 0.4.0
0.4.0 defines how MMS represents imported artifacts as **machine-readable, append-only JSONL records**.

This is *not* a claim of truth. JSONL is only a durable representation of system-scoped artifacts, including:
- provenance
- stated assumptions/limits
- STOP/UNKNOWN/CONFLICT status

0.4.0 builds on 0.3.0:
- 0.3.0 defines the **handover entry contract**
- 0.4.0 defines the **stable output format**

---

### Output primitives
Each line in a JSONL file is a single `artifact_record` object.

Minimum guarantees:
1) **Traceability:** every record points back to a specific handover manifest and artifact entry.
2) **Reproducibility:** given the same handover + same normalization rules, record ids are stable.
3) **Fail-closed:** STOP/UNKNOWN/CONFLICT are preserved and never auto-repaired.

---

### Files
- `jsonl/record.schema.json` — JSON Schema for one JSONL line (one record)
- `jsonl/record.example.json` — single-record example (JSON)

---

### Record identity
`record_id` must be deterministic.

Recommended (normative for MMS output, not epistemic):
- Compute `record_id` as `sha256(canonical_json(provenance) + "\n" + canonical_json(payload))`.
- Canonical JSON means: UTF-8, sorted keys, no insignificant whitespace.

---

### Non-goals
0.4.0 does *not* specify:
- how artifacts are interpreted semantically
- how conflicts are resolved
- how decisions are justified

Those remain external (research-program, governance, humans).
