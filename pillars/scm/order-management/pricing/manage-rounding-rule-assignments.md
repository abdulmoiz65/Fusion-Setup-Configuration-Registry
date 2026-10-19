---
task_code: "ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS"
task_name: "Manage Rounding Rule Assignments"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "pricingRoundingRuleAssignments"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Rounding Rule Assignments

## Setup Task Metadata

- Task name: `Manage Rounding Rule Assignments`
- Task code: `ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `pricingRoundingRuleAssignments`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader` using the `pricingRoundingRuleAssignments` business object.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Rounding Rule Assignments`
- Setup task code: `ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS`

## List Existing Rounding Rule Assignments

Use this read-only workflow when the request is to list or review the existing
currency-to-rounding-rule assignments. Route the collection GET through
`core.fusion-api.rest-api-client`; do not use the Data Loader import route.

```text
GET /fscmRestApi/resources/11.13.18.05/pricingRoundingRuleAssignments
```


Send `REST-Framework-Version: 9`, `onlyData=true`, `limit=500`, and `offset=0`.
Advance `offset` by the returned item count until `hasMore=false`. Retain only
the assignment fields returned by the resource:

- `RoundingRuleAssignmentId`
- `RoundingRuleId`
- `RoundingAssignmentTypeCode`
- `UnitCode`

For display names, resolve `RoundingRuleId` against the documented
`pricingRoundingRules` collection GET and resolve each `UnitCode` against the
documented `currenciesLOV` collection GET. Match `UnitCode` exactly to
`CurrencyCode`, retain the returned currency `Name` as `CurrencyName`, and
preserve the original `UnitCode` in the result. Do not infer rounding-rule
availability, setup-enabled status, or currency eligibility from this
assignment collection.
An empty terminal collection is a valid result; a failed or incomplete page is a
read failure and must not be reported as an empty assignment list.

Before creating or updating an assignment, validate the requested values through
the task's reference lookups:

1. Resolve the exact rounding-rule name through `pricingRoundingRules` and
   require both `ActiveFlag=true` and `SetupEnabledFlag=true`.
2. Resolve the exact currency code through `currenciesLOV` and require an
   enabled, monetary, currently effective currency.
3. Review the completed assignment collection for existing currency-to-rule
   assignments. Do not infer currency eligibility from that collection.

Only after these read-only validations pass may the Data Loader preparation and
approval workflow begin.




## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `pricingRoundingRuleAssignments` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "pricingRoundingRuleAssignments" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Rounding Rule Assignments` under `Pricing`.
