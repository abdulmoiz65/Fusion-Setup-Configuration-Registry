---
task_code: "QSC_MANAGE_PRODUCT_GROUPS"
task_name: "Manage Product Groups"
parent_skill_id: "cx.service.service-catalog"
pillar: "CX"
offering: "Service"
functional_area: "Service Catalog"
functional_area_code: "ORA_SVC_SERVICE_CATALOG"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Product Groups

## Setup Task Metadata

- Task name: `Manage Product Groups`
- Task code: `QSC_MANAGE_PRODUCT_GROUPS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Product Groups` under `Service Catalog`.
