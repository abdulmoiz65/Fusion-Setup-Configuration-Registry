---
task_code: "CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET"
task_name: "Event Notification Rules and Templates Set"
parent_skill_id: "cx.subscriptions.foundation-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Foundation Setup"
functional_area_code: "CUSTOM_FOUNDATION_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "notificationTemplates"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Event Notification Rules and Templates Set

## Setup Task Metadata

- Task name: `Event Notification Rules and Templates Set`
- Task code: `CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `notificationTemplates`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `notificationTemplates` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "notificationTemplates" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Event Notification Rules and Templates Set` under `Foundation Setup`.
