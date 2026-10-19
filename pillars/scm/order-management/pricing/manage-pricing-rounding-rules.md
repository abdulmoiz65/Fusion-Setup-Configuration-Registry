---
task_code: "ORA_QP_MANAGE_ROUNDING_RULES"
task_name: "Manage Rounding Rules"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "pricingRoundingRules"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Pricing Rounding Rules

## Setup Task Metadata

- Task name: `Manage Rounding Rules`
- Task code: `ORA_QP_MANAGE_ROUNDING_RULES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `pricingRoundingRules`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. When a rounding-direction or rounding-type name is supplied, resolve its code through the applicable Manage Pricing Lookups step below before preparing the import data.
3. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
4. Import setup task data with `core.data-loader` using pricingRoundingRules as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Rounding Rules`
- Setup task code: `ORA_QP_MANAGE_ROUNDING_RULES`

## List Existing Rounding Rules

Use this read-only workflow when the request is to list or review existing
rounding rules. Fetch the rules through `core.fusion-api.rest-api-client`; do
not use the Data Loader import route.

1. Read the complete `pricingRoundingRules` collection with `REST-Framework-Version: 9`, `onlyData=true`, `limit=500`, and `offset=0`; advance the offset by the returned item count until `hasMore=false`.
2. Retain each rule's `Name`, `RoundValue`, `RoundingRuleTypeCode`, `RoundingRuleDirectionCode`, `ActiveFlag`, and `SetupEnabledFlag`.
3. For the distinct returned type and direction codes, invoke [Manage Pricing Lookups](manage-pricing-lookups/SKILL.md) (`scm.order-management.pricing.manage-pricing-lookups`) with read-only lookup-code requests for `ORA_QP_ROUND_TYPES` and `ORA_QP_ROUND_DIRECTIONS`.
4. Match each returned code exactly to `LookupCode` and add the associated `Meaning` to the review result as `RoundingRuleTypeName` or `RoundingRuleDirectionName`. Keep the original codes in the result; names are for display only.
5. If either lookup is incomplete or a code has no unique display-name match, show its code and report the unresolved display name. Do not infer a name from the code or report an incomplete rule collection as an empty result.


## Resolve a Rounding Direction Name

1. If `RoundingRuleDirection` is supplied as a name, invoke [Manage Pricing Lookups](manage-pricing-lookups/SKILL.md) (`scm.order-management.pricing.manage-pricing-lookups`) with `pricing_lookup_type: ORA_QP_ROUND_DIRECTIONS` and a read-only lookup-code request. Include the supplied name and the Manage Rounding Rules task context. Let that skill route the lookup through Apps Common; do not select a direct REST endpoint here.
2. Match the name to one enabled, currently effective lookup `Meaning`, using the name-resolution contract in [Reference Lookups](ora-resource/ora_reference_lookups.md). Set `RoundingRuleDirectionCode` to the returned `LookupCode`; do not derive it by uppercasing the name.
3. If no unique match exists, or a supplied code conflicts with the matched code, stop and resolve the conflict. When only a code is supplied, retain it and skip name resolution.
4. Put the resolved code in the Data Loader source before validation and approval. If resolution changes an already prepared source, rebuild and revalidate its immutable archive and rerun Task Hook before requesting submission approval.

## Resolve a Rounding Type Name

1. If a rounding type is supplied as a name, invoke [Manage Pricing Lookups](manage-pricing-lookups/SKILL.md) (`scm.order-management.pricing.manage-pricing-lookups`) with `pricing_lookup_type: ORA_QP_ROUND_TYPES` and a read-only lookup-code request. Include the supplied name and the Manage Rounding Rules task context. Let that skill route the lookup through Apps Common; do not select a direct REST endpoint here.
2. Match the trimmed name case-insensitively to exactly one enabled, currently effective lookup `Meaning` in the response language. Set `RoundingRuleTypeCode` to the returned `LookupCode`; do not infer the code from the name or use fuzzy matching.
3. If no unique match exists, or a supplied code conflicts with the matched code, stop and resolve the conflict. When only a code is supplied, retain it and skip name resolution.
4. Put the resolved code in the Data Loader source before validation and approval. If resolution changes an already prepared source, rebuild and revalidate its immutable archive and rerun Task Hook before requesting submission approval.

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `pricingRoundingRules` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "pricingRoundingRules" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.



## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for the `Manage Rounding Rules` setup task under `Pricing`.
