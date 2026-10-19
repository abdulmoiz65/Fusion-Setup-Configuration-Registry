---
task_code: "CUSTOM_MANAGE_BALANCE_CODES"
task_name: "Manage Balance Codes"
parent_skill_id: "cx.subscriptions.usage-rating-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Usage Rating Setup"
functional_area_code: "CUSTOM_USAGE_RATING_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObjects:
  - "subscriptionBalanceCodes"
  - "subscriptionBalanceCodes_activate"
  - "subscriptionBalanceCodes_deActivate"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Balance Codes

## Setup Task Metadata

- Task name: `Manage Balance Codes`
- Task code: `CUSTOM_MANAGE_BALANCE_CODES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Objects: `subscriptionBalanceCodes`, `subscriptionBalanceCodes_activate`, `subscriptionBalanceCodes_deActivate`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.

## Default Read-Only List Presentation

When a user asks to list Balance Codes without supplying a `BalanceCode`, use the
declared `list_balance_codes` lookup. Unless the user explicitly supplies a
different `fields` selection, return each row with `BalanceCode`,
`BalanceCodeDescription`, `BalanceCodeStatus`, `BalanceCodeType`, and the
applicable `BalanceUnitofMeasureCode` or `BalanceCurrencyCode`.

Always include `BalanceCodeStatus` in this default presentation; do not infer
that a listed code is active. Include the returned `count`, `hasMore`, and
`offset` metadata so callers can determine whether another page is required.

## Balance-Code Activation Route

When a user asks to activate a balance code, use the registered Data Loader business object `subscriptionBalanceCodes_activate`.

1. Use the declared read-only `find_balance_code_by_exact_code` lookup to resolve exactly one `BalanceCode` and its current `BalanceCodeStatus`. Stop if the code is absent, ambiguous, or already active.
2. Generate the current live `subscriptionBalanceCodes_activate` sample through `core.data-loader`; use its exact headers, required values, and operation shape. Do not substitute a direct REST activation call or a status `PATCH`.
3. Prepare and validate the activation source with the resolved balance-code identity. Complete `core.data-loader` immutable-preview and Task Hook validation where applicable.
4. Obtain explicit approval for the exact archive immediately before upload and initiation. Do not retry a failed or uncertain load without a newly validated archive and approval.
5. Verify the resulting status through the declared read-only lookup and report the result. Preserve Data Loader diagnostics if processing fails.

## Balance-Code Deactivation Route

When a user asks to deactivate a balance code, use the registered Data Loader business object `subscriptionBalanceCodes_deActivate`.

1. Use the declared read-only `find_balance_code_by_exact_code` lookup to resolve exactly one `BalanceCode` and its current `BalanceCodeStatus`. Stop if the code is absent, ambiguous, or already inactive.
2. Generate the current live `subscriptionBalanceCodes_deActivate` sample through `core.data-loader`; use its exact headers, required values, and operation shape. Do not substitute a direct REST deactivation call or a status `PATCH`.
3. Prepare and validate the deactivation source with the resolved balance-code identity. Complete `core.data-loader` immutable-preview and Task Hook validation where applicable.
4. Obtain explicit approval for the exact archive immediately before upload and initiation. Do not retry a failed or uncertain load without a newly validated archive and approval.
5. Verify the resulting status through the declared read-only lookup and report the result. Preserve Data Loader diagnostics if processing fails.

## Create Route Selection

For balance-code creation, use Fusion Data Loader by default. Use REST only when
the user explicitly requests creation **via REST**.

| Create request | Selected route | Required handling |
| --- | --- | --- |
| Create a balance code, with no route specified | Fusion Data Loader | Validate that the exact balance code is absent, resolve the requested UOM and charge-definition codes, then generate and validate the local `subscriptionBalanceCodes` workbook through `core.data-loader`. Do not upload or import without the separate immutable-preview and explicit upload approval. |
| Create a balance code **via Data Loader** | Fusion Data Loader | Use the same Data Loader workflow. |
| Create a balance code **via REST** | Direct Fusion REST | Use the REST create route below. |

The default route creates only a local source artifact. It does not authorize a
Fusion create, upload, or import.

## REST Create Route

When a request explicitly says to create a balance code **via REST**, use `core.fusion-api.rest-api-client` rather than Data Loader. Before preparing the preview, resolve each named charge definition with `resolve_charge_definition_code_by_exact_name` and confirm that the requested `BalanceCode` is absent through `find_balance_code_by_exact_code`. Do not infer a charge code or overwrite an existing balance code.

For a quantity balance code, use `BalanceCodeType: "ORA_OSS_QUANTITY"`, include `BalanceUnitofMeasureCode`, and send each resolved charge in `balanceCodeCharges` with its `ChargeDefinitionCode`. Use a deterministic child `BalanceCodeChargeNumber` in the form `<BalanceCode>-BACC-<sequence>`.

Show the exact environment, `POST` endpoint, and complete payload before writing. Obtain explicit approval immediately before the `POST`; submit once only, do not retry automatically, and verify the created balance code through the declared read-only lookup.

## Balance Type and Charge-Association Requirements

Choose the balance type from the business measure before creating a source or payload:

| Business measure | Required design | Validation requirement |
| --- | --- | --- |
| Count or capacity, such as sends, units, credits, or workflow slots | Quantity balance | Use `ORA_OSS_QUANTITY` and resolve the exact target-environment UOM code. |
| Monetary value | Amount balance | Resolve the target currency and use the amount-balance contract confirmed by current Fusion metadata or Oracle guidance. |

For each balance code, resolve every associated charge definition by exact display name. Persist each returned `ChargeDefinitionCode` as a separate `balanceCodeCharges` child row with a deterministic `BalanceCodeChargeNumber`. Do not infer a UOM, currency, charge-definition code, or whether a capacity measure should be decremented; document the business rule before preparation.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `subscriptionBalanceCodes`, `subscriptionBalanceCodes_activate`, `subscriptionBalanceCodes_deActivate` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionBalanceCodes" \
     "subscriptionBalanceCodes_activate" \
     "subscriptionBalanceCodes_deActivate" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Quantity Balance Code Example

For a quantity balance code, provide the balance-code identity, description, quantity type, and UOM. Resolve the associated charge by its exact display name before preparing the child row; never infer the `ChargeDefinitionCode` from the display name.

```json
{
  "BalanceCode": "MINUTES_BALANCE_CODE",
  "BalanceCodeDescription": "Minutes Balance Code",
  "BalanceCodeType": "ORA_OSS_QUANTITY",
  "BalanceUnitofMeasureCode": "MNS",
  "balanceCodeCharges": [
    {
      "BalanceCodeChargeNumber": "MINUTES_BALANCE_CODE-BACC-1",
      "ChargeDefinitionCode": "USAGE_SALE_PRICE"
    }
  ]
}
```

When preparing this example for Data Loader, use the `resolve_charge_definition_code_by_exact_name` lookup in `ora-resource/ora_reference_lookups.md` with `ChargeDefinitionName` set to `Usage Sale Price`. Continue only when it returns exactly one record whose `Name` is `Usage Sale Price` and whose `ChargeDefinitionCode` is nonblank; place that returned code in the `balanceCodeCharges` child row.

## Reuse or Create a Minutes Balance Code Data Loader Workbook

Interpret a customer request such as _“Create a balance code based on Quantity called ‘Minutes Balance Code’ with UOM MNS with a Usage Sale Price charge”_ as this exact requested configuration:

| Field | Required value |
|---|---|
| `BalanceCode` | `MINUTES_BALANCE_CODE` |
| `BalanceCodeDescription` | `Minutes Balance Code` |
| `BalanceCodeType` | `ORA_OSS_QUANTITY` |
| `BalanceUnitofMeasureCode` | `MNS` |
| Charge display name | `Usage Sale Price` |

Before generating anything, search the selected project's durable artifacts for a Data Loader XLSX that is both:

- for the `subscriptionBalanceCodes` business object; and
- an exact match for the configuration above, including its resolved `Usage Sale Price` `ChargeDefinitionCode` child row.

Do not treat a filename, an unvalidated workbook, or a workbook from another project as a match. If one exact, validated workbook exists, provide links to that workbook and its companion attribute-details and key-fields workbooks when available. Do not create another workbook at this point. Ask the customer whether they explicitly want a **new** workbook; only an affirmative response authorizes fresh workbook generation.

When preparing a new workbook, first use the read-only `find_balance_code_by_exact_code` lookup with `BalanceCode=MINUTES_BALANCE_CODE`. If it finds a record, provide the existing balance-code details and its associated charges through `list_balance_code_charges`; do not prepare a duplicate-create workbook. A customer may still request a fresh **workbook** for a supported update workflow, but a request to create the same balance code is an overwrite conflict and requires a distinct balance-code identifier and confirmation before a new create source can be prepared.

If no matching workbook or balance code exists, or the customer explicitly asks for a new workbook for a supported non-create workflow, use `core.data-loader` to generate the current `subscriptionBalanceCodes` XLSX trio in the selected project's artifact directory. Obtain the current template and headers from live Data Loader metadata, resolve `Usage Sale Price` with `resolve_charge_definition_code_by_exact_name`, and populate the parent and `balanceCodeCharges` child rows with the exact values above and the returned charge-definition code. Keep the generated XLSX trio together and report direct links to all three files.

This workflow creates only a local Data Loader source artifact. It does not authorize upload, initiation, or creation of the balance code in Fusion. Before any later import, `core.data-loader` must complete its source review, immutable-preview, Task Hook validation where applicable, and separate explicit upload approval.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Balance Codes` under `Usage Rating Setup`.
