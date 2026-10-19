---
skill_id: "scm.order-management.orders.reservation-priority-for-sales-orders"
name: "Reservation Priority for Sales Orders Setup Task Guidance"
description: "Provides task-specific setup guidance and intent-based section routing for Reservation Priority for Sales Orders under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "ORA_RESERVATION_PRIORITY_FOR_SALES_ORDERS"
task_name: "Reservation Priority for Sales Orders"
parent_skill_id: "scm.order-management.orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.2.7"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/reservation-priority-for-sales-orders/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/reservation-priority-for-sales-orders/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Reservation Priority for Sales Orders Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Reservation Priority for Sales Orders` under `Orders`.

## Setup Task Skill Contract

- task_code: `ORA_RESERVATION_PRIORITY_FOR_SALES_ORDERS`
- task_name: `Reservation Priority for Sales Orders`
- parent_skill_id: `scm.order-management.orders`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Orders`
- functional_area_code: `ORA_DOO_ORDER_FULLFILLMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Reservation Priority for Sales Orders` under `Orders`.

## Setup Task Metadata

- Task name: `Reservation Priority for Sales Orders`
- Task code: `ORA_RESERVATION_PRIORITY_FOR_SALES_ORDERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Fetch the current live state for each requested Reservation Priority section
   with `core.fusion-api.rest-api-client`, using the contracts in
   `ora-resource/ora_reference_lookups.md`.
3. Validate setup task data with `shared.validation.setup-data-validator`.
4. Validate reference data with `shared.validation.reference-data-validator`.
5. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Orders`
- Setup task name: `Reservation Priority for Sales Orders`
- Setup task code: `ORA_RESERVATION_PRIORITY_FOR_SALES_ORDERS`

## Reservation Priority Configuration Sections

Classify the user's configuration intent before preparing or validating an FSM
package. The two sections are independent and must not be substituted for each
other.

| User Intent | Target Section | FSM CSV Member | Routing Rule |
|---|---|---|---|
| Create, add, or change a default sorting order for Reservation Priority | Order Preferences Details | `ORA_ORDER_PREFERENCES_DETAILS.csv` | Route the validated Reservation Priority attribute and requested ordering only to Order Preferences Details. Set `Priority` to `0` for ascending or first position, and `1` for descending or second position. Do not create an Order Preference Rule for this intent. |
| Create, add, or change a Reservation Priority sorting rule | Order Preference Rules | `ORA_PREFERENCE_RULE.csv` | Route the rule definition only to Order Preference Rules. Do not add a default-sorting-order row to Order Preferences Details for this intent. |
| Request includes both a default sorting order and a sorting rule | Both sections | Both CSV members | Validate and update each requested intent in its own section while preserving all unrelated exported rows. |
| Intent does not distinguish a default sorting order from a sorting rule | Clarification required | None | Stop before package preparation and ask whether the request is for Order Preferences Details, Order Preference Rules, or both. |

For a default sorting order, resolve the supplied attribute through
`ORA_FOM_RESERVE_PRIORITY_ATTR`, then use its returned `LookupCode` with the
exported `ORA_ORDER_PREFERENCES_DETAILS.csv` header and field contract. Map
the requested direction or position to `Priority`: `ASC` or first maps to `0`;
`DESC` or second maps to `1`. Use the task-local attribute CSV mapping below
for `AttributeDatatype` and the populated value field. Preserve all other
export-derived fields and rows.

Before preparing a default-sort change, fetch the live default sorting orders
with `fetch_reservation_priority_default_sort_orders`. Before preparing a
sorting-rule change, fetch the live rule details with
`fetch_reservation_priority_rules`. Use these read-only responses to reconcile
the current Reservation Priority state with the fresh FSM export. The REST
responses do not replace the export-derived CSV baseline required for package
creation or import.

For a sorting rule, preserve the exported
`ORA_PREFERENCE_RULE.csv` header and derive the rule-row shape from the current
exported baseline; do not infer undocumented rule fields.

### Sorting Rule Identity and Description

