# MMS – Glossary (PUBLIC)

This document defines the **binding terminology**
of the **Matrix Management System (MMS)**.

All terms in this glossary are **normative**.
In case of interpretation disputes, this glossary prevails.

---

## Artifact

An **artifact** is a canonical, persisted unit within MMS.

Artifacts are:
- append-only
- schema-bound
- provenance-rich
- auditable

Artifacts are **not facts**, but structured representations
of statements, relationships, or contradictions.

---

## Claim

A **claim** is an artifact representing an explicit statement made by a source.

A claim:
- is neither true nor false within the system
- is associated with a source, time, and context
- has no implicit priority or authority

---

## Relation

A **relation** is an artifact describing a structural relationship
between artifacts.

Relations:
- contain no evaluation
- express no authority
- may represent alternatives, dependencies, or references

---

## Conflict

A **conflict** is an artifact representing an explicit incompatibility
between artifacts.

Conflicts:
- are not errors
- may persist indefinitely
- are never resolved automatically

---

## Canonical

**Canonical** refers to artifacts or structures
that are part of the **binding system state**.

Canonical artifacts:
- originate exclusively from runs
- follow append-only semantics
- form the basis for all derivations

---

## Derived

**Derived** refers to structures
that are produced from canonical artifacts.

Derived structures:
- are not canonical
- contain no knowledge
- may be deleted at any time
- must be reproducible

Examples include indices, views, mirrors, and snapshots.

---

## Run

A **run** is the atomic execution and audit unit of MMS.

A run:
- has explicit inputs
- executes under a defined configuration
- produces artifacts or correctly ends in STOP / NOCLAIM
- is immutable

> No run → no artifact.

---

## STOP

**STOP** is a valid and expected run outcome.

STOP occurs when:
- structural admissibility is violated
- implicit authority would be introduced
- high-stakes requirements are requested

STOP:
- produces no artifacts
- requires no fallback response
- preserves system integrity

---

## NOCLAIM / Absence

**NOCLAIM** (or absence) denotes a run outcome
in which no artifacts are produced
without an error occurring.

NOCLAIM is:
- not STOP
- not a failure
- a correct and neutral outcome

---

## Kernel

The **kernel** is the minimal MMS component
that enforces architectural invariants.

The kernel:
- validates schemas
- protects append-only semantics
- contains no semantics
- makes no decisions

---

## Process

A **process** defines permitted sequences of runs
and their abort conditions.

Processes:
- orchestrate execution
- do not decide outcomes
- may terminate in STOP or failure

---

## Profile

A **profile** defines permissions within the system.

Profiles:
- regulate capabilities
- confer no authority
- have no epistemic priority

---

## Tool

A **tool** is an external system or software
used within a run.

Tools:
- have no authority
- make no decisions
- are replaceable
- operate only through explicit runs

---

## Provenance

**Provenance** describes the explicit origin of an artifact.

It includes, at minimum:
- source
- time
- context
- run identity

Provenance is mandatory and non-optional.

---

## Authority

**Authority** refers to the attribution of validity,
correctness, or priority.

MMS:
- does not create authority
- does not manage authority
- does not delegate authority implicitly

Authority always exists outside the system.

---

## Auditability

**Auditability** is the ability
to fully trace and inspect all state changes.

Auditability requires:
- append-only history
- explicit runs
- stable identities
- complete provenance

---

## Summary

- Terms are **precisely defined**
- There are **no implicit meanings**
- Semantic deviations are errors
- Implementations must use these terms exactly

