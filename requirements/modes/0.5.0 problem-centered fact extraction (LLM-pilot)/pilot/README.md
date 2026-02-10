# MMS 0.5.0 — Pilot Ablauf (LLM-basierte Fakt-Extraktion)

Dieses Dokument beschreibt den **konkreten Ablauf** des 0.5.0-Piloten.
Der Pilot dient der **praktischen Validierung** des MMS-Designs,
nicht der Erstellung einer veröffentlichten Wissensbasis.

---

## Ziel des Piloten

Der Pilot beantwortet ausschließlich diese Fragen:

- Lassen sich **Problem Records** stabil als Ausgangspunkt verwenden?
- Können **LLMs kontrolliert** zu atomaren Fakten abgefragt werden?
- Sind **Schemas, Prompts und Skripte ausreichend robust**?
- Bleiben Fehler sichtbar, nachvollziehbar und „fail-closed“?

Der Pilot trifft **keine Aussagen über Wahrheit, Vollständigkeit oder Qualität**.

---

## Grundprinzip

> **Problem → Extraktion → Fact Records → (optional) Matrix**

- Alles startet bei einem klar definierten `mms.problem`
- LLMs werden als **Quellen**, nicht als Autoritäten behandelt
- Ergebnisse werden ausschließlich als `mms.fact_record` gespeichert
- Die Matrix ist ein **abgeleiteter View**, kein Primärartefakt

---

## Pilot-Struktur

```text
pilot/
├── README.md          ← dieses Dokument
├── problems/          ← manuell erstellte Problem Records
├── contexts/          ← optionale Kontexttexte
├── prompts/           ← versionierte Prompt-Templates
├── scripts/           ← Extraktions- & Hilfsskripte
├── outputs/           ← generierte Artefakte (lokal / privat)
└── notes/             ← Beobachtungen & Lessons Learned

