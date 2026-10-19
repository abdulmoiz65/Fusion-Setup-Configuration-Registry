---
task_code: "ORA_CONFIGURE_ACTION_BAR_PARAMETERS"
task_name: "Configure Action Bar Parameters"
parent_skill_id: "cx.service.productivity-tools"
pillar: "CX"
offering: "Service"
functional_area: "Productivity Tools"
functional_area_code: "ORA_SVC_PRODUCTIVITY"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Configure Action Bar Parameters

## Setup Task Metadata

- Task name: `Configure Action Bar Parameters`
- Task code: `ORA_CONFIGURE_ACTION_BAR_PARAMETERS`
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

- Offering: `Service`
- Functional area / Setup Object: `Productivity Tools`
- Setup task name: `Configure Action Bar Parameters`
- Setup task code: `ORA_CONFIGURE_ACTION_BAR_PARAMETERS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Configure Action Bar Parameters` under `Productivity Tools`.
