---
task_code: "ORA_MANAGE_OBJECT_LINK_TYPES"
task_name: "Manage Object Link Types"
parent_skill_id: "cx.service.service-request"
pillar: "CX"
offering: "Service"
functional_area: "Service Request"
functional_area_code: "ORA_SVC_SERVICE_REQUEST"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "objectLinkTypes"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Object Link Types

## Setup Task Metadata

- Task name: `Manage Object Link Types`
- Task code: `ORA_MANAGE_OBJECT_LINK_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Route to: `core.data-loader` after task-level export and validation

## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records. Use it only for read-only identity lookups and verification.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Service Request`
- Setup task name: `Manage Object Link Types`
- Setup task code: `ORA_MANAGE_OBJECT_LINK_TYPES`


## FSM Data Loader Package Requirements

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `objectLinkTypes` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "objectLinkTypes" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Object Link Types` under `Service Request`.
