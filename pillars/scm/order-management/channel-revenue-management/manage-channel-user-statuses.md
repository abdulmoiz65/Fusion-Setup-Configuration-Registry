---
task_code: "ORA_CJM_MANAGE_CHANNEL_USER_STATUSES"
task_name: "Manage Channel User Statuses"
parent_skill_id: "scm.order-management.channel-revenue-management"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "channelUserStatuses"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Channel User Statuses

## Setup Task Metadata

- Task name: `Manage Channel User Statuses`
- Task code: `ORA_CJM_MANAGE_CHANNEL_USER_STATUSES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `channelUserStatuses`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `channelUserStatuses` as the business object.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel User Statuses`
- Setup task code: `ORA_CJM_MANAGE_CHANNEL_USER_STATUSES`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task's business object.

1. Confirm that `channelUserStatuses` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "channelUserStatuses" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated editable sample, attribute-details workbook, and key-fields workbook together.
4. Review the generated headers and key fields before preparing source data. Metadata retrieval is read-only and does not upload or import data.
5. Use the editable workbook as the starting point for Data Loader preparation and approval.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel User Statuses` under `Channel Revenue Management`.
