---
skill_id: "scm.order-management.orders.revision-preferences-for-sales-orders"
name: "Revision Preferences for Sales Orders Setup Task Guidance"
description: "Provides a declarative Data Loader source contract for Revision Preferences for Sales Orders under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "ORA_FOM_REVISION_PREFERENCES_FOR_SALES_ORDERS"
task_name: "Revision Preferences for Sales Orders"
parent_skill_id: "scm.order-management.orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "omSalesOrderAttributePreferences"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "SCM order management pillar team"
version: "0.2.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/revision-preferences-for-sales-orders/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/revision-preferences-for-sales-orders/current/"
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
  - "Reads the current Revision Preferences attribute catalog when the active workflow selects the documented read-only REST discovery step."
  - "Prepares an omSalesOrderAttributePreferences DAT from the declared live-template contract; upload and initiation are Fusion mutations and require explicit approval immediately before execution."
required_privileges:
  - "Manage Revision Preferences (FOM_MANAGE_REVISION_PREFERENCES)"
  - "Privileges required by core.data-loader to validate, upload, and initiate the omSalesOrderAttributePreferences Data Loader REST operation."
---

# Revision Preferences for Sales Orders Setup Task Guidance

## Purpose

Provides task-specific setup planning, attribute discovery, and Business Object
Data Loader REST guidance for `Revision Preferences for Sales Orders` under
`Orders`.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Revision Preferences for Sales Orders` under `Orders`.

## Business Object Data Loader Workflow

Use `core.data-loader` with the live
`omSalesOrderAttributePreferences` Business Object template and the declared
Revision Preferences source contract below. This task does not use an FSM CSV
export, an FSM ZIP, or a direct REST PATCH.

The task workflow renders the declared DAT from live discovery facts;
`core.data-loader` validates, archives, uploads, and initiates the immutable
source. Do not invoke a task-local DAT builder or substitute an FSM CSV export,
FSM ZIP, or direct REST PATCH for that route.

## Revision Preference Scope and Prerequisites

This task configures the order-line attributes that users can update without
revising a sales order. It applies to the Redwood update-without-revision
feature. Before preparing configuration, record either a successful feature
lookup or the requester's attestation that the parent Redwood Search and Apply
Actions on Multiple Sales Orders feature is opted in, and confirm that the
operator has the Manage Revision Preferences privilege
(`FOM_MANAGE_REVISION_PREFERENCES`).

Use a requester attestation when the active workflow cannot read feature
metadata. Persist the attestation, its source, and timestamp with the
configuration blueprint. An attestation is evidence for this prerequisite only;
it does not authorize a Data Loader upload or initiation.

The Oracle 26A readiness note is the source for the feature behavior, setup
navigation, opt-in dependency, and privilege. The live attribute catalog, not
this skill or the readiness note, is authoritative for attributes that can be
configured.

## Attribute Discovery Contract

Before accepting, validating, previewing, or preparing a change, use the
active workflow's read-only REST client to retrieve the current, complete
attribute catalog:

- Resource: `omSalesOrderAttributePreferences`
- Method: `GET`
- Query parameters: `limit=1000`, `offset=0`, `onlyData=true`,
  `totalResults=true`

Use the returned total-result count to verify that the response contains the
entire result set. If it indicates more than 1,000 attributes, continue with
the documented paged GET sequence before validation; never validate against a
partial response. Persist a sanitized discovery snapshot with the configuration
blueprint, excluding environment URLs, credentials, tokens, and other secret
material.

Treat the returned attribute name as the sole allowed user-facing identifier.
A requested attribute name must exactly match an `AttributeName` returned by
the complete discovery response. The returned attribute code is internal
resolution data only and must not be shown as the user-facing identifier.

`RevisionRequiredFlag` is the live representation of this preference: true
means Required and false means Not Required. Use it to show the current and
intended states in the preview. Map each complete discovery line as follows:
`AttributeCode` to `AttributeEntity`, `CategoryCode` to
`AttributeGroupCode`, Required to `AttributeValue: Y`, Not Required to
`AttributeValue: N`, and the selected live action's value type to `DataType:
VARCHAR`. Do not use `RevisionPreferenceAttributeFlag` or an FSM
`AttributeStringValue`.

Normalize the input alias `SunInventoryCode` to the returned attribute name
`Subinventory code` before attribute-name validation. If `Subinventory code`
is not returned, stop and report that the attribute is unavailable; do not
infer an alternate attribute.

## Preference Input and Value Normalization

Accept exactly one preference for each requested attribute:

| User-facing preference | Normalized meaning | Preview value |
|---|---|---|
| Required | Require a revision for the attribute | true |
| Not Required | Allow the attribute to be updated without a revision | false |

Interpret `Required` and `Not Required` semantically in the language used by
the requester. Normalize an unambiguous localized equivalent to one of the
two canonical meanings before validation; retain the original localized value
in the preview for review. Do not accept a third state, an ambiguous
translation, a boolean literal, or `Y`/`N` as user input. Ask for clarification
when the language or phrase cannot be mapped unambiguously to `Required` or
`Not Required`.

Validate the normalized value before group expansion. The Data Loader workflow
selects the registered route; do not substitute an FSM row
contract, generic flat sample, or guessed representation.

## Grouped Attribute Rules

Some configuration values are atomic groups. Resolve every group member by its
returned attribute name. A request for any member sets the same preference on
every available member of that group:

| Group | Internal group members |
|---|---|
| Fulfillment organization, subinventory, supplier site, and supplier | RequestedFulfillmentOrganizationId; SubInventoryCode; SupplierSiteId; SupplierId |
| Override schedule and scheduled dates | OverrideScheduleDateFlag; ScheduleArrivalDate; ScheduleShipDate |
| Ship-to details | ShipToAddress; ShipToContact; ShipToContactMethod; ShipToCustomer |

After alias and localization normalization, reject a request that supplies
different preferences for members of the same group. Expand a valid single
member request to all available group members. If a required group member is
not returned by discovery, stop before Data Loader source preparation and
report the incomplete group.

## Preflight Checks

Before preparing a Data Loader source or making a live Fusion write, confirm
all of the following:

1. The request has one exact live attribute name and one unambiguous Required
   or Not Required preference; normalize the preference to true or false.
2. The configured target environment is identified, the operator has
   `FOM_MANAGE_REVISION_PREFERENCES`, and the prerequisite Redwood feature is
   either confirmed by a successful lookup or attested by the requester.
3. A fresh `omSalesOrderAttributePreferences` discovery is complete, contains
   every requested group member exactly once, and uses `totalResults`, returned
   item count, and `hasMore` to prove completeness.

4. The prepared DAT/ZIP is validated against the declared source contract,
   immutable,
   and has a recorded SHA-256.
5. Core Data Loader preflight and every applicable Task Hook rule result have
   passed for the exact immutable ZIP.
6. Before the first upload or initiation, present the target environment,
   group expansion, intended Required/Not Required states, source hash, and
   exact source to the requester, then obtain explicit approval bound to that
   unchanged source.

Stop before side effects when any check fails. Classify and persist the
sanitized diagnostic using the failure and safety rules below.

## Business Object Preparation and Import Workflow

1. Run the complete read-only discovery contract to validate each user-facing
   attribute name, determine its current `RevisionRequiredFlag`, and expand
   grouped requests.
2. Download the current live template through `core.data-loader` before
   preparing a source. It must resolve the
   `omSalesOrderAttributePreferences` Business Object and its `attributes`
   section. Do not copy a prior DAT or invoke a task-local source-builder.
3. Produce a human-reviewable preview showing returned attribute names,
   requested/localized preference, normalized Required/Not Required value, and
   group expansion. Do not show internal attribute codes.
4. Render the DAT using the following source contract. It is the task's
   declared live-template mapping, not a generic sample. Preserve the section,
   field, and field-value order exactly.

   ```text
   METADATA|omSalesOrderAttributePreferences|actionCode|RestAction
   MERGE|omSalesOrderAttributePreferences|REVISION_PREFERENCES|POST
   METADATA|attributes|AttributeEntity|AttributeGroupCode|AttributeValue|DataType|actionCode|RestAction
   MERGE|attributes|<AttributeCode>|<CategoryCode>|<Y-or-N>|VARCHAR|REVISION_PREFERENCES|POST
   ```

   Create exactly one child `MERGE` row for each resolved attribute. Substitute
   `AttributeCode` and `CategoryCode` only from the complete live discovery
   response. Substitute `Y` for Required and `N` for Not Required. Each
   `AttributeEntity` must be unique; every value must be nonblank and contain
   no `|`, carriage return, or newline. Do not use the template's
   `SAMPLE_CODE`, `SAMPLE_VALUE`, or generic `POST` sample rows as source data.
   The root and child action values above are fixed by this task contract.
5. Save the rendered file with the exact name
   `omSalesOrderAttributePreferences.dat`. `core.data-loader` resolves the
   business object from this filename. Use it to validate the DAT and produce
   an immutable ZIP that contains exactly that one DAT member; do not use a
   task-local DAT builder.
6. Use `core.data-loader` to create its persisted preflight for that exact ZIP.
   Perform no upload or initiation at this stage.
7. Invoke the `core.data-loader` Task Hook for the same preflighted ZIP,
   execute every applicable input, discovery, and group rule, and retain its
   local pre-upload approval preview.
8. Obtain explicit approval immediately before `core.data-loader` uploads and
   initiates the exact validated DAT/ZIP through the registered
   `omSalesOrderAttributePreferences` route. Do not use an FSM ZIP, a generic
   flat DAT row, or a direct REST PATCH.
9. After the Data Loader operation completes, repeat read-only discovery and
   verify the affected attributes' `RevisionRequiredFlag` values. Record the
   sanitized verification result and source identity in the project workspace.

## Failure and Safety Rules

- Stop on an unavailable attribute name, ambiguous localized preference,
  conflicting group preference, incomplete group, incomplete discovery page,
  or an unregistered or ambiguous Data Loader Business Object contract.
- Classify discovery failures as auth/authz, transport/environment, or Fusion
  API failures. A 401 or 403 may be retried once only through the workflow's
  cached-token refresh path; do not retry an import automatically.
- Treat Data Loader validation, upload, initiation, or verification failure as
  a failed or partial result. Preserve sanitized diagnostics, the immutable
  source reference, the last status, and the next safe action under the
  project workspace.
- Never upload, initiate, or retry a failed Data Loader operation without a
  fresh approval for the exact immutable source.

## Source Traceability

- Oracle readiness source: [Redwood: Update Attributes and Flexfields Without Revising the Order](https://docs.oracle.com/en/cloud/saas/readiness/scm/26a/order26a/26A-order-mgmt-wn-f41987.htm)
- Attribute eligibility source at execution time: the complete read-only
  `omSalesOrderAttributePreferences` discovery response defined above.




## Implementation Notes

Use the parent functional-area skill `scm.order-management.orders` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
