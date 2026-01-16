# INDEX

## Repository Cascade Index  
**Epistemic Architecture · Operative Systems · Instantiated Artifacts**

---

## Purpose of This File

This file is the **canonical navigation and orientation index**
for the entire repository cascade.

It exists to:
- make responsibilities explicit
- prevent layer confusion
- provide a stable entry point for readers, auditors, and maintainers
- avoid implicit authority by structural clarity

This file contains **no epistemic content** and **no decisions**.
It is purely structural.

---

## How to Read This Index

The system is organized as a **strict cascade of responsibility**.

Each layer:
- depends on the previous one
- must not assume the role of any other layer
- increases specificity without increasing authority

Reading order matters.

---

## Layer 1 — Epistemic Kernel (Neutral)

### Repository: `research-program`

**Purpose:**  
Define the conditions under which scientific reasoning is admissible.

**Produces:**  
- rules
- constraints
- STOP conditions

**Does NOT produce:**  
- claims  
- data  
- truth  
- results  

**Key Files:**

- `1.README_research-program+mms+matrix.md`  
  → Cross-layer architecture contract and responsibility boundaries

- `5.README.research-program.md`  
  → Epistemic kernel, neutrality rules, contexts, STOP zones

---

## Layer 2 — Operative System (Rule-Bound, Non-Neutral)

### Repository: `mms` (Matrix Management System)

**Purpose:**  
Manage epistemic artifacts (claims, relations, conflicts)
under explicit structural constraints.

**Produces:**  
- structured epistemic artifacts
- explicit provenance
- append-only history

**Does NOT produce:**  
- truth  
- rankings  
- decisions  
- recommendations  

**Key Files:**

- `README.md`  
  → MMS scope, role, and non-goals

- `ARCHITECTURE.md`  
  → Non-negotiable architectural invariants

- `DECISIONS.md`  
  → Record of accepted architectural decisions

- `GLOSSARY.md`  
  → Normative terminology (authoritative)

---

## Layer 3 — Instantiated State (Non-Authoritative Product)

### Repository: `matrix`

**Purpose:**  
Public stress test of structured epistemic artifacts
under real-world domains and pressure.

**Produces:**  
- instantiated epistemic states
- conflicts, gaps, contradictions
- structural evidence of survivability

**Does NOT produce:**  
- knowledge  
- facts  
- decisions  
- liability-bearing statements  

**Key Files:**

- `README.md`  
  → Matrix semantics, non-authority, reading rules

- `domains/`  
  → Domain-specific interpretation spaces

- `artifacts/`  
  → Consolidated canonical artifacts

- `runs/`  
  → Execution snapshots

- `raw/`  
  → Non-normative, pre-matrix material (explicitly excluded)

---

## Outside the System (Explicitly Out of Scope)

The following are **not part of this architecture**:

- decision-making systems
- policy engines
- governance processes
- commercial knowledge bases
- operational AI products

Any system consuming Matrix output must:
- re-establish its own authority
- assume full responsibility for decisions
- not attribute epistemic authority backward

---

## Responsibility Summary (One-Line)

| Layer | Responsibility | Authority |
|------|---------------|-----------|
| research-program | epistemic legitimacy | none |
| MMS | structural enforcement | none |
| Matrix | representation & stress | none |
| external systems | decisions & action | full |

---

## Canonical Rule

> **If something appears to decide, recommend, conclude, or assert truth,  
> it is already outside this system.**

---

## Maintenance Rules

- This index may only change when:
  - repositories are added or removed
  - responsibility boundaries shift (rare)
- It must never contain:
  - epistemic claims
  - examples used as evidence
  - domain-specific content

Its only job is **orientation without authority**.

---

## Status

This file is **structural glue**.

If this file feels boring, it is doing its job.

