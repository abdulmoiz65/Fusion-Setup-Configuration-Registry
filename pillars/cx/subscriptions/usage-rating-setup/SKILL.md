---
skill_id: "cx.subscriptions.usage-rating-setup"
name: "Usage Rating Setup Implementation Guidance"
description: "Provides CX Subscriptions implementation guidance for the Usage Rating Setup functional area."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Usage Rating Setup"
functional_area_code: "CUSTOM_USAGE_RATING_SETUP"
type: "advisory"
execution_mode: "hybrid"
owner_team: "CX subscriptions pillar team"
version: "0.1.8"
inputs:
  - "implementation_objective"
  - "project_context"
  - "usage_rating_setup_scope"
  - "usage_rating_setup_requirements"
  - "prerequisite_configuration_confirmation"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "prerequisite_confirmation_request"
  - "skill_run_record"
  - "token_usage_record"
  - "data_loader_workbook_set"
  - "execution_result"
  - "diagnostics"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "shared.validation.setup-data-validator"
  - "scm.product-management.items"
  - "scm.order-management"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/usage-rating-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/usage-rating-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/usage-rating-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_MANAGE_BALANCE_CODES"
  - "CUSTOM_MANAGE_BALANCE_PROFILES"
  - "CUSTOM_MANAGE_USAGE_ENTITLEMENT"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Generates local Data Loader workbook artifacts in the selected project workspace."
  - "Performs approved read-only Fusion REST lookups and verification."
  - "Performs approved Fusion REST create, update, or activation actions only through the declared core client."
  - "Uploads or initiates Data Loader operations only through core.data-loader after its immutable-preview and approval gates."
required_privileges:
  - "Fusion REST access for CX Subscriptions balance codes, balance profiles, usage entitlements, entitlement plans, and entitlement assignments."
  - "Fusion Data Loader access for the selected registered business object when a Data Loader route is selected."
---

# Usage Rating Setup Implementation Guidance

## Purpose

Provides CX Subscriptions implementation guidance for the Usage Rating Setup functional area.

## When to Use

Use this functional-area skill after Subscriptions scope is confirmed and the project needs guidance for Usage Rating Setup prerequisites, balance design, entitlement design, validation checkpoints, or an approved REST/Data Loader route.

## Execution Controls

This package is advisory until a task selects an execution route. Route all Fusion
REST calls through `core.fusion-api.rest-api-client`, all Data Loader artifact and
load operations through `core.data-loader`, and setup-data artifact validation
through `shared.validation.setup-data-validator`.

### Preflight Checks

Before any side effect, confirm the selected environment, required privileges,
catalog/task support, exact object identity, dependency readiness, and payload or
workbook shape. Generate and validate local artifacts before upload. Immediately
before a REST create, update, activation, upload, or load initiation, present the
exact target, operation, and immutable payload or artifact and obtain explicit
approval. Do not retry an uncertain or failed live write automatically.

### Diagnostics and Redaction

For input, catalog, authorization, transport, Fusion API, artifact-persistence, or
approval failures, stop and record the failure class, message, recommended action,
environment, artifact references, and available request or process identifiers in
the project workspace. The core client may refresh a cached OAuth token once after
HTTP 401 or 403; all other retry behavior follows the selected core skill.

