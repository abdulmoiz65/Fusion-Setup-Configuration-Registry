---
task_code: "CUSTOM_MANAGE_AVAILABILITY"
task_name: "Manage Availability"
parent_skill_id: "cx.subscriptions.coverage-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Coverage Setup"
functional_area_code: "CUSTOM_COVERAGE_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObjects:
  - "subscriptionCoverageSchedules"
  - "subscriptionCoverageExceptions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Availability

## Setup Task Metadata

- Task name: `Manage Availability`
- Task code: `CUSTOM_MANAGE_AVAILABILITY`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Objects: `subscriptionCoverageSchedules`, `subscriptionCoverageExceptions`

## Availability Setup Scope

Manage Availability has two distinct REST setup objects:

| Setup part | Business Object | Purpose |
|---|---|---|
| Availability schedules | `subscriptionCoverageSchedules` | Defines the availability schedule, including its time zone and associated exception when applicable. |
| Availability exceptions | `subscriptionCoverageExceptions` | Defines exception dates or periods associated with availability. |

Use the appropriate object for the setup part being prepared. Data Loader
metadata registers both objects: use `subscriptionCoverageSchedules` for
coverage schedules and `subscriptionCoverageExceptions` for coverage
exceptions. Prepare each object through its own source section; do not combine
schedule and exception rows into one object request.

## Create-Request Mapping

Treat the request phrase **Manage Availability** as the catalog task
**Manage Availability**. For a request to create an availability schedule with
an exception and interval, preserve the requested schedule, exception, date,
and availability values in this canonical payload.

For example, the request **Create a availability schedule "Winter Schedule"
exception name Holiday, having interval 2026-11-01 to 2027-03-31 and
availability "Daily 9:00 AM - 5:00 PM", using skill "Manage Availability"
create xlsx for data-loader** maps to:

```json
{
  "ScheduleName": "Winter Schedule",
  "ExceptionName": "Holiday",
  "SubscriptionCoverageInterval": [
    {
      "StartDate": "2026-11-01",
      "EndDate": "2027-03-31",
      "Availability": "Daily 9:00 AM - 5:00 PM"
    }
  ]
}
```

When materializing that payload into a Data Loader XLSX, convert interval dates
to `YYYY/MM/DD` (`2026/11/01` and `2027/03/31`). Preserve ISO `YYYY-MM-DD`
dates for REST payloads. Resolve any additional live-template-required fields,
such as `TimezoneCode`, before upload unless the user explicitly waives the
task-validation requirement.

For create-oriented schedule rows, **do not populate `ScheduleId`**. Leave the
same `ScheduleId` column blank in the `SubscriptionCoverageInterval` row.
Do not populate `IntervalId`; Fusion generates it. `SchedulePuid` remains the
local parent-child linkage value in the workbook.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `subscriptionCoverageSchedules`, `subscriptionCoverageExceptions` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionCoverageSchedules" \
     "subscriptionCoverageExceptions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Availability` under `Coverage Setup`.
