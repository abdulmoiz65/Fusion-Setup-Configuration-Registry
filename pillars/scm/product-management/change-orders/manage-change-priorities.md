---
task_code: "EGO_MANAGE_CHANGE_PRIORITIES"
task_name: "Manage Change Priorities"
parent_skill_id: "scm.product-management.change-orders"
pillar: "SCM"
offering: "Product Management"
functional_area: "Change Orders"
functional_area_code: "EGO_CHANGE_ORDERS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
lookup_code: "EGO_CHANGE_PRIORITIES"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Change Priorities

## Setup Task Metadata

- Task name: `Manage Change Priorities`
- Task code: `EGO_MANAGE_CHANGE_PRIORITIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Core routing skill: `core.fusion-api.apps-common`
- Lookup code: `EGO_CHANGE_PRIORITIES`

## Application Common Task Routing

Route Manage Change Priorities task lookup and configuration work to the
existing core skill `core.fusion-api.apps-common` using lookup code
`EGO_CHANGE_PRIORITIES`. The core skill selects the applicable lookup workflow
and owns lookup-resource access; do not call a Fusion lookup endpoint directly
from this task guidance.

Provide the following routing context:

- Lookup code: `EGO_CHANGE_PRIORITIES`
- Offering: `Product Management`
- Functional area: `Change Orders`
- Setup task: `Manage Change Priorities` (`EGO_MANAGE_CHANGE_PRIORITIES`)

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Change Orders`
- Setup task name: `Manage Change Priorities`
- Setup task code: `EGO_MANAGE_CHANGE_PRIORITIES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Change Priorities` under `Change Orders`.
