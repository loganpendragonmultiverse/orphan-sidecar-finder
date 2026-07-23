"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from orphan_sidecar_finder.core import PRIMARY_EXTENSIONS, SIDECAR_EXTENSIONS, ScanReport, scan


def markdown(report: ScanReport) -> str:
    """Render a compact Markdown report."""
    lines = [
        "# Orphan sidecar report",
        "",
        f"- Primary files: {report.primary_count}",
        f"- Sidecar files: {report.sidecar_count}",
        f"- Matched sidecars: {len(report.matches)}",
        f"- Orphan sidecars: {len(report.orphan_sidecars)}",
        f"- Primaries without sidecars: {len(report.primaries_without_sidecars)}",
        "",
        "## Orphan sidecars",
        "",
    ]
    lines.extend(f"- `{path}`" for path in report.orphan_sidecars)
    lines.extend(["", "## Primaries without sidecars", ""])
    lines.extend(f"- `{path}`" for path in report.primaries_without_sidecars)
    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    result = argparse.ArgumentParser(
        description="Find unmatched sidecar and primary files locally."
    )
    result.add_argument("root", type=Path)
    result.add_argument("--no-recursive", action="store_true")
    result.add_argument("--primary-ext", action="append", default=[])
    result.add_argument("--sidecar-ext", action="append", default=[])
    result.add_argument("--json", type=Path, dest="json_output")
    result.add_argument("--markdown", type=Path, dest="markdown_output")
    return result


def main(argv: list[str] | None = None) -> int:
    """Run the command."""
    args = parser().parse_args(argv)
    primary = set(args.primary_ext) or set(PRIMARY_EXTENSIONS)
    sidecars = set(args.sidecar_ext) or set(SIDECAR_EXTENSIONS)
    try:
        report = scan(
            args.root,
            recursive=not args.no_recursive,
            primary_extensions=primary,
            sidecar_extensions=sidecars,
        )
    except (OSError, ValueError) as error:
        parser().error(str(error))
    rendered = markdown(report)
    if args.json_output:
        args.json_output.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if report.orphan_sidecars else 0
