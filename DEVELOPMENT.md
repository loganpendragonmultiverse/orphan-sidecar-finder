# Development record

Version 1.0.0 implements the complete initial scope: local filename matching, reviewable two-direction reports, configurable extensions, and no file mutation. Content hashing, media probing, fuzzy cross-directory matching, and cleanup actions are intentionally excluded.


## Version 1.1.0

Same-directory primary files with the same case-insensitive stem now remain separate candidates. A sidecar matching multiple candidates appears in `ambiguous_matches`; no primary is chosen and it is not counted as an orphan. Candidate primaries remain in `primaries_without_sidecars` until a unique sidecar match exists. The additive `explanations` field and Markdown report show the normalized base, recognized suffixes removed, and all candidates for every sidecar. Recognized language and role suffixes are unchanged; unfamiliar suffixes remain unmatched. Matching stays directory-local and filename-only.
