# this_file: src/tags/plugin.py
# --------------------------------------------
# MkDocs "tags" plugin.
#
# Scans the YAML front matter of every Markdown page for a `tags:` key and
# builds a single auto-generated page that lists each tag and the pages that
# declare it.
#
# JL Diaz (c) 2019, MIT License
# Modernized for the vexy-mkdocs-tags distribution.
# --------------------------------------------
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

import jinja2
import yaml
from jinja2.ext import Extension
from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

try:
    from pymdownx.slugs import uslugify_cased_encoded as slugify
except ImportError:
    from markdown.extensions.toc import slugify


# A single page's parsed front matter plus the injected `filename` key.
PageMeta = dict[str, Any]


def slugify_this(text: str) -> str:
    """Slugify `text` with a hyphen separator, matching MkDocs anchor slugs."""
    return slugify(text, "-")


class SlugifyExtension(Extension):
    """Expose `slugify` as a Jinja2 filter so custom templates can build anchors."""

    def __init__(self, environment: jinja2.Environment) -> None:
        super().__init__(environment)
        environment.filters["slugify"] = slugify_this


class TagsPlugin(BasePlugin):
    """Generate a tags index page from the `tags:` key in each page's front matter.

    On every build the plugin scans all Markdown sources, collects the `tags`
    list from each page's YAML header, and writes a single Markdown file
    (``aux/tags.md`` by default) that groups pages by tag. The file lives
    outside ``docs_dir`` so writing it does not retrigger ``mkdocs serve``, but
    it is appended to the build so MkDocs renders it like any other page.
    """

    config_scheme = (
        ("tags_filename", Type(str, default="tags.md")),
        ("tags_folder", Type(str, default="aux")),
        ("tags_template", Type(str)),
    )

    def __init__(self) -> None:
        self.metadata: list[PageMeta] = []
        self.tags_filename: Path = Path("tags.md")
        self.tags_folder: Path = Path("aux")
        self.tags_template: Path | None = None

    def on_config(self, config: Any) -> Any:
        """Resolve the output location and make sure the tags folder exists."""
        self.tags_filename = Path(self.config.get("tags_filename") or self.tags_filename)
        self.tags_folder = Path(self.config.get("tags_folder") or self.tags_folder)
        # A relative folder is resolved against the parent of docs_dir so the
        # generated file sits beside the docs tree, not inside it.
        if not self.tags_folder.is_absolute():
            self.tags_folder = Path(config["docs_dir"]) / ".." / self.tags_folder
        self.tags_folder.mkdir(parents=True, exist_ok=True)

        tags_template_config = self.config.get("tags_template")
        if tags_template_config:
            self.tags_template = Path(tags_template_config)
        return config

    def on_files(self, files: Any, config: Any) -> Any:
        """Collect tags from every Markdown source and inject the tags page."""
        for f in files:
            if not f.src_path.endswith(".md"):
                continue
            meta = get_metadata(f.src_path, config["docs_dir"])
            if meta:
                self.metadata.append(meta)

        self.generate_tags_file()

        new_file = File(
            path=str(self.tags_filename),
            src_dir=str(self.tags_folder),
            dest_dir=config["site_dir"],
            use_directory_urls=False,
        )
        files.append(new_file)
        return files

    def generate_tags_page(self, data: dict[str, list[PageMeta]]) -> str:
        """Render the tags page from `data`, a mapping of tag -> pages.

        Tags are sorted case-insensitively; each tag's pages are sorted by
        title so the output is deterministic across builds.
        """
        if self.tags_template is None:
            templ_path = Path(__file__).parent / "templates"
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(templ_path)),
                extensions=[SlugifyExtension],
            )
            templ = environment.get_template("tags.md.template")
        else:
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(searchpath=str(self.tags_template.parent)),
                extensions=[SlugifyExtension],
            )
            templ = environment.get_template(str(self.tags_template.name))

        sorted_tags = [
            (tag, sorted(pages, key=lambda p: str(p.get("title", "")).lower()))
            for tag, pages in sorted(data.items(), key=lambda t: t[0].lower())
        ]
        return templ.render(tags=sorted_tags)

    def generate_tags_file(self) -> None:
        """Group collected pages by tag and write the rendered tags file."""
        tag_dict: dict[str, list[PageMeta]] = defaultdict(list)
        for meta in self.metadata:
            meta.setdefault("title", "Untitled")
            tags = meta.get("tags", [])
            # `tags` is normally a YAML list, but tolerate a bare string.
            if isinstance(tags, str):
                tags = [tags]
            if isinstance(tags, list):
                for tag in tags:
                    if isinstance(tag, str):
                        tag_dict[tag].append(meta)

        rendered = self.generate_tags_page(tag_dict)
        with (self.tags_folder / self.tags_filename).open("w", encoding="utf-8") as f:
            f.write(rendered)


def get_metadata(name: str, path: str) -> PageMeta | None:
    """Parse the triple-dash YAML header of a Markdown file.

    Returns the front matter as a dict with an added `filename` key (the source
    path relative to ``docs_dir``), or ``None`` when the file has no header, an
    empty header, or a header that does not parse to a mapping.
    """

    def extract_yaml(f: Any) -> str:
        # Collect the lines between the first and second `---` fences.
        result: list[str] = []
        fences = 0
        for line in f:
            if line.strip() == "---":
                fences += 1
                continue
            if fences == 2:
                break
            if fences == 1:
                result.append(line)
        return "".join(result)

    filename = Path(path) / Path(name)
    with filename.open(encoding="utf-8") as f:
        metadata_str = extract_yaml(f)
        if not metadata_str:
            return None
        try:
            meta = yaml.safe_load(metadata_str)
        except yaml.YAMLError:
            return None
        if not isinstance(meta, dict):
            return None
        meta["filename"] = name
        return meta
