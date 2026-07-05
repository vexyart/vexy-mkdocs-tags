# this_file: tests/test_plugin.py
# SPDX-License-Identifier: MIT
"""Unit and edge-case tests for the tags plugin's parsing and rendering."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pytest

from tags.plugin import TagsPlugin, get_metadata

# --- get_metadata -----------------------------------------------------------


def test_get_metadata_valid_yaml_header(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "page.md").write_text(
        "---\ntitle: Test Page\ntags:\n  - tag1\n  - tag2\n---\n# Content\n",
        encoding="utf-8",
    )
    meta = get_metadata("page.md", str(docs_dir))
    assert meta is not None
    assert meta["title"] == "Test Page"
    assert meta["tags"] == ["tag1", "tag2"]
    assert meta["filename"] == "page.md"


def test_get_metadata_no_yaml_header(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "plain.md").write_text("# No front matter", encoding="utf-8")
    assert get_metadata("plain.md", str(docs_dir)) is None


def test_get_metadata_non_mapping_header_returns_none(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "list.md").write_text("---\n- item1\n- item2\n---\n# C\n", encoding="utf-8")
    assert get_metadata("list.md", str(docs_dir)) is None


def test_get_metadata_empty_file(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "empty.md").touch()
    assert get_metadata("empty.md", str(docs_dir)) is None


def test_get_metadata_invalid_yaml_returns_none(tmp_path: Path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "bad.md").write_text("---\ntitle: : :\n  - broken\n---\n", encoding="utf-8")
    assert get_metadata("bad.md", str(docs_dir)) is None


def test_get_metadata_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        get_metadata("nope.md", str(tmp_path))


# --- TagsPlugin -------------------------------------------------------------


def test_plugin_defaults():
    plugin = TagsPlugin()
    assert plugin.tags_filename == Path("tags.md")
    assert plugin.tags_folder == Path("aux")
    assert plugin.tags_template is None


def test_on_config_custom_relative_folder(tmp_path: Path):
    plugin = TagsPlugin()
    plugin.config = {"tags_filename": "all-tags.md", "tags_folder": "generated/tags"}
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    plugin.on_config({"docs_dir": str(docs_dir)})
    assert plugin.tags_filename == Path("all-tags.md")
    expected = docs_dir / ".." / "generated/tags"
    assert plugin.tags_folder == expected
    assert expected.exists()


def test_on_config_absolute_folder(tmp_path: Path):
    plugin = TagsPlugin()
    absolute = tmp_path / "abs_tags"
    plugin.config = {"tags_folder": str(absolute)}
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    plugin.on_config({"docs_dir": str(docs_dir)})
    assert plugin.tags_folder == absolute
    assert absolute.exists()


def test_generate_tags_page_empty():
    output = TagsPlugin().generate_tags_page(defaultdict(list))
    assert "# Contents grouped by tag" in output
    assert '<span class="tag">' not in output


def test_generate_tags_page_with_data():
    plugin = TagsPlugin()
    p1 = {"title": "Page One", "filename": "page1.md"}
    p2 = {"title": "Page Two", "filename": "page2.md"}
    data = {"cat": [p1, p2], "dog": [p1], "fish": [p2]}
    output = plugin.generate_tags_page(data)
    assert '## <span class="tag">cat</span>' in output
    assert '## <span class="tag">dog</span>' in output
    assert '## <span class="tag">fish</span>' in output
    assert "[Page One](page1.md)" in output
    assert "[Page Two](page2.md)" in output


def test_generate_tags_page_sorts_case_insensitively():
    plugin = TagsPlugin()
    page = {"title": "P", "filename": "p.md"}
    data = {"Zebra": [page], "apple": [page]}
    output = plugin.generate_tags_page(data)
    assert output.index("apple") < output.index("Zebra")


def test_generate_tags_file_writes_output(tmp_path: Path):
    plugin = TagsPlugin()
    plugin.tags_folder = tmp_path / "out"
    plugin.tags_folder.mkdir()
    plugin.tags_filename = Path("final.md")
    plugin.metadata = [{"title": "Test", "filename": "test.md", "tags": ["sample"]}]
    plugin.generate_tags_file()
    written = (plugin.tags_folder / plugin.tags_filename).read_text(encoding="utf-8")
    assert '## <span class="tag">sample</span>' in written
    assert "[Test](test.md)" in written


def test_generate_tags_file_tolerates_bare_string_tag(tmp_path: Path):
    plugin = TagsPlugin()
    plugin.tags_folder = tmp_path / "out"
    plugin.tags_folder.mkdir()
    plugin.metadata = [{"title": "Solo", "filename": "solo.md", "tags": "single"}]
    plugin.generate_tags_file()
    written = (plugin.tags_folder / "tags.md").read_text(encoding="utf-8")
    assert '<span class="tag">single</span>' in written


def test_untitled_default_applied(tmp_path: Path):
    plugin = TagsPlugin()
    plugin.tags_folder = tmp_path / "out"
    plugin.tags_folder.mkdir()
    plugin.metadata = [{"filename": "x.md", "tags": ["t"]}]
    plugin.generate_tags_file()
    written = (plugin.tags_folder / "tags.md").read_text(encoding="utf-8")
    assert "[Untitled](x.md)" in written
