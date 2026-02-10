"""
Test-Konfiguration für MMS 0.1.3.

Stellt sicher, dass das Projekt-Root (mit dem Paket `engine`)
im Python-Suchpfad liegt, damit Imports wie

    from engine import add_domains
    from engine import add_problems
    from engine.utils import layout

zuverlässig funktionieren – unabhängig davon, von wo aus pytest gestartet wird.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Projektwurzel (0.1.3) vorne in sys.path eintragen, falls noch nicht vorhanden
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

