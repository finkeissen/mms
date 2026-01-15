# MMS 0.4.0 — JSONL Fact Records

**Version:** 0.4.0  
**Status:** In development  
**Scope:** Fact-Record-Spezifikation & strukturelle Vorbereitung der Fakt×Quelle-Matrix

---

## Ziel dieser Version

Version **0.4.0** etabliert die **strukturellen und formalen Grundlagen**
für die Speicherung und Vernetzung von Fakten im MMS.

Der Fokus liegt auf der **Definition von Fakt-Records**
als standardisierte, versionierbare und reproduzierbare Artefakte
(in erster Linie im **JSONL-Format**).

Diese Version trifft **keine epistemischen Entscheidungen**
und implementiert **keine vollständige Pipeline**,
sondern definiert die **operativen Voraussetzungen** dafür.

---

## Einordnung im Versionsverlauf

- **0.3.x**  
  → explizite Handover-Disziplin  
  → kontrollierter Import von Wissensquellen  

- **0.4.x (diese Version)**  
  → Definition von Fakt-Records  
  → Vorbereitung der Fakt×Quelle-Matrix  

- **≥ 1.0 (Ziel)**  
  → vollständige, technisch selbsttragende Generierung
    einer Fakt×Quelle-Matrix aus Wissensquellen

---

## Was ist ein „Fakt“ im MMS?

Ein Fakt im MMS ist **keine Wahrheit**.

Ein Fakt ist eine **explizite, quellengebundene Aussage**
über einen behaupteten Zustand der Welt.

Fakten im MMS sind:
- atomar (eine Aussage pro Record)
- quellenabhängig
- zeitlich gebunden
- potenziell widersprüchlich
- nicht abschließend entscheidbar

---

## Fact Records (JSONL)

In MMS 0.4.0 wird ein Fakt als **einzelner JSONL-Record** modelliert.

Jeder Record ist:
- **append-only**
- eindeutig identifizierbar
- vollständig provenance-trackbar
- unabhängig von anderen Records speicherbar

Ein Record repräsentiert **eine Faktbehauptung aus genau einer Quelle**.

---

## Inhalte eines Fact Records (konzeptionell)

Ein Fact Record enthält mindestens:

- eine **stabile ID**
- die **behauptete Aussage** (Claim)
- eine **Quellenreferenz**
- Kontext- und Zeitinformationen
- einen **Status**
  - asserted
  - conflicting
  - unknown
  - no-claim
- optionale Referenzen auf andere Records
  - z. B. Ähnlichkeit, Konflikt, Revision

Die konkrete Felddefinition ist im JSON Schema festgelegt.

Siehe:
- `jsonl/record.schema.json`
- `jsonl/record.example.json`

---

## Beziehungen zwischen Fakten

MMS 0.4.0 erlaubt explizite Beziehungen zwischen Fact Records,
erzwingt jedoch **keine Ontologie**.

Beziehungen dienen der:
- Nachvollziehbarkeit
- Konfliktdarstellung
- Revisionsverfolgung
- Matrixbildung

Die Interpretation dieser Beziehungen liegt **außerhalb** von MMS 0.4.0.

---

## Was 0.4.0 ausdrücklich nicht tut

- keine Wahrheitsentscheidung
- keine Konfliktauflösung
- keine Gewichtung oder Bewertung
- keine Ontologie-Festlegung
- keine vollständige Extraktionspipeline

Alle diese Punkte sind **bewusst außerhalb des Scopes** dieser Version.

---

## Beitrag zur Fakt×Quelle-Matrix

MMS 0.4.0 macht es erstmals möglich,

- Fakten aus Wissensquellen
- als standardisierte Records
- konsistent zu speichern
- und explizit miteinander zu verknüpfen

Damit schafft diese Version die **notwendige Struktur**,
um in späteren Versionen (≥ 1.0)
eine vollständige Fakt×Quelle-Matrix
technisch reproduzierbar zu erzeugen.

---

## Bezug zum Research Program

MMS 0.4.0 ist methodisch kompatibel mit
**research-program 0.4**.

- Begriffe und Grenzen werden übernommen
- keine epistemische Autorität wird abgeleitet
- normative Fragen werden nicht entschieden

Das Research Program definiert den Rahmen,
MMS 0.4.0 implementiert die Struktur.

---

## Zusammenfassung

MMS 0.4.0 ist ein **Struktur-Release**.

Es definiert:
- was ein Fakt im MMS ist
- wie Fakten gespeichert werden
- wie Fakten miteinander in Beziehung treten können

Es entscheidet nicht:
- welche Fakten gelten
- welche Quellen vertrauenswürdig sind
- wie Konflikte aufzulösen sind

Diese Trennung ist **konstitutiv** für das Systemdesign.

