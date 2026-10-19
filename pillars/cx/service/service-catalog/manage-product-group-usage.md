---
task_code: "QSC_MANAGE_PRODUCT_GROUP_USAGE"
task_name: "Manage Product Group Usage"
parent_skill_id: "cx.service.service-catalog"
pillar: "CX"
offering: "Service"
functional_area: "Service Catalog"
functional_area_code: "ORA_SVC_SERVICE_CATALOG"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Product Group Usage

## Setup Task Metadata

- Task name: `Manage Product Group Usage`
- Task code: `QSC_MANAGE_PRODUCT_GROUP_USAGE`
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
- Functional area / Setup Object: `Service Catalog`
- Setup task name: `Manage Product Group Usage`
- Setup task code: `QSC_MANAGE_PRODUCT_GROUP_USAGE`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Product Group Usage` under `Service Catalog`.
