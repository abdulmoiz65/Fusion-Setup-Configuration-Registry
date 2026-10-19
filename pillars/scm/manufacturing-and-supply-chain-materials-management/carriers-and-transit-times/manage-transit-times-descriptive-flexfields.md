---
task_code: "ORA_RCS_MANAGE_TRANSIT_TIMES_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Transit Times Descriptive Flexfields"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.carriers-and-transit-times"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Carriers and Transit Times"
functional_area_code: "ORA_RCS_CARRIERS_TRANSIT_TIMES"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Transit Times Descriptive Flexfields

## Setup Task Metadata

- Task name: `Manage Transit Times Descriptive Flexfields`
- Task code: `ORA_RCS_MANAGE_TRANSIT_TIMES_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`

## Application Common Descriptive Flexfield Routing

Route every request for this task through `core.fusion-api.apps-common` as a
Descriptive Flexfield request. Pass the fixed DFF code
`WSH_TRANSIT_TIME_VALUES` with the task context for discovery, export, import,
and validation. Do not implement task-local OAuth, REST, CSV, or Data Loader
transport.

For configuration changes, use the core skill's read-before-write, preview,
and explicit-approval gates.

## CSV Export, Import, and Validation Workflow

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

## Usage

Use this metadata file when planning or validating `Manage Transit Times
Descriptive Flexfields` under `Carriers and Transit Times`.
