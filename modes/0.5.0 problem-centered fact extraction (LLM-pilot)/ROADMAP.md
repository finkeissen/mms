# MMS 0.5.0 — Pilot Roadmap  
**problem-centered LLM extraction (pilot)**

Diese Roadmap beschreibt die **konkreten Schritte** für Version **0.5.0**.
Sie ist bewusst **operativ**, **kleinskalig** und **revisionsoffen**.

0.5.0 dient nicht der Vollständigkeit, sondern dem **Belastungstest**
der in 0.4.0 definierten Strukturen.

---

## Leitfrage

> *Funktioniert das MMS-Modell unter realen Bedingungen
> mit echten Problemen und echten LLMs,
> ohne strukturelle Nachbesserungen zu erzwingen?*

---

## Phase 0 — Vorbereitung (Setup)

### Ziele
- saubere Trennung von **Struktur** (0.4.0) und **Ausführung** (0.5.0)
- minimale, aber reproduzierbare Pilotumgebung

### Aufgaben
- [ ] 0.4.0 taggen und einfrieren
- [ ] 0.5.0-Branch anlegen
- [ ] Ordnerstruktur gemäß README anlegen
- [ ] Pilot-Notizen-Template vorbereiten

### Deliverables
- leeres, aber vollständiges `mms/versions/0.5.0/` Verzeichnis
- bestätigte Schema-Kompatibilität zu 0.4.0

---

## Phase 1 — Pilot-Probleme definieren

### Ziele
- Auswahl einer **überschaubaren, aber realistischen** Menge an Problemen
- Abdeckung unterschiedlicher Domänen und Problemtypen

### Umfang
- **10–30 atomare Probleme** (Start)
- optional Erweiterung auf **50–100**, falls stabil

### Kriterien für Problem-Auswahl
- klar formulierbar
- faktisch beschreibbar
- potenziell konfliktträchtig
- aus unterschiedlichen Domänen

### Aufgaben
- [ ] Problem-IDs vergeben
- [ ] `mms.problem` Records erstellen
- [ ] minimale Terminologie (2–5 Begriffe pro Problem)
- [ ] Problems in `pilot/problems/` ablegen

### Deliverables
- valide `problem.example.json`-ähnliche Dateien
- Schema-Validierung erfolgreich

---

## Phase 2 — Prompt-Design (minimal)

### Ziele
- **keine Optimierung**, sondern **Stabilität**
- Fokus auf atomare Claims und saubere Status-Zuordnung

### Umfang
- **1–2 Prompt-Templates**
- problemzentrierte Abfrage
- sprachlich klar, aber nicht „smart“

### Aufgaben
- [ ] Prompt-Templates definieren
- [ ] Prompt-Versionen festlegen
- [ ] `prompt_id` vergeben
- [ ] `prompt_hash`-Erzeugung testen

### Deliverables
- dokumentierte Prompt-Templates
- reproduzierbare Prompt-Hashes

---

## Phase 3 — LLM-Anbindung (Quellen)

### Ziele
- Vergleichbarkeit, nicht Vielfalt
- LLMs als **gleichberechtigte Quellen**

### Umfang
- **1–3 LLMs**
  - z. B. ein „großes“, ein „kleineres“, ggf. ein alternatives Modell

### Aufgaben
- [ ] Provider festlegen
- [ ] Modellnamen fixieren
- [ ] Temperatur & Basisparameter dokumentieren
- [ ] erste Testanfragen durchführen

### Deliverables
- dokumentierte LLM-Konfigurationen
- reproduzierbare Antworten bei identischen Inputs

---

## Phase 4 — Extraktionsläufe (Pilot Runs)

### Ziele
- reale Fact Records erzeugen
- Failure-Modes sichtbar machen

### Umfang
- pro Problem:
  - 1–2 Runs
  - pro LLM
- insgesamt:
  - **ca. 30–200 Fact Records**

### Aufgaben
- [ ] Extraktionsläufe durchführen
- [ ] pro Aussage **einen** Fact Record erzeugen
- [ ] Status korrekt setzen
- [ ] `problem_id` überall setzen
- [ ] alle Records schema-validieren

### Deliverables
- JSONL-Dateien mit Fact Records
- vollständige Provenienz
- keine stillen Abbrüche

---

## Phase 5 — Erste Vernetzung & Beobachtung

### Ziele
- prüfen, ob die Struktur **Konflikte zulässt**
- nicht: Konflikte lösen

### Aufgaben
- [ ] gleiche / ähnliche Claims identifizieren
- [ ] `links.related_to` / `links.conflicts_with` testweise setzen
- [ ] Begriffsüberschneidungen dokumentieren
- [ ] Mehrsprachigkeit beobachten

### Deliverables
- annotierte Fact Records
- Notizen zu typischen Konfliktmustern

---

## Phase 6 — Optional: Matrix-Export (Demo)

### Ziele
- **Demonstration**, nicht Vollständigkeit
- Validierung des Matrix-Konzepts

### Umfang
- 1–3 ausgewählte Probleme
- wenige Quellen

### Aufgaben
- [ ] Fact Records gruppieren
- [ ] Matrix-Row(s) erzeugen
- [ ] Export gegen `matrix-row.schema.json` prüfen

### Deliverables
- kleine Fakt×Quelle-Matrix
- Lessons Learned

---

## Phase 7 — Auswertung & Entscheidung

### Ziele
- entscheiden, **ob** und **wie** skaliert wird

### Leitfragen
- Haben die Schemas getragen?
- Gab es strukturelle Brüche?
- Wo war menschliche Nacharbeit nötig?
- Wo entstehen Skalierungsprobleme?

### Aufgaben
- [ ] Erkenntnisse dokumentieren
- [ ] offene Fragen sammeln
- [ ] Go / No-Go für 0.6.0 vorbereiten

### Deliverables
- `RELEASE-0.5.0.md` (Erfahrungsbericht)
- klare Entscheidungsvorlage für nächste Version

---

## Definition of Done (0.5.0)

0.5.0 gilt als abgeschlossen, wenn:

- mindestens ein vollständiger Pilot-End-to-End-Lauf existiert
- alle erzeugten Artefakte schema-konform sind
- kein 0.4.0-Schema geändert werden musste
- reale Konflikte sichtbar wurden
- die nächste Version klar begründet werden kann

---

## Schlussbemerkung

0.5.0 ist bewusst **klein**.

Sein Wert liegt nicht in der Menge der Daten,
sondern in der **Belastbarkeit des Modells**.

