# MMS ↔ Research Program (0.3)
## Relationship & Compatibility Contract

This document defines the **strict relationship** between:

- `research-program/0.3` (epistemic research with domain connectors)
- `mms/0.1.5` (operational system for processing artifacts)

Its purpose is to prevent **implicit authority**, **semantic drift**, and
**accidental coupling** between research and system layers.

---

## 1. Separation of Roles

### Research Program (0.3)

The research program:

- produces **research artifacts**, not truth and not decisions
- defines assumptions, boundaries, domain interfaces, translations, and STOP conditions
- remains **non-authoritative** by design

Artifacts produced here are conditional, scoped, and revisable.

---

### MMS (0.1.5)

MMS:

- processes, stores, transforms, validates, and exports artifacts
- executes pipelines and system-level workflows
- remains **non-epistemic**

MMS does not become an authority by executing workflows.

---

## 2. Non-Authority Rule (Hard Constraint)

MMS must never claim:

- truth
- correctness
- legitimacy
- recommendation
- decision authority

MMS outputs are:

- system outputs
- computed transformations
- validations against schemas
- traceable derivations

They are not:

- answers
- verdicts
- advice
- judgments

Any decision-like structure must be explicitly modeled as:
- constraints
- classifications
- conflict sets
- STOP outcomes

---

## 3. Explicit Handover Only

MMS may consume artifacts from the research program **only** via explicit handover.

This requires:

- explicit artifact files
- explicit schema compatibility
- explicit provenance references
- explicit domain connector identity

There is no implicit import of:

- assumptions
- definitions
- boundaries
- normativity

If something is not explicit in an artifact, it does not exist for MMS.

---

## 4. Provenance and Traceability

Any artifact ingested by MMS that originates from the research program must preserve:

- source reference
- commit or version identifier (if available)
- creation or ingestion timestamp
- domain identity (e.g. `legal-law`, `medicine`)

MMS may enrich provenance with system-level metadata, but must not overwrite
research provenance.

---

## 5. STOP Is a First-Class Outcome

STOP is a valid and expected outcome.

STOP may result from:

- missing scope
- missing jurisdiction or domain context
- missing evidence
- unresolved conflict
- undecidability

MMS must preserve STOP artifacts and their explanations.
STOP must not be repaired or bypassed by guessing.

---

## 6. Domain Connectors Are Contracts, Not Plugins

Domain connectors defined in `research-program/0.3/domains/*` specify:

- what a domain provides
- what it refuses
- its primitives, boundaries, and translations

For MMS, these act as:

- interpretive contracts
- validation constraints
- documentation for safe processing

They are not:

- executable authority modules
- automated decision engines
- global ontologies

---

## 7. Integrated Views and World Models (Not Yet)

A more integrated, cross-domain view of the world may be constructed in MMS
in the future.

If this occurs, it must satisfy:

- integration is explicit, versioned, and reversible
- conflicts remain representable
- domain boundaries remain visible
- no epistemic authority is claimed
- research artifacts remain the auditable substrate

This is **not** a requirement for MMS/0.1.5 and must not be implied by current documentation.

---

## 8. Compatibility Summary

MMS/0.1.5 is compatible with research-program/0.3 if and only if:

- artifacts are treated as artifacts
- provenance is preserved
- STOP is preserved
- domain contracts remain explicit
- no authority is asserted

Any MMS feature that violates these constraints constitutes
a design error and must be corrected at the contract or documentation level
before implementation changes.

