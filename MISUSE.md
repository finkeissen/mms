# MISUSE

## Misuse and Abuse Scenarios (Explicit)

---

## Purpose of This Document

This document enumerates **known and foreseeable misuse scenarios**
for the repository cascade:

- `research-program`
- `mms`
- `matrix`

Its purpose is **preventive**.

It exists to:
- surface structural misuse risks early
- make boundary violations explicit
- prevent implicit authority transfer
- support audits and reviews

This document is **normative**.
Ignoring it is an architectural violation.

---

## General Rule

> **If a use case depends on conclusions, decisions, or truth,
> it is incompatible with this system by design.**

This is not a limitation.
It is the defining property.

---

## Category A — Epistemic Misuse

### A1. Treating the Matrix as a Knowledge Base

**Description:**  
Using Matrix artifacts as if they represented
established facts or current knowledge.

**Why This Is Misuse:**  
The Matrix preserves claims and conflicts without resolution.
Treating it as knowledge collapses epistemic uncertainty.

**Indicators:**
- citations of Matrix artifacts as facts
- “according to the Matrix” used as authority
- absence of conflict discussion

**Correct Handling:**  
Matrix artifacts may be cited **only** as representations of claims,
never as statements about reality.

---

### A2. Inferring Truth from Structure

**Description:**  
Assuming that structural properties
(e.g. frequency, connectivity, persistence)
imply correctness or likelihood.

**Why This Is Misuse:**  
Structure encodes representation, not validation.

**Indicators:**
- “most connected claim”
- “longest surviving statement”
- “dominant narrative”

**Correct Handling:**  
Any inference from structure to truth
must happen outside the system
with explicit responsibility.

---

### A3. Collapsing Conflict into Synthesis

**Description:**  
Producing summaries or syntheses
that eliminate visible disagreement.

**Why This Is Misuse:**  
Conflict is epistemic state, not noise.

**Indicators:**
- automatic summaries
- “overall conclusion” sections
- merged claims without explicit conflict artifacts

**Correct Handling:**  
Conflict must remain explicit.
Any synthesis must be external, documented, and reversible.

---

## Category B — Operative Misuse

### B1. Silent Automation

**Description:**  
Allowing tools or pipelines to create or modify
canonical artifacts without explicit runs.

**Why This Is Misuse:**  
It destroys provenance and accountability.

**Indicators:**
- artifacts without run IDs
- undocumented automation
- background processes writing state

**Correct Handling:**  
All artifact creation must occur via explicit runs.

---

### B2. Implicit Defaults

**Description:**  
Introducing defaults that shape outcomes
without explicit representation.

**Why This Is Misuse:**  
Defaults encode hidden decisions.

**Indicators:**
- undocumented parameters
- implicit filtering
- auto-pruning

**Correct Handling:**  
All defaults must be explicit, documented, and auditable.

---

### B3. Treating Tools as Authorities

**Description:**  
Assuming tool output is more correct or trustworthy
than other runs.

**Why This Is Misuse:**  
Tools have no epistemic privilege.

**Indicators:**
- “the model says”
- preferential treatment of automated runs
- suppression of human-generated artifacts

**Correct Handling:**  
Tool output is treated identically to any other run.

---

## Category C — Governance and Responsibility Misuse

### C1. Using Matrix to Justify Decisions

**Description:**  
Citing Matrix artifacts as justification
for actions, policies, or obligations.

**Why This Is Misuse:**  
The system explicitly refuses liability.

**Indicators:**
- decision memos referencing Matrix as authority
- policy documents citing Matrix conclusions

**Correct Handling:**  
Decisions must establish their own authority and evidence.

---

### C2. Shifting Liability Backward

**Description:**  
Attributing responsibility for outcomes
to the system or its maintainers.

**Why This Is Misuse:**  
Responsibility ends at representation.

**Indicators:**
- “the system told us”
- blame deflection to architecture

**Correct Handling:**  
Responsibility always lies with the decision-maker.

---

## Category D — Structural Misuse

### D1. Normalizing Heterogeneity Away

**Description:**  
Forcing schema, terminology, or language alignment prematurely.

**Why This Is Misuse:**  
It erases epistemic variation before testing.

**Indicators:**
- enforced global schemas
- mandatory terminology harmonization
- silent translation

**Correct Handling:**  
Heterogeneity must be preserved until explicitly analyzed.

---

### D2. Treating Derived Artifacts as Canonical

**Description:**  
Using views, summaries, or indices
as if they were authoritative.

**Why This Is Misuse:**  
Derived artifacts are disposable.

**Indicators:**
- citations of views as source
- edits to derived state
- persistence assumptions

**Correct Handling:**  
Only canonical artifacts may be cited as state.

---

## Category E — Process Misuse

### E1. Avoiding STOP

**Description:**  
Forcing progress when STOP conditions are met.

**Why This Is Misuse:**  
STOP protects epistemic integrity.

**Indicators:**
- retry loops without change
- fallback heuristics
- “best effort” outputs

**Correct Handling:**  
STOP must be accepted as a valid outcome.

---

### E2. Treating Failure as Error

**Description:**  
Interpreting epistemic failure
as system malfunction.

**Why This Is Misuse:**  
Failure is a valid signal.

**Indicators:**
- suppression of failed runs
- deletion of incomplete artifacts

**Correct Handling:**  
Failures must be preserved and inspected.

---

## Enforcement and Auditing

Misuse detection relies on:

- `AUDIT.md`
- architectural reviews
- explicit documentation
- peer inspection

There is no automatic enforcement.

---

## Final Statement

> **This system is easy to use incorrectly.  
> That is unavoidable.  
> Making misuse visible is the only defense.**

---

## Status

This document is **preventive infrastructure**.

It should evolve only to:
- enumerate new misuse patterns
- clarify boundaries
- harden responsibility separation

Never to legitimize misuse.

