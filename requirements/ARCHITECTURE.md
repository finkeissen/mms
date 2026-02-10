# MMS Architecture (PUBLIC, Normative)

This document defines the **normative architectural invariants**
of the **Matrix Management System (MMS)**.

It answers the question:

> **What must never change — regardless of implementation, technology, or productization?**

This document is **authoritative**.
In case of conflict, the following precedence applies:

1. `requirements/ARCHITECTURE.md`
2. `requirements/RESPONSIBILITIES.md`
3. other documents in `requirements/`
4. implementations in `gateway/`

---

## Architectural Scope

MMS is an infrastructure for managing **epistemic artifacts**
under conditions of:

- incompleteness
- contradiction
- alternative interpretations
- long-term revision and auditability

MMS is **not** a:
- reasoning system
- truth system
- expert system
- decision or recommendation system

MMS provides **structure, identity, and history**.
Meaning, evaluation, and decisions are always external.

---

## Architecture vs. Implementation

This document defines **architectural invariants**, not implementations.

- programming languages
- storage systems
- tools
- runtime models

may change **as long as the invariants defined here are preserved**.

---

## Normative vs. Explanatory Content

This document contains two kinds of content:

- **Normative invariants** (binding, enforceable)
- **Explanatory rationale and warning signals** (non-exhaustive, guiding)

Unless explicitly stated otherwise, all rules in this document
are **normative**.

Rationale and warning sections exist to:
- make violations detectable,
- prevent authority leakage,
- preserve epistemic integrity over time.

---

## Core Architectural Invariants

The following invariants are **non-negotiable**.

---

### 1. Append-Only Semantics (Normative)

All **canonical artifacts** are append-only.

- no artifact is deleted
- no artifact is overwritten
- revisions are new artifacts
- history is complete and inspectable

There is no “update in place”.

**Rationale:**  
Append-only semantics are a prerequisite for epistemic traceability.

---

### 2. Explicit Origin (Runs) (Normative)

Every canonical artifact originates from **exactly one run**.

- no run → no artifact
- manual injection is forbidden
- runs are immutable
- runs are the atomic audit unit

Runs are the only permitted transition
from processing to canonical state.

---

### 3. Explicit Structure (Schemas) (Normative)

All canonical artifacts are **schema-bound**.

- schemas are explicit and versioned
- validation is strict
- invalid artifacts are rejected
- schemas describe **form**, not meaning

Schemas must **not enforce semantics**.

---

### 4. No Implicit Decisions (Normative)

MMS makes **no silent decisions**.

In particular, MMS does not:
- resolve conflicts
- prioritize artifacts
- determine truth
- collapse uncertainty
- apply default interpretations

If a decision exists,
it must be explicit, attributable, and historically reversible.

---

### 5. Conflict as a First-Class Artifact (Normative)

Conflicts are **canonical artifacts**.

- conflicts are not errors
- conflicts may persist indefinitely
- conflicts are never resolved automatically
- conflict-freedom must not be assumed

---

## Separation of Responsibilities

### Kernel (Normative)

The kernel:

- enforces invariants
- validates schemas
- protects append-only semantics
- contains **no semantics**
- contains **no heuristics**

The kernel is intentionally minimal
and acts as a **firewall against implicit authority**.

---

### Processes (Normative)

Processes:

- define permitted sequences of runs
- encode staging and abort conditions
- orchestrate, but **do not decide**

A process may end in STOP or Failure
without producing artifacts.

---

### Profiles (Normative)

Profiles define **permissions**, not authority.

- who may execute which runs
- who may add which structures

No profile may create epistemic priority.

---

### Tools (Normative)

Tools are external.

- they operate only through explicit runs
- they are replaceable
- they must not bypass the kernel

Automation is optional, never implicit.

---

## Derived Artifacts (Normative)

Derived structures (indices, views, projections):

- are not canonical
- contain no knowledge
- may be deleted at any time
- must be reproducible

The system remains valid without them.

---

## Identity & Integrity (Normative)

Artifacts have explicit identities.

- no implicit identity
- identity is stable over time
- reorganization does not change identity

Hashes guarantee:
- integrity
- reproducibility
- auditability

Hashes **do not imply authority**.

---

## STOP as an Architectural Anchor (Normative)

STOP is a **correct and expected architectural outcome**.

STOP occurs when:
- structural admissibility is violated
- implicit authority would be introduced
- high-stakes requirements are requested

STOP:
- produces no artifacts
- requires no “fallback answer”
- preserves system integrity

---

## Enrichment (Non-Authoritative Additions)

Enrichments may:
- compare
- diagnose differences
- mark gaps
- document experience

Enrichments must **not**:
- assert truth
- resolve conflicts
- overwrite artifacts
- imply authority

---

## Evolution (Normative)

Architecture may evolve only under these rules:

- invariants may only be **tightened**, never loosened
- history must remain interpretable
- clarity takes precedence over backward compatibility

Breaking history is worse than breaking APIs.

---

## Architectural Prohibitions (Hard Rules)

The following changes are **forbidden**:

- in-place updates of canonical artifacts
- artifacts without run origin
- implicit conflict resolution
- ranking or scoring in the kernel
- default interpretations
- tool bypasses of the kernel
- treating derived artifacts as canonical
- hiding or smoothing uncertainty

When in doubt: **STOP**.

---

## Audit Triggers (Warning Signals, Non-Exhaustive)

The following statements are **warning signals**.
They indicate a high risk of architectural violation:

- “Let’s just fix this directly.”
- “We’ll take the best source.”
- “We can merge this automatically.”
- “This is probably just noise.”
- “The model decided.”

These are not opinions,
but indicators of impending authority leakage.

---

## Summary

MMS is an architecture for:

- explicit structure
- auditable history
- reproducibility
- conflict tolerance
- long-term epistemic integrity

Any change that weakens these properties
is architecturally invalid.
