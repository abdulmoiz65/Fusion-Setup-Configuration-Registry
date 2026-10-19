---
task_code: "ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Channel Descriptive Flexfields"
parent_skill_id: "scm.order-management.channel-revenue-management"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Channel Descriptive Flexfields

## Setup Task Metadata

- Task name: `Manage Channel Descriptive Flexfields`
- Task code: `ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Descriptive Flexfield Routing

Route all task requests for this descriptive flexfield to
`core.fusion-api.apps-common`, which selects
`core.fusion-api.apps-common.descriptive-flexfields`.

- Require the request to identify the target descriptive flexfield code.
- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Descriptive Flexfields`
- Setup task code: `ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS`

The selected Apps Common DFF workflow owns the downstream setup-data route:

1. Export through `shared.setup-export.task-level-export`.
2. Import an approved task-level CSV artifact through the FSM workflow in
   `core.data-loader`.
3. Do not substitute direct REST transport for this DFF workflow.

`dataloader_import_mode: FSM` records the selected downstream transport; it
does not replace Apps Common as the task's primary route.

For an FSM segment package, derive the required DFF parent and requested
context parent carrier rows from the supplied DFF identity, resolved
application ID, source context identities, and task template. A current export
is reconciliation evidence for an existing carrier, not a user-supplied
dependency. Do not produce a child-only package.

## Value Set Dependency and REST Reference

When a DFF segment is created or updated with a `ValueSetCode`, resolve the
exact value-set definition through `core.fusion-api.apps-common`, selecting
`core.fusion-api.apps-common.value-sets`. The core workflow owns the
read-only REST interaction; this task must not construct or call it directly.

When the source supplies a value-set name or description instead of a code,
apply the task-scoped `resolve_value_set_code_from_name` lookup in
[ora_reference_lookups.md](ora-resource/ora_reference_lookups.md) before
generating the FSM CSV row.

The applicable reference is the Fusion value-set collection:

```text
GET /fscmRestApi/resources/11.13.18.05/valueSets
```

Resolve exactly one returned `ValueSetCode` and retain its validation contract,
including validation type, data type, subtype, maximum length, format flags,
and the returned navigation reference for child values when applicable. A
missing, ambiguous, or incompatible result blocks FSM package preparation.

For any proposed `DefaultType: CONSTANT`, validate `DefaultValue` against the
resolved value-set contract before preparing the FSM package. Validate format,
data type, length, and other returned constraints. Resolve a child value only
when the current DFF export or documented value-set contract explicitly makes
child-value selection applicable; do not infer that dependency solely from a
value-set name, code, or metadata classification. Do not hard-code value-set
names, codes, validation behavior, or default-value rules in this task
guidance.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Descriptive Flexfields` under `Channel Revenue Management`.
