# Epistemic Hygiene (MMS Operational Contract)

This document specifies purely operational mechanisms for:
- detection,
- marking,
- isolation,
- and enforcement
of epistemic contamination signals defined by the research-program.

No remediation, correction, or resolution is performed.

## Contamination Classes (Operational Tags)

- EH01_IMPLICIT_NORMATIVITY
- EH02_HIDDEN_AUTHORITY
- EH03_LAYER_COLLAPSE
- EH04_UNDECLARED_ASSUMPTION_DRIFT
- EH05_HEURISTIC_SUBSTITUTION

## Enforcement Actions (Non-Normative)

- FLAG: record receives contamination tags; processing may continue only if allowed by RP contract.
- QUARANTINE: record is isolated; downstream propagation is blocked.
- REJECT: record is rejected with an operational error.
- STOP_FLAG: MMS records STOP/HARD_STOP state when RP-defined conditions are violated.

## State Machine

OK → FLAGGED → (OK | QUARANTINED | REJECTED)
Any RP-violation → STOP_FLAG (STOP or HARD_STOP)

## Audit Requirements

Every hygiene action must record:
- timestamp
- rule reference (RP document + section id)
- triggering field(s)
- action taken
- actor (system/user)

