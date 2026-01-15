# MMS 0.5.0 — problem-centered LLM extraction (pilot)

**Status:** in development  
**Vorgängerversion:** 0.4.0 — problem-centered fact modeling  
**Charakter:** Pilot / Proof-of-Process

---

## Ziel von 0.5.0

Version **0.5.0** ist ein **Pilot-Release**.

Ziel ist es zu zeigen, dass die in 0.4.0 definierten Strukturen
(**Problem Records**, **Fact Records**, **Prompt-Contract**)
in der Praxis funktionieren, wenn **echte Wissensquellen**
(insbesondere **LLMs**) angebunden werden.

Die zentrale Frage dieser Version lautet:

> *Können wir problemzentriert, reproduzierbar und konfliktfähig
> Fakten aus LLMs extrahieren, ohne das Modell zu verbiegen?*

---

## Leitprinzip

> **Problems first. Extraction second. Matrix last.**

- Jedes Pilot-Experiment startet von **Problem Records**
- LLMs werden gezielt zu **konkreten Problemen** befragt
- Ergebnisse werden ausschließlich als **Fact Records** gespeichert
- Die Matrix ist optionaler Export, nicht Primärziel

---

## Scope von 0.5.0

### Was 0.5.0 tut

- Aufbau einer **minimalen Extraktionspipeline**
- Verwendung von **echten LLMs** als Wissensquellen
- Extraktion von Fakten zu:
  - 10–100 ausgewählten Problem Records
- Erzeugung von:
  - validen `mms.fact_record` JSONL-Dateien
  - inkl. vollständiger LLM-Provenienz (`prompt_hash`, Modell, Provider)
- optional:
  - erster Matrix-Export als Demonstration

---

### Was 0.5.0 ausdrücklich nicht tut

- keine Vollständigkeit über Domänen hinweg
- keine Skalierung auf 100k / 10M Probleme
- keine Ontologie- oder Begriffsnormierung
- keine Konfliktauflösung
- keine Bewertung oder Gewichtung von Quellen
- keine Optimierung von Prompts
- keine Automatisierung „auf Knopfdruck“

Alles oben Genannte ist **bewusst außerhalb des Scopes**.

---

## Eingangsartefakte

0.5.0 arbeitet ausschließlich mit Artefakten,
die in 0.4.0 spezifiziert wurden:

- `problem/problem.schema.json`
- `jsonl/record.schema.json`
- `extraction/prompt-contract.md`
- optional: `matrix/matrix-row.schema.json`

0.5.0 **ändert diese Spezifikationen nicht**,
sondern verwendet sie.

---

## Ausgangsartefakte

Ein erfolgreicher 0.5.0-Pilot erzeugt:

- eine kleine Menge realer `mms.problem` Records
- eine reproduzierbare Menge realer `mms.fact_record` Records
- Logs/Notizen zu:
  - Prompt-Verhalten
  - Status-Verteilung (asserted / unknown / no-claim)
  - typischen Failure-Modes
- optional:
  - eine kleine Fakt×Quelle-Matrix als Export

---

## Ordnerstruktur (empfohlen)

```text
mms/versions/0.5.0/
├── README.md
├── CHANGELOG.md
├── RELEASE-0.5.0.md
├── ROADMAP.md
├── pilot/
│   ├── problems/
│   ├── prompts/
│   ├── runs/
│   └── outputs/
└── notes/

