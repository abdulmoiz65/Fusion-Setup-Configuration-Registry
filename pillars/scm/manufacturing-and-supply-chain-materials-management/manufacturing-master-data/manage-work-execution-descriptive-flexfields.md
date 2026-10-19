---
task_code: "ORA_WIP_WORK_EXECUTION_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Work Execution Descriptive Flexfields"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Manufacturing Master Data"
functional_area_code: "ORA_WIS_COMMON_MFG_WORK_SETUP"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Work Execution Descriptive Flexfields

## Setup Task Metadata

- Task name: `Manage Work Execution Descriptive Flexfields`
- Task code: `ORA_WIP_WORK_EXECUTION_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Manufacturing Master Data`
- Setup task name: `Manage Work Execution Descriptive Flexfields`
- Setup task code: `ORA_WIP_WORK_EXECUTION_DESCRIPTIVE_FLEXFIELDS`

## Application Common Descriptive Flexfield Routing

Route descriptive-flexfield requests for this task through
`core.fusion-api.apps-common`. Identify the requested flexfield code
explicitly; do not implement OAuth or REST transport in this task metadata.

Use these flexfield codes:

- `WIE_OPERATION_TRANSACTIONS`
- `WIE_RESOURCE_TRANSACTIONS`
- `WIE_WORK_ORDERS`
- `WIE_WORK_ORDER_GROUPS`
- `WIE_WO_OPERATIONS`
- `WIE_WO_OPERATION_MATERIALS`
- `WIE_WO_OPERATION_OUTPUTS`
- `WIE_WO_OPERATION_RESOURCES`
- `WIE_WO_OPERATION_RESOURCE_INSTANCES`

For a change request, use the core skill's read-before-write, preview, and
explicit approval gates. For DFF setup guidance, follow the descriptive
flexfield routing defined by `core.fusion-api.apps-common`.


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Work Execution Descriptive Flexfields` under `Manufacturing Master Data`.
