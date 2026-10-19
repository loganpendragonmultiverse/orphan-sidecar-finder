from pathlib import Path
from typing import Any

import pytest

from orphan_sidecar_finder.cli import markdown
from orphan_sidecar_finder.core import scan


@pytest.mark.parametrize("stem", ["My.Movie", "My Movie", "My-Movie", "My_Movie"])
def test_shared_separator_conventions(tmp_path: Path, stem: str) -> None:
    (tmp_path / (stem + ".mkv")).touch()
    (tmp_path / "My.Movie.en.srt").touch()
    assert len(scan(tmp_path).matches) == 1


def test_normalized_collision_stays_ambiguous(tmp_path: Path) -> None:
    for name in ["My.Movie.mkv", "My-Movie.mp4", "My Movie.en.srt"]:
        (tmp_path / name).touch()
    report = scan(tmp_path)
    assert len(report.ambiguous_matches) == 1
    assert not report.orphan_sidecars
    assert len(report.primaries_without_sidecars) == 2


def test_scan_does_not_open_content(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ["Movie.mkv", "Movie.srt"]:
        (tmp_path / name).touch()

    def forbidden(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("scanner opened file contents")

    monkeypatch.setattr(Path, "open", forbidden)
    assert len(scan(tmp_path).matches) == 1


@pytest.mark.parametrize("extension", ["", ".", "bad/ext", "bad ext"])
def test_bad_extensions(tmp_path: Path, extension: str) -> None:
    with pytest.raises(ValueError, match="extensions"):
        scan(tmp_path, primary_extensions={extension})


def test_overlapping_extensions(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="overlap"):
        scan(tmp_path, primary_extensions={"srt"})


def test_literal_markdown(tmp_path: Path) -> None:
    (tmp_path / "A`B.srt").touch()
    text = markdown(scan(tmp_path))
    assert "``A`B.srt``" in text
    assert "base ``a`b``" in text


def test_primary_role_words_are_not_removed(tmp_path: Path) -> None:
    for name in ["Film.en.mp4", "Film.en.srt"]:
        (tmp_path / name).touch()
    report = scan(tmp_path)
    assert report.matches[0].primary == "Film.en.mp4"
    assert not report.orphan_sidecars
    (tmp_path / "Film.mkv").touch()
    report = scan(tmp_path)
    assert len(report.ambiguous_matches) == 1
    assert set(report.ambiguous_matches[0].candidates) == {"Film.en.mp4", "Film.mkv"}
    assert not report.matches
