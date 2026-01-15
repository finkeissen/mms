# Pilot Outputs (0.5.0)

Dieses Verzeichnis enthält die Outputs von Pilot-Runs.

---

## files

### facts.jsonl
- 1 Zeile = 1 `mms.fact_record`
- Jede Zeile MUSS schema-konform sein (0.4.0 `record.schema.json`)
- Jeder LLM-Fact MUSS `source.llm.prompt_hash` enthalten
- `problem_id` SOLLTE gesetzt sein (Pilot: praktisch verpflichtend)

### run-report.json
Ein Report pro Run mit:
- Zusammenfassung (Counts)
- Liste der verwendeten Probleme
- Fehlerliste (falls vorhanden)
- Parameter (Provider/Model/Temperature)

---

## empfohlenes Fehlermanagement (Härtung)

- **Fail-closed**: Bei Parser-/Schemafehlern keine Records schreiben, sondern Fehler loggen.
- **Retry-Regeln** (max 2):
  1) einmal mit identischem Prompt neu versuchen
  2) dann mit `status="unknown"` abbrechen
- **Idempotenz**:
  - Wenn `run_id` + `problem_id` bereits geschrieben wurde, nicht doppelt schreiben.
- **Schema-Validation**:
  - jede Zeile validieren bevor sie persistiert wird.
- **Audit**:
  - `run-report.json` MUSS alle Fehler enthalten.

