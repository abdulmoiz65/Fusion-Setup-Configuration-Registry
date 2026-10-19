---
task_code: "ORA_CJM_MANAGE_CHANNEL_LOOKUPS"
task_name: "Manage Channel Lookups"
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

# Manage Channel Lookups

## Setup Task Metadata

- Task name: `Manage Channel Lookups`
- Task code: `ORA_CJM_MANAGE_CHANNEL_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Lookups`
- Setup task code: `ORA_CJM_MANAGE_CHANNEL_LOOKUPS`

## Shared Apps Common Lookup Route

Use `core.fusion-api.apps-common.lookups` for lookup classification, identity
resolution, and read-only lookup validation. That shared skill owns the
Application Common lookup resource contracts; do not duplicate its REST paths,
payloads, or authentication guidance here.

For an existing lookup type, a read-only REST response is not an FSM parent
baseline. An FSM import may proceed only when an export supplies the parent
carrier and its alternate-key context. In the assembled package, retain the
parent's current business fields but blank its system-audit fields; leave all
new child system-audit fields blank. If that carrier cannot be exported, use
the Fusion application UI for the lookup-code change rather than constructing a
parent row from REST fields.

This task supports setup-data import only through FSM with `core.data-loader`.
Do not use direct lookup REST create, update, delete, or bulk operations as an
import route for `ORA_CJM_MANAGE_CHANNEL_LOOKUPS`.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Lookups` under `Channel Revenue Management`.
