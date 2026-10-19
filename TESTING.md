# Testing

## Feature-wave regression gate

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build` after installing `.[dev]` in an isolated environment. The focused regressions are in `tests/test_feature_wave.py`; run them together with the existing suite. Keep the configured coverage threshold. Repository CI supplies the supported OS/Python matrix.

## 1.1.2 acceptance

Match dotted, hyphenated and spaced primary names consistently with their sidecars.

- Normalize separators and case on both sides without removing role tokens from primary titles. Consider both the complete sidecar stem and recognized-suffix-stripped stem; multiple candidates stay ambiguous.
- Refuse overlapping or empty extension sets, preserve existing/racing report destinations, and render filenames literally in Markdown.

Tests prove scanning uses names and file metadata without opening discovered file content. Exercise normal and ambiguous matches, malformed configuration, pre-existing/duplicate/dangling/racing output paths, real closed stdout, and Markdown containing backticks or line breaks. Preserve input bytes and the existing coverage floor. Run formatting, lint, strict typing for source and tests, the full suite and wheel/source builds. Reinstall the built distributions in isolation for CLI acceptance before release.

Paired output preflight avoids known collisions; exclusive creation protects later collisions. A later failure may leave a new partial report; no rollback deletion or power-loss transaction is promised.
