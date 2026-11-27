# ADMISSION_EVIDENCE.md — Executed Admission Runs (Gatekeeper Role)

## Purpose

The MMS defines admission (Zulässigkeit) as a **governance function**: no artifact
is `admissible` without

1. **permissibility** — the gatekeeper (a fixed, tested function; never a free
   chat answer),
2. **model inspection** — a content checker from a *different* model family than
   the producer,
3. **human release** — person, date, reason, class recorded.

Until 2026-11-22 this role existed only in the architecture documents. This file
records that it has since been **executed as a script**, with measured results.

## Decision classes

| Class | Meaning | Consequence |
|---|---|---|
| SUCCESS | admissible | advances to delta ingestion |
| NOCLAIM | not load-bearing partial material | stays in storage; **never discarded** |
| CONFLICT | double registration / rule violation | back to extraction, not dropped |
| STOP | hard gate condition | pipeline halts; author word required |

## Executed runs (all numbers measured, Nov 22–27 2026)

| Date | Domain / mark | Objects | SUCCESS | NOCLAIM | CONFLICT |
|---|---|---|---|---|---|
| 2026-11-22 | CSB investigation recommendations (first executed admission ever) | problems + solutions | 554 + 554 | 0 | 0 |
| 2026-11-22/23 | HSE guidance (know/do template) | problems + solutions | 67 + 67 | 0 | 0 |
| 2026-11-23 | MSHA fatality alerts | problems + solutions | 373 + 373 | 0 | 0 |
| 2026-11-23 | MSHA hazard alerts | problems + solutions | 78 + 78 | 0 | 0 |
| 2026-11-23 | OSV vulnerabilities (2,000-entry sample) | problems + solutions | 1,856 + 1,856 | 0 | 0 |
| 2026-11-23 | OSV vulnerabilities (full, SEMVER branch) | atoms | 59,289 | 13 (legitimate, technical prose) | 0 |
| 2026-11-23 | OSV vulnerabilities (full, + GIT-range branch) | atoms | 570,701 | 238 | 0 |
| 2026-11-27 | GAO report recommendations (gao1) | atoms | 10,533 | 4 | 0 |

Follow-on delta ingestion (separate governance step, author-gated): OSV full corpus
+581,878 atoms to production (118/118 deltas), GAO +10,537 atoms, bank/kette
consolidation run 146/146 with 0 errors (2026-11-27).

## Evidence that the gate finds real defects

A gate that never rejects proves nothing. Two **real gatekeeper defects** were
found and fixed during the OSV full run (commit `25f146a`):

1. **chunk known-rule:** entries split across chunks could pass twice; the
   known-set rule had a gap → fixed, re-run clean.
2. **technical prose as placeholder:** titles like `NULL pointer dereference`
   or phrases like `not identified by the reporter` triggered the placeholder
   warning — rule corrected: technical vocabulary belongs in the content field,
   never in source metadata; word-identical descriptions under different
   identifiers are *references to the same fact*, not duplicates (identifier is
   part of the admission core).

The GAO run added the mirror case: word-identical findings under **different
report numbers** *are* double registrations (CONFLICT) until the report number
was made part of the admission core — 194 conflicts resolved to 0.

## What this evidence does not claim

- Not that admitted artifacts are true, correct, or useful.
- Not that the producer or checker prompts are error-free (a separate,
  human-held gold standard of 200 judgments is defined but not yet sealed).
- Quality claims about *content* remain explicitly outside admission scope;
  admission decides permissibility only.
