# MMS 0.4.0 — Vorgehen (APPROACH)

Dieses Dokument beschreibt das **konkrete Vorgehen** in MMS **Version 0.4.0**.
Es ist bewusst **operativ** und **nicht epistemisch**.
Es ergänzt die formalen Spezifikationen (Schemas), ersetzt sie aber nicht.

---

## Ziel von 0.4.0

MMS 0.4.0 ist ein **Struktur- und Vorbereitungs-Release**.

Ziel ist es,
- Fakten,
- Probleme,
- Quellen
in **klar getrennten, stabilen Artefaktformen** abzulegen,
sodass spätere Versionen (≥ 1.0) daraus
eine vollständige Fakt×Quelle-Matrix erzeugen können.

0.4.0 selbst erzwingt **keine Vollständigkeit** und **keine Wahrheit**.

---

## Zentrales Designprinzip

> **Ein atomarer Sachverhalt → ein Problem-Record.**  
> **Eine behauptete Aussage aus einer Quelle → ein Fact Record.**

Alles Weitere (Vernetzung, Matrix, Normalisierung) ist **abgeleitet**.

---

## Artefakttypen in 0.4.0

### 1) Problem Records (`mms.problem`)

- genau **ein JSON-Objekt pro atomarem Problem**
  - z. B. Krankheitsbild
  - Tatbestand
  - juristischer Normtatbestand
- Problem Records sind **Ankerobjekte**
- sie enthalten:
  - Domäne / Subdomäne
  - Titel / Kurzbeschreibung
  - Terminologieoberfläche (Begriffe, Sprachen, Synonyme)
- sie treffen **keine Aussagen über Fakten**

Schema:
- `problem/problem.schema.json`

---

### 2) Fact Records (`mms.fact_record`)

- genau **eine behauptete Aussage aus genau einer Quelle**
- Facts sind **quellenabhängig** und **potenziell widersprüchlich**
- Fact Records enthalten:
  - Claim (Text + Sprache)
  - Quelle + Locator
  - Status (asserted / unknown / no-claim / conflicting)
  - optionale Provenienz
- Fact Records **können**, aber müssen nicht,
  einem Problem zugeordnet sein (`problem_id`)

Schema:
- `jsonl/record.schema.json`

---

## Bindung zwischen Problems und Facts

- In 0.4.0 ist `problem_id` in Fact Records **optional**
- Ziel ist es, schrittweise:
  - alle Fact Records
  - eindeutig an ein Problem zu binden
- spätere Versionen können `problem_id` verpflichtend machen

Diese Bindung ermöglicht:
- problemzentrierte Extraktion
- problemzentrierte Auswertung
- problemzentrierte Matrixbildung

---

## Terminologie & Vernetzung (Soft Linking)

In 0.4.0 erfolgt Vernetzung **nicht über Ontologien**, sondern über Begriffe.

### Begriffe in Problem Records
- Problem Records enthalten eine Liste von `terms`
- Jeder Term ist:
  - sprachlich markiert
  - typisiert (label, synonym, code, …)
- Diese Begriffe dienen:
  - Auffindbarkeit
  - initialer Vernetzung
  - späterer Normalisierung

### Wichtige Einschränkung
- Gleichheit von Begriffen impliziert **keine Identität**
- Synonymie ist **nicht garantiert**
- Mehrsprachigkeit ist **nicht normalisiert**

Normalisierung, Synonym-Clustering und Sprachabgleich
sind **explizit außerhalb von 0.4.0**.

---

## Fakt×Quelle-Matrix

- Die Fakt×Quelle-Matrix ist **kein Primärartefakt**
- MMS 0.4.0 speichert **keine Matrix**
- Die Matrix ist:
  - ein **View**
  - ein **Export**
  - ein **Snapshot**

Matrixbildung erfolgt:
- aus Fact Records
- gruppiert nach Fact Keys oder Problems
- optional, on-demand

Spezifikation:
- `matrix/fact-source-matrix.md`
- optionales Schema: `matrix/matrix-row.schema.json`

---

## Extraktion aus Wissensquellen (LLMs)

- MMS 0.4.0 erlaubt Extraktion aus LLMs
- Extraktion ist **nicht automatisch vollständig**
- Jeder LLM-basierte Fact Record MUSS:
  - Modell
  - Provider
  - Prompt-Kontext
  - Prompt-Hash
  enthalten

Prompts selbst sind:
- versioniert
- referenzierbar
- aber **nicht Teil des MMS-Core**

Siehe:
- `extraction/prompt-contract.md` (separates Dokument)

---

## Explizit außerhalb des Scopes von 0.4.0

MMS 0.4.0 tut **bewusst nicht**:

- vollständige Domänenabdeckung (80+ Domänen)
- vollständige Subdomänenabdeckung (1.700+)
- Generierung von 100.000+ Problemfeldern
- Generierung von Millionen atomarer Probleme
- Konfliktauflösung oder Wahrheitsentscheidung
- Gewichtung oder Trust-Scoring
- Ontologie-Definition

Diese Schritte sind:
- datengetrieben
- skalierungsabhängig
- versionsübergreifend

---

## Rolle von 0.4.0 im Gesamtfahrplan

- **0.4.0**
  - definiert stabile Artefaktformen
  - trennt Probleme, Fakten und Quellen
  - macht spätere Skalierung möglich

- **0.5.x – 0.9.x**
  - Pipeline-Aufbau
  - Massenextraktion
  - Terminologie-Normalisierung
  - Qualitätsmetriken

- **≥ 1.0**
  - technisch selbsttragendes MMS
  - reproduzierbare Fakt×Quelle-Matrizen
  - DBMS-analoges Fact Management

---

## Zusammenfassung

MMS 0.4.0 schafft **Ordnung vor Skalierung**.

Es stellt sicher, dass:
- jedes Problem einen klaren Anker hat
- jede Aussage nachvollziehbar bleibt
- Konflikte nicht verdeckt werden
- spätere Erweiterungen ohne Bruch möglich sind

Alles Weitere ist bewusst **nachgelagert**.

