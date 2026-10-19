# Configure Planning Analytics Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve the dimension catalog | For a deletion of this catalog type only, retrieve its default status, creator, and associated-plan count. |
| 2 | Resolve the planning measure catalog | For a deletion of this catalog type only, retrieve its default status, creator, and associated-plan count. |
| 3 | Apply the deletion blockers | Do not route a blocked deletion to the Data Loader REST business-object workflow. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Deletion of a dimension catalog is requested | Error | find_dimension_catalog_by_id | IsDefault is true, CreatedBy equals SEED_DATA_FROM_APPLICATION, or PlanDefCount is greater than zero; also block if any required evidence is absent, malformed or identity-mismatched. | Do not delete the catalog. Select a non-default, non-seeded catalog with no associated plans. | No |
| Deletion of a planning measure catalog is requested | Error | find_planning_measure_catalog_by_id | IsDefault is true, CreatedBy equals SEED_DATA_FROM_APPLICATION, or PlanDefCount is greater than zero; also block if any required evidence is absent, malformed or identity-mismatched. | Do not delete the catalog. Select a non-default, non-seeded catalog with no associated plans. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_dimension_catalog_by_id | A dimension-catalog deletion is requested | CatalogId, IsDefault, CreatedBy, PlanDefCount | ora_reference_lookups.md |
| find_planning_measure_catalog_by_id | A planning-measure-catalog deletion is requested | CatalogId, IsDefault, CreatedBy, PlanDefCount | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPA.ENFORCE_CATALOG_DELETION | decision | 52 | design_enforcement | pass->CPA.DIMENSION_DELETION_CHECKED;blocked->CPA.LOOKUP_FAILURE | CPA.LOOKUP_DIMENSION_CATALOG | stop | Evaluate only the dimension-catalog deletion rule for the requested dimension CatalogId |
| CPA.ENFORCE_MEASURE_CATALOG_DELETION | decision | 53 | design_enforcement | pass->CPA.MEASURE_DELETION_CHECKED;blocked->CPA.LOOKUP_FAILURE | CPA.LOOKUP_MEASURE_CATALOG_DETAILS | stop | Evaluate only the planning-measure-catalog deletion rule for the requested measure CatalogId |
