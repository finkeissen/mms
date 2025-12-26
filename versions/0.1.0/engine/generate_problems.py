#!/usr/bin/env python3
"""
generate_problems.py

Generiert oder aktualisiert Probleme (Problems) für ein bestimmtes Fachgebiet (Domain)
im MMS-Projekt.

Verhalten:
- Liest bestehende data/problems.jsonl (falls vorhanden)
- Fasst zusammen, wie viele Probleme insgesamt und für die angegebene Domain existieren
- Prüft die Struktur und meldet Probleme
- Bricht bei harten Fehlern ab (statt etwas zu zerstören)
- Liest data/domains.json und holt die angegebene Domain (domain_id)
- Ruft das LLM mit PROTOKOLL_GENERIERE_PROBLEME_FUER_FACHGEBIET auf
- Merged neue Probleme in die bestehende Liste (Update-Modus)
- Schreibt die aktualisierte problems.jsonl zurück

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
PROBLEMS_FILE = DATA_DIR / "problems.jsonl"


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Domains
# ---------------------------------------------------------------------------

def load_domains() -> List[Dict[str, Any]]:
    if not DOMAINS_FILE.exists():
        print(f"[ERROR] {DOMAINS_FILE} existiert nicht. Bitte zuerst 'mms domains' ausführen.")
        sys.exit(1)
    try:
        data = json.loads(DOMAINS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] domains.json ist kein gültiges JSON: {e}")
        sys.exit(1)
    if not isinstance(data, list):
        print("[ERROR] domains.json muss ein JSON-Array sein.")
        sys.exit(1)
    return data


def find_domain(domains: List[Dict[str, Any]], domain_id: str) -> Dict[str, Any]:
    for d in domains:
        if d.get("id") == domain_id:
            return d
    print(f"[ERROR] Domain mit id '{domain_id}' wurde in domains.json nicht gefunden.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Hilfsfunktionen: Problems laden/validieren
# ---------------------------------------------------------------------------

def load_existing_problems() -> List[Dict[str, Any]]:
    """Lädt bestehende Probleme aus problems.jsonl (eine JSON pro Zeile)."""
    if not PROBLEMS_FILE.exists():
        print("[INFO] data/problems.jsonl existiert noch nicht. Starte mit leerer Liste.")
        return []

    lines = PROBLEMS_FILE.read_text(encoding="utf-8").splitlines()
    problems: List[Dict[str, Any]] = []
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Zeile #{idx+1} in problems.jsonl ist kein gültiges JSON: {e}")
            sys.exit(1)
        if not isinstance(obj, dict):
            print(f"[ERROR] Zeile #{idx+1} in problems.jsonl ist kein Objekt: {type(obj)}")
            sys.exit(1)
        problems.append(obj)

    return problems


def validate_problems(problems: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Prüft bestehende Probleme grob auf Strukturfehler."""
    errors: List[str] = []
    ids: Set[Tuple[str, str]] = set()  # (domain_id, id)

    for idx, p in enumerate(problems):
        if not isinstance(p, dict):
            errors.append(f"Eintrag #{idx} ist kein Objekt: {type(p)}")
            continue

        for key in ("id", "domain_id", "label", "short_description", "coordinates", "tension_type"):
            if key not in p:
                errors.append(f"Eintrag #{idx} fehlt Feld '{key}': {p}")
        pid = p.get("id")
        did = p.get("domain_id")
        if isinstance(pid, str) and isinstance(did, str):
            key = (did, pid)
            if key in ids:
                errors.append(f"Doppelte Kombination (domain_id, id) {key!r} in problems.jsonl")
            ids.add(key)
        else:
            errors.append(f"Eintrag #{idx} hat ungültige id/domain_id: id={pid!r}, domain_id={did!r}")

        coords = p.get("coordinates")
        if not isinstance(coords, list):
            errors.append(f"Eintrag #{idx} 'coordinates' ist nicht Liste: {coords!r}")

        tt = p.get("tension_type")
        if not isinstance(tt, str):
            errors.append(f"Eintrag #{idx} 'tension_type' ist kein String: {tt!r}")

    ok = len(errors) == 0
    return ok, errors


