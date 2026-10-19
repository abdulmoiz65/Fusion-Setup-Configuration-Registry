# Configure Item Shortage Parameters Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| `ora_defaulting_rules.md` — Source Provenance | Pins the `ruleConfigurationHeaders` REST/UI route and physical shape to exact Redwood source artifacts, digests, and line ranges |
| Generated task skill metadata | Declares REST-backed Data Loader routing and the ordered business object `ruleConfigurationHeaders` from the effective setup-task catalog |
| Per-run Data Loader metadata preflight | Verifies selected-environment visibility; this is required runtime readiness evidence and cannot be reused |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Context defaulting and input route mapping | Apply the approved RuleType context mapping and Module default; retain catalog/category values as project inputs |
| 2 | Catalog and category resolution | Resolve catalog to CatalogId, then resolve category within that CatalogId to CategoryId; stage Context1 and DefaultValue respectively |
| 3 | Default Period resolution | For the three approved period RuleTypes, resolve a supplied period meaning or code through its context-specific standard lookup |
| 4 | Data Loader metadata preflight | For every run, verify ruleConfigurationHeaders metadata in the selected environment before handing data to core.data-loader |
| 5 | Governed execution handoff | Pass only preflight-ready data to core.data-loader; Fusion remains the system of execution |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| rule_configuration_headers_route | Source-pinned BO route | Yes | Authoring and execution planning | Satisfied | `ora_defaulting_rules.md` Source Provenance | | Source-pinned UI/catalog evidence identifies the resource and child route but does not prove current runtime readiness | Retain ruleConfigurationHeaders as the selected ordered BO; do not treat the source snapshot as a load preflight | Business object discriminator |
| item_catalog_lookup | Item Catalog identity | Conditional | RuleType is ITEM_CATEGORY | Lookup | /fscmRestApi/resources/11.13.18.05/itemCatalogs | resolve_item_catalog | DefaultCatalogName must become one CatalogId before the category can be scoped | Supply a project-specific DefaultCatalogName | Context1 / CatalogId |
| item_category_lookup | Item Category identity | Conditional | RuleType is ITEM_CATEGORY | Lookup | /fscmRestApi/resources/11.13.18.05/itemCategories, scoped to returned CatalogId | resolve_item_category | DefaultCategoryName must become one CategoryId within the selected catalog | Supply a project-specific DefaultCategoryName | DefaultValue / CategoryId |
| average_demand_period_lookup | Average Demand Period identity | Conditional | RuleType is AVERAGE_DEMAND_PERIOD and a period meaning or code is supplied | Lookup | standardLookupsLOV with ORA_INV_SHORT_AVG_DEMAND_DAYS | resolve_average_demand_period | The Redwood UI displays Meaning and stages LookupCode | Supply DefaultPeriod or DefaultPeriodMeaning, DefaultPeriodCode, or matching values for both | DefaultValue or ValueId; DefaultPeriodMeaning |
| open_supply_period_lookup | Open Supply Period identity | Conditional | RuleType is OPEN_SUPPLY_PERIOD and a period meaning or code is supplied | Lookup | standardLookupsLOV with ORA_INV_SHORT_OP_SUPPLY_DAYS | resolve_open_supply_period | The Redwood UI displays Meaning and stages LookupCode | Supply DefaultPeriod or DefaultPeriodMeaning, DefaultPeriodCode, or matching values for both | DefaultValue or ValueId; DefaultPeriodMeaning |
| open_demand_period_lookup | Open Demand Period identity | Conditional | RuleType is OPEN_DEMAND_PERIOD and a period meaning or code is supplied | Lookup | standardLookupsLOV with ORA_INV_SHORT_OP_DEMAND_DAYS | resolve_open_demand_period | The Redwood UI displays Meaning and stages LookupCode | Supply DefaultPeriod or DefaultPeriodMeaning, DefaultPeriodCode, or matching values for both | DefaultValue or ValueId; DefaultPeriodMeaning |
| rule_configuration_headers_metadata_preflight | Per-run Data Loader metadata preflight | Yes | Before every core.data-loader handoff | Verify | Selected environment and ruleConfigurationHeaders metadata | | A successful prior preflight is runtime evidence only for that run and must not be reused | Record the selected environment and ruleConfigurationHeaders result for the current run; block when metadata is unavailable or not visible | Selected environment; business object discriminator; metadata result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Source-pinned route identifies ruleConfigurationHeaders | Continue planning only |
| Lookup | A supplied Default Period meaning or code needs RuleType-specific standard-lookup resolution | Read-only only |
| Lookup | A Category catalog/category display value needs catalog-first ID resolution | Read-only only |
| Verify | The current run must confirm selected-environment Data Loader metadata | Read-only metadata preflight only |
| Blocked | Metadata is unavailable, the BO is not visible, or the selected environment cannot be identified | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.CHECK_METADATA | decision | 80 | resolve_dependency | ready->ISP.DATA_LOADER_HANDOFF;blocked->ISP.HANDLE_ERROR | ISP.RESOLVE_OPEN_DEMAND_PERIOD | stop | After approved defaulting, catalog/category and period resolution, and before every Data Loader handoff |
