# tests/test_problem_pipeline.py
from __future__ import annotations

from pathlib import Path

from engine import add_problems
from engine.utils import layout
from engine.utils import utils_jsonl


def test_problems_add_with_valid_file(monkeypatch, tmp_path, capsys) -> None:
    # Ersetze das PROBLEMS_DIR temporär durch ein tmp-Verzeichnis
    problems_dir = tmp_path / "problems"
    problems_dir.mkdir()

    test_file = problems_dir / "testdomain.jsonl"
    utils_jsonl.write_jsonl(
        test_file,
        [
            {"id": "p1", "name": "Problem 1"},
            {"id": "p2", "name": "Problem 2"},
        ],
    )

    monkeypatch.setattr(layout, "PROBLEMS_DIR", problems_dir)

    # Rufe die Pipeline ohne Argumente auf (soll alle Dateien prüfen)
    rc = add_problems.main([])
    assert rc == 0

    out = capsys.readouterr().out
    assert "Einträge: 2" in out

