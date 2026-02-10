# MMS 0.4.0 — Prompt / Extraction Contract

Dieses Dokument definiert den **verbindlichen Contract** für die Extraktion
von Fakten aus Wissensquellen mithilfe von **Large Language Models (LLMs)**
im Rahmen von **MMS 0.4.0**.

Der Fokus liegt ausschließlich auf:
- **Reproduzierbarkeit**
- **Nachvollziehbarkeit**
- **klarer Verantwortungsabgrenzung**

Nicht auf Qualität, Wahrheit oder Vollständigkeit.

---

## Ziel des Prompt-Contracts

Der Prompt-Contract stellt sicher, dass jede mit LLMs erzeugte Aussage:

- technisch reproduzierbar ist
- eindeutig einer Quelle, einem Modell und einem Prompt zugeordnet werden kann
- als **Fact Record** in MMS abgelegt werden kann
- **keine implizite epistemische Autorität** erhält

---

## Grundprinzip

> **Ein Prompt-Run ist eine Quelle.**

LLMs werden im MMS wie andere Wissensquellen behandelt:
- nicht als Wahrheitserzeuger
- sondern als **Aussagengeneratoren unter expliziten Bedingungen**

---

## Verpflichtende Metadaten bei LLM-Extraktion

Jeder Fact Record mit `source.source_type = "llm"` MUSS folgende Angaben enthalten:

### Quelle (LLM)
- `source.llm.provider`  
  z. B. `"openai"`, `"anthropic"`, `"google"`

- `source.llm.model`  
  z. B. `"gpt-5.2"`, `"claude-3-opus"`

### Prompt-Reproduzierbarkeit
- `source.llm.prompt_hash` (**pflichtig**)  
  Hash über den **exakten Prompt**, inkl.:
  - Template
  - eingesetzte Variablen
  - System-/Developer-Prompt
  - ggf. Kontextfenster

Optional:
- `source.llm.prompt_id`  
  Referenz auf ein versioniertes Prompt-Template

Ohne `prompt_hash` ist ein LLM-basierter Fact Record **ungültig**.

---

## Prompt-Templates

Prompt-Templates sind **nicht Teil des MMS-Core**.

Sie:
- leben in separaten Repositories oder Pipelines
- sind versioniert
- werden über `prompt_id` referenziert
- werden über `prompt_hash` reproduzierbar gemacht

MMS speichert **keine Prompts**, sondern nur deren **Referenzen und Hashes**.

---

## Extraktionsregeln (minimal)

Ein LLM-Prompt zur Fakt-Extraktion MUSS:

1. **Atomare Aussagen erzeugen**
   - genau eine Aussage pro Fact Record
   - keine Listen, keine aggregierten Texte

2. **Unsicherheit explizit zulassen**
   - wenn keine klare Aussage möglich ist:
     - `status = "unknown"` oder
     - `status = "no-claim"`

3. **Keine Konfliktauflösung erzwingen**
   - widersprüchliche Aussagen werden getrennt gespeichert
   - Konflikte werden markiert, nicht gelöst

4. **Keinen Wahrheitsanspruch formulieren**
   - Aussagen werden als Behauptungen formuliert
   - keine normativen Bewertungen

---

## Status-Zuordnung bei LLM-Extraktion

Empfohlene Zuordnung:

- **asserted**  
  → LLM formuliert eine klare, explizite Aussage

- **no-claim**  
  → LLM sagt explizit, dass keine Aussage möglich ist

- **unknown**  
  → LLM-Ausgabe ist unklar, mehrdeutig oder nicht extrahierbar

- **conflicting**  
  → wird nicht vom LLM entschieden, sondern
    durch MMS beim Vergleich mehrerer Records gesetzt

---

## Beziehung zu Problems

- LLM-Extraktion kann problemzentriert erfolgen
- In diesem Fall SOLLTE der Fact Record:
  - `problem_id` enthalten
- Die Zuordnung ist in 0.4.0 optional,
  wird aber für skalierte Extraktion empfohlen

---

## Explizit außerhalb des Scopes

Der Prompt-Contract regelt **nicht**:

- Prompt-Qualität
- Prompt-Optimierung
- Halluzinationsvermeidung
- Bewertungsmetriken
- Ranking oder Gewichtung von LLM-Aussagen
- Auswahl „besserer“ Modelle

Diese Fragen liegen:
- in der Pipeline
- im Research Program
- oder in späteren MMS-Versionen

---

## Minimaler Compliance-Check

Ein LLM-basierter Fact Record ist **0.4.0-konform**, wenn:

- `source.source_type = "llm"`
- `source.llm.provider` vorhanden
- `source.llm.model` vorhanden
- `source.llm.prompt_hash` vorhanden
- Claim ist atomar
- Status ist korrekt gesetzt

---

## Zusammenfassung

Der Prompt-Contract macht LLM-Extraktion:

- explizit
- reproduzierbar
- überprüfbar
- nicht-autoritativ

Er ist die **Brücke** zwischen
sprachbasierten Modellen und
strukturierter Faktverwaltung im MMS.

Alles Weitere ist bewusst **nachgelagert**.

