---
task_code: "CUSTOM_MANAGE_USAGE_ENTITLEMENT"
task_name: "Manage Usage Entitlement"
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
  - "subscriptionUsageEntitlements"
  - "subscriptionEntitlementPlans"
  - "subscriptionEntitlementAssignments"
  - "subscriptionEntitlementPlans_activate"
  - "subscriptionEntitlementPlans_deActivate"
  - "subscriptionEntitlementAssignments_activate"
  - "subscriptionEntitlementAssignments_deActivate"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Usage Entitlement

## Setup Task Metadata

- Task name: `Manage Usage Entitlement`
- Task code: `CUSTOM_MANAGE_USAGE_ENTITLEMENT`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Objects: `subscriptionUsageEntitlements`, `subscriptionEntitlementPlans`, `subscriptionEntitlementAssignments`, `subscriptionEntitlementPlans_activate`, `subscriptionEntitlementPlans_deActivate`, `subscriptionEntitlementAssignments_activate`, `subscriptionEntitlementAssignments_deActivate`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export`. A Data Loader route is permitted only when the user explicitly requests Data Loader and live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.

## Default Read-Only Entitlement-Plan List Presentation

When a user asks to list Usage Rating entitlement plans without supplying an
`EntitlementPlanNumber`, use the declared `list_usage_entitlement_plans`
lookup first. Present one row per entitlement plan using this default format:

| Plan | Entitlement details | Balance profile | Status | Linked item |
| --- | --- | --- | --- | --- |
| EntitlementPlanName | One entry for every Allowance, Estimate, or Commitment detail, prefixed with `Allowance:`, `Estimate:`, or `Commitment:` as applicable; include BalanceCode, ChargeDefinitionCode, and quantity/UOM or amount/currency | BalanceProfileName and BalanceProfileNumber | Status from the primary usage-entitlement row or EntitlementPlanStatus from the fallback plan row | ItemNumber from the primary row or InventoryItemName from the fallback assignment row |

Do not infer a model type from a plan name. When no model-detail child record is
returned, show `Unspecified — no model-detail record returned`. When a plan has
no matching assignment in the fallback result, show `— no assignment` for the
linked item.

If `subscriptionUsageEntitlements` returns an API or pagination failure, use
the declared fallback exactly once: list `subscriptionEntitlementPlans`, list
`subscriptionEntitlementAssignments`, and join the results by exact
`EntitlementPlanNumber`. Do not use the fallback for an empty primary result,
and do not retry a failed primary or fallback request automatically.

## Creation Model Selection

Manage Usage Entitlement supports three Data Loader creation paths. Select the path from the user's request before preparing any source or payload.

| User request | Selected Data Loader business object | Result |
| --- | --- | --- |
| Explicitly create an **entitlement plan only** | `subscriptionEntitlementPlans` | Create only the entitlement plan. Do not create an assignment. |
| Explicitly create an **entitlement plan assignment** | `subscriptionEntitlementAssignments` | Create only the assignment, using the exact validated entitlement-plan identity. |
| Any other create request, including a usage-entitlement request | `subscriptionUsageEntitlements` | Create the composite usage entitlement. |

Do not treat the objects as interchangeable, split a composite usage-entitlement request into separate objects, or add an assignment to an explicit plan-only request. Use `subscriptionUsageEntitlements` unless the user explicitly requests an entitlement plan only or an entitlement plan assignment.

## Object Documentation and Data Loader Routing

Use the official object documentation to validate source attributes and identity. For creation, route through `core.data-loader`; do not select a direct REST create route.

| User request | Required Oracle REST documentation | Data Loader business object | Identity used for later operations |
| --- | --- | --- | --- |
| Explicitly create an entitlement plan only | [Subscription Entitlement Plans REST API](https://docs.oracle.com/en/cloud/saas/sales/faaps/api-subscription-entitlement-plans.html) | `subscriptionEntitlementPlans` | `EntitlementPlanNumber` |
| Explicitly create an entitlement assignment | [Subscription Entitlement Assignments REST API](https://docs.oracle.com/en/cloud/saas/sales/faaps/api-subscription-entitlement-assignments.html) | `subscriptionEntitlementAssignments` | `EntitlementAssignmentNumber` |
| Any other create request | [Subscription Usage Entitlements REST API](https://docs.oracle.com/en/cloud/saas/sales/faaps/api-subscription-usage-entitlements.html) | `subscriptionUsageEntitlements` | `UsageEntitlementId` |

For a plan-and-assignment design, create and verify the plan before preparing an assignment that references it. For every branch, generate and validate the selected Data Loader source, complete immutable-preview and Task Hook validation, then obtain approval immediately before upload and initiation.

## Entitlement Plan Allowance Payload Generation

Interpret a request such as _“Create an entitlement plan \"Silver Plan\" using Balance Profile \"Sub Level BP\", and allowance detail for Balance Code \"Mobile Balance Code\" and \"Mobile Charge\" having allowance 100.”_ as an entitlement-plan request in the separate plan-and-assignment model.

Keep rate-plan mapping outside the entitlement-plan create payload. Never send
`RatePlanId` or `RatePlanNumber` to `subscriptionEntitlementPlans`; retain the
commercial-rate-plan-to-entitlement-plan mapping in the implementation design and
apply the item and plan association through the separate entitlement-assignment
workflow.

Before generating the plan payload, resolve these dependencies exactly:

| Request value | Required lookup | Payload value | Required result |
| --- | --- | --- | --- |
| `Sub Level BP` | `subscriptionBalanceProfiles` exact-name lookup | `BalanceProfileId`, `BalanceProfileNumber` | Exactly one active profile; use its generated ID and number. |
| `Mobile Balance Code` | `subscriptionBalanceCodes` exact code or display-name lookup | `subscriptionEntitlementPlanDetails[].BalanceCode` | Exactly one active balance code; use its returned `BalanceCode`. |
| `Mobile Charge` | `subscriptionChargeDefinitions` exact-name lookup | `subscriptionEntitlementPlanDetails[].ChargeDefinitionCode` | Exactly one active charge definition with a nonblank returned code. |
| `100` | Validate as a positive allowance quantity | `subscriptionEntitlementPlanDetails[].AllowanceQuantity` | A positive numeric value; do not coerce invalid text. |

When all lookups pass, generate this payload shape. Use the requested plan name for both name and description unless a different description is explicitly supplied:

```json
{
  "EntitlementPlanName": "Silver Plan",
  "EntitlementPlanNumber": "<requested-plan-number>",
  "EntitlementPlanDescription": "Silver Plan",
  "BalanceProfileId": "<resolved-balance-profile-id>",
  "BalanceProfileNumber": "<resolved-balance-profile-number>",
  "subscriptionEntitlementPlanDetails": [
    {
      "BalanceCode": "<resolved-balance-code>",
      "ChargeDefinitionCode": "<resolved-charge-definition-code>",
      "AllowanceQuantity": 100
    }
  ]
}
```

For the stated example, do not prepare a source until the profile, balance-code, charge-definition, and allowance validations succeed. Then generate and validate a `subscriptionEntitlementPlans` Data Loader source and obtain approval immediately before upload and initiation.

### Multiple allowance-detail pattern

For a plan that grants more than one measure, include one `subscriptionEntitlementPlanDetails` row for each approved balance-code and charge-definition pair. Each row requires an independently validated positive `AllowanceQuantity`.

```json
{
  "EntitlementPlanName": "<plan-name>",
  "EntitlementPlanNumber": "<plan-number>",
  "EntitlementPlanDescription": "<plan-description>",
  "BalanceProfileId": "<resolved-balance-profile-id>",
  "BalanceProfileNumber": "<resolved-balance-profile-number>",
  "subscriptionEntitlementPlanDetails": [
    {
      "BalanceCode": "<resolved-first-balance-code>",
      "ChargeDefinitionCode": "<resolved-first-charge-definition-code>",
      "AllowanceQuantity": "<positive-first-allowance>"
    },
    {
      "BalanceCode": "<resolved-second-balance-code>",
      "ChargeDefinitionCode": "<resolved-second-charge-definition-code>",
      "AllowanceQuantity": "<positive-second-allowance>"
    }
  ]
}
```

Use the same resolved charge definition in multiple rows only when the approved business design explicitly uses one usage charge for multiple measures. Do not infer an allowance reset cadence from the quantity; define it through the selected profile, charge period, billing frequency, and entitlement-assignment design.

## Entitlement Plan Activation Route

When a user asks to activate an entitlement plan, use `subscriptionEntitlementPlans_activate`. Resolve exactly one non-active plan by `EntitlementPlanNumber`, generate the current live Data Loader sample, and prepare the source with its exact headers and action shape. Complete immutable-preview and Task Hook validation, obtain approval immediately before upload and initiation, then verify the plan status. Do not substitute a direct REST action or status `PATCH`, and do not retry a failed or uncertain load.

## Entitlement Plan Deactivation Route

When a user asks to deactivate an entitlement plan, use `subscriptionEntitlementPlans_deActivate`. Resolve exactly one active plan by `EntitlementPlanNumber`, generate and validate the live Data Loader source, complete immutable-preview and Task Hook validation, obtain approval immediately before upload and initiation, then verify the plan is inactive. Do not substitute a direct REST action or status `PATCH`, and do not retry a failed or uncertain load.

## Entitlement Plan Association Prerequisites

An entitlement-plan association is the final required step of the separate plan-and-assignment model. Perform it only after the entitlement plan was created, verified, and activated.

Before preparing an association payload, require all of the following:

| Required input | Reason | Missing-input handling |
| --- | --- | --- |
| Active entitlement plan | The association must reference the generated active `EntitlementPlanNumber`. | Stop and complete plan creation or activation first. |
| Entitlement assignment number | The create API requires `EntitlementAssignmentNumber`. | Default it to `<EntitlementPlanNumber>_ASSIGNMENT`; require the resulting value to be no longer than 120 characters and unique. If it is too long or already exists, ask the user for an alternate number. |
| Inventory organization | Items are resolved in an inventory-organization context. | Derive `OrganizationCode` from supplied project documents only when one exact organization is identified; otherwise ask the user for it. Do not infer it from an item, plan, or charge name. |
| Item | The association identifies the sellable item to which the plan applies. | Stop and ask the user to specify the item; do not infer one from the plan name, charge, or balance profile. |
| Assignment precedence | Determines selection when multiple assignments match. | Use `1` for the first assignment to the same product; otherwise determine the next unused positive integer for that product in the resolved inventory organization. |

Do not treat the plan definition, a balance profile, a charge definition, or an entitlement-plan name as an item association. The item must be explicit and must resolve to exactly one item in the supplied organization.

## Entitlement Assignment Payload Generation

Interpret a request such as _“Create an entitlement assignment \"Silver Plan Assignment\" for Organization V1, Item QP_Item3 and Entitlement Plan \"Silver Plan\" via Rest”_ as the assignment half of the separate plan-and-assignment model, using the REST assignment endpoint.

Before generating the assignment payload, resolve and validate:

| Request value | Required validation or lookup | Payload value | Required result |
| --- | --- | --- | --- |
| `V1` | Supplied project documents or current inventory-organization lookup | `OrganizationCode` | Derive the code from supplied documentation only when exactly one organization is identified; otherwise ask the user. The resolved code must match exactly one active organization. |
| `QP_Item3` | Current item lookup scoped to the resolved organization | `InventoryItemName` | Exactly one item available in organization `V1`. |
| `Silver Plan` | `subscriptionEntitlementPlans` exact-name lookup | `EntitlementPlanNumber` | Exactly one active plan; use its generated `EntitlementPlanNumber`. |
| Entitlement assignment number | Derived from the resolved `EntitlementPlanNumber` | `EntitlementAssignmentNumber` | Default to `<EntitlementPlanNumber>_ASSIGNMENT`. Require a unique value of 120 characters or fewer; ask the user for an alternate number if either validation fails. |
| Rate plan mapping | Current subscription-rate-plan lookup scoped to the resolved item | `RatePlanId`, `RatePlanNumber` | When the approved design associates this assignment to a rate plan, resolve exactly one item-compatible rate plan and send its returned ID and number. |
| Assignment precedence | Existing assignments for the resolved product in the resolved organization | `AssignmentPrecedence` | Use `1` when no assignment exists for that product. When assignments already exist, use the next unused positive integer (`2`, then `3`, and so on); do not reuse a precedence value for the same product. |

When all checks pass, generate this payload shape. The required assignment number
defaults to the exact resolved entitlement-plan number plus `_ASSIGNMENT`.

```json
{
  "EntitlementAssignmentNumber": "<resolved-entitlement-plan-number>_ASSIGNMENT",
  "OrganizationCode": "V1",
  "InventoryItemName": "QP_Item3",
  "EntitlementPlanNumber": "<resolved-entitlement-plan-number>",
  "RatePlanId": "<resolved-rate-plan-id>",
  "RatePlanNumber": "<resolved-rate-plan-number>",
  "AssignmentPrecedence": 1
}
```

Include `RatePlanId` and `RatePlanNumber` only in the entitlement-assignment
payload, never in the entitlement-plan create payload. Omit both only when the
approved assignment design has no rate-plan association.

Never send `BalanceProfileId` or `BalanceProfileNumber` in an
entitlement-assignment payload. Fusion derives the balance profile from the
referenced entitlement plan.

Before preparing a payload, determine whether the resolved item already has entitlement
assignments in the resolved organization. If none exist, use
`AssignmentPrecedence: 1`. Otherwise, use the next unused positive integer for that
same product. Show the resolved precedence in the approval payload and obtain
approval for that exact payload before submitting it.

Generate and validate a `subscriptionEntitlementAssignments` Data Loader source for the resolved assignment. Obtain approval immediately before upload and initiation, then preserve the generated `EntitlementAssignmentNumber` and verify it through the declared read-only lookup. Do not retry a failed or uncertain load automatically.

## Entitlement Assignment Activation Route

When a user asks to activate an entitlement assignment, use `subscriptionEntitlementAssignments_activate`. Resolve exactly one non-active assignment by `EntitlementAssignmentNumber`, generate and validate the live Data Loader source, complete immutable-preview and Task Hook validation, obtain approval immediately before upload and initiation, then verify the assignment status. Do not substitute a direct REST action or status `PATCH`, and do not retry a failed or uncertain load.

## Entitlement Assignment Deactivation Route

When a user asks to deactivate an entitlement assignment, use `subscriptionEntitlementAssignments_deActivate`. Resolve exactly one active assignment by `EntitlementAssignmentNumber`, generate and validate the live Data Loader source, complete immutable-preview and Task Hook validation, obtain approval immediately before upload and initiation, then verify the assignment is inactive. Do not substitute a direct REST action or status `PATCH`, and do not retry a failed or uncertain load.

## Usage-Entitlement Rate-Plan Status Propagation

Usage-entitlement status is automatically linked to its associated rate plan. When a rate plan is activated, Fusion activates each associated usage entitlement; when a rate plan is deactivated, Fusion deactivates each associated usage entitlement. Do not prepare a separate usage-entitlement activation or deactivation action for this propagated status change. Before a rate-plan status action, resolve the exact associated usage entitlements and preserve the relationship evidence in the immutable preview. No usage-entitlement activation or deactivation Data Loader business object is registered by this task; do not infer one from the entitlement-plan or entitlement-assignment action objects.

## Create and Update Route Selection

For creation, use Fusion Data Loader. Select `subscriptionEntitlementPlans` only for an explicit entitlement-plan-only request, `subscriptionEntitlementAssignments` only for an explicit entitlement-plan-assignment request, and `subscriptionUsageEntitlements` for all other requests. Complete source validation, immutable-preview and Task Hook validation, then obtain separate approval immediately before upload and initiation. Read-only lookup requests continue to use the declared REST lookups and do not select or authorize a create or update.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `subscriptionUsageEntitlements`, `subscriptionEntitlementPlans`, `subscriptionEntitlementAssignments`, `subscriptionEntitlementPlans_activate`, `subscriptionEntitlementPlans_deActivate`, `subscriptionEntitlementAssignments_activate`, `subscriptionEntitlementAssignments_deActivate` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionUsageEntitlements" \
     "subscriptionEntitlementPlans" \
     "subscriptionEntitlementAssignments" \
     "subscriptionEntitlementPlans_activate" \
     "subscriptionEntitlementPlans_deActivate" \
     "subscriptionEntitlementAssignments_activate" \
     "subscriptionEntitlementAssignments_deActivate" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Usage Entitlement` under `Usage Rating Setup`.
