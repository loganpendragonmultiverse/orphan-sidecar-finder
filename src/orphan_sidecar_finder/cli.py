"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from orphan_sidecar_finder.core import PRIMARY_EXTENSIONS, SIDECAR_EXTENSIONS, ScanReport, scan

from .markdown import literal
from .output import validate_outputs, write_report, write_stdout


def markdown(report: ScanReport) -> str:
    """Render a compact Markdown report."""
    lines = [
        "# Orphan sidecar report",
        "",
        f"- Primary files: {report.primary_count}",
        f"- Sidecar files: {report.sidecar_count}",
        f"- Matched sidecars: {len(report.matches)}",
        f"- Ambiguous sidecars: {len(report.ambiguous_matches)}",
        f"- Orphan sidecars: {len(report.orphan_sidecars)}",
        f"- Primaries without sidecars: {len(report.primaries_without_sidecars)}",
        "",
        "## Orphan sidecars",
        "",
    ]
    lines.extend(f"- {literal(path)}" for path in report.orphan_sidecars)
    lines.extend(["", "## Primaries without sidecars", ""])
    lines.extend(f"- {literal(path)}" for path in report.primaries_without_sidecars)
    lines.extend(["", "## Ambiguous matches", ""])
    lines.extend(
        f"- {literal(item.sidecar)}: {', '.join(map(literal, item.candidates))}"
        for item in report.ambiguous_matches
    )
    lines.extend(["", "## Matching explanations", ""])
    for item in report.explanations:
        suffix = ", ".join(map(literal, item.removed_suffixes)) or "none"
        candidates = ", ".join(map(literal, item.candidates)) or "none"
        lines.append(
            f"- {literal(item.sidecar)}: base {literal(item.normalized_base)}; removed suffixes: {suffix}; candidates: {candidates}"
        )
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
        rendered = markdown(report)
        paths = [path for path in (args.json_output, args.markdown_output) if path]
        validate_outputs(paths)
        if args.json_output:
            write_report(
                args.json_output.expanduser(), json.dumps(report.to_dict(), indent=2) + "\n"
            )
        if args.markdown_output:
            write_report(args.markdown_output.expanduser(), rendered)
        write_stdout(rendered)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 1 if report.orphan_sidecars else 0