When a sorting-rule request omits a rule name, generate its identity from the
validated Reservation Priority attributes in their requested attribute order.
For one attribute, generate `Prioritize <Attribute Label>`,
`PRIORITIZE_<ATTRIBUTE_LOOKUP_CODE>`, and `Prioritizes Reservation Priority
orders by <Attribute Label>.` For two or more attributes, join the resolved
labels with commas and `and` for the display name and description, and join the
ordered resolved LookupCodes with underscores for the RuleCode. For example,
Customer, Demand Class, and Promised Date generates `Prioritize Customer,
Demand Class, and Promised Date`,
`PRIORITIZE_CUSTOMER_DEMAND_CLASS_PROMISED_DATE`, and `Prioritizes Reservation
Priority orders by Customer, Demand Class, and Promised Date.`

RuleCode values must not exceed 30 characters. When the normal generated code
fits, use it unchanged. Otherwise, generate
`PRIORITIZE_<A1>_<A2>_<A3>_<H6>`, omitting unused attribute segments, where
each `A` segment is the first three uppercase characters of its ordered resolved
LookupCode and `H6` is the first six uppercase hexadecimal characters of the
SHA-256 hash of the ordered LookupCodes joined with `|`. For example, Customer,
Demand Class, and Promised Date generates `PRIORITIZE_CUS_DMD_PRM_D81838`.
Check this length-safe generated RuleCode against the fresh baseline; an
existing code still blocks creation unless the user explicitly requests an
update.

Use the resolved attribute labels and LookupCodes, not the user's unvalidated
input. Preserve a supplied rule name or description. `ORA_PREFERENCE_RULE.csv`
has no name or description columns. For every created rule, add the generated
or supplied name and description to `ORA_TRANSLATION_FOR_PREFERENCE_RULE.csv`.
Use its exported header and add the source-language row:

| ORA_ORDER_PREFERENCES.OrderPreferenceCode | ORA_PREFERENCE_RULE.RuleCode | RuleName | Language | Description | SourceLang |
|---|---|---|---|---|---|
| `RESERVATION_PRIORITY` | created rule `RuleCode` | generated or supplied name | `US` | generated or supplied description | `US` |

Do not invent translated rows for other languages. Preserve all baseline rows;
for an explicit rule update, update only the matching `US` source-language row
unless the user supplies a separate translation. Store the RuleCode in the
export-derived `RuleCode` column, and retain rule identity and description in
the configuration blueprint and approval preview. Before adding a generated
RuleCode, check the fresh baseline. An existing code blocks creation unless the
user explicitly requests an update of that rule.

### Sorting Rule Entry Ordering

For every created Reservation Priority rule entry in `AttributePriorityJson`,
set `Priority` to `1`. Express the requested order exclusively with
`SortingOrder`: first is `1`, second is `2`, and each later choice increments
by one. Do not use `Priority` to represent first, second, or later choices.
Preserve the export-derived JSON field names and types.

### Sorting Rule Attribute Limit

A single Reservation Priority rule can contain at most three distinct selected
attributes. Count distinct `AttributeCode` values, not individual
`AttributePriorityJson` entries: multiple entries for different values of the
same attribute count as one attribute. Stop before package preparation if the
requested rule would contain more than three distinct attributes.

### Sorting Rule State

For a created Reservation Priority rule, set `IsActive` to `N` unless the user
explicitly asks to make the rule active; only then set it to `Y`. Set `IsDefault`
to `N` unless the user explicitly asks to make the rule the default; only then
set it to `Y`.

When a rule is explicitly made the default, inspect the fresh exported
`ORA_PREFERENCE_RULE.csv` baseline and set `IsDefault` to `N` on every other
`RESERVATION_PRIORITY` rule currently marked `Y`, while retaining all their
other export-derived values. The final package must have exactly one default
Reservation Priority rule: the explicitly selected rule. Do not change the
default state of an existing rule when the request does not explicitly set a
default.

## Reservation Priority Attribute Lookups

Resolve every supplied Reservation Priority attribute first through the
following authoritative eligibility lookup. Do not use a hardcoded allowlist of
attribute names.

| Purpose | Lookup Resource | Finder and Parameter | Match and Storage Rule |
|---|---|---|---|
| Valid Reservation Priority attribute | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | `finder=LookupTypeFinder` and `LookupType=ORA_FOM_RESERVE_PRIORITY_ATTR` | Require exactly one exact match for the supplied attribute name or code. Store the returned `LookupCode` as the selected Reservation Priority attribute. Zero or multiple matches block package preparation. |

