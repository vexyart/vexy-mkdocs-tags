# this_file: tests/test_integration.py
# SPDX-License-Identifier: MIT
"""End-to-end test: run a real `mkdocs build` against a tiny fixture site."""

from __future__ import annotations

from pathlib import Path

import pytest

mkdocs_build = pytest.importorskip("mkdocs.commands.build")
mkdocs_config = pytest.importorskip("mkdocs.config")


def _write_site(root: Path) -> Path:
    """Create a minimal MkDocs site that enables the tags plugin."""
    docs = root / "docs"
    docs.mkdir()
    (docs / "index.md").write_text(
        "---\ntitle: Home\ntags:\n  - intro\n  - python\n---\n# Home\n",
        encoding="utf-8",
    )
    (docs / "about.md").write_text(
        "---\ntitle: About\ntags:\n  - python\n---\n# About\n",
        encoding="utf-8",
    )
    (root / "mkdocs.yml").write_text(
        "site_name: Fixture\nuse_directory_urls: false\nplugins:\n  - tags\n",
        encoding="utf-8",
    )
    return root / "mkdocs.yml"


def test_mkdocs_build_generates_tags_page(tmp_path: Path):
    config_file = _write_site(tmp_path)
    site_dir = tmp_path / "site"

    cfg = mkdocs_config.load_config(config_file=str(config_file), site_dir=str(site_dir))
    # The plugin must have registered under its entry-point name.
    assert "tags" in cfg["plugins"]

    mkdocs_build.build(cfg)

    tags_html = site_dir / "tags.html"
    assert tags_html.exists(), "plugin did not add a tags page to the build"
    body = tags_html.read_text(encoding="utf-8")
    assert "intro" in body
    assert "python" in body
    # Both pages carry the `python` tag, so both titles must be listed.
    assert "Home" in body
    assert "About" in body


def test_mkdocs_build_writes_aux_source(tmp_path: Path):
    config_file = _write_site(tmp_path)
    cfg = mkdocs_config.load_config(config_file=str(config_file), site_dir=str(tmp_path / "site"))
    mkdocs_build.build(cfg)
    # Default tags_folder is `aux`, resolved beside docs_dir.
    aux = tmp_path / "aux" / "tags.md"
    assert aux.exists()
    assert "Contents grouped by tag" in aux.read_text(encoding="utf-8")
