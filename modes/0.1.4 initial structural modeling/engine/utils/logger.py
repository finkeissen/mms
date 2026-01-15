# engine/utils/logger.py

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from engine.utils import layout, utils_jsonl


def write_log(
    event: str,
    status: str,
    details: Mapping[str, Any] | None = None,
) -> None:
    """
    Zentraler Logger für MMS 0.1.4.

    - Schreibt eine JSON-Zeile nach logs/log.jsonl
    - Hält sich an das in README definierte Format:
      {
        "timestamp": "<ISO-8601>",
        "event": "<command>",
        "version": "0.1.4",
        "status": "success" | "error",
        "details": { ... }
      }
    - Nutzt layout.LOGS_MAIN_FILE (damit monkeypatch in Tests greift).
    """
    details_dict = dict(details or {})
    timestamp = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    entry = {
        "timestamp": timestamp,
        "event": event,
        "version": layout.get_version(),
        "status": status,
        "details": details_dict,
    }

    log_path = Path(layout.LOGS_MAIN_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    utils_jsonl.append_jsonl(log_path, [entry])

