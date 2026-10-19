---
skill_id: "cx.customer-data-management.resources.run-reporting-hierarchy-generation"
name: "Run Reporting Hierarchy Generation Setup Task Guidance"
description: "Discovers eligible Reporting Hierarchy Generation tree codes or tree versions through read-only Fusion lookups and, after explicit approval, delegates validated ESS submission and tracking."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Resources"
functional_area_code: "ORA_CRM_RESOURCES"
task_code: "HZ_RUN_REPORTING_HIERARCHY_GENERATION"
task_name: "Run Reporting Hierarchy Generation"
parent_skill_id: "cx.customer-data-management.resources"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.1.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "tree_structure_code"
  - "tree_code"
  - "tree_version_id"
  - "submit"
  - "fusion_environment_context"
  - "ess_execution_options"
  - "execution_approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "tree_code_candidates"
  - "tree_version_candidates"
  - "candidate_selection_status"
  - "ess_request_id"
  - "ess_status"
  - "diagnostics"
  - "audit_summary"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/run-reporting-hierarchy-generation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/run-reporting-hierarchy-generation/current/"
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
  - "Submits the Reporting Hierarchy Generation ESS process after explicit approval."
  - "Tracks the submitted ESS request until completion or the configured wait timeout."
required_privileges:
  - "Run Trading Community Resource Reporting Hierarchy Generation"
---

# Run Reporting Hierarchy Generation Setup Task Guidance

## Purpose

Validate the Reporting Hierarchy Generation parameters and, after explicit approval, delegate submission and tracking to the Oracle Fusion ESS process for `Run Reporting Hierarchy Generation` under `Resources`.

## Setup Task Skill Contract

- task_code: `HZ_RUN_REPORTING_HIERARCHY_GENERATION`
- task_name: `Run Reporting Hierarchy Generation`
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

Use this skill to validate and run `Run Reporting Hierarchy Generation` under `Resources`. This task is not an FSM or CSV export/import task.

## Setup Task Metadata

- Task name: `Run Reporting Hierarchy Generation`
- Task code: `HZ_RUN_REPORTING_HIERARCHY_GENERATION`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `tree_structure_code` (Tree Structure Code): Required for every request; accept `RESOURCE_ORG_TREE_STRUCTURE` or `PARTNER_ORG_TREE_STRUCTURE`.
- `tree_code` (Tree Code): Optional. When supplied without a Tree Version ID and without `submit=true`, returns read-only Tree Version candidates.
- `tree_version_id` (Tree Version ID): Required only with `submit=true`; do not accept it for discovery.
- `submit`: Explicit Boolean execution intent. Set to `true` only to request ESS submission; omit or set to `false` for read-only discovery. With only Tree Structure Code, the skill returns Tree Code candidates.
- `fusion_environment_context`: The configured Fusion connection used by the delegated REST and ESS clients; this task does not require a caller-supplied environment selection.
- `ess_execution_options`: Polling and timeout options supported by `core.fusion-api.ess-job-submitter`.
- `execution_approval`: Explicit approval identifying the job and exact parameters supplied in the current execution request.

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `tree_code_candidates`
- `tree_version_candidates`
- `candidate_selection_status`
- `ess_request_id`
- `ess_status`
- `diagnostics`
- `audit_summary`

## Preflight and Submission Gate

Before any Fusion call, confirm the configured target environment and submitting
identity. Before ESS submission, complete and record the following preflight
checks in the current execution request:

- Require `submit=true`, all three business values, the documented submitting
  privilege, and an explicit approval that identifies the target job and exact
  Tree Structure Code, Tree Code, and Tree Version ID.
- Use the configured read-only Fusion lookups to verify the exact Tree Structure
  Code/Tree Code pair and exact Tree Version ID; record its Fusion status and
  effective-date classification.
- Verify the fixed ESS job definition, application, and ordered argument binding
  below. Do not derive values from discovery results or previous conversation
  history.
- If an existing request is supplied, or a known compatible request is active or
  blocked, track that request instead of submitting another one.

Fail closed on a missing, ambiguous, or failed preflight check. Follow
`ora-resource/ora_error_handling.md` for the failure classification, disclosure,
and recovery action. Do not invoke ESS until the entire preflight has passed.

## Diagnostics, Redaction, and Recovery

Persist only sanitized validation outcomes, tree identifiers, ESS request ID,
last status, timestamps, failure class, and recommended next action in the
declared project outputs. Never print, persist, or include in diagnostics OAuth
tokens, credentials, client secrets, authorization headers, token-cache
contents, or unredacted raw request/response payloads.

On an authorization failure, process failure, or timeout, preserve the sanitized
submitter diagnostics and request ID when available. Do not automatically retry
or resubmit; require a newly validated request and explicit execution approval.

## ESS Submission Routing

## REST Request Header Requirement

For every delegated Fusion REST call in this skill, pass the following header
through `core.fusion-api.rest-api-client`:

