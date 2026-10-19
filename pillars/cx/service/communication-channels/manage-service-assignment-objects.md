---
task_code: "ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS"
task_name: "Manage Service Assignment Objects"
parent_skill_id: "cx.service.communication-channels"
pillar: "CX"
offering: "Service"
functional_area: "Communication Channels"
functional_area_code: "ORA_SVC_COMM_CHANNELS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Service Assignment Objects

## Setup Task Metadata

- Task name: `Manage Service Assignment Objects`
- Task code: `ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Communication Channels`
- Setup task name: `Manage Service Assignment Objects`
- Setup task code: `ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Service Assignment Objects` under `Communication Channels`.
