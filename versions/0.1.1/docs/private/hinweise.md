 # Interne Hinweise (nicht veröffentlichen)
Version 0.1.1

Dieses Dokument enthält interne Überlegungen, Entscheidungen und Notizen,
die nicht Teil der öffentlichen Version des MMS werden sollen.

---

## Offene Punkte (intern)

- Feinabstimmung der Koordinatendefinitionen.
- Diskussion: Sollen Knowledge Units immer domain_ids enthalten?
- Wie granular sollen Reife- und Fehlallokationsscores werden?
- Problem: Quality Score ist noch nicht operationalisiert.
- Export-Strategie: Kapitelbildungslogik noch offen.

---

## Nicht-öffentliche Designentscheidungen

- Knowledge Units sind bewusst atomic gehalten (eine Einheit = ein Gedanke).
- JSONL als Format für Knowledge Base wurde gewählt, um Append-Only zu ermöglichen.
- Die Protokolle werden erst ab Version 0.2 öffentlich dokumentiert.

---

## Mögliche Erweiterungen (noch nicht öffentlich diskutieren)

- Einführung eines „Praxislevels“
- Langzeitgraph „human maturity evolution“
- automatische Cluster-Erkennung
- Qualitätssicherung über Heuristiken + LLM


