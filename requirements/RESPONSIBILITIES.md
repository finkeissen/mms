# MMS – Responsibilities & Scope (PUBLIC)

This document defines the **binding responsibilities**
of the **Matrix Management System (MMS)**.

It specifies **what MMS is responsible for**, **where its responsibility ends**,
and **which tasks are explicitly outside its scope**.

This document is part of the **public contract**.

---

## Purpose of This Document

This document exists to:

- establish clear expectations for users, integrators, and operators,
- provide an explicit responsibility boundary to adjacent systems,
- prevent implicit responsibility creep,
- serve as a normative reference for architecture, security, and governance decisions.

---

## Normative Status

Unless explicitly stated otherwise, all statements in this document are
**normative and binding**.

This document is authoritative for:
- architectural decisions,
- implementation constraints,
- audit and compliance evaluation.

In case of conflict, precedence is defined in `requirements/ARCHITECTURE.md`.

---

## Primary Responsibilities of MMS

MMS is responsible for the following, and **only** the following.

---

### 1. Management of Epistemic Artifacts (Normative)

MMS is responsible for managing **canonical epistemic artifacts**, namely:

- **Claims**
- **Relations**
- **Conflicts**

For these artifacts, MMS guarantees:

- stable and explicit artifact identities,
- append-only history without silent mutation,
- immutable artifacts once created,
- explicit provenance (source, time, context),
- long-term inspectability and auditability.

---

### 2. Run-Based Processing (Normative)

MMS is responsible for executing **runs** as the only admissible unit of processing.

Normative guarantees:

- every artifact originates from exactly one run,
- runs are atomic and explicitly bounded,
- runs are fully traceable and reproducible,
- runs may terminate in:
  - successful artifact creation,
  - **STOP**,
  - **NOCLAIM**.

STOP and NOCLAIM are **correct and expected outcomes**, not errors.

---

### 3. Structured Accessibility (Gateway Responsibility) (Normative)

MMS is responsible for providing **technical accessibility** to artifacts via
non-canonical projections.

This includes:

- snapshots,
- mirrors,
- indices,
- other technical views.

Normative constraints:

- canonical artifacts remain read-only,
- projections introduce no new information,
- projections are discardable and reproducible,
- projections must never be treated as authoritative.

---

### 4. Enforcement of System Invariants (Normative)

MMS is responsible for enforcing all architectural invariants, including:

- strict append-only semantics,
- read-only protection of existing artifacts,
- explicit error handling,
- explicit STOP handling,
- explicit absence handling (NOCLAIM),
- prohibition of implicit defaults or silent decisions.

---

### 5. Auditability & Verifiability (Normative)

MMS is responsible for ensuring that:

- every run and artifact is auditable,
- all guarantees are technically verifiable,
- no hidden processing or “black box” behavior exists at the gateway level.

---

## Explicit Non-Responsibilities (Normative)

MMS explicitly **does not** take responsibility for:

- evaluating, ranking, or weighting content,
- determining truth, relevance, or correctness,
- automatically resolving conflicts,
- making recommendations or decisions,
- providing guidance, advice, or action instructions,
- semantic interpretation of artifacts,
- harmonizing contradictory content,
- deriving authority from sources, status, or frequency,
- hiding, smoothing, or collapsing uncertainty,
- product logic or user-facing decision-making.

Any task that requires interpretation, prioritization,
or normative judgment is **outside the scope of MMS**.

---

## Relationship to Adjacent Systems (Normative)

- MMS is **not a knowledge base**,
  but infrastructure for managing epistemic artifacts.
- MMS does **not replace decision, reasoning, or recommendation systems**.
- MMS does **not delegate responsibility** to external systems.

External systems may only be used as **tools**
within explicitly bounded runs
and must not introduce authority.

---

## Responsibility Boundary (Explicit Cut)

| Task | MMS |
|------|-----|
| Store canonical artifacts | ✔ |
| Manage provenance | ✔ |
| Maintain append-only history | ✔ |
| Execute runs reproducibly | ✔ |
| Represent conflicts explicitly | ✔ |
| Generate technical projections | ✔ |
| Determine truth | ✖ |
| Resolve conflicts | ✖ |
| Evaluate or rank content | ✖ |
| Make decisions | ✖ |
| Give recommendations | ✖ |

---

## Binding Nature

These responsibilities are:

- **binding** for all implementations,
- **authoritative** for architectural interpretation,
- **precedent-setting** in cases of ambiguity.

Implementations may **concretize** these responsibilities,
but MUST NOT:
- extend them,
- restrict them,
- reinterpret them.

If an implementation cannot satisfy a responsibility,
it MUST STOP.

---

## Summary

- MMS provides **structure**, not meaning.
- MMS manages **artifacts**, not truth.
- MMS enables **traceability**, not decisions.
- All authority lies **outside** of MMS.

---

_End of responsibilities and scope._
