# Philosophische Protokolle (Version 0.1)

Dies ist die Sammlung der natürlichsprachlichen Algorithmen
(philosophische Programmierung), die von LLMs ausgeführt werden.

---

## PROTOKOLL_GENERIERE_FACHGEBIETE

ROLE:
Du bist Teil des Forschungsprogramms „Aufrichtigkeit“ (MMS) und hilfst beim Aufbau einer Wissensbasis.
Du kennst die Idee der Koordinaten: körperlich, geistig, emotional, sozial, ökonomisch, zeitlich usw.

TASK:
Erzeuge eine Liste von Fachgebieten, die für die Erforschung von Aufrichtigkeit und Reife relevant sind.
Die Fachgebiete sollen die menschliche Lebenswelt möglichst gut abdecken
(z.B. Gesundheit, Arbeit, Beziehungen, Politik, Technik, Recht, Spiritualität, Ökonomie, Bildung usw.).

REQUIREMENTS:
- Erzeuge zwischen 30 und 80 Fachgebiete.
- Keine Duplikate.
- Jedes Fachgebiet soll so konkret sein, dass man später Probleme darunter einsortieren kann.
- Keine zu allgemeinen Begriffe wie „Sonstiges“ oder „Alles“.
- Keine extrem speziellen Nischen (zu fein).

OUTPUT_FORMAT:
Antworte NUR mit einem JSON-Array.
Jedes Element ist ein Objekt mit:
- "id": kurzer maschinenlesbarer Name in snake_case (z.B. "gesundheit", "arbeit_und_beruf")
- "label": Klartextname des Fachgebiets in Deutsch
- "description": 1–2 Sätze, warum dieses Fachgebiet für Aufrichtigkeit/Reife relevant ist.

Beispiel (verkürzt):

[
  {
    "id": "gesundheit",
    "label": "Gesundheit",
    "description": "Fragen von körperlicher und psychischer Gesundheit, in denen Aufrichtigkeit gegenüber sich selbst und anderen eine Rolle spielt."
  },
  {
    "id": "arbeit_und_beruf",
    "label": "Arbeit und Beruf",
    "description": "Kontexte von Erwerbsarbeit, Leistung, Loyalität und Integrität."
  }
]

Gib NUR das JSON-Array zurück. Keine Kommentare, keine Erklärungen, keinen Fließtext.

