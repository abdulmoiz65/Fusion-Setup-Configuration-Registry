# Configure Planning Analytics Lookup Outcomes

## Error Situations

| Situation | What Should Happen |
|---|---|
| A requested catalog, dimension, hierarchy, planning measure, planning measure group, or requested planning level has no exact match | Stop the configuration selection and report the requested identity as missing. |
| A name-based lookup returns more than one exact match | Stop the configuration selection and require an exact identifier. |
| A lookup response identity differs from the supplied path identifier | Stop the configuration selection; do not use the returned record. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPA.DONE_LOOKUP_DIMENSION_CATALOGS | terminal | 100 | terminal | none | CPA.LOOKUP_DIMENSION_CATALOGS | stop | Return only the requested find_dimension_catalogs lookup result; no write |
| CPA.DONE_LOOKUP_DIMENSION_CATALOG | terminal | 101 | terminal | none | CPA.LOOKUP_DIMENSION_CATALOG | stop | Return only the requested find_dimension_catalog_by_id lookup result; no write |
| CPA.DONE_LOOKUP_CATALOG_HIERARCHIES | terminal | 102 | terminal | none | CPA.LOOKUP_CATALOG_HIERARCHIES | stop | Return only the requested find_dimension_catalog_hierarchies lookup result; no write |
| CPA.DONE_LOOKUP_CATALOG_HIERARCHY | terminal | 103 | terminal | none | CPA.LOOKUP_CATALOG_HIERARCHY | stop | Return only the requested find_dimension_catalog_hierarchy_by_id lookup result; no write |
| CPA.DONE_LOOKUP_DIMENSIONS | terminal | 104 | terminal | none | CPA.LOOKUP_DIMENSIONS | stop | Return only the requested find_dimensions lookup result; no write |
| CPA.DONE_LOOKUP_DIMENSION | terminal | 105 | terminal | none | CPA.LOOKUP_DIMENSION | stop | Return only the requested find_dimension_by_code lookup result; no write |
| CPA.DONE_LOOKUP_DIMENSION_HIERARCHIES | terminal | 106 | terminal | none | CPA.LOOKUP_DIMENSION_HIERARCHIES | stop | Return only the requested find_dimension_hierarchies lookup result; no write |
| CPA.DONE_LOOKUP_DIMENSION_HIERARCHY | terminal | 107 | terminal | none | CPA.LOOKUP_DIMENSION_HIERARCHY | stop | Return only the requested find_dimension_hierarchy_by_id lookup result; no write |
| CPA.DONE_LOOKUP_PLANNING_HIERARCHIES | terminal | 108 | terminal | none | CPA.LOOKUP_PLANNING_HIERARCHIES | stop | Return only the requested find_planning_hierarchies lookup result; no write |
| CPA.DONE_LOOKUP_PLANNING_HIERARCHY | terminal | 109 | terminal | none | CPA.LOOKUP_PLANNING_HIERARCHY | stop | Return only the requested find_planning_hierarchy_by_id lookup result; no write |
| CPA.DONE_LOOKUP_MEASURE_CATALOG | terminal | 110 | terminal | none | CPA.LOOKUP_MEASURE_CATALOG | stop | Return only the requested find_planning_measure_catalog lookup result; no write |
| CPA.DONE_LOOKUP_MEASURE_CATALOG_DETAILS | terminal | 111 | terminal | none | CPA.LOOKUP_MEASURE_CATALOG_DETAILS | stop | Return only the requested find_planning_measure_catalog_by_id lookup result; no write |
| CPA.DONE_LOOKUP_MEASURE_CATALOG_MEASURES | terminal | 112 | terminal | none | CPA.LOOKUP_MEASURE_CATALOG_MEASURES | stop | Return only the requested find_planning_measure_catalog_measures lookup result; no write |
| CPA.DONE_LOOKUP_PLANNING_MEASURES | terminal | 113 | terminal | none | CPA.LOOKUP_PLANNING_MEASURES | stop | Return only the requested find_planning_measure_by_id_or_name lookup result; no write |
| CPA.DONE_LOOKUP_PLANNING_MEASURE_GROUPS | terminal | 114 | terminal | none | CPA.LOOKUP_PLANNING_MEASURE_GROUPS | stop | Return only the requested find_planning_measure_group_by_id_or_name lookup result; no write |
| CPA.DONE_LOOKUP_GROUP_PLANNING_MEASURES | terminal | 115 | terminal | none | CPA.LOOKUP_GROUP_PLANNING_MEASURES | stop | Return only the requested list_planning_measures_in_group lookup result; no write |
| CPA.DONE_LIST_PLANNING_LEVELS | terminal | 119 | terminal | none | CPA.LIST_PLANNING_LEVELS | stop | Return only the requested list_planning_levels lookup result; no write |
| CPA.DONE_FIND_PLANNING_LEVEL_BY_NAME | terminal | 120 | terminal | none | CPA.FIND_PLANNING_LEVEL_BY_NAME | stop | Return only the requested find_planning_level_by_name lookup result; no write |
| CPA.DONE_FIND_PLANNING_LEVEL_BY_ID | terminal | 121 | terminal | none | CPA.FIND_PLANNING_LEVEL_BY_ID | stop | Return only the requested find_planning_level_by_id lookup result; no write |
| CPA.ITEM_ATTRIBUTE_VALIDATED | terminal | 130 | terminal | none | CPA.VALIDATE_ITEM_ATTRIBUTE | stop | Return successful item-level name and supplied datatype validation; no write |
| CPA.ORGANIZATION_ATTRIBUTE_VALIDATED | terminal | 131 | terminal | none | CPA.VALIDATE_ORGANIZATION_ATTRIBUTE | stop | Return successful organization-level name and supplied datatype validation; no write |
| CPA.LEVEL_ATTRIBUTES_COMPLETE | terminal | 132 | terminal | none | CPA.SELECT_LEVEL_ATTRIBUTE_NAMES | stop | Return existing attributes without creation validation or a write |
| CPA.DIMENSION_DELETION_CHECKED | terminal | 133 | terminal | none | CPA.ENFORCE_CATALOG_DELETION | stop | Return dimension-catalog deletion eligibility; no deletion or approval |
| CPA.MEASURE_DELETION_CHECKED | terminal | 134 | terminal | none | CPA.ENFORCE_MEASURE_CATALOG_DELETION | stop | Return measure-catalog deletion eligibility; no deletion or approval |
| CPA.LOOKUP_FAILURE | terminal | 999 | terminal | none | none | stop | Return missing, unsupported, invalid, ambiguous, failed or blocked details and the corrective action; no write |
