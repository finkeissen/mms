#!/usr/bin/env python3
"""
engine/add_domains.py

Pipeline-Schritt 1 für MMS 0.1.3:
Arbeitet auf facts/domains.jsonl.

- keine LLM-Anbindung
- einfache JSONL-Validierung
- Logging ins globale Systemlog (logs/log.jsonl)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

from engine.utils import layout, utils_jsonl


def _write_log(event: str, status: str, details: dict) -> None:
    """
    Minimaler Logger gemäß README Kapitel 9.

    WICHTIG:
    - nutzt layout.LOGS_MAIN_FILE direkt (kein Caching),
      damit monkeypatch in den Tests greift.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "event": event,
        "version": layout.get_version(),
        "status": status,
        "details": details or {},
    }
    utils_jsonl.append_jsonl(layout.LOGS_MAIN_FILE, [entry])


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

    Verwendet layout.DOMAINS_SOURCE_FILE als Quelle.
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

        _write_log(
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
        _write_log(
            event="domains.add",
            status="error",
            details={"path": str(path), "error": msg},
        )
        return 1
    except Exception as exc:  # Fallback
        msg = f"Unerwarteter Fehler: {exc}"
        print(f"[domains.add] {msg}", file=sys.stderr)
        _write_log(
            event="domains.add",
            status="error",
            details={"path": str(path), "error": msg},
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

