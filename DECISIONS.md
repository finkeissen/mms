# MMS Architectural Decisions

This document records **architectural decisions** made for the
Matrix Management System (MMS).

Its purpose is to:
- preserve decision context
- make trade-offs explicit
- prevent silent architectural drift
- enable future review and revision

This is **not** a log of implementation details.
Only decisions that affect architecture belong here.

---

## How to Read This Document

Each decision is recorded as:

- **ID** — stable identifier
- **Status** — Accepted | Superseded | Deprecated
- **Context** — the problem or pressure that required a decision
- **Decision** — the chosen architectural rule
- **Consequences** — implications and trade-offs

If a decision is superseded, the superseding decision must be referenced.

---

## DEC-001: Append-Only Canonical Artifacts

**Status:** Accepted

### Context
Epistemic artifacts change over time.
Silent modification destroys auditability and makes disagreement invisible.

### Decision
All canonical artifacts in MMS are **append-only**.

Artifacts:
- are never modified or deleted
- may only be superseded by new artifacts
- remain permanently inspectable

### Consequences
- History grows monotonically
- Storage cost increases
- Auditability and reversibility are guaranteed

---

## DEC-002: Runs as the Sole Origin of Canonical Artifacts

**Status:** Accepted

### Context
Allowing multiple creation paths for artifacts leads to ambiguity,
implicit authority, and unverifiable provenance.

### Decision
Every canonical artifact must originate from exactly one **Run**.

- No run → no artifact
- Manual insertion is forbidden
- Runs are immutable once completed

### Consequences
- All artifacts are attributable
- Automation and humans are treated uniformly
- Debugging and audits are simplified

---

## DEC-003: Explicit Schemas at the Kernel Boundary

**Status:** Accepted

### Context
Implicit structure leads to silent divergence and brittle tooling.

### Decision
All canonical artifacts must validate against explicit,
versioned **JSON Schemas** at the kernel boundary.

Schemas:
- define structure, not meaning
- are normative
- reject invalid artifacts

### Consequences
- Structural errors are caught early
- Schema evolution must be managed explicitly
- Tooling becomes simpler and more robust

---

## DEC-004: No Implicit Conflict Resolution

**Status:** Accepted

### Context
Automated or hidden conflict resolution encodes epistemic authority
and erases disagreement.

### Decision
Conflicts are **first-class artifacts** and are never resolved implicitly.

- Conflicts may persist indefinitely
- Absence of conflict is not assumed to imply agreement

### Consequences
- Consumers must handle disagreement explicitly
- The system remains neutral with respect to truth
- Downstream complexity increases by design

---

## DEC-005: Separation of Kernel and Tooling

**Status:** Accepted

### Context
Embedding automation logic into the core leads to lock-in
and implicit behavior.

### Decision
The kernel is minimal and passive.
All automation lives outside the kernel and interacts only via runs.

### Consequences
- The kernel remains stable
- Tooling is replaceable
- Automation is optional and explicit

---

## DEC-006: Derived Artifacts Are Non-Canonical

**Status:** Accepted

### Context
Indices, views, and summaries are convenient but ephemeral.

### Decision
All derived artifacts are **non-canonical**.

- They may be deleted at any time
- They never add information
- They never resolve conflicts

### Consequences
- Canonical state remains minimal
- Rebuild cost is accepted
- Operational complexity is shifted outward

---

## DEC-007: Profiles Define Capability, Not Authority

**Status:** Accepted

### Context
Role-based systems often smuggle epistemic authority into permissions.

### Decision
Profiles define **what may be done**, not **what is correct**.

- No profile has epistemic priority
- Permissions do not imply trust or truth

### Consequences
- Authority remains external
- Governance must be explicit
- Social processes are not encoded implicitly

---

## DEC-008: Modes Are Historical, Not Canonical

**Status:** Accepted

### Context
Early exploration artifacts risk being mistaken for reference implementations.

### Decision
The `modes/` directory is treated as a **historical archive**.

- It is preserved for traceability
- It is not authoritative
- New development must not happen there

### Consequences
- Architectural clarity is preserved
- Historical context remains available
- Duplication is accepted

---

## DEC-009: Architecture Over Convenience

**Status:** Accepted

### Context
Short-term convenience often erodes long-term clarity and auditability.

### Decision
When in conflict, **architectural integrity wins over convenience**.

### Consequences
- Some workflows are intentionally more verbose
- Tooling may feel restrictive
- Long-term stability and inspectability improve

---

## Open Decisions

The following areas are intentionally undecided:

- query language or API
- indexing strategies
- conflict consumption patterns
- governance and social processes
- trust and reputation mechanisms

These are deferred by design.

---

## Adding New Decisions

New architectural decisions must:

- have a clear ID
- describe context and trade-offs
- state consequences explicitly
- not contradict accepted decisions without superseding them

Undocumented decisions do not exist.

---

## Summary

This document is the **memory of architectural intent**.

When in doubt:
- consult this file
- prefer explicitness
- resist silent drift