Never print or persist credentials, access tokens, token caches, private keys,
tenant secrets, wallet files, full base64 payloads, or sensitive customer data in
skill output, diagnostics, or project artifacts.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Subscriptions` (`CUSTOM_SUBSCRIPTIONS`)
- Functional area / Setup Object: `Usage Rating Setup` (`CUSTOM_USAGE_RATING_SETUP`)

## Setup Tasks

1. [Manage Balance Codes](manage-balance-codes.md) (`CUSTOM_MANAGE_BALANCE_CODES`)
2. [Manage Balance Profiles](manage-balance-profiles.md) (`CUSTOM_MANAGE_BALANCE_PROFILES`)
3. [Manage Usage Entitlement](manage-usage-entitlement.md) (`CUSTOM_MANAGE_USAGE_ENTITLEMENT`)

## Request Routing

Usage Rating Setup begins only after its upstream commercial and product configuration is defined. The following prerequisite objects are outside this functional area and are advisory dependencies, not Usage Rating Setup tasks:

1. Create the applicable **Unit of Measure Class** and **Unit of Measure**.
2. Create the required **one-time, recurring, and usage charges**.
3. Create the **rate plan** with its charges and defined values.
4. Create the subscription **item or product** so the entitlement plan can be associated to it.

For a subscription that originates in Order Management, the opt-in **Integrate Order
Management with Subscription Management to Process Subscriptions** is also required.
Treat the opt-in as a prerequisite confirmation. Do not assume it is enabled or enable
it as part of Usage Rating Setup guidance.

Do not route a charge-definition, rate-plan, item, product, or UOM create/update request to a Usage Rating Setup task. Identify it as a prerequisite and retain Usage Rating Setup in advisory mode until the dependency is confirmed.

Route every Usage Rating Setup request whose primary object is a **Balance Code** to [Manage Balance Codes](manage-balance-codes.md), including create, update, activation, lookup, and Data Loader workbook requests.

Route every Usage Rating Setup request whose primary object is a **Balance Profile** to [Manage Balance Profiles](manage-balance-profiles.md) (the **Manage Balance Profile** skill), including create, update, activation, lookup, and Data Loader workbook requests.

Route every Usage Rating Setup request whose primary object is a **Usage Entitlement**, **Entitlement Plan**, or **Entitlement Assignment** to [Manage Usage Entitlement](manage-usage-entitlement.md), including create, update, activation, lookup, list, and Data Loader workbook requests.

Route a request for **Usage Rating**, **Consumption Plan**, **Allowance**, or another Usage Rating Setup object not covered above to its dedicated task skill in this functional area when one is present in the current setup-task catalog. Do not silently map it to Balance Codes, Balance Profiles, or Manage Usage Entitlement. If no dedicated task skill is available, retain it at the Usage Rating Setup functional-area level and report the routing gap before execution.

## Prerequisite Confirmation Gate

Before advising a Usage Rating Setup design that depends on a commercial plan, confirm the prerequisite configuration with the user. Do not infer a UOM, charge, rate-plan amount, or item/product from a plan name.

Record prerequisite confirmations as design inputs. If any prerequisite is
unconfirmed, provide the outstanding-input list and stop at advisory guidance;
do not prepare a Fusion payload, workbook, import, or external operation.

### Balance Code UOM Resolution

Before preparing or executing a quantity-balance-code payload, resolve the exact
approved UOM record through the selected read-only endpoint. Use the UOM display
value confirmed in the project design inputs; do not substitute an example value:

```text
/fscmRestApi/resources/latest/unitsOfMeasure?limit=500&fields=UOMCode,UOMClass,UOMClassCode,UOMClassName,UOM,Description&onlyData=true&orderBy=CreationDate:desc&q=UOM='<approved UOM display value>'
```

Require exactly one matching row with a nonblank `UOMCode`. Set
`BalanceUnitofMeasureCode` from the returned `UOMCode` only. Never pass the display
value `UOM` as `BalanceUnitofMeasureCode`. Treat no match, multiple matches, a blank
UOM code, authorization, transport, or Fusion API failure as a blocker; do not
prepare a create payload or retry automatically.

## Optional Post-Setup Verification

After the opt-in, item, charge definitions, price list, and rate plans have been
created and activated through their approved workflows, a user may request a read-only
verification. Use `core.fusion-api.rest-api-client` and the configured Fusion
environment; do not infer completion from design inputs or perform any mutation.

1. For each approved charge definition, issue an exact-name `GET` to
   `/crmRestApi/resources/latest/subscriptionChargeDefinitions` with
   `q=Name='<approved charge name>'`, requesting `Name`, `ChargeDefinitionCode`,
   and `ChargeDefinitionId`. Require exactly one row and the expected code from
   the approved design inputs.

   | Project input | Required value |
   | --- | --- |
   | Charge name | Approved charge name |
   | Expected charge-definition code | Approved charge-definition code |

2. For each approved rate plan, issue an exact-name `GET` to
   `/fscmRestApi/resources/latest/ratePlans/` with
   `q=RatePlanName='<approved rate plan name>'`. Require exactly one row.

3. Report each result as present, absent, ambiguous, or lookup failed. Persist the
   validation result and a skill-run record under the active project workspace. A
   missing, ambiguous, authorization, transport, or Fusion API failure blocks any
   downstream build step; do not retry automatically except for the shared client's
   one allowed OAuth refresh after HTTP 401 or 403.

## Inputs

- `implementation_objective`
- `project_context`
- `usage_rating_setup_scope`
- `usage_rating_setup_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For a Minutes Balance Code request, follow the reuse-or-create workflow in [Manage Balance Codes](manage-balance-codes.md): return an exact matching validated project workbook or existing Fusion balance code first, and generate a fresh Data Loader workbook only after the customer explicitly requests one. Never prepare a duplicate-create source for an existing balance-code identifier.
