---
skill_id: "hcm.goal-management.review-period.review-periods"
name: "Review Periods Setup Task Guidance"
description: "Provides task-specific setup guidance for Review Periods under the Review Period functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Review Period"
functional_area_code: "ORA_REVIEW_PERIOD"
task_code: "ORA_HRG_MANAGE_REVIEW_PERIODS"
task_name: "Review Periods"
parent_skill_id: "hcm.goal-management.review-period"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "goal_management_execution_control"
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
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/review-period/review-periods/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/review-period/review-periods/current/"
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
side_effects: []
required_privileges: []
---

# Review Periods Setup Task Guidance

## Review Period prerequisite guidance

This task establishes the time boundary for regular Goal Plans. Goal Management
planning must validate the Review Period before dependent plan-definition work.
The shared implementation-planning services own executable task sequencing.

## Purpose

For create-status intent and post-create activation decisions, follow
[the lifecycle follow-up contract](../../goal-management-common/lifecycle-follow-up.md).

Before any mutation preview, require an `allowed` Goal Management execution
control whose exact task identity, Review Period functional area, sequence,
skill path, and approved plan fingerprint match this task. The resolved queue
may contain any number of tasks. A request to create or activate a Review
Period cannot bypass the earliest unfinished applicable task. Missing, stale,
stopped, or mismatched control returns `BLOCKED` before target lookup.

Support the consultant lifecycle `get`, `list`, `search`, `create`, `update`, `inactivate`,
metadata-gated `delete`, `csv_export`, and `csv_import`. Use
`reviewPeriodsLOV` only for safe ID resolution. Supplied UI/runtime evidence
establishes create, fetch, and update behavior and the fields Review Period ID,
name, description, start/end dates, status, `InUseFlag`, and concurrency state.
It does not establish DELETE. Prefer the validated relative standard root
`/hcmRestApi/resources/latest/reviewPeriods`, confirm the operation through
`/describe`, and use returned same-host item links only after validation.
Resolve a volatile current runtime root only when the standard collection is
not exposed; reject placeholder roots such as `rv:null`. Keep any fallback in
memory only and execute through the core REST client. Do not launch a browser
to fetch Review Periods.

## Best-practice context

Consult sections 2-7 and 14 of the [HCM Goal Management best-practice
reference](../../goal-management-common/best-practice-rules/hcm-goal-management/README.md)
for tenant route selection, lifecycle, naming, date design, integration
checks, and the create/update checklist. Treat it as advisory only: this task
contract, current Oracle documentation, and target-tenant behavior control the
operation, validation, approval, and deletion rules.

## Deterministic operation and safety

For explicit REST batch intent, read [REST batch workflow](../../goal-management-common/rest-batch.md).
Reuse this skill's current create/update contracts and validation for every period.
Resolve parent CRUD batch eligibility through the maintained Goal Management
capability resolver plus current Review Period describe methods. Do not require a
`batchEnabled` field on the collection or reuse the search action's flag. Batch
preparation does not authorize execution or bypass usage checks.

Resolve exactly one Review Period for get/update/inactivate/delete. Create
requires no exact-name duplicate. Require a nonblank name and valid inclusive
date range; dates are validated but do not distinguish duplicate Review Periods.
Before date change, inactivation, or deletion, re-read `InUseFlag` and usage by Goal Plans and
other exposed consumers. Prefer a new period and inactivation when it is in
use; deletion additionally requires that current authoritative metadata
explicitly advertises DELETE, proven zero usage, and separate approval.

Safe item, list, and search reads require no write approval, including the
read-only advanced-search action whose transport method is POST. Every mutation and CSV import requires a
final preview, exact approval, one submission, and fresh verification. A stale
target or changed fingerprint invalidates approval. Do not retry an ambiguous
write; return `UNKNOWN_AFTER_SUBMISSION` and reconcile by reading.

## Outcomes

Return exactly one of `READ`, `CREATED`, `UPDATED`, `INACTIVATED`, `DELETED`,
`CSV_READY`, `NO_CHANGE`, `MISSING`, `BLOCKED`, `FAILED`, or
`UNKNOWN_AFTER_SUBMISSION`, together with sanitized diagnostics and a resume
context.

## Business duplicate comparison

Before any HDL or standard create, follow [the shared duplicate identity contract](../../goal-management-common/duplicate-identity.md). Use its executable helper for candidate comparison and incoming-row checks. After complete pagination, an exact Review Period name match is a duplicate regardless of dates.
