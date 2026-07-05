# this_file: src/tags/__init__.py
"""vexy-mkdocs-tags: MkDocs plugin that processes tags in YAML front matter."""

try:
    from tags._version import __version__
except ImportError:  # editable install before hatch-vcs has written the file
    __version__ = "0.0.0+local"

__all__ = ["__version__"]
