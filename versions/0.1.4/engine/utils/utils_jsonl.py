#!/usr/bin/env python3
"""
engine/utils/utils_jsonl.py

Einfache JSONL-Hilfsfunktionen für MMS 0.1.3.
Technische Schicht, keine Fachlogik.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Any


def read_jsonl(path: Path) -> Iterator[Mapping[str, Any]]:
    """
    Liest eine JSONL-Datei zeilenweise und liefert pro Zeile ein Dict zurück.

    Leere Zeilen werden ignoriert.
    Wenn die Datei nicht existiert, wird ein leerer Iterator zurückgegeben.
    """
    if not path.exists():
        return iter(())

    def _iter() -> Iterator[Mapping[str, Any]]:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)

    return _iter()


def write_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    """
    Schreibt die gegebenen Records als JSONL (überschreibt bestehende Datei).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False))
            f.write("\n")


def append_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    """
    Hängt Records an eine bestehende JSONL-Datei an
    (oder legt sie neu an, falls nicht vorhanden).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False))
            f.write("\n")

