# MMS Gateway — Failure Modes

This document defines **explicit, admissible failure modes** of the MMS Gateway.

Failure is not an error.
Failure is a **valid structural outcome**.

The Gateway must fail **early, explicitly, and traceably**.

---

## Failure Mode Categories

### 1. STOP — Structural Violation

Definition:
- A structural rule defined by the Research Program or MMS is violated.

Typical causes:
- Claim without explicit problem assignment
- Implicit decision or authority attribution
- Layer transition skipped
- Evaluation, ranking, or optimization language detected

Gateway behavior:
- Halt processing immediately
- Emit STOP outcome
- Provide a structural reason
- Do not suggest corrections

---

### 2. Absence — Explicit Missing Element

Definition:
- A required element is missing but explicitly acknowledged as absent.

Typical causes:
- No assumptions provided
- No scope boundaries defined
- No claims submitted for a problem

Gateway behavior:
- Continue processing where structurally possible
- Emit Absence outcome for the missing element
- Record absence explicitly in the Matrix

---

### 3. Inadmissible Aggregation

Definition:
- Multiple structural layers are collapsed into a single input.

Typical causes:
- Problem, claim, and decision combined in one statement
- Execution implied as validation

Gateway behavior:
- Emit STOP outcome
- Identify collapsed layers
- Require separation before any further processing

---

### 4. Responsibility Collapse

Definition:
- Responsibility is implicitly assigned to the system.

Typical causes:
- “The system decides…”
- “The model recommends…”
- “Automatically choose…”

Gateway behavior:
- Emit STOP outcome
- Explicitly mark responsibility collapse

---

## Non-Failure Conditions

The following are **not** failure modes:

- Uncertainty
- Incompleteness
- Lack of conclusions
- Absence of action
- Multiple admissible claims

These conditions are valid and must not trigger STOP by themselves.

---

## Audit Requirement

Every failure mode must be:
- logged
- traceable
- reviewable ex post

Failure modes are subject to audit.
They must not be optimized away.

