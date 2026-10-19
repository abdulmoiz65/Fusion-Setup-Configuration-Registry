---
task_code: "ORA_CSE_MANAGE_ASSET_TRACKING_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Asset Tracking Descriptive Flexfields"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.maintenance-management"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Maintenance Management"
functional_area_code: "ORA_MNT_MGMT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
dff_codes:
  - "CSE_ASSETS"
  - "CSE_ASSET_QUALIFICATIONS"
  - "CSE_FAILURE_EVENTS"
  - "CSE_FAILURE_INSTANCES"
  - "CSE_FAILURE_ROOT_CAUSES"
route_skill: "core.fusion-api.apps-common"
---

# Manage Asset Tracking Descriptive Flexfields

## Setup Task Metadata

- Task name: `Manage Asset Tracking Descriptive Flexfields`
- Task code: `ORA_CSE_MANAGE_ASSET_TRACKING_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Descriptive flexfield codes:
  - `CSE_ASSETS`
  - `CSE_ASSET_QUALIFICATIONS`
  - `CSE_FAILURE_EVENTS`
  - `CSE_FAILURE_INSTANCES`
  - `CSE_FAILURE_ROOT_CAUSES`
- DFF route: `core.fusion-api.apps-common`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Maintenance Management`
- Setup task name: `Manage Asset Tracking Descriptive Flexfields`
- Setup task code: `ORA_CSE_MANAGE_ASSET_TRACKING_DESCRIPTIVE_FLEXFIELDS`
- Flexfield codes: `CSE_ASSETS`, `CSE_ASSET_QUALIFICATIONS`, `CSE_FAILURE_EVENTS`, `CSE_FAILURE_INSTANCES`, and `CSE_FAILURE_ROOT_CAUSES`

## Application Common Descriptive Flexfield Routing

Route descriptive-flexfield requests for this task through
`core.fusion-api.apps-common`. Identify the requested flexfield code
explicitly; do not implement OAuth or REST transport in this task metadata.

Use one of these flexfield codes, according to the requested maintenance object:

- `CSE_ASSETS`
- `CSE_ASSET_QUALIFICATIONS`
- `CSE_FAILURE_EVENTS`
- `CSE_FAILURE_INSTANCES`
- `CSE_FAILURE_ROOT_CAUSES`

| Requested maintenance object | DFF code |
| --- | --- |
| Asset Tracking assets | `CSE_ASSETS` |
| Asset qualifications | `CSE_ASSET_QUALIFICATIONS` |
| Failure events | `CSE_FAILURE_EVENTS` |
| Failure instances | `CSE_FAILURE_INSTANCES` |
| Failure root causes | `CSE_FAILURE_ROOT_CAUSES` |

Require the requester or calling workflow to supply exactly one DFF code. Do
not infer a code from a partial or ambiguous object name; request clarification
before a read, export, import, or change operation.

For a change request, use the core skill's read-before-write, preview, and
explicit approval gates. For DFF setup guidance, follow the descriptive
flexfield routing defined by `core.fusion-api.apps-common`.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Asset Tracking Descriptive Flexfields` under `Maintenance Management`.