def summarize_problems(problems: List[Dict[str, Any]], domain_id: str) -> None:
    total = len(problems)
    per_domain = sum(1 for p in problems if p.get("domain_id") == domain_id)
    print(f"[INFO] Gesamtzahl bestehender Probleme: {total}")
    print(f"[INFO] Bestehende Probleme für Domain '{domain_id}': {per_domain}")


# ---------------------------------------------------------------------------
# Protokoll & LLM-Aufruf
# ---------------------------------------------------------------------------

PROTOKOLL_GENERIERE_PROBLEME = """
PROTOKOLL_GENERIERE_PROBLEME_FUER_FACHGEBIET

ROLE:
Du bist ein interpretierender Agent des MMS und analysierst die menschliche Lebenswelt
im Hinblick auf Reife, Aufrichtigkeit und Fehlallokation.

INPUT:
Du erhältst ein Fachgebiet-Objekt mit Feldern:
- id
- label
- description
- coordinates

TASK:
Generiere typische Probleme (Spannungsfelder, Fehlallokationen, Konflikte),
die im angegebenen Fachgebiet vorkommen und für Reife/Unreife relevant sind.

REQUIREMENTS:
- Erzeuge zwischen 30 und 80 Probleme.
- Jedes Problem muss ein echtes, nicht-triviales Spannungsfeld beschreiben.
- KEINE medizinischen Diagnosen.
- KEINE pathologischen Extremfälle.
- Fokus auf menschliche Dynamiken, Konflikte, Widersprüche.
- Keine Dopplungen innerhalb der Antwort.

OUTPUT_FORMAT:
Antworte NUR mit einem JSON-Array von Objekten mit Feldern:
- "id": maschinenlesbarer Kurzname in snake_case (z.B. "fehlende_berufliche_identitaet")
- "domain_id": id des Fachgebiets
- "label": Klartextproblem
- "short_description": 1–2 Sätze Beschreibung
- "coordinates": Liste von MMS-Koordinaten (z.B. ["sozial", "ökonomisch"])
- "tension_type": z.B. "innere_spannung", "äußere_spannung", "innere_und_äußere_spannung"

Gib NUR das JSON-Array zurück, ohne Erklärungen, ohne Fließtext.
"""


def build_prompt_for_domain(domain: Dict[str, Any]) -> str:
    """Fügt die Domain-Informationen in das Protokoll ein."""
    # Wir hängen die konkrete Domain als JSON-Kontext unten an.
    domain_json = json.dumps(domain, ensure_ascii=False, indent=2)
    prompt = PROTOKOLL_GENERIERE_PROBLEME.strip() + "\n\nFACHGEBIET:\n" + domain_json
    return prompt


