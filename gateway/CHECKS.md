# MMS Gateway — Structural Checks

This document defines the **minimal structural checks** performed by the MMS Gateway.

All checks are:
- content-agnostic
- non-evaluative
- non-optimizing

The Gateway enforces **form only**, never meaning.

---

## Layer 1 — Problem Articulation

Checks:
- A problem statement is explicitly present.
- Scope or boundary markers are provided.
- Non-goals (or exclusions) are explicitly stated or marked as absent.

STOP if:
- No explicit problem can be identified.
- Claims are presented without a problem reference.

---

## Layer 2 — Claim Formation

Checks:
- Each claim is explicitly bound to a problem.
- Claims are stated as propositions or hypotheses.
- No truth, correctness, or optimality language is used.

STOP if:
- Claims stand alone without problem assignment.
- Claims assert evaluation, ranking, or solutions.

---

## Layer 3 — Structural Admissibility

Checks:
- Claims remain within declared problem scope.
- No layer transitions are skipped.
- Responsibility is not assigned to the system.

Outcomes:
- admissible
- STOP
- Absence

STOP if:
- Decision, execution, or authority is implied.

---

## Layer 4 — Decision Attribution

Checks:
- A decision holder is explicitly named (external).
- The decision is marked as external to the system.

STOP if:
- Decisions are delegated to the MMS or Gateway.
- Decisions are implicit or unnamed.

---

## Layer 5 — Execution / Application

Checks:
- Execution is explicitly marked as external.
- Consequences are acknowledged as irreversible.

STOP if:
- Execution is treated as epistemic validation.

---

## Layer 6 — Audit / Reflection

Checks:
- Audit occurs ex post.
- Findings are descriptive, not justificatory.

STOP if:
- Audit is used to retroactively legitimize decisions.

