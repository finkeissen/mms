# MMS Glossary

This glossary defines **normative terms** used throughout the
Matrix Management System (MMS) documentation.

If a term is used ambiguously or inconsistently elsewhere,
the definition in this document is authoritative.

---

## Artifact

A structured, schema-bound object managed by MMS.

Artifacts are:
- immutable (append-only semantics)
- provenance-rich
- explicitly typed

Canonical artifact types are:
- Claim
- Relation
- Conflict

Derived artifacts are not canonical.

---

## Canonical

Refers to artifacts, structures, or documents that are
**architecturally authoritative**.

Canonical artifacts:
- originate from runs
- are schema-validated
- are append-only
- define the official state of the system

Non-canonical artifacts may be derived, historical, or auxiliary.

---

## Claim

An atomic epistemic assertion extracted from a source.

A claim:
- states something that *may* be true
- does not assert correctness
- may conflict with other claims
- exists independently of interpretation

Claims are never edited.
Corrections result in new claims.

---

## Conflict

An explicit artifact representing incompatibility
between two or more claims.

A conflict:
- does not imply error
- does not require resolution
- may persist indefinitely
- is never resolved implicitly

Absence of a conflict does not imply agreement.

---

## Derived Artifact

An artifact computed from canonical artifacts.

Examples:
- indices
- views
- projections
- summaries
- rankings
- graphs

Derived artifacts:
- are non-canonical
- may be deleted and rebuilt
- never add information
- never resolve conflicts

---

## Hash

A cryptographic digest used to ensure integrity and identity.

Hashes provide:
- immutability guarantees
- reproducibility
- auditability

Hashes do not provide meaning, trust, or truth.

---

## Kernel

The minimal, passive core of MMS.

The kernel:
- enforces architectural invariants
- validates schemas
- enforces append-only semantics
- contains no heuristics
- has no domain knowledge

The kernel never decides truth.

---

## Mode

A historical configuration bundling profiles, tools, and processes.

Modes:
- represent exploratory or deprecated states
- are preserved for traceability
- are not canonical
- must not be extended

Modes explain evolution, not current operation.

---

## Process (Logical Process)

An explicit definition of allowed stages and transitions
between runs.

A process:
- defines ordering constraints
- defines failure modes
- does not decide truth
- does not modify artifacts

Processes orchestrate, they do not judge.

---

## Profile

A permission definition describing what actions are allowed.

Profiles:
- define capabilities
- do not imply authority
- do not encode trust
- do not rank contributors

Profiles constrain behavior, not meaning.

---

## Relation

A structural link between claims.

Relations:
- describe alternatives, dependencies, support, or structure
- do not assert correctness
- may participate in conflicts
- are schema-bound

Relations add structure, not resolution.

---

## Run

The atomic execution and audit unit of MMS.

A run:
- records inputs, configuration, and outputs
- is immutable once completed
- is append-only
- is the sole origin of canonical artifacts

> No run, no claim.

---

## Schema

A formal, versioned description of artifact structure.

Schemas:
- define shape and constraints
- do not define meaning
- are validated at the kernel boundary
- are normative

Invalid artifacts never enter the system.

---

## Tool

An external program or service interacting with MMS.

Tools:
- operate via explicit runs
- may assist humans or automation
- are replaceable
- never bypass kernel invariants

Tools are optional.

---

## Truth

An epistemic property **explicitly out of scope** for MMS.

MMS does not:
- determine truth
- enforce correctness
- resolve disagreement

Truth judgments may exist externally,
but never implicitly inside MMS.

---

## View

A derived representation of canonical artifacts.

Views:
- are non-canonical
- may aggregate or project data
- never add information
- may be deleted and rebuilt

Views exist for convenience only.

---

## Summary

This glossary defines the **shared language** of MMS.

If a term is unclear:
- consult this document
- prefer explicit definitions
- avoid overloaded terminology

