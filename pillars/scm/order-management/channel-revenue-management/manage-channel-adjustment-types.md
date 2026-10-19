---
task_code: "ORA_CJM_MANAGE_ADJ_TYPES"
task_name: "Manage Channel Adjustment Types"
parent_skill_id: "scm.order-management.channel-revenue-management"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "channelAdjustmentTypes"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Channel Adjustment Types

## Setup Task Metadata

- Task name: `Manage Channel Adjustment Types`
- Task code: `ORA_CJM_MANAGE_ADJ_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `channelAdjustmentTypes`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader` using channelAdjustmentTypes as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Adjustment Types`
- Setup task code: `ORA_CJM_MANAGE_ADJ_TYPES`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `channelAdjustmentTypes` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "channelAdjustmentTypes" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.



## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Adjustment Types` under `Channel Revenue Management`.
