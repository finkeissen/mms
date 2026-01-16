# MMS Architecture

This document defines the **normative architectural principles** of the
Matrix Management System (MMS).

It answers the question:

> *What must never change, regardless of implementation details?*

This document is authoritative.
If other documents conflict with it, this document wins.

---

## Architectural Scope

MMS is an infrastructure for managing **epistemic artifacts**
under uncertainty and disagreement.

It is **not**:
- a reasoning engine
- a truth-finding system
- an expert system
- a knowledge graph with implicit semantics

MMS provides structure, identity, and history.
Meaning and resolution are always external.

---

### Clarification — Architecture vs. Implementation

This document defines **architectural invariants**, not implementation choices.
Programming languages, storage backends, and tooling may change;
architectural responsibilities must not.

---

## Core Architectural Invariants

The following invariants are **non-negotiable**.

### 1. Append-Only Semantics

All canonical artifacts are append-only.

- Artifacts are never modified or deleted
- Corrections are new artifacts
- Revisions are explicit and historical
- History is inspectable and immutable

There is no concept of “update in place”.

---

### Architectural Note — Historical Integrity

Append-only semantics are required to preserve **epistemic traceability**.
Any mechanism that obscures prior states,
even for performance or convenience reasons,
violates architectural integrity.

---

### 2. Explicit Origin (Runs)

Every canonical artifact originates from exactly one **Run**.

- No run → no artifact
- Manual insertion is forbidden
- Runs are immutable once completed
- Runs are the atomic audit unit

Runs are the only bridge between automation and canonical state.

---

### Clarification — Runs as Responsibility Anchors

Runs bind:
- tooling behavior
- configuration
- inputs
- outputs

to a single accountable execution context.
Without runs, attribution and audit collapse.

---

### 3. Explicit Structure (Schemas)

All canonical artifacts are schema-bound.

- Schemas are explicit and versioned
- Validation happens at the kernel boundary
- Invalid artifacts never enter the system
- Schemas describe structure, not meaning

Schema violations are structural errors, not soft warnings.

---

### Explicit Boundary — No Semantic Enforcement

Schemas must never encode:
- truth conditions
- domain correctness
- epistemic priority
- implicit interpretation

Any attempt to encode meaning into schemas
constitutes a category error.

---

### 4. No Implicit Decisions

MMS never makes silent decisions.

This includes:
- conflict resolution
- claim prioritization
- truth selection
- uncertainty collapse
- default interpretation

If a decision exists, it must be:
- explicit
- inspectable
- attributable
- reversible by history

---

### Clarification — Silence Is Not Neutrality

Implicit behavior is **not** neutral behavior.
Silence at the architectural level is interpreted as a defect.

---

### 5. Conflict Is a First-Class Concept

Conflicts are not failures.

- Conflicts are explicit artifacts
- Conflicts may persist indefinitely
- Conflicts are never auto-resolved
- Conflict absence must not be assumed

Disagreement is preserved, not normalized away.

---

### Architectural Note — Conflict Persistence

The system must remain valid
even if conflicts are never resolved.
Resolution is optional; representation is mandatory.

---

## Separation of Concerns

MMS enforces strict separation.

### Kernel

The kernel:
- enforces invariants
- validates schemas
- guards append-only semantics
- has no domain knowledge
- contains no heuristics

The kernel is deliberately minimal.

---

### Clarification — Kernel as Firewall

The kernel acts as a **firewall**
against implicit epistemic behavior.
Any logic requiring interpretation
must live outside the kernel.

---

### Processes

Processes:
- define allowed sequences of runs
- encode ordering and staging
- define failure modes
- never decide truth

Processes orchestrate, they do not judge.

---

### Explicit Boundary — Process Termination

A process may terminate in failure or STOP
without producing artifacts.
This is a valid and expected outcome.

---

### Profiles

Profiles define permissions.

- who may create which runs
- who may add which structures
- who may transform representations

Profiles define **capability**, not authority.

---

### Clarification — No Epistemic Privilege

