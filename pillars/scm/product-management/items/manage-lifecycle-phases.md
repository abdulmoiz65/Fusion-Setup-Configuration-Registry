---
task_code: "EGP_MANAGE_LIFECYCLE_PHASES"
task_name: "Manage Lifecycle Phases"
parent_skill_id: "scm.product-management.items"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Lifecycle Phases

## Setup Task Metadata

- Task name: `Manage Lifecycle Phases`
- Task code: `EGP_MANAGE_LIFECYCLE_PHASES`
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

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Lifecycle Phases`
- Setup task code: `EGP_MANAGE_LIFECYCLE_PHASES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Lifecycle Phases` under `Items`.
