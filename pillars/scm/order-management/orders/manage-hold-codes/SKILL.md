---
skill_id: "scm.order-management.orders.manage-hold-codes"
name: "Manage Hold Codes Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Hold Codes under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "DOO_MANAGE_HOLD_CODE"
task_name: "Manage Hold Codes"
parent_skill_id: "scm.order-management.orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "omHoldDefinitions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.1.38"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.auth.fusion-oauth-authentication"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-hold-codes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-hold-codes/current/"
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
  - "Reads Fusion hold-definition, role, set, and task metadata when the active workflow selects the documented read-only discovery, preflight, or verification steps."
  - "Prepares Data Loader artifacts for hold-code changes; upload and import are Fusion mutations performed only through core.data-loader after its required approval workflow."
required_privileges:
  - "Privileges to view Order Management hold definitions and the referenced roles, reference sets, and task definitions in the selected Fusion environment."
  - "Privileges required by core.data-loader to validate, upload, initiate, and inspect the omHoldDefinitions data load when execution is approved."
---

# Manage Hold Codes Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Hold Codes` under `Orders`.

## Setup Task Skill Contract

- task_code: `DOO_MANAGE_HOLD_CODE`
- task_name: `Manage Hold Codes`
- parent_skill_id: `scm.order-management.orders`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Orders`
- functional_area_code: `ORA_DOO_ORDER_FULLFILLMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `omHoldDefinitions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Hold Codes` under `Orders`.

## Setup Task Metadata

