 #!/usr/bin/env python3
"""
engine/add_knowledge.py

Pflege und Aktualisierung der Knowledge-Einträge für MMS 0.1.2.

Dieses Skript arbeitet rein auf Dateiebene und verwendet KEINE generate_*-Skripte.
Stattdessen übernimmt es die Aufgabe, Knowledge aus einer JSONL-Quelle zu laden,
mit bestehenden Einträgen zu mergen, optional gegen Problems zu validieren und
als JSON abzulegen.

Datenfluss:

- Quelle:
    layout.KNOWLEDGE_SOURCE_FILE  (z. B. data/knowledge_base.jsonl)
    Eine Zeile = ein JSON-Objekt mit typischer Struktur:
        - knowledge_id (str)
        - domain_id (str)
        - problem_id (str, optional)
        - kind (str, z. B. "definition", "step", "example", optional)
        - title (str, optional)
        - content (str) oder text (str)
        - tags (Liste von Strings, optional)
        - origin (z. B. "human" oder "llm", optional)

- Ziel:
    layout.GLOBAL_KNOWLEDGE_FILE  (z. B. data/knowledge.json)
    JSON-Array aller Knowledge-Objekte.

Verhalten:

1. Lese existierende Knowledge-Einträge aus GLOBAL_KNOWLEDGE_FILE (falls vorhanden).
2. Lese neue/aktualisierte Einträge aus KNOWLEDGE_SOURCE_FILE (JSONL).
3. Mische beide:
   - gleiche knowledge_id -> Eintrag aus der Quelle überschreibt den alten.
   - neue knowledge_id -> neuer Eintrag.
4. Sortiere nach (domain_id, problem_id, kind, title).
5. Schreibe das Ergebnis nach GLOBAL_KNOWLEDGE_FILE.
6. Falls eine Problems-Datei existiert (layout.GLOBAL_PROBLEMS_FILE), prüfe
   referenzierte domain_id/problem_id und gib Warnungen bei Inkonsistenzen aus.

Dieses Skript ruft kein LLM direkt auf. Die Generierung neuer Knowledge-Einträge
kann separat erfolgen, indem KNOWLEDGE_SOURCE_FILE befüllt wird.
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
class Knowledge:
    knowledge_id: str
    domain_id: str
    problem_id: Optional[str]
    kind: str
    title: str
    content: str
    tags: List[str]
    origin: str = "unknown"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Knowledge":
        """
        Erzeugt ein Knowledge-Objekt aus einem Dictionary.
        Setzt sinnvolle Defaults und ist robust gegen fehlende Felder.
        """
        raw_tags = data.get("tags") or []
        if not isinstance(raw_tags, list):
            raw_tags = [str(raw_tags)]

        # content-Feld: wir akzeptieren "content" oder "text"
        content = data.get("content")
        if content is None:
            content = data.get("text", "")

        kind = str(data.get("kind", "")).strip()
        if not kind:
            # einfacher Default, falls nichts angegeben ist
            kind = "note"

        title = str(data.get("title", "")).strip()

        problem_id = data.get("problem_id")
        if problem_id is not None:
            problem_id = str(problem_id).strip() or None

        return cls(
            knowledge_id=str(data.get("knowledge_id", "")).strip(),
            domain_id=str(data.get("domain_id", "")).strip(),
            problem_id=problem_id,
            kind=kind,
            title=title,
            content=str(content).strip(),
            tags=[str(t).strip() for t in raw_tags],
            origin=str(data.get("origin", "unknown")).strip() or "unknown",
        )


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Laden bestehender Knowledge-Einträge
# ---------------------------------------------------------------------------


def _load_existing_knowledge(path: Path) -> List[Knowledge]:
    """
    Lädt existierende Knowledge-Einträge aus einer JSON-Datei
    (GLOBAL_KNOWLEDGE_FILE). Erwartet ein JSON-Array von Objekten.
    """
    import json

    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"⚠️  Konnte bestehende Knowledge aus {path} nicht laden: {exc}")
        return []

    if not isinstance(raw, list):
        print(f"⚠️  Unerwartetes Format in {path}: erwarte eine Liste.")
        return []

    result: List[Knowledge] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(
                f"⚠️  Unerwarteter Eintragstyp in {path}, Index {idx}: "
                f"{type(item).__name__}"
            )
            continue
        try:
            k = Knowledge.from_dict(item)
        except Exception as exc:
            print(
                f"⚠️  Fehler beim Parsen bestehender Knowledge in {path}, "
                f"Index {idx}: {exc}"
            )
            continue
        if not k.knowledge_id:
            print(
                f"⚠️  Bestehender Knowledge-Eintrag ohne knowledge_id in {path}, "
                f"Index {idx} wird übersprungen."
            )
            continue
        if not k.domain_id:
            print(
                f"⚠️  Bestehender Knowledge-Eintrag ohne domain_id in {path}, "
                f"Index {idx} wird übersprungen."
            )
            continue
        result.append(k)

    return result


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Laden aus Quelle (JSONL)
# ---------------------------------------------------------------------------


def _load_source_knowledge(path: Path) -> List[Knowledge]:
    """
    Lädt Knowledge-Einträge aus der JSONL-Quelle (KNOWLEDGE_SOURCE_FILE).
    """
    if not path.exists():
        print(f"⚠️  Quell-Datei für Knowledge existiert nicht: {path}")
        return []

    raw = load_jsonl(path)
    result: List[Knowledge] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(
                f"⚠️  Unerwarteter Eintragstyp in {path}, "
                f"Zeile {idx + 1}: {type(item).__name__}"
            )
            continue
        try:
            k = Knowledge.from_dict(item)
        except Exception as exc:
            print(
                f"⚠️  Fehler beim Parsen eines Knowledge-Eintrags in {path}, "
                f"Zeile {idx + 1}: {exc}"
            )
            continue
        if not k.knowledge_id:
            print(
                f"⚠️  Knowledge-Eintrag ohne knowledge_id in {path}, "
                f"Zeile {idx + 1} wird übersprungen."
            )
            continue
        if not k.domain_id:
            print(
                f"⚠️  Knowledge-Eintrag ohne domain_id in {path}, "
                f"Zeile {idx + 1} wird übersprungen."
            )
            continue
        result.append(k)
    return result


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Mergen, Sortieren, Speichern
# ---------------------------------------------------------------------------


def _merge_knowledge(existing: List[Knowledge], updates: List[Knowledge]) -> List[Knowledge]:
    """
    Merged zwei Knowledge-Listen nach knowledge_id.
    Einträge aus `updates` überschreiben Einträge aus `existing`.
    """
    by_id: Dict[str, Knowledge] = {}

    for k in existing:
        by_id[k.knowledge_id] = k

    for k in updates:
        by_id[k.knowledge_id] = k

    return list(by_id.values())


def _sort_knowledge(entries: List[Knowledge]) -> List[Knowledge]:
    """
    Sortiert Knowledge-Einträge nach (domain_id, problem_id, kind, title, knowledge_id).
    """
    def sort_key(k: Knowledge) -> Tuple[str, str, str, str, str]:
        domain = k.domain_id.lower()
        problem = (k.problem_id or "").lower()
        kind = (k.kind or "").lower()
        title = (k.title or "").lower()
        kid = k.knowledge_id.lower()
        return domain, problem, kind, title, kid

    return sorted(entries, key=sort_key)


def _save_knowledge(path: Path, entries: List[Knowledge]) -> None:
    """
    Speichert die Knowledge-Einträge als JSON-Array in die Ziel-Datei.
    """
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(k) for k in entries]
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Optionale Validierung gegen Problems
# ---------------------------------------------------------------------------


def _load_problem_index(path: Path) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Lädt ein grobes Index-Mapping von problem_id -> domain_id und
    domain_id -> domain_id (als Set-Ersatz) aus der globalen Problems-Datei,
    falls diese existiert.

    Rückgabe:
        problems_by_id:  Mapping problem_id -> domain_id
        domains_seen:    Mapping domain_id -> domain_id (Set-ähnlich)
    """
    import json

    problems_by_id: Dict[str, str] = {}
    domains_seen: Dict[str, str] = {}

    if not path.exists():
        return problems_by_id, domains_seen

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"⚠️  Konnte Problems aus {path} zur Validierung nicht laden: {exc}")
        return problems_by_id, domains_seen

    if not isinstance(raw, list):
        print(f"⚠️  Unerwartetes Format in {path}: erwarte eine Liste.")
        return problems_by_id, domains_seen

    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        pid = str(item.get("problem_id", "")).strip()
        did = str(item.get("domain_id", "")).strip()
        if not pid or not did:
            continue
        problems_by_id[pid] = did
        domains_seen[did] = did

    return problems_by_id, domains_seen


