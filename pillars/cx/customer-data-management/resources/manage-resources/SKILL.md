---
skill_id: "cx.customer-data-management.resources.manage-resources"
name: "Manage Resources Setup Task Guidance"
description: "Routes ResourceUser CX Import and Export, exact read-only Resource Users lookups, direct reportees, and eligible post-import ESS processing for Manage Resources under Customer Data Management Resources."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Resources"
functional_area_code: "ORA_CRM_RESOURCES"
task_code: "HZ_MANAGE_RESOURCES"
task_name: "Manage Resources"
parent_skill_id: "cx.customer-data-management.resources"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "CXIMPORT"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.24"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "resource_import_source"
  - "cx_import_object_code"
  - "cx_import_mapping"
  - "data_load_status_request"
  - "remaining_rows_validation_confirmation"
  - "reporting_hierarchy_tree_version_id"
  - "ldap_user_type"
  - "ldap_batch_size"
  - "resource_operation"
  - "resource_export_job_name"
  - "resource_export_filter"
  - "resource_export_columns"
  - "resource_export_output_options"
  - "resource_export_activation_choice"
  - "resource_user_get"
  - "resource_user_reportees"
  - "resource_email"
  - "manager_resource_email"
  - "manager_party_name"
  - "resource_party_number"
  - "polling_request"
  - "execution_approval"
  - "post_import_ess_execution_approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "unresolved_resource_role_codes"
  - "data_load_preview"
  - "data_load_request_id"
  - "data_load_status"
  - "post_import_ess_summary"
  - "reporting_hierarchy_handoff"
  - "reporting_hierarchy_request_id"
  - "ldap_request_id"
  - "export_activity_summary"
  - "export_download_path"
  - "resource_user_reportees_summary"
  - "diagnostics"
  - "audit_summary"
  - "post_import_ess_approval_audit"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.data-loader"
  - "core.data-loader.task-hook"
  - "core.fusion-api.cx-import-export-management"
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
depends_on:
  - "cx.customer-data-management.resources.run-reporting-hierarchy-generation"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/manage-resources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/manage-resources/current/"
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
  - "Delegates approved ResourceUser CX Import initiation to core.data-loader."
  - "Delegates approved ResourceUser Export Management activity creation and activation to core.fusion-api.cx-import-export-management."
  - "Delegates eligible Reporting Hierarchy Generation to its dedicated skill after a successful ResourceUser completion status confirms hierarchy changes and fresh post-import approval is explicit."
  - "Submits Send Pending LDAP Requests after a successful ResourceUser completion status confirms eligible user-account creation, readiness checks pass, and fresh post-import approval is explicit."
required_privileges: []
---

# Manage Resources Setup Task Guidance

## Purpose

