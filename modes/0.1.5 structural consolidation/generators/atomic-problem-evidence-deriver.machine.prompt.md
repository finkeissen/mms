# ============================================================
# ATOMIC PROBLEM EVIDENCE DERIVER (MACHINE-OPTIMIZED, v1)
# Bootloader-bound • Epistemic • Fail-Closed
# ============================================================

# BINDING (HARD)
# This prompt is strictly bound to:
# - the BOOTLOADER
# - the EPISTEMIC STRUCTURE DERIVER
#
# Input MUST consist exclusively of ATOMIC PROBLEMS.
# No new DOMAINS, SUBDOMAINS, or STRUCTURAL PROBLEMS may be introduced.

# ENTITY AXIOM
# Exactly one entity type exists: PROBLEM.
# All outputs MUST be PROBLEMS or references to PROBLEMS.

# ============================================================
# PURPOSE
# ============================================================

# Bind EVIDENCE to existing ATOMIC PROBLEMS.
# Evidence is represented only as PROBLEMS that
# support, weaken, or contextualize symptoms, causes, or consequences.

# ============================================================
# EPISTEMIC DEFINITION
# ============================================================

EVIDENCE:
An EVIDENCE-PROBLEM is a PROBLEM that represents a concrete,
checkable, domain-relevant fact or observation that:
- supports
- contradicts
- constrains
- or conditions
another PROBLEM.

Evidence has no meaning outside a PROBLEM relation.

# ============================================================
# SCOPE RULES
# ============================================================

S1 INPUT SCOPE:
Only ATOMIC PROBLEMS may be enriched.
Non-atomic PROBLEMS MUST NOT receive evidence directly.

S2 NO STRUCTURE CREATION:
- Do NOT create new DOMAINS.
- Do NOT change atomarity.
- Do NOT split or merge ATOMIC PROBLEMS.

S3 RELATIONAL ONLY:
Evidence MUST always be attached as:
- symptom of a PROBLEM, or
- cause of a PROBLEM, or
- consequence of a PROBLEM.

No standalone evidence nodes without relations.

# ============================================================
# EVIDENCE TYPES (NON-ONTOLOGICAL TAGS)
# ============================================================

# Tags are metadata only, not entity types.
evidence_kind ∈ {
  "empirical_observation",
  "measurement",
  "study_result",
  "historical_record",
  "legal_norm",
  "expert_assessment",
  "experiential_report"
}

uncertainty_level ∈ {
  "high",
  "medium",
  "low",
  "unknown"
}

# ============================================================
# GENERATION RULES
# ============================================================

G1 MINIMALITY:
Create only as many EVIDENCE-PROBLEMS as necessary
to meaningfully constrain the ATOMIC PROBLEM.

G2 RELEVANCE:
Every EVIDENCE-PROBLEM MUST change at least one of:
- plausibility of a cause
- credibility of a symptom
- severity or likelihood of a consequence

G3 TRACEABILITY:
Evidence MUST be concrete enough to be checkable in principle
(even if not verified here).

G4 NON-AGGREGATION:
Do NOT aggregate heterogeneous evidence into a single node.
Prefer multiple minimal EVIDENCE-PROBLEMS.

# ============================================================
# FAILURE & GAP HANDLING
# ============================================================

If relevant evidence is:
- missing
- contradictory
- insufficient to assess causes/consequences

THEN:
- create explicit EVIDENCE-PROBLEMS with
  evidence_kind="missing" or "conflict"
- attach them as causes/symptoms accordingly
- do NOT resolve the conflict

# ============================================================
# STOP RULE
# ============================================================

STOP when:
- additional evidence does not further constrain
  the ATOMIC PROBLEM in a decision-relevant way.

# ============================================================
# OUTPUT CONSTRAINTS
# ============================================================

O1 Output consists solely of PROBLEMS.
O2 Every reference resolves to an existing PROBLEM.
O3 Output is finite and discrete.
O4 No narrative or explanatory prose outside PROBLEM objects.

# ============================================================
# END
# ============================================================

