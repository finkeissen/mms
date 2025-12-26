# MMS Extraction Job Contract
## Domain → Subdomain → Problem Area → Atomic Problem → Problem Detail

**Version:** 0.1  
**Scope:** MMS 0.2.x extraction pipeline  
**Authority:** None (system contract, not epistemic truth)

---

## 1. Purpose

This contract defines a single, stable “job” interface for extracting structured
domain artifacts from an LLM in a reproducible and auditable way.

It exists to ensure:
- strict JSON-only outputs
- schema-validation compatibility
- traceability (provenance)
- deterministic hierarchy (parent/child)
- STOP as a valid outcome

---

## 2. The Five Levels (Canonical)

MMS extraction supports exactly five canonical levels:

1. **domain**
2. **subdomain**
3. **problem_area**
4. **atomic_problem**
5. **problem_detail**

Each level is represented as artifacts in an explicit parent/child tree.

No additional levels may be introduced without versioning this contract.

---

## 3. Artifact Identity and Hierarchy

### 3.1 IDs
Every artifact must have a stable, deterministic identifier:

- `id`: string, unique within its level namespace
- `parent_id`: string, required for levels 2–5

IDs must be stable under re-runs when inputs are identical.

### 3.2 Recommended ID Scheme (deterministic)
- `domain`: `dom::<slug>`
- `subdomain`: `sub::<domain_slug>::<slug>`
- `problem_area`: `area::<subdomain_slug>::<slug>`
- `atomic_problem`: `ap::<area_slug>::<slug>`
- `problem_detail`: `pd::<atomic_problem_slug>::<slug>`

Slugs are lowercase, ASCII, `a-z0-9-`, no spaces.

---

## 4. Provenance (Minimum Required)

Every artifact produced by an extraction job must include provenance fields:

- `provenance.run_id` (unique per MMS run)
- `provenance.model` (e.g. gpt-*)
- `provenance.prompt_id` (identifier of the prompt template)
- `provenance.created_at` (ISO 8601)
- `provenance.input_hash` (hash of canonicalized input)

MMS may add additional system-level provenance, but must not delete these fields.

---

## 5. Output Mode: JSON Only

The LLM output for every job must be:
- valid JSON
- no prose
- no markdown
- no trailing commentary

If output is invalid JSON, the job must enter “repair mode” (see §9).

---

## 6. Canonical Output Shape (Job Result)

Every job returns exactly one JSON object of this shape:

```json
{
  "job": {
    "job_id": "string",
    "job_type": "domain|subdomain|problem_area|atomic_problem|problem_detail",
    "version": "0.1",
    "inputs": {},
    "constraints": {}
  },
  "result": {
    "status": "ok|stop|error",
    "items": [],
    "stop_reason": null,
    "errors": []
  },
  "provenance": {
    "run_id": "string",
    "model": "string",
    "prompt_id": "string",
    "created_at": "string",
    "input_hash": "string"
  }
}

