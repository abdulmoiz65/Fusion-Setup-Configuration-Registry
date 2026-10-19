---
task_code: "ORA_WIS_MANAGE_PRODUCTION_LOOKUPS"
task_name: "Manage Production Lookups"
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

# Manage Production Lookups

## Setup Task Metadata

- Task name: `Manage Production Lookups`
- Task code: `ORA_WIS_MANAGE_PRODUCTION_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Manufacturing Master Data`
- Setup task name: `Manage Production Lookups`
- Setup task code: `ORA_WIS_MANAGE_PRODUCTION_LOOKUPS`

## Application Common Lookup Routing

Route lookup read or maintenance requests for this task through
`core.fusion-api.apps-common`. Identify the requested standard lookup type
explicitly; do not implement OAuth or REST transport in this task metadata.

Use these lookup types:

- `ORA_WIS_RESOURCE_CLASS`
- `ORA_WIS_WC_RESOURCE_GROUP`
- `ORA_WIS_RESOURCE_ACTIVITY`
- `ORA_WIE_REASON_CODE`
- `ORA_WIE_WO_SUB_TYPE`

For a write, use the core skill's read-before-write, preview, and explicit
approval gates. For a lookup read, use the standard-lookup routing defined by
`core.fusion-api.apps-common`.


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Production Lookups` under `Manufacturing Master Data`.
