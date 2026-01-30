# Audit — Structural Checklist

This checklist is used for **ex post inspection** of RP → MMS → Matrix passes.

Audit evaluates **structure only**, never outcomes.

---

## A. Boundary Integrity

- [ ] Was a problem explicitly articulated?
- [ ] Were claims strictly bound to that problem?
- [ ] Were any layer transitions skipped?

STOP finding if:
- Any claim appears without problem assignment.

---

## B. Authority Leakage

- [ ] Did the system imply recommendation, ranking, or decision?
- [ ] Was responsibility ever attributed to the system?
- [ ] Did language suggest “best”, “correct”, or “optimal”?

STOP finding if:
- Any implicit authority is detected.

---

## C. Role Discipline

- [ ] Are all roles external to the system?
- [ ] Is STOP authority limited to structural checks?
- [ ] Are decision and execution clearly external?

STOP finding if:
- Roles collapse or merge implicitly.

---

## D. Failure Handling

- [ ] Are STOP and Absence logged as valid outcomes?
- [ ] Was processing halted correctly on STOP?
- [ ] Were failures logged without guidance?

STOP finding if:
- Failures are optimized away or justified.

---

## E. Log Integrity

- [ ] Is the log entry append-only and immutable?
- [ ] Does each log reference exactly one Gateway pass?
- [ ] Is the structural reason non-evaluative?

STOP finding if:
- Logs contain recommendations or priorities.

---

## Audit Outcome

- **Status:** clean / issues detected
- **Findings:** (list, descriptive only)
- **Required action:** none / structural clarification only

