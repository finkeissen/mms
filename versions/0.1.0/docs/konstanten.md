# Philosophische Konstanten des MMS  
Version 0.1  
Metamodell des Menschlichen Systems

Dieses Dokument definiert die grundlegenden Konstanten des MMS.
Sie bilden das Axiomfundament des gesamten Projekts und sind für alle
philosophischen Protokolle (natürlichsprachliche Algorithmen) verbindlich.

Alle späteren Strukturen (Domains, Probleme, Reifegrade, Reifeprozesse,
Unaufrichtigkeitsmuster, Verknüpfungen) basieren auf diesen Konstanten.

---

# 1. Grundaxiome

Diese Axiome gelten systemweit. Sie beschreiben die fundamentalen
Eigenschaften menschlicher Wahrnehmung, Interpretation und Handlung.

## 1.1 Axiom – Wahrnehmung
Wahrnehmung ist immer unvollständig, perspektivabhängig und selektiv.
Sie wird beeinflusst durch:
- Aufmerksamkeit
- Emotionen
- Interessen
- kulturelle Muster
- Angst und Abwehrmechanismen
- Reifegrad

## 1.2 Axiom – Interpretation
Interpretationen sind Modelle der Realität.
Sie können:
- reif oder unreif sein  
- verzerrt oder kohärent  
- komplexitätsfähig oder vereinfachend  
- stabil oder fragil  

Interpretation ist niemals neutral.

## 1.3 Axiom – Handeln
Handeln ist die Umsetzung von Wahrnehmung + Interpretation + Motivation
in konkretes Verhalten.
Es zeigt, wie ein Mensch tatsächlich die Welt navigiert.

## 1.4 Axiom – Aufrichtigkeit
Aufrichtigkeit ist die Kohärenz zwischen:
- Wahrnehmung  
- Interpretation  
- Motivation  
- Handlung  

Sie erfordert:
- Minimierung verzerrender Mechanismen  
- Bereitschaft zur Realität  
- Integrität zwischen Innen und Außen  
- Mut, Spannungen und Widersprüche auszuhalten  

## 1.5 Axiom – Reife
Reife ist die Fähigkeit,
- Komplexität wahrzunehmen  
- Widersprüche zu integrieren  
- Perspektiven auszuhalten  
- langfristig zu handeln  
- Verantwortung zu übernehmen  

Reife ist ein gradueller, kontinuierlicher Prozess.

## 1.6 Axiom – Fehlallokation
Fehlallokation ist eine inkonsistente oder ineffiziente Zuordnung von:
- Aufmerksamkeit  
- Zeit  
- Energie  
- Werten  
- Emotion  
- Handlungsmöglichkeiten  

Fehlallokation ist oft das Kernproblem hinter Unaufrichtigkeit und Unreife.

---

# 2. Koordinaten menschlicher Existenz

Die Koordinaten definieren den konzeptuellen Raum, in dem Probleme,
Domänen und Reifeprozesse eingeordnet werden.

Sie sind **keine Kategorien**, sondern **Dimensionen**, entlang derer
Phänomene beschrieben werden.

## 2.1 Standard-Koordinaten des MMS (Version 0.1)

1. **körperlich**  
   – alles, was den Körper, Gesundheit, biologische Grenzen betrifft

2. **geistig**  
   – Denken, Wissen, Orientierung, Rationalität, Modelle

3. **emotional**  
   – Gefühle, Bindung, Affektregulation, emotionale Intelligenz

4. **sozial**  
   – Beziehungen, Rollen, Status, Gruppendynamik, Kooperation

5. **ökonomisch**  
   – Ressourcen, Arbeit, Versorgung, materielle Sicherheit

6. **zeitlich**  
   – Vergangenheit, Gegenwart, Zukunft; Planung und Reifeverläufe

7. **existentiell**  
   – Sinn, Tod, Freiheit, Verantwortung, Identität, Werte

8. **technisch/digital**  
   – Technologie, Systeme, KI, Infrastruktur, digitale Navigation

Diese Koordinaten dienen:
- der Einordnung von Fachgebieten  
- der Analyse von Problemen  
- der Ableitung von Reifeprozessen  
- der Bewertung von Unaufrichtigkeit  

---

# 3. Qualitätskriterien

Diese Kriterien definieren, wann ein Wissenseintrag (Domain oder Problem)
als qualitativ hochwertig gilt.

## 3.1 Klarheit
Der Eintrag ist verständlich, präzise und eindeutig formuliert.

## 3.2 Relevanz
Der Eintrag trägt zur Erforschung von Aufrichtigkeit, Reife oder Fehlallokation bei.

## 3.3 Strukturqualität
Der Eintrag ist korrekt im MMS-Koordinatenraum positioniert.

## 3.4 Fraktalität
Der Eintrag lässt es zu, dass über- oder untergeordnete Probleme sinnvoll
aus ihm abgeleitet werden können.

## 3.5 Nicht-Trivialität
Der Eintrag beschreibt echte Spannungen oder Konflikte, keine Banalitäten.

---

# 4. System-Operationen

Diese Operationen bilden die „philosophische Programmiersprache“ des MMS.

## 4.1 erzeuge()
Erzeugt neue Entitäten: Domains, Probleme, Relationen, Beispiele usw.

## 4.2 verfeinere()
Macht eine Entität granularer oder detaillierter.

## 4.3 verallgemeinere()
Hebt eine Entität auf ein höheres Abstraktionsniveau.

## 4.4 verknüpfe()
Setzt Beziehungen:  
- up_relations  
- down_relations  
- side_relations  

## 4.5 bewerte()
Bestimmt Qualität, Reifegrad, Fehlallokation.

## 4.6 bereinige()
Entfernt Duplikate und behebt strukturelle Inkonsistenzen.

---

# 5. Speicher- und Wissensstrategie

## 5.1 Kanonische Wissensbasis
Datei: `data/knowledge_base.jsonl`  
Format: jede Zeile ein JSON-Objekt  
Eigenschaft:
- unveränderlicher Append-Only-Log  
- ideal für semantische Suche  
- ideal für LLM-Abfragen

## 5.2 Menschlich lesbare Exporte
Unter `exports/` liegen später Kapitel wie:
- `kapitel_arbeit.md`
- `kapitel_beziehungen.md`
- `kapitel_ökonomie.md`
- usw.

Diese Exporte sind nur „Views“ auf die Wissensbasis.

---

# 6. Versionierung

Diese Datei beschreibt Version 0.1 der MMS-Konstanten.
Spätere Versionen ändern oder erweitern diese Liste,
aber niemals rückwirkend („keine Geschichte umschreiben“).

