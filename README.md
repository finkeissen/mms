# Matrix Management System (MMS)

**Status:** Draft  
**Current version:** 0.2.x  
**Scope:** Conceptual architecture + reference structure  
**Goal:** A DBMS-like system for epistemic artifacts (claims, relations, conflicts)

---

## What MMS Is

The **Matrix Management System (MMS)** is a system for managing
**epistemic artifacts** under conditions of:

- incomplete knowledge
- conflicting sources
- alternative interpretations
- long-term revision and auditability

MMS does **not** decide what is true.

Instead, it provides:
- stable identities
- explicit provenance
- append-only history
- explicit conflict representation

MMS is closer to a **database system** than to an expert system.
It is an infrastructure for *managing uncertainty*, not resolving it.

---

## Non-Authority, Merit Exposure

MMS is a strictly **non-authoritative system**.

It does not derive authority from sources, authors, institutions,
historical standing, or social recognition.
No form of eminence has structural effect within the system.

All inputs enter MMS exclusively as explicit artifacts
(claims, relations, conflicts),
bound to provenance, context, and time.

---

MMS does not evaluate, rank, score, or select claims.
It does not decide which claims are stronger, better,
more relevant, or more correct.

The system produces **structural effects only**.
Any epistemic judgment, interpretation, or validation
must occur explicitly outside MMS.

---

Merit is therefore not enforced, optimized, or operationalized.

Merit may become visible through:
- explicit formulation
- stable reference structures
- reproducibility across runs
- persistence under conflict

Such effects are **emergent**, not systemic.

---

In MMS:
- authority does not accumulate
- status does not propagate
- consensus does not collapse disagreement
- visibility replaces validation
- responsibility replaces truth

Any appearance of authority is external to MMS
and must be introduced explicitly.

---

## Core Design Principle

> **Nothing is silently decided.  
> Everything is explicit, inspectable, and reversible by history.**

This principle applies uniformly to:
- extraction
- structure
- conflicts
- revisions
- automation

There are no hidden defaults, implicit resolutions, or silent overwrites.

---

### Architectural Note — Reversibility

Reversibility refers to **structural reversibility by history**,  
not to undoing or correcting claims.
Nothing is deleted; later structure may contradict earlier structure.

---

## MMS as a DBMS (Conceptual Analogy)

MMS deliberately mirrors the architecture of a classical DBMS,
but replaces *data* with *knowledge claims*.

| DBMS Concept        | MMS Equivalent |
|--------------------|----------------|
| Table / Record     | Claim / Relation / Conflict |
| Schema             | JSON Schema (kernel-bound) |
| Transaction        | Run |
| WAL / History      | Append-only run history |
| Constraint Check   | Kernel Gate |
| Index              | Derived, optional access layer |
| Query Language     | External / out of scope |
| Truth / Consistency| Explicitly **not enforced** |

This analogy is **architectural**, not literal.
MMS borrows structural rigor, not epistemic authority.

---

### Explicit Boundary — Analogy Limit

The DBMS analogy must not be read as implying:
- correctness
- consistency
- convergence
- completeness
- queryable truth

It is a **structural analogy only**.

---

## What MMS Manages

MMS manages exactly three **canonical artifact types**:

1. **Claims**  
   Atomic assertions extracted from sources.

2. **Relations**  
   Structural links between claims (e.g. alternatives, dependencies).

3. **Conflicts**  
   Explicit representations of incompatibility between claims.

These artifacts are:
- append-only
- schema-bound
- provenance-rich
- conflict-capable
- never silently modified

Everything else is derived.

---

### Clarification — Claims Are Not Facts

Claims are **statements made by sources**, not facts about the world.
Their presence in MMS implies admissibility, not correctness.

---

## Clarification — Scope of Claims (Additive)

Claims managed by MMS may represent, without distinction or special status:

- descriptive statements,
- normative statements,
- alternative options or courses of action,
- advantages, disadvantages, and tradeoffs,
- rules, norms, or requirements,
- institutional or authoritative statements,
- interpretations and counter-interpretations.

