# Changelog

## [0.3.0]

### Changed
- Renamed PyPI distribution to `vexy-mkdocs-tags` (was `tags-macros-plugin`).
- Migrated build to `hatchling` + `hatch-vcs` with VCS-derived version (`tags/__version__.py`, gitignored).
- `requires-python` bumped to `>=3.12`.
- `tags/__init__.py` now exposes `__version__`.

### Removed
- Obsolete `setup.py` (buggy: `Path` used without import, hardcoded version).
- Excess `[tool.hatch.envs.*]` / `[tool.hatch.scripts]` cruft from `pyproject.toml`.

### Added
- `build.sh` / `publish.sh` convention scripts.
