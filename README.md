# MMS – Matrix Management System

This repository contains the **public, normative requirements** of the
**Matrix Management System (MMS)**.

It is intentionally a **requirements-only** repository.

The purpose of this repository is to define **what MMS is and guarantees** —
not how it is implemented.

---

## Scope and Intent

This repository defines the **authoritative public contract** of MMS.

It specifies:
- responsibilities and obligations,
- public concepts and terminology,
- normative rules, constraints, and invariants,
- schemas, formats, and validation requirements,
- versioning and change rules for public behavior.

Anything not defined in this repository is **not part of the MMS public contract**.

This repository does **not** contain:
- implementation code,
- runtime systems,
- - implementation code (e.g., gateways, runtimes, processing systems),
- pipelines, tools, or operational logic.

---

## Repository Structure

### `requirements/` — Public, Normative, Authoritative

The `requirements/` directory is the **single source of truth** for MMS.

All content in this directory is:
- **public**
- **normative**
- **authoritative**
- **versioned and auditable**

If something is defined in `requirements/`, implementations are expected to
**comply exactly**.

If something is **not** defined in `requirements/`, it is **not guaranteed** by MMS.

Start here:
- `requirements/README.md`
- `requirements/INDEX.md`

---

## Authority Model

Authority in MMS flows strictly in one direction:

requirements → implementation


This means:
- Requirements define obligations and guarantees.
- Implementations realize those guarantees.
- Implementations must not reinterpret, weaken, or extend requirements.
- Undefined behavior is considered **forbidden**, not implicit.

In case of any contradiction:
> **The requirements always take precedence.**

---

## Implementation

Implementations of MMS (e.g., gateways, runtimes, processing systems) exist outside this public contract repository.
are **intentionally not part of this public repository**.

Implementations may exist in separate repositories or internal systems.
They are expected to:
- consume these requirements,
- declare their own conformance,
- remain strictly subordinate to the requirements defined here.

This repository defines **what MMS guarantees**.  
Implementations define **how those guarantees are realized**.

---

## Contributing

This repository accepts contributions related to:
- requirements,
- contracts,
- schemas,
- normative documentation,
- clarifications of public guarantees.

It does **not** accept:
- implementation code,
- runtime logic,
- tooling or execution pipelines,
- experimental or operational artifacts.

See `CONTRIBUTING.md` for details.

---

## Versioning and Change Policy

Public behavior of MMS is defined exclusively by the contents of
the `requirements/` directory.

Any change to public behavior requires:
- an explicit change to the relevant requirement,
- clear documentation of intent,
- appropriate versioning,
- an auditable change history.

Backward-incompatible changes must be explicit and justified.

---

## Architecture Overview

The architecture consists of four strictly separated layers:

0. **Legacy**  
   Preserves prior assumptions,
   unresolved contradictions,
   structural patterns,
   and contextual material
   that exist *before* admissibility,
   governance,
   or instantiation.
           ↓
1. **Research Program (RP)**  
   Defines ontological primitives
   and admissible structural forms.
           ↓
2. **Meta-Management System (MMS)**  
   Enforces admissibility rules
   without structural or epistemic authority.
           ↓
3. **Matrix**  
   Records concrete instantiations,
   conflicts,
   STOPs,
   and explicit absences.


The Matrix contains only what remains after RP definition and MMS enforcement.

No layer may absorb the role of another.

## License and Security

- License information is available in `LICENSE`.
- Security reporting guidelines are defined in `SECURITY.md`.

---

## Status

MMS requirements are under active development and refinement.

This repository is designed to be:
- stable in structure,
- explicit in guarantees,
- conservative in public commitments,
- clear about authority and responsibility boundaries.

## Role in the epistemic flow

MMS operationalizes the admissibility rules defined in the Research Program.

It does not create knowledge.
It manages transitions.

MMS determines whether:
- artifacts may enter the Matrix,
- must remain absent,
- or trigger STOP and regress to Legacy.

## STOP as an operational outcome

Within MMS, STOP is not an error condition.

STOP indicates that admissibility cannot be established under the current context.

When STOP occurs:
- transitions are blocked,
- the Matrix records the state,
- unresolved structures may be preserved in Legacy.

## Non-authority clarification

MMS enforces structure without acquiring epistemic authority.

It does not:
- validate truth,
- resolve disagreement,
- rank evidence,
- or produce decisions.

Its role is constraint enforcement and state management.

## Interfaces

- Research Program → defines admissibility rules
- MMS → enforces transitions and STOP
- Matrix → records resulting epistemic states
- Legacy → preserves unresolved or inadmissible structures

