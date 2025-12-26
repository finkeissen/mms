#!/usr/bin/env python3
"""
generate_domains.py

Generiert oder aktualisiert Fachgebiete (Domains) für das MMS.

Verhalten:
- Liest bestehende data/domains.json (falls vorhanden)
- Prüft die Struktur und meldet Probleme
- Bricht bei harten Fehlern ab (statt etwas zu zerstören)
- Ruft das LLM mit PROTOKOLL_GENERIERE_FACHGEBIETE auf
- Merged neue Domains in die bestehende Liste (Update-Modus)
- Schreibt die aktualisierte domains.json zurück

Dieses Skript verändert nichts außerhalb des Projektcontainers (0.1).
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set

from llm_wrapper import call_llm

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
DOMAINS_FILE = DATA_DIR / "domains.json"


def load_existing_domains() -> List[Dict[str, Any]]:
    """Lädt bestehende Domains, falls vorhanden. Bei leerer Datei -> []."""
    if not DOMAINS_FILE.exists():
        print("[INFO] data/domains.json existiert noch nicht. Starte mit leerer Liste.")
        return []

    text = DOMAINS_FILE.read_text(encoding="utf-8").strip()
    if not text:
        print("[INFO] data/domains.json ist leer. Starte mit leerer Liste.")
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[ERROR] domains.json ist kein gültiges JSON: {e}")
        return []

    if not isinstance(data, list):
        print("[ERROR] domains.json muss ein JSON-Array sein.")
        return []

    return data


def validate_domains(domains: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Prüft bestehende Domains grob auf Strukturfehler."""
    errors: List[str] = []
    ids: Set[str] = set()
    for idx, d in enumerate(domains):
        if not isinstance(d, dict):
            errors.append(f"Eintrag #{idx} ist kein Objekt: {type(d)}")
            continue

        for key in ("id", "label", "description"):
            if key not in d:
                errors.append(f"Eintrag #{idx} fehlt Feld '{key}': {d}")
        dom_id = d.get("id")
        if isinstance(dom_id, str):
            if dom_id in ids:
                errors.append(f"Doppelte id '{dom_id}' in domains.json")
            ids.add(dom_id)
        else:
            errors.append(f"Eintrag #{idx} hat ungültige id: {dom_id!r}")

        coords = d.get("coordinates")
        if coords is not None and not isinstance(coords, list):
            errors.append(f"Eintrag #{idx} 'coordinates' ist nicht Liste: {coords!r}")

    ok = len(errors) == 0
    return ok, errors


PROTOKOLL_GENERIERE_FACHGEBIETE = """
PROTOKOLL_GENERIERE_FACHGEBIETE

ROLE:
Du bist Teil des Forschungsprogramms „Aufrichtigkeit“ (MMS). 
Du kennst die MMS-Koordinaten: körperlich, geistig, emotional, sozial, ökonomisch, zeitlich, existentiell, technisch/digital.

TASK:
Erzeuge eine Liste von Fachgebieten, die für die Erforschung von Aufrichtigkeit, Reife und Fehlallokation relevant sind.
Die Fachgebiete sollen die menschliche Lebenswelt möglichst vollständig abdecken
(z.B. Gesundheit, Arbeit, Beziehungen, Politik, Technik, Recht, Spiritualität, Ökonomie, Bildung usw.).

REQUIREMENTS:
- Erzeuge zwischen 30 und 80 Fachgebiete.
- Keine Duplikate.
- Jedes Fachgebiet soll so konkret sein, dass man später Probleme darunter einsortieren kann.
- Keine zu allgemeinen Begriffe wie „Sonstiges“ oder „Alles“.
- Keine extrem speziellen Nischen (zu fein).
- Jedes Fachgebiet soll sinnvoll in die MMS-Koordinaten eingetragen werden können.

OUTPUT_FORMAT:
Antworte NUR mit einem JSON-Array.
Jedes Element ist ein Objekt mit:
- "id": kurzer maschinenlesbarer Name in snake_case (z.B. "gesundheit", "arbeit_und_beruf")
- "label": Klartextname des Fachgebiets in Deutsch
- "description": 1–3 Sätze, warum dieses Fachgebiet für Aufrichtigkeit/Reife relevant ist.
- "coordinates": Liste der relevanten MMS-Koordinaten (z.B. ["sozial", "ökonomisch"])
"""


