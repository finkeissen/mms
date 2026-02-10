# Philosophische Protokolle  
Version 0.1  
Metamodell des Menschlichen Systems

Dieses Dokument definiert die natürlichsprachlichen Algorithmen des MMS.
Sie werden von LLMs ausgeführt und bilden die Grundlage für alle Engine-Skripte.

Das MMS nutzt „philosophische Programmierung“:
– alle Operationen werden durch präzise formulierte Protokolle geregelt  
– LLMs führen diese Protokolle strikt aus  
– Ausgaben erfolgen in definierten JSON-Formaten  

Die Protokolle basieren auf den philosophischen Konstanten in `konstanten.md`.

---

# 1. PROTOKOLL_GENERIERE_FACHGEBIETE

**ROLE**  
Du bist Teil des Forschungsprogramms „Aufrichtigkeit“ (MMS).  
Du kennst die MMS-Koordinaten: körperlich, geistig, emotional, sozial, ökonomisch, zeitlich, existentiell, technisch/digital.

**TASK**  
Erzeuge eine strukturierte Liste von Fachgebieten, die für die Erforschung von Aufrichtigkeit, Reife und Fehlallokation relevant sind.  
Die Fachgebiete sollen die menschliche Lebenswelt möglichst vollständig abdecken.

**REQUIREMENTS**
- 30 bis 80 Fachgebiete  
- keine Duplikate  
- klar benennbar, keine Nischen  
- so konkret, dass man später Probleme zuordnen kann  
- jedes Fachgebiet muss sinnvoll in MMS-Koordinaten verortbar sein (siehe `konstanten.md`)  

**OUTPUT_FORMAT**  
Antworte **NUR** mit einem JSON-Array folgender Struktur:

```json
[
  {
    "id": "arbeit_und_beruf",
    "label": "Arbeit und Beruf",
    "description": "Kontexte von Erwerbsarbeit, Leistung, Integrität, Loyalität und Wirksamkeit.",
    "coordinates": ["sozial", "ökonomisch"]
  },
  ...
]

