---
task_code: "ORA_RCS_MANAGE_ITEM_ORG_VALUE_SETS"
task_name: "Manage Item Organizations Value Sets"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.facilities"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Facilities"
functional_area_code: "ORA_RCS_FACILITIES"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Item Organizations Value Sets

## Setup Task Metadata

- Task name: `Manage Item Organizations Value Sets`
- Task code: `ORA_RCS_MANAGE_ITEM_ORG_VALUE_SETS`
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

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Facilities`
- Setup task name: `Manage Item Organizations Value Sets`
- Setup task code: `ORA_RCS_MANAGE_ITEM_ORG_VALUE_SETS`

## Value Set Route

Route every value-set request for this task to
`core.fusion-api.apps-common`, which selects its `value-sets` child skill.
The value set is user-defined: require the caller to provide the exact
`value_set_code` before the handoff. Do not derive it from this setup-task
code or task name.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Item Organizations Value Sets` under `Facilities`.
