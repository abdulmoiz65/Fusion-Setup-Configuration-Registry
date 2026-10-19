---
task_code: "CUSTOM_MANAGE_DEFAULT_COVERAGE"
task_name: "Manage Default Coverage"
parent_skill_id: "cx.subscriptions.coverage-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Coverage Setup"
functional_area_code: "CUSTOM_COVERAGE_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "subscriptionCoverageDefaults"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Default Coverage

## Setup Task Metadata

- Task name: `Manage Default Coverage`
- Task code: `CUSTOM_MANAGE_DEFAULT_COVERAGE`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `subscriptionCoverageDefaults`

## Default Coverage Guidance

Use default coverage to apply a standard coverage template globally or to a
specific customer. When a service request is evaluated for milestones, a
customer-level default coverage takes precedence over a matching global default
coverage for that customer.

## Lifecycle Route

Use `core.data-loader` for every Default Coverage create, update, and delete.
Do not construct a direct `crmRestApi` write and do not substitute the Default
Coverage page when a Data Loader preflight is blocked.

1. Resolve `subscriptionCoverageDefaults` from live Data Loader metadata and
   generate the operation-specific sample: omit `--operation` for create, use
   `--operation update` for update, or use `--operation delete` for delete.
2. Populate the generated workbook with the documented Default Level, Customer
   when the level is Customer, Standard Coverage, and effective dates. Use an
   empty end date only for an open-ended coverage.
3. Validate the source and let `core.data-loader` prepare its immutable upload
   artifact and approval preview. Its Run Book and approval gates are
   authoritative for submission.
4. Submit only the approved artifact through Data Loader. Do not retry an
   upload, initiation, or delete after a partial or uncertain outcome; use the
   documented Data Loader status route to reconcile it.

If live Data Loader metadata, source validation, or approval preflight fails,
stop with the reported diagnostic. Do not fall back to manual UI entry or a
direct REST mutation.

## Date Input Normalization

Normalize every unambiguous user-supplied date to `YYYY-MM-DD` before using it
in a UI instruction, validation result, or later approved execution artifact.
Interpret numeric dates in the user's stated regional convention when one is
known; otherwise, ask for clarification only when both day-first and
month-first interpretations are valid. For example, `01/02/2025` is normalized
to `2025-02-01` after the user confirms day-first interpretation. Do not invent
an end date when the user leaves it empty.

Do not create overlapping global and customer coverage records with ambiguous
business intent. When both can apply, document that the customer-level record
overrides the global record for milestone assignment.

## Retrieve Default Coverages

When asked to get the Default Coverages defined in the Fusion environment, use
the task-scoped `DEFCOV.LIST` read-only lookup in
`ora-resource/ora_reference_lookups.md`. It retrieves the collection from:

```text
{{baseUrl}}/crmRestApi/resources/latest/subscriptionCoverageDefaults
```

The equivalent trailing-slash collection path is also permitted:

```text
{{baseUrl}}/crmRestApi/resources/latest/subscriptionCoverageDefaults/
```

Use a GET request only; it is read-only.

Run the lookup only after the active implementation workflow and environment
gates are satisfied. Return the collection response, return an empty result
when no Default Coverages are defined, and report authorization, transport, or
Fusion API failures without retrying automatically.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Generate a Data Loader Sample

Use this workflow for every Default Coverage lifecycle operation.

1. Confirm that `subscriptionCoverageDefaults` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`. Omit
   `--operation` for a create, add `--operation update` for an update, or add
   `--operation delete` for a delete:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionCoverageDefaults" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the required
   Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Default Coverage` under `Coverage Setup`.
