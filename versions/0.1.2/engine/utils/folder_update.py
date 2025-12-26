#!/usr/bin/env python3
"""
engine/folder_update.py

Erzeugt/ergänzt die Ordnerstruktur und Platzhalter-Dateien gemäß engine.layout.
Jetzt BEREINIGT: es werden KEINE generate_* Skripte mehr erzeugt.

Kompatibel mit MMS 0.1.2 und add_domains / add_problems / add_knowledge.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from . import layout


# ─────────────────────────────────────────────────────────────────────────────
#  Verzeichnis-Definitionen
# ─────────────────────────────────────────────────────────────────────────────

def _expected_dirs() -> list[Path]:
    return [
        layout.CONFIG_DIR,
        layout.DATA_DIR,
        layout.DOMAINS_DIR,
        layout.PROBLEMS_DIR,
        layout.KNOWLEDGE_DIR,
        layout.SNAPSHOTS_DIR,
        layout.SCHEMAS_DIR,
        layout.META_DIR,
        layout.DOCS_DIR,
        layout.DOCS_PHILOSOPHY_DIR,
        layout.TESTS_DIR,
        layout.EXPORTS_DIR,
        layout.EXPORTS_GRAPHS_DIR,
        layout.EXPORTS_REPORTS_DIR,
        layout.EXPORTS_VIEWS_DIR,
    ]


# ─────────────────────────────────────────────────────────────────────────────
#  Platzhalter-Dateien
# ─────────────────────────────────────────────────────────────────────────────

def _placeholder_files() -> Dict[Path, str]:
    return {
        # Config
        layout.CONFIG_DIR / "config.yaml": (
            "# MMS config (0.1.2)\n"
            "# TODO: Konfiguration ergänzen.\n"
        ),

        # Meta
        layout.META_LOG_FILE: "",
        layout.META_CONFIG_LOG_FILE: "",
        layout.META_VERSION_DIFFS_FILE: "",
        layout.META_QA_REPORTS_FILE: "",

        # Schemas
        layout.SCHEMAS_DIR / "problem.schema.json": (
            '{ "$schema": "http://json-schema.org/draft-07/schema#" }\n'
        ),
        layout.SCHEMAS_DIR / "domain_meta.schema.json": (
            '{ "$schema": "http://json-schema.org/draft-07/schema#" }\n'
        ),
        layout.SCHEMAS_DIR / "quality.schema.json": (
            '{ "$schema": "http://json-schema.org/draft-07/schema#" }\n'
        ),
        layout.SCHEMAS_DIR / "relations.schema.json": (
            '{ "$schema": "http://json-schema.org/draft-07/schema#" }\n'
        ),
        layout.SCHEMAS_DIR / "log_entry.schema.json": (
            '{ "$schema": "http://json-schema.org/draft-07/schema#" }\n'
        ),

        # Docs
        layout.DOCS_ARCHITECTURE: "# Architektur\n\nTODO.\n",
        layout.DOCS_PIPELINE: "# Pipeline\n\nTODO.\n",
        layout.DOCS_PROTOKOLLE: "# Protokolle\n\nTODO.\n",
        layout.DOCS_OUTPUT_POLICY: "# Output-Policy\n\nTODO.\n",
        layout.DOCS_QUERY_PREFLIGHT: "# Query-Preflight\n\nTODO.\n",
        layout.DOCS_EPISTEMICS: "# Epistemik\n\nTODO.\n",
        layout.DOCS_METAMODELL: "# Metamodell\n\nTODO.\n",
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Engine-Skelette – nur benötigte Dateien!
# ─────────────────────────────────────────────────────────────────────────────

def _engine_skeletons() -> Dict[Path, str]:
    eng = layout.BASE_DIR / "engine"
    return {
        eng / "add_domains.py": '"""\nAdd domains\n"""\n',
        eng / "add_problems.py": '"""\nAdd problems\n"""\n',
        eng / "add_knowledge.py": '"""\nAdd knowledge\n"""\n',
        eng / "enrich_problem.py": '"""\nEnrich problem\n"""\n',
        eng / "link_problems.py": '"""\nLink problems\n"""\n',
        eng / "evaluate_quality.py": '"""\nEvaluate quality\n"""\n',
        eng / "utils_jsonl.py": '"""\nJSONL utilities\n"""\n',
        eng / "llm_wrapper.py": '"""\nLLM wrapper\n"""\n',
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Main (CLI-Einstiegspunkt)
# ─────────────────────────────────────────────────────────────────────────────

def main(verbose: bool = True) -> int:
    if verbose:
        print(f"📁 Basisverzeichnis: {layout.BASE_DIR}")
        print("🔧 Erzeuge/verifiziere Verzeichnisse …")

    for d in _expected_dirs():
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            if verbose:
                print(f"  [+] Verzeichnis angelegt: {d.relative_to(layout.BASE_DIR)}")

    if verbose:
        print("🔧 Erzeuge/verifiziere Platzhalter-Dateien …")

    for path, content in _placeholder_files().items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            if verbose:
                print(f"  [+] Datei angelegt: {path.relative_to(layout.BASE_DIR)}")

    if verbose:
        print("🔧 Erzeuge/verifiziere Engine-Skelette …")

    for path, content in _engine_skeletons().items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            if verbose:
                print(f"  [+] Engine-Skript angelegt: {path.relative_to(layout.BASE_DIR)}")

    if verbose:
        print("✅ Ordnerstruktur-Update abgeschlossen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

