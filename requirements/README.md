# MMS Requirements

This directory contains the **public, normative requirements** for the MMS system.

All documents under `requirements/` define the **contractual, conceptual, and structural
expectations** of MMS. They describe **what MMS is**, **what it must guarantee**, and
**how its outputs are structured**, independent of any concrete implementation.

---

## Scope and Authority

The contents of this directory are **normative**.

They define:
- conceptual models and terminology
- required system behavior and guarantees
- data structures, schemas, and contracts
- process expectations and invariants

Anything **outside** this directory is **non-normative** unless explicitly stated otherwise.

---

## Public vs. Non-Public Content

This repository distinguishes strictly between:

- **Public requirements** (this directory)
- **Non-public implementations** (e.g. gateways, runtimes, execution systems)

The **public repository release** contains **no implementation code**.

Implementations MAY exist:
- in non-public distributions
- in separate repositories
- in internal or deployment-specific environments

They are **explicitly out of scope** for this requirements repository.

---

## Relationship to Implementations (e.g. `gateway/`)

Some MMS deployments may include a directory commonly referred to as `gateway/`.

The gateway:
- represents a **concrete implementation** of MMS requirements
- is **non-normative**
- is **not part of the public repository release**
- MUST NOT be relied upon when interpreting requirements

Any `gateway/` directory:
- MAY be used internally for validation, experimentation, or execution
- MAY be excluded entirely from public distributions
- MUST NOT be considered part of the public contract

The authoritative definition of MMS behavior is **always** the requirements
documents contained in this directory.

---

## Directory Overview

The `requirements/` directory is organized into thematic areas:

- `ARCHITECTURE.md`  
  High-level structural and conceptual system architecture

- `INDEX.md`  
  Canonical index of all requirement documents and their relationships

- `GLOSSARY.md`  
  Normative terminology and definitions

- `DECISIONS.md`  
  Design decisions and their rationales

- `RESPONSIBILITIES.md`  
  Responsibility boundaries and role expectations

- `MISUSE.md`  
  Explicitly disallowed interpretations and usages

- `docs/`  
  Detailed requirement documents and conceptual deep dives

- `schemas/`  
  Machine-readable schema definitions

- `modes/`, `pipelines/`, `profiles/`, `runs/`, `tools/`  
  Structured requirement sets, examples, and reference artifacts  
  (normative unless explicitly marked as examples)

---

## Examples and Reference Artifacts

Some subdirectories contain **examples**, **reference artifacts**, or **illustrative data**.

Unless explicitly stated otherwise:
- examples are **non-normative**
- schemas and contracts remain **normative**
- example executions do **not** define required behavior

Normative authority is always defined by the surrounding documentation.

---

## Implementation Disclaimer

This requirements repository intentionally avoids prescribing:
- specific technologies
- concrete execution strategies
- deployment layouts
- operational tooling

Such choices belong to implementations and are **outside the scope** of this repository.

For further clarification on implementation boundaries, see `IMPLEMENTATION.md`
in the repository root.

---

## Summary

- `requirements/` defines the **public MMS contract**
- implementations (e.g. gateways) are **optional, non-public, and non-normative**
- public releases of this repository contain **requirements only**
- no implementation is required to understand or apply MMS requirements

If a statement is unclear, **the requirements take precedence** over any implementation.

