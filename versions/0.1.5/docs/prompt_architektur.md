 # MMS Prompt-Building-Mechanismus

Der MMS Prompt-Building-Mechanismus erzeugt aus mehreren Informationsquellen
einen vollständigen Prompt für ein LLM.  
Der Prompt wird **nicht statisch gespeichert**, sondern **dynamisch erzeugt**.

## 1. Grundidee
Ein MMS-Prompt besteht aus fünf exakt getrennten Schichten:

1. SYSTEM – Regeln, Haltung, Grenzen
2. STRATEGY – operative Arbeitsweise
3. TASK – die konkrete Aufgabe
4. CONTEXT – relevante Daten (Domains, Synonyme, Beispiele)
5. SCHEMA – die exakte Ausgabeform, die einzuhalten ist

Jede Schicht stammt aus einer anderen Datei des Projekts.

## 2. Prompt-Schichten im Detail

### 2.1 SYSTEM (aus: docs/ziele.md)
Enthält:
- Zweck des MMS
- Abgrenzungen
- Qualitätskriterien
- philosophische Leitlinien
- sprachliche Grundregeln

Dieser Teil wird als dauerhafte Systemprompt-Basis genutzt.

### 2.2 STRATEGY (aus: docs/strategy.md)
Enthält:
- Arbeitsprinzipien (klar, präzise, nicht interpretativ)
- Schrittfolgen (zuerst Problem erfassen, dann Frage bilden, etc.)
- Umgang mit Unsicherheit
- Umgang mit Alternativen / Lehrmeinungen

Dieser Teil ist stabil, aber kompakter als SYSTEM.

### 2.3 TASK (aus den Engine-Funktionen)
Kommt aus den Skripten:
- generate_problems.py
- enrich_problem.py
- link_problems.py
- evaluate_quality.py

Der TASK sagt:
- *Was* das LLM tun soll
- *Wie viele* Einträge erzeugt werden sollen
- *Welche Domain* oder *welches Problem* betroffen ist

Beispiel:
„Erzeuge 5 Problem-Einträge für die Domain 'arbeit' nach problem.schema.json.“

### 2.4 CONTEXT (aus data/)
Kommt dynamisch aus:
- domains.jsonl
- domain_hierarchy.jsonl (Dimensionen, Bereiche, Ebenen)
- Synonymlisten
- vorhandene problems/… Dateien
- knowledge/… Dateien
- alternative Lehrmeinungen

Der Kontext wird **automatisch kleiner gemacht**, z.B.:

- Nur relevante Domain-Objekte werden geladen.
- Synonyme nur für die betreffende Domain.
- Knowledge-Einträge nur bei enrich/link.

### 2.5 SCHEMA (aus schema/)
Der exakte JSON-Outputrahmen:
- problem.schema.json
- knowledge_entry.schema.json
- domain.schema.json

Die SCHEMA-Schicht ist **normativ**:  
Das LLM *muss* sich daran halten.

Diese Schicht ist immer **am Ende** des Prompts.

---

## 3. Ablauf der Prompt-Erzeugung

### Schritt 1: SYSTEM laden
→ 3–8 Sätze, extrahiert aus docs/ziele.md

### Schritt 2: STRATEGY laden
→ kurze Arbeitsanweisungen

### Schritt 3: TASK definieren
→ abhängig vom CLI-Befehl

### Schritt 4: CONTEXT einbringen
→ nur relevante Teile

### Schritt 5: SCHEMA anfügen
→ garantiert valide Ausgabe

---

## 4. Beispielhafte Promptstruktur

Der endgültige Prompt sieht immer so aus:


