# engine/add_knowledge.py

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

from engine.utils.layout import FACTS_DIR, LOGS_MAIN_FILE, get_version
from engine.utils import utils_jsonl


KNOWLEDGE_DIR = Path(FACTS_DIR) / "knowledge"


def _write_log(event: str, status: str, details: dict) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "event": event,
        "version": get_version(),
        "status": status,
        "details": details or {},
    }
    utils_jsonl.append_jsonl(LOGS_MAIN_FILE, [entry])


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


def _collect_files(problem: str | None) -> list[Path]:
    if problem is None:
        return sorted(KNOWLEDGE_DIR.glob("*.jsonl"))
    return [KNOWLEDGE_DIR / f"{problem}.jsonl"]


def main(argv: list[str] | None = None) -> int:
    """
    Verarbeitet facts/knowledge/*.jsonl.

    Verhalten gemäß README:
    - ohne Argument: alle Knowledge-Dateien
    - mit <problem>: nur facts/knowledge/<problem>.jsonl
    - JSON-Validierung
    - Zählt Dateien und Knowledge-Einträge
    - schreibt Log-Eintrag 'knowledge.add'
    """
    argv = argv if argv is not None else sys.argv[1:]
    problem = argv[0] if argv else None

    files = _collect_files(problem)
    files = [f for f in files if f.exists()]

    total_files = 0
    total_entries = 0

    try:
        if not files:
            if problem:
                print(
                    f"[knowledge.add] Keine Knowledge-Datei für Problem '{problem}' gefunden "
                    f"unter: {KNOWLEDGE_DIR}"
                )
            else:
                print(
                    f"[knowledge.add] Keine Knowledge-Dateien gefunden unter: {KNOWLEDGE_DIR}"
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

        _write_log(
            event="knowledge.add",
            status="success",
            details={
                "dir": str(KNOWLEDGE_DIR),
                "files": total_files,
                "entries": total_entries,
                **({"problem": problem} if problem else {}),
            },
        )
        return 0

    except ValueError as exc:
        msg = str(exc)
        print(f"[knowledge.add] Fehler: {msg}", file=sys.stderr)
        _write_log(
            event="knowledge.add",
            status="error",
            details={
                "dir": str(KNOWLEDGE_DIR),
                "error": msg,
                **({"problem": problem} if problem else {}),
            },
        )
        return 1
    except Exception as exc:
        msg = f"Unerwarteter Fehler: {exc}"
        print(f"[knowledge.add] {msg}", file=sys.stderr)
        _write_log(
            event="knowledge.add",
            status="error",
            details={
                "dir": str(KNOWLEDGE_DIR),
                "error": msg,
                **({"problem": problem} if problem else {}),
            },
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