def parse_new_domains(raw: str) -> List[Dict[str, Any]]:
    """Parst und validiert die vom LLM generierten Domains."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM-Antwort ist kein gültiges JSON: {e}") from e

    if not isinstance(data, list):
        raise ValueError("LLM-Antwort muss ein JSON-Array sein.")

    for idx, d in enumerate(data):
        if not isinstance(d, dict):
            raise ValueError(f"Eintrag #{idx} ist kein Objekt: {type(d)}")
        for key in ("id", "label", "description", "coordinates"):
            if key not in d:
                raise ValueError(f"Eintrag #{idx} fehlt Feld '{key}': {d}")
        if not isinstance(d["id"], str) or not d["id"]:
            raise ValueError(f"Eintrag #{idx} hat ungültige id: {d['id']!r}")
        if not isinstance(d["coordinates"], list):
            raise ValueError(f"Eintrag #{idx} 'coordinates' ist nicht Liste: {d['coordinates']!r}")

    return data


def merge_domains(existing: List[Dict[str, Any]], new: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    Merged neue Domains in die bestehenden.
    - existierende werden nach id erkannt
    - neue ids werden hinzugefügt
    Rückgabe: (merged_list, count_new, count_updated)
    """
    by_id: Dict[str, Dict[str, Any]] = {d["id"]: d for d in existing if "id" in d}
    count_new = 0
    count_updated = 0

    for d in new:
        dom_id = d["id"]
        if dom_id in by_id:
            # Update-Strategie: wir übernehmen neue Felder,
            # überschreiben aber bestehende nicht blind.
            old = by_id[dom_id]
            updated = old.copy()
            # hier einfache Politik: description/coordinates/label dürfen aktualisiert werden
            for key in ("label", "description", "coordinates"):
                if key in d and d[key] != old.get(key):
                    updated[key] = d[key]
            by_id[dom_id] = updated
            count_updated += 1
        else:
            by_id[dom_id] = d
            count_new += 1

    merged_list = sorted(by_id.values(), key=lambda x: x.get("id", ""))
    return merged_list, count_new, count_updated


def main():
    print(f"[INFO] MMS Domains-Update gestartet. Basis: {BASE}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Bestehende Domains laden und prüfen
    existing = load_existing_domains()
    print(f"[INFO] Gefundene bestehende Domains: {len(existing)}")

    ok, errors = validate_domains(existing)
    if not ok:
        print("[WARN] Es wurden Probleme in bestehenden Domains gefunden:")
        for e in errors:
            print("  -", e)
        print("[ABBRUCH] Bitte domains.json manuell prüfen/korrigieren, bevor neue Domains generiert werden.")
        sys.exit(1)

    # 2. LLM aufrufen
    print("[INFO] Rufe LLM mit PROTOKOLL_GENERIERE_FACHGEBIETE auf ...")
    prompt = PROTOKOLL_GENERIERE_FACHGEBIETE.strip()
    raw_output = call_llm(prompt)

    # 3. Neue Domains parsen
    new_domains = parse_new_domains(raw_output)
    print(f"[INFO] Vom LLM erzeugte Domains: {len(new_domains)}")

    # 4. Mergen
    merged, count_new, count_updated = merge_domains(existing, new_domains)

    print(f"[INFO] Neue Domains hinzugefügt: {count_new}")
    print(f"[INFO] Bestehende Domains aktualisiert: {count_updated}")
    print(f"[INFO] Gesamtzahl Domains nach Merge: {len(merged)}")

    # 5. Schreiben
    DOMAINS_FILE.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] Domains nach {DOMAINS_FILE} geschrieben.")


if __name__ == "__main__":
    main()
