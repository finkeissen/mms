#!/usr/bin/env python3
"""
engine/utils_jsonl.py

Hilfsfunktionen zum Lesen/Schreiben von JSONL-Dateien.

JSONL-Konvention im MMS:
- eine Zeile = ein JSON-Objekt (dict)
- UTF-8
- keine leeren Zeilen (werden beim Laden übersprungen)

Dieses Modul sollte von allen Engine-Skripten verwendet werden, um
direkte Dateizugriffe zu vereinheitlichen.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Dict, Any, List, Iterator
import json


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    """
    Lädt eine JSONL-Datei vollständig in den Speicher und gibt eine Liste von Dicts zurück.
    Falls die Datei nicht existiert, wird eine leere Liste zurückgegeben.
    """
    items: List[Dict[str, Any]] = []
    if not path.exists():
        return items

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def iter_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    """
    Iterator über eine JSONL-Datei.
    Gibt nacheinander Dict-Objekte zurück.
    Falls die Datei nicht existiert, ist der Iterator leer.
    """
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_jsonl(path: Path, items: Iterable[Dict[str, Any]]) -> None:
    """
    Schreibt eine Liste von Dicts als JSONL-Datei.
    Überschreibt die Datei vollständig.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, items: Iterable[Dict[str, Any]]) -> None:
    """
    Hängt eine Liste von Dicts an eine bestehende JSONL-Datei an.
    Legt die Datei an, falls sie nicht existiert.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def count_jsonl(path: Path) -> int:
    """
    Zählt die Anzahl der nicht-leeren Zeilen in einer JSONL-Datei.
    """
    if not path.exists():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count


if __name__ == "__main__":
    # Minimaler Selbsttest
    test_path = Path("_jsonl_test.tmp")
    data = [{"a": 1}, {"b": 2}]
    write_jsonl(test_path, data)
    loaded = load_jsonl(test_path)
    print("Wrote:", data)
    print("Loaded:", loaded)
    print("Count:", count_jsonl(test_path))
    test_path.unlink(missing_ok=True)

