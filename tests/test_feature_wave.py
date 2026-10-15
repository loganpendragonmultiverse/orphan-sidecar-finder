from pathlib import Path

from orphan_sidecar_finder.cli import markdown
from orphan_sidecar_finder.core import scan


def test_ambiguity_suffix_case_and_isolation(tmp_path: Path) -> None:
    names = (
        "Movie.mkv",
        "movie.MP4",
        "Movie.en.forced.srt",
        "Movie.eng.srt",
        "Missing.en.srt",
        "Movie.fr.srt",
    )
    for name in names:
        (tmp_path / name).touch()
    (tmp_path / "other").mkdir()
    (tmp_path / "other/Movie.en.srt").touch()
    report = scan(tmp_path)
    assert len(report.ambiguous_matches) == 2
    assert len(report.matches) == 0
    assert len(report.orphan_sidecars) == 3
    assert len(report.primaries_without_sidecars) == 2
    group = report.ambiguous_matches[0]
    assert set(group.candidates) == {"Movie.mkv", "movie.MP4"}
    assert report.explanations[0].normalized_base
    forced = next(e for e in report.explanations if "forced" in e.sidecar)
    assert forced.removed_suffixes == ("en", "forced")
    assert "Ambiguous matches" in markdown(report)
    assert "candidates" in markdown(report)
    assert report.to_dict()["ambiguous_matches"]


def test_single_match_and_unknown_language_explanation(tmp_path: Path) -> None:
    for name in ("Film.mp4", "FILM.EN.srt", "Film.fr.srt"):
        (tmp_path / name).touch()
    report = scan(tmp_path)
    assert report.matches[0].primary == "Film.mp4"
    assert report.orphan_sidecars == ("Film.fr.srt",)
    assert not report.ambiguous_matches
    assert not report.primaries_without_sidecars
