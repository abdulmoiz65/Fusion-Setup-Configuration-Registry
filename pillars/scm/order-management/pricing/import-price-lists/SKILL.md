---
skill_id: "scm.order-management.pricing.import-price-lists"
name: "Import Price Lists Setup Task Guidance"
description: "Prepares, validates, and submits Import Price Lists FBDI packages, using the Oracle workbook macro or an in-skill spreadsheet fallback to generate a ZIP from a populated Price Lists XLSM, then offers an optional customer-pricing-definition setup verification."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
task_code: "CUSTOM_IMPORT_PRICE_LISTS"
task_name: "Import Price Lists"
parent_skill_id: "scm.order-management.pricing"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "FBDI"
businessObject: "Price List"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "SCM order management pillar team"
version: "0.1.4"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "customer_price_list_source"
  - "target_environment"
  - "post_import_setup_test_option"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "generated_fbdi_zip"
  - "fbdi_preview"
  - "fbdi_process_result"
  - "post_import_setup_test_decision"
  - "post_import_setup_test_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/pricing/import-price-lists/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/pricing/import-price-lists/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Runs the approved Oracle workbook macro on a disposable copy to create a local Price Lists FBDI ZIP when requested."
  - "When the macro is unavailable or fails, reads a disposable workbook copy and creates equivalent local CSV and ZIP artifacts under this skill's fallback contract."
  - "Delegates approved UCM upload and data-load initiation to core.data-loader."
  - "After a successful import, can perform an explicitly selected setup verification through the registered customerPricingDefinitions Data Loader workflow."
required_privileges:
  - "Fusion privileges required by core.data-loader for live Price List FBDI validation and submission."
  - "Fusion privileges required by core.data-loader to create or update a customer pricing definition when the optional setup verification is selected."
---

# Import Price Lists Setup Task Guidance

## Purpose

Prepare and validate Price Lists FBDI packages for `Import Price Lists` under
`Pricing`. Prefer the Oracle workbook's Generate CSV File macro for XLSM-to-ZIP
creation. When that macro cannot produce a valid ZIP, use the fallback contract
in this file. Delegate live upload, initiation, status, and diagnostics to
`core.data-loader`.

## Setup Task Skill Contract

- task_code: `CUSTOM_IMPORT_PRICE_LISTS`
- task_name: `Import Price Lists`
- parent_skill_id: `scm.order-management.pricing`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Pricing`
- functional_area_code: `ORA_FOM_PRICING`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `FBDI`
- businessObject: `Price List`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Import Price Lists` under `Pricing`.

## Setup Task Metadata

