---
title: Home
layout: default
nav_order: 1
---

# vexy-mkdocs-tags

Add `tags: [python, cli]` to a page's front matter. A tags page appears, grouping every page under each tag.

## Install

```shell
pip install vexy-mkdocs-tags
```

## Enable

In `mkdocs.yml`:

```yaml
plugins:
  - search
  - tags
```

## Tag a page

```markdown
---
title: Getting started
tags:
  - intro
  - python
---
```

## The generated page

On every build the plugin scans each Markdown source, reads the `tags` list from its YAML header, and writes one Markdown file — `aux/tags.md` by default — that MkDocs renders like any other page. It looks like this:

```markdown
# Contents grouped by tag

## <span class="tag">intro</span>
  * [Getting started](getting-started.md)

## <span class="tag">python</span>
  * [Getting started](getting-started.md)
```

Tags sort case-insensitively; pages under each tag sort by title. Style `h2.tag` with CSS to taste.

## Options

| Option | Default | What it does |
|---|---|---|
| `tags_filename` | `tags.md` | Name of the generated file. |
| `tags_folder` | `aux` | Where the file is written. Relative paths resolve beside `docs/`, so writing it does not retrigger `mkdocs serve`. Absolute paths work too; missing folders are created. |
| `tags_template` | *(built-in)* | Path to your own Markdown + Jinja2 template. `None` uses the packaged one. |

Example with all options:

```yaml
plugins:
  - search
  - tags:
      tags_folder: /tmp/mysite/aux
      tags_template: docs/theme/tags.md.template
```

## Custom template

The template receives `tags` — a list of `(tag, pages)` pairs. Each `page` carries its front matter plus a `.filename` attribute (the source path relative to `docs/`). A `slugify` Jinja2 filter is available for building anchors.

## Versus Material's built-in tags

MkDocs Material ships its own tags plugin. It renders inline tag chips on each page and needs the Material theme. This plugin is theme-agnostic and produces a single plain-Markdown index — useful when you are not on Material, or you want one grep-friendly list of every tag.
