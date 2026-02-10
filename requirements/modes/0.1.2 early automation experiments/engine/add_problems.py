#!/usr/bin/env python3
"""
engine/add_problems.py

Pflege und Aktualisierung der Problems für MMS 0.1.2.

NEUES VERHALTEN:
- Es werden NICHT mehr nur data/problems.jsonl eingelesen.
- Stattdessen werden ALLE *.jsonl-Dateien im Verzeichnis data/problems/
  als Quellen verwendet (z. B. arbeit.jsonl, gesundheit.jsonl usw.).
- Optional wird zusätzlich data/problems.jsonl (layout.PROBLEMS_SOURCE_FILE)
  als globale Quelle eingelesen, falls vorhanden.

Ziel:
- Alle Probleme in eine globale Liste (data/problems.json) mergen,
  dabei Duplikate nach problem_id auflösen und sortiert speichern.

Datenfluss:

- Quellen:
    layout.PROBLEMS_DIR/*.jsonl (z. B. data/problems/gesundheit.jsonl)
    layout.PROBLEMS_SOURCE_FILE (optional, z. B. data/problems.jsonl)

    Eine Zeile = ein JSON-Objekt mit mindestens:
        - problem_id (str, eindeutig)
        - domain_id (str)
        - title (str)
        - description (str)
      optional:
        - tags (Liste von Strings)
        - difficulty (str: z. B. "low", "medium", "high")
        - origin (z. B. "human" oder "llm")

- Ziel:
    layout.GLOBAL_PROBLEMS_FILE  (z. B. data/problems.json)
    JSON-Array aller Problem-Objekte.

Verhalten:

1. Lese existierende Problems aus GLOBAL_PROBLEMS_FILE (falls vorhanden).
2. Lese neue/aktualisierte Problems aus:
   - allen *.jsonl in PROBLEMS_DIR (außer index.jsonl)
   - optional PROBLEMS_SOURCE_FILE (data/problems.jsonl), falls vorhanden.
3. Mische beide:
   - gleiche problem_id -> Eintrag aus den Quellen überschreibt den alten.
   - neue problem_id -> neuer Eintrag.
4. Sortiere nach (domain_id, difficulty, title, problem_id).
5. Schreibe das Ergebnis nach GLOBAL_PROBLEMS_FILE.

Dieses Skript ruft kein LLM direkt auf.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import layout
from .utils_jsonl import load_jsonl


# ---------------------------------------------------------------------------
# Datentypen
# ---------------------------------------------------------------------------


@dataclass
class Problem:
    problem_id: str
    domain_id: str
    title: str
    description: str
    tags: List[str]
    difficulty: str = "unknown"
    origin: str = "unknown"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Problem":
        """
        Erzeugt ein Problem-Objekt aus einem Dictionary.
        Setzt sinnvolle Defaults und ist robust gegen fehlende Felder.
        """
        raw_tags = data.get("tags") or []
        if not isinstance(raw_tags, list):
            raw_tags = [str(raw_tags)]

        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()

        difficulty = str(data.get("difficulty", "unknown")).strip() or "unknown"
        origin = str(data.get("origin", "unknown")).strip() or "unknown"

        return cls(
            problem_id=str(data.get("problem_id", "")).strip(),
            domain_id=str(data.get("domain_id", "")).strip(),
            title=title,
            description=description,
            tags=[str(t).strip() for t in raw_tags],
            difficulty=difficulty,
            origin=origin,
        )


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Laden bestehender Problems
# ---------------------------------------------------------------------------


def _load_existing_problems(path: Path) -> List[Problem]:
    """
    Lädt existierende Problems aus einer JSON-Datei (GLOBAL_PROBLEMS_FILE).
    Erwartet ein JSON-Array von Objekten.
    """
    import json

    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"⚠️  Konnte bestehende Problems aus {path} nicht laden: {exc}")
        return []

    if not isinstance(raw, list):
        print(f"⚠️  Unerwartetes Format in {path}: erwarte eine Liste.")
        return []

    result: List[Problem] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(
                f"⚠️  Unerwarteter Eintragstyp in {path}, Index {idx}: "
                f"{type(item).__name__}"
            )
            continue
        try:
            p = Problem.from_dict(item)
        except Exception as exc:
            print(
                f"⚠️  Fehler beim Parsen bestehender Problems in {path}, "
                f"Index {idx}: {exc}"
            )
            continue
        if not p.problem_id:
            print(
                f"⚠️  Bestehendes Problem ohne problem_id in {path}, "
                f"Index {idx} wird übersprungen."
            )
            continue
        if not p.domain_id:
            print(
                f"⚠️  Bestehendes Problem ohne domain_id in {path}, "
                f"Index {idx} wird übersprungen."
            )
            continue
        result.append(p)

    return result


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Laden aus Quellen (JSONL)
# ---------------------------------------------------------------------------


def _load_source_problems_from_file(path: Path) -> List[Problem]:
    """
    Lädt Problems aus einer einzelnen JSONL-Datei.
    """
    if not path.exists():
        return []

    raw = load_jsonl(path)
    result: List[Problem] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(
                f"⚠️  Unerwarteter Eintragstyp in {path}, "
                f"Zeile {idx + 1}: {type(item).__name__}"
            )
            continue
        try:
            p = Problem.from_dict(item)
        except Exception as exc:
            print(
                f"⚠️  Fehler beim Parsen eines Problems in {path}, "
                f"Zeile {idx + 1}: {exc}"
            )
            continue
        if not p.problem_id:
            print(
                f"⚠️  Problem ohne problem_id in {path}, "
                f"Zeile {idx + 1} wird übersprungen."
            )
            continue
        if not p.domain_id:
            print(
                f"⚠️  Problem ohne domain_id in {path}, "
                f"Zeile {idx + 1} wird übersprungen."
            )
            continue
        result.append(p)
    return result


def _load_source_problems_all(
    problems_dir: Path,
    global_source: Optional[Path],
) -> List[Problem]:
    """
    Lädt Problems aus:
    - allen *.jsonl in problems_dir (z. B. data/problems/*.jsonl, außer index.jsonl)
    - optional global_source (data/problems.jsonl), falls vorhanden.
    """
    all_problems: List[Problem] = []

    # 1) Domain-spezifische Dateien im Verzeichnis data/problems/
    if problems_dir.exists():
        print(f"Quell-Verzeichnis (Problems, JSONL): {problems_dir}")
        for path in sorted(problems_dir.glob("*.jsonl")):
            if path.name.lower() == "index.jsonl":
                continue
            print(f"  - Lade aus Datei: {path.name}")
            part = _load_source_problems_from_file(path)
            print(f"    -> {len(part)} Problems geladen")
            all_problems.extend(part)
    else:
        print(f"⚠️  Problems-Verzeichnis existiert nicht: {problems_dir}")

    # 2) Optionale globale Quelle data/problems.jsonl
    if global_source is not None and global_source.exists():
        print(f"Zusätzliche globale Quelle: {global_source}")
        part = _load_source_problems_from_file(global_source)
        print(f"    -> {len(part)} Problems aus globaler Quelle geladen")
        all_problems.extend(part)

    return all_problems


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Mergen, Sortieren, Speichern
# ---------------------------------------------------------------------------


def _merge_problems(existing: List[Problem], updates: List[Problem]) -> List[Problem]:
    """
    Merged zwei Problem-Listen nach problem_id.
    Einträge aus `updates` überschreiben Einträge aus `existing`.
    """
    by_id: Dict[str, Problem] = {}

    for p in existing:
        by_id[p.problem_id] = p

    for p in updates:
        by_id[p.problem_id] = p

    return list(by_id.values())


def _sort_problems(entries: List[Problem]) -> List[Problem]:
    """
    Sortiert Problems nach (domain_id, difficulty, title, problem_id).
    """
    def sort_key(p: Problem) -> Tuple[str, str, str, str]:
        return (
            p.domain_id.lower(),
            p.difficulty.lower(),
            p.title.lower(),
            p.problem_id.lower(),
        )

    return sorted(entries, key=sort_key)


def _save_problems(path: Path, entries: List[Problem]) -> None:
    """
    Speichert die Problems als JSON-Array in die Ziel-Datei.
    """
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(p) for p in entries]
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    source_dir = layout.PROBLEMS_DIR
    global_source = layout.PROBLEMS_SOURCE_FILE  # optional
    target_path = layout.GLOBAL_PROBLEMS_FILE

    print(f"Quell-Verzeichnis (Problems, JSONL): {source_dir}")
    if global_source.exists():
        print(f"Optionale globale Quelle (JSONL):   {global_source}")
    else:
        print(f"Optionale globale Quelle (JSONL):   {global_source} (nicht vorhanden)")

    print(f"Ziel-Datei  (Problems, JSON):        {target_path}")

    existing = _load_existing_problems(target_path)
    print(f"Bereits vorhandene Problems:         {len(existing)}")

    updates = _load_source_problems_all(source_dir, global_source)
    print(f"Problems aus Quellen (gesamt):       {len(updates)}")

    merged = _merge_problems(existing, updates)
    print(f"Problems nach Merge:                 {len(merged)}")

    merged_sorted = _sort_problems(merged)
    _save_problems(target_path, merged_sorted)
    print(f"Problems gespeichert in:             {target_path}")

    print("Problems-Update abgeschlossen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

