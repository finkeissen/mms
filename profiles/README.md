# profiles/

Profiles define operational permissions and limits for modes.

See:
- `docs/30_profiles-and-modes.md`

Profiles:
- producer/
- enricher/
- translator/

---

## Purpose of Profiles

Profiles define **what actions are permitted** within MMS executions.

They exist to:
- constrain behavior
- separate responsibilities
- prevent accidental capability escalation
- make permissions explicit and auditable

Profiles do **not**:
- define truth
- assign epistemic authority
- imply correctness
- rank contributions
- validate outputs

They are **operational**, not epistemic.

---

### Clarification — Permission, Not Authority

A profile grants **capability**, never **authority**.

Using a profile means:
- an action is allowed
- not that the action is correct
- not that the result is trusted
- not that the outcome is preferred

Any interpretation of profiles as authority
is an architectural violation.

---

## Relationship to Modes and Pipelines

Historically, profiles were often bundled implicitly with modes.

Under the current architecture:
- modes are frozen historical artifacts
- pipelines are the execution layer
- profiles are attached explicitly to runs

No profile is activated implicitly.

Every run must explicitly declare
which profile(s) were used.

---

### Clarification — Explicit Profile Declaration

If a run does not declare its profile,
the run is invalid.

Implicit inheritance of profile permissions
is forbidden.

---

## Profile Granularity

Profiles should be:
- minimal
- narrowly scoped
- capability-focused

Profiles should **not**:
- encode domain assumptions
- embed workflow logic
- imply role hierarchy
- reflect organizational power structures

Granularity exists to **limit blast radius**,
not to optimize convenience.

---

## Canonical Profile Categories

The following high-level profile categories exist:

### producer/

Profiles responsible for **extracting candidate claims**
from raw sources.

Typical permissions:
- read raw materials
- produce draft claims
- record provenance

Explicit non-permissions:
- validate correctness
- resolve conflicts
- synthesize across sources

---

### enricher/

Profiles responsible for **adding structure**
to existing claims.

Typical permissions:
- create relations
- surface conflicts
- add scope or uncertainty qualifiers

Explicit non-permissions:
- delete or override claims
- prioritize competing claims
- assert truth

---

### translator/

Profiles responsible for **representation changes**.

Typical permissions:
- translate language
- map schemas
- reformat artifacts

Explicit non-permissions:
- alter meaning
- collapse distinctions
- normalize disagreement away

---

### Architectural Note — Category Boundaries

Category boundaries are conceptual.
Concrete profiles may combine permissions,
but any combination must be **explicitly justified and documented**.

---

## Prohibited Profile Behaviors

The following are **architecturally forbidden**:

- profiles that auto-resolve conflicts
- profiles that encode “best source” logic
- profiles that rank or score claims
- profiles that hide uncertainty
- profiles that silently filter artifacts
- profiles that bypass run recording

If such behavior is desired,
it must occur **outside MMS**.

---

## Profiles and Audit

Profiles are a key audit surface.

Auditors should verify:
- profile declarations on runs
- consistency between profile and behavior
- absence of implicit permissions
- no authority leakage through profiles

Profile misuse is a **structural violation**,
not a configuration error.

---

## Evolution Rules for Profiles

Profiles may evolve only by:
- tightening permissions
- splitting overly broad profiles
- making implicit assumptions explicit

Profiles must not evolve by:
- adding authority
- expanding scope silently
- introducing defaults

Any significant change to profiles
should be recorded as an architectural decision.

---

## Summary

Profiles exist to **limit what may be done**,
not to legitimize what was done.

If a profile feels powerful,
it is almost certainly too broad.

