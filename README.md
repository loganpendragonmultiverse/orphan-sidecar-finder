# Orphan Sidecar Finder

Orphan Sidecar Finder is a read-only local CLI that matches subtitles, metadata, and other sidecar files to primary media or document files. It reports sidecars with no primary and primary files with no sidecar without opening, renaming, moving, or deleting anything.

## Three-minute use

```sh
python -m pip install "orphan-sidecar-finder @ https://github.com/loganpendragonmultiverse/orphan-sidecar-finder/releases/download/v1.0.0/orphan_sidecar_finder-1.0.0-py3-none-any.whl"
orphan-sidecar-finder "D:\Media" --markdown sidecars.md --json sidecars.json
```

Recognized sidecar suffixes include common language and role markers such as `.en`, `.forced`, and `.sdh`. Matching is deliberately directory-local and conservative. Custom primary and sidecar extensions can be supplied repeatedly with `--primary-ext` and `--sidecar-ext`.

## Privacy and limitations

Everything stays local. Reports contain filenames, so review them before sharing. The tool does not inspect file contents, infer renamed editions, match across directories, or decide whether every primary should have a sidecar. A reported result is a review lead, not deletion advice.

## Development

```sh
python -m pip install -e ".[dev]"
ruff format --check . && ruff check .
mypy src tests
pytest
python -m build
```

Version 1.0.0 is feature complete for conservative filename matching. Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md), security reports follow [SECURITY.md](SECURITY.md), and the project uses the MIT License.
