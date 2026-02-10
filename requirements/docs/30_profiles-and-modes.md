# MMS Profiles and Modes

**Status:** Draft  
**Target version:** 0.2.2  
**Scope:** Operative role model, contract-bound  
**Role:** Defines allowed behaviors of MMS execution modes

---

## Purpose of This Document

This document defines the **profile and mode model** of the
**Matrix Management System (MMS)**.

It specifies:
- which categories of modes exist
- what each category is allowed to do
- which kernel invariants apply
- how modes relate to runs and artifacts

This document is **normative** for all MMS implementations.

It does not define:
- truth or correctness
- extraction quality
- automation strategy
- domain semantics

---

## Why Profiles and Modes Exist

MMS explicitly separates:

- **what may exist** (kernel contract)
- **what happens when** (logical process model)
- **who may do what** (profiles and modes)

Without this separation:
- pipelines acquire implicit authority
- extraction logic leaks into epistemic semantics
- auditability and reproducibility collapse

Profiles and modes exist to make **behavior explicit, bounded, and inspectable**.

---

## Terminology

- **Profile**  
  A class of behavior with clearly defined permissions and limits.

- **Mode**  
  A concrete implementation or configuration operating under a profile.

Profiles define **what is allowed**.  
Modes define **how it is done**.

Profiles confer permission, not epistemic authority.

---

## Canonical Profiles

MMS defines exactly **three canonical profiles**:

1. **Producer**
2. **Enricher**
3. **Translator**

No other profile has kernel-level permission.

Any additional operational roles
must reduce to one of these profiles explicitly.

---

## 1. Producer Profile

### Role

Producer modes are responsible for
**generating candidate claims** from sources.

They are the **only profile permitted to introduce new claims**
into MMS processing.

---

### Allowed Actions

Producer modes MAY:

- read declared, frozen source material
- generate candidate claim records
- attach extraction metadata
- explicitly emit `NOCLAIM` or `UNKNOWN` outcomes

Producer modes MAY NOT:

- alter existing canonical claims
- delete or overwrite artifacts
- resolve conflicts
- rank claims by validity or preference
- introduce truth semantics

---

### Characteristics

Producer modes are often:
- probabilistic
- model-driven
- domain-specific

Typical examples include:
- prompt-based LLM extraction
- rule-based or pattern-based parsers
- domain-tailored extraction pipelines

Probabilistic behavior is permitted,
but must always be explicitly bounded by runs and manifests.

---

### Contract Obligations

All producer outputs MUST:

- reference the producing run
- conform to the canonical claim schema
- include explicit provenance
- be eligible for kernel validation (Stage 3)

Candidate claims that do not conform
are rejected at the kernel gate
and do not enter the canonical Matrix.

---

## 2. Enricher Profile

### Role

Enricher modes **add structure, metadata, and diagnostics**
to existing canonical artifacts.

They **never change epistemic content**.

---

### Allowed Actions

Enricher modes MAY:

- add relations between claims
- create conflict records
- attach QA, audit, or coverage markers
- annotate uncertainty or incompleteness
- generate reports, views, or derived access artifacts

Enricher modes MAY NOT:

- create new claims
- alter claim assertions
- split or merge claim identities
- remove or overwrite artifacts

---

### Characteristics

Enricher modes are typically:
- deterministic
- rule-based
- audit-oriented

Examples include:
- conflict detection heuristics
- provenance consistency checks
- coverage analysis
- deduplication suggestions (explicit and non-destructive)

---

### Contract Obligations

All enricher outputs MUST:

- reference existing canonical artifacts
- preserve append-only semantics
- carry provenance and timestamps
- remain reversible by inspection

No enricher may introduce hidden state
or implicit semantic decisions.

---

## 3. Translator Profile (Exceptional)

### Role

Translator modes perform **explicit representation-changing transformations**.

They exist to:
- experiment with alternative claim granularities
- migrate between schema versions
- integrate or map external representations

Translator modes are **explicitly exceptional**.

---

### Allowed Actions

Translator modes MAY:

- split claims into finer-grained claims
- merge claims into composite claims
- reinterpret relation or conflict semantics
- map between different representation contracts

Translator modes MAY NOT:

- silently modify canonical artifacts
- merge results implicitly into the canonical Matrix

---

### Mandatory Constraints

Translator usage MUST:

- be explicitly declared in the run manifest
- produce a new Matrix instantiation
  or an explicit import step
- never overwrite canonical artifacts

Silent divergence is explicitly disallowed.

---

## Profile Interaction Rules

- Producer modes always execute **before** enricher modes.
- Enricher modes may be chained freely.
- Translator modes form an explicit branch,
  not part of the default pipeline.

No mode may bypass kernel validation
or run-level auditability.

---

## Modes and Runs

Each run MUST declare:
- which modes were used
- their profile classification
- their configuration identifiers

Modes are part of the run’s permanent audit trail.

---

## Modes and Automation

Automation systems may:
- schedule runs
- select modes
- manage execution

Automation systems may NOT:
- change profile permissions
- bypass kernel constraints
- reinterpret or rewrite artifacts

Automation is an operational convenience,
not an epistemic authority.

---

## Non-Goals

Profiles and modes do NOT:

- encode epistemic authority
- decide correctness or truth
- express preference or ranking
- define domain semantics

They define **operational permission only**.

---

## Summary

MMS profiles and modes:

- make behavior explicit and bounded
- prevent silent semantic drift
- separate extraction from structure
- preserve auditability and dissensus

Everything a mode does
must be explainable in terms of:
- its profile
- the kernel contract
- the run that executed it

