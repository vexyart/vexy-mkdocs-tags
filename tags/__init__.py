# this_file: tags/__init__.py
"""vexy-mkdocs-tags: MkDocs plugin that processes tags in YAML front matter."""

try:
    from tags.__version__ import __version__
except ImportError:  # editable install before hatch-vcs has run
    __version__ = "0.0.0+local"

__all__ = ["__version__"]