def _validate_references(entries: List[Knowledge]) -> None:
    """
    Falls GLOBAL_PROBLEMS_FILE existiert, prüft diese Funktion,
    ob referenzierte problem_id/domain_id-Kombinationen plausibel sind.
    Gibt nur Warnungen aus, bricht den Lauf aber nicht ab.
    """
    problems_path = layout.GLOBAL_PROBLEMS_FILE
    problems_by_id, domains_seen = _load_problem_index(problems_path)

    if not problems_by_id and not domains_seen:
        # Kein Problems-Index vorhanden oder nicht ladbar -> nichts zu prüfen
        return

    for k in entries:
        # domain_id-Prüfung
        if k.domain_id and k.domain_id not in domains_seen:
            print(
                f"⚠️  Knowledge {k.knowledge_id!r} verweist auf unbekannte domain_id {k.domain_id!r}."
            )

        # problem_id-Prüfung
        if k.problem_id:
            did = problems_by_id.get(k.problem_id)
            if did is None:
                print(
                    f"⚠️  Knowledge {k.knowledge_id!r} verweist auf unbekannte "
                    f"problem_id {k.problem_id!r}."
                )
            elif did != k.domain_id:
                print(
                    f"⚠️  Inkonsistenz bei Knowledge {k.knowledge_id!r}: "
                    f"problem_id {k.problem_id!r} gehört zu domain_id {did!r}, "
                    f"nicht zu {k.domain_id!r}."
                )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    source_path = layout.KNOWLEDGE_SOURCE_FILE
    target_path = layout.GLOBAL_KNOWLEDGE_FILE

    print(f"Quell-Datei (Knowledge, JSONL): {source_path}")
    print(f"Ziel-Datei  (Knowledge, JSON):  {target_path}")

    existing = _load_existing_knowledge(target_path)
    print(f"Bereits vorhandene Knowledge-Einträge:  {len(existing)}")

    updates = _load_source_knowledge(source_path)
    print(f"Knowledge-Einträge aus Quelle (JSONL): {len(updates)}")

    merged = _merge_knowledge(existing, updates)
    print(f"Knowledge-Einträge nach Merge:          {len(merged)}")

    merged_sorted = _sort_knowledge(merged)

    # Optionale Validierung gegen Problems
    _validate_references(merged_sorted)

    _save_knowledge(target_path, merged_sorted)
    print(f"Knowledge-Einträge gespeichert in:      {target_path}")

    print("Knowledge-Update abgeschlossen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