Provides ResourceUser-specific import and export routing for `Manage Resources` under `Customer Data Management Resources`.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_RESOURCES`
- task_name: `Manage Resources`
- parent_skill_id: `cx.customer-data-management.resources`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Resources`
- functional_area_code: `ORA_CRM_RESOURCES`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Resources` under `Customer Data Management Resources`.

## CX Resource Import and Export Contract

Use `core.data-loader` for ResourceUser CX Import and
`core.fusion-api.cx-import-export-management` only for ResourceUser Export
Management.

- CX Import object code: default to `ResourceUser` when this Manage Resources
  workflow receives an import without a valid CX mapping CSV. A mapping CSV's
  `IMPORT OBJECT` is authoritative. Stop for clarification if the caller
  explicitly requests a different object code.
- CX Import source: one CX ZIP or one or more direct CSV files. Data Loader
  resolves the UCM account from live object metadata; do not hard-code or
  accept a caller-supplied UCM account or `InputFileContentId`.
- Export Management object: `ResourceUser`.
- Export options: caller-supplied column names, filter criteria, mapping, file,
  output settings, polling duration, and optional local download path.

The FSM catalog flags below describe setup-task export/import support. They do
not prohibit this separate CX Import or Export Management workflow.

## Setup Task Metadata

- Task name: `Manage Resources`
- Task code: `HZ_MANAGE_RESOURCES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`

## FSM Setup-Data Boundary

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

The CX REST export workflow is separate from that FSM setup-data capability.

## CX ResourceUser Import and Export Routing

All delegated Fusion REST calls in this task, including the ResourceUser role,
parent, and hierarchy lookups, must include `Rest-Framework-Version: 9`.

## Direct Reportees Lookup

Use the read-only `resource_user_reportees` operation for requests such as
"direct reportees of <manager>" or "resources reporting to <manager>."

The request must supply exactly one manager `ResourceEmail` or exact manager
`PartyName`. Resolve the manager to one complete Resource User with a nonblank
email, then list Resource Users whose `ResourceOrgManagerEmail` exactly equals
that resolved email. Retrieve every page and retain only current resources
(blank or future `ResourceEndDate`).

This branch is read-only: it does not use Data Loader, a preview, approval,
POST/PATCH, Reporting Hierarchy Generation, or Send Pending LDAP Requests.
Return an explicit empty list when the manager has no current reportees. Do not
infer reportees from a shared organization, role name, or hierarchy position.

## Read-Only Resource Users and Backport Boundary

Use `resource_user_get` for exactly one existing Resource User identified by
ResourceEmail or ResourcePartyNumber. Resolve one complete visible match through
`core.fusion-api.rest-api-client` and return only requested authorized fields.
Use `resource_user_reportees` for the separate read-only direct-reportees route.
Neither read branch enters Data Loader, preview, approval, or post-processing.

This 26.10 backport does not route one-resource create, update, promotion,
demotion, transfer, end-date, or permanent deletion through Resource Users
REST Data Loader. The required Data Loader REST business-object seed is not
assumed to be available. Do not substitute direct Resource Users POST/PATCH or
construct a one-resource Data Loader source. For resource creation or updates,
use the documented ResourceUser CX Import only when the caller supplies a CSV
or CX ZIP source; otherwise stop and request a supported import source.
Standalone organization-membership changes remain outside the one-resource
route. ResourceUser CX Import retains its documented CSV membership fields.

Use the following task-specific routing. Do not duplicate either core skill's
command templates, OAuth workflow, UCM upload mechanics, or API calls.

- For `resource_user_reportees`, use only
  `core.fusion-api.rest-api-client` for the documented Resource Users GET
  lookups. This operation is separate from CX Import and Export Management.

- For `resource_user_get`, use only `core.fusion-api.rest-api-client` and the
  exact Resource Users identity lookup. Return the requested authorized fields
  from one complete result; stop on zero, multiple, incomplete, or unauthorized
  results. Do not route this operation to Data Loader.

- For import, use the `core.data-loader` CX Import route. Begin with the
  immutable preview using `upload_and_initiate.py` and `--cx-import`, without
  `--approve-upload`. Direct CSV groups use repeated `--ide-file` inputs. For a
  source without a valid CX mapping CSV, default the object code to
  `ResourceUser` and pass `--cx-import-object-code ResourceUser` to Data
  Loader. Do not override a valid mapping CSV's `IMPORT OBJECT`. If the caller
  explicitly names a different object code, stop for clarification rather than
  substituting `ResourceUser`. Data Loader must read
  `objectMetadata/ResourceUser?fields=UcmAccount&onlyData=true` during preview
  and approval, and use that returned nonblank account for all CX uploads.
  For each import row, map `Role` to `ResourceOrgRoleCode` when an
  `Organization` is supplied. Use `IndividualRoleCode` only when the caller
  explicitly identifies the role as individual; otherwise stop for role-routing
  clarification.
  A single CSV may contain parent and dependent ResourceUser rows when every
  parent row is listed before each row that references it. Validate the ordered
  dependency chain before preview; do not split a correctly ordered file solely
  because it contains parent and child resources.
  Before preview, select only the first 10 non-header CSV rows in source order.
  Collect distinct nonblank `ResourceOrgRoleCode` and `IndividualRoleCode`
  values from that sample only. Use
  `core.fusion-api.rest-api-client` to retrieve active roles from
  `GET /crmRestApi/resources/11.13.18.05/resourceRoles` with
  `finder=AllActiveResourceRolesRowFinder`, an exact `q` predicate that joins
  all distinct sampled role codes with `OR`, and
  `Rest-Framework-Version: 9`. Compare the returned `RoleCode` values. A code
  is valid only when returned by this exact active-role lookup. Preserve the
  routing context (`ResourceOrgRoleCode` or
  `IndividualRoleCode`) but never include source row details in diagnostics.
  If any distinct code is unresolved, block the import and report a sanitized,
  de-duplicated list of unresolved codes by routing context. Do not submit a
  partial import.
  Collect `ResourceOrgManagerEmail` values from the same first 10 rows only.
  An earlier sampled parent row satisfies the dependency; otherwise use the
  exact parent lookup below. Do not look up role codes or manager emails from
  rows after the first 10. Inform the user that only the first 10 rows were
  validated and require explicit confirmation to proceed for all remaining
  rows. Record that the result is a first-10-row sample, not full-file
  reference validation. This confirmation permits normal import preview and
  approval only; it does not initiate the data load.
  For every parent email referenced by `ResourceOrgManagerEmail` that is not
  supplied by an earlier CSV row, use the exact ResourceUser lookup
  `GET /crmRestApi/resources/11.13.18.05/resourceUsers?q=ResourceEmail='<email>'`
  through `core.fusion-api.rest-api-client` with `Rest-Framework-Version: 9`.
  Require exactly one returned item
  whose `ResourceEmail` exactly matches the requested email. Do not infer a
  missing parent from an unfiltered, partial, or paginated collection request.
  A zero-result lookup establishes only that the parent is not visible to the
  calling principal; stop for confirmation rather than reporting that the
  parent is absent from the target environment. Treat multiple results, a REST
  error, or an incomplete response as inconclusive and stop for resolution.
- For export, use `operation=create-export` and `ExportObject=ResourceUser`.
  Pass a unique job name, a caller-provided filter on the top-level object,
  optional selected columns and output settings, the activation choice, and an
  optional local download path.
For ResourceUser CX Import, after the non-write rules finish, use
`core.data-loader.task-hook` to build the
data-load preview with the final archive SHA-256 and ordered rule results. Only
after explicit approval, approve and verify that preview to produce the exact
task-validation envelope. Immediately before the first POST, rerun the same
immutable source with `--cx-import`, `--task-routed`, the verified
`--task-validation-envelope`, `--approve-upload`, and
`--approved-sha256 <complete-preview-sha256>`.

Data Loader initiation is not import completion. Do not poll automatically.
Only when the user explicitly asks for status, results, counts, or errors, use
the Data Loader status route. Once that route—or another selected completion
check—confirms a successful completed ResourceUser load, continue directly into
post-import ESS routing.

Do not end a successful import result before post-import routing. Independently
validate eligibility and readiness for Reporting Hierarchy Generation and Send
Pending LDAP Requests, then present the eligible job or jobs and ask for one
fresh `post_import_ess_execution_approval` to submit them. The import approval
never authorizes post-import ESS processing, and no ESS job is submitted until
that fresh approval is supplied.

## Post-Import ESS Routing

Only after a Data Loader completion check confirms a complete ResourceUser load
with successful rows, independently determine whether either documented
scheduled process is needed. Do not start a post-import process for an
initiated, unavailable, incomplete, or failed load.

- Reporting Hierarchy Generation applies when the import changes resource
  organizations or reporting-manager hierarchy. Resolve the active Tree Version
  ID through the lookup below, then hand off only the validated current-request
  values to `cx.customer-data-management.resources.run-reporting-hierarchy-generation`:
  `tree_structure_code=RESOURCE_ORG_TREE_STRUCTURE`,
  `tree_code=GLOBAL_SALES_MARKETING`, `tree_version_id=<validated ID>`,
  `submit=true`, target Fusion environment context, and successful
  import-completion evidence. Manage Resources must not construct, preview, or
  submit the Reporting Hierarchy `CrmEss` request. The receiving skill owns the
  application, job definition, ordered `submit.argument1` through
  `submit.argument3` bindings, final tree/version validation, ESS submission,
  and tracking. After that skill returns its preview, pass the fresh approved
  Reporting Hierarchy item as its required `execution_approval`.
- Evaluate `CreateUserAccountFlag` across every imported row before deciding
  Send Pending LDAP Requests. Suppress the LDAP job only when every row
  explicitly sets `CreateUserAccountFlag=N`; state that all rows suppress LDAP
  processing. If any row is absent or has a value other than `N`, ignore this
  suppression rule and submit the LDAP job without a flag-specific message.
  Invoke `core.fusion-api.ess-job-submitter` using the verified deployment
  contract: application `EarHcmEss`, job definition
  `JobDefinition://oracle/apps/ess/hcm/users/ProcessLdapRequests`, and these
  ordered request parameters:

  ```json
  [
    { "name": "submit.argument1", "paramType": "STRING", "value": "ALL" },
    { "name": "submit.argument2", "paramType": "STRING", "value": "ALL" },
    { "name": "submit.argument3", "paramType": "STRING", "value": "A" }
  ]
  ```

  The Oracle Scheduled Processes documentation identifies the business values
  `User Type=All` and `Batch Size=A` (automatic calculation). Bind them as
  `submit.argument1=ALL` and `submit.argument3=A`, respectively. Preserve the
  required middle value `submit.argument2=ALL` as part of the verified runtime
  contract; the Oracle page does not publish its technical argument name or UI
  label. Do not infer or rename that argument, substitute UI display labels for
  technical parameter names, or omit a parameter. The caller may override only
  a business value when its corresponding technical argument mapping is known
  and the resulting complete request is previewed before submission.