When a user supplies `Order Type`, `Demand Class`, `Sales Channel`, `Customer
Class`, `Shipment Priority`, or `Customer` as a Reservation Priority attribute,
resolve the supplied value before package preparation. Use the applicable
read-only resolver below and store the specified returned identifier, never the
submitted display value.

| Input Attribute | Lookup Resource | Finder and Parameter | Match and Storage Rule |
|---|---|---|---|
| Order Type | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | `finder=LookupTypeFinder` and `LookupType=ORA_DOO_ORDER_TYPES` | Require exactly one exact match for the supplied Order Type value. Store the returned `LookupCode` in the export-derived field for the selected Reservation Priority section. Zero or multiple matches block package preparation. |
| Demand Class | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | `finder=LookupTypeFinder` and `LookupType=ORA_DOO_DEMAND_CLASS` | Require exactly one exact match for the supplied Demand Class value. Store the returned `LookupCode` in the export-derived field for the selected Reservation Priority section. Zero or multiple matches block package preparation. |
| Sales Channel | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | `finder=LookupTypeFinder` and `LookupType=ORA_QP_CHANNEL_METHODS` | Require exactly one exact match for the supplied Sales Channel value. Store the returned `LookupCode` in the export-derived field for the selected Reservation Priority section. Zero or multiple matches block package preparation. |
| Customer Class | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | `finder=LookupTypeFinder` and `LookupType=CUSTOMER CLASS` | Require exactly one exact match for the supplied Customer Class value. Store the returned `LookupCode` in the export-derived field for the selected Reservation Priority section. Zero or multiple matches block package preparation. |
| Shipment Priority | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | `finder=LookupTypeFinder` and `LookupType=WSH_SHIPPING_PRIORITY` | Require exactly one exact match for the supplied Shipment Priority value. Store the returned `LookupCode` in the export-derived field for the selected Reservation Priority section. Zero or multiple matches block package preparation. |
| Customer | `/fscmRestApi/resources/11.13.18.05/omCustomersLOV` | Use the customer LOV response to evaluate the supplied Customer value | Require exactly one exact match for the supplied Customer value. Store the returned `PartyId` in the export-derived field for the selected Reservation Priority section. Zero or multiple matches block package preparation. |

These lookups resolve attribute values only. They do not choose between the
Default Sorting Order and Sorting Rules sections; apply the section-intent
routing above first.

## Reservation Priority Attribute CSV Mapping

For a validated Reservation Priority attribute, use this mapping to construct
the `ORA_ORDER_PREFERENCES_DETAILS.csv` row. Populate exactly the mapped value
column; leave the two other value columns blank. For `CUSTOMER`, resolve and
store the returned `PartyId` as the numeric value.

| Attribute LookupCode | AttributeDatatype | Populated CSV Value Column |
|---|---|---|
| `CUSTOMER` | `NUMBER` | `AttributeNumValue` |
| `CUSTOMER_CLASS` | `VARCHAR` | `AttributeStringValue` |
| `DEMAND_CLASS` | `VARCHAR` | `AttributeStringValue` |
| `ORDERED_DATE` | `DATE` | `AttributeDateValue` |
| `ORDER_TYPE` | `VARCHAR` | `AttributeStringValue` |
| `PROMISED_DATE` | `DATE` | `AttributeDateValue` |
| `REQUESTED_DATE` | `DATE` | `AttributeDateValue` |
| `SALES_CHANNEL` | `VARCHAR` | `AttributeStringValue` |
| `SCHEDULED_ARRIVAL_DATE` | `DATE` | `AttributeDateValue` |
| `SCHEDULED_SHIP_DATE` | `DATE` | `AttributeDateValue` |
| `SHIPMENT_PRIORITY` | `VARCHAR` | `AttributeStringValue` |

Examples:

- “Create a default sorting order for Promised Date ascending” routes to
  `ORA_ORDER_PREFERENCES_DETAILS.csv`.
- “Create a Reservation Priority sorting rule” routes to
  `ORA_PREFERENCE_RULE.csv`.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.order-management.orders` for functional-area sequencing and scope decisions. Classify the requested Reservation Priority section before invoking export, validation, or Data Loader workflows. Track token usage for any generated project artifact or skill-run record using the manifest policy.
