"""Read-only sidecar matching."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

PRIMARY_EXTENSIONS = frozenset(
    {
        ".avi",
        ".cb7",
        ".cbr",
        ".cbz",
        ".epub",
        ".flac",
        ".jpeg",
        ".jpg",
        ".m4a",
        ".mkv",
        ".mov",
        ".mp3",
        ".mp4",
        ".pdf",
        ".png",
        ".wav",
        ".webm",
    }
)
SIDECAR_EXTENSIONS = frozenset(
    {".ass", ".idx", ".json", ".nfo", ".srt", ".ssa", ".sub", ".vtt", ".xml"}
)
SUFFIX_TOKENS = frozenset(
    {"cc", "commentary", "descriptive", "en", "eng", "english", "forced", "hi", "sdh", "signs"}
)


@dataclass(frozen=True)
class Match:
    """A sidecar and the primary file it matched."""

    sidecar: str
    primary: str


@dataclass(frozen=True)
class ScanReport:
    """Complete deterministic scan result."""

    root: str
    primary_count: int
    sidecar_count: int
    matches: tuple[Match, ...]
    orphan_sidecars: tuple[str, ...]
    primaries_without_sidecars: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready representation."""
        return asdict(self)


def normalize_extensions(values: set[str] | frozenset[str]) -> frozenset[str]:
    """Normalize extension values to lowercase dotted forms."""
    return frozenset(
        value.casefold() if value.startswith(".") else f".{value.casefold()}" for value in values
    )


def sidecar_base(stem: str) -> str:
    """Remove recognized language and role suffixes from a sidecar stem."""
    parts = re.split(r"[._-]+", stem)
    while len(parts) > 1 and parts[-1].casefold() in SUFFIX_TOKENS:
        parts.pop()
    return " ".join(parts).casefold()


def scan(
    root: Path,
    *,
    recursive: bool = True,
    primary_extensions: set[str] | frozenset[str] = PRIMARY_EXTENSIONS,
    sidecar_extensions: set[str] | frozenset[str] = SIDECAR_EXTENSIONS,
) -> ScanReport:
    """Scan root without opening or modifying any discovered file."""
    resolved = root.resolve()
    if not resolved.is_dir():
        raise NotADirectoryError(str(root))
    primary_exts = normalize_extensions(primary_extensions)
    sidecar_exts = normalize_extensions(sidecar_extensions)
    paths = sorted(
        (resolved.rglob("*") if recursive else resolved.glob("*")),
        key=lambda item: str(item).casefold(),
    )
    files = [path for path in paths if path.is_file()]
    primaries = [path for path in files if path.suffix.casefold() in primary_exts]
    sidecars = [path for path in files if path.suffix.casefold() in sidecar_exts]
    primary_index = {(path.parent, path.stem.casefold()): path for path in primaries}
    matches: list[Match] = []
    orphans: list[str] = []
    matched_primaries: set[Path] = set()
    for sidecar in sidecars:
        primary = primary_index.get((sidecar.parent, sidecar_base(sidecar.stem)))
        relative_sidecar = sidecar.relative_to(resolved).as_posix()
        if primary is None:
            orphans.append(relative_sidecar)
            continue
        matched_primaries.add(primary)
        matches.append(Match(relative_sidecar, primary.relative_to(resolved).as_posix()))
    unmatched = tuple(
        path.relative_to(resolved).as_posix() for path in primaries if path not in matched_primaries
    )
    return ScanReport(
        root=str(resolved),
        primary_count=len(primaries),
        sidecar_count=len(sidecars),
        matches=tuple(matches),
        orphan_sidecars=tuple(orphans),
        primaries_without_sidecars=unmatched,
    )
