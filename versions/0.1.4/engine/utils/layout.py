#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Basisverzeichnisse
# ---------------------------------------------------------------------------

# Datei liegt in: <root>/engine/utils/layout.py
# -> root = zwei Ebenen höher
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

FACTS_DIR: Path = PROJECT_ROOT / "facts"
SCHEMAS_DIR: Path = PROJECT_ROOT / "schemas"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
ENGINE_DIR: Path = PROJECT_ROOT / "engine"
DOCS_DIR: Path = PROJECT_ROOT / "docs"
TESTS_DIR: Path = PROJECT_ROOT / "tests"
EXPORTS_DIR: Path = PROJECT_ROOT / "exports"
GRAPHS_DIR: Path = PROJECT_ROOT / "graphs"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
VIEWS_DIR: Path = PROJECT_ROOT / "views"

ENGINE_UTILS_DIR: Path = ENGINE_DIR / "utils"
CONFIG_FILE: Path = ENGINE_UTILS_DIR / "config.yaml"

DOMAINS_SOURCE_FILE: Path = FACTS_DIR / "domains.jsonl"
PROBLEMS_DIR: Path = FACTS_DIR / "problems"
KNOWLEDGE_DIR: Path = FACTS_DIR / "knowledge"

DOMAINS_SCHEMA_FILE: Path = SCHEMAS_DIR / "domains.schema.json"
PROBLEM_SCHEMA_FILE: Path = SCHEMAS_DIR / "problem.schema.json"
KNOWLEDGE_SCHEMA_FILE: Path = SCHEMAS_DIR / "knowledge.schema.json"

LOGS_MAIN_FILE: Path = LOGS_DIR / "log.jsonl"
LOGS_CONFIG_FILE: Path = LOGS_DIR / "config_log.jsonl"
LOGS_VERSION_DIFFS_FILE: Path = LOGS_DIR / "version_diffs.jsonl"
LOGS_QA_REPORTS_FILE: Path = LOGS_DIR / "qa_reports.jsonl"

VERSION_FILE: Path = PROJECT_ROOT / "VERSION"


def get_version() -> str:
    if not VERSION_FILE.exists():
        raise FileNotFoundError(f"VERSION-Datei fehlt: {VERSION_FILE}")
    text = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("VERSION-Datei ist leer.")
    return text


def as_dict() -> Dict[str, Any]:
    return {
        key: str(value)
        for key, value in globals().items()
        if isinstance(value, Path)
    }


def debug_print() -> None:
    print("MMS 0.1.3 – Layout-Übersicht")
    print("----------------------------")
    for key, value in sorted(as_dict().items()):
        print(f"{key:28s}: {value}")

