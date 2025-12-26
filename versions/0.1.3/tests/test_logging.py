# tests/test_logging.py
from __future__ import annotations

from pathlib import Path

from engine import add_domains
from engine.utils import layout
from engine.utils import utils_jsonl


def test_domains_add_writes_log_entry(monkeypatch, tmp_path, capsys) -> None:
    # Domänen-Datei in tmp-Verzeichnis
    facts_dir = tmp_path / "facts"
    facts_dir.mkdir()
    domains_file = facts_dir / "domains.jsonl"
    utils_jsonl.write_jsonl(domains_file, [{"id": "d1", "name": "Test-Domain"}])

    # Log-Datei ebenfalls in tmp-Verzeichnis
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    log_file = logs_dir / "log.jsonl"

    monkeypatch.setattr(layout, "DOMAINS_SOURCE_FILE", domains_file)
    monkeypatch.setattr(layout, "LOGS_MAIN_FILE", log_file)

    rc = add_domains.main([])
    assert rc == 0

    # Prüfen, dass mindestens ein Log-Eintrag geschrieben wurde
    entries = list(utils_jsonl.read_jsonl(log_file))
    assert entries, "Es wurden keine Log-Einträge geschrieben"

    # Optional: Ereignis-Typ prüfen
    assert any(e.get("event") == "domains.add" for e in entries)

