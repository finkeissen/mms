# Changelog

## 0.1.1 – Strategische Konsolidierung, neue Domänenstruktur & Engine-Erweiterung
**Veröffentlicht:** 2025-xx-xx

### 🔧 Strukturelle Kernänderungen
- **Trennung von statischen und dynamischen Domänen**
  - Neue Datei: `data/domains.jsonl` für *statische* (menschlich definierte) Basisdomänen.
  - Neue Datei: `data/generated_domains.jsonl` für *dynamisch* vom MMS erzeugte Domänen.
  - Engines schreiben ausschließlich in `generated_domains.jsonl`.

- **Neues Domänen-Schema**
  - Vollständig überarbeitete `domain.schema.json`:
    - Pflichtfelder: `domain_id`, `title`, `description`, `coordinate`, `type`.
    - Neue Felder: `jurisdiction`, `level`, `origin`, Zeitstempel.
    - `type: static | generated` zur eindeutigen Herkunftsmarkierung.

- **Statische Domänenbasis erweitert**
  - Aufnahme der Domäne **„Medizin“**.
  - Hinzufügen aller relevanten Domänen des **deutschen Bundes- und Landesrechts**.
  - Diese bilden nun das semantische Fundament für spätere automatische Domänengenerierung.

---

### 🤖 Engine- & Protokoll-Verbesserungen
- Engines auf die neue Domänenlogik angepasst:
  - `add_domains.py` erstellt/ergänzt *generated* Domains statt statischer Basis.
  - `add_problems.py` & `add_knowledge.py` sharden korrekt in:
    - `data/problems/<domain_id>.jsonl`
    - `data/knowledge/<domain_id>.jsonl`
  - Idempotente Append-Only-Strategie weiter gefestigt.

- **Selbstkalibrierung vorbereitet**
  - Grundstruktur für Modelltests (`model_performance.jsonl`) angelegt.
  - Protokolle erweitert um Calibration-Hooks.

- **Runtime-Fehlerprotokolle eingeführt**
  - Jeder Engine-Step erzeugt strukturierte Logfiles unter `logs/…`.
  - Fehler werden nicht mehr erst am Ende sichtbar.

---

### 🔍 Verbesserungen in CLI & Infrastruktur
- CLI (`mms`) weiter robust gemacht:
  - Nutzung von `sys.executable` statt festen Python-Strings.
  - Zuverlässige Pfadauflösung innerhalb des Versionscontainers.
  - Verbesserte Fehlermeldungen und konsistentere Konsolen-Ausgaben.

- Konsistente Nutzung von `BASE` in allen Skripten.
- Aufräumarbeiten:
  - Entfernen aller temporären Backup-Artefakte (`*~`).
  - Vereinheitlichte Imports.
  - Entfernen veralteter Module & interne Fixes.

---

### 📘 Dokumentation
- **Metamodell überarbeitet**:
  - Präzise Trennung von Problem-, Knowledge-, Relations- und Meta-Ebenen.
  - Statische vs. dynamische Domänen klar definiert.
- **Strategie aktualisiert**:
  - Selbstkalibrierung, Self-Healing, Fehlerlogs, Qualitätsebenen.
  - Strukturierte Definition der autonomen Wissenspipeline.
- **Schemas dokumentiert** (Domains/Problems/Knowledge).
- **README strukturell modernisiert**.

---

## 0.1.0 – Erstveröffentlichung des MMS-Containers
**Veröffentlicht:** 2025-xx-xx

- Basisprojektstruktur: Erster Versionscontainer `0.1/`
- Erste CLI-Version (`mms`)
- Grundlegende Engine (Domains / Problems)
- Dummy-LLM-Backend
- Erste Dokumentation (`docs/`)

