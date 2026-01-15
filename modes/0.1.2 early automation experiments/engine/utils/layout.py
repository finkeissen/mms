#!/usr/bin/env python3
"""
engine/layout.py

Zentraler Pfad- und Layout-Manager für MMS 0.1.2
Kompatibel mit folder_update.py, add_domains.py, add_problems.py, add_knowledge.py.

Diese Datei definiert nur Konstanten & Hilfsfunktionen.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Basisverzeichnisse
# ---------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent

DATA_DIR: Path = BASE_DIR / "data"
SCHEMAS_DIR: Path = BASE_DIR / "schemas"

# Dokumentation
DOCS_DIR: Path = BASE_DIR / "docs"
DOCS_PHILOSOPHY_DIR: Path = DOCS_DIR / "philosophy"

# Einzelne Dokumentationsdateien (alle erwartet von folder_update.py)
DOCS_ARCHITECTURE: Path = DOCS_DIR / "architecture.md"
DOCS_PIPELINE: Path = DOCS_DIR / "pipeline.md"
DOCS_PROTOKOLLE: Path = DOCS_DIR / "protokolle.md"
DOCS_OUTPUT_POLICY: Path = DOCS_DIR / "output_policy.md"
DOCS_QUERY_PREFLIGHT: Path = DOCS_DIR / "query_preflight.md"
DOCS_EPISTEMICS: Path = DOCS_DIR / "epistemics.md"
DOCS_METAMODELL: Path = DOCS_DIR / "metamodell.md"

# Tests
TESTS_DIR: Path = BASE_DIR / "tests"

# Konfiguration
CONFIG_DIR: Path = BASE_DIR / "config"

# Meta / Logs
META_DIR: Path = BASE_DIR / "meta"
META_LOG_FILE: Path = META_DIR / "activity.log"
META_CONFIG_LOG_FILE: Path = META_DIR / "config.log"
META_VERSION_DIFFS_FILE: Path = META_DIR / "version_diffs.log"
META_QA_REPORTS_FILE: Path = META_DIR / "qa_reports.log"

# Exporte
EXPORTS_DIR: Path = BASE_DIR / "exports"
EXPORTS_GRAPHS_DIR: Path = EXPORTS_DIR / "graphs"
EXPORTS_REPORTS_DIR: Path = EXPORTS_DIR / "reports"
EXPORTS_VIEWS_DIR: Path = EXPORTS_DIR / "views"

# ---------------------------------------------------------------------------
# Domains
# ---------------------------------------------------------------------------

DOMAINS_DIR: Path = DATA_DIR / "domains"
DOMAINS_SOURCE_FILE: Path = DATA_DIR / "domains.jsonl"
GLOBAL_DOMAINS_FILE: Path = DATA_DIR / "domains.json"

# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------

PROBLEMS_DIR: Path = DATA_DIR / "problems"
PROBLEMS_SOURCE_FILE: Path = DATA_DIR / "problems.jsonl"
GLOBAL_PROBLEMS_FILE: Path = DATA_DIR / "problems.json"
PROBLEMS_INDEX_FILE: Path = PROBLEMS_DIR / "index.jsonl"

# ---------------------------------------------------------------------------
# Knowledge
# ---------------------------------------------------------------------------

KNOWLEDGE_DIR: Path = DATA_DIR / "knowledge"
KNOWLEDGE_SOURCE_FILE: Path = DATA_DIR / "knowledge_base.jsonl"
GLOBAL_KNOWLEDGE_FILE: Path = DATA_DIR / "knowledge.json"

# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------

SNAPSHOTS_DIR: Path = DATA_DIR / "snapshots"

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

VERSION_FILE: Path = BASE_DIR / "VERSION"

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def get_version() -> str:
    """
    Liest die Version aus der VERSION-Datei.
    """
    if not VERSION_FILE.exists():
        raise FileNotFoundError(f"VERSION-Datei fehlt: {VERSION_FILE}")

    text = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("VERSION-Datei ist leer.")
    return text


def as_dict() -> Dict[str, Any]:
    """
    Übersicht aller Pfade als Dict (Debug / Tests).
    """
    return {
        key: str(value)
        for key, value in globals().items()
        if isinstance(value, Path)
    }


def debug_print() -> None:
    """
    Gibt alle relevanten Pfade sortiert aus.
    """
    print("MMS 0.1.2 – Layout-Übersicht")
    print("----------------------------")
    for key, value in sorted(as_dict().items()):
        print(f"{key:28s}: {value}")

