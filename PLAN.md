# PLAN

## v1.0.0 modernization — DONE

Completed in the current pass (see CHANGELOG "Unreleased"):

- [x] Fix the import-breaking missing type imports in `plugin.py`.
- [x] Align the default template with the documented output; fix the tests.
- [x] `src/` layout, hatch-vcs version file, ruff + mypy + coverage config.
- [x] Real `mkdocs build` integration test on a fixture site; ~93% coverage.
- [x] CI (test matrix + MkDocs compat + lint) and release workflows; dependabot.
- [x] Jekyll + Just the Docs docs; README trimmed with Quick Start first.
- [x] `CLAUDE.md` / `AGENTS.md`.

## Next

Tracked in [TODO.md](TODO.md): visible per-page tag chips, non-triple-dash front
matter, H1 title fallback, `tags.json` export, per-tag pages.
