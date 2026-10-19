---
task_code: "CUSTOM_MANAGE_BALANCE_PROFILES"
task_name: "Manage Balance Profiles"
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
  - "subscriptionBalanceProfiles"
  - "subscriptionBalanceProfiles_activate"
  - "subscriptionBalanceProfiles_deActivate"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Balance Profiles

## Setup Task Metadata

- Task name: `Manage Balance Profiles`
- Task code: `CUSTOM_MANAGE_BALANCE_PROFILES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Objects: `subscriptionBalanceProfiles`, `subscriptionBalanceProfiles_activate`, `subscriptionBalanceProfiles_deActivate`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.

## Default Read-Only List Presentation

When a user asks to list Balance Profiles without supplying a
`BalanceProfileNumber`, use the declared `list_balance_profiles` lookup. For
every returned profile, also use
`list_balance_profile_group_criteria_balance_predicates` and present the
returned predicates in a **Grouping Criteria** column as
`BalanceObjectName.BalanceAttributeName`, ordered by
`BalancePredicateSequence`. Separate multiple predicates with `; `.

Return the profile page metadata (`count`, `hasMore`, and `offset`) and the
predicate results. Show `None returned` when a profile has no predicates; do
not infer grouping criteria from its name or status. If a predicate lookup
fails, report that profile's grouping criteria as unavailable and retain the
lookup failure rather than omitting it silently.

## Create Route Selection

For balance-profile creation, use Fusion Data Loader by default. Use REST only
when the user explicitly requests creation **via REST**.

| Create request | Selected route | Required handling |
| --- | --- | --- |
| Create a balance profile, with no route specified | Fusion Data Loader | Select the applicable profile model, validate that the exact profile name is absent, then generate and validate the local `subscriptionBalanceProfiles` workbook through `core.data-loader`. Do not upload or import without the separate immutable-preview and explicit upload approval. |
| Create a balance profile **via Data Loader** | Fusion Data Loader | Use the same Data Loader workflow. |
| Create a balance profile **via REST** | Direct Fusion REST | Use the explicit REST create route below. |

The default route creates only a local source artifact. It does not authorize a
Fusion create, upload, or import.

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `subscriptionBalanceProfiles`, `subscriptionBalanceProfiles_activate`, `subscriptionBalanceProfiles_deActivate` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionBalanceProfiles" \
     "subscriptionBalanceProfiles_activate" \
     "subscriptionBalanceProfiles_deActivate" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Subscription Number Balance Profile Data Loader Workbook

Interpret a customer request such as _“Create a balance profile \"Subscription Number Balance Profile\" with rate plan enabled and grouping at SubscriptionSubscriptionNumber level using skill \"Manage Balance Profile\" create xlsx for data-loader”_ as a rate-plan-model request because it explicitly enables the rate plan. When a request explicitly identifies the new or rate-plan model, set `RatePlanFlag: true` and prepare the local Data Loader XLSX for `subscriptionBalanceProfiles` with this hierarchy:

```json
{
  "BalanceProfileName": "Subscription Number Balance Profile",
  "RatePlanFlag": true,
  "groupCriteria": [
    {
      "BalanceCriteriaDescription": "Subscription Subscription Number grouping",
      "subscriptionBalancePredicates": [
        {
          "BalanceObjectName": "Subscription",
          "BalanceAttributeName": "SubscriptionNumber",
          "BalancePredicateSequence": 1
        }
      ]
    }
  ]
}
```

`SubscriptionSubscriptionNumber` denotes the `Subscription` balance object and its `SubscriptionNumber` attribute. For the rate plan model, populate the root `subscriptionBalanceProfiles` row with `RatePlanFlag: true`, then its `groupCriteria` child row, then the `subscriptionBalancePredicates` child row using the generated live-metadata headers and their declared parent-linking fields. Do not add legacy billing, `profileCharges`, or `profileBalanceCodes` rows. Use `POST` for each create row.

If `RatePlanFlag` is absent, do not treat this short request as a complete legacy-profile workbook request. Collect the legacy billing, group-criteria status and usage, charge, and balance-code values before preparing the workbook, and omit `RatePlanFlag` from the legacy source.

For every request to create a balance profile, first run the declared read-only `find_balance_profile_by_exact_name` lookup with the requested `BalanceProfileName`. Require exactly one returned item whose `BalanceProfileName` equals the requested name. When it exists, return its profile details and grouping criteria; do not create a second Data Loader workbook or attempt a duplicate Fusion create. When it is absent, prepare the new local workbook and continue only through the normal Data Loader validation, immutable-preview, and separate upload-approval gates. A lookup failure or multiple exact matches blocks creation.

## Create Payload Models

Manage Balance Profiles supports two mutually exclusive create-payload models. Prefer the new rate-plan model when the request explicitly identifies it as the new model or enables the rate plan. Otherwise, use the legacy profile model. Select the model before generating a workbook, validation result, preview, or REST payload.

### Rate plan model

Use the rate plan model only when the request explicitly identifies the new model, explicitly enables the rate plan, or explicitly supplies `RatePlanFlag: true`. Set `RatePlanFlag: true` in the generated source and payload, and send only the rate-plan fields shown below; do not add legacy billing, charge, or balance-code fields.

```json
{
  "BalanceProfileName": "Gold Balance Profile",
  "RatePlanFlag": true,
  "groupCriteria": [
    {
      "BalanceCriteriaDescription": "Inline group criteria",
      "subscriptionBalancePredicates": [
        {
          "BalanceObjectName": "SubscriptionProduct",
          "BalanceAttributeName": "OriginalSubscriptionProductPuid",
          "BalancePredicateSequence": 1
        }
      ]
    }
  ]
}
```

### Legacy profile model

Use the legacy profile model when the request does not explicitly identify the new model or enable the rate plan. Do not send `RatePlanFlag` in this model. Include group criteria, profile charges, and balance codes. Group-criteria description and status are optional: include them only when the request explicitly supplies or approves them. Root billing attributes are optional: include them only when the request explicitly supplies or approves them. Preserve explicit `null` values when supplied; do not remove, infer, or replace them with defaults.

For a legacy profile, `RatePlanFlag` is intentionally absent; do not set it to either
`true` or `false`. Keep project-specific payload identities, charge definitions,
balance codes, and periods in the project workspace rather than this reusable skill.

```json
{
  "BalanceProfileNumber": "Balance_Profile_01",
  "BalanceProfileName": "Balance_Profile_01",

  "groupCriteria": [
    {

      "BalanceCriteriaUsage": "ORA_OSS_ENTPLAN_GROUP_CRITERIA",
      "subscriptionBalancePredicates": [
        {
          "BalanceObjectName": "SubscriptionProduct",
          "BalanceAttributeName": "PONumber",
          "BalancePredicateSequence": 1
        }
      ]
    }
  ],
  "profileCharges": [
    {
      "ChargeDefinitionCode": "MOBILE_CHARGE",
      "ChargePeriod": "0zG",
      "AllowanceGrantFlag": false,
      "EstimateFlag": true,
      "CommitmentFlag": false,
      "RelatedChargeDefinitionCode": "OSS_MF"
    },
    {
      "ChargeDefinitionCode": "OSS_MF",
      "ChargePeriod": "0zG",
      "AllowanceGrantFlag": false,
      "EstimateFlag": true,
      "CommitmentFlag": false
    }
  ],
  "profileBalanceCodes": [
    {
      "BalanceCode": "Balance_Code_01",
      "BalancePrecedence": 1,
      "AllowanceGrantCodeFlag": false,
      "EstimateCodeFlag": true,
      "CommitmentCodeFlag": false
    }
  ]
}
```

Fail closed when the request is ambiguous about the model. Do not infer the rate plan model from the presence of group criteria or from any legacy field; select it only from an explicit new-model or rate-plan-enabled request, then set `RatePlanFlag: true`.

### Legacy profile setup checklist

Before generating a legacy-profile workbook, preview, or REST payload, capture all of these design inputs:

| Configuration area | Required input |
| --- | --- |
| Identity | Unique `BalanceProfileName`; Fusion generates the number on create. |
| Billing | Optional billing frequency, bill-period alignment, invoicing rule, billing-date rule, offsets, and true-up settings. Include only explicitly supplied values and preserve explicit nulls; do not default them. |
| Grouping | At least one balance object, attribute, and sequence; define the group-criteria usage and status. |
| Profile charges | Exact charge-definition identity, charge period, allowance-grant behavior, and estimate/commitment behavior for each charge. |
| Balance codes | Exact balance-code identity, unique precedence, and allowance-grant, estimate, and commitment behavior for each code. |

Resolve periodicity and billing frequency independently through the declared time-unit lookup only when a charge period or billing frequency is requested. A profile charge establishes the charge context for allowance rating; each selected balance code establishes the balance that is granted, consumed, or checked. Do not add `RatePlanFlag` to this legacy model or default any optional root billing attribute.

## Legacy REST Create with Charges and Balance Codes

When a request explicitly says to create a balance profile **via REST** and does not identify the new/rate-plan model, use the legacy model and `core.fusion-api.rest-api-client`. Resolve every named dependency before constructing the payload:

| Requested value | Required resolver | Payload value | Failure handling |
| --- | --- | --- | --- |
| Balance profile name | `find_balance_profile_by_exact_name` | `BalanceProfileName` | Stop on an existing exact name, multiple matches, or a lookup failure. `BalanceProfileNumber` is Fusion-generated for create and must not be sent. |
| Charge display name | Exact `subscriptionChargeDefinitions` name lookup | `profileCharges[].ChargeDefinitionCode` | Require exactly one active charge with a nonblank code. |
| Charge period | Exact `timeUnitOfMesaures` lookup described below | `profileCharges[].ChargePeriod` | Require exactly one matching returned time-unit code; do not default or infer a period. |
| Billing frequency | Exact `timeUnitOfMesaures` lookup described below | `profileCharges[].BillingFrequency` | When the request specifies a billing frequency, require exactly one matching returned time-unit code; do not default or infer a frequency. |
| Balance-code display name | Exact `subscriptionBalanceCodes` name/code lookup | `profileBalanceCodes[].BalanceCode` | Require exactly one active balance code with a nonblank code. |

Interpret a request such as _“Create a balance profile \"Sub Level BP\" with BillPeriodAlignDate set to \"2022-01-01\" and grouping at SubscriptionSubscriptionNumber level having charges \"Landline Charge\" \"Mobile Charge\" and balance codes \"Mobile Balance Code\" and \"Land Line Balance Code\" with Allowance grant set for both balance codes using skill \"Manage Balance Profile\" via Rest”_ as a legacy REST-create request. Map `SubscriptionSubscriptionNumber` to `BalanceObjectName: "Subscription"` and `BalanceAttributeName: "SubscriptionNumber"`.

### Time Unit Resolution for Charge Period and Billing Frequency

`profileCharges[].ChargePeriod` and `profileCharges[].BillingFrequency` are independent of the selected charge definition's `UsageUomClass`. Query the Fusion units-of-measure collection for the `TIME` class:

```http
GET /fscmRestApi/resources/latest/unitsOfMeasure?limit=500&fields=UOMCode,UOMClass,UOMClassCode,UOMClassName,UOM,Description&onlyData=true&orderBy=CreationDate:desc&q=UOMClass='TIME'
```

Match each requested period or billing-frequency attribute against returned `UOM` values case-insensitively. Normalize case and surrounding whitespace, and when the request uses a numeric period phrase, remove the leading quantity before matching the unit name; for example, normalize `1 month` to `MONTH`. Use the matched `UOMCode` as `profileCharges[].ChargePeriod` and, when requested, as `profileCharges[].BillingFrequency`. When a prompt says to set both period and billing frequency to the same value, resolve that time unit once and map the same returned `UOMCode` to both fields on every requested profile-charge row. Do not map that phrase to root `BillingFrequency` unless the prompt separately identifies the root attribute. Require exactly one match; stop on no match, multiple matches, or any lookup failure. Do not assume a code or reuse one from another request.

After the resolvers return `LANDLINE_CHARGE`, `MOBILE_CHARGE`, `MOBILE_BALANCE_CODE`, `LAND_LINE_BALANCE_CODE`, and their time-unit-derived charge-period and billing-frequency values, generate a payload in this shape. Set allowance-grant flags to `true` for each requested allowance-granting charge and balance code; retain `Estimate*` and `Commitment*` flags as `false` unless the request explicitly supplies another value.

```json
{
  "BalanceProfileName": "Sub Level BP",
  "BillPeriodAlignDate": "2022-01-01",
  "groupCriteria": [
    {
      "BalanceCriteriaUsage": "ORA_OSS_ENTPLAN_GROUP_CRITERIA",
      "subscriptionBalancePredicates": [
        {
          "BalanceObjectName": "Subscription",
          "BalanceAttributeName": "SubscriptionNumber",
          "BalancePredicateSequence": 1
        }
      ]
    }
  ],
  "profileCharges": [
    {
      "ChargeDefinitionCode": "LANDLINE_CHARGE",
      "ChargePeriod": "<resolved-landline-charge-period>",
      "BillingFrequency": "<resolved-billing-frequency>",
      "AllowanceGrantFlag": true,
      "EstimateFlag": false,
      "CommitmentFlag": false
    },
    {
      "ChargeDefinitionCode": "MOBILE_CHARGE",
      "ChargePeriod": "<resolved-mobile-charge-period>",
      "BillingFrequency": "<resolved-billing-frequency>",
      "AllowanceGrantFlag": true,
      "EstimateFlag": false,
      "CommitmentFlag": false
    }
  ],
  "profileBalanceCodes": [
    {
      "BalanceCode": "MOBILE_BALANCE_CODE",
      "BalancePrecedence": 1,
      "AllowanceGrantCodeFlag": true,
      "EstimateCodeFlag": false,
      "CommitmentCodeFlag": false
    },
    {
      "BalanceCode": "LAND_LINE_BALANCE_CODE",
      "BalancePrecedence": 2,
      "AllowanceGrantCodeFlag": true,
      "EstimateCodeFlag": false,
      "CommitmentCodeFlag": false
    }
  ]
}
```

Show the exact `POST /crmRestApi/resources/11.13.18.05/subscriptionBalanceProfiles` payload and target environment for approval only after all dependency and charge-period checks pass. A user must approve that immutable preview immediately before the one REST write; verify the profile through the declared read-only lookup afterward.

## Balance-Profile Activation Route

When a user asks to activate a balance profile, use the registered Data Loader business object `subscriptionBalanceProfiles_activate`.

1. Use the declared read-only `find_balance_profile_by_exact_number` lookup to resolve exactly one `BalanceProfileNumber` and its current `BalanceProfileStatus`. Stop if the profile is absent, ambiguous, or already active.
2. Generate the current live `subscriptionBalanceProfiles_activate` sample through `core.data-loader`; use its exact headers, required values, and operation shape. Do not substitute a direct REST activation call or a status `PATCH`.
3. Prepare and validate the activation source with the resolved balance-profile identity. Complete `core.data-loader` immutable-preview and Task Hook validation where applicable.
4. Obtain explicit approval for the exact archive immediately before upload and initiation. Do not retry a failed or uncertain load without a newly validated archive and approval.
5. Verify the resulting status through the declared read-only lookup and report the result. Preserve Data Loader diagnostics if processing fails.

## Balance-Profile Deactivation Route

When a user asks to deactivate a balance profile, use the registered Data Loader business object `subscriptionBalanceProfiles_deActivate`.

1. Use the declared read-only `find_balance_profile_by_exact_number` lookup to resolve exactly one `BalanceProfileNumber` and its current `BalanceProfileStatus`. Stop if the profile is absent, ambiguous, or already inactive.
2. Generate the current live `subscriptionBalanceProfiles_deActivate` sample through `core.data-loader`; use its exact headers, required values, and operation shape. Do not substitute a direct REST deactivation call or a status `PATCH`.
3. Prepare and validate the deactivation source with the resolved balance-profile identity. Complete `core.data-loader` immutable-preview and Task Hook validation where applicable.
4. Obtain explicit approval for the exact archive immediately before upload and initiation. Do not retry a failed or uncertain load without a newly validated archive and approval.
5. Verify the resulting status through the declared read-only lookup and report the result. Preserve Data Loader diagnostics if processing fails.

Before generating a new workbook, search the selected project's durable artifacts for an exact, validated `subscriptionBalanceProfiles` workbook with this profile name and grouping hierarchy. Return a matching workbook rather than creating a duplicate. If no matching workbook or Fusion profile exists, use `core.data-loader` to generate the current XLSX trio, populate the hierarchy above, and validate the editable workbook against the live Data Loader schema. This creates only a local source artifact; upload and Fusion creation require the separate Data Loader approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Balance Profiles` under `Usage Rating Setup`.