def parse_new_problems(raw: str, expected_domain_id: str) -> List[Dict[str, Any]]:
    """Parst und validiert die vom LLM generierten Probleme."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM-Antwort ist kein gültiges JSON: {e}") from e

    if not isinstance(data, list):
        raise ValueError("LLM-Antwort muss ein JSON-Array sein.")

    for idx, p in enumerate(data):
        if not isinstance(p, dict):
            raise ValueError(f"Eintrag #{idx} ist kein Objekt: {type(p)}")
        for key in ("id", "domain_id", "label", "short_description", "coordinates", "tension_type"):
            if key not in p:
                raise ValueError(f"Eintrag #{idx} fehlt Feld '{key}': {p}")
        if p["domain_id"] != expected_domain_id:
            raise ValueError(
                f"Eintrag #{idx} hat domain_id='{p['domain_id']}', erwartet wurde '{expected_domain_id}'."
            )
        if not isinstance(p["coordinates"], list):
            raise ValueError(f"Eintrag #{idx} 'coordinates' ist nicht Liste: {p['coordinates']!r}")
        if not isinstance(p["tension_type"], str):
            raise ValueError(f"Eintrag #{idx} 'tension_type' ist kein String: {p['tension_type']!r}")

    return data


# ---------------------------------------------------------------------------
# Merge & Schreiben
# ---------------------------------------------------------------------------

def merge_problems(
    existing: List[Dict[str, Any]],
    new: List[Dict[str, Any]],
    domain_id: str,
) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    Merged neue Probleme in die bestehenden.
    - Schlüssel ist (domain_id, id)
    - bestehende Probleme anderer Domains bleiben unberührt
    - bestehende Probleme derselben Domain werden ggf. aktualisiert
    Rückgabe: (merged_list, count_new, count_updated)
    """
    by_key = {}  # (domain_id, id) -> problem
    for p in existing:
        did = p.get("domain_id")
        pid = p.get("id")
        if isinstance(did, str) and isinstance(pid, str):
            by_key[(did, pid)] = p
        else:
            # Ungültige Einträge werden trotzdem übernommen, aber nicht als Schlüssel verwendet
            pass

    count_new = 0
    count_updated = 0

    for p in new:
        key = (domain_id, p["id"])
        if key in by_key:
            old = by_key[key]
            updated = old.copy()
            for field in ("label", "short_description", "coordinates", "tension_type"):
                if field in p and p[field] != old.get(field):
                    updated[field] = p[field]
            by_key[key] = updated
            count_updated += 1
        else:
            by_key[key] = p
            count_new += 1

    # Reihenfolge ist für JSONL egal, aber wir sortieren nach (domain_id, id) zur Stabilität.
    merged_list = list(by_key.values())
    merged_list.sort(key=lambda x: (x.get("domain_id", ""), x.get("id", "")))
    return merged_list, count_new, count_updated


def write_problems(problems: List[Dict[str, Any]]) -> None:
    """Schreibt alle Probleme in problems.jsonl (eine JSON pro Zeile)."""
    lines = [json.dumps(p, ensure_ascii=False) for p in problems]
    PROBLEMS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Verwendung: generate_problems.py <domain_id>")
        sys.exit(1)

    domain_id = sys.argv[1]
    print(f"[INFO] MMS Problems-Update gestartet für Domain '{domain_id}'. Basis: {BASE}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Domains laden und Ziel-Domain finden
    domains = load_domains()
    domain = find_domain(domains, domain_id)
    print(f"[INFO] Fachgebiet gefunden: {domain.get('label')} ({domain_id})")

    # 2. Bestehende Probleme laden und prüfen
    existing = load_existing_problems()
    summarize_problems(existing, domain_id)

    ok, errors = validate_problems(existing)
    if not ok:
        print("[WARN] Es wurden Probleme in bestehenden Problemen gefunden:")
        for e in errors:
            print("  -", e)
        print("[ABBRUCH] Bitte problems.jsonl manuell prüfen/korrigieren, bevor neue Probleme generiert werden.")
        sys.exit(1)

    # 3. LLM aufrufen
    print("[INFO] Rufe LLM mit PROTOKOLL_GENERIERE_PROBLEME_FUER_FACHGEBIET auf ...")
    prompt = build_prompt_for_domain(domain)
    raw_output = call_llm(prompt)

    # 4. Neue Probleme parsen
    new_problems = parse_new_problems(raw_output, domain_id)
    print(f"[INFO] Vom LLM erzeugte Probleme für Domain '{domain_id}': {len(new_problems)}")

    # 5. Mergen
    merged, count_new, count_updated = merge_problems(existing, new_problems, domain_id)

    print(f"[INFO] Neue Probleme hinzugefügt: {count_new}")
    print(f"[INFO] Bestehende Probleme aktualisiert: {count_updated}")
    print(f"[INFO] Gesamtzahl Probleme nach Merge: {len(merged)}")

    # 6. Schreiben
    write_problems(merged)
    print(f"[OK] Probleme nach {PROBLEMS_FILE} geschrieben.")


if __name__ == "__main__":
    main()

