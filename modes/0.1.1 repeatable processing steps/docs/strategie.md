# Strategie des MetaModell-Systems (MMS)
Version 0.1.1

Dieses Dokument beschreibt die technische und prozessuale Gesamtstrategie des 
Matrix-Management-Systems (MMS). Alle Engine-Skripte, Datenstrukturen und
Protokolle werden an dieser Strategie ausgerichtet.

---

# 1. Systemzweck

Das Matrix-Management-System (MMS) ist ein vollständig autonom lernendes,
lokal ausführbares Wissenssystem. Es verfolgt drei Kernziele:

1. **Alle relevanten Domänen identifizieren**  
2. **Alle Probleme innerhalb jeder Domäne erfassen**  
3. **Zu jedem Problem vollständiges, strukturiertes Wissen erzeugen (Fakten & Lösungen)**  

Dabei soll das System:

- Neues Wissen aus verschiedenen LLM extrahieren,
- mit Hilfe von Tests für jede Aufgabe das optimale LLM ermitelln,
- sich selbst inkrementell erweitern,
- sich laufend selbst kalibrieren,
- Fehler und Probleme während der Laufzeit erkennen,
- und seine eigene Qualität dauerhaft verbessern.

---

# 2. Grundprinzipien

## 2.1 Autonomie
Das MMS arbeitet weitgehend selbständig:

- erzeugt neue Domänen,
- findet und formuliert Probleme,
- erzeugt und erweitert Wissen,
- bewertet sich selbst,
- trifft Entscheidungen zur Modell- und Protokollwahl.

## 2.2 Inkrementalität & Idempotenz
Jeder Lauf eines Skripts:

- **ergänzt** Daten (append-only),
- ist **idempotent** (mehrfach ausführbar ohne Zerstörung),
- kann jederzeit abgebrochen und später fortgesetzt werden.

Keine Engine soll jemals „alles neu generieren“ müssen, sondern immer nur:

> *„Was fehlt noch?“* ergänzen.

## 2.3 Selbstkalibrierung auf allen Ebenen
Das MMS kalibriert sich kontinuierlich selbst:

- **Modell-Ebene:**  
  Welches LLM eignet sich für welche Aufgabe am besten (Domänen, Probleme, Knowledge, Qualität, Summaries, Exporte…)?

- **Protokoll-Ebene:**  
  Welche Prompt-Varianten, Parameter, Temperaturen, Samplingmethoden liefern die besten Ergebnisse?

- **System-Ebene:**  
  Welche Bereiche sind unterversorgt, redundant, widersprüchlich oder qualitativ schwach?

Diese Entscheidungen werden in Konfigurations- und Metadateien persistiert und in zukünftigen Läufen berücksichtigt.

## 2.4 Lokale Ausführung
Das System ist vollständig lokal lauffähig:

- lokales Dateisystem,
- lokale LLMs (oder konfigurierbare Backends),
- keine Cloud-Abhängigkeit erforderlich.

## 2.5 Domänenspezifisches Sharding
Alle Problems und Knowledge Units werden **pro Domäne** in eigenen Dateien abgelegt:

- `data/problems/<domain_id>.jsonl`
- `data/knowledge/<domain_id>.jsonl`

So bleiben die Dateien auch bei sehr großen Datenmengen handhabbar.

## 2.6 Self-Healing & Fehlerprotokolle
Fehler werden nicht nur am Ende sichtbar, sondern:

- während der Laufzeit erkannt,
- in Fehlerprotokollen erfasst,
- für spätere Analysen und Lernprozesse genutzt.

Das System soll aus Fehlern lernen und diese schrittweise reduzieren.

---

# 3. Gesamtprozess (Autonomie-Pipeline)

Der Gesamtprozess ist rekurrent, d. h. er wird immer wieder durchlaufen.  
Jeder Durchlauf erweitert, verbessert und kalibriert das System.

## 3.1 Schritte der Pipeline

1. **Domänen erzeugen & pflegen**  
   - Engine: `add_domains.py`  
   - Protokoll: GENERATE_DOMAINS  

2. **Probleme erzeugen & erweitern**  
   - Engine: `add_problems.py`  
   - Protokoll: GENERATE_PROBLEMS  

3. **Probleme anreichern (Kontext)**  
   - Engine: `enrich_problem.py`  
   - Protokoll: ENRICH_PROBLEM  

4. **Wissen erzeugen (Knowledge Units)**  
   - Engine: `add_knowledge.py`  
   - Protokoll: ADD_KNOWLEDGE  

5. **Relationen herstellen**  
   - Engine: `link_problems.py`  
   - Protokoll: LINK_PROBLEMS  

6. **Qualität bewerten & Reife prüfen**  
   - Engine: `evaluate_quality.py`  
   - Protokoll: EVALUATE_QUALITY  

7. **Selbstkalibrierung & Modelltests**  
   - Engine: `calibrate_models.py` (später)  
   - Protokoll: CALIBRATE_MODELS  

8. **Exports & Views erzeugen**  
   - Engine: `export_views.py` (später)  
   - Protokoll: EXPORT_VIEWS  

Jede dieser Stufen kann unabhängig voneinander erneut ausgeführt werden.

---

# 4. Datenlayout und Speicherstrategie

Die Datenorganisation ist entscheidend für Skalierbarkeit, Robustheit und Transparenz.

## 4.1 Domains (Hauptdomänen)

Datei:

