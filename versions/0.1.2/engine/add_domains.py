#!/usr/bin/env python3
"""
engine/add_domains.py

Pflege und Aktualisierung der Fachgebiete (Domains) für MMS 0.1.2.

Dieses Skript arbeitet rein auf Dateiebene und verwendet KEINE direkten
generate_*-Skripte mehr. Stattdessen übernimmt es die Aufgabe, die globale
Domänenliste aus einer JSONL-Quelle zu laden, zu mergen und als JSON
abzuspeichern.

Datenfluss:

- Quelle:
    layout.DOMAINS_SOURCE_FILE  (z. B. data/domains.jsonl)
    Eine Zeile = ein JSON-Objekt mit mindestens:
        - domain_id (str)
        - title (str)
        - description (str)
        - tags (Liste von Strings, optional)
        - origin (z. B. "human" oder "llm", optional)

- Ziel:
    layout.GLOBAL_DOMAINS_FILE  (z. B. data/domains.json)
    JSON-Array aller Domänenobjekte.

Verhalten:

1. Lese existierende Domains aus GLOBAL_DOMAINS_FILE (falls vorhanden).
2. Lese neue/aktualisierte Domains aus DOMAINS_SOURCE_FILE (JSONL).
3. Mische beide:
   - gleiche domain_id -> Eintrag aus der Quelle überschreibt den alten.
   - neue domain_id -> neuer Eintrag.
4. Sortiere nach title (fallback: domain_id).
5. Schreibe das Ergebnis nach GLOBAL_DOMAINS_FILE.

Dieses Skript ruft kein LLM direkt auf. Die Generierung neuer Domänen kann
z. B. separat geschehen, indem DOMAINS_SOURCE_FILE bearbeitet oder aus einem
anderen Tool/Script befüllt wird.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Any

from . import layout
from .utils_jsonl import load_jsonl


# ---------------------------------------------------------------------------
# Datentypen
# ---------------------------------------------------------------------------


@dataclass
class Domain:
    domain_id: str
    title: str
    description: str
    tags: List[str]
    origin: str = "unknown"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Domain":
        """
        Erzeugt ein Domain-Objekt aus einem Dictionary.
        Setzt sinnvolle Defaults und ist robust gegen fehlende Felder.
        """
        raw_tags = data.get("tags") or []
        if not isinstance(raw_tags, list):
            raw_tags = [str(raw_tags)]

        return cls(
            domain_id=str(data.get("domain_id", "")).strip(),
            title=str(data.get("title", "")).strip(),
            description=str(data.get("description", "")).strip(),
            tags=[str(t).strip() for t in raw_tags],
            origin=str(data.get("origin", "unknown")).strip() or "unknown",
        )


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------


def _load_existing_domains(path: Path) -> List[Domain]:
    """
    Lädt existierende Domains aus einer JSON-Datei (GLOBAL_DOMAINS_FILE).
    Erwartet ein JSON-Array von Objekten.
    """
    import json

    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # defensiv: kaputte Datei soll den Lauf nicht zerstören
        print(f"⚠️  Konnte bestehende Domains aus {path} nicht laden: {exc}")
        return []

    if not isinstance(raw, list):
        print(f"⚠️  Unerwartetes Format in {path}: erwarte eine Liste.")
        return []

    result: List[Domain] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(f"⚠️  Unerwarteter Eintragstyp in {path}, Index {idx}: {type(item).__name__}")
            continue
        try:
            d = Domain.from_dict(item)
        except Exception as exc:
            print(f"⚠️  Fehler beim Parsen bestehender Domain in {path}, Index {idx}: {exc}")
            continue
        if not d.domain_id:
            print(f"⚠️  Bestehende Domain ohne domain_id in {path}, Index {idx} wird übersprungen.")
            continue
        result.append(d)

    return result


def _load_source_domains(path: Path) -> List[Domain]:
    """
    Lädt Domains aus der JSONL-Quelle (DOMAINS_SOURCE_FILE).
    """
    if not path.exists():
        print(f"⚠️  Quell-Datei für Domains existiert nicht: {path}")
        return []

    raw = load_jsonl(path)
    result: List[Domain] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            print(f"⚠️  Unerwarteter Eintragstyp in {path}, Zeile {idx + 1}: {type(item).__name__}")
            continue
        try:
            d = Domain.from_dict(item)
        except Exception as exc:
            print(f"⚠️  Fehler beim Parsen der Domain in {path}, Zeile {idx + 1}: {exc}")
            continue
        if not d.domain_id:
            print(f"⚠️  Domain ohne domain_id in {path}, Zeile {idx + 1} wird übersprungen.")
            continue
        result.append(d)
    return result


def _merge_domains(existing: List[Domain], updates: List[Domain]) -> List[Domain]:
    """
    Merged zwei Domain-Listen nach domain_id.
    Einträge aus `updates` überschreiben Einträge aus `existing`.
    """
    by_id: Dict[str, Domain] = {}

    # Zuerst bestehende eintragen
    for d in existing:
        by_id[d.domain_id] = d

    # Dann Updates anwenden (überschreiben)
    for d in updates:
        by_id[d.domain_id] = d

    return list(by_id.values())


def _sort_domains(domains: List[Domain]) -> List[Domain]:
    """
    Sortiert Domains nach title (fallback: domain_id).
    """
    return sorted(
        domains,
        key=lambda d: (d.title.lower() or d.domain_id.lower()),
    )


def _save_domains(path: Path, domains: List[Domain]) -> None:
    """
    Speichert die Domains als JSON-Array in die Ziel-Datei.
    """
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(d) for d in domains]
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    source_path = layout.DOMAINS_SOURCE_FILE
    target_path = layout.GLOBAL_DOMAINS_FILE

    print(f"📄 Quell-Datei (Domains, JSONL): {source_path}")
    print(f"📄 Ziel-Datei  (Domains, JSON):  {target_path}")

    existing = _load_existing_domains(target_path)
    print(f"   Bereits vorhandene Domains:  {len(existing)}")

    updates = _load_source_domains(source_path)
    print(f"   Domains aus Quelle (JSONL):  {len(updates)}")

    merged = _merge_domains(existing, updates)
    print(f"   Domains nach Merge:          {len(merged)}")

    merged_sorted = _sort_domains(merged)
    _save_domains(target_path, merged_sorted)
    print(f"   Domains gespeichert in:      {target_path}")

    print("✅ Domains-Update abgeschlossen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

