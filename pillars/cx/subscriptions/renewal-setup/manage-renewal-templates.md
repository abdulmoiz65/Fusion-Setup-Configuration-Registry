---
task_code: "CUSTOM_MANAGE_RENEWAL_TEMPLATES"
task_name: "Manage Renewal Templates"
parent_skill_id: "cx.subscriptions.renewal-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Renewal Setup"
functional_area_code: "CUSTOM_RENEWAL_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "renewalTemplates"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Renewal Templates

## Setup Task Metadata

- Task name: `Manage Renewal Templates`
- Task code: `CUSTOM_MANAGE_RENEWAL_TEMPLATES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `renewalTemplates`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `renewalTemplates` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "renewalTemplates" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Renewal Templates` under `Renewal Setup`.
