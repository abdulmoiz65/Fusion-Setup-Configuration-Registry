---
task_code: "FND_MANAGE_PROFILE_OPTIONS"
task_name: "Manage Profile Options"
scoped_task_name: "Manage Pricing Profile Options"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
route_skill_id: "core.fusion-api.apps-common"
route_child_skill_id: "core.fusion-api.apps-common.profile-options"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Pricing Profile Options

## Setup Task Metadata

- Task name: `Manage Profile Options`
- Pricing-scoped task name: `Manage Pricing Profile Options`
- Task code: `FND_MANAGE_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`

## Mandatory Route

Route every request for the Pricing profile options listed below to
`core.fusion-api.apps-common`. That core entry point must select
`core.fusion-api.apps-common.profile-options`; do not call a Fusion REST
client, data loader, or browser workflow directly from this Pricing task.

Use the profile-options workflow to read effective values or configured
profile-option definitions and values. Before any create, update, or delete,
validate the target environment, profile definition, level, scope key, current
value, intended value, and required privilege. Obtain explicit approval
immediately before the write. Do not retry a mutating request automatically.

## Pricing Profile Options

```text
ORA_QP_ALGO_ENABLE_RECOMPIL_THRU_ESS
ORA_QP_COST_LISTS_REDWOOD_ENABLED
ORA_QP_CURRENCY_CONV_LISTS_REDWOOD_ENABLED
ORA_QP_DISCOUNT_LISTS_REDWOOD_ENABLED
ORA_QP_ORDER_MANAGEMENT_PARAMETERS_REDWOOD_ENABLED
ORA_QP_PL_MASS_ACTION_ONLINE_LIMIT
ORA_QP_PRCPROF_SEGMENTS_REDWOOD_ENABLED
ORA_QP_PRICE_ELEMENTS_REDWOOD_ENABLED
ORA_QP_PRICE_LISTS_REDWOOD_ENABLED
ORA_QP_PRICING_ADMINISTRATION_LANDING_PAGE_REDWOOD_ENABLED
ORA_QP_PRICING_BASES_REDWOOD_ENABLED
ORA_QP_PRICING_CHARGE_DEFINITIONS_REDWOOD_ENABLED
ORA_QP_PRICING_MATRIX_TYPES_REDWOOD_ENABLED
ORA_QP_PRICING_MESSAGES_REDWOOD_ENABLED
ORA_QP_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS_REDWOOD_ENABLED
ORA_QP_PRICING_PARAMETERS_REDWOOD_ENABLED
ORA_QP_PRICING_PROCESS_ASSIGNMENTS_REDWOOD_ENABLED
ORA_QP_PRICING_ROUNDING_RULES_REDWOOD_ENABLED
ORA_QP_PRICING_ROUNDING_RULE_ASSIGNMENTS_REDWOOD_ENABLED
ORA_QP_PRICING_STRATEGIES_REDWOOD_ENABLED
ORA_QP_SERVICE_MAPPINGS_GROOVY_PARSER_VERSION
ORA_QP_SHIPPING_CHARGE_LISTS_REDWOOD_ENABLED
QP_ALGO_ENABLE_FACTORY_MODE_RUN
QP_CONTEXT_SERVICE_PROFILER_CONFIG
RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION
```

## Usage

Use this metadata when planning, validating, reading, or changing a listed
Pricing profile option under the Order Management Pricing functional area. For
`RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION`, read the current Site value when
resolving a recurring charge definition's Price Periodicity UOM Class.
