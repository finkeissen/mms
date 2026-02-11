# INDEX.md

## Repository Purpose

This repository defines the **normative specification, contracts, schemas, and documentation**
for the **MMS (Matrix Management System)**.

It is **not** an implementation repository.

No executable system, runtime, gateway, service, or deployment is provided here.

---

## Normativity Legend

- **NORMATIVE**  
  Binding specification. Implementations MUST conform.

- **NON-NORMATIVE**  
  Informational, explanatory, historical, or illustrative content.

- **NON-PUBLIC**  
  Content that MUST NOT be published, relied upon, or assumed to exist by third parties.

---

## Root-Level Files

| Path | Role | Normativity |
|-----|-----|-------------|
| `README.md` | Repository overview | NON-NORMATIVE |
| `CHANGELOG.md` | Specification history | NON-NORMATIVE |
| `CONTRIBUTING.md` | Contribution rules | NON-NORMATIVE |
| `SECURITY.md` | Security policy | NON-NORMATIVE |
| `IMPLEMENTATION.md` | Implementation guidance | NON-NORMATIVE |
| `AUDIT_COMPLETENESS.md` | Audit checklist | NON-NORMATIVE |
| `CLEANUP.md` | Maintenance notes | NON-NORMATIVE |
| `ToDo` | Internal notes | NON-NORMATIVE |

---

## Directory: `requirements/`  (NORMATIVE ROOT)

All content under `requirements/` defines the **authoritative MMS specification**.

### Core Documents

| Path | Description |
|-----|-------------|
| `requirements/README.md` | Normative scope and rules |
| `requirements/INDEX.md` | Canonical index (this file) |
| `requirements/LICENSE` | Licensing |
| `requirements/ARCHITECTURE.md` | System architecture |
| `requirements/DECISIONS.md` | Architectural decisions |
| `requirements/GLOSSARY.md` | Terminology |
| `requirements/RESPONSIBILITIES.md` | Role definitions |
| `requirements/AUDIT.md` | Audit requirements |
| `requirements/MISUSE.md` | Misuse constraints |
| `requirements/CHANGELOG.md` | Spec change history |
| `requirements/CONTRIBUTING.md` | Spec contribution rules |

---

## Directory: `requirements/docs/`

Conceptual and theoretical foundations.

| Path | Description |
|-----|-------------|
| `00_super.manifest.md` | Global manifest |
| `10_kernel-contract.md` | Kernel contract |
| `11_epistemic_hygiene.md` | Epistemic constraints |
| `15_epistemics.md` | Epistemic framework |
| `20_logical-process.md` | Logical process model |
| `25_stage-to-artifacts-mapping.md` | Stage mappings |
| `30_profiles-and-modes.md` | Profiles and modes |
| `35_matrix-identity-and-versioning.md` | Versioning |
| `40_automation-and-ops.md` | Ops considerations |

All files: **NORMATIVE unless explicitly stated otherwise inside the file**.

---

## Directory: `requirements/kernel/`

| Path | Description |
|-----|-------------|
| `README.md` | Kernel definition |

**NORMATIVE**

---

## Directory: `requirements/modes/`

Historical and versioned evolution of MMS modes.

Each version directory is **NORMATIVE for its declared version**.

Examples:
- `0.1.x` — exploratory and early automation
- `0.2.x` — structured information processing
- `0.3.x` — explicit source handover
- `0.4.x` — problem-centered modeling
- `0.5.x` — LLM-assisted extraction

Contents may include:
- schemas
- prompts
- pipelines
- examples
- tests
- documentation

---

## Directory: `requirements/pipelines/`

Pipeline definitions and prompt producers.

| Path | Description |
|-----|-------------|
| `README.md` | Pipeline overview |
| `prompt/` | Prompt-based pipelines |

**NORMATIVE**

---

## Directory: `requirements/profiles/`

Execution and usage profiles.

| Path | Description |
|-----|-------------|
| `README.md` | Profile definitions |

**NORMATIVE**

---

## Directory: `requirements/runs/`

Run manifests and examples.

| Path | Description |
|-----|-------------|
| `README.md` | Run structure |
| `examples/` | Example manifests |

Schemas are **NORMATIVE**, example data is **NON-NORMATIVE**.

---

## Directory: `requirements/schemas/`

All JSON schemas defining MMS data contracts.

**STRICTLY NORMATIVE**

---

## Directory: `requirements/tools/`

Validation and helper tools.

| Path | Description |
|-----|-------------|
| `validate_run.py` | Run validator |

Tools are **NON-NORMATIVE**, schemas they validate against are NORMATIVE.

---

## Directory: `gateway/`

**NON-PUBLIC · NON-NORMATIVE · OPTIONAL**

- Not part of the MMS specification
- No guarantees of existence
- No stability or compatibility guarantees
- May be absent entirely
- Must not be referenced as a required component

Any mention of `gateway/` is **descriptive only**.

Implementations MAY:
- maintain private gateways
- mirror requirements internally
- replace or omit gateways entirely

---

## Global Rules

1. This repository defines **WHAT**, never **HOW**
2. No file outside `requirements/` is binding
3. No implementation is required, implied, or provided
4. Absence of a component MUST NOT be treated as an error
5. Specifications are self-contained

---

## Canonical Status

This file is the **single authoritative index** of the repository.

All interpretations MUST conform to this structure.


