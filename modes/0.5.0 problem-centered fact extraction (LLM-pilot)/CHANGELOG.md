# MMS 0.5.0 — Changelog  
**problem-centered LLM extraction (pilot)**

Dieses Changelog dokumentiert **ausschließlich Änderungen gegenüber 0.4.0**.  
Version 0.5.0 ist ein **Pilot-Release** und dient der praktischen Validierung
der in 0.4.0 definierten Strukturen.

---

## [0.5.0] — problem-centered LLM extraction (pilot)

### Added
- Pilot-Architektur für problemzentrierte LLM-Extraktion
- `ROADMAP.md` zur operativen Steuerung des Pilotablaufs
- Pilot-Ordnerstruktur (`pilot/`) für:
  - Problems
  - Prompts
  - Runs
  - Outputs
- Definition von **realen Extraktionsläufen** mit LLMs
- Definition von Erfolgskriterien für Pilot-Runs
- Optionale Matrix-Exports als Demonstration

---

### Changed
- **Keine Schemaänderungen** an:
  - `problem.schema.json`
  - `record.schema.json`
- Nutzung der bestehenden 0.4.0-Spezifikationen
  als **verbindlicher Rahmen**
- Fokuswechsel:
  - von *Strukturdefinition* (0.4.0)
  - zu *praktischer Anwendung* (0.5.0)

---

### Deprecated
- Keine Features oder Artefakte wurden deprecated

---

### Removed
- Keine Artefakte oder Konzepte wurden entfernt

---

### Fixed
- Keine Bugs behoben (keine operative Implementierung in 0.4.0)

---

### Notes
- 0.5.0 ist bewusst **nicht vollständig**
- 0.5.0 trifft **keine epistemischen Entscheidungen**
- Alle gewonnenen Erkenntnisse fließen in die Planung von **0.6.0+**
- Ein Abbruch oder Neustart nach 0.5.0 ist explizit vorgesehen

---

## Vergleich zu früheren Versionen

- **0.4.0 — problem-centered fact modeling**  
  → definierte stabile Artefaktformen

- **0.5.0 — problem-centered LLM extraction (pilot)**  
  → testet diese Artefaktformen unter realen Bedingungen

---

## Upgrade-Hinweis

Es ist **kein Upgrade bestehender Artefakte** erforderlich.

0.5.0 baut vollständig auf 0.4.0 auf
und verändert keine bestehenden Datenformate.

