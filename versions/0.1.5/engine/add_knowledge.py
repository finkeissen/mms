#!/usr/bin/env python3
"""
engine/add_knowledge.py – Version 0.1.4

Pipeline-Schritt 3:
- arbeitet auf layout.KNOWLEDGE_DIR (facts/knowledge/)
- prüft alle *.jsonl
- validiert JSONL
- zählt Dateien und Knowledge-Einträge
- schreibt Log-Eintrag über den zentralen Logger
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

from engine.utils import layout
from engine.utils.logger import write_log


def _iter_json_lines(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Ungültiges JSON in {path.name} Zeile {lineno}: {exc}"
                ) from exc


def _collect_files(knowledge_dir: Path, problem: str | None) -> list[Path]:
    if problem is None:
        return sorted(knowledge_dir.glob("*.jsonl"))
    return [knowledge_dir / f"{problem}.jsonl"]


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    problem = argv[0] if argv else None

    knowledge_dir = Path(layout.KNOWLEDGE_DIR)
    files = _collect_files(knowledge_dir, problem)
    files = [f for f in files if f.exists()]

    total_files = 0
    total_entries = 0

    try:
        if not files:
            if problem:
                print(
                    f"[knowledge.add] Keine Knowledge-Datei für Problem '{problem}' gefunden "
                    f"unter: {knowledge_dir}"
                )
            else:
                print(
                    f"[knowledge.add] Keine Knowledge-Dateien gefunden unter: {knowledge_dir}"
                )
        else:
            for path in files:
                count = 0
                for _ in _iter_json_lines(path):
                    count += 1
                total_files += 1
                total_entries += count
                print(
                    f"[knowledge.add] Datei: {path} – Knowledge-Einträge: {count}"
                )

        print(
            f"[knowledge.add] Zusammenfassung: {total_files} Datei(en), "
            f"{total_entries} Knowledge-Einträge"
        )

        write_log(
            event="knowledge.add",
            status="success",
            details={
                "dir": str(knowledge_dir),
                "files": total_files,
                "entries": total_entries,
                **({"problem": problem} if problem else {}),
            },
        )
        return 0

    except ValueError as exc:
        msg = str(exc)
        print(f"[knowledge.add] Fehler: {msg}", file=sys.stderr)
        write_log(
            event="knowledge.add",
            status="error",
            details={
                "dir": str(knowledge_dir),
                "error": msg,
                **({"problem": problem} if problem else {}),
            },
        )
        return 1
    except Exception as exc:
        msg = f"Unerwarteter Fehler: {exc}"
        print(f"[knowledge.add] {msg}", file=sys.stderr)
        write_log(
            event="knowledge.add",
            status="error",
            details={
                "dir": str(knowledge_dir),
                "error": msg,
                **({"problem": problem} if problem else {}),
            },
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

