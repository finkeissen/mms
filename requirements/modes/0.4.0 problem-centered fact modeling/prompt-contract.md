# MMS 0.4.0 — Prompt / Extraction Contract

## Ziel
Reproduzierbare Extraktion aus LLM-Quellen.

## Anforderungen
- Jeder LLM-Record MUSS enthalten:
  - source.llm.provider
  - source.llm.model
  - source.llm.prompt_hash
- prompt_hash ist Hash über den *exakten* Prompt (Template + Variablen).

## Prompt IDs
- prompt_id referenziert ein versioniertes Prompt-Template (optional).
- prompt_hash ist verpflichtend für Reproduzierbarkeit.

## Output-Regel
LLM-Extraktion MUSS Fact Records erzeugen, die:
- atomare Claims enthalten
- Status korrekt setzen (asserted/unknown/no-claim/conflicting)
- ausreichende Provenienz besitzen

