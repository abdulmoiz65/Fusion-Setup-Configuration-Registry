---
task_code: "ORA_MANAGE_WORKFLOW_REJECT_REASON_LOOKUP"
task_name: "Manage Workflow Rejection Reasons"
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
lookup_code: "ORA_ACA_REJECTION_REASON"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Workflow Rejection Reasons

## Setup Task Metadata

- Task name: `Manage Workflow Rejection Reasons`
- Task code: `ORA_MANAGE_WORKFLOW_REJECT_REASON_LOOKUP`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Core routing skill: `core.fusion-api.apps-common`
- Lookup code: `ORA_ACA_REJECTION_REASON`

## Application Common Lookup Routing

Route Manage Workflow Rejection Reasons lookup work to
`core.fusion-api.apps-common` with lookup code
`ORA_ACA_REJECTION_REASON`. The core skill selects the applicable lookup
workflow and owns lookup-resource access; do not call a Fusion lookup endpoint
directly from this task guidance.

Provide the following routing context:

- Lookup code: `ORA_ACA_REJECTION_REASON`
- Offering: `Product Management`
- Functional area: `Change Orders`
- Setup task: `Manage Workflow Rejection Reasons` (`ORA_MANAGE_WORKFLOW_REJECT_REASON_LOOKUP`)

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Change Orders`
- Setup task name: `Manage Workflow Rejection Reasons`
- Setup task code: `ORA_MANAGE_WORKFLOW_REJECT_REASON_LOOKUP`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Workflow Rejection Reasons` under `Change Orders`.
