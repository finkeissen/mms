# MMS Gateway — Logging Specification

This document defines how the MMS Gateway **records outcomes** into the Matrix.

Logging is:
- append-only
- non-evaluative
- non-optimizing
- irreversible once written

The Gateway logs **what occurred**, not what should occur.

---

## Logging Principles

- Every Gateway pass produces exactly one log entry.
- Log entries are immutable.
- Logs record structure, not meaning.

The Matrix is a **record**, not a control surface.

---

## Log Entry Structure

Each log entry MUST include:

- **Log ID**
  - Unique identifier.

- **Timestamp**
  - Time of Gateway processing.

- **Input Reference**
  - Pointer to the received problem and claims.

- **Outcome**
  - admissible / STOP / Absence

- **Structural Reason**
  - Short description of the structural condition.
  - No evaluative language.

- **Layer Reference**
  - Lowest layer reached before halt or pass.

- **Role Labels (if provided)**
  - Problem Owner
  - Claim Author
  - Decision Holder
  - Executor
  - Auditor

---

## Prohibited Log Content

Log entries must not contain:

- recommendations
- priorities
- rankings
- confidence scores
- inferred intent
- corrective suggestions

STOP if:
- a log entry attempts to guide external behavior.

---

## Relationship to Audit

- Logs are the **primary audit substrate**.
- Audit operates strictly ex post.
- Logs must remain readable without external context.

---

## Failure Logging

- STOP and Absence outcomes are logged identically to admissible outcomes.
- Failure is not treated as an exception.
- Failure frequency must not be optimized away.

---

## Traceability Constraint

Each log entry must be traceable to:
- one problem articulation
- zero or more claims
- exactly one Gateway pass

No aggregation across passes is permitted.

