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

### Non-Canonical Areas (Historical / Derived)

The following areas are **not** authoritative:

- `modes/`       — historical exploration archive
- `exports/`     — derived artifacts
- `tmp/`, `logs/`, `snapshots/` — runtime artifacts

Do **not** introduce new development into `modes/`.
It is preserved for traceability only.

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

## Runs and Artifacts

Remember:

> **No run, no claim.**

Canonical artifacts must always originate from a **Run**.
Manual insertion or modification of claims, relations, or conflicts
outside a run is not permitted.

---

## Tests and Validation

Before submitting a contribution, please ensure:

```bash
python -m compileall -q .
pytest --import-mode=importlib

