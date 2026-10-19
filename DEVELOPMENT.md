# Development record

Version 1.0.0 implements the complete initial scope: local filename matching, reviewable two-direction reports, configurable extensions, and no file mutation. Content hashing, media probing, fuzzy cross-directory matching, and cleanup actions are intentionally excluded.


## Version 1.1.0

Same-directory primary files with the same case-insensitive stem now remain separate candidates. A sidecar matching multiple candidates appears in `ambiguous_matches`; no primary is chosen and it is not counted as an orphan. Candidate primaries remain in `primaries_without_sidecars` until a unique sidecar match exists. The additive `explanations` field and Markdown report show the normalized base, recognized suffixes removed, and all candidates for every sidecar. Recognized language and role suffixes are unchanged; unfamiliar suffixes remain unmatched. Matching stays directory-local and filename-only.

## 1.1.2 acceptance

Match dotted, hyphenated and spaced primary names consistently with their sidecars.

- Normalize separators and case on both sides without removing role tokens from primary titles. Consider both the complete sidecar stem and recognized-suffix-stripped stem; multiple candidates stay ambiguous.
- Refuse overlapping or empty extension sets, preserve existing/racing report destinations, and render filenames literally in Markdown.

Tests prove scanning uses names and file metadata without opening discovered file content. Exercise normal and ambiguous matches, malformed configuration, pre-existing/duplicate/dangling/racing output paths, real closed stdout, and Markdown containing backticks or line breaks. Preserve input bytes and the existing coverage floor. Run formatting, lint, strict typing for source and tests, the full suite and wheel/source builds. Reinstall the built distributions in isolation for CLI acceptance before release.

Paired output preflight avoids known collisions; exclusive creation protects later collisions. A later failure may leave a new partial report; no rollback deletion or power-loss transaction is promised.

The wheel includes the handoff documents under `share/orphan-sidecar-finder` in the installation prefix; the source archive keeps them at its top level.
