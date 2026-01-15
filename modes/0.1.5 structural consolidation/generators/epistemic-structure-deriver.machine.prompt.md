# ============================================================
# BOOTLOADER-BOUND EPISTEMIC DERIVER (MACHINE-OPTIMIZED, v3)
# Deterministic • Fail-Closed • Non-Narrative • Stop-Report Normalized
# ============================================================

# BINDING (HARD)
B0 ENTITY: Exactly one entity type exists: PROBLEM.
B1 EXISTENCE: A PROBLEM exists iff it has:
   - symptoms: at least 1 reference to another PROBLEM
   - causes:   at least 1 reference to another PROBLEM
B2 REFERENCES: All lists (symptoms/causes/consequences/diagnostics/therapies/links)
   contain only references to PROBLEMS. Missing references MUST be created.
B3 FINITENESS: Output MUST be finite and discrete. No open-ended lists.
B4 NO PROSE: No narrative/explanation outside PROBLEM objects.

# OPTIONAL TAGS (NOT ENTITY TYPES)
# These are metadata labels for determinism; they do NOT introduce new entity types.
kind ∈ {"domain","subdomain","field","atomic","support","stop","missing","conflict","ambiguity"}

# ============================================================
# EPISTEMIC DEFINITIONS
# ============================================================

NECESSITY (CONSTRAINT):
A necessity-type is what cannot be negotiated away without changing what is the case.

DOMAIN:
A DOMAIN is a PROBLEM whose core represents an IRREDUCIBLE necessity-type.

SUBDOMAIN:
A SUBDOMAIN is a PROBLEM that restricts a DOMAIN by context/scale/time/responsibility
while preserving the same necessity-type.

FIELD / THEME:
A FIELD is a PROBLEM representing a projection/view over existing PROBLEMS.
FIELDS introduce no new necessity-types.

ATOMIC PROBLEM:
An ATOMIC PROBLEM is a PROBLEM that cannot be further decomposed without destroying
at least one of: causality, responsibility, decision capability.
Atomarity is relative to DOMAIN + CONTEXT.

# ============================================================
# DOMAIN VALIDITY CONDITIONS (ALL REQUIRED)
# ============================================================

DV1 IRREDUCIBILITY: The necessity-type cannot be fully reduced to another necessity-type.
DV2 NECESSITY: There exist PROBLEMS that cannot be coherently modeled without this DOMAIN.
DV3 DISTINCTNESS: No two DOMAINS share the same necessity-core (no synonyms/duplicates).
DV4 STABILITY: Necessity-core holds across contexts/time (not institutional/disciplinary).
DV5 MINIMALITY: Removing the DOMAIN breaks coverage or mandatory consequence derivation.

# ============================================================
# SUBDOMAIN STOP CONDITION
# ============================================================

SV-STOP:
Do not create further SUBDOMAINS when additional restriction yields no new
mandatory consequences.

# ============================================================
# FIELD RULES
# ============================================================

F1 NO NEW NECESSITIES: FIELDS MUST NOT introduce new necessity-types.
F2 VIEW ONLY: FIELDS may only group/index/reference PROBLEMS via links.

# ============================================================
# ATOMICITY CONDITIONS (ALL REQUIRED)
# ============================================================

AV1 SINGLE DOMINANT NECESSITY: Exactly one DOMAIN necessity-core dominates.
AV2 NO GAINFUL DECOMPOSITION: Further decomposition yields no additional mandatory consequences.
AV3 CONTEXT-RELATIVE: Atomarity assessed relative to DOMAIN + CONTEXT.

# ============================================================
# FIXPOINT (MUTUAL VALIDATION)
# ============================================================

FP1 DOMAINS → ATOMS: DOMAINS define what counts as "single dominant necessity" (AV1).
FP2 ATOMS → DOMAINS: A DOMAIN is invalid if no ATOMIC PROBLEM requires it (violates DV2).
FP3 MULTI-CORE CONFLICT: If an ATOM requires multiple irreducible DOMAIN cores:
    - split the ATOM, or
    - refine domains,
    but never keep a multi-core ATOM.

Iterate adjustments until:
- all DV* and AV* hold, OR
- STOP is triggered.

# ============================================================
# NORMALIZED STOP REPORT (FAIL-CLOSED)
# ============================================================

# Rule: If STOP triggers, output ONLY a STOP GRAPH (still PROBLEMS only).
# No partial domain/subdomain/field/atom output is allowed in a STOP response.

STOP TRIGGERS (any one):
S1 Cannot satisfy DV1..DV5 without violating finiteness (B3) or distinctness (DV3).
S2 Cannot satisfy AV1..AV3 without violating B1/B2.
S3 Further differentiation yields no new mandatory consequences (global stop).
S4 Unresolved definition conflicts about necessity-types.
S5 Insufficient input constraints to decide irreducibility/distinctness/minimality.

STOP OUTPUT SHAPE (MUST):
- Create exactly one root PROBLEM with:
  kind="stop"
  id="stop:root"  (id format is advisory, not a schema constraint here)
- Its symptoms MUST reference one or more PROBLEMS of kind in {"missing","conflict","ambiguity"}.
- Its causes MUST reference one or more PROBLEMS of kind in {"missing","conflict","ambiguity"}.
- All referenced PROBLEMS MUST exist (B2).

STOP PROBLEM KINDS (semantics):
kind="missing":
- Represents a required constraint/definition that is absent.
- symptoms: references to PROBLEMS that expose the gap
- causes: references to PROBLEMS that would provide/ground the missing element

kind="conflict":
- Represents an inconsistency (two requirements cannot both hold).
- symptoms: references to the conflicting PROBLEMS
- causes: references to PROBLEMS that generate the inconsistency

kind="ambiguity":
- Represents underdetermination (multiple non-equivalent options fit).
- symptoms: references to PROBLEMS whose mapping is ambiguous
- causes: references to PROBLEMS representing alternative necessity-cores/options

FAIL-CLOSED:
- Do NOT invent resolutions.
- Do NOT continue generation past STOP.
- Do NOT output prose. Only PROBLEM objects.

# ============================================================
# GLOBAL OUTPUT REQUIREMENTS
# ============================================================

O1 Output consists solely of PROBLEMS (with optional kind tags).
O2 Every reference resolves to an existing PROBLEM.
O3 Finite, discrete graph.
O4 No narrative/explanatory text outside PROBLEM objects.

# ============================================================
# END (v3)
# ============================================================

