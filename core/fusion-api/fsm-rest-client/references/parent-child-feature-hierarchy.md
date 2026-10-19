---
name: parent-child-feature-hierarchy
description: Fetch Oracle Fusion parent-to-child feature relationships with feature codes, classifications, display sequence, and product context. Use when the user asks to browse or export a setup-feature hierarchy, direct feature dependencies, or ordered child features.
---

# Parent Child Feature Hierarchy

Retrieve direct parent-to-child feature relationships from the BOSS
`featureHierarchies` business object. Its single mapping query constrains the
hierarchy root to the direct parent, so it includes standalone offerings,
functional areas, and features without walking each root separately. Batched
Feature lookups for only the returned parents add family product context.

Default output is a compact JSON preview. When the user asks for the entire
list, run the script with `--all`; it writes a CSV and reports its path. Do not
present a partial export as complete.

## Output

`PRODUCT`, `PARENT_FEATURE_NAME`, `PARENT_FEATURE_CODE`,
`PARENT_CLASSIFICATION`, `DISPLAY_SEQUENCE`, `CHILD_FEATURE_NAME`,
`CHILD_FEATURE_CODE`, and `CHILD_CLASSIFICATION`.

`PRODUCT` is the parent feature's family `userModuleName`. The script preserves
the direct relationship (rather than inferring it from a flattened path) and
orders rows by product, parent, then numeric display sequence. Normalize raw
BOSS classifications to `Offering`, `Functional Area`, or `Feature`.

## Execution

Run from the repository workspace root:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/parent-child-feature-hierarchy.py \
  --properties core/auth/fusionEnv.properties \
  --preview-limit 25
```

For a complete export:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/parent-child-feature-hierarchy.py \
  --properties core/auth/fusionEnv.properties \
  --all --project-id <project_id>
```

Use `--parent-feature-code` to restrict output to one direct parent and
`--output` to choose an explicit CSV path. Use BOSS OAuth (`boss_scope`) and never print
tokens or authorization headers. Review the API contract below before changing
endpoint behavior.

Pass `--verbose` for updates after hierarchy retrieval, the existing batched
parent-feature metadata lookup, and CSV creation.

## API contract

| Purpose | Endpoint |
|---|---|
| Direct hierarchy edge, parent and child feature codes/names/classifications, and display sequence | `GET /api/boss/data/objects/ora/commonSetup/features/v1/featureHierarchies` |
| Feature-family product context | `GET /api/boss/data/objects/ora/commonSetup/features/v1/features` |

`featureHierarchies` is the direct FeatureHierarchy business object. Its default
view returns `featureHierarchyId` and `displaySequence`, with embedded
`parentFeature` and `childFeature` objects that return codes, names, and
classifications. The bulk Feature resource supplies `family.userModuleName`.

Use `$limit` and `$offset` for every page. For the complete direct mapping, use
one paginated hierarchy query:

`$filter=feature.featureShortName=parentFeature.featureShortName`

It keeps rows where the hierarchy root and the direct parent are the same,
including parents that are offerings, FAs, or standalone features. Join product
context by retrieving only the returned parent codes from the Feature resource
in `featureShortName in (...)` batches. For `--parent-feature-code`, replace
that comparison with `$filter=feature.featureShortName='{parent_feature_code}'`.
