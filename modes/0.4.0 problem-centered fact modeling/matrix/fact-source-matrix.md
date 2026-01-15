# MMS 0.4.0 — Fakt×Quelle-Matrix (Spezifikation als View)

## Definition

Die **Fakt×Quelle-Matrix** ist keine eigene „Wahrheitstabelle“, sondern eine
**ableitbare Sicht (View)** über Fact Records.

- Zeilen: *Fakt-Kandidaten* (Claim-Gruppen / Fact Keys)
- Spalten: *Quellen* (inkl. LLM-Modelle als Quellenklasse)
- Zellen: *Status + Referenzen* auf konkrete Records

Wichtig:
- MMS 0.4.0 **speichert Records**.
- Die Matrix wird **aus Records erzeugt** (on-demand oder als Export-Artefakt).

---

## Fakt-Key (Fact Key)

Um Records zu gruppieren, definiert MMS einen **Fact Key**:

- `fact_key` = deterministische Normalisierung eines Claims (minimal)
- Zweck: *Gruppierung*, nicht Ontologie

### Minimaler Ansatz (0.4.0-tauglich)
- `fact_key = hash(normalize(claim.text + claim.language + optional subject.ref))`

> Ohne `subject.ref` bleibt es rein textbasiert (schwächer, aber zulässig).

---

## Matrix-Zelle (Cell)

Eine Zelle enthält keine Wahrheit, sondern:

- `status` ∈ { asserted, unknown, no-claim, conflicting }
- `record_ids`: Liste der Records, die diese Zelle begründen
- optional `notes` (operativ)

Regel:
- **asserted**: mind. 1 asserted-record in dieser Quelle für diesen fact_key
- **no-claim**: Quelle äußert explizit „keine Aussage“
- **unknown**: MMS kann nicht sicher extrahieren / Quelle unklar
- **conflicting**: Quelle liefert widersprüchliche asserted-records zum selben fact_key
  (oder MMS markiert Konflikt via `links.conflicts_with` innerhalb derselben Quelle)

---

## Matrix-Exportformat (JSONL)

MMS kann die Matrix als JSONL exportieren: 1 Zeile = 1 fact_key.

### matrix_record (JSONL line)
- `record_type`: "mms.matrix_row"
- `matrix_id`: Export-Run/Version
- `fact_key`
- `claim_canonical` (optional: ein canonical text für Human-Readability)
- `by_source`: Map `source_id -> cell`

---

## Beispiel: Matrix-Row (JSON)

{
  "record_type": "mms.matrix_row",
  "matrix_id": "matrix-2025-12-31T12:00:00Z",
  "fact_key": "sha256:9f2a...e31",
  "claim_canonical": {
    "text": "Berlin ist die Hauptstadt von Deutschland.",
    "language": "de"
  },
  "by_source": {
    "https://example.org/sources/wiki-berlin": {
      "status": "asserted",
      "record_ids": ["01JH2K7Z1VJQ5Q8N0K2H3F3X8A"]
    },
    "llm:openai:gpt-5.2": {
      "status": "asserted",
      "record_ids": ["01JH2K9A4R..."]
    },
    "https://example.org/sources/other-doc": {
      "status": "unknown",
      "record_ids": ["01JH2K8B7S..."]
    }
  }
}

---

## Scope-Hinweis (warum das in 0.4.0 reicht)

0.4.0 definiert:
- wie Records aussehen (Fact Records)
- wie Gruppierung/Matrix als View entsteht (Fact Key + Cell-Regeln)
- wie Matrix exportiert werden kann (matrix_row JSONL)

0.4.0 definiert NICHT:
- „beste“ Normalisierung
- Ontologien
- Konfliktauflösung über Quellen hinweg
- Gewichtung/Trust

Das kommt (falls gewünscht) in späteren Versionen, ohne das Grundmodell zu brechen.

