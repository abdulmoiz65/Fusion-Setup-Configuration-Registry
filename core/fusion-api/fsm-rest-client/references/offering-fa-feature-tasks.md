# Offering, Functional Area, and Feature Relationships

Use this reference to retrieve an offering's functional areas and feature
hierarchy. The CSV contains only `OFFERING`, `FA`, and `FEATURE` columns.

```bash
python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature-tasks.py \
  --offering-short-name DOO_ORCHESTRATION
```

Omit `--offering-short-name` to retrieve every available offering. Use
`--offering-offset` and `--offering-limit` to run resumable batches.

The collector calls the read-only BOSS `availableOfferings`,
`availableSetupFunctionalAreasByOffering`, and `availableFeaturesByOffering`
endpoints, then writes the relationship rows to the project CSV.

Pass `--verbose` for updates after offering enumeration and each offering's
functional-area/feature hierarchy retrieval.
