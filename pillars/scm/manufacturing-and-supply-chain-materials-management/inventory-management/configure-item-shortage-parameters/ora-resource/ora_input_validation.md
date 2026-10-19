# Configure Item Shortage Parameters Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| `ora_defaulting_rules.md` — Source Provenance | Pins the sections, physical header/line fields, `ruleConfigurationHeaders` route, and three period lookup contracts to exact Redwood source artifacts, digests, and line ranges |
| Per-run Data Loader metadata preflight | Verifies current target-environment visibility only; it is mandatory before every load and is not provenance for domain mappings |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local validation ownership | Apply the approved parameter-context RuleType mapping and Module default, preserve the remaining source-backed physical field mappings, and require the governed metadata preflight before Data Loader handoff |
| Backend-owned validation | Data Loader and Fusion own required fields, keys, uniqueness, lengths, numeric domains, rule-expression semantics, and unsupported input checks |
| LOV and default handling | Resolve explicitly supplied catalog and category display names to physical IDs before Data Loader handoff. Project-specific catalog/category defaults belong in a project-scoped decision or configuration artifact, not this reusable skill. The three approved Default Period resolvers normalize only their documented period contexts. |
| REST execution | Do not create direct REST write guidance; core.data-loader owns governed execution for ruleConfigurationHeaders |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Header rule context | Item Shortage Parameter context, OrganizationId, Context1, DefaultValue, RuleType, Module | Default RuleType from the approved context and Module to SHORTAGE; preserve other omissions for Data Loader and Fusion validation | Supply one approved context value and the intended physical header fields | Before Data Loader preparation | |
| Rule line mapping | InvRuleConfigurationLines with RuleName, RuleExpression, ValueId, and Context1 when a line is configured | Preserve the omission for Data Loader and Fusion validation | Provide the rule data in the registered business-object shape | Before Data Loader preparation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A request contains shortage-parameter header or line data | Continue after RuleType is derived from the approved parameter context and Module is SHORTAGE | Run the per-run ruleConfigurationHeaders Data Loader metadata preflight | |
| A Category request contains DefaultCatalogName and DefaultCategoryName | Resolve the required catalog name first and resolve the required category name in the returned catalog context before Data Loader preparation | Fill Context1 with CatalogId and DefaultValue with CategoryId | resolve_item_catalog |
| A Default Period meaning or code is supplied for Average Demand Period | Continue only after the resolver returns one LookupCode | Fill DefaultValue for a section default or ValueId for a rule line with the resolved LookupCode | resolve_average_demand_period |
| A Default Period meaning or code is supplied for Open Supply Period | Continue only after the resolver returns one LookupCode | Fill DefaultValue for a section default or ValueId for a rule line with the resolved LookupCode | resolve_open_supply_period |
| A Default Period meaning or code is supplied for Open Demand Period | Continue only after the resolver returns one LookupCode | Fill DefaultValue for a section default or ValueId for a rule line with the resolved LookupCode | resolve_open_demand_period |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| RuleType context normalization | Map Category to ITEM_CATEGORY; Shortage threshold to SHORTAGE_THRESHOLD; Average demand period to AVERAGE_DEMAND_PERIOD; Open supply period to OPEN_SUPPLY_PERIOD; Open demand period to OPEN_DEMAND_PERIOD; and Shortage Threshold for Kanban to SHORTAGE_THRESHOLD_FOR_KANBAN | An Item Shortage Parameter context is supplied | |
| Conflicting RuleType | Reject when an explicit RuleType differs from the approved mapping for the supplied context | Both Item Shortage Parameter context and RuleType are supplied | |
| Module default and validation | Fill an omitted Module with SHORTAGE; reject an explicit Module other than SHORTAGE | A ruleConfigurationHeaders header is prepared | |
| Average Demand Default Period normalization | Accept DefaultPeriod or DefaultPeriodMeaning as a Meaning, DefaultPeriodCode as a LookupCode, or both; resolve through ORA_INV_SHORT_AVG_DEMAND_DAYS and fill DefaultValue or ValueId with LookupCode | RuleType is AVERAGE_DEMAND_PERIOD | resolve_average_demand_period |
| Open Supply Default Period normalization | Accept DefaultPeriod or DefaultPeriodMeaning as a Meaning, DefaultPeriodCode as a LookupCode, or both; resolve through ORA_INV_SHORT_OP_SUPPLY_DAYS and fill DefaultValue or ValueId with LookupCode | RuleType is OPEN_SUPPLY_PERIOD | resolve_open_supply_period |
| Open Demand Default Period normalization | Accept DefaultPeriod or DefaultPeriodMeaning as a Meaning, DefaultPeriodCode as a LookupCode, or both; resolve through ORA_INV_SHORT_OP_DEMAND_DAYS and fill DefaultValue or ValueId with LookupCode | RuleType is OPEN_DEMAND_PERIOD | resolve_open_demand_period |
| Item category mapping | Require DefaultCatalogName and DefaultCategoryName. Resolve the catalog to one CatalogId, then resolve the category name within that CatalogId. Fill Context1 with CatalogId and DefaultValue with CategoryId. | RuleType is ITEM_CATEGORY | resolve_item_category |
| Period mapping | Redwood stages a selected LookupCode in DefaultValue for a section default and ValueId for a rule line; Meaning is display-only | AVERAGE_DEMAND_PERIOD, OPEN_DEMAND_PERIOD, or OPEN_SUPPLY_PERIOD is configured | |
| Threshold mapping | Redwood stages a numeric value in DefaultValue for a section default and ValueId for a rule line | SHORTAGE_THRESHOLD or SHORTAGE_THRESHOLD_FOR_KANBAN is configured | |
| Kanban threshold applicability | Preserve the section only when the ORA_INV_ITEM_SHORTAGE_KANBAN feature is enabled; Fusion owns feature validation | SHORTAGE_THRESHOLD_FOR_KANBAN is supplied | |
| Blank values | Preserve blanks; Data Loader and Fusion own defaulting and validation | Any field is omitted | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.VALIDATE_INPUT | step | 20 | validate_input | valid->ISP.RESOLVE_ITEM_CATALOG;invalid->ISP.HANDLE_ERROR | ISP.APPLY_CONTEXT_DEFAULTS | stop | After approved RuleType and Module defaulting, before catalog/category and Default Period resolution and Data Loader preparation |
