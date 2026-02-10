# MMS – Index (PUBLIC)

## Repository Orientation Index  
**Contracts · Architecture · Decisions · Terminology**

---

## Purpose of This File

This file is the **canonical navigation and orientation index**
for the **MMS repository**.

Its purpose is to:
- provide a stable entry point for readers and auditors
- make responsibility boundaries explicit
- prevent layer confusion
- avoid implicit authority through structural clarity

This file contains:
- **no epistemic content**
- **no architectural decisions**
- **no implementation details**

It is purely **structural**.

---

## How to Read This Index

The repository is organized as a **strict separation of concerns**.

Each section:
- has a clearly defined role
- must not assume responsibilities of other sections
- increases specificity **without increasing authority**

Reading order matters.

---

## Public Contract Layer (Normative)

### Directory: `requirements/`

**Role:**  
Define the **binding public contract** of the Matrix Management System (MMS).

**Responsibilities:**
- define what MMS is and guarantees
- define what MMS explicitly does not do
- establish non-negotiable architectural invariants
- fix normative terminology

**Does NOT:**
- describe implementation details
- define runtime behavior
- prescribe tooling or technologies

---

### Core Contract Documents

These documents are **normative and binding**:

- `README.md`  
  → Entry point: scope, guarantees, non-goals

- `RESPONSIBILITIES.md`  
  → Explicit responsibilities and scope boundaries

- `ARCHITECTURE.md`  
  → Non-negotiable architectural invariants

- `DECISIONS.md`  
  → Record of explicit, binding system decisions

- `GLOSSARY.md`  
  → Normative terminology (authoritative)

---

### Supporting Contract Material

- `schemas/`  
  → Canonical schemas defining valid artifact structure

- `docs/`  
  → Additional normative explanations and clarifications  
  (must not contradict core documents)

---

### Implementation

This repository does not include implementation code (e.g., gateways).
See `IMPLEMENTATION.md`.


### Directory: `gateway/`

**Role:**  
Provide a **reference implementation** of the MMS contracts.

**Responsibilities:**
- implement the guarantees defined in `requirements/`
- execute runs
- enforce invariants at runtime
- provide technical projections and access paths

**Does NOT:**
- define contracts
- introduce new responsibilities
- make epistemic decisions

All content under `gateway/` is **NON-PUBLIC**
and may change without affecting the contract,
as long as the contract is upheld.

---

## Canonical Reading Order

1. `requirements/README.md`
2. `requirements/RESPONSIBILITIES.md`
3. `requirements/ARCHITECTURE.md`
4. `requirements/DECISIONS.md`
5. `requirements/GLOSSARY.md`
6. `gateway/README.md` (implementation context)

---

## Canonical Rule

> **If something appears to decide, recommend, conclude,  
> or assert truth, it is already outside the scope of MMS.**

---

## Maintenance Rules

- This index changes **only** when:
  - repository structure changes
  - responsibility boundaries shift (rare)
- This index must never contain:
  - epistemic claims
  - domain examples
  - implementation specifics
  - references to external or former repositories

Its sole purpose is **orientation without authority**.

---

## Status

This file is **structural glue**.

If this file feels boring,
it is doing its job.