MMS does not interpret, enforce, prioritize, or evaluate
any such claims.
Their representation has **no normative or authoritative effect**
within the system.

This clarification introduces no new artifact types,
no new kernel behavior,
and no additional admissibility criteria.

---

## What MMS Explicitly Does NOT Do

MMS does **not**:

- determine correctness or truth
- rank, score, or weight claims
- resolve conflicts automatically
- enforce a global ontology
- hide uncertainty
- collapse alternatives

All such operations may exist **outside** the MMS kernel,
but never implicitly inside it.

Any resolution must be explicit, reversible, and external.

---

### Explicit Boundary — No Implicit Resolution

Any process that *appears* to reduce disagreement
without explicit representation is architecturally invalid.

---

## Kernel, Process, and Roles

MMS separates concerns strictly.

---

### Kernel

The **Kernel** defines:
- invariants
- identity rules
- append-only semantics
- minimal structural guarantees

The kernel is:
- passive
- non-intelligent
- non-heuristic

It validates structure, not meaning.

---

### Clarification — Kernel Scope

The kernel never inspects semantic content.
It enforces only:
- schema validity
- identity constraints
- append-only guarantees

---

### Logical Process

The **Logical Process** defines:
- stages from extraction to publication
- ordering constraints
- allowed transitions
- failure modes

Processes do not decide truth.
They only define *what may happen when*.

---

### Explicit Boundary — Process vs. Authority

A process may fail, stop, or abort,
but it may never *decide*.

---

### Profiles and Modes

**Profiles** define *who may do what*.
**Modes** bundle profiles, tools, and processes into reproducible configurations.

Profiles define **permissions**, not authority.
No profile has epistemic priority.

---

### Clarification — Reproducibility Without Correctness

Modes guarantee reproducibility of structure,
never correctness of content.

---

## Runs: The Transaction Unit

A **Run** is the atomic execution and audit unit of MMS.

A run records:
- inputs (sources, prior artifacts)
- configuration (modes, prompts, tools)
- outputs (claims, relations, conflicts)
- outcome (e.g. SUCCESS, NOCLAIM, STOP)

Runs are:
- append-only
- never modified or deleted
- the sole origin of canonical artifacts

> **No run, no claim.**

---

### Explicit Boundary — STOP as Valid Outcome

STOP is a valid, expected, and correct run outcome.
A run ending in STOP produces no claims
and requires no repair.

---

## Identity, Hashes, and Integrity

MMS relies on **explicit identity**, not implicit context.

Hashes are used to ensure:
- source immutability
- configuration traceability
- reproducibility
- integrity verification

Hashes provide **identity and integrity**, not meaning or trust.

---

### Clarification — Hashes Are Not Validation

Hashes do not imply:
- source quality
- correctness
- authority
- endorsement

---

## Indices and Access (Derived, Optional)

MMS does **not** define a central index.

> **Indices are derived artifacts, not kernel objects.**

They:
- never add information
- never resolve conflicts
- may always be deleted and rebuilt

The system remains valid without them.

---

### Architectural Note — Index Volatility

Indices must be treated as disposable views,
never as epistemic artifacts.

---

## Automation and Tooling

Automation in MMS is:
- optional
- external to the kernel
- contract-bound

Tools never bypass:
- kernel invariants
- append-only semantics
- explicit run boundaries

There is no hidden automation.

---

### Explicit Boundary — Tool Responsibility

Any tool that introduces:
- aggregation
- summarization
- ranking
- interpretation

operates **outside** MMS responsibility.

---

## Repository Structure (Conceptual)

```text
docs/        # Normative architecture and design
schemas/     # Canonical JSON Schemas (kernel-bound)
kernel/      # Core invariants and validation logic
pipelines/   # Logical process definitions
profiles/    # Role and permission definitions
runs/        # Append-only execution records
tools/       # Optional helper tools
modes/       # Historical archive (non-canonical)


## Gateway

The `gateway/` folder contains the **structural enforcement layer**:
- form-only checks
- STOP / Absence as valid outcomes
- append-only logging into the Matrix

It introduces no evaluation, ranking, or decision-making.

