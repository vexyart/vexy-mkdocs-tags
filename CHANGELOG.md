# Changelog

## [0.3.3]

### Fixed
- Plugin now imports at all. `plugin.py` used `Any`, `Optional`, `Dict`, `List`,
  `DefaultDict`, and `Tuple` in method signatures without importing them, so
  `import tags.plugin` raised `NameError` and every test errored at collection.
  Added `from __future__ import annotations` and proper `typing` imports.
- Default template now matches the documented output. Releases ≤0.3.2 shipped an
  "Index of Topics" template that diverged from the README and from the test
  expectations; the default is now the documented `# Contents grouped by tag`
  format, and the tests assert against it.
- `generate_tags_file` sorted `self.metadata` (unfiltered) instead of the
  `valid_metadata` it had just computed, and relied on a site-specific `year`
  key for ordering. Grouping is now straightforward: pages sort by title,
  tags sort case-insensitively — deterministic across builds.
- YAML parsing switched from `yaml.FullLoader` to `yaml.safe_load`.

### Changed
- Moved to `src/` layout (`src/tags/`); version file is `src/tags/_version.py`.
- `requires-python` lowered from `>=3.12` to `>=3.10` (broader support).
- Dropped the undocumented `topic-tags` / `topic-auto` front-matter keys and the
  unused `on_nav` hook. The plugin scans the documented `tags` key only.

### Added
- Type hints and explanatory comments across `plugin.py`.
- Test suite rebuilt: 15 unit/edge tests plus a real `mkdocs build` integration
  test on a fixture site. Coverage ~93%.
- `.github/workflows/ci.yml` — test matrix (Python 3.10–3.13 on Linux + Windows),
  MkDocs 1.5/1.6 compat lane, ruff + ruff-format + mypy lint lane, codecov upload.
- `.github/workflows/release.yml` — build, PyPI trusted publishing, GitHub release.
- `.github/dependabot.yml` — weekly pip + github-actions updates.
- `mypy` (strict-ish) and `coverage` config in `pyproject.toml`.
- Jekyll + Just the Docs documentation under `docs/`.
- `CLAUDE.md` / `AGENTS.md` agent notes.

## [0.3.0]

### Changed
- Renamed PyPI distribution to `vexy-mkdocs-tags` (was `tags-macros-plugin`).
- Migrated build to `hatchling` + `hatch-vcs` with VCS-derived version.
- `requires-python` bumped to `>=3.12`.
- `tags/__init__.py` now exposes `__version__`.

### Removed
- Obsolete `setup.py` (buggy: `Path` used without import, hardcoded version).
- Excess `[tool.hatch.envs.*]` / `[tool.hatch.scripts]` cruft from `pyproject.toml`.

### Added
- `build.sh` / `publish.sh` convention scripts.
