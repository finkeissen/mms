# MMS Kernel Contract

**Status:** Draft  
**Target version:** 0.2.2  
**Scope:** Canonical, implementation-independent  
**Role:** Normative contract for all MMS components

---

## Purpose of This Document

This document defines the **canonical kernel contract** of the
**Matrix Management System (MMS)**.

It specifies:
- the **core epistemic entities** managed by MMS
- their **roles and boundaries**
- the **invariants** that apply regardless of implementation
- the **minimum semantics** required for interoperability

This document is:
- **normative** for MMS
- **independent** of prompts, models, or programming languages
- **binding** for all producer, enricher, and translator modes

This document does **not**:
- define truth or validity
- prescribe extraction methods
- specify storage backends
- implement pipelines
- define access paths or indices

---

## Architectural Position

The MMS kernel occupies a role analogous to a **DBMS kernel**.

In particular, the kernel:
- defines **canonical entity types**
- defines **schemas and invariants**
- enforces **append-only semantics**
- guarantees **explicit provenance**
- ensures **auditability and reproducibility**

The kernel is **passive**:
- it does not interpret meaning
- it does not evaluate correctness
- it does not optimize access

All higher-level behavior
(pipelines, prompts, automation, orchestration, views)
operates **against this contract**, never inside it.

---

## Canonical Entities

The MMS kernel manages exactly four canonical entity types:

1. **Claim**
2. **Relation**
3. **Conflict**
4. **Run**

No other entity type has kernel status.

Additional structures may exist,
but must reduce to or reference these entities explicitly.

---

## 1. Claim

### Definition

A **Claim** is an explicit, attributable assertion
about some aspect of the world.

A claim is:
- not a fact
- not validated truth
- not authoritative
- potentially false, incomplete, or contradictory

Claims are the **atomic epistemic units** of MMS.

---

### Minimal Semantic Properties

Every claim MUST have:

- **Assertion**
  - the propositional content of the claim
- **Provenance**
  - who or what asserts it, and via which run
- **Context / Scope**
  - under which assumptions or conditions it applies
- **Temporal Binding**
  - when it was asserted or considered applicable
- **Claim Status Marker**
  - a *claim-level* marker describing the claim’s epistemic posture (not a run outcome)

Claims MUST NOT:
- encode truth judgments
- encode confidence or probability as validity
- collapse disagreement or alternatives

**Note (important):**  
Run-level outcomes such as `STOP`, `UNKNOWN`, `NOCLAIM`, `CONFLICT`, `SUCCESS`
belong to **Run** records. They are not claim-level truth semantics.

---

### Identity and Stability

- Claims have **stable identities** once created.
- Claims are **append-only**.
- Claims MUST NOT be silently modified, split, or merged.

If a claim must be reinterpreted, revised, or challenged:
- a **new claim** is created
- relations and/or conflicts are added to express the change

Identity guarantees are structural, not epistemic.

---

## 2. Relation

### Definition

A **Relation** is an explicit, typed structural link
between two or more claims.

Relations express **structure**, not resolution.

---

### Examples (Non-Exhaustive)

- supports
- contradicts
- refines
- generalizes
- specializes
- is-derived-from
- is-alternative-to

---

### Properties

Relations MUST:
- reference existing claims
- be explicitly typed
- carry provenance
- be time-bound where applicable

Relations MUST NOT:
- resolve conflicts
- imply correctness or truth
- collapse competing claims

---

## 3. Conflict

### Definition

A **Conflict** represents an explicit recognition
that two or more claims are incompatible
under a defined context or scope.

Conflict is a **first-class epistemic object**.

---

### Properties

Conflicts:
- do not decide which claim is correct
- do not require symmetry
- may evolve over time
- may themselves be contested or superseded

A conflict MUST:
- reference the involved claims
- specify the conflict scope
- carry provenance and temporal information

---

### Design Note

Conflicts are **represented**, not resolved.

The MMS kernel guarantees that conflicts
are **preserved**, not eliminated or hidden.

---

## 4. Run

### Definition

A **Run** is a reproducible execution instance
of MMS processing.

Runs are the **transactional and audit unit** of MMS,
analogous to transactions in a DBMS.

---

### Properties

A run captures:
- input sources
- processing configuration
- execution time
- produced artifacts
- encountered failure or boundary conditions

Runs are:
- append-only
- comparable
- reproducible
- never retroactively altered

---

### Outcomes and Failure Modes

Runs may explicitly record outcomes such as:
- `SUCCESS`
- `STOP`
- `UNKNOWN`
- `NOCLAIM`
- `CONFLICT`

Outcomes are **descriptive run artifacts**, not epistemic decisions.

---

## Global Invariants

The following invariants apply system-wide:

### Append-Only
No canonical entity is overwritten or deleted.

### Provenance Required
All claims, relations, conflicts, and runs
must be explicitly attributable.

### No Truth Semantics
The kernel encodes structure and traceability,
not validity or correctness.

### Explicit Alternatives
Competing claims and approaches are preserved.

### Silent Divergence Disallowed
Any transformation that changes claim identity
must be explicit, versioned, and traceable via runs.

---

## Relationship to Modes and Pipelines

- **Producer modes** may introduce new claims
- **Enricher modes** may add structure or metadata
- **Translator modes** may create alternative representations explicitly

All modes MUST:
- operate via runs
- respect kernel invariants
- remain externally replaceable

Modes have permissions, not authority.

---

## Non-Goals (Explicit)

The MMS kernel does NOT:
- define authoritative ontologies
- provide decision support
- rank claims or sources
- optimize for consensus
- provide indexing or access strategies
- model the world

It models **epistemic structure only**.

---

## Versioning

This contract is versioned independently.

Breaking changes:
- require a major version bump
- imply a new Matrix instantiation

Non-breaking extensions:
- may add optional fields
- must preserve existing semantics and invariants

---

## Summary

The MMS kernel defines:

- **what exists**
- **what must never happen silently**
- **what remains undecidable by design**

Everything else is implementation, tooling, or interpretation.

