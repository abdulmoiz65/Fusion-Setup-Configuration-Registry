---
task_code: "CUSTOM_CUSTOMER_PRICING_DEFINITIONS"
task_name: "Manage Customer Pricing Definitions"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "customerPricingDefinitions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Customer Pricing Definitions

## Setup Task Metadata

- Task name: `Manage Customer Pricing Definitions`
- Task code: `CUSTOM_CUSTOMER_PRICING_DEFINITIONS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `customerPricingDefinitions`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.

## Assignment Type Code Defaulting

During customer-pricing-definition source preparation, set
`AssignmentTypeCode` to `ORA_QP_ALL` when the field is omitted. Preserve an
explicitly supplied assignment type; this default must never overwrite a
user-provided value.

Validate the resulting assignment type through the registered
`customerPricingDefinitions` Data Loader source-review workflow against lookup
type `ORA_QP_CUST_PRICING_ASSN_TYPES`. If `ORA_QP_ALL` is unavailable or the
supplied code is not valid for that lookup type, stop before preview and correct
the source. Rebuild the immutable source artifact after applying the default.

## Global Customer Pricing Definition Name Defaulting

When `Name` is omitted and the resulting `AssignmentTypeCode` is `ORA_QP_ALL`,
set the name to `Customer Pricing Definition for Validation`. Preserve an
explicitly supplied name; this default must never overwrite a user-provided
value.

For any assignment type other than `ORA_QP_ALL`, a name remains required. Apply
the name default before the global-assignment uniqueness lookup, then rebuild
the immutable source artifact before preview.

## Global Assignment Type Uniqueness

Allow only one customer pricing definition whose `AssignmentTypeCode` is
`ORA_QP_ALL` in a target environment. Before preparing a create or update with
that assignment type, use `core.fusion-api.rest-api-client` to perform the
registered read-only `customerPricingDefinitions` lookup.

For a create, if the lookup finds exactly one existing global definition,
prompt the user to use that customer pricing definition instead. If accepted,
return the resolved existing definition for downstream use without creating,
updating, or repurposing it. If declined, stop without a mutation.

For an update, exclude the current definition's resolved primary identifier and
require that no other definition has that value. Multiple results, an ambiguous
result, or a lookup failure block preview; do not create, overwrite, or
repurpose a global definition. Rebuild the immutable source artifact only after
the uniqueness check or accepted reuse decision passes.

## Specific Customer or Group Recommendation

When a request is for a specific customer or customer group rather than a
global assignment, first suggest using the existing customer pricing definition
whose `AssignmentTypeCode` is `ORA_QP_ALL` when it meets the requested pricing
need.

Ask whether the user wants to reuse that global definition. If accepted, use
`core.fusion-api.rest-api-client` to resolve exactly one existing global
definition and return it for downstream use without creating or updating any
customer pricing definition. If the user declines, retain the requested
customer- or group-specific scope and continue through the normal validated
Data Loader workflow. Do not automatically convert a specific request to a
global assignment, and do not suggest reuse when the global lookup is missing,
ambiguous, or fails.

## Currency Code Defaulting

During customer-pricing-definition source preparation, set `CurrencyCode` to
`USD` when the field is omitted. Preserve an explicitly supplied currency code;
this default must never overwrite a user-provided value.

Apply the default only when the registered `customerPricingDefinitions` Data
Loader sample for the target environment includes `CurrencyCode`. Use the
sample's exact field/header name and rebuild the immutable source artifact
after defaulting. If the registered sample does not expose `CurrencyCode`, stop
before preview rather than adding an unsupported field. The normal Data Loader
source review, preview, and approval workflow remains required.

## Pricing Strategy Child Associations

When a request associates any child entity under a Pricing Strategy, always
route the association to the existing global customer pricing definition whose
`AssignmentTypeCode` is `ORA_QP_ALL`. Use that definition's resolved
`PricingStrategyId` for every child association in the request.

1. Perform the read-only `customerPricingDefinitions` lookup through
   `core.fusion-api.rest-api-client`, filtering for `AssignmentTypeCode`
   `ORA_QP_ALL` and requesting `CustomerPricingDefinitionId`,
   `AssignmentTypeCode`, and `PricingStrategyId`.
2. When exactly one global definition has a nonblank `PricingStrategyId`, use
   it. When none exists, prepare a separate global Customer Pricing Definition
   create load with `AssignmentTypeCode=ORA_QP_ALL`, the documented global name
   default when Name is omitted, and the documented currency default when the
   live sample supports it. Validate, preview, and obtain approval for that
   create load. After it succeeds, rerun this association route to resolve the
   newly generated `PricingStrategyId`. Multiple, ambiguous, or failed results
   stop before preview or Data Loader preparation.
3. Resolve the requested entity's type through its registered read-only Fusion
   business-object contract. Select only the matching
   `customerPricingDefinitions` child collection, such as
   `associatedSegmentPriceLists`, `associatedCeilingPriceLists`,
   `associatedFloorPriceLists`, `associatedReturnPriceLists`,
   `associatedGSAPriceLists`, `associatedCostLists`,
   `associatedCurrencyConversionLists`, `associatedDiscountLists`,
   `associatedPricingGuidelines`, or `associatedShippingChargeLists`. Do not
   infer a child collection from a name; an absent, unsupported, or ambiguous
   type stops the workflow.
4. Populate the selected child association from the resolved global definition's
   `PricingStrategyId`. Do not substitute a caller-supplied ID. A supplied ID
   that differs from the resolved global strategy is a conflict and stops the
   workflow.
5. Format every `AssociationStartDate` as
   `YYYY-MM-DDTHH:MI:SS.sss+hh:mm`, for example
   `2026-09-25T00:00:00.000+00:00`. Do not submit Excel serial dates, locale
   dates, or timestamps without a numeric UTC offset.
6. Revalidate and regenerate the immutable Data Loader artifact after applying
   the derived strategy, type, and timestamp; the normal preview and approval
   workflow remains required.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `customerPricingDefinitions` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "customerPricingDefinitions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Customer Pricing Definitions` under `Pricing`.
