---
task_code: "ORA_CJM_MANAGE_CHANNEL_VALUE_SETS"
task_name: "Manage Channel Value Sets"
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

# Manage Channel Value Sets

## Setup Task Metadata

- Task name: `Manage Channel Value Sets`
- Task code: `ORA_CJM_MANAGE_CHANNEL_VALUE_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Value Set Routing

Route requests for `Manage Channel Value Sets` first to
`core.fusion-api.apps-common`, which selects
`core.fusion-api.apps-common.value-sets`.

The selected Apps Common workflow owns the supported direct REST behavior:

1. Read a value-set definition and its validation-table metadata.
2. Read, create, update, or delete supported child value-set values, subject
   to its preflight and immediate approval gate for writes.
3. Do not treat a root value-set definition as writable through this route;
   root definition create or update is unsupported until the core skill has a
   current supported contract.

`dataloader_import_mode: FSM` remains the catalog-derived route for an
explicit, approved task-level CSV artifact. It does not replace Apps Common as
the primary route, and it must not be used as an unverified fallback for a
direct REST request.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Value Sets`
- Setup task code: `ORA_CJM_MANAGE_CHANNEL_VALUE_SETS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Value Sets` under `Channel Revenue Management`.
