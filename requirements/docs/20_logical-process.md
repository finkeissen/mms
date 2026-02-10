# MMS Logical Process Model

**Status:** Draft  
**Target version:** 0.2.2  
**Scope:** Operative logic, schema-derivable  
**Role:** Defines the canonical execution flow and artifact lifecycle

---

## Purpose of This Document

This document defines the **logical process model** of MMS.

It specifies:
- the canonical sequence of processing stages
- the role of producer / enricher / translator modes in that sequence
- which artifacts are created at each stage
- where STOP / UNKNOWN / NOCLAIM / CONFLICT may be produced
- how append-only and auditability are preserved

This is an **implementation-independent** model.

It is intended to make later schema definitions
largely mechanical.

---

## Design Constraints (Non-Negotiable)

The process model inherits kernel invariants:

- **append-only**
- **provenance required**
- **no truth semantics**
- **explicit alternatives**
- **silent divergence disallowed**

All stages must be expressible without introducing
implicit authority or hidden state.

---

## Canonical Processing Stages

MMS processing is defined in stages.

Not every run must execute all stages,
but **stage order is fixed whenever a stage is used**.

Stages are grouped into:
- **Run setup**
- **Ingestion**
- **Enrichment**
- **Publication**

Each stage produces explicit artifacts.

---

## Stage 0 — Run Setup (Manifest-First)

### Goal
Create a run identity and bind the intended execution to explicit inputs.

### Inputs
- declared source set (references, paths, URLs, snapshots)
- declared processing intent (domain, mode selection)
- declared configuration (parameters)

### Outputs (Artifacts)
- run manifest (created immediately)
- input inventory (explicit list of intended sources)
- configuration snapshot

### Outcome Notes
A run can STOP here if:
- inputs are missing
- source references are undefined
- configuration violates kernel constraints

**Rule:** No processing may begin without a manifest.

---

## Stage 1 — Source Acquisition and Freezing (Explicit Handover)

### Goal
Bind all source material to an explicit, inspectable handover state.

### Inputs
- source declarations from the manifest

### Outputs (Artifacts)
- source snapshot references (hashes, filenames, ids)
- acquisition logs
- optional normalization of source formats (without semantic transformation)

### Outcome Notes
- STOP if sources cannot be acquired as declared
- UNKNOWN if source state is ambiguous or unstable

**Rule:** Claims must never point to a moving target.
They point to a declared snapshot.

---

## Stage 2 — Candidate Extraction (Producer Stage)

### Goal
Generate candidate claims from sources.

This stage may be probabilistic (LLM) or deterministic (parsers).

### Inputs
- frozen sources (Stage 1)
- producer mode configuration

### Outputs (Artifacts)
- candidate claim records (raw candidates)
- extraction logs
- explicit “no candidates” markers if applicable

### Outcome Notes
- NOCLAIM if extraction yields no admissible candidates
- UNKNOWN if extraction cannot determine admissibility
- STOP if producer violates contract formatting requirements

**Rule:** Producers generate candidates, not truth.

---

## Stage 3 — Canonicalization and Contract Conformance (Kernel Gate)

### Goal
Ensure produced candidates conform to the canonical claim contract.

This stage is conceptually a **constraint gate**.

It is expected to become increasingly deterministic over time.

### Inputs
- candidate claim records from Stage 2

### Outputs (Artifacts)
- accepted claims (canonical records)
- rejected candidates (with reasons)
- normalization notes (if any)
- contract validation report

### Outcome Notes
- NOCLAIM if no candidates pass the gate
- STOP if validation cannot be performed
- UNKNOWN if conformance cannot be established

**Rule:** Only accepted claims enter the canonical Matrix.

---

## Stage 4 — Structural Linking (Enricher Stage)

### Goal
Add relations between claims without altering claim identity.

This includes:
- similarity links
- refinement links
- derivation links
- domain-local structure

### Inputs
- accepted claims from Stage 3
- optional domain heuristics

### Outputs (Artifacts)
- relation records
- linking reports
- optional link candidates (separate from accepted relations)

### Outcome Notes
- May produce CONFLICT candidates, but does not resolve them
- Must remain append-only and explicit

**Rule:** Enrichers may add structure, never rewrite claims.

---

## Stage 5 — Conflict Detection and Representation (Enricher Stage)

### Goal
Represent explicit incompatibilities as first-class artifacts.

### Inputs
- accepted claims
- relations (optional)

### Outputs (Artifacts)
- conflict records
- conflict classification notes
- explicit scope/context bindings for incompatibility

### Outcome Notes
- CONFLICT is a valid outcome state
- conflicts may be partial, contested, or time-bound

**Rule:** Conflicts are preserved, not eliminated.

---

## Stage 6 — Quality and Audit Enrichment (Enricher Stage)

### Goal
Attach audit and quality markers without changing epistemic content.

Examples:
- completeness markers
- provenance validation
- input coverage reports
- explicit non-extraction markers (`NOCLAIM` scoped)

### Inputs
- all prior artifacts

### Outputs (Artifacts)
- QA markers
- audit reports
- coverage maps

### Outcome Notes
This stage never changes claim identity.

**Rule:** Quality is additive, not rewriting.

---

## Stage 7 — Publication (Matrix Assembly)

### Goal
Assemble or export the current run outputs into publishable artifacts.

Publication does not decide truth.
It packages the current state.

### Inputs
- canonical claims
- relations
- conflicts
- run manifest and logs

### Outputs (Artifacts)
- Matrix export(s)
- views (optional)
- derived indices (optional)
- publication manifest (optional)

### Outcome Notes
Publication may include multiple exports:
- domain-specific views
- claim×source projections
- time-sliced snapshots

**Rule:** Publication is formatting and packaging, not interpretation.

**Note on indices:** Indices are **derived, optional access artifacts**.
They never add information, never resolve conflicts, and may always be deleted and rebuilt.

---

## Translator Modes (Exceptional Branch)

Translator modes form an explicit branch in the process model.

They may:
- split or merge claims
- re-segment claim granularity
- reinterpret conflict semantics
- map between representation contracts

Translator usage is always explicit:
- a run is marked as translator-run
- resulting outputs are a **new Matrix instantiation** or an explicit import step
- no silent merge into canonical outputs is permitted

---

## Deterministic vs Probabilistic Responsibilities

MMS is expected to evolve toward stronger determinism over time.

### Probabilistic components (typical)
- candidate extraction (LLMs)
- weak classification tasks

### Deterministic components (target)
- contract validation
- normalization and formatting
- run orchestration
- audit and completeness checks
- view generation and derived indexing

The kernel contract is stable across this evolution.

---

## Artifact Classes (Abstract)

Across stages, MMS produces five abstract artifact classes:

1. **Manifests**
   - run manifests, publication manifests
2. **Records**
   - claims, relations, conflicts
3. **Reports**
   - validation, QA, coverage, comparison
4. **Logs**
   - execution traces and diagnostics
5. **Snapshots**
   - source freezes, configuration captures

Schemas will later formalize these.

---

## Summary

The MMS logical process model:

- starts with a manifest
- freezes sources explicitly
- produces candidate claims (producers)
- gates candidates into canonical records (kernel conformance)
- adds relations and conflicts (enrichers)
- attaches QA and audit layers (enrichers)
- publishes Matrix exports as artifacts
- treats translators as explicit, exceptional branches

This flow preserves:
- append-only semantics
- provenance and auditability
- explicit alternatives and dissensus
- separation between extraction and persistence

