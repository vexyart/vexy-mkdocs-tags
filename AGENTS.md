# this_file: AGENTS.md
See [CLAUDE.md](CLAUDE.md) for full agent notes. Summary:

- MkDocs plugin; source in `src/tags/`, tests in `tests/`.
- Verify with `pytest`, `ruff check src tests`, `ruff format --check src tests`, `mypy src`.
- Versioning via hatch-vcs from git tags; release with `uvx gitnextver@latest .`.
- Public plugin name is `tags`; keep the package named `tags`.
