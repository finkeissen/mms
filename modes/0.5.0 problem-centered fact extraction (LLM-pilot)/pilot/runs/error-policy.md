# Pilot Error Policy (0.5.0)

Diese Policy definiert die minimalen Härtungsregeln für Pilot-Skripte.

---

## Prinzipien

1) **Fail-closed**  
   Bei Unsicherheit wird nicht “geraten”, sondern `unknown` gesetzt oder abgebrochen.

2) **No partial writes**  
   Wenn ein Problem nicht vollständig verarbeitet werden kann, wird für dieses Problem
   **kein** Fact Record geschrieben (oder nur solche, die validiert sind und explizit `unknown` tragen).

3) **Idempotenz**  
   Wiederholte Runs sollen nicht zu Duplikaten führen.

4) **Auditability**  
   Jeder Fehler muss im `run-report.json` dokumentiert werden.

---

## Fehlerklassen

### E1 — Transport/Provider Errors
- Timeouts, Rate limits, Network
- Handling:
  - Retry (max 2)
  - Backoff (mind 5s, dann 30s)
  - danach `unknown` oder Abbruch

### E2 — Output Parsing Errors
- Output ist kein JSON
- Output verletzt Schema
- Handling:
  - 1 Retry mit identischem Prompt + Hinweis “Output MUST be JSON”
  - wenn erneut fehlschlägt: `unknown`

### E3 — Atomicity Violations
- Modell liefert mehrere Aussagen in einem Claim
- Handling:
  - split attempt (nur wenn eindeutig)
  - sonst `unknown`

### E4 — Missing Provenance
- prompt_hash fehlt
- Handling:
  - Record verwerfen
  - Fehler loggen
  - `errors++`

---

## Retry Policy (maximal)

- pro Problem und Prompt:
  - 0–2 Retries
- danach:
  - `unknown` für diesen Prompt/Problem
  - weiter mit nächstem Problem

---

## Minimum Logging

Für jeden Fehler:
- timestamp
- error_code
- problem_id
- prompt_id
- provider/model
- short message
- raw response hash (optional, falls gespeichert)

