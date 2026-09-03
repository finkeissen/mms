# MMS → Matrix: Integration Interface (Information Hiding Contract)

**Status:** Normative (interface-level).  
**Scope:** Defines the *structural* exchange between the MMS repository (Layer-2) and the Matrix repository (Layer-3).  
**Non-scope:** Does not define how either side stores data internally or how Matrix renders/queries snapshots.

---

## 1) Purpose

This interface exists to enforce **information hiding**:

- Matrix must not depend on MMS internals (folder layout, DB schema, implementation details).
- MMS must not depend on Matrix internals (snapshot layout, domain indexing strategy, engine versions).
- Cross-layer transfer must be **mechanically verifiable** and **append-only compatible**.

The interface is a *contracted payload* that allows Matrix to ingest MMS outputs with:
- explicit run binding
- explicit artifact identity
- explicit provenance hooks
- explicit STOP / failure localization

---

## 2) Layer Roles & Authority Boundary

### 2.1 Roles
- **MMS (Layer-2)**: stores canonical artifacts produced by runs; enforces admissibility; no truth arbitration.
- **Matrix (Layer-3)**: records concrete instantiations, conflicts, STOPs, and explicit absences into a navigable state/snapshot; no decisions or prioritization.

### 2.2 Authority rule
Neither MMS nor Matrix may introduce epistemic authority.
Any decision, prioritization, or trade-off is external (Layer-6).

---

## 3) Invariants (MUST hold)

1. **Append-only semantics**  
   Payloads are immutable. Updates are new payloads with new IDs.

2. **Run binding**  
   Every exported artifact MUST be bound to exactly one `run_id`.

3. **Artifact identity**  
   Every exported artifact MUST include `artifact_id` unique within its run.
   A `content_hash` SHOULD be included to enable deduplication and audit.

4. **No silent repair**  
   Matrix must not silently drop invalid entries.  
   If payload validation fails, Matrix MUST record a STOP-equivalent ingestion result in its own run system.

5. **STOP propagation**  
   If MMS indicates `outcome = STOP`, Matrix MUST ingest the run + logs/failure metadata,
   and MUST NOT treat missing canonical artifacts as a success.

6. **Information hiding**  
   References in this payload MUST NOT require MMS repo access to interpret
   (no implicit file paths into MMS, no “read this internal table”).

---

## 4) Minimal Exchange Model

MMS exports a **bundle**:

- interface metadata
- MMS context (commit/version identifiers)
- an export selection (what is included)
- run manifests (or run summaries) for all referenced runs
- artifact collections (claims/relations/conflicts/sources/observations/stop_records/logs)
- optional integrity section (hashes, counts)

Matrix may ingest the bundle into its own storage and/or re-emit a Matrix snapshot,
but that is outside this interface.

---

## 5) Envelope Schema (SELF-CONTAINED)

The following JSON Schema defines the MMS→Matrix export envelope.
It intentionally models only representation, not meaning.

