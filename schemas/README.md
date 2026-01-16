# MMS Schemas

**Status:** Draft  
**Target version:** 0.2.2  
**Schema version:** v0.1  
**Scope:** Canonical, kernel-bound  
**Role:** Machine-readable enforcement of the MMS kernel contract

---

## Purpose of This Directory

This directory contains the **canonical JSON Schemas**
used by the **Matrix Management System (MMS)**.

The schemas define:
- the machine-readable structure of MMS artifacts
- mandatory fields and invariants
- explicit guardrails against silent semantic drift

They are the **technical enforcement layer**
of the MMS kernel contract.

---

### Clarification — Schemas as Enforcement, Not Interpretation

Schemas enforce **structural admissibility only**.
They do not interpret, evaluate, or prioritize content.

Any attempt to read epistemic meaning into schema validation
is a category error.

---

## Relationship to the Architecture

The schemas are **derived mechanically** from:

- `docs/10_kernel-contract.md`
- `docs/20_logical-process.md`
- `docs/30_profiles-and-modes.md`
- `docs/35_matrix-identity-and-versioning.md`
- `runs/README.md`

They do **not** introduce new semantics.

If a rule is not present in the kernel or process documents,
it must not appear in the schemas.

---

### Architectural Note — One-Way Dependency

Architecture → Schemas is a one-way dependency.

Schemas may never:
- add constraints not justified by architecture
- encode convenience assumptions
- compensate for tooling weaknesses

If schemas appear to “decide” something,
the architecture must be revisited instead.

---

## Canonical Schemas (v0.1)

The following schemas are canonical in version v0.1:

- `claim.schema.json`  
  Defines canonical **Claim** records (epistemic atoms)

- `relation.schema.json`  
  Defines **Relations** between claims (structure, not resolution)

- `conflict.schema.json`  
  Defines **Conflicts** as first-class epistemic objects

- `run-manifest.schema.json`  
  Defines **Runs** as transactional and audit units

- `log-entry.schema.json`  
  Defines **Log Entries** as append-only operational events
  forming the audit trail of a run

Together, these schemas define the **minimum MMS contract**
that all implementations must satisfy.

---

### Clarification — Minimum Means Minimum

“Minimum” means:
- no convenience fields
- no inferred defaults
- no redundancy for tooling ease

Any extension must be justified explicitly.

---

## Design Philosophy

The schemas follow these principles:

- **minimal but binding**
- **explicit over implicit**
- **append-only by design**
- **conflict-capable**
- **audit-first**

They intentionally avoid:
- truth semantics
- scoring or ranking fields
- implicit defaults
- ontology enforcement

---

### Explicit Boundary — No Semantic Fields

Schemas must not include fields whose only purpose is to:
- imply correctness
- encode likelihood
- suggest importance
- collapse disagreement

Such fields introduce hidden epistemic authority.

---

## Schema Versioning Rules

Schema versions are independent of MMS release versions.

### Patch Changes (v0.1.x)

Allowed:
- clarification of descriptions
- bug fixes in constraints
- tightening validation where no valid artifacts are broken

Not allowed:
- adding new required fields
- changing semantics of existing fields

---

### Clarification — Patch Strictness

If there is doubt whether a change breaks an artifact,
it is not a patch change.

---

### Minor Changes (v0.2)

Allowed:
- adding new **optional** fields
- extending enums conservatively
- adding new artifact schemas

Not allowed:
- breaking existing valid artifacts

---

### Major Changes (v1.0)

Required when:
- required fields change
- claim identity rules change
- conflict semantics change
- run identity or append-only rules change

Major schema changes imply:
- a new MMS kernel contract version
- potentially a new Matrix instantiation

---

### Architectural Note — Major Change Cost

Major schema changes are intentionally expensive.
They signal epistemic or structural shifts,
not routine evolution.

---

## Schemas and Modes

Schemas enforce **profile permissions indirectly**:

- **Producer modes**
  - may create artifacts conforming to `claim.schema.json`
- **Enricher modes**
  - may create artifacts conforming to `relation.schema.json` and `conflict.schema.json`
- **Translator modes**
  - may produce artifacts under a different schema version
  - must never overwrite canonical artifacts

Schemas do not encode *who* produced an artifact,
but they encode *what is structurally allowed*.

---

### Clarification — Indirect Enforcement Only

Schemas do not replace:
- profiles
- runs
- audits

They support them structurally.

---

## Schemas and Validation

Schemas are intended to be used by:

- validators (e.g. Python, CI checks)
- run orchestration tools
- audit and QA pipelines
- automation systems

A valid MMS artifact MUST:
- conform to its schema
- reference a valid run
- respect append-only semantics

Log artifacts are optional.
If present, each log entry MUST validate against
`log-entry.schema.json`.

Artifacts that fail validation:
- must be rejected explicitly
- must not be silently corrected

---

### Explicit Boundary — No Auto-Correction

Automatic “fix-up” of invalid artifacts
is forbidden.

Correction requires:
- a new run
- explicit documentation
- preserved failure history

---

## What Schemas Do Not Guarantee

Schemas alone do NOT guarantee:

- epistemic quality
- correctness of extraction
- completeness of coverage
- absence of contradictions

Schemas guarantee **structural legitimacy only**.

Epistemic evaluation remains external.

---

## Relationship to the Matrix

Schemas define the **shape of Matrix artifacts**,
not their interpretation.

Multiple Matrix versions or instantiations
may share the same schema version.

Identity is defined by:
- claim identities
- relations
- conflicts

Not by schema version alone.

---

### Clarification — Schema Stability vs. Matrix Evolution

The Matrix may evolve rapidly
while schemas remain stable.
This asymmetry is intentional.

---

## Summary

The MMS schemas:

- are the executable form of the kernel contract
- make MMS DBMS-like in practice
- prevent silent divergence
- enable automation without authority
- ensure long-term auditability

They are intentionally conservative.

Change them slowly.

