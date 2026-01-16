# MMS Runs and Artifacts

**Status:** Draft  
**Target version:** 0.2.1  
**Scope:** Operative, normative for all MMS executions  
**Role:** Definition of runs as transactional and audit units

---

## Purpose of This Document

This document defines what a **Run** is in the context of the
**Matrix Management System (MMS)**.

It specifies:
- the role of runs as **transactional units**
- the structure of run artifacts
- append-only and reproducibility rules
- how failures, uncertainty, and non-results are represented

This document is **normative** for all MMS executions.

---

### Clarification — Normative Strength

This document is binding for:
- humans
- automation
- tooling
- historical reconstruction

If any execution contradicts this document,
the execution is invalid under MMS architecture.

---

## Conceptual Role of a Run

A **Run** is the MMS equivalent of a **database transaction log entry**.

It captures:
- *what was attempted*
- *under which configuration*
- *with which inputs*
- *and what artifacts resulted*

A run is **not**:
- a truth claim
- a decision
- a validation step
- a quality judgment

A run is an **explicit, inspectable event**.

---

### Clarification — Run vs. Result

Runs record **events**, not outcomes in the evaluative sense.
The existence of a run does not imply success, usefulness, or correctness.

---

## Why Runs Are First-Class Objects

Runs are first-class because MMS must guarantee:

- reproducibility
- auditability
- comparability over time
- traceability of all claims

Without explicit runs:
- provenance collapses
- QA becomes implicit
- regressions become invisible
- automation becomes unsafe

---

### Architectural Note — Runs as Epistemic Firebreaks

Runs prevent implicit accumulation of authority.
Each run is isolated, attributable, and inspectable.

---

## Run Invariants (Hard Rules)

All runs MUST satisfy the following invariants:

### Append-Only
Runs are never modified or deleted.

If a mistake occurs:
- a new run is executed
- the previous run remains visible

---

### Explicit Inputs
Every run MUST explicitly declare:
- input sources
- source versions or snapshots
- preprocessing assumptions (if any)

Implicit reuse of context is disallowed.

---

### Clarification — Input Exhaustiveness

If an input influences a run,
it must be declared.
Undeclared influence constitutes an invalid run.

---

### Explicit Configuration
Every run MUST record:
- the producer/enricher/translator modes used
- configuration parameters
- model or tool identifiers (if applicable)

---

### Clarification — Configuration Identity

Configuration identity is part of run identity.
Changing configuration without a new run
is architecturally forbidden.

---

### Explicit Outputs
Every run MUST enumerate:
- produced artifacts
- their locations
- their types (claims, relations, conflicts, logs)

---

### Clarification — Empty Output Is Valid

A run that produces no claims or relations
is still a valid run if its outcome is explicit.

---

### Explicit Outcome
Every run MUST record its outcome state,
even if no claims are produced.

---

## Canonical Run Outcomes

Runs may result in one or more of the following **explicit outcomes**:

- **SUCCESS**
  - claims or artifacts were produced
- **NOCLAIM**
  - processing completed, but no admissible claims were extracted
- **UNKNOWN**
  - admissibility could not be determined
- **CONFLICT**
  - incompatible claims were detected or generated
- **STOP**
  - processing was halted due to a rule violation or boundary condition

Outcomes are **descriptive**, not evaluative.

They are part of the audit trail.

---

### Explicit Boundary — Outcome Semantics

Outcomes must never be:
- ranked
- weighted
- interpreted as quality signals
- collapsed into success/failure metrics

---

## Run as the Unit of Comparison

Runs are designed to be:
- comparable across time
- comparable across modes
- comparable across domains

This enables:
- regression detection
- quality trend analysis
- model or pipeline comparison
- domain maturity analysis

Runs do not compete.
They accumulate.

---

### Clarification — Comparison Without Selection

Comparison exists to observe structure,
not to select winners.

Any selection logic must be external.

---

## Recommended Run Directory Structure (Minimal and Human-Readable)

MMS prioritizes **human auditability** and **operational simplicity**.

Therefore, the recommended default for runs is a **flat directory**
with minimal nesting:

```text
runs/
└── run_2026-01-15T10-00-00Z_example/
    ├── manifest.json
    ├── claims.jsonl
    ├── relations.jsonl
    ├── conflicts.jsonl
    ├── sources.list
    ├── pipeline.yaml
    ├── execution.log
    └── run.log.jsonl

{"schema":"mms.conflict.v0.1","record_type":"conflict","conflict_id":"cnf_demo_0001","run_id":"run_2026-01-15T10-00-00Z_example","claim_ids":["clm_demo_0001","clm_demo_0002"],"scope":{"text":"Both claims assert different operating voltages for the same component under the same stated demo scope.","domain":"demo"},"classification":{"kind":"incompatibility","contested":false},"temporal":{"asserted_at":"2026-01-15T10:00:08Z"},"provenance":{"sources":[{"source_id":"src_demo_doc_001","type":"document","locator":"demo://example-source"}],"method":"enricher.conflict.demo.v0"},"created_at":"2026-01-15T10:00:08Z","notes":"Conflict is represented, not resolved."}

