# MMS 0.2.0 — Extraction Pipeline Quickstart
## Domain → Subdomain → Problem Area → Atomic Problem → Problem Detail

This quickstart explains how to run the hardened extraction pipeline end-to-end.

The pipeline is built around:
- a stable **job contract**
- a single **JSON schema** for job results
- strict **JSON-only** prompt templates
- validation + repair loop
- append-only **JSONL persistence**

---

## 1. Prerequisites

### Python
Use Python 3.10+.

### Dependencies
The validator requires `jsonschema`.

Minimal install:
```bash
python -m pip install jsonschema

