# Setup Catalog Hierarchy Browser

Static browser for the generated setup catalog hierarchy:

- `effective/pillars-offerings-mapping.json`
- `effective/offering-functional-area-task-catalog.json`

The effective layer is composed as `release - pre_release.removals +
pre_release.items + custom.items`; the browser must never read a release
catalog directly.

Open directly without a server:

```text
knowledge/setup-task-catalog/hierarchy-browser/index.html
```

The browser loads `catalog-data.js`, a generated static data bundle refreshed by
`core/fusion-dev/catalog-management/scripts/build_effective_catalog.py` from the two effective catalog JSON files.

To use live JSON loading instead, run from the repository root:

```bash
python3 -m http.server 8099
```

Open:

```text
http://localhost:8099/knowledge/setup-task-catalog/hierarchy-browser/
```
