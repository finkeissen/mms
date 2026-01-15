# Stage-to-Artifacts Mapping  
(Logical Process → Schemas)

**Status:** Draft  
**Target version:** 0.2.2  
**Scope:** Operative mapping, schema-derivable  
**Role:** Defines which logical process stage produces which artifact class and schema

---

## Purpose of This Document

This document maps the **logical process stages** defined in:

- `docs/20_logical-process.md`

to concrete **artifact classes** and **canonical schemas** defined in:

- `schemas/`

It does **not** introduce new semantics.

Its purpose is to make the MMS process:
- mechanically enforceable
- auditable
- automation-friendly
- free of implicit assumptions

---

## Canonical Artifact Types and Schemas

The MMS kernel defines exactly the following
**schema-bound canonical artifacts**:

| Artifact kind | Schema | Notes |
|---------------|--------|-------|
| Claim record | `schemas/claim.schema.json` | Canonical accepted epistemic atoms |
| Relation record | `schemas/relation.schema.json` | Structural links (no resolution) |
| Conflict record | `schemas/conflict.schema.json` | First-class incompatibilities |
| Run manifest | `schemas/run-manifest.schema.json` | Transaction and audit unit |

In addition, runs may produce **non-schema-bound artifacts**, such as:
- logs
- reports
- snapshots
- derived **views**
- derived **indices**

These artifacts are important for audit and operations,
but are **not kernel-canonical** in v0.1.

---

## Stage-to-Artifact Mapping

### Stage 0 — Run Setup (Manifest-First)

**Primary output**
- Run Manifest (`run-manifest.schema.json`)

**Additional outputs**
- configuration snapshot
- initial execution logs

**Notes**
- No processing may start without a manifest.
- STOP may occur here if inputs or configuration are missing or invalid.

---

### Stage 1 — Source Acquisition and Freezing

**Primary outputs**
- explicit input inventory
- source snapshot references (hashes, locators)

**Schema impact**
- Run Manifest MUST list frozen sources under `inputs.sources`.

**Notes**
- Claims must never reference moving targets.
- UNKNOWN or STOP may occur here.

---

### Stage 2 — Candidate Extraction (Producer Stage)

**Primary outputs**
- candidate claim records (internal or external)

**Schema impact**
- If candidates already conform to the canonical claim schema,
  they MAY be emitted directly as Claim Records.
- Otherwise, candidates remain **non-canonical artifacts**
  until validated in Stage 3.

**Notes**
- NOCLAIM, UNKNOWN, or STOP may occur here.
- v0.1 does not standardize candidate-only schemas;
  only accepted claims are canonical.

---

### Stage 3 — Canonicalization and Contract Conformance  
(Kernel Gate)

**Primary outputs**
- Claim Records (`claim.schema.json`) for accepted claims

**Additional outputs**
- rejection reports (non-schema)
- validation and normalization reports (non-schema)

**Notes**
- This stage is the conceptual **constraint gate**.
- Only claims that pass this stage enter the canonical Matrix.
- If no candidates pass: NOCLAIM.

---

### Stage 4 — Structural Linking (Enricher Stage)

**Primary outputs**
- Relation Records (`relation.schema.json`)

**Notes**
- Enrichers MUST NOT split or merge claims.
- Link candidates may exist as non-schema artifacts
  until explicitly promoted.

---

### Stage 5 — Conflict Detection and Representation  
(Enricher Stage)

**Primary outputs**
- Conflict Records (`conflict.schema.json`)

**Notes**
- Conflicts are preserved, not resolved.
- CONFLICT is a valid and expected run outcome.

---

### Stage 6 — Quality and Audit Enrichment  
(Enricher Stage)

**Primary outputs**
- audit reports (non-schema)
- coverage maps (non-schema)
- QA markers

**Schema impact**
- QA markers may be embedded as optional fields
  in future schema versions.
- v0.1 treats them as non-schema artifacts.

**Notes**
- This stage is strictly additive.
- Claim identity must never change.

---

### Stage 7 — Publication (Matrix Assembly)

**Primary outputs**
- exports
- derived views (optional)
- derived indices (optional)

**Schema impact**
- Publication does NOT define Matrix identity.
- Manifests MUST list publication outputs
  under `outputs.artifacts`.

**Notes**
- **Views** are derived presentation/query artifacts.
- **Indices** are derived access/acceleration artifacts.
- Both are optional, deletable, and rebuildable.
- Neither adds epistemic content or resolves conflicts.

---

## Translator Branch (Exceptional)

Translator runs form an **explicit branch**
outside the default pipeline.

Translator runs may produce:
- claims, relations, and conflicts
  under an **alternative Matrix instantiation**
- possibly using different schema versions

Translator usage MUST be explicit in the run manifest.

At minimum, a translator run MUST:
- declare itself as translator-run (explicit flag or profile classification)
- reference the source Matrix instantiation (or source run lineage)
- ensure outputs are not silently merged into canonical runs

Recommended (non-binding) manifest fields include:
- a translator classification flag
- a source matrix identifier
- a list of source run ids

The exact field names are schema-defined and may evolve,
but the requirement of **explicit declaration** is invariant.

---

## Summary

This stage-to-artifact mapping ensures that:

- every canonical artifact has a defined origin stage
- schema validation can be applied mechanically
- automation can reason about run structure and outcomes
- semantic drift is prevented by explicit stage boundaries

The mapping is descriptive and enforceable,
not interpretive.