No profile may introduce
epistemic priority or correctness by role.

---

### Tooling

Tools are external.

- tools assist humans or automation
- tools operate via explicit runs
- tools are replaceable
- tools never bypass the kernel

Automation is always optional.

---

### Explicit Boundary — Tool Responsibility

Any tool that:
- aggregates
- summarizes
- ranks
- interprets

operates outside MMS responsibility
and must not write canonical artifacts implicitly.

---

## Identity and Integrity

### Identity

Artifacts are identified explicitly.

- no implicit identity by position or context
- identity survives reindexing and restructuring
- identity is stable across views

---

### Hashes

Hashes are mandatory for integrity.

They provide:
- immutability guarantees
- reproducibility
- auditability

Hashes do not provide trust or meaning.
They only guarantee sameness.

---

### Clarification — Integrity vs. Authority

Integrity ensures sameness over time.
It does not imply correctness, relevance, or trustworthiness.

---

## Derived Artifacts

Indices, views, projections, summaries, rankings, and graphs are:

- derived
- optional
- non-canonical
- disposable

They may be deleted and rebuilt at any time.

The system remains valid without them.

---

### Architectural Note — Derived Artifact Risk

Derived artifacts must never be confused
with canonical state.
Any coupling between them
is an architectural violation.

---

## Architectural Non-Goals

The following are explicitly out of scope:

- global consistency enforcement
- automatic conflict resolution
- implicit ontology alignment
- probabilistic truth scoring
- hidden optimization layers

These may exist externally,
but never inside the MMS kernel.

---

### Explicit Boundary — Optimization

Performance optimization must never:
- alter semantics
- obscure history
- introduce defaults

---

## Evolution Rules

Architecture evolves under strict rules:

- invariants may only be tightened, never weakened
- new concepts must not introduce implicit behavior
- backward compatibility is preferred but secondary to clarity
- history must remain interpretable

Breaking history is worse than breaking APIs.

---

### Clarification — Evolution as Constraint Tightening

Evolution serves to **reduce ambiguity**,
not to expand system power.

---

## Decision Record

Architectural decisions must be:

- documented
- justified
- attributable
- reviewable

Undocumented architecture does not exist.

---

### Architectural Note — Decision Transparency

Decision records are part of the architecture.
Omitting them is equivalent to making hidden decisions.

---

## Summary

MMS is an infrastructure for **preserving epistemic structure over time**.

It optimizes for:
- explicitness
- auditability
- reversibility
- disagreement tolerance

Any change that weakens these properties
is architecturally invalid.

---

## Forbidden Changes (Hard Prohibitions)

The following changes are architecturally forbidden,
even if they appear convenient, performant, or “more useful”:

- introducing in-place updates of canonical artifacts
- allowing canonical artifacts without a Run origin
- allowing manual insertion into canonical state
- adding implicit conflict resolution
- adding implicit claim prioritization or ranking
- adding default interpretations or “best effort” synthesis
- embedding domain semantics into the kernel
- allowing tools to bypass kernel validation
- treating derived artifacts as canonical state
- deleting history to “clean up” or reduce size

If any of these are proposed,
the burden of proof is on the proposer to show that
the prohibition is not being violated.
If unclear, the correct outcome is STOP.

---

## Misuse Triggers (Audit Alerts)

The following signals should be treated as audit triggers:

- “We should just fix it in place.”
- “Let’s pick the best source.”
- “We can auto-merge similar claims.”
- “This conflict is probably noise.”
- “Let’s hide contradictions for users.”
- “We can infer truth from structure.”
- “The model concluded that…”

These are not “opinions”.
They are structural indicators of authority creep.

---

## STOP and Non-Production (Kernel-Compatible)

STOP is a valid, expected architectural outcome.

- STOP does not require repair
- STOP does not imply failure of the system
- STOP preserves integrity when admissibility is violated

Any mechanism that attempts to bypass STOP
by producing “something anyway”
introduces implicit decisions and is forbidden.

