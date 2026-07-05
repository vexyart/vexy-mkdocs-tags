# TODO

Future ideas beyond the v1.0 modernization pass (larger than low-hanging fruit):

- [ ] Optional per-page tag chips: rewrite each page to surface its tags visibly,
      not just in the generated index (long-requested; needs an `on_page_markdown`
      hook and a documented opt-in).
- [ ] Support front matter that is not triple-dash delimited (e.g. `+++` TOML).
- [ ] Fall back to the page's first `# H1` when `title:` is absent, instead of
      labelling it "Untitled".
- [ ] Emit a machine-readable `tags.json` alongside `tags.md` for search indexes.
- [ ] Optional per-tag pages (one file per tag) for large sites.
