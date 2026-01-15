# MMS Architecture

This document defines the **normative architectural principles** of the
Matrix Management System (MMS).

It answers the question:

> *What must never change, regardless of implementation details?*

This document is authoritative.
If other documents conflict with it, this document wins.

---

## Architectural Scope

MMS is an infrastructure for managing **epistemic artifacts**
under uncertainty and disagreement.

It is **not**:
- a reasoning engine
- a truth-finding system
- an expert system
- a knowledge graph with implicit semantics

MMS provides structure, identity, and history.
Meaning and resolution are always external.

---

## Core Architectural Invariants

The following invariants are **non-negotiable**.

### 1. Append-Only Semantics

All canonical artifacts are append-only.

- Artifacts are never modified or deleted
- Corrections are new artifacts
- Revisions are explicit and historical
- History is inspectable and immutable

There is no concept of “update in place”.

---

### 2. Explicit Origin (Runs)

Every canonical artifact originates from exactly one **Run**.

- No run → no artifact
- Manual insertion is forbidden
- Runs are immutable once completed
- Runs are the atomic audit unit

Runs are the only bridge between automation and canonical state.

---

### 3. Explicit Structure (Schemas)

All canonical artifacts are schema-bound.

- Schemas are explicit and versioned
- Validation happens at the kernel boundary
- Invalid artifacts never enter the system
- Schemas describe structure, not meaning

Schema violations are structural errors, not soft warnings.

---

### 4. No Implicit Decisions

MMS never makes silent decisions.

This includes:
- conflict resolution
- claim prioritization
- truth selection
- uncertainty collapse
- default interpretation

If a decision exists, it must be:
- explicit
- inspectable
- attributable
- reversible by history

---

### 5. Conflict Is a First-Class Concept

Conflicts are not failures.

- Conflicts are explicit artifacts
- Conflicts may persist indefinitely
- Conflicts are never auto-resolved
- Conflict absence must not be assumed

Disagreement is preserved, not normalized away.

---

## Separation of Concerns

MMS enforces strict separation.

### Kernel

The kernel:
- enforces invariants
- validates schemas
- guards append-only semantics
- has no domain knowledge
- contains no heuristics

The kernel is deliberately minimal.

---

### Processes

Processes:
- define allowed sequences of runs
- encode ordering and staging
- define failure modes
- never decide truth

Processes orchestrate, they do not judge.

---

### Profiles

Profiles define permissions.

- who may create which runs
- who may add which structures
- who may transform representations

Profiles define **capability**, not authority.

---

### Tooling

Tools are external.

- tools assist humans or automation
- tools operate via explicit runs
- tools are replaceable
- tools never bypass the kernel

Automation is always optional.

---

## Identity and Integrity

### Identity

Artifacts are identified explicitly.

- no implicit identity by position or context
- identity survives reindexing and restructuring
- identity is stable across views

---

### Hashes

Hashes are mandatory for integrity.

They provide:
- immutability guarantees
- reproducibility
- auditability

Hashes do not provide trust or meaning.
They only guarantee sameness.

---

## Derived Artifacts

Indices, views, projections, summaries, rankings, and graphs are:

- derived
- optional
- non-canonical
- disposable

They may be deleted and rebuilt at any time.

The system remains valid without them.

---

## Architectural Non-Goals

The following are explicitly out of scope:

- global consistency enforcement
- automatic conflict resolution
- implicit ontology alignment
- probabilistic truth scoring
- hidden optimization layers

These may exist externally,
but never inside the MMS kernel.

---

## Evolution Rules

Architecture evolves under strict rules:

- invariants may only be tightened, never weakened
- new concepts must not introduce implicit behavior
- backward compatibility is preferred but secondary to clarity
- history must remain interpretable

Breaking history is worse than breaking APIs.

---

## Decision Record

Architectural decisions must be:

- documented
- justified
- attributable
- reviewable

Undocumented architecture does not exist.

---

## Summary

MMS is an infrastructure for **preserving epistemic structure over time**.

It optimizes for:
- explicitness
- auditability
- reversibility
- disagreement tolerance

Any change that weakens these properties
is architecturally invalid.