> Draft: 2020-12

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "mms-matrix-interface.schema.json",
  "title": "MMS → Matrix Interface Envelope (self-contained)",
  "type": "object",
  "additionalProperties": false,
  "required": ["interface", "mms_context", "export", "runs", "artifacts"],
  "properties": {
    "interface": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "version", "produced_at"],
      "properties": {
        "name": { "const": "mms-matrix" },
        "version": { "type": "string", "description": "SemVer. Breaking changes bump MAJOR." },
        "produced_at": { "type": "string", "format": "date-time" },
        "generator": { "type": "string" },
        "notes": { "type": "string" }
      }
    },

    "mms_context": {
      "type": "object",
      "additionalProperties": false,
      "required": ["mms_commit", "requirements_contract"],
      "properties": {
        "mms_commit": {
          "type": "string",
          "description": "Commit hash (or immutable build id) of MMS."
        },
        "requirements_contract": {
          "type": "object",
          "additionalProperties": false,
          "required": ["id", "version"],
          "properties": {
            "id": {
              "type": "string",
              "description": "Identifier of the normative MMS contract set."
            },
            "version": {
              "type": "string",
              "description": "Contract version (SemVer or date-based)."
            }
          }
        }
      }
    },

    "export": {
      "type": "object",
      "additionalProperties": false,
      "required": ["export_id", "created_at", "selection"],
      "properties": {
        "export_id": {
          "type": "string",
          "minLength": 1,
          "description": "Unique identifier of this export bundle."
        },
        "created_at": { "type": "string", "format": "date-time" },

        "selection": {
          "type": "object",
          "additionalProperties": false,
          "required": ["mode", "run_ids"],
          "properties": {
            "mode": {
              "type": "string",
              "enum": ["EXPLICIT_RUNS", "SINCE_TIMESTAMP", "TAGGED_SET", "OTHER"],
              "description": "How this export was selected."
            },
            "run_ids": {
              "type": "array",
              "items": { "type": "string", "minLength": 1 },
              "minItems": 1,
              "uniqueItems": true
            },
            "since": {
              "type": "string",
              "format": "date-time",
              "description": "Used when mode=SINCE_TIMESTAMP."
            },
            "tags": {
              "type": "array",
              "items": { "type": "string" },
              "description": "Used when mode=TAGGED_SET."
            }
          }
        }
      }
    },

    "runs": {
      "type": "array",
      "description": "Run manifests or run summaries for all included run_ids.",
      "items": { "$ref": "#/$defs/mms_run_manifest_v1" },
      "minItems": 1
    },

    "artifacts": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "claims",
        "relations",
        "conflicts",
        "sources",
        "observations",
        "stop_records",
        "logs"
      ],
      "properties": {
        "claims": { "$ref": "#/$defs/artifact_collection" },
        "relations": { "$ref": "#/$defs/artifact_collection" },
        "conflicts": { "$ref": "#/$defs/artifact_collection" },
        "sources": { "$ref": "#/$defs/artifact_collection" },
        "observations": { "$ref": "#/$defs/artifact_collection" },
        "stop_records": { "$ref": "#/$defs/artifact_collection" },
        "logs": { "$ref": "#/$defs/artifact_collection" }
      }
    },

    "integrity": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "bundle_hash": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$",
          "description": "Optional sha256 of the canonicalized bundle (excluding this field)."
        },
        "counts": {
          "type": "object",
          "additionalProperties": { "type": "integer", "minimum": 0 },
          "description": "Optional counts per artifact type."
        }
      }
    }
  },

  "$defs": {
    "artifact_collection": {
      "type": "object",
      "additionalProperties": false,
      "required": ["format", "items"],
      "properties": {
        "format": {
          "type": "string",
          "enum": ["INLINE_JSON_ARRAY", "JSONL_URI", "OTHER"]
        },

        "items": {
          "type": "array",
          "description": "Inline artifacts (used when format=INLINE_JSON_ARRAY).",
          "items": { "$ref": "#/$defs/mms_artifact_v1" },
          "default": []
        },

        "uri": {
          "type": "string",
          "description": "Resolvable URI for JSONL export (used when format=JSONL_URI)."
        },

        "content_hash": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$",
          "description": "Optional hash of the exported artifact collection content (e.g., JSONL file)."
        }
      },
      "allOf": [
        {
          "if": {
            "properties": { "format": { "const": "JSONL_URI" } },
            "required": ["format"]
          },
          "then": { "required": ["uri"] }
        }
      ]
    },

    "mms_run_manifest_v1": {
      "type": "object",
      "additionalProperties": false,
      "required": ["run_id", "created_at", "outcome", "inputs", "outputs"],
      "properties": {
        "run_id": { "type": "string", "minLength": 1 },
        "created_at": { "type": "string", "format": "date-time" },

        "outcome": {
          "type": "string",
          "enum": ["SUCCESS", "NOCLAIM", "UNKNOWN", "CONFLICT", "STOP"]
        },

        "inputs": {
          "type": "object",
          "additionalProperties": true,
          "description": "Structural input declaration; interpretation is out of scope."
        },

        "outputs": {
          "type": "object",
          "additionalProperties": true,
          "description": "Structural output declaration; interpretation is out of scope."
        },

        "failure": {
          "type": "object",
          "additionalProperties": false,
          "required": ["code", "message", "blame"],
          "properties": {
            "code": {
              "type": "string",
              "enum": [
                "ADMISSIBILITY_MISSING",
                "SCHEMA_INVALID",
                "INPUT_UNREADABLE",
                "POLICY_BLOCKED",
                "INTERNAL_ERROR",
                "UNKNOWN"
              ]
            },
            "message": { "type": "string" },
            "blame": {
              "type": "string",
              "enum": ["INPUT", "SCHEMA", "GENERATOR", "POLICY", "UNKNOWN"]
            },
            "evidence_refs": {
              "type": "array",
              "items": { "type": "string" },
              "description": "References to artifact_id/log artifact_id within this bundle."
            }
          }
        },

        "notes": { "type": "string" }
      },

      "allOf": [
        {
          "if": {
            "properties": { "outcome": { "enum": ["STOP", "UNKNOWN"] } },
            "required": ["outcome"]
          },
          "then": { "required": ["failure"] }
        }
      ]
    },

    "mms_artifact_v1": {
      "type": "object",
      "additionalProperties": true,
      "required": ["run_id", "artifact_id"],
      "properties": {
        "run_id": {
          "type": "string",
          "minLength": 1,
          "description": "The producing run."
        },
        "artifact_id": {
          "type": "string",
          "minLength": 1,
          "description": "Unique within run."
        },

        "content_hash": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$",
          "description": "Optional sha256 of canonical JSON for this artifact."
        },

        "artifact_type": {
          "type": "string",
          "description": "Optional discriminator if the MMS kernel uses one (e.g., claim, relation, conflict, ...)."
        }
      }
    }
  }
}

