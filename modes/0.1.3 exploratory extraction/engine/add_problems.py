#!/usr/bin/env python3
"""
engine/add_problems.py

Pipeline-Schritt 2 für MMS 0.1.3:
Arbeitet auf facts/problems/*.jsonl.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

from engine.utils import layout, utils_jsonl


def _write_log(event: str, status: str, details: dict) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "event": event,
        "version": layout.get_version(),
        "status": status,
        "details": details or {},
    }
    utils_jsonl.append_jsonl(layout.LOGS_MAIN_FILE, [entry])


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


def _collect_files(problems_dir: Path, domain: str | None) -> list[Path]:
    if domain is None:
        return sorted(problems_dir.glob("*.jsonl"))
    return [problems_dir / f"{domain}.jsonl"]


def main(argv: list[str] | None = None) -> int:
    """
    Verarbeitet facts/problems/*.jsonl.

    Verwendet layout.PROBLEMS_DIR als Basis.
    """
    argv = argv if argv is not None else sys.argv[1:]
    domain = argv[0] if argv else None

    problems_dir = Path(layout.PROBLEMS_DIR)
    files = _collect_files(problems_dir, domain)
    files = [f for f in files if f.exists()]

    total_files = 0
    total_problems = 0

    try:
        if not files:
            if domain:
                print(
                    f"[problems.add] Keine Problem-Datei für Domäne '{domain}' gefunden "
                    f"unter: {problems_dir}"
                )
            else:
                print(
                    f"[problems.add] Keine Problem-Dateien gefunden unter: {problems_dir}"
                )
        else:
            for path in files:
                count = 0
                for _ in _iter_json_lines(path):
                    count += 1
                total_files += 1
                total_problems += count
                # Wichtig: Der Test sucht nach "Einträge: 2" → dieser Substring muss vorkommen
                print(f"[problems.add] Datei: {path} – Einträge: {count}")

        print(
            f"[problems.add] Zusammenfassung: {total_files} Datei(en), "
            f"{total_problems} Problem-Einträge"
        )

        _write_log(
            event="problems.add",
            status="success",
            details={
                "dir": str(problems_dir),
                "files": total_files,
                "problems": total_problems,
                **({"domain": domain} if domain else {}),
            },
        )
        return 0

    except ValueError as exc:
        msg = str(exc)
        print(f"[problems.add] Fehler: {msg}", file=sys.stderr)
        _write_log(
            event="problems.add",
            status="error",
            details={
                "dir": str(problems_dir),
                "error": msg,
                **({"domain": domain} if domain else {}),
            },
        )
        return 1
    except Exception as exc:
        msg = f"Unerwarteter Fehler: {exc}"
        print(f"[problems.add] {msg}", file=sys.stderr)
        _write_log(
            event="problems.add",
            status="error",
            details={
                "dir": str(problems_dir),
                "error": msg,
                **({"domain": domain} if domain else {}),
            },
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