After the import result is successful, present a fresh post-import preview for
each eligible ESS job. The preview must identify the target environment,
purpose, application, job definition ID, and exact parameters. For Reporting
Hierarchy Generation, obtain those ESS details from the receiving skill's
validated preview; do not duplicate or infer its `CrmEss` contract locally.
Require `post_import_ess_execution_approval` immediately before submitting any
listed job. Pass the approved Reporting Hierarchy item to the receiving skill
as its required `execution_approval`; the import approval never authorizes
post-import ESS processing. Do not
perform a Scheduler active-instance lookup and do not accept a concurrency
override. Submit only the eligible jobs named in the current approval. When
both are approved, submit and poll them asynchronously and independently; an
unsuccessful job must not cancel monitoring of the other job.

For post-import Reporting Hierarchy Generation, use
`core.fusion-api.rest-api-client` to query
`GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions` for the selected Tree
Structure Code and Tree Code, with `Rest-Framework-Version: 9`. Use a candidate only when all conditions hold on
the target environment's current date: `Status=ACTIVE`,
`EffectiveStartDate` is on or before the current date, and `EffectiveEndDate`
is blank or on or after the current date. If no candidate or more than one
candidate meets these conditions, stop the ESS branch and record the returned
candidate metadata; do not select a version arbitrarily.

