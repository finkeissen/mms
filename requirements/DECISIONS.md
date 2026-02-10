# MMS – Normative Decisions (PUBLIC)

This document records the **explicit, normative decisions**
of the **Matrix Management System (MMS)**.

It answers the question:

> **Which fundamental decisions were made deliberately — and are binding?**

This document is part of the **public contract**.

---

## Purpose of This Document

This document exists to:

- make foundational architectural and system decisions explicit,
- prevent implicit or accidental re-decisions,
- serve as a binding reference for implementations, reviews, and audits,
- enable controlled evolution without semantic drift.

This document lists **decisions**, not options, proposals, or TODOs.

---

## Normative Status

Unless explicitly stated otherwise, all decisions in this document are:

- **normative**
- **binding**
- **precedent-setting**

In case of conflict, precedence is defined in `requirements/ARCHITECTURE.md`.

---

## Decision Format

Each decision follows this structure:

- **Decision** – what is binding
- **Rationale** – why this decision was made
- **Consequence** – what follows (including explicit exclusions)

---

## D-001: Append-Only as a Non-Negotiable Semantic

**Decision**  
All canonical artifacts are append-only.

**Rationale**  
Epistemic traceability requires a complete and immutable history.

**Consequence**  
- No updates, deletions, or silent corrections
- Revisions are new artifacts
- History remains auditable and reproducible

---

## D-002: Run Origin as the Only Entry Point

**Decision**  
Every canonical artifact must originate from exactly one run.

**Rationale**  
Responsibility, attribution, and auditability require an atomic origin.

**Consequence**  
- Manual artifact creation is forbidden
- Tooling and automation are bound to runs
- “No run → no artifact”

---

## D-003: No Implicit Decisions in the System

**Decision**  
MMS makes no silent or implicit decisions.

**Rationale**  
Implicit decisions are not auditable and leak authority.

**Consequence**  
- No automatic conflict resolution
- No prioritization or ranking
- No default interpretations
- STOP instead of “best effort”

---

## D-004: Conflict Is a Canonical State

**Decision**  
Conflicts are valid, persistent artifacts.

**Rationale**  
Contradiction is a stable condition in epistemic systems.

**Consequence**  
- Conflicts are stored explicitly
- Conflicts may persist indefinitely
- Conflict-free states must not be assumed

---

## D-005: STOP Is a Correct Outcome

**Decision**  
STOP is a valid and expected run outcome.

**Rationale**  
Not every request is structurally or normatively admissible.

**Consequence**  
- STOP produces no artifacts
- STOP requires no fallback answer
- STOP preserves system integrity

---

## D-006: Separation of Structure and Meaning

**Decision**  
MMS manages structure, not meaning.

**Rationale**  
Meaning, evaluation, and truth are context- and actor-dependent.

**Consequence**  
- Schemas describe form, not semantics
- The kernel contains no heuristics
- Interpretation is always external

---

## D-007: Tools Have No Authority

**Decision**  
External systems are tools, not decision-makers.

**Rationale**  
Authority must not be delegated implicitly.

**Consequence**  
- Tools operate only within explicit runs
- Tool outputs are artifacts, not decisions
- No tool may bypass kernel rules

---

## D-008: Derived Artifacts Are Not Canonical

**Decision**  
Derived structures are technical, not epistemic.

**Rationale**  
Canonicity requires stability, provenance, and append-only origin.

**Consequence**  
- Indices, views, and mirrors are discardable
- They contain no knowledge
- The system remains valid without them

---

## D-009: Public Contract Before Implementation

**Decision**  
Contracts are public; implementations are internal.

**Rationale**  
Stable expectations require explicit, publicly inspectable contracts.

**Consequence**  
- `requirements/` is PUBLIC and binding
- `gateway/` is NON-PUBLIC and replaceable
- Implementations must not extend contracts

---

## D-010: Architecture Changes Require Explicit Decisions

**Decision**  
Architecture may change only through explicit, documented decisions.

**Rationale**  
Undocumented changes are implicit decisions.

**Consequence**  
- New invariants must be recorded
- Prohibitions must not be silently weakened
- When in doubt, STOP applies

---

## Non-Decisions (Intentionally Open)

The following topics are **explicitly not decided**:

- truth or correctness of artifacts,
- prioritization of competing claims,
- product or UI logic,
- user guidance or decision support,
- optimization goals beyond structural integrity.

This openness is **part of the system design**.

---

## Relationship to Other Normative Documents

- `ARCHITECTURE.md` defines **invariants**
- `RESPONSIBILITIES.md` defines **scope and obligations**
- this document defines **deliberate commitments**

All three are required for a complete understanding of the MMS contract.

---

## Summary

- All core system decisions are explicitly documented
- There are no implicit architectural assumptions
- Implementations are bound by these decisions
- Changes require deliberate, traceable additions

---

_End of normative decisions._
