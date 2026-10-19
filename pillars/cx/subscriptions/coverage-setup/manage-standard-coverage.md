---
task_code: "CUSTOM_MANAGE_STANDARD_COVERAGE"
task_name: "Manage Standard Coverage"
parent_skill_id: "cx.subscriptions.coverage-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Coverage Setup"
functional_area_code: "CUSTOM_COVERAGE_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "subscriptionCoverageHeaders"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Standard Coverage

## Setup Task Metadata

- Task name: `Manage Standard Coverage`
- Task code: `CUSTOM_MANAGE_STANDARD_COVERAGE`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `subscriptionCoverageHeaders`

## Standard Coverage Guidance

Use Standard Coverage templates to manage included and extended warranty
contracts for customers. Templates can support warranties for tangible or
intangible goods, including software and hardware; warranty pricing and
billing through one-time or recurring charges; entitlement tracking; and
warranty renewals.

Associate a Standard Coverage template in Oracle Product Information Management
with a Service item whose sales-product type is **Extended Warranty** or
**Included Warranty**. The template should define the service coverage model,
including:

- coverage times and days
- service-request reaction and resolution times
- discounted rates for work performed on covered products

Complete the documented Order Management parameter setup before setting up an
included or extended warranty. Use the existing Standard Coverage lookup and
design-readiness workflow for read-only review; it does not create or update
the template.

Source: [Oracle Subscription Management: Overview of Standard Coverage Templates](https://docs.oracle.com/en/cloud/saas/subscription-management/fasim/overview-of-standard-coverage-templates.html)

### Subscription Entitlements Procedure

For Subscription Entitlements, a Standard Coverage is a template of
entitlement rules that determines milestone timing and conditions. Create it in
Fusion as follows:

1. From **Subscription Configuration**, select **Entitlements Management >
   Standard Coverage**, then create a coverage with entitlement type
   **Subscription Entitlements**. If Service Contracts is in use, navigate to
   **Navigator > Contract Management > Contracts > Tasks > Standard Coverage**
   and select **Contracts Service Entitlements**.
2. Use **Actions > Add Entitlements** to configure the entitlement-rule
   structure. Severity is included as a condition; add Channel Type only when
   milestone behavior must differ by request channel.
3. Select the optional result columns needed for the milestones and thresholds
   being measured. A milestone that is not tracked must have its metric and
   warning-threshold columns omitted together.
4. Add each entitlement-rule row with its condition values and results:
   - Set a coverage schedule (calendar) for milestone due-date calculation.
   - Enter each tracked milestone metric in minutes.
   - Enter its warning threshold in minutes before expiry.
5. Save the coverage. Multiple rules are allowed when each service request can
   match exactly one rule.

Blank condition values can act as wildcards when the associated matrix class
allows nulls and treats them as wildcards. Do not define overlapping rows: if a
service request matches more than one row in the same coverage, no milestones
are applied. For example, a severity-only rule for **High** can coexist with
channel-specific rules for **Medium**, but a **Medium** wildcard cannot coexist
with **Medium / Phone** and **Medium / Email** rows.

## Create-Request Mapping

Treat the request phrase **Manage Standard Coverage** as the catalog task
**Manage Standard Coverage**. When the user requests a Standard Coverage XLSX and
provides its name and entitlement type, prepare the create-oriented source with
these fields:

| Data Loader field | Source |
|---|---|
| CoverageName | User-supplied Standard Coverage name |
| CoverageDescription | User-supplied description; otherwise use the CoverageName value |
| DynamicMatrixClassName | User-supplied entitlement type, for example Subscription Entitlements |
| StartDate | The current run date; format it by execution route as defined below |

### Date Format by Execution Route

| Route | `StartDate` format | Example for 13 August 2026 |
|---|---|---|
| Data Loader XLSX | `YYYY/MM/DD` | `2026/08/13` |
| REST payload | `YYYY-MM-DD` | `2026-08-13` |

For example, **Create a standard coverage "Gold Standard Coverage" of type
"Subscription Entitlements" using skill "Manage Standard Coverage" create
xlsx for data-loader** maps to:

```json
{
  "CoverageName": "Gold Standard Coverage",
  "CoverageDescription": "Gold Standard Coverage",
  "DynamicMatrixClassName": "Subscription Entitlements",
  "StartDate": "<current run date in YYYY/MM/DD format for Data Loader XLSX, or YYYY-MM-DD for REST>"
}
```

### Adjustment Prompt Mapping

For the exact request **Create a standard coverage "Gold Standard Coverage" of
type "Subscription Entitlements" with an adjustment for activity Install, Bill
type Material, of 2 percent discount on QP_AdjBasisForListPrc for "Depot
Repair" using skill "Manage Standard Coverage" create xlsx for data-loader**,
build this canonical create payload:

```json
{
  "CoverageName": "Platinum Coverage3",
  "CoverageDescription": "Gold Coverage Template",
  "DynamicMatrixClassName": "Subscription Entitlements",
  "StartDate": "2020-01-01",
  "CoverageChargeDiscounts": [
    {
      "ServiceActivityName": "Install",
      "BillingTypeMeaning": "Material",
      "AdjustmentTypeMeaning": "Discount percent",
      "AdjustmentAmount": 2,
      "PricingBasisName": "QP_AdjBasisforListPrc",
      "BusinessProcessMeaning": "Depot Repair"
    }
  ]
}
```

When this canonical payload is materialized into a Data Loader XLSX, convert
the `StartDate` value to `2020/01/01`; preserve `2020-01-01` for a REST
payload. The explicit prompt mapping takes precedence over the general
defaulting rules.

For example, a request for **Test Standard Coverage** of type **Subscription
Entitlements** should populate `CoverageName=Test Standard Coverage`,
`CoverageDescription=Test Standard Coverage`,
`DynamicMatrixClassName=Subscription Entitlements`, and the current run date
for `StartDate`.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `subscriptionCoverageHeaders` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionCoverageHeaders" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Standard Coverage` under `Coverage Setup`.
