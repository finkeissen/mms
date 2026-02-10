# Changelog

Dieses Changelog dokumentiert **wesentliche Änderungen** an diesem Repository.

Der Fokus liegt auf:
- normativen Änderungen
- strukturellen Anpassungen
- breaking changes

Nicht jede interne Refaktorierung wird hier aufgeführt.

---

## Versionierung

Dieses Projekt folgt **keiner klassischen SemVer-Logik**.

Stattdessen wird unterschieden zwischen:
- **normativen Änderungen**
- **strukturellen Änderungen**
- **rein technischen Änderungen**

Die Versionsnummern dienen der Orientierung, nicht der Kompatibilitätsgarantie.

---

## Begriffe

### Normative Änderung
Eine Änderung, die:
- Schnittstellenverträge betrifft
- Schema-Strukturen verändert
- garantierte Eigenschaften beeinflusst
- Failure-Modes oder Invarianten anpasst

Normative Änderungen **können breaking sein**, auch ohne API-Änderung.

---

### Strukturelle Änderung
Eine Änderung, die:
- Projektstruktur
- Dokumentationshierarchie
- Referenzimplementierung

betrifft, ohne die normativen Aussagen zu verändern.

---

### Technische Änderung
Eine Änderung, die:
- Codequalität
- Tests
- interne Abläufe

betrifft und keine externen Garantien verändert.

---

## Breaking Changes

Eine Änderung gilt als *breaking*, wenn sie:
- bestehende Snapshots ungültig macht
- Schema-Validierung verändert
- implizite Annahmen einführt oder entfernt
- das Verhalten an Fehler- oder Grenzfällen ändert

Breaking Changes werden **explizit gekennzeichnet**.

---

## Unreleased

### Normativ
- —

### Strukturell
- Initiale Definition von CONTRIBUTING, SECURITY und CHANGELOG

### Technisch
- —

---

## Historie

### Initiale Veröffentlichung

- Definition des Gateway-/Mirror-Kerns
- Snapshot- und Read-only-Prinzip
- Trennung von Knowledge- und Derived-Schemas
- Referenzimplementierung zur Verifikation der Garantien

