# Changelog

## 1.1.2 - 2026-10-19

- Normalize separators and case on both sides without removing role tokens from primary titles. Consider both the complete sidecar stem and recognized-suffix-stripped stem; multiple candidates stay ambiguous.
- Refuse overlapping or empty extension sets, preserve existing/racing report destinations, and render filenames literally in Markdown.

## 1.1.1 - 2026-10-16

- Correct release wording and the original publication date; update installation references. Feature behavior is unchanged.

## 1.1.0 - 2026-10-15

- Retain ambiguous same-stem primary candidates and explain suffix matching.

## 1.0.0 - 2026-07-22

- Added recursive and single-directory read-only scans.
- Added conservative language and role suffix matching.
- Added Markdown and JSON reports plus custom extension sets.
