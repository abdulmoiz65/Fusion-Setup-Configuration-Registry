# Configure Item Shortage Parameters Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| `ora_defaulting_rules.md` — Source Provenance | Pins each Default Period `standardLookupsLOV` control and the CatalogId/CategoryId Redwood field mappings to source artifacts, digests, and line ranges |
| Per-run configured-target REST verification | Confirms the selected environment can currently read the source-pinned contracts; it is not reusable provenance or a substitute for the resolver's failure handling |

## Core REST Delegation

All five resolvers are read-only lookup requirements, not task-local REST execution. Invoke them only through `core.fusion-api.rest-api-client`. That core service owns authentication, selected-target validation, token refresh, request diagnostics, redaction, the one permitted 401/403 refresh retry, and timeout handling. This task owns only the lookup contract, exact-match rule, and physical value mapping. Do not call a task-local REST client or use direct REST write guidance.

All resolvers use the stable relative paths below. The configured core REST client joins each path to the selected environment's REST base URL; this task does not persist a host, environment-specific ID, or release suffix.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_item_catalog | RuleType is ITEM_CATEGORY and DefaultCatalogName is supplied | DefaultCatalogName | /fscmRestApi/resources/11.13.18.05/itemCatalogs with `onlyData=true`, `fields=CatalogId,CatalogName`, and `q=CatalogName='<escaped DefaultCatalogName>'` | CatalogId, CatalogName | Trim outer whitespace and require exactly one case-insensitive exact match of DefaultCatalogName to CatalogName. | Context1: CatalogId; DefaultCatalogName: CatalogName | Zero or multiple matches, inaccessible route, or an invalid query input blocks Data Loader preparation. Do not prefix-match, fuzzy-match, or select the first candidate. |
| resolve_item_category | RuleType is ITEM_CATEGORY and DefaultCategoryName is supplied | Context1/CatalogId from resolve_item_catalog; DefaultCategoryName | /fscmRestApi/resources/11.13.18.05/itemCategories with request header `REST-Framework-Version: 9`, `onlyData=true`, `fields=CategoryCode,CategoryId,CategoryName`, and `q=CatalogId=<resolved CatalogId> and UPPER(CategoryName) LIKE UPPER('<escaped DefaultCategoryName>%')` | CategoryCode, CategoryId, CategoryName | Trim outer whitespace and require exactly one case-insensitive exact match of DefaultCategoryName to CategoryName within the resolved CatalogId. | DefaultValue: CategoryId; DefaultCategoryName: CategoryName; CategoryCode: returned diagnostic/display value only | Zero or multiple matches, inaccessible route, a missing or rejected framework-version header, or a category outside the resolved catalog blocks Data Loader preparation. Do not prefix-match in final matching, fuzzy-match, or select the first candidate. |
| resolve_average_demand_period | RuleType is AVERAGE_DEMAND_PERIOD and a Default Period meaning, code, or both are supplied | DefaultPeriod, DefaultPeriodMeaning, DefaultPeriodCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder%3BLookupType%3DORA_INV_SHORT_AVG_DEMAND_DAYS&fields=Meaning%2CLookupCode&onlyData=true | Meaning, LookupCode | Trim outer whitespace and require exactly one case-insensitive exact match: DefaultPeriod or DefaultPeriodMeaning to Meaning, and DefaultPeriodCode to LookupCode. When both meaning and code are supplied, they must identify the same row. | DefaultValue: LookupCode for a section default; ValueId: LookupCode for a rule line; DefaultPeriodMeaning: Meaning | Zero or multiple matches, inaccessible LOV, or conflicting supplied values block Data Loader preparation. Do not fuzzy-match or select the first candidate. |
| resolve_open_supply_period | RuleType is OPEN_SUPPLY_PERIOD and a Default Period meaning, code, or both are supplied | DefaultPeriod, DefaultPeriodMeaning, DefaultPeriodCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder%3BLookupType%3DORA_INV_SHORT_OP_SUPPLY_DAYS&fields=Meaning%2CLookupCode&onlyData=true | Meaning, LookupCode | Trim outer whitespace and require exactly one case-insensitive exact match: DefaultPeriod or DefaultPeriodMeaning to Meaning, and DefaultPeriodCode to LookupCode. When both meaning and code are supplied, they must identify the same row. | DefaultValue: LookupCode for a section default; ValueId: LookupCode for a rule line; DefaultPeriodMeaning: Meaning | Zero or multiple matches, inaccessible LOV, or conflicting supplied values block Data Loader preparation. Do not fuzzy-match or select the first candidate. |
| resolve_open_demand_period | RuleType is OPEN_DEMAND_PERIOD and a Default Period meaning, code, or both are supplied | DefaultPeriod, DefaultPeriodMeaning, DefaultPeriodCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder%3BLookupType%3DORA_INV_SHORT_OP_DEMAND_DAYS&fields=Meaning%2CLookupCode&onlyData=true | Meaning, LookupCode | Trim outer whitespace and require exactly one case-insensitive exact match: DefaultPeriod or DefaultPeriodMeaning to Meaning, and DefaultPeriodCode to LookupCode. When both meaning and code are supplied, they must identify the same row. | DefaultValue: LookupCode for a section default; ValueId: LookupCode for a rule line; DefaultPeriodMeaning: Meaning | Zero or multiple matches, inaccessible LOV, or conflicting supplied values block Data Loader preparation. Do not fuzzy-match or select the first candidate. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A Default Period meaning is supplied | Run the resolver for the header RuleType and fill the route-specific LookupCode output |
| DefaultCatalogName and DefaultCategoryName are supplied for Category | Run resolve_item_catalog through the standard Item Catalog route, then run resolve_item_category using only the returned CatalogId; fill Context1 and DefaultValue with the returned IDs |
| resolve_item_category is run | Send `REST-Framework-Version: 9` through the configured core REST client. Do not assume its framework-version default is suitable for this resolver. |
| A Default Period code is supplied | Validate it through the same header-RuleType resolver before Data Loader handoff |
| A meaning and code are supplied | Resolve both and block unless they identify the same single row |
| No Default Period input is supplied | Continue without a lookup; Data Loader and Fusion own required-field validation |
| The header RuleType is not a period context | Do not run these resolvers |