- Task name: `Import Price Lists`
- Task code: `CUSTOM_IMPORT_PRICE_LISTS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `FBDI`
- Business Object: `Price List`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## FBDI Data Loader Workflow

`dataloader_import_mode` is `FBDI`. Route Price Lists FBDI package validation,
approval, upload, initiation, status, and diagnostics through
`core.data-loader`. Do not invoke a product-specific FBDI adapter directly from
this pillar skill; Data Loader selects the supported adapter after validating
the task context and exact immutable ZIP.

The catalog's `CSVExportImportSupportedFlag: N` blocks the generic FSM
setup-task CSV route; it does not replace the explicitly selected Price Lists
FBDI route. Before a live import, require Data Loader source review, applicable
Task Hook validation, an immutable preview, and the approval defined by
`core.data-loader`. Do not retry an upload or import automatically after a
failure, timeout, or uncertain response.

### Template authority and drift

Use Oracle's current **Price Lists Batch** FBDI page as the authority for
`PriceListsImportBatchTemplate.xlsm`, its interface tables, scheduled process,
and UCM account. The current 26C source is
`https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/oefsc/pricelistsbatch-3167.html`;
check for a newer Oracle Cloud release at execution time instead of assuming
26C remains current.

Treat the current Oracle workbook and its Generate CSV File macro as the
preferred authority for worksheet-to-CSV conversion. If the macro is
unavailable, unsupported, or fails before producing a valid ZIP, apply the
fallback conversion contract below directly from this `SKILL.md`. Do not add or
use a task-specific converter script, converter module, or separate processing
resource. Before using a generated ZIP, require `core.data-loader` live FBDI
metadata to resolve every generated member to the single `Price List` business
object and its UCM account. Treat any difference in template identity,
generated member names, business object, or UCM account as template drift and
stop before upload.

### Preflight and error handling

Before generating or validating a ZIP, read
`ora-resource/ora_input_validation.md` and
`ora-resource/ora_error_handling.md`. Apply these local preflight checks before
creating a file:

1. Confirm the source is the intended readable `.xlsm`, the selected task is
   `CUSTOM_IMPORT_PRICE_LISTS`, and any requested live operation identifies one
   target environment.
2. Use a disposable workbook copy and select a new ZIP path in the user-approved
   source location or a controlled transient directory; never overwrite an
   existing artifact. Obtain explicit approval before running workbook macros.
3. Confirm the workbook is the current Oracle Price Lists Batch template. Use
   its Generate CSV File macro when a trusted Excel runtime is available and
   macro execution is approved; otherwise select the fallback contract below.
4. After either generation path, reopen and validate the exact ZIP before
   passing it to Task Hook and `core.data-loader`. Any workbook or ZIP change
   restarts these checks and invalidates the earlier preview or approval.

Fail before upload on an input, mapping, template-drift, output-path, or archive
validation error. Report only the failure category and the workbook sheet/cell
location needed to correct it. Never print or persist workbook row values,
credentials, tokens, authorization headers, customer payloads, or generated CSV
contents. Delegate Fusion-side redaction, diagnostics, timeout handling, and
retry controls to `core.data-loader`.

For a supplied Price Lists XLSM, run the Generate CSV File macro only with the
user's explicit approval and a trusted Excel runtime. Operate on a disposable
copy and preserve the supplied workbook unchanged. If Excel or macro execution
is unavailable, unsupported, or fails before producing a valid ZIP, close the
disposable workbook and use the fallback below. A macro failure does not
authorize a second macro attempt unless the user approves it.

### Approval-status decision

Before generating an immutable ZIP, inspect each `QP_PRICE_LISTS_INT` header
row using the template's `STATUS_CODE` and `SOURCE_PRICE_LIST_ID` fields. When
a header has either a supplied matching `QP_PRICE_LIST_SETS_INT` access-set row
or a fallback-generated `COMMON` association, the proposed status for this
import is `APPROVED`. Ask the user to confirm that proposal before setting an
`IN_PROGRESS` or blank header to `APPROVED`. Identify the affected workbook
sheet and row count, but never disclose source cell values in the prompt.

The status decision is separate from FBDI submission. On a clear confirmation,
change only the matching `STATUS_CODE` values in the disposable workbook copy
or fallback export data, then generate a new ZIP and restart source review,
Task Hook validation, immutable preview, and the separate `core.data-loader`
upload approval. On a decline or no response, preserve `IN_PROGRESS` or blank
status and continue only with the normal validated-upload workflow. Never
change an already `APPROVED` or other nonblank status; never approve a header
that has no matching access-set association; and never treat status-change
confirmation as approval to upload or initiate a load.

### Preparation defaults

When preparing a new Price List import, default a blank or absent header
`PRICE_LIST_TYPE_CODE` to `SEGMENT`, and default a blank or absent item
`LINE_TYPE_CODE` to `ORA_BUY`. Preserve any supplied nonblank value. Apply a
default only in the disposable workbook copy or fallback export data; never
change the supplied workbook. Record only the affected sheet and row count,
not source values. Applying either default is a data transformation, so create
and validate a new ZIP and restart source review, Task Hook validation,
immutable preview, and the separate Data Loader upload approval.

### In-skill XLSM conversion fallback

Use an available general-purpose spreadsheet reader and CSV/ZIP writer at
runtime. Do not add a task-local script, converter module, hard-coded workbook
copy, or new processing resource. Treat the current workbook as the schema for
column order and data types, and apply all of these rules:

1. Recognize a Price Lists data sheet only when cells `A1:A4` contain exactly
   `Name`, `Description`, `Data Type`, and `Technical Name`, in that order.
   Column A and rows 1 through 4 are workbook metadata and never become CSV
   fields or data rows.
2. Use the nonempty `Technical Name` cells on row 4, starting at column B and
   ending at the last nonempty technical-name cell, as the complete ordered
   export schema. Do not remove, insert, or reorder fields, including unused
   optional fields.
3. Treat access-set data as optional input. When `QP_PRICE_LIST_SETS_INT` has
   no populated data rows, generate one `COMMON` access-set row for every
   populated `QP_PRICE_LISTS_INT` header row in the fallback ZIP only; never
   alter the supplied workbook. Use the template's technical-name columns and
   preserve their order. Set `OPERATION_CODE` to `CREATE`, copy
   `SOURCE_PRICE_LIST_ID` and (when present) `BATCH_NAME` from the related
   header, set `SOURCE_PRICE_LIST_SET_ID` to the deterministic value
   `COMMON_<SOURCE_PRICE_LIST_ID>`, and set `SET_CODE` to `COMMON`. Leave
   every other access-set field empty. If either sheet is unrecognized, a
   populated header lacks `SOURCE_PRICE_LIST_ID`, or a required technical-name
   column is absent, fail as input validation or template drift rather than
   generating a partial association. If any access-set row is supplied,
   preserve every supplied row and do not add, merge, replace, or infer a
   `COMMON` row.
4. Data begins on row 5. Ignore only fully empty trailing rows. If a fully empty
   row is followed by a later nonempty row within the data region, fail with the
   sheet and row location instead of silently discarding the gap. Omit an
   otherwise recognized sheet when it contains no data rows.
5. Resolve each populated sheet's exact CSV filename from the current
   workbook's own export definition, such as its macro output declaration or
   workbook-maintained sheet-to-file configuration. When the workbook does not
   expose that definition, use this explicit fallback mapping:

   | Workbook sheet | CSV filename |
   | --- | --- |
   | `QP_PRICE_LISTS_INT` | `PriceListsHeaders.csv` |
   | `QP_PRICE_LIST_SETS_INT` | `PriceListsSets.csv` |
   | `QP_PRICE_LIST_ITEMS_INT` | `PriceListsItems.csv` |
   | `QP_PRICE_LIST_CHARGES_INT` | `PriceListsCharges.csv` |
   | `QP_TIER_HEADERS_INT` | `TierHeaders.csv` |
   | `QP_TIER_LINES_INT` | `TierLines.csv` |
   | `QP_MATRIX_DIMENSIONS_INT` | `MatrixDimensionsInterface.csv` |
   | `QP_MATRIX_RULES_INT` | `MatrixRulesInterface.csv` |
   | `QP_PL_COVERED_ITEMS_INT` | `PriceListsCoveredItems.csv` |
   | `QP_PL_COMP_ITEMS_INT` | `PriceListsCompItems.csv` |
   | `QP_RATE_PLANS_INT` | `PriceListsRatePlans.csv` |

   Prefer a workbook-declared filename when available and require it to match
   live FBDI metadata. For a newly added populated sheet that is not listed
   above, use its workbook-declared filename automatically. If neither the
   workbook nor this table provides one unambiguous filename, treat the sheet
   as template drift and stop rather than guessing.

6. Emit headerless CSV data only. Never emit instruction rows, display names,
   descriptions, data-type rows, technical-name rows, or column A. Preserve the
   full field width on every row, including trailing empty fields.
7. For columns identified as dates or date-times by the workbook's `Data Type`
   row, convert Excel date values and valid textual date values to
   `YYYY/MM/DD hh:mm:ss`, using a zero-padded 24-hour value for `hh`. Fail on a
   populated date value that cannot be parsed unambiguously; do not substitute
   a locale-dependent interpretation. Apply only the explicit transformations
   in **Approval-status decision** and **Preparation defaults**. Preserve every
   other text and numeric value without guessing or applying additional
   business defaults.
8. Write UTF-8 comma-delimited CSV using RFC 4180 quoting and CRLF line endings.
   Add only populated CSV members at the ZIP root, in workbook worksheet order.
   Do not rely on filesystem or alphabetical order.
9. Reopen the ZIP and fail closed unless it is readable, contains root-level
   expected members only, has no duplicate or unsafe paths, preserves member
   order, and every row has the exact schema width. Recheck row counts, date
   formatting, and trailing empty fields. Bind the ZIP basename, byte size,
   ordered member list, row counts, and SHA-256 digest to the immutable preview.

Fallback diagnostics may contain only the failure category and sheet/cell
location required for correction. Do not include raw cell values or generated
CSV content. Successful local fallback generation authorizes neither UCM upload
nor import initiation.

Treat a macro-generated or fallback-generated ZIP as a newly generated
artifact. Reopen and validate it, then run Data Loader source review and Task
Hook validation for its exact bytes. Local generation does not authorize UCM
upload or import initiation.

## Optional Post-Import Setup Verification

Only after `core.data-loader` reports that the exact Price Lists FBDI import
has completed successfully, ask the user:

> Do you want to perform a setup verification by making the imported price
> list available through a global customer pricing definition? Choose **skip**,
> **use an existing global definition**, or **create a global definition**.

Do not ask this question after a failed, timed-out, uncertain, or unverified
import result. Treat **skip** or no answer as a completed import with no
customer-pricing-definition change, and record that decision in the validation
result.

Oracle Pricing associates a customer pricing definition with a pricing
strategy; the strategy references the imported price list. Do not represent or
attempt this verification as a direct Price List-to-customer-pricing-definition
assignment. Use this sequence when the user selects either verification option:

1. Confirm the successful import result identifies the intended price list and
   target environment. If the imported list cannot be identified unambiguously,
   stop and ask for a corrected test scope.
2. Perform a read-only lookup through `core.fusion-api.rest-api-client` for an
   existing global customer pricing definition. A global definition is one
   whose `AssignmentTypeCode` is `ORA_QP_ALL`. Require exactly one user-selected
   match before reusing it; do not select among multiple matches.
3. Resolve or prepare the pricing strategy that references the imported price
   list. If no suitable strategy exists, stop and report that the requested
   verification needs a separately scoped pricing-strategy setup; do not create
   or alter a strategy as an implicit side effect of this test.
4. If the user chose **use an existing global definition**, associate the
   resolved strategy with that exact global definition. If the user chose
   **create a global definition**, prepare a new uniquely named global
   definition with `AssignmentTypeCode: ORA_QP_ALL`, then associate the
   resolved strategy. Never overwrite an existing definition or association.
5. Route customer-pricing-definition preparation, immutable preview, approval,
   execution, status, and diagnostics through `core.data-loader` for
   `customerPricingDefinitions`, using the rules in
   `../manage-customer-pricing-definitions.md` and the Pricing functional-area
   `ora-resource` guidance. Obtain the core workflow's approval immediately
   before any create or update.
6. Record the selected option, reuse/create result, resolved definition and
   strategy identities, and redacted validation outcome in
   `post_import_setup_test_result`. Do not record customer data, access tokens,
   or raw request payloads.

The optional verification proves only that the imported list is available to
the selected pricing strategy and global customer-pricing-definition setup. A
transaction-pricing test requires a separately scoped test order and is not
implied by this import workflow.

## Behavioral Verification

Use [tests/golden-scenarios.md](tests/golden-scenarios.md) to review the
fallback contract after any change to workbook recognition, field extraction,
date handling, CSV serialization, filename resolution, or ZIP validation.
Exercise the scenarios with synthetic data in a transient location and record
each result. Do not use a customer workbook as test evidence, create a
task-specific converter solely for the tests, or perform a live Fusion upload.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `customer_price_list_source`
- `target_environment`
- `post_import_setup_test_option`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `generated_fbdi_zip`
- `fbdi_preview`
- `fbdi_process_result`
- `post_import_setup_test_decision`
- `post_import_setup_test_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.order-management.pricing` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
