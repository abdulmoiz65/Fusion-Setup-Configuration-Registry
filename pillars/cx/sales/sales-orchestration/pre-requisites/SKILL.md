---
skill_id: "cx.sales.sales-orchestration.pre-requisites"
name: "Sales Orchestration Pre-requisite Readiness Guidance"
description: "Answers source-backed questions about Sales Orchestration prerequisite readiness, including the Oracle Sales baseline, signals, Dispatcher routing, Knowledge Management content readiness, Microsoft Outlook and email integration, supported web-conference capture, Exchange email and calendar integration, and general end-user access. Use for functional prerequisite questions under CUSTOM_PRE_REQUISITES; route Sales Motion, Sales Plays and Content, and Data Capture Rule setup or security questions to their owning nested skills without duplicating their guidance or executing configuration changes."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Orchestration"
functional_area_code: "CUSTOM_SALES_ORCHESTRATION"
task_code: "CUSTOM_PRE_REQUISITES"
task_name: "Pre-requisites"
parent_skill_id: "cx.sales.sales-orchestration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.6.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "prerequisite_question"
  - "requested_answer_mode"
outputs:
  - "question_classification"
  - "prerequisite_answer"
  - "task_routing"
  - "source_gap"
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-orchestration/pre-requisites/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-orchestration/pre-requisites/current/"
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

# Sales Orchestration Pre-requisite Readiness Guidance

## Purpose

Answer source-backed functional prerequisite-readiness questions for
`CUSTOM_PRE_REQUISITES`. Route task-specific questions to the owning nested
skill and do not duplicate its product, setup, security, or API guidance.

## Setup Task Skill Contract

- task_code: `CUSTOM_PRE_REQUISITES`
- task_name: `Pre-requisites`
- parent_skill_id: `cx.sales.sales-orchestration`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Sales Orchestration`
- functional_area_code: `CUSTOM_SALES_ORCHESTRATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Question Scope and Required Source

For every question:

1. Read `../references/sales-orchestration-question-routing.md`.
2. Classify the question before loading any execution or authentication source.
3. For Oracle Sales baseline, signals, Dispatcher, Knowledge Management,
   Microsoft Outlook or email integration, web-conference, Exchange integration,
   or general seller-access readiness, read
   `references/sales-orchestration-prerequisites.md` and answer from that source.
   Use its local endpoint templates and UI navigation as the complete source for
   validation guidance; do not fetch the provenance Confluence page to answer a
   future question.
4. For task-specific setup, access, roles, privileges, permission groups, data
   policies, fields, APIs, or troubleshooting, return `ROUTED` and select the
   nested skill specified in the prerequisite reference.
5. Return `SOURCE_GAP` for prerequisite behavior not established by the public
   overview. Do not infer configuration requirements from prior chat history.

An explanation-only question does not authorize browser navigation,
authentication, a Fusion request, an ESS submission, or a project artifact.
This skill has no configuration-change path. A live validation read is allowed
only when the parent implementation workflow selects it and supplies the target
environment and acting-user context; otherwise return the documented checklist.
For a signal-activation question, use the approval-gated target-record PATCH
contract in `references/sales-orchestration-prerequisites.md`. Do not execute
the PATCH from this assisted skill; provide the documented sample only after
stating its target-environment, signal-ID, and explicit-approval requirements.

## Execution Safety

### Preflight

Before a live validation read is selected, confirm the parent implementation
workflow selected this skill, the target environment and acting-user context
are present, the operation is read-only, and the requested signal name or
validation scope is bounded. For the documented signal-remediation sample,
confirm the signal-definition ID was resolved by an exact-name GET in the same
environment and that an authorized administrator has explicit approval
immediately before any PATCH. Do not authenticate, navigate a browser, submit
an ESS job, or make an external request for explanation-only guidance.

### Failure Handling

Classify a missing target, acting-user context, exact signal name, or supported
source as `input_validation` or `SOURCE_GAP` and stop with the documented
checklist. Treat a missing signal, `ActiveFlag` other than `true`, inactive
email or Outlook integration record, or missing Dispatcher rule as a failed
prerequisite—not as authorization to change it. Do not retry a failed PATCH;
route remediation to the authorized environment administrator, require fresh
approval, and rerun the bounded validation after remediation. Preserve only
sanitized status, failure class, recommended action, environment identifier,
and artifact reference when a project validation result is required.

### Redaction

Never request, display, log, or persist Microsoft application keys, client
secrets, passwords, OAuth tokens, authorization headers, token caches, private
keys, or sensitive environment and customer data. Validate only the presence
of Microsoft 365 or Outlook credential fields; do not reproduce their values
in an answer, diagnostic, or project artifact.

## Setup Task Metadata

- Task name: `Pre-requisites`
- Task code: `CUSTOM_PRE_REQUISITES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

Do not treat an unsupported export or import request as permission to use a
browser, direct REST call, or another loader.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `prerequisite_question`
- `requested_answer_mode`: EXPLAIN, CLARIFY, ROUTE, GAP, or REFUSE

## Outputs

- `question_classification`
- `prerequisite_answer`
- `task_routing`
- `source_gap`
- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.sales-orchestration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Help Sources

- Functional prerequisite readiness and task-routing boundary:
  `references/sales-orchestration-prerequisites.md`
- Cross-task question classification and response contract:
  `../references/sales-orchestration-question-routing.md`
