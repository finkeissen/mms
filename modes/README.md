# modes/

## Historical Modes Archive (Non-Canonical)

---

## Purpose of This Directory

The `modes/` directory is a **historical exploration archive**.

It contains:
- early experiments
- prototype pipelines
- exploratory configurations
- abandoned or superseded approaches
- pre-architectural iterations

These materials document **how MMS came to be** —
not **how MMS is meant to operate now**.

---

## Canonical Status (Explicit)

> **Nothing in `modes/` is canonical.**

This directory is:
- ❌ not part of the MMS execution model
- ❌ not authoritative
- ❌ not normative
- ❌ not safe to extend
- ❌ not a reference for current architecture

Its contents are preserved **for traceability only**.

---

## Relationship to Current MMS Architecture

The current MMS architecture is defined exclusively by:

- `mms/README.md`
- `mms/ARCHITECTURE.md`
- `mms/DECISIONS.md`
- `mms/GLOSSARY.md`
- `mms/MISUSE.md`
- `mms/AUDIT.md`
- `INDEX.md`

If anything in `modes/` contradicts these documents:

> **The architecture wins.  
> The mode is considered invalid under current rules.**

No exception.

---

## Why `modes/` Still Exists

Keeping historical modes serves four purposes:

1. **Traceability**  
   They show which paths were tried — and rejected.

2. **Learning**  
   They make architectural trade-offs concrete.

3. **Auditability**  
   They prevent silent loss of design history.

4. **Anti-Regression**  
   They document patterns that must *not* be reintroduced.

Deletion would erase epistemic memory.
Preservation without authority is the correct compromise.

---

## Prohibited Uses of `modes/`

The following uses are **architecturally forbidden**:

- using a mode as a reference implementation
- reviving a mode “because it worked”
- copying logic from a mode into canonical code without re-derivation
- citing modes as justification for design choices
- extending or modifying existing modes
- adding new modes

If a mode appears useful, its ideas must be:
- re-derived explicitly
- evaluated against current invariants
- documented as a **new decision** if accepted

---

## Classification Guidance (Recommended)

For internal orientation, modes may be **informally classified** as:

- `pre-mms`  
  → before core invariants were defined

- `proto-mms`  
  → partial alignment, but architecturally incomplete

- `invalid-under-current-architecture`  
  → explicitly incompatible with current rules

These labels are **descriptive only**.
They do not grant legitimacy.

---

## No Forward Evolution Rule

> **`modes/` is frozen by design.**

No new development may occur here.

All new work must happen in:
- `docs/`
- `schemas/`
- `kernel/`
- `pipelines/`
- `profiles/`
- `runs/`

Any pull request touching `modes/`
must justify why it is not violating this rule.
In almost all cases, it will be rejected.

---

## Relationship to STOP

Many modes represent **implicit STOP conditions** discovered historically.

They are valuable precisely because they show:
- where assumptions collapsed
- where authority crept in
- where ambiguity became unmanageable

Reintroducing them would mean
ignoring known STOP signals.

---

## Final Statement

> **`modes/` is memory, not method.  
> History, not guidance.  
> Evidence of restraint, not permission.**

If you find yourself wanting to use a mode,
that is usually a signal to revisit the architecture —
not the archive.

