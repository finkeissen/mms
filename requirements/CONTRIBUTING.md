# Contributing to Matrix Management System (MMS)

Thank you for your interest in contributing to MMS.

This project is **architecture-driven**, not feature-driven.
Contributions are evaluated primarily on **conceptual clarity,
structural correctness, and auditability**, not on speed or volume.

---

## Guiding Principles

All contributions must respect the core MMS principles:

- Nothing is silently decided
- Everything is explicit and inspectable
- History is append-only
- Conflicts are represented, not resolved implicitly
- Structure is preferred over heuristics

If a change introduces hidden assumptions, implicit behavior,
or irreversible effects, it is not acceptable.

---

### Clarification — Contribution Bar

The bar for acceptance is intentionally high.
Rejection of a contribution does not imply poor quality;
it usually indicates architectural mismatch.

---

## Canonical vs. Non-Canonical Areas

### Canonical Areas (Authoritative)

All active development must happen in:

- `docs/`        — normative architecture and design
- `schemas/`     — canonical JSON Schemas
- `kernel/`      — core invariants and validation logic
- `pipelines/`   — logical process definitions
- `profiles/`    — role and permission definitions
- `runs/`        — append-only execution records

Changes in these areas are considered **architecturally binding**.

---

### Clarification — Canonical Responsibility

Changes in canonical areas affect:
- auditability
- responsibility boundaries
- downstream interpretation

Contributors are expected to understand these implications.

---

### Non-Canonical Areas (Historical / Derived)

The following areas are **not** authoritative:

- `modes/`       — historical exploration archive
- `exports/`     — derived artifacts
- `tmp/`, `logs/`, `snapshots/` — runtime artifacts

Do **not** introduce new development into `modes/`.
It is preserved for traceability only.

---

### Explicit Boundary — Derived Does Not Mean Safe

Non-canonical does not mean unimportant.
It means **non-authoritative**.

Derived areas must never be used
to smuggle implicit decisions back into canonical state.

---

## What to Contribute

Appropriate contributions include:

- clarifications or refinements of architectural documentation
- tightening of schemas or invariants
- improved validation or tooling that respects kernel boundaries
- tests that enforce existing assumptions
- explicit documentation of trade-offs or limitations

Inappropriate contributions include:

- automatic conflict resolution
- implicit ranking or scoring of claims
- hidden defaults or heuristics
- shortcuts that bypass runs, schemas, or kernel checks
- rewriting history

---

### Clarification — “Helpful” Is Not a Criterion

A contribution being “useful” or “convenient”
is not sufficient for acceptance.
Architectural integrity always wins over convenience.

---

## Runs and Artifacts

Remember:

> **No run, no claim.**

Canonical artifacts must always originate from a **Run**.
Manual insertion or modification of claims, relations, or conflicts
outside a run is not permitted.

---

### Clarification — Responsibility of the Contributor

If you introduce a run, you introduce responsibility.
You must be able to explain:
- why the run exists
- what assumptions it encodes
- why STOP was or was not triggered

---

## Tests and Validation

Before submitting a contribution, please ensure:

```bash
python -m compileall -q .
pytest --import-mode=importlib

