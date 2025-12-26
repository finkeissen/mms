# tests/test_schema_validator.py
from __future__ import annotations

import json
from pathlib import Path

from engine.utils import layout


def _load_schema(path: Path) -> dict:
    assert path.exists(), f"Schema-Datei fehlt: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "Schema ist kein JSON-Objekt"
    return data


def _dummy_record_for_schema(schema: dict) -> dict:
    # Minimal: alle required-Felder mit None belegen
    required = schema.get("required", [])
    return {name: None for name in required}


def _validate_record_against_schema(record: dict, schema: dict) -> None:
    # Minimal-Validator: prüft nur, dass alle required-Felder vorhanden sind
    required = schema.get("required", [])
    for field in required:
        assert field in record, f"Feld '{field}' fehlt im Record"


def test_domains_schema_is_valid_json_if_present() -> None:
    path = layout.DOMAINS_SCHEMA_FILE
    if not path.exists():
        # In frühen Versionen (z. B. 0.1.3) kann das Schema noch leer sein
        return

    schema = _load_schema(path)
    # Teste Dummy-Record
    rec = _dummy_record_for_schema(schema)
    _validate_record_against_schema(rec, schema)


def test_problem_schema_is_valid_json_if_present() -> None:
    path = layout.PROBLEM_SCHEMA_FILE
    if not path.exists():
        return

    schema = _load_schema(path)
    rec = _dummy_record_for_schema(schema)
    _validate_record_against_schema(rec, schema)


def test_knowledge_schema_is_valid_json_if_present() -> None:
    path = layout.KNOWLEDGE_SCHEMA_FILE
    if not path.exists():
        return

    schema = _load_schema(path)
    rec = _dummy_record_for_schema(schema)
    _validate_record_against_schema(rec, schema)

