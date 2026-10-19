---
skill_id: "cx.customer-data-management.trading-community-foundation.run-classification-hierarchy-generation"
name: "Run Classification Hierarchy Generation Setup Task Guidance"
description: "Previews, submits once, and tracks the Oracle Fusion Classification Hierarchy Generation ESS scheduled process for trading community classification hierarchies."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_RUN_CLASSIFICATION_HIERARCHY_GENERATION"
task_name: "Run Classification Hierarchy Generation"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.3.1"
inputs:
  - "execution_intent"
  - "fusion_environment_context"
  - "classification_category"
  - "flattening_method"
  - "requestId"
  - "execution_options"
  - "project_id"
outputs:
  - "execution_preview"
  - "ess_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.fusion-api.ess-job-submitter"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-classification-hierarchy-generation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-classification-hierarchy-generation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-classification-hierarchy-generation/current/"
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
  - "After an exact immutable preview and standalone approval, submits the Classification Hierarchy Generation ESS scheduled process once to the selected Fusion environment."
  - "The scheduled process flattens the selected trading community classification category hierarchy, or all category hierarchies when no category is supplied."
  - "May refresh the local gitignored OAuth token cache through core.fusion-api.ess-job-submitter."
required_privileges:
  - "Administrator access to the Manage Classification Categories setup task."
  - "Run Trading Community Classification Hierarchy Generation (HZ_RUN_TRADING_COMMUNITY_CLASSIFICATION_REPORTING_HIERARCHY_GENERATION_PRIV)."
---

# Run Classification Hierarchy Generation

## Purpose

Preview, submit, and track Oracle Fusion's `Classification Hierarchy Generation` ESS scheduled process. The process flattens trading community classification hierarchies maintained through `Manage Classification Categories`.

## When to Use

Use this skill when the user asks to run the scheduled process, obtain a submission preview, or check an existing ESS request ID. Oracle states that hierarchy changes are normally flattened immediately; run this process manually on demand when flattened hierarchy data has an identified issue or after a classification-category change requires it.

This skill does not create or modify classification categories or classification codes. It is not a Data Loader import and must not invoke `core.data-loader`.

## Setup Task Skill Contract

- task_code: `HZ_RUN_CLASSIFICATION_HIERARCHY_GENERATION`
- task_name: `Run Classification Hierarchy Generation`
- parent_skill_id: `cx.customer-data-management.trading-community-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Trading Community Foundation`
- functional_area_code: `ORA_HZ_CDM_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `ESS`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Inputs

- `execution_intent`: a direct request to run the scheduled process, a preview-only request, or a status request for an existing `requestId`.
- `fusion_environment_context`: exactly one target Fusion environment for a new submission.
- `classification_category`: optional Classification Category Tree Code. Blank means all categories.
- `flattening_method`: optional `INCREMENTAL_FLATTENING` or `FORCE_FLATTENING`; default `INCREMENTAL_FLATTENING`.
- `requestId`: an existing positive ESS request identifier for status tracking; mutually exclusive with new-submission inputs.
- `execution_options`: optional bounded tracking values used only for an explicit status request.
- `project_id`: optional durable workspace. Do not create a project solely because this input is absent.

## Oracle Parameter Contract

| Parameter | Requirement | Accepted value | Default and effect |
|---|---|---|---|
| Classification Category | Optional | One supplied Classification Category Tree Code | Blank processes all categories |
| Flattening Method | Optional | `INCREMENTAL_FLATTENING` or `FORCE_FLATTENING` | `INCREMENTAL_FLATTENING` |

Accept a supplied Classification Category Tree Code as the direct `ATTRIBUTE1` value. Do not perform an environment LOV lookup, rewrite the value, or require the caller to prove that it is active. The caller is responsible for supplying the intended Tree Code; Fusion remains the authority for rejecting an invalid value.

Use force flattening only when the user explicitly selects it. Never infer force flattening from a general request to run or fix the hierarchy.

## Fixed ESS Contract

Use this reviewed Scheduler contract for every new submission:

| Field | Fixed value |
|---|---|
| `jobDefinitionId` | `JobDefinition://oracle/apps/ess/cdm/foundation/parties/HzClassHierarchyFlattenedDataGenJob` |
| `application` | `CrmEss` |
| `product` | `HZ` |
| Classification Category parameter | `ATTRIBUTE1` as `STRING`; send the supplied Tree Code or an empty value for all categories |
| Flattening Method parameter | `ATTRIBUTE2` as `STRING`; send `INCREMENTAL_FLATTENING` or `FORCE_FLATTENING` |

The process has exactly two ordered business arguments. Bind `ATTRIBUTE1` before `ATTRIBUTE2`; do not use `submit.argument1`, `submit.argument2`, the setup-task code, or the display name as substitutes. The public Oracle scheduled-process page documents the business process but not this REST contract; the fixed values come from reviewed HZ ESS job metadata and a successful Scheduler REST submission.

## Preflight Checks

