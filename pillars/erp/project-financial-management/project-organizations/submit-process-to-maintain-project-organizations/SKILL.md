---
skill_id: "erp.project-financial-management.project-organizations.submit-process-to-maintain-project-organizations"
name: "Submit Process to Maintain Project Organizations Setup Task Guidance"
description: "Prepares, submits once after exact approval, and monitors the fixed parameterless Maintain Project Organizations ESS job."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
task_code: "PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY"
task_name: "Submit Process to Maintain Project Organizations"
parent_skill_id: "erp.project-financial-management.project-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.3.1"
inputs:
  - "project_id"
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "target_environment"
  - "explicit_submission_approval"
  - "request_id_for_resume"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "execution_receipt_record"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.ess-job-submitter"
  - "schemas/ess-delegation-contract.schema.json"
uses_core:
  - "core.fusion-api.ess-job-submitter"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
persists_project_state: true
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/submit-process-to-maintain-project-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/submit-process-to-maintain-project-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/submit-process-to-maintain-project-organizations/current/"
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
  - "May submit one fixed parameterless OrgDenormJob after explicit approval and monitor only its returned request ID."
  - "Writes task plans, validation/preview evidence, execution receipts and redacted diagnostics to the selected project workspace through core project services."
required_privileges:
  - "Project Application Administrator or equivalent privilege to schedule and monitor Maintain Project Organizations"
---

# Submit Process to Maintain Project Organizations

## Purpose

