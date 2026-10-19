# Pre-release Catalog Layer

Use this layer to stage the next release without changing the authoritative
`release/` extracts. The effective catalog is:

```text
release - pre_release.removals + pre_release.items + custom.items
```

Each supplement supports a `removals` array keyed by its stable identity:

| Catalog | Removal key |
|---|---|
| `Offerings_catalog_supplement.json` | `FeatureCode` |
| `Functional_areas_catalog_supplement.json` | `FeatureCode` |
| `setupTasks_supplement.json` | `TaskCode` |

Removal entries must include the stable key; `FeatureName` or `TaskName`,
`effectiveRelease`, and `reason` are strongly recommended for reviewability.
For example, HCM Communicate is removed by the `ORA_IRC_HCM_COMMUNICATE`
offering tombstone in `Offerings_catalog_supplement.json`.

Do not add a disabled duplicate item to model a removal. A tombstone removes the
release item from every effective-catalog consumer, including the hierarchy
browser and pillar-skill generator.

## Hierarchy task associations

`offering-functional-area-task-catalog_supplement.json` can also contain a
`taskAssociations` array. Use it to place an existing release or pre-release
task in a specific existing offering and functional area without replacing the
whole offering hierarchy. Each association requires `TaskCode`, `TaskName`,
`Pillar`, `OfferingCode`, `OfferingName`, `FunctionalAreaCode`, and
`FunctionalAreaName`; the referenced names and codes must match the effective
catalog. An association can include an optional `DisplaySequence` as a positive
canonical integer to control the task's position in the functional area.
