"""Behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from orphan_sidecar_finder.cli import main, markdown
from orphan_sidecar_finder.core import sidecar_base, scan


def touch(path: Path) -> None:
    """Create a fixture file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"fixture")


def test_suffix_normalization() -> None:
    assert sidecar_base("Film.en.forced") == "film"
    assert sidecar_base("Film-directors-cut") == "film directors cut"


def test_scan_matches_and_reports_both_directions(tmp_path: Path) -> None:
    touch(tmp_path / "Film.mkv")
    touch(tmp_path / "Film.en.srt")
    touch(tmp_path / "Loose.vtt")
    touch(tmp_path / "Silent.mp4")
    report = scan(tmp_path)
    assert report.primary_count == 2
    assert report.sidecar_count == 2
    assert report.matches[0].primary == "Film.mkv"
    assert report.orphan_sidecars == ("Loose.vtt",)
    assert report.primaries_without_sidecars == ("Silent.mp4",)


def test_scan_keeps_directories_separate(tmp_path: Path) -> None:
    touch(tmp_path / "a" / "Film.mkv")
    touch(tmp_path / "b" / "Film.srt")
    assert scan(tmp_path).orphan_sidecars == ("b/Film.srt",)


def test_nonrecursive_scan(tmp_path: Path) -> None:
    touch(tmp_path / "nested" / "Film.srt")
    assert scan(tmp_path, recursive=False).sidecar_count == 0


def test_custom_extensions(tmp_path: Path) -> None:
    touch(tmp_path / "Thing.raw")
    touch(tmp_path / "Thing.note")
    report = scan(tmp_path, primary_extensions={"raw"}, sidecar_extensions={".note"})
    assert len(report.matches) == 1


def test_missing_directory_fails(tmp_path: Path) -> None:
    with pytest.raises(NotADirectoryError):
        scan(tmp_path / "missing")


def test_markdown_and_json_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    touch(tmp_path / "Loose.srt")
    output = tmp_path / "report.json"
    assert main([str(tmp_path), "--json", str(output)]) == 1
    assert json.loads(output.read_text(encoding="utf-8"))["orphan_sidecars"] == ["Loose.srt"]
    assert "Orphan sidecars: 1" in capsys.readouterr().out
    assert "`Loose.srt`" in markdown(scan(tmp_path))


def test_clean_cli_exit(tmp_path: Path) -> None:
    touch(tmp_path / "Film.mkv")
    touch(tmp_path / "Film.srt")
    assert main([str(tmp_path)]) == 0
