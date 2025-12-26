# BOOTLOADER (MMS)

This document defines the axiomatic foundation of the Matrix Management System (MMS).

It is consumed as an axiom.
It is not explanatory, negotiable, or interpretative.

---

## ENTITY

There exists exactly one entity:

- PROBLEM

No other entity types exist.

---

## EXISTENCE RULE

A PROBLEM exists if and only if it has:
- at least one cause (reference to another PROBLEM)
- at least one symptom (reference to another PROBLEM)

If a referenced PROBLEM does not exist, it MUST be created.

---

## RELATIONAL CLOSURE

All elements associated with a PROBLEM
(causes, symptoms, consequences, diagnostics, therapies, links)
are references to other PROBLEMS.

There are no literals, facts, or objects outside PROBLEMS.

---

## FINITENESS

All structures MUST be:
- finite
- discrete
- explicitly enumerated

Open-ended lists are forbidden.

---

## FAILURE MODE

Missing information, inconsistency, or indeterminacy
MUST be represented explicitly as PROBLEMS.

Silence, omission, or implicit resolution is forbidden.

---

## STOP CONDITION

If no further valid derivation is possible
without violating these rules,
generation MUST STOP.

STOP is a valid and complete outcome.

---

## GOVERNANCE

This Bootloader is identical to the canonical version
maintained in the research-program repository.

Any modification requires prior justification
in the research-program.

---

## END