## Golden Scenario

| Scenario | Synthetic Input Context | Expected Local Path | Expected Result |
|---|---|---|---|
| Non-category threshold | Item Shortage Parameter context is `Shortage threshold`; no catalog, category, or Default Period input | ISP.VALIDATE_INPUT -> ISP.RESOLVE_ITEM_CATALOG (not_required) -> ISP.RESOLVE_AVERAGE_DEMAND_PERIOD (not_required) -> ISP.RESOLVE_OPEN_SUPPLY_PERIOD (not_required) -> ISP.RESOLVE_OPEN_DEMAND_PERIOD (not_required) -> ISP.CHECK_METADATA | RuleType is SHORTAGE_THRESHOLD, catalog/category lookups are skipped, and the per-run ruleConfigurationHeaders metadata preflight is reached. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.RESOLVE_ITEM_CATALOG | decision | 30 | reference_lookup | resolved->ISP.RESOLVE_ITEM_CATEGORY;not_required->ISP.RESOLVE_AVERAGE_DEMAND_PERIOD;blocked->ISP.HANDLE_ERROR;failure->ISP.HANDLE_ERROR | ISP.VALIDATE_INPUT | stop | Resolve required DefaultCatalogName through the standard Item Catalog route for ITEM_CATEGORY; skip for every other RuleType |
| ISP.RESOLVE_ITEM_CATEGORY | decision | 40 | reference_lookup | resolved->ISP.RESOLVE_AVERAGE_DEMAND_PERIOD;not_required->ISP.RESOLVE_AVERAGE_DEMAND_PERIOD;blocked->ISP.HANDLE_ERROR;failure->ISP.HANDLE_ERROR | ISP.RESOLVE_ITEM_CATALOG | stop | Resolve required DefaultCategoryName within the CatalogId returned by resolve_item_catalog; skip for every other RuleType |
| ISP.RESOLVE_AVERAGE_DEMAND_PERIOD | decision | 50 | reference_lookup | resolved->ISP.RESOLVE_OPEN_SUPPLY_PERIOD;not_required->ISP.RESOLVE_OPEN_SUPPLY_PERIOD;blocked->ISP.HANDLE_ERROR;failure->ISP.HANDLE_ERROR | ISP.RESOLVE_ITEM_CATEGORY | stop | Resolve Default Period for AVERAGE_DEMAND_PERIOD when supplied |
| ISP.RESOLVE_OPEN_SUPPLY_PERIOD | decision | 60 | reference_lookup | resolved->ISP.RESOLVE_OPEN_DEMAND_PERIOD;not_required->ISP.RESOLVE_OPEN_DEMAND_PERIOD;blocked->ISP.HANDLE_ERROR;failure->ISP.HANDLE_ERROR | ISP.RESOLVE_AVERAGE_DEMAND_PERIOD | stop | Resolve Default Period for OPEN_SUPPLY_PERIOD when supplied |
| ISP.RESOLVE_OPEN_DEMAND_PERIOD | decision | 70 | reference_lookup | resolved->ISP.CHECK_METADATA;not_required->ISP.CHECK_METADATA;blocked->ISP.HANDLE_ERROR;failure->ISP.HANDLE_ERROR | ISP.RESOLVE_OPEN_SUPPLY_PERIOD | stop | Resolve Default Period for OPEN_DEMAND_PERIOD when supplied |
