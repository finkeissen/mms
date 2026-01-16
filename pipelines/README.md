# pipelines/

Pipelines are implementations of modes and stage sequences.

They are replaceable clients of the MMS kernel contract.
They MUST NOT redefine kernel semantics.

Subdirectories group implementation strategies:
- prompt/
- python/
- hybrid/

---

## Purpose of Pipelines

Pipelines define **how runs are orchestrated**, not **what is decided**.

They exist to:
- sequence runs
- coordinate tools
- apply configurations
- manage execution flow

Pipelines do **not**:
- determine truth
- resolve conflicts
- rank claims
- validate correctness
- introduce epistemic authority

They are **procedural**, not epistemic.

---

### Clarification — Pipeline vs. Architecture

Pipelines are **not part of MMS architecture**.
They are clients of the architecture.

If a pipeline requires a change in architectural rules to function,
the pipeline is invalid.

---

## Relationship to Runs

Every pipeline execution consists of one or more **explicit Runs**.

Rules:
- each run must be separately recorded
- run boundaries must not be blurred
- pipelines must never merge runs implicitly
- retries must be explicit and recorded as new runs

> **A pipeline may fail without producing runs.  
> It may also stop after producing partial runs.**

Both outcomes are valid.

---

### Clarification — No Pipeline-Level State

Pipelines must not maintain hidden state
that influences later runs without explicit declaration.

Any such state constitutes an implicit input
and violates run invariants.

---

## Replaceability and Non-Authority

Pipelines are **replaceable by design**.

This implies:
- no pipeline is canonical
- no pipeline has epistemic priority
- no pipeline output is privileged

Two different pipelines may:
- process the same sources
- produce different claims
- surface different conflicts

This is expected and acceptable.

---

### Architectural Note — Pipeline Diversity

Diversity of pipelines is a diagnostic asset.
Uniformity is not a goal.

---

## Subdirectory Semantics

### `prompt/`

Pipelines primarily driven by structured prompts
and language models.

Risks:
- implicit summarization
- silent aggregation
- hidden defaults

All such risks must be explicitly mitigated
at the pipeline documentation level.

---

### `python/`

Pipelines implemented primarily in code.

Risks:
- hidden heuristics
- implicit filtering
- stateful transformations

Code pipelines must be especially strict
about explicit configuration and logging.

---

### `hybrid/`

Pipelines combining prompt-driven and code-driven stages.

Risks:
- unclear responsibility boundaries
- mixed failure semantics
- obscured provenance

Hybrid pipelines must document
stage boundaries explicitly.

---

## Prohibited Pipeline Behaviors

The following behaviors are **architecturally forbidden**:

- implicit conflict resolution
- default claim prioritization
- silent schema coercion
- best-effort extraction without STOP
- collapsing multiple runs into one output
- modifying run artifacts post hoc
- bypassing kernel validation

If a pipeline relies on any of these,
it must not be used.

---

## STOP Compatibility

Pipelines must be STOP-compatible.

This means:
- STOP may occur at any stage
- STOP must halt further execution
- STOP must be recorded explicitly
- STOP must not be “handled away”

Producing artifacts after STOP
is an architectural violation.

---

### Clarification — STOP Is Not an Error

STOP is not an exception to catch.
It is a correct outcome.

---

## Documentation Requirements

Every pipeline directory MUST contain
a `README.md` that documents:

- intended purpose
- admissible inputs
- run structure
- STOP conditions
- known failure modes
- explicit non-goals

Undocumented pipelines are invalid.

---

## Relationship to Modes

Historically, pipelines evolved from modes.

Under the current architecture:
- modes are frozen historical artifacts
- pipelines are the active execution layer

No pipeline may claim legitimacy
by reference to a historical mode.

---

## Summary

Pipelines exist to **execute structure under constraint**.

They are:
- optional
- replaceable
- non-authoritative
- failure-tolerant

If a pipeline feels powerful, automatic,
or decisive, it is almost certainly wrong.

