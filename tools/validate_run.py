#!/usr/bin/env python3
"""
MMS Run Validator (v0.1)

Validates a flat run directory against schemas in ./schemas/.

- Validates manifest.json against run-manifest.schema.json
- Validates JSONL artifacts referenced in the manifest:
  - claims     -> claim.schema.json
  - relations  -> relation.schema.json
  - conflicts  -> conflict.schema.json

Design goals:
- minimal and readable
- deterministic
- clear error messages
- no auto-fixing (fail loud)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    import jsonschema
except ImportError:
    print(
        "ERROR: Missing dependency 'jsonschema'. Install with:\n"
        "  pip install jsonschema",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Schema handling
# ---------------------------------------------------------------------------

@dataclass
class SchemaBundle:
    claim: Dict[str, Any]
    relation: Dict[str, Any]
    conflict: Dict[str, Any]
    run_manifest: Dict[str, Any]


# Only these artifact kinds are schema-validated in v0.1
KIND_TO_SCHEMA = {
    "claims": "claim",
    "relations": "relation",
    "conflicts": "conflict",
}


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl_lines(path: str) -> List[Tuple[int, str]]:
    """
    Returns non-empty lines as (lineno, line) pairs, 1-indexed.
    Empty files are allowed.
    """
    lines: List[Tuple[int, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            lines.append((i, line))
    return lines


def load_schemas(schema_dir: str) -> SchemaBundle:
    def p(name: str) -> str:
        return os.path.join(schema_dir, name)

    return SchemaBundle(
        claim=read_json(p("claim.schema.json")),
        relation=read_json(p("relation.schema.json")),
        conflict=read_json(p("conflict.schema.json")),
        run_manifest=read_json(p("run-manifest.schema.json")),
    )


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_obj(obj: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Returns a list of human-readable validation errors.
    """
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(obj), key=lambda e: e.path)
    formatted: List[str] = []

    for e in errors:
        path = ".".join(str(p) for p in e.path) if e.path else "(root)"
        formatted.append(f"{path}: {e.message}")

    return formatted


def validate_manifest(
    manifest_path: str, schemas: SchemaBundle
) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    if not os.path.exists(manifest_path):
        return None, [f"Missing manifest file: {manifest_path}"]

    try:
        manifest = read_json(manifest_path)
    except Exception as ex:
        return None, [f"Failed to read/parse manifest JSON ({ex})"]

    errors = validate_obj(manifest, schemas.run_manifest)
    return manifest, errors


def resolve_artifact_path(run_dir: str, artifact_path: str) -> str:
    if os.path.isabs(artifact_path):
        return artifact_path
    return os.path.normpath(os.path.join(run_dir, artifact_path))


def validate_jsonl_artifact(
    run_dir: str,
    artifact_ref: Dict[str, Any],
    schema: Dict[str, Any],
) -> List[str]:
    errors: List[str] = []

    path = artifact_ref.get("path")
    if not isinstance(path, str) or not path:
        return ["Artifact reference missing valid 'path'."]

    full_path = resolve_artifact_path(run_dir, path)
    if not os.path.exists(full_path):
        return [f"Missing artifact file: {path}"]

    try:
        lines = read_jsonl_lines(full_path)
    except Exception as ex:
        return [f"Failed to read artifact file {path} ({ex})"]

    for lineno, line in lines:
        try:
            obj = json.loads(line)
        except Exception as ex:
            errors.append(f"{path}:{lineno}: invalid JSON ({ex})")
            continue

        ve = validate_obj(obj, schema)
        for msg in ve:
            errors.append(f"{path}:{lineno}: {msg}")

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an MMS run directory against schema v0.1."
    )
    parser.add_argument(
        "run_dir",
        help="Path to a run directory (flat layout recommended).",
    )
    parser.add_argument(
        "--schema-dir",
        default="schemas",
        help="Path to schema directory (default: ./schemas).",
    )
    args = parser.parse_args()

    run_dir = os.path.normpath(args.run_dir)
    schema_dir = os.path.normpath(args.schema_dir)

    if not os.path.isdir(run_dir):
        print(f"ERROR: run_dir is not a directory: {run_dir}", file=sys.stderr)
        return 2

    if not os.path.isdir(schema_dir):
        print(f"ERROR: schema_dir is not a directory: {schema_dir}", file=sys.stderr)
        return 2

    try:
        schemas = load_schemas(schema_dir)
    except Exception as ex:
        print(f"ERROR: failed to load schemas ({ex})", file=sys.stderr)
        return 2

    manifest_path = os.path.join(run_dir, "manifest.json")
    manifest, manifest_errors = validate_manifest(manifest_path, schemas)

    all_errors: List[str] = []
    if manifest_errors:
        all_errors.extend([f"manifest.json: {e}" for e in manifest_errors])

    if manifest is None or manifest_errors:
        print("VALIDATION FAILED\n", file=sys.stderr)
        for e in all_errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    outputs = manifest.get("outputs", {})
    artifacts = outputs.get("artifacts", [])

    if not isinstance(artifacts, list):
        all_errors.append("manifest.json: outputs.artifacts must be a list.")
    else:
        for a in artifacts:
            if not isinstance(a, dict):
                all_errors.append("manifest.json: artifact entries must be objects.")
                continue

            kind = a.get("kind")
            if not isinstance(kind, str) or not kind:
                all_errors.append("manifest.json: artifact entry missing 'kind'.")
                continue

            schema_name = KIND_TO_SCHEMA.get(kind)
            if schema_name is None:
                continue  # non-schema-bound artifact

            schema = getattr(schemas, schema_name)
            errs = validate_jsonl_artifact(run_dir, a, schema)
            all_errors.extend(errs)

    if all_errors:
        print("VALIDATION FAILED\n", file=sys.stderr)
        for e in all_errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    print("VALIDATION OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

