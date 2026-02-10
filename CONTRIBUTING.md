# Contributing

## Ziel dieses Dokuments

Dieses Repository ist kein klassisches Open-Source-Projekt im Sinne von Feature-Wachstum oder Community-getriebener Evolution.  
Beiträge sind willkommen, **sofern sie die normativen Ziele des Projekts respektieren**.

Ziel ist Prüfbarkeit, Stabilität und klare Autoritätsgrenzen – nicht maximale Funktionalität.

---

## Grundprinzipien

### 1. Normativ vor funktional
Änderungen an:
- Schnittstellenverträgen
- Schema-Strukturen
- Invarianten
- Garantierten Eigenschaften

haben **Vorrang vor** Implementierungsdetails.

Funktionaler Code darf normativen Regeln **nicht implizit widersprechen**.

---

### 2. Explizite Änderungen statt impliziter Effekte
Beiträge müssen:
- explizit benennen, **was sich ändert**
- klar machen, **ob es sich um eine normative Änderung handelt**
- beschreiben, **welche bestehenden Annahmen dadurch ungültig werden**

„Nebenwirkungen“ gelten als Fehler.

---

### 3. Breaking Changes
Eine Änderung gilt als *breaking*, wenn sie:
- bestehende Snapshots ungültig macht
- Schema-Validierung verändert
- Garantien oder Failure-Modes beeinflusst
- implizite Default-Annahmen einführt oder entfernt

Breaking Changes sind **nur akzeptabel**, wenn sie:
- explizit markiert sind
- begründet werden
- im Changelog klar ausgewiesen sind

---

## Arten von Beiträgen

### Akzeptiert
- Klarstellungen in Dokumentation
- Tests zur Absicherung bestehender Garantien
- Referenzimplementierungen, die bestehende Verträge präziser abbilden
- Werkzeuge zur Verifikation oder Inspektion

### Mit Vorsicht
- Erweiterungen von Schemata
- Neue optionale Komponenten
- Zusätzliche Export-/Integrationspfade

### Nicht akzeptiert
- Implizite Semantik
- Ranking-, Bewertungs- oder Optimierungslogik
- „Convenience Defaults“
- Automatische Konfliktauflösung
- Heuristiken ohne formale Beschreibung

---

## Pull Requests

Jeder Pull Request sollte enthalten:
- eine klare Beschreibung der Änderung
- eine Einordnung: **normativ / strukturell / rein technisch**
- Hinweise auf betroffene Dokumente oder Verträge
- ggf. neue oder angepasste Tests

Pull Requests ohne diese Einordnung können ohne weitere Diskussion geschlossen werden.

---

## Entscheidungsfindung

Die Maintainer behalten sich vor, Beiträge abzulehnen, auch wenn sie technisch korrekt sind,  
sofern sie:
- die Rolle des Systems verwässern
- Autoritätsgrenzen verschieben
- implizite Intelligenz einführen

Ablehnung ist keine Wertung der Qualität, sondern der **Passung zum Systemziel**.

---

## Kommunikation

Diskussionen sollten:
- sachlich
- präzise
- kontraktorientiert

geführt werden.

„Was wäre praktischer?“ ist kein ausreichendes Argument ohne formale Begründung.

---

## Lizenz

Mit Einreichung eines Beitrags erklärst du dich einverstanden, dass dein Beitrag unter der im Repository definierten Lizenz veröffentlicht wird.

