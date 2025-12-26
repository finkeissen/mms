#!/usr/bin/env python3
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Sicherheitscheck: nur im Versionsordner 0.1 laufen
if BASE.name != "0.1":
    raise SystemExit(
        f"SICHERHEIT: setup_mms_project.py darf nur im Ordner '0.1' laufen. Aktuell: {BASE}"
    )

DIRS = [
    "docs",
    "data",
    "engine",
    "exports",
    "schema",
]

FILES = {
    "docs/README.md": "# MMS – Metamodell des Menschlichen Systems\n\n"
                      "Dies ist die Version 0.1 des MMS-Projekts.\n"
                      "Ziel: Aufbau einer Wissensbasis über Probleme, Reife und Aufrichtigkeit\n"
                      "mittels philosophischer Programmierung (LLM-gestützte Algorithmen in natürlicher Sprache).\n",

    "docs/konstanten.md": "# Philosophische Konstanten des MMS\n\n"
                          "Hier werden die grundlegenden Axiome, Koordinaten und Qualitätskriterien\n"
                          "des MMS festgehalten. (Entwurfsversion 0.1)\n",

    "docs/strategy.md": "# Gesamtstrategie MMS 0.1\n\n"
                        "1. Aufbau der Projektstruktur und Container-Sicherheit\n"
                        "2. Definition philosophischer Protokolle (natürlichsprachige Algorithmen)\n"
                        "3. Generierung von Fachgebieten (Domains)\n"
                        "4. Generierung von Problemen je Fachgebiet\n"
                        "5. Anreicherung der Probleme (Ursachen, Folgen, Reife, Unaufrichtigkeit)\n"
                        "6. Verknüpfung (up/down/side) und Qualitätsbewertung\n"
                        "7. Export in menschenlesbare Kapitel\n",

    "docs/protokolle.md": "# Philosophische Protokolle (Version 0.1)\n\n"
                          "Hier werden die natürlichsprachigen Algorithmen definiert,\n"
                          "die von LLMs ausgeführt werden (philosophische Programmierung).\n\n"
                          "- PROTOKOLL_GENERIERE_FACHGEBIETE\n"
                          "- PROTOKOLL_GENERIERE_PROBLEME_FUER_FACHGEBIET\n"
                          "- PROTOKOLL_ANREICHERE_PROBLEM\n"
                          "- PROTOKOLL_VERKNUEPFE_PROBLEME\n"
                          "- PROTOKOLL_BEWERTE_QUALITAET\n",

    "docs/metamodell.md": "# Metamodell des MMS\n\n"
                          "Hier wird das bestehende Metamodell dokumentiert und später mit den\n"
                          "Schemas in /schema verknüpft. In Version 0.1 verwenden wir das bereits\n"
                          "vorhandene Metamodell und verfeinern es iterativ.\n",

    "data/domains.json": "[]",
    "data/problems.jsonl": "",
    "data/knowledge_base.jsonl": "",

    "engine/llm_wrapper.py":
        "def call_llm(prompt: str) -> str:\n"
        "    \"\"\"Platzhalter: Hier wird der Aufruf zum lokalen oder API-LLM implementiert.\"\"\"\n"
        "    raise NotImplementedError('Implementiere den LLM-Aufruf hier.')\n",

    "engine/generate_domains.py": "# TODO: Implementiere Generierung der Fachgebiete (Domains).\n",
    "engine/generate_problems.py": "# TODO: Implementiere Generierung der Probleme je Fachgebiet.\n",
    "engine/enrich_problem.py": "# TODO: Implementiere Anreicherung der Probleme (Ursachen, Folgen, Reife...).\n",
    "engine/link_problems.py": "# TODO: Implementiere Verknüpfung (up/down/side) und Duplikatbereinigung.\n",
    "engine/evaluate_quality.py": "# TODO: Implementiere Qualitäts- und Reife-Bewertung.\n",

    "schema/problem.schema.json": "{}\n",
    "schema/domain.schema.json": "{}\n",
    "schema/metadata.schema.json": "{}\n",

    "VERSION": "0.1.0\n",
}

def main():
    print(f"Erzeuge/aktualisiere MMS-Projektstruktur unter {BASE}")

    for d in DIRS:
        path = BASE / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Verzeichnis: {path}")

    for file_path, content in FILES.items():
        full_path = BASE / file_path
        if not full_path.exists():
            full_path.write_text(content, encoding="utf-8")
            print(f"[OK] Datei erstellt: {full_path}")
        else:
            print(f"[SKIP] Datei existiert bereits: {full_path}")

    print("\n🎉 MMS Projektstruktur (0.1) ist konsistent und sicher eingerichtet.")

if __name__ == "__main__":
    main()

