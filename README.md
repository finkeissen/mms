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

## Kernel, Process, and Roles

MMS separates concerns strictly.

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

### Logical Process

The **Logical Process** defines:
- stages from extraction to publication
- ordering constraints
- allowed transitions
- failure modes

Processes do not decide truth.
They only define *what may happen when*.

---

### Profiles and Modes

**Profiles** define *who may do what*.
**Modes** bundle profiles, tools, and processes into reproducible configurations.

Profiles define **permissions**, not authority.
No profile has epistemic priority.

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

## Identity, Hashes, and Integrity

MMS relies on **explicit identity**, not implicit context.

Hashes are used to ensure:
- source immutability
- configuration traceability
- reproducibility
- integrity verification

Hashes provide **identity and integrity**, not meaning or trust.

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
```

---

## Position of MMS in the Repository Cascade

MMS is **not a standalone epistemic system**.
It is part of a **deliberately layered repository cascade**:

```text
research-program
→ Matrix Management System (MMS)
→ Matrix
→ external decision-making systems
```

### research-program

Defines the **epistemic rules of legitimacy**:
- which kinds of claims are admissible
- how disagreement must be represented
- where reasoning must explicitly stop

It produces **no results**, **no truth**, and **no conclusions**.

### MMS (this repository)

Implements the **operative handling rules** derived from the research-program.

MMS:
- manages claims, relations, and conflicts
- enforces structure, provenance, and history
- produces no truth, rankings, or decisions

MMS is **not neutral** in the abstract sense:
it is a concrete, rule-bound implementation.
What remains non-negotiable is that it produces
**no epistemic authority**.

### Matrix

The **Matrix** is the concrete, instantiational product
generated by MMS runs.

It represents:
- what is claimed
- by whom
- when
- under which assumptions
- and in conflict with what

The Matrix is **not truth**, **not authority**, and **not a decision**.

---

## Architectural Contract

The cross-repository architectural contract
and the precise responsibility boundaries between:

- research-program
- MMS
- Matrix

are defined in the following document:

→ **README_research-program+mms+matrix.md**  
(maintained in the `research-program` repository)

That document is **authoritative for layering and responsibility**,
but **not MMS-internal architecture**.

For MMS-internal norms, see:
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `GLOSSARY.md`

---

## How to Work With This Repository

All authoritative development happens in:
- `docs/`
- `schemas/`
- `kernel/`
- `pipelines/`
- `profiles/`
- `runs/`

The `modes/` directory is preserved for historical traceability only.

---

## Summary

MMS exists to **manage epistemically structured statements**
under explicit rules of provenance, temporality, and conflict —
without collapsing them into truth, consensus, or decision.

If something feels implicit, it is probably wrong.
