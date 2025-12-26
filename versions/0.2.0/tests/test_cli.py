# tests/test_cli.py
from __future__ import annotations

from pathlib import Path
import subprocess


def _mms_path() -> Path:
    # Test-Datei liegt unter 0.1.3/tests/
    # -> Projekt-Root ist ein Verzeichnis höher
    root = Path(__file__).resolve().parents[1]
    return root / "mms"


def test_mms_version_runs() -> None:
    mms = _mms_path()
    result = subprocess.run(
        [str(mms), "version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "MMS-Version:" in result.stdout


def test_mms_help_runs() -> None:
    mms = _mms_path()
    result = subprocess.run(
        [str(mms), "help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "domains.add" in result.stdout
    assert "problems.add" in result.stdout
    assert "knowledge.add" in result.stdout