Before any new submission, confirm exactly one configured target environment,
the fixed job definition and `ATTRIBUTE1`/`ATTRIBUTE2` contract, the required
privilege, the supplied category Tree Code or explicit all-categories choice,
and the normalized flattening method. Confirm that no active incompatible
instance is known, the project artifact destination is writable, and the exact
immutable preview has received standalone approval. Stop before side effects
when any preflight item is missing, ambiguous, or changed after approval.

## Execution Workflow

1. Classify the request as advisory, preview-only, new submission, or tracking an existing `requestId`. A status request never creates a new submission.
2. For a new submission, resolve exactly one target Fusion environment. When exactly one configured environment is available, use it without asking the caller for technical ESS metadata.
3. Normalize an omitted Flattening Method to `INCREMENTAL_FLATTENING`. Preserve a blank Classification Category as the explicit all-categories selection.
4. Pass a supplied Classification Category Tree Code through unchanged as `ATTRIBUTE1`; do not perform a target-environment validation lookup. Verify the required privilege. Oracle documents the process as incompatible with itself; do not submit when another active instance is known. Recommend off-peak execution.
5. Present an immutable preview containing the environment, process name, fixed job definition ID, application, the fixed technical parameter mapping, category Tree Code or `All categories`, flattening method, expected impact, and the fact that submission will occur once without automatic retry.
6. Stop and require a later standalone `approve` for that exact preview. A change to the environment, ESS metadata, parameter mapping, category, method, or preview fingerprint invalidates approval.
7. After approval, invoke `core.fusion-api.ess-job-submitter` with the exact approved contract, `--submit-only`, and `--retries 0`. Do not call Scheduler REST directly and do not invoke Data Loader.
8. Submit exactly once, capture the returned `requestId`, report it, and stop without polling. Monitor only after a separate explicit status request using that same request ID.
9. For status tracking, invoke the core skill with `--request-id <requestId>` and bounded polling. A timeout is nonterminal and must resume the same request; it must never trigger a replacement submission.

## Approval and Retry Boundaries

- An initial request to run the job authorizes validation and preview only.
- Only standalone `approve` authorizes the exact previewed ESS POST.
- Never retry an ESS POST automatically, including after transport failure, timeout, missing response, or missing request ID.
- A missing request ID after submission is an uncertain mutation. Record the uncertainty and reconcile server state before considering any new request.
- Allow the core OAuth workflow to refresh a rejected cached token once, but do not interpret token refresh as approval to repeat an uncertain ESS POST.
- Never claim that hierarchy data was corrected merely because submission was accepted. Report completion only from terminal ESS status, and report data correction only from separate business validation.

## Outputs

- `execution_preview`: the exact target, technical ESS contract, normalized parameters, impact, and approval fingerprint.
- `ess_execution_result`: request ID after submission, or terminal/last-known status for an explicit tracking request.
- `diagnostics`: failure class, safe next action, and available request ID, status, or ECID without secrets.
- `skill_run_record`
- `token_usage_record`

## Failure Handling

Classify failures as `input_validation`, `catalog_mismatch`, `auth_or_authorization`, `transport_or_environment`, `Fusion_API`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`. Preserve the request ID whenever one exists. On terminal failure, retrieve available ESS status and diagnostic information through the core skill; never resubmit automatically.

Never print or persist access tokens, refresh tokens, client secrets, authorization headers, token-cache contents, or sensitive customer data.

## Golden Scenarios

| Scenario | Expected result |
|---|---|
| User asks to run with no parameters | Resolve all categories plus incremental flattening, apply the fixed ESS contract, show the exact preview, and wait for standalone approval |
| User supplies a category Tree Code | Pass it unchanged as `ATTRIBUTE1` and preview only that category |
| User selects force flattening | Preserve `FORCE_FLATTENING`, highlight its broader impact, and require exact approval |
| User supplies only business parameters | Apply the fixed ESS contract; do not ask for job metadata or parameter names |
| User supplies `TEST` | Use `ATTRIBUTE1=TEST` directly; do not perform an LOV lookup or request extra validation |
| Another active instance is known | Stop because the process is incompatible with itself |
| Approved submission succeeds | Return the request ID and stop without polling |
| User supplies an existing request ID | Track that request without a new POST |
| Polling times out | Preserve and resume the same request ID; do not submit another job |

## Source Boundaries

- Oracle scheduled-process reference: `https://docs.oracle.com/en/cloud/saas/sales/fauss/classification-hierarchy-generation.html`
- Reviewed HZ ESS metadata: `HzClassHierarchyFlattenedDataGenJob.xml` and `ClassificationHierarchyParamVO.xml` in the HZ parties ESS source tree.
- Scheduler execution owner: `core.fusion-api.ess-job-submitter`
- Effective task catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

The Oracle public source confirms the business process, privilege, compatibility, and LOV parameter semantics. The reviewed HZ ESS metadata establishes the fixed Scheduler REST job definition, application, and `ATTRIBUTE1`/`ATTRIBUTE2` parameter mapping.

## Parent Skill

Use the parent functional-area skill `cx.customer-data-management.trading-community-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
