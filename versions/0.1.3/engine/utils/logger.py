# engine/utils/logger.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from engine.utils.layout import LOGS_MAIN_FILE, get_version


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_log(event: str, status: str, details: dict) -> None:
    """
    Minimaler Logger für 0.1.3.

    - Schreibt eine Zeile JSON nach logs/log.jsonl
    - Keine Rotation, keine Sperren, keine Parallelität
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "event": event,
        "version": get_version(),
        "status": status,
        "details": details or {},
    }

    log_path = Path(LOGS_MAIN_FILE)
    _ensure_parent(log_path)
    with log_path.open("a", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")

