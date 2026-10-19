---
task_code: "ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS"
task_name: "Manage Pricing Charge Definitions"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "pricingChargeDefinitions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Pricing Charge Definitions

## Setup Task Metadata

- Task name: `Manage Pricing Charge Definitions`
- Task code: `ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `pricingChargeDefinitions`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Create and update charge definitions only through `core.data-loader` using the registered `pricingChargeDefinitions` REST Data Loader business object. Do not use FSM import for this task.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Pricing Charge Definitions`
- Setup task code: `ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS`

## Apps Common Lookup Routing

Route standard lookup resolution for this task through
`core.fusion-api.apps-common`, which selects
`core.fusion-api.apps-common.lookups`. Use read-only standard-lookup retrieval
before preparing a charge-definition payload; do not create or update a lookup
as part of this task.

| Charge-definition field | Lookup type | Filter condition |
|---|---|---|
| Price Type | ORA_QP_PRICE_TYPES | LookupType = ORA_QP_PRICE_TYPES; exclude LookupCode = ORA_USAGE; include shared ORA_QP_ALL values when returned by the Pricing lookup view |
| Charge Type | ORA_QP_CHARGE_TYPES | LookupType = ORA_QP_CHARGE_TYPES; include shared ORA_QP_ALL values when returned by the Pricing lookup view |
| Charge Subtype | ORA_QP_CHARGE_SUBTYPES | LookupType = ORA_QP_CHARGE_SUBTYPES; include shared ORA_QP_ALL values when returned by the Pricing lookup view |
| Tax Charge Type | ZX_CHARGE_TYPE | LookupType = ZX_CHARGE_TYPE |

Use the standard lookup read contract documented by
`core.fusion-api.apps-common.lookups`; pass the selected lookup type and these
filter conditions as task-specific inputs. A custom charge type or subtype is
allowed only after its lookup code is verified as enabled.

## Recurring Price-Periodicity UOM-Class Defaulting

For a recurring charge definition, derive the Price Periodicity UOM Class from
the Site-level profile option **SCM Common: Default UOM Class for Service
Duration** (`RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION`) when the user does
not provide a value. Route that read through **Manage Pricing Profile Options**
(`scm.order-management.pricing.manage-pricing-profile-options`), which selects
the `core.fusion-api.apps-common.profile-options` workflow. Do not use a
task-local REST or OAuth route.

If the profile option has no current Site value, do not infer a periodicity UOM
class: require the user to supply it. If the user supplies a UOM class, preserve
that value. When it exactly matches the resolved profile value, tell the user
that it is the configured default from **SCM Common: Default UOM Class for
Service Duration** and recommend retaining it as the best-practice choice. Use
the profile display name in user-facing recommendations; retain
`RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` for the implementation lookup and
audit traceability. This recommendation is informational and must not replace
an explicitly supplied different UOM class.

## Charge-Type and Charge-Subtype Decision Path

1. When the request supplies both Charge Type and Charge Subtype, retrieve the
   specified lookup codes and the current charge definitions. If both codes are
   enabled and the exact `(PriceTypeCode, ChargeTypeCode, ChargeSubtypeCode)`
   combination is absent, prepare the definition source. If either code is
   absent or disabled, route creation or enablement of that exact supplied code
   through **Manage Pricing Lookups**
   (`scm.order-management.pricing.manage-pricing-lookups`), verify the code is
   enabled, then recheck the combination before preparing the definition.
2. When either Charge Type or Charge Subtype is omitted, retrieve every enabled
   value in `ORA_QP_PRICE_TYPES`, `ORA_QP_CHARGE_TYPES`, and
   `ORA_QP_CHARGE_SUBTYPES`, and retrieve all current charge definitions
   read-only. Preserve a supplied Price Type; otherwise include each enabled
   Price Type in the search. Evaluate every applicable exact three-code
   combination against the current definitions, continuing past combinations
   that are already assigned. Stop only when an enabled, unused combination is
   found, or after the complete candidate set has been exhausted. Present the
   first available combination, together with the rejected combinations and
   their conflicting definition codes; require explicit user approval before
   preparing the definition source. If no available combination exists, report
   the exhausted search and stop without preparing a source or changing a
   lookup.

Never overwrite supplied type or subtype codes. A lookup create or enablement
requires its own exact-payload approval immediately before the lookup write;
the later charge-definition import remains subject to its separate Data Loader
preview and approval gate.

## Explicitly Supplied Missing Lookup Codes

If an explicitly supplied Charge Type or Charge Subtype code is absent or
disabled in its respective Pricing lookup, route that individual lookup change
to **Manage Pricing Lookups**. Do not substitute a different existing code.

Before that separate lookup mutation, retain the exact user-supplied code,
meaning, description, target environment, and lookup type; read the current
lookup to confirm its absence or disabled state; present the exact creation or
enablement payload; and obtain explicit approval immediately before the write.
The lookup workflow must create or enable only the explicitly supplied missing
value, verify it is enabled through a read-only lookup, then return control to
this charge-definition workflow. Re-run all lookup and exact-combination
uniqueness checks before preparing a Data Loader preview.

## Charge-Type Combination Readiness

Before creating a `pricingChargeDefinitions` record, resolve the selected Price
Type, Charge Type, and Charge Subtype through the lookup workflow above and
verify that all selected lookup codes are enabled and that the exact
`(PriceTypeCode, ChargeTypeCode, ChargeSubtypeCode)` combination is absent
from every current charge definition. Do not create a charge definition until
this check passes.

1. Retrieve all selected lookup values read-only through
   `core.fusion-api.apps-common.lookups` and require each code to be enabled.
2. Verify the requested `(Price Type, Charge Type, Charge Subtype)` combination
   against all current Pricing charge definitions before building a Data Loader
   source or preview. An existing combination blocks creation; do not overwrite
   or reuse a definition implicitly.
3. Create or enable a missing Charge Type or Charge Subtype only through the
   separate **Manage Pricing Lookups** workflow, using the exact supplied code.
4. Re-run the lookup and pair checks whenever the selected Charge Type or
   Charge Subtype changes, including after the separate lookup workflow
   completes. A change invalidates the prior Data Loader preview and requires
   fresh validation and approval.

Fail closed on ambiguous lookup matches, disabled codes, an existing pair, or
an unavailable pair. Report the blocker and the missing or conflicting lookup
category without exposing source payloads.

## REST Read Details Workflow

For a current charge-definition detail request, use
`core.fusion-api.rest-api-client` with a read-only `GET` against
`/fscmRestApi/resources/11.13.18.05/pricingChargeDefinitions`.

1. Retrieve `pricingChargeDefinitions/describe` when the current field
   contract must be verified.
2. Filter the collection by the exact `ChargeDefinitionCode` or another
   user-selected queryable identifier.
3. Return only the requested current attributes; retrieve
   `chargeDefinitionsDFF` only when DFF values are requested.
4. Do not use Data Loader or a task-level export for a live detail lookup.
   Data Loader is reserved for create and update imports.




## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `pricingChargeDefinitions` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "pricingChargeDefinitions" \
     --output-dir "<project-artifact-directory>"
   ```


3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Pricing Charge Definitions` under `Pricing`.