## Resource Guidance Routing

Use `ora-resource/ora_rule_registry.json` as the authoritative task-local
execution graph. It selects ResourceUser CX Import, Export Management, exact
single-resource GET, or direct reportees, with separate successful terminals. Use the following guidance files for the
selected branch:

- `ora-resource/ora_input_intake.md` for operation selection and runtime
  inputs.
- `ora-resource/ora_defaulting_rules.md` for ResourcePartyNumber import and export
  output defaults before validation.
- `ora-resource/ora_input_validation.md` for import or export input checks and
  result evaluation.
- `ora-resource/ora_dependency_readiness.md` for import prerequisites and
  export visibility dependencies.
- `ora-resource/ora_reference_lookups.md` for role, parent, direct-reportees,
  and hierarchy-version lookups.
- `ora-resource/ora_bulk_intake.md` for ResourceUser CSV mapping and bulk
  import preparation.
- `ora-resource/ora_design_enforcement.md` for supported import scope,
  duplicate-import, export-filter, and access-policy gates.
- `ora-resource/ora_rest_execution.md` for read-only GET and direct-reportees
  result branches plus import/export preview, approval, delegated execution,
  polling, download, and result-review gates.
- `ora-resource/ora_error_handling.md` for stop-before-retry behavior and
  post-import ESS outcomes.

These files define task-specific policy and branch routing. Delegate CX Import
preview, metadata lookup, UCM staging, initiation, and requested status checks
to `core.data-loader`; delegate only ResourceUser export creation, activation,
polling, and download to `core.fusion-api.cx-import-export-management`.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `resource_import_source`
- `cx_import_object_code`
- `cx_import_mapping`
- `data_load_status_request`
- `remaining_rows_validation_confirmation`
- `reporting_hierarchy_tree_version_id`
- `ldap_user_type`
- `ldap_batch_size`
- `resource_operation`
- `resource_export_job_name`
- `resource_export_filter`
- `resource_export_columns`
- `resource_export_output_options`
- `resource_export_activation_choice`
- `polling_request`
- `execution_approval`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `unresolved_resource_role_codes`
- `data_load_preview`
- `data_load_request_id`
- `data_load_status`
- `post_import_ess_summary`
- `reporting_hierarchy_request_id`
- `ldap_request_id`
- `export_activity_summary`
- `export_download_path`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.resources` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
