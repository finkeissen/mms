# MMS Gateway — Input / Output Specification

This document defines the **formal input and output structures** of the MMS Gateway.

The specification is:
- content-agnostic
- non-evaluative
- non-optimizing

It defines **shape only**, never meaning.

---

## Inputs

### Required Inputs

- **Problem Statement**
  - Explicit articulation of a problem.
  - May include scope and boundary markers.

- **Claim(s)**
  - One or more propositions explicitly bound to the problem.
  - Claims must not assert truth, correctness, or optimality.

### Optional Inputs

- **Assumptions**
  - Explicitly stated assumptions.
  - If absent, must be marked as such.

- **Context Metadata**
  - Source reference
  - Date / time
  - Domain label (non-binding)

---

## Input Constraints

- Every claim must reference exactly one problem.
- Problems may exist without claims.
- Claims may not exist without a problem.

STOP if:
- A claim is submitted without a problem reference.
- Input collapses problem, claim, and decision into a single statement.

---

## Outputs

### Structural Outcomes

- **admissible**
  - Input satisfies all structural checks.

- **STOP**
  - Structural violation detected.
  - Processing must halt.

- **Absence**
  - Required element is explicitly missing but acknowledged.

---

### Output Payload

Each output includes:

- **Outcome Type**
  - admissible / STOP / Absence

- **Structural Reason**
  - Short, non-evaluative description of the structural condition.

- **Trace Reference**
  - Identifier for logging into the Matrix.

---

## Output Constraints

- Outputs contain no recommendations.
- Outputs contain no rankings or comparisons.
- Outputs contain no decisions or actions.

STOP if:
- Output attempts to guide or optimize external behavior.

