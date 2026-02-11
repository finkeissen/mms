# MMS — Matrix Management System  
**Normative Requirements Repository**

---

## Purpose

This repository defines the **public, normative specification** of the  
**MMS (Matrix Management System)**.

It specifies **what MMS is**, **what it guarantees**, and **how its artifacts are
structured** — independent of any concrete software, runtime, or deployment.

This is **not** an implementation repository.

---

## Normative Authority

All **normative authority** resides exclusively in:

requirements/


Everything outside `requirements/` is **NON-NORMATIVE**, unless a file
explicitly states otherwise.

If any ambiguity arises, **documents under `requirements/` take precedence**.

---

## What This Repository Contains

### ✅ Included (Public, Normative)

- Conceptual and logical system models  
- Contracts, invariants, and guarantees  
- Data models and JSON schemas  
- Process descriptions and constraints  
- Versioned modes, pipelines, and profiles  
- Validation rules and interpretation boundaries  

All of this content lives under:

requirements/


---

### ❌ Explicitly Out of Scope

This repository **does not provide**:

- a runtime
- a service
- an executable system
- a gateway
- any concrete implementation

- deployment tooling

No implementation is required, implied, or assumed.

---

## Implementations (Out of Scope)

Concrete implementations of MMS MAY exist:

- in private repositories
- in internal deployments
- in experimental or operational systems

Such implementations are:
- **NON-NORMATIVE**
- **OPTIONAL**
- **NOT PART OF THIS REPOSITORY’S PUBLIC CONTRACT**

The MMS specification deliberately separates **WHAT** (requirements)
from **HOW** (implementations).

---

## About `gateway/` (If Present)

Some working copies or internal distributions MAY include a directory
named `gateway/`.

If present, `gateway/` is:

- **NON-PUBLIC**
- **NON-NORMATIVE**
- **OPTIONAL**
- **REPLACEABLE**
- **EXCLUDABLE**

It MUST NOT be:
- required to understand MMS
- referenced as authoritative
- treated as part of the public system definition

Public releases of this repository MAY omit `gateway/` entirely.

---

## Repository Structure (High Level)

.
├── README.md # This file (overview, non-normative)
├── IMPLEMENTATION.md # Implementation boundary guidance
├── SECURITY.md # Security policy
├── CHANGELOG.md # Repository-level history
└── requirements/ # NORMATIVE ROOT


---

## The `requirements/` Directory

`requirements/` contains the **complete MMS specification**.

Key files include:

- `requirements/README.md` — normative scope and interpretation rules  
- `requirements/INDEX.md` — canonical index of all specification documents  
- `requirements/ARCHITECTURE.md` — system architecture  
- `requirements/GLOSSARY.md` — terminology  
- `requirements/DECISIONS.md` — architectural decisions  
- `requirements/RESPONSIBILITIES.md` — role boundaries  
- `requirements/MISUSE.md` — forbidden interpretations  
- `requirements/schemas/` — machine-readable contracts  
- `requirements/modes/` — versioned system modes  
- `requirements/pipelines/` — processing pipelines  
- `requirements/profiles/` — usage and execution profiles  
- `requirements/runs/` — run manifests and examples  

Refer to `requirements/INDEX.md` for the authoritative structure.

---

## Normativity Rules

- Files under `requirements/` are **NORMATIVE by default**
- Examples are **NON-NORMATIVE** unless stated otherwise
- Schemas and contracts are **STRICTLY NORMATIVE**
- Tools are **NON-NORMATIVE**, schemas they validate are normative
- No behavior may be inferred from implementations

---

## Interpretation Rules

1. This repository defines **WHAT**, never **HOW**
2. Implementations must adapt to requirements, not vice versa
3. Absence of an implementation is **not an error**
4. No file outside `requirements/` can impose obligations
5. Requirements are self-contained and complete

---

## Summary

- This is a **requirements-only repository**
- MMS is defined **without reference to any implementation**
- Implementations are optional, private, and out of scope
- `requirements/` is the single source of truth

For implementation boundaries and guidance, see `IMPLEMENTATION.md`.

---
