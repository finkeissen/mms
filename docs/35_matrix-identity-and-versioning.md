# Matrix Identity and Versioning

**Status:** Draft  
**Target version:** 0.2.2  
**Scope:** Normative, kernel-adjacent  
**Role:** Defines when a Matrix is the same, revised, or alternative

---

## Purpose of This Document

This document defines the rules for **Matrix identity** in the
**Matrix Management System (MMS)**.

It specifies:
- when two Matrix states are considered the *same Matrix*
- when a new Matrix version exists
- when a fundamentally **alternative Matrix instantiation** exists
- how this relates to runs, modes, and translators

This document is **normative**.

Without an explicit identity model,
auditability, comparability, and trust collapse.

---

## Why Matrix Identity Matters

MMS is explicitly designed to:
- accumulate claims over time
- preserve disagreement and alternatives
- evolve through refinement without erasure

Without clear identity rules:
- quality improvements become indistinguishable from reinterpretations
- alternative representations are silently merged
- audit trails lose meaning

Matrix identity is the **epistemic guardrail**
between refinement and reinterpretation.

---

## Core Principle

> **A Matrix is defined by its canonical claim identities  
> and the relations between them.**

Everything else is:
- metadata
- enrichment
- presentation
- access structure

---

## Definition: Same Matrix

Two states are considered the **same Matrix** if and only if:

- the **set of canonical claim identities is identical**
- no claim has been split or merged
- relations and conflicts reference the same claim identities
- only additive artifacts have changed

Allowed changes *within the same Matrix* include:

- adding relations
- adding conflict records
- refining provenance metadata
- attaching QA and audit annotations
- new runs that add no new claims
- new runs that add new claims (append-only)

These changes constitute **Matrix growth**, not a change of identity.

---

## Definition: Matrix Version

A **new version of the same Matrix** exists when:

- new claims are added (append-only)
- new relations or conflicts are added
- provenance information is refined
- QA and audit layers are extended

Matrix versions are:

- monotonic
- comparable
- ordered by time and run lineage

A Matrix version never removes, rewrites,
or invalidates prior content.

---

## Definition: Alternative Matrix Instantiation

An **alternative Matrix instantiation** exists when:

- claims are split into multiple claims
- multiple claims are merged into one
- claim granularity rules are changed
- conflict semantics are redefined
- the canonical claim contract is intentionally reinterpreted

Alternative instantiations:

- are always explicit
- are never silently merged
- must declare their derivation
- may reference another Matrix as a source

They represent **different representations of epistemic structure**,  
not quality improvements of the same structure.

---

## Role of Translator Modes

Translator modes are the **only permitted mechanism**
to create alternative Matrix instantiations.

Translator runs MUST:

- declare themselves as translator runs
- specify the source Matrix instantiation
- produce outputs under a new Matrix identity
- never overwrite canonical artifacts

Translator usage is exceptional by design
and always visible in the audit trail.

---

## Matrix Identity and Runs

- Every run belongs to exactly one Matrix instantiation.
- Multiple runs may contribute to the same Matrix.
- A run never retroactively changes Matrix identity.

Run lineage enables:
- time-based comparison
- regression analysis
- quality evolution tracking
- explicit branching histories

---

## Matrix Identity and Publication

Publication does **not** define Matrix identity.

Multiple publications may exist for:
- the same Matrix
- different versions of the same Matrix
- alternative Matrix instantiations

Identity is defined by **content and structure**,
not by export format or presentation.

---

## Anti-Patterns (Explicitly Disallowed)

The following behaviors are contract violations:

- silently rewriting claims
- collapsing alternative representations without declaration
- treating reinterpretation as quality refinement
- mixing translator outputs into canonical runs
- using publication formats to imply identity

These patterns break auditability and trust.

---

## Summary

Matrix identity in MMS is governed by:

- stable claim identities
- append-only growth
- explicit versioning
- explicit alternative instantiations

This ensures that:

- disagreement is preserved
- refinement remains transparent
- reinterpretation is never silent
- long-term auditability is maintained