Prepare and run the Oracle Fusion Maintain Project Organizations scheduled process whenever invoked by the FSCR framework or directly on demand. The framework owns sequencing and the decision to invoke this task. This skill performs only ESS execution; it does not inspect prior setup, PABF, organizations or hierarchy state.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY`
- task_name: `Submit Process to Maintain Project Organizations`
- parent_skill_id: `erp.project-financial-management.project-organizations`
- functional_area_code: `ORA_PJF_PROJ_ORG`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `ESS`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Fixed Parameterless Payload

Every new invocation prepares only:

```json
{
  "jobDefinitionId": "JobDefinition://oracle/apps/ess/projects/foundation/setup/system/OrgDenormJob",
  "application": "FscmEss",
  "product": "PJF"
}
```

Omit `requestParameters`; reject user-supplied request parameters, including empty or null values and `--parameter`. Reject conflicting job/application/product values and any additional payload fields, schedules or retry controls. There is no tree metadata or prerequisite lookup. No organization-change evidence, hierarchy flags, audit/activation, flatten processing or downstream organization eligibility check belongs to this task.

## ESS Execution Workflow

1. Select the project and configured target environment with ESS scheduling/monitoring privileges. Perform [Task Plan Validation and Execution](#task-plan-validation-and-execution) using the shipped registry and its six owning resource files; record a `planned` / `ready` plan without an override. Use the configured `restBaseUrl`; never hardcode a pod.
2. Prepare the fixed payload locally. `scripts/run_maintain_project_organizations.py --dry-run` displays it without authentication or external calls.
3. Show the exact configured environment, `restBaseUrl`, complete payload and its canonical SHA-256 digest. Obtain explicit approval immediately before submission. Record that approval through the active workflow in an immutable task-local approval JSON; never fabricate or automatically grant approval:
   ```json
   {
     "approved": true,
     "operation": "submit",
     "environment": "<configured environment>",
     "restBaseUrl": "<configured target restBaseUrl>",
     "payload_sha256": "<SHA-256 of UTF-8 JSON with sorted keys and compact separators>"
   }
   ```
   The wrapper's `payload_digest` computes this digest. Approval is valid only for this exact target and complete fixed payload; a changed target or payload requires fresh approval.
4. Record the [approved Core handoff](#approved-core-handoff) from that exact approval, then invoke the task wrapper with `--properties <target-properties>`, `--approval-file <explicit-approval.json>`, optional `--payload-file <fixed-payload.json>` and a distinct task-local `--output <receipt.json>`. The wrapper validates the supplied payload and approval before authentication, freezes the fixed approved object in memory, and calls core's importable functions once for submission. It never calls core's retrying `main()`.
5. Require a positive returned request ID. Save and read back `<receipt.json>.accepted.json` before the first polling call. Retain target, fixed payload, approval digest and submission evidence.
6. Poll that same ID through `core.fusion-api.ess-job-submitter` to terminal status within the configured wait budget. Completion means terminal success for that request only. HTTP acceptance or a running state is not completion. Preserve acceptance evidence in the final result.
7. Resume with `--request-id <saved-ID>`, selected target properties and a new `--output` path. Resume requires no submission approval and never POSTs. Compare returned request/job identity when present and stop on mismatch. The supplied ID selects resume even when operation is omitted; explicit submit plus an existing ID is refused.
8. Stop on failure, timeout or uncertain submission. Report saved ID, last status, elapsed wait and redacted diagnostics; resume a known ID or reconcile uncertainty through the active workflow. Never automatically replay a POST, refresh credentials to replay submission, or use a new request as a polling fallback.

The optional `--submit-only` stops after durable acceptance; it is not a completion result. Both receipt paths must be unused. A new invocation after a failed/uncertain attempt must not reuse its approval; the workflow must reconcile first and obtain explicit new approval if a genuinely new submission is authorized.

Scheduler submission uses `POST /ess/rest/scheduler/v1/requests`; tracking uses `GET /ess/rest/scheduler/v1/requests/{requestId}` through the core adapter. Authentication, REST transport, status interpretation and polling remain core-owned. Do not generate an import ZIP or substitute an FSM import route for this ESS process. Export/import catalog flags describe separate migration capabilities.

## Task Plan Validation and Execution

Build `setup_task_plan` locally by assisted inspection of
[the shipped registry](ora-resource/ora_rule_registry.json) and its six owning
`ora-resource/ora_*.md` files. This graph-contract check requires no authoring
tool, planner script, authentication, external call or prior-setup lookup.

- Select exactly one `PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY`
  / `Submit Process to Maintain Project Organizations` entry in the nested schema
  `3.0` registry. Require task and reachable-node readiness `ready` without
  blocking reasons; stored flags alone are insufficient.
- Confirm unique node IDs, start node `MPO.VALIDATE_INPUT`, supported actions,
  existing prerequisite/transition targets and terminating paths. Resolve each
  source file inside this task's resource folder and its heading. Match each node
  to exactly one source Task Nodes row by Rule ID; compare type, sequence, action,
  transitions, prerequisites, failure behavior and applicability. Source line
  numbers are navigation hints. Read owning rules and each named resolver's one
  definition, including inputs, authority, matching, outputs and failure behavior.
- Missing, unresolved, ambiguous or inconsistent required contracts block the
  plan. Do not repair the registry, invent ESS identity or add organization/tree
  prerequisites. After checks pass, record `status: planned`,
  `validation.status: ready`, exact task identity, start node, checked sources and
  validated nodes through the declared project services and task workspace paths.
  Recheck each new run or changed rule source; no readiness override is allowed.

On failure, stop before further tracking or submission. Persist a redacted
diagnostic with stage, failure class, task/target, blockers and one safe next
action. Use `input_validation` or `catalog_or_metadata_mismatch` for input or
rule-contract gaps; preserve actual wrapper/Core failure classes.

Begin at `MPO.VALIDATE_INPUT`, satisfy prerequisites, evaluate applicability,
apply only reached owning rules and follow each observed declared outcome to a
terminal. Record sanitized evidence and path/outcomes. Never execute all nodes
by sequence or invent an outcome. Plan readiness is not submission approval;
`MPO.RETURN_READY_TO_SUBMIT` requires the exact explicit approval in step 3 and
does not mean the job was submitted or completed. `MPO.RETURN_READY_TO_RESUME`
selects read-only tracking of the saved ID, never a replacement submission.
Only the existing wrapper/Core route performs steps 4-8; do not duplicate it
when evaluating the graph or polling through its resolver.

Retain the normalized request fingerprint, current node, path/outcomes, sanitized
resolver/default evidence, missing requirements and safe resume stage in task-owned
planning evidence. Return task identity, actual stage/outcome, blockers and one
safe next action. Refresh changed evidence when resuming preparation; changed
target/payload invalidates approval. Once submission is attempted, the wrapper's
consumed-approval and saved-ID recovery rules govern; a new plan never authorizes
replay. Keep receipts, partial failures and resume context through the declared
project services without copying Core transport/authentication logic.

## Approved Core Handoff

For a new submission only, record and validate an `approved_submission` envelope
against [ESS delegation contract 1.0](../../../../../schemas/ess-delegation-contract.schema.json)
after step 3's actual approval and before step 4. Use `contract_version: "1.0"`,
`stage: approved_submission`, this exact task code/name, the selected
`fusion_environment_context`, positive integer `execution_options.wait_seconds`
and `poll_interval_seconds`, and `job_contract` with the fixed job-definition ID
and application. `request_payload` must equal the complete three-field fixed
payload. `approval.explicit_submission_approval` is true only from that recorded
approval; `approved_payload_sha256` must equal its canonical payload digest.
Check schema fields, target, job, payload and digest agreement; a mismatch blocks.

Use this validated envelope to derive the wrapper's internal payload, target and
polling arguments, keeping its approval JSON bound to the same values. This
records the existing Core skill-level contract, adds no approval prompt and does
not replace the wrapper's runtime checks. A saved-ID resume uses the existing
read-only tracking route; never manufacture a new submission envelope or approval
for it. Persist no credentials or tokens in the handoff.

## Durable Artifacts and Review

Resolve `project_id` from the selected implementation project. Persist the displayed payload, explicit approval, receipts and redacted diagnostics under `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/submit-process-to-maintain-project-organizations/current/`. Never persist credentials or tokens.

Use declared artifact versioning, artifact registry and project state services; record the run under `project/{project_id}/state/runs/` and token usage under the manifest policy. Save acceptance before polling and retain partial failures and safe next actions.

Required reviewers: ERP Pillar Development Lead or SME, FSCR A-Team/core reviewer, and QA for execution changes.
