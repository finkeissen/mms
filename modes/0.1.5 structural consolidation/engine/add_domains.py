#!/usr/bin/env python3
"""
engine/add_domains.py – Version 0.1.4

Pipeline-Schritt 1:
- arbeitet auf layout.DOMAINS_SOURCE_FILE (facts/domains.jsonl)
- validiert JSONL
- zählt Einträge
- schreibt Log-Eintrag über den zentralen Logger
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

from engine.utils import layout, utils_jsonl
from engine.utils.logger import write_log


def _iter_json_lines(path: Path) -> Iterable[dict]:
    """
    Liest JSONL-Datei zeilenweise und validiert jede Zeile als JSON.
    Leere Zeilen werden ignoriert.
    """
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Ungültiges JSON in Zeile {lineno}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    """
    Verarbeitet facts/domains.jsonl.
    """
    path = Path(layout.DOMAINS_SOURCE_FILE)
    created = False
    entries = 0

    try:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
            created = True
            print(f"[domains.add] Domains-Datei neu erstellt: {path}")
            print("[domains.add] (noch keine Einträge vorhanden)")
        else:
            for _ in _iter_json_lines(path):
                entries += 1

            print(f"[domains.add] Domains-Datei: {path}")
            print(f"[domains.add] Anzahl Einträge: {entries}")

        write_log(
            event="domains.add",
            status="success",
            details={
                "path": str(path),
                "entries": entries,
                "created": created,
            },
        )
        return 0

    except ValueError as exc:
        msg = str(exc)
        print(f"[domains.add] Fehler: {msg}", file=sys.stderr)
        write_log(
            event="domains.add",
            status="error",
            details={"path": str(path), "error": msg},
        )
        return 1
    except Exception as exc:  # Fallback
        msg = f"Unerwarteter Fehler: {exc}"
        print(f"[domains.add] {msg}", file=sys.stderr)
        write_log(
            event="domains.add",
            status="error",
            details={"path": str(path), "error": msg},
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