```text
REST-Framework-Version: 9
```

This applies to Tree Code discovery, Tree Version discovery, the pre-submit
`fndTrees` exact-pair lookup, and the pre-submit `fndTreeVersions` exact-version
lookup. Do not replace the core client's OAuth authorization or `Accept` header.

Use the supplied business fields to select the route. With only Tree Structure
Code and `submit` omitted or `false`, use only `core.fusion-api.rest-api-client`
to return Tree Code candidates. With Tree Structure Code and Tree Code, no Tree
Version ID, and `submit` omitted or `false`, return Tree Version candidates.
These discovery routes never invoke `core.fusion-api.ess-job-submitter`. Invoke
`core.fusion-api.ess-job-submitter` only when `submit=true`, all three business
values are supplied, validation passes, and execution approval is explicit. Do
not implement Scheduler REST calls in this skill.

When this skill receives a verified ResourceUser CX Import
handoff from `Manage Resources`, treat the handoff's Tree Structure Code, Tree
Code, and Tree Version ID as the current-request values. The handoff must
identify the successful ResourceUser completion and its exact tree triple. Do
not request those values again, mix them with user-provided values, or accept
an unverified completion. The separate ESS approval remains mandatory.

Use the approved ESS contract:

- Job definition ID: `JobDefinition://oracle/apps/ess/cdm/foundation/resources/resourceRepMgrSync/ResourceHierarchyUpdateJob`
- Application: `CrmEss`
- Request parameters, in this order:
  - `submit.argument1=STRING=<tree_structure_code>` — Tree Structure Code
  - `submit.argument2=STRING=<tree_code>` — Tree Code
  - `submit.argument3=STRING=<tree_version_id>` — Tree Version ID

Bind the exact `tree_structure_code`, `tree_code`, and `tree_version_id` values
supplied in the current execution request to the three arguments. Do not default,
derive, reuse, or substitute a business value from prior conversation history.
Do not use the scheduled-process display labels (`Tree Structure Code`, `Tree
Code`, or `Tree Version ID`) as ESS REST parameter names. Do not send UI-only
`display.*` fields or system-generated request parameters unless a future
approved contract requires them.

For Tree Code discovery, use `core.fusion-api.rest-api-client` to query
`GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>'`
with fields `TreeCode,TreeVersionId,Status,EffectiveStartDate,EffectiveEndDate`.
Retrieve every page, discard blank Tree Codes, and return deduplicated Tree Codes
only. Do not return a Tree Version ID, infer a Tree Code, or bind a value for a
later submission.

For Tree Version discovery, use `core.fusion-api.rest-api-client` to query
`GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>'`
with fields `TreeVersionId,Status,EffectiveStartDate,EffectiveEndDate`. Retrieve
every page and return the candidate IDs with Fusion status, effective dates, and
the ACTIVE/FUTURE/INACTIVE classification. A sole current-effective candidate
may be labelled recommended, but it must not be selected, retained, or submitted
without a later request containing all three values and `submit=true`.

For `submit=true`, before ESS metadata binding, use `core.fusion-api.rest-api-client` to validate the
current Tree Structure Code and Tree Code through the configured Fusion
connection with
`GET /fscmRestApi/resources/11.13.18.05/fndTrees?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>'`.
Accept the Tree Code only when the response contains an exact match for both
values. If it does not, stop before ESS submission and report the lookup result
to the user; do not infer, default, or substitute a Tree Code.

After the Tree Code check, use `core.fusion-api.rest-api-client` to query
`GET /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>'`.
Within that response, require exactly one `TreeVersionId` equal to the supplied
`tree_version_id`. If no exact version is returned, stop and report the lookup
result. Always show the matched version's `Status`, `EffectiveStartDate`, and
`EffectiveEndDate`. Classify it from its dates: `FUTURE` when
`EffectiveStartDate` is after the current validation date; `INACTIVE` only when
`EffectiveStartDate` is before that date and `EffectiveEndDate` is before
it; otherwise `ACTIVE` (including a blank or current/future end date). Report
the Fusion `Status` separately. Require explicit confirmation only for an
`INACTIVE` version. In every classification, the final execution approval must
confirm all three submitted parameter values.

Before submission, require all three values and `submit=true` in the current
execution request, validate that the structure code is one of the two documented values,
require a non-empty tree code and tree version ID, and require the internal
hierarchy tree code to be `GLOBAL_SALES_MARKETING`. For a partner hierarchy,
require the caller to explicitly confirm the supplied partner tree code and
version in the approval. Discovery results are not current-request business
values and must not be reused for submission.

The submitting identity must hold the documented privilege. If an existing ESS request ID is supplied, route only to tracking and do not submit again. If a known Reporting Hierarchy Generation request is active or blocked, do not submit a parallel request. On authorization failure, process failure, or timeout, preserve the submitter diagnostics and request ID when available; do not automatically resubmit.
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.resources` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