- Task name: `Manage Hold Codes`
- Task code: `DOO_MANAGE_HOLD_CODE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `omHoldDefinitions`

## Hold Definition Guidance

Use the Redwood **Manage Hold Codes** setup task to define unique holds with
codes, descriptions, types, business-unit applicability, task applicability,
and apply/release role permissions. A hold can be generic for all task types or
restricted to specific task types and roles.

Apply these design constraints before preparing an import artifact:

- Hold names must be unique. Each `HoldCode` plus
  `OrchestrationApplicationId` combination must also be unique; the same hold
  code is allowed when it belongs to a different orchestration application.
- Start and end dates must be logically ordered.
- A task-specific hold requires at least one task; Pause is not an eligible
  task.
- Holds already applied to sales orders cannot be deleted or end dated.
- Change-request holds are predefined and read-only.
- A role-specific apply or release permission requires at least one role.

## Creation Defaulting

For a new hold definition, always set `EffectiveStartDate` from the current
UTC calendar date before archive generation, formatted as `YYYY-MM-DD` (for
example, UTC `2026-08-28` remains `2026-08-28`). Do not use slash-delimited
or locale formats, timestamps, a Fusion-environment-local date, or a stale
value from a prior sample or run. Do not defer this default to immutable-preview
generation: it must be present in the final Data Loader source and approval
preview.

For a new hold definition, if the source omits either role-eligibility value,
default both `ApplyHoldRoleEligibility` and `ReleaseHoldRoleEligibility` to
`A`, meaning all roles. Include each resolved value in the immutable approval
preview. An explicit `R` overrides this default and requires the corresponding
role mappings in the Data Loader source.

For a new hold definition, omit `HoldCodeId` from the parent Data Loader
record. The business object generates the identifier in the backend. Do not
preallocate, validate for nonexistence, infer, or submit a client-supplied
hold-code ID for a create.

For a create with child records, use only the parent-child relationship
mechanism supported by the current live `omHoldDefinitions` Data Loader
template. Do not require a generated parent `HoldCodeId` in a child record
before the load. If the live template cannot express the requested child
relationship without a server-generated ID, stop with
`catalog_or_metadata_mismatch` and obtain the updated template or business
object guidance; do not fall back to a REST mutation or invent a linkage key.

## Orchestration Application and Hold-Code Uniqueness

Accept `OrchestrationApplicationId` as the application identifier; do not
accept or resolve an `Application` name or code. If the requester does not
specify `OrchestrationApplicationId`, silently default it to `10008` (Order
Management). Include the supplied or defaulted value and its Order Management
meaning in the approval preview.

Before a create, use a read-only `omHoldDefinitions` lookup to verify that no
existing hold has the same exact `HoldCode` and `OrchestrationApplicationId`.
The same `HoldCode` may be created for a different
`OrchestrationApplicationId`. For an update, confirm that the combination
identifies only the intended existing hold. If the identifier is missing,
ambiguous, or the uniqueness check is unavailable, stop before archive
generation with an `input_validation`, `catalog_or_metadata_mismatch`, or
`transport_or_environment` failure. Never submit a guessed application ID.

For a new hold definition, `SystemFlag` must be `false`. Do not inherit,
generate, or submit a `true` value for this field; include the resolved value
in the approval preview.

## Role Resolution

Accept role names as the requester input for role-specific apply or release
eligibility. Before building an approval archive, use the read-only live Fusion
`/hcmRestApi/resources/11.13.18.05/rolesLOV` resource to resolve every
requested exact `RoleName` to exactly one canonical numeric Fusion `RoleId`
accepted by the `accessRoles` child resource. Do not use HCM SCIM Roles for
this resolution.

Do not use an HCM SCIM role UUID, a display-name string, a cached identifier,
or a guessed value in the `RoleId` field. Validate that the resolved identifier
is a positive numeric Fusion identifier and that it belongs to the requested
exact role name. Whenever a `RoleId` is shown in an approval preview,
diagnostic, or user-facing response, show its exact `RoleName` beside it.
Retain the same name-and-ID pair in the redacted resolution diagnostic.

If any role name is missing, unknown, ambiguous, resolves to a nonnumeric ID,
or the live role lookup is unavailable, stop before archive generation with a
`catalog_or_metadata_mismatch` or `transport_or_environment` failure. For an
existing hold, enumerate the current `accessRoles` mappings before generating
the Data Loader child records; use the resolved numeric ID for every child
create or update.

## Role-Restricted Hold Creation

Route every new hold, including a task-specific, role-restricted hold, through
`core.data-loader`. Complete the normal immutable source, validation, Task
Hook, approval, upload, initiation, and status workflow; do not use direct
REST `POST` to create `omHoldDefinitions` or either child resource.

Build the source from the live `omHoldDefinitions` Data Loader template and
preserve its parent-before-child section structure. Set `RestAction` to `POST`
in each populated parent, `serviceMappingDetails`, and `accessRoles` section.
Omit `HoldCodeId` from a new parent record because the backend generates it.
Use only relationships and key values permitted by the validated template for
each child create record. If the validated Data Loader contract cannot express
the requested relationship without a pre-existing parent ID, stop with
`catalog_or_metadata_mismatch`; do not fall back to direct REST.

For a service-mapping create record, include the template-supported parent
linkage plus the resolved `ServiceId`, exact `TaskTypeName`, and exact
`TaskTypeId`. Do not populate `serviceMappingDetails.HoldCodeId` unless the
current live template explicitly requires and supports it for a new parent
whose ID is generated by the backend.

Before generating the immutable approval preview, complete all read-only
preflight checks in this skill: resolve the exact `SetCode`, task definition,
and numeric role IDs; confirm the hold-code/application pair is unused; and
validate that the requested roles are distinct action mappings where required.
Use only the supplied `OrchestrationApplicationId` or the `10008` Order
Management default.

Include the resolved service and task fields for the requester-selected task and
create separate apply-only and release-only role records. An apply-hold role record uses
`ApplyHoldFlag: "Y"` and `ReleaseHoldFlag: "N"`; a release-hold role record
uses `ApplyHoldFlag: "N"` and `ReleaseHoldFlag: "Y"`.

Complete the immutable Data Loader approval gate immediately before upload, and
do not retry a failed upload or initiation. After Data Loader initiation, verify
the created hold with the read-only workflow using
`expand=accessRoles,serviceMappingDetails`. Confirm the resolved service and task
mapping, both action-specific role records, and both role-eligibility values; persist the
redacted verification diagnostic and returned parent ID.

For the Data Loader source, an apply-hold role
record uses `ApplyHoldFlag: "Y"` and `ReleaseHoldFlag: "N"`; a release-hold
role record uses `ApplyHoldFlag: "N"` and `ReleaseHoldFlag: "Y"`. Create a
separate child record for each requested action, including when the same
resolved role is assigned to both apply and release.

## Set Selection

Accept only `SetCode` as user input for a hold definition's reference set. Do
not accept, infer from the requester, or preserve caller-supplied `SetId` or
`SetName` values for creates or updates.

Before building an immutable approval artifact, the active workflow must use
the read-only, intent-scoped Fusion `omSetIdSetsLOV` resource to resolve the
supplied `SetCode` to exactly one authoritative `SetId` and `SetName`.
Use the configured Fusion host and the active REST route for
`/fscmRestApi/resources/11.13.18.05/omSetIdSetsLOV` with
`finder=IntentFinder;Intent=DOO_MANAGE_ORCHESTRATION_HOLD_CODE_DEFINITION_DATA`.
Request `SetCode,SetId,SetName`, order by `SetCode`, follow pagination, and
resolve the supplied value against returned `SetCode` values only. Prefer one
case-sensitive exact match. When none exists, accept one case-insensitive exact
`SetCode` match automatically and use its canonical returned casing; do not ask
the requester to confirm that normalization. Record both the supplied and
canonical codes in the redacted resolution diagnostic and use the canonical
code in the immutable approval preview. Do not use `SetName` as a match
candidate, or use `setIdSets`, `setIdSetsLOV`, BOSS Set ID Sets, a current hold
record, cache, or schema validation as a substitute.

Whenever a set identifier is shown, show `SetName`, `SetCode`, and `SetId`
together. Whenever a task or service identifier is shown, show its exact
`TaskTypeName` or `ServiceName` beside `TaskTypeId` or `ServiceId`. Apply this
convention in previews, diagnostics, and user-facing responses.

If the code is missing, unknown, yields multiple case-insensitive `SetCode`
matches, or the live reference lookup is unavailable, stop before archive generation with a
`catalog_or_metadata_mismatch` or `transport_or_environment` failure. Do not
submit a guessed identifier or name.

Source: [Redwood: Manage Hold Definitions](https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/order26c/26C-order-mgmt-wn-f46377.htm).

## Task Definition Resolution

For every task-specific hold, resolve the requester-supplied exact task name
through the read-only, live Fusion `omHoldTaskDefinitions` resource before
preparing any parent or service-mapping artifact. Use the configured Fusion
host and the active REST route for
`/fscmRestApi/resources/11.13.18.05/omHoldTaskDefinitions`.
Request `CheckHoldsFlag,ServiceCode,ServiceId,ServiceName,TaskTypeId,TaskTypeName`,
order by `TaskTypeName`, follow pagination, and require exactly one record with
the requested exact `TaskTypeName`. Validate that `ServiceId` and `TaskTypeId`
are positive numeric Fusion identifiers and retain the returned service and
task names alongside their identifiers for the approval preview.

Do not infer a task mapping from an existing hold definition, a cached mapping,
or another task type. A missing, ambiguous, inactive, or nonnumeric mapping is
a `catalog_or_metadata_mismatch` blocker. Do not create a parent archive or
service-mapping record until the task definition resolves.

## Data Loader and Read-Only REST Mapping

The registered Data Loader business object is `omHoldDefinitions`. Route every
create, update, and delete through `core.data-loader`'s standard immutable
artifact, approval, upload, initiation, and status workflow.

`core.fusion-api.rest-api-client` is permitted only for read-only discovery,
preflight, and verification against the configured resource:

```text
https://<fusion-host>/fscmRestApi/resources/11.13.18.05/omHoldDefinitions
```

For collection and resource `GET` operations, pass only explicit query
parameters supported by the OpenAPI contract: `q`, `fields`, `expand`,
`limit`, `offset`, `orderBy`, `onlyData`, and `totalResults`, with
`Accept: application/json`.

Example read-only request for one hold with its related access roles and
service mappings:

```text
GET /omHoldDefinitions/<hold-code-id>?expand=accessRoles,serviceMappingDetails
Accept: application/json
```

## Mutation Routing

All creates, updates, and deletes are Data Loader-only, including parent
attributes, task/service mappings, role mappings, and apply/release
eligibility. Do not combine a Data Loader import with REST mutations for this
task.

For update and delete sources, include the exact existing hold-definition key
and required child keys from the read-only lookup. A source mapping change,
including any changed identifier or operation, invalidates the preview and
requires a new approval.

For every parent `omHoldDefinitions` `PATCH` record, populate every updatable
parent attribute from the current read-only hold-definition response, even when
that value is unchanged. Preserve the live values for the orchestration
application, hold code, name, description, generic-hold flag, effective dates,
service-mappings flag, reference-set fields, role-eligibility fields, and any
other parent attributes that the validated Data Loader template marks
updatable; change only the attributes requested by the user. Do not create a
sparse parent patch with placeholder empty fields. Before archive generation,
verify that the parent data row has exactly the same number of values as its
`METADATA|omHoldDefinitions` header and represent false/true values in the
template's accepted format.

## Existing-Hold Role Updates

Route every existing-hold role or eligibility update through `core.data-loader`.
This includes `accessRoles` creates, updates, and deletes; changes to
`ApplyHoldRoleEligibility` or `ReleaseHoldRoleEligibility`; and all related
service-mapping changes. Do not use direct REST `POST`, `PATCH`, or `DELETE`
against an existing hold or either child collection. Prepare one immutable Data
Loader archive, obtain its separate approval, and verify the imported result.

For an `accessRoles`-only update or delete, include an
`omHoldDefinitions` parent section and complete parent `PATCH` record before
the child records, following the parent-patch rule above. The parent record
must contain the exact existing `HoldCodeId` and applicable parent
`RestAction`. Do not submit a child-only DAT because the Data Loader upload
validator requires a registered top-level business object.

For an existing `accessRoles` delete, identify the record by the exact parent
`HoldCodeId`, exact `RoleId`, action flags, and exact `HoldAccessRoleId` from
the live expanded hold response. Always populate that `HoldAccessRoleId` in the
Data Loader delete row; Fusion requires this local child key for the delete
operation. For an apply-access deletion, set `ApplyHoldFlag` to `Y`; for a
release-access deletion, set `ReleaseHoldFlag` to `Y`. Include the other action
flag as `N`. Do not populate `ServiceMappingIds` in an `accessRoles` delete
row: it is not an `accessRoles` key and must be omitted, including as an empty
placeholder. If the live response does not yield exactly one matching action
record, stop with `catalog_or_metadata_mismatch`.

One `DOO_HOLD_CODE_ACCESS_ROLES` / `accessRoles` record can grant both apply
and release access to the same role, with both flags set to `Y`. For a request
to remove apply-hold access, find the exact hold-and-role record whose
`ApplyHoldFlag` is `Y`, then patch only `ApplyHoldFlag` to `N` while preserving
the current release flag. For a request to remove release-hold access, patch
only `ReleaseHoldFlag` to `N` while preserving the current apply flag. Delete
the record only when the resulting values of both flags are `N`. Enumerate the
live role records first; do not infer a separate row for apply and release.
For new role rows, leave the generated `HoldAccessRoleId` empty and supply the
resolved `RoleId`.

Include `serviceMappingDetails` in the Data Loader source only when the
requested change creates, updates, or deletes a service/task mapping. For
role-only, eligibility-only, set-only, or other parent-only changes, omit the
entire `serviceMappingDetails` section, including its `METADATA` header; do
not emit a header-only section.

## Task-Specific-to-Generic Hold Transitions

Route a request to change an existing task-specific hold to a generic hold
through `core.data-loader`. First use the read-only expanded hold response to
enumerate every current `serviceMappingDetails` record and obtain the exact
child identifiers required by the validated Data Loader business-object
contract. Prepare one immutable archive that deletes every enumerated service
mapping and includes a complete parent `omHoldDefinitions` `PATCH` record
that sets `GeneralHoldFlag` to `true` and `HasServiceMappingsFlag` to `false`.
Preserve every other updatable parent value from the live response as required
by the parent-patch rule; do not use a sparse conversion patch or delete the
parent hold.

For a request to remove one task association, enumerate the complete current
mapping collection before archive generation. If the target is the last
remaining service mapping, use the same task-specific-to-generic conversion:
delete that mapping and set the parent `GeneralHoldFlag` to `true` and
`HasServiceMappingsFlag` to `false` in the same immutable archive. If one or
more mappings remain, delete only the requested mapping and retain the live
non-generic parent values. Stop with `catalog_or_metadata_mismatch` if the
target mapping cannot be identified exactly or the expected remaining mapping
count does not match the live response.

Use the child-record identity and parent/child record order required by the
currently validated Data Loader template. After the approved import completes,
fetch the hold with `serviceMappingDetails` expanded and verify that a generic
conversion has `GeneralHoldFlag=true`, `HasServiceMappingsFlag=false`, and no
remaining service mappings. Do not retry a failed import automatically.

## Delete Through Data Loader

Prepare every deletion as a Data Loader `delete` operation. Do not send an
ADF batch or a direct HTTP `DELETE` request.

Before preparing a deletion artifact, use the read-only GET workflow to
confirm all of the following:

1. The exact hold definition and target environment are correct.
2. `InUseFlag` is not `true`; holds applied to sales orders cannot be deleted.
3. `SystemFlag` is not `true`, and the hold is not a predefined change-request
   hold.
4. All affected access-role and service-mapping child records have been
   enumerated with their exact identifiers.
5. The Data Loader source includes child-delete records before the parent when
   the validated loader contract does not support parent cascading.

For an `accessRoles` patch, preserve `HoldCodeId`, `RoleId`, and the exact
existing `HoldAccessRoleId` required by the validated business-object contract.
Set the requested action flag to `N` and preserve the other flag. Use an
`accessRoles` delete only if both resulting action flags are `N`.

The immutable archive must preserve that validated record order. A failed
delete must stop the Data Loader workflow, preserve the returned diagnostic,
and never be retried automatically.

Use `GET` only for approved read-only baseline, lookup, and validation work.

## Read-Only Hold Code Fetch Workflow

Use this workflow when the requester asks to retrieve hold codes. It is limited
to the `GET` operations in the table above and must not send a request body or
perform a state-changing operation.

1. Confirm the selected Fusion environment and that the authenticated user has
   permission to view Order Management hold definitions. Read the environment
   from `core/auth/fusionEnv.properties`; do not copy its host or OAuth values
   into project artifacts or the response.
2. Use `core.auth.fusion-oauth-authentication` for OAuth handling and
   `core.fusion-api.rest-api-client` for the request. The client uses the
   configured `restBaseUrl`, protects the token cache, and retries one rejected
   authentication response at most once.
3. Fetch the collection through the standard REST client using the
   environment-specific OpenAPI base path. Optional collection filters and
   pagination values must be passed as explicit query parameters, never
   concatenated into the endpoint.

   ```bash
   python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
     /fscmRestApi/resources/11.13.18.05/omHoldDefinitions \
     --method GET \
     --header "Accept: application/json" \
     --header "REST-Framework-Version: 9"
   ```

4. For a specific known identifier, replace the endpoint suffix with
   `/{holdCodeId}` and keep `--method GET`. Validate that the identifier
   is a positive numeric Fusion identifier before issuing the request.
5. Return only the requested hold-code fields and operationally useful status;
   redact or omit personal, role, and environment-sensitive data that is not
   needed for the request. Record an audit summary with the environment alias,
   endpoint path, method, result status, and timestamp, without credentials,
   tokens, or raw authorization headers.
6. If authorization fails, report the failure classification and required
   Fusion privilege; refresh OAuth once only when the client identifies a 401
   or 403. Do not retry non-authentication failures automatically.

For every existing-hold mutation, follow `core.data-loader`, validate the IDs
and source data, and obtain the required approval immediately before execution.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using omHoldDefinitions as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Orders`
- Setup task name: `Manage Hold Codes`
- Setup task code: `DOO_MANAGE_HOLD_CODE`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `omHoldDefinitions` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "omHoldDefinitions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.order-management.orders` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
