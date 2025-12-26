# MMS – LLM-Protokolle
Version 0.1.1

Dieses Dokument definiert alle Protokolle des MetaModell-Systems (MMS).  
Ein Protokoll beschreibt, **was** das LLM erzeugen soll und wie die Engine die Ausgabe verarbeitet.

Alle Protokolle arbeiten **inkrementell**, ergänzend und domänenspezifisch.

---

# 1. GENERATE_DOMAINS

## Zweck
Erzeugt neue Domänen (Fachgebiete) als oberste Wissenseinheiten des MMS.

## Eingabe
- bestehende Domains (eingelesen aus `data/domains.jsonl`)

## Ausgabe
- neue Domain-Objekte gemäß `domain.schema.json`

## Regeln
- `domain_id` muss eindeutig sein
- `title` klar und gut verständlich
- `coordinate` gültige Koordinate (körperlich, geistig, emotional, sozial, ökonomisch, zeitlich, existentiell)
- aussagekräftige Beschreibung
- keine Duplikate

## Speicherort

