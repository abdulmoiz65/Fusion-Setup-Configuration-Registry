---
skill_id: "hcm.performance-management.requested-feedback-template.feedback-templates"
name: "Feedback Templates Setup Task Guidance"
description: "Provides task-specific setup guidance for Feedback Templates under the Requested Feedback Template functional area."
layer: "pillar"
pillar: "HCM"
offering: "Performance Management"
functional_area: "Requested Feedback Template"
functional_area_code: "ORA_REQUESTED_FEEDBACK_TEMPLATE"
task_code: "ORA_HRA_FEEDBACK_TEMPLATES"
task_name: "Feedback Templates"
parent_skill_id: "hcm.performance-management.requested-feedback-template"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM performance management pillar team"
version: "0.1.8"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "questionnaire_compatibility_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.validation.reference-data-validator"
  - "hcm.hcm-tool.questionnaire.questionnaires"
  - "core.fusion-api.apps-common.lookups"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/requested-feedback-template/feedback-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/requested-feedback-template/feedback-templates/current/"
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
  - "Creates or updates Feedback Templates through explicitly approved REST POST or PATCH."
required_privileges:
  - "Authenticated target-tenant Feedback Templates read before preview; Fusion authorizes the selected POST or PATCH at dispatch."
---

# Feedback Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, REST routing, and validation guidance for `Feedback Templates` under `Requested Feedback Template`.

## Setup Task Skill Contract

- task_code: `ORA_HRA_FEEDBACK_TEMPLATES`
- task_name: `Feedback Templates`
- parent_skill_id: `hcm.performance-management.requested-feedback-template`
- pillar: `HCM`
- offering: `Performance Management`
- functional_area: `Requested Feedback Template`
- functional_area_code: `ORA_REQUESTED_FEEDBACK_TEMPLATE`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, reading, creating, updating, or validating setup data for `Feedback Templates` under `Requested Feedback Template`.

### Intake guidance and ordinary updates

Use offline `plan_requirements` with `requested_channel` and `business_values`
for conversational creation intake. Surface `follow_up_questions`,
`missing_business_fields` and `supported_alternatives`; retain confirmed inputs
across user replies and rerun after explicit answers. Unsupported execution
requests do not authorize a REST conversion. CSV/BRD documents can supply
requirements for a separately requested REST plan.

For an ordinary edit, obtain the existing template name and requested changes,
resolve one current template, complete existing preflight checks, and use
`update_template` / `before_template_update` with `patch_feedback_template`.
This preserves questionnaire/type and needs no questionnaire creation or new
content verification. Questionnaire/type fields, even unchanged values, require
`associate` and its compatibility gate. In-use templates accept only Name and
Comments through this action. Field mapping, manager validation, goal activation
review, approval, concurrency, readback and no-retry guards remain mandatory.
See `ora-resource/ora_rest_execution.md` for the input contract.

## Setup Task Metadata

- Task name: `Feedback Templates`
- Task code: `ORA_HRA_FEEDBACK_TEMPLATES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- Execution routing: `REST-only`
- Business Object: ``

## Routing: REST-only Feedback Templates

General Feedback Templates and Performance Goal Feedback Templates support only
the GET, POST, and PATCH operations declared in
[`ora-resource/ora_rest_execution.json`](ora-resource/ora_rest_execution.json).
Read [`ora-resource/ora_rest_execution.md`](ora-resource/ora_rest_execution.md)
and all applicable task-local validation, dependency, lookup, design, and error
resources before preview or execution. Invoke requests through
`core.fusion-api.rest-api-client` only.

FSM/CSV import/export, HDL/HSDL, and Data Loader execution are unsupported for
these two template types. Return `UNSUPPORTED_EXECUTION_CHANNEL` when requested;
do not redirect an explicit unsupported-channel request into a REST write.
CSV/workbooks may supply requirements for a separately requested REST plan.
This restriction does not change questionnaire, profile-option, or runtime
FeedbackRequest provider routes.

### Catalog discrepancy

The external effective catalog currently advertises export/import and CSV
support for `ORA_HRA_FEEDBACK_TEMPLATES`. The local `N` flags reflect the
confirmed REST-only object scope. Record `catalog_mismatch` in project readiness;
never use those external `Y` flags to enable an unsupported route. If a downstream
workflow insists on FSM/Data Loader, stop that handoff instead of bypassing it.
The external catalog correction is outside this folder-only change.

### REST preflight, validation, and approval

Before any external operation, verify the configured environment identity,
authenticated access to the declared target read, source inputs, and safe project
artifact paths. Review any known authorization denial. The declared route has no
read-only method-specific create/update privilege check: do not require or invent
a separate write-privilege receipt. Fusion enforces authorization on the one
approved POST or PATCH. A 401/403 response is an auth/authz failure, not a
reason to retry the write automatically.

Validate the selected method and relative path, allow only declared payload
fields, require every declared required field, and enforce declared enums and
field types. Resolve identity, questionnaire, manager-type, lifecycle, route
supportability, and activation-impact evidence before preview.

Task-local rules are evaluated by the executing agent and their results are
persisted with the REST preview. This route does not invoke the Data Loader
Task Hook or its archive-specific preview commands. Use the contract's JCS
canonicalization and request-binding checks; absent tooling or unverifiable
evidence blocks preview/write rather than permitting an invented digest.

Declared GET operations run without consultant approval. Present the exact
target, operation, path, payload, digest, and validation results; obtain fresh
explicit approval immediately before one POST or PATCH. Recheck the approved
request binding before dispatch. Never retry a write automatically.

## Scope, prerequisites, and execution boundary

This task must not bypass the parent functional-area profile baseline. Before a
Feedback Templates mutation, require verified SITE values of `Y` for both
`HRA_REQUEST_FEEDBACK_ENABLED` and
`ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED`. The parent skill owns conditional Run
Book mapping through one leading `Manage Administrator Profile Values` task and
`core.fusion-api.apps-common.profile-options`; this task does not write profile
values through the Feedback Templates REST contract. A verified current `Y` is
a no-change outcome. A non-`Y`, absent, or unresolved value blocks the dependent
template mutation until the separately approved profile route verifies `Y`.

Performance Goal Feedback templates must use the seeded **Performance Goal
Feedback** questionnaire (`PERF_GOAL_QSTNR_V1`) for both creation and updates.
Resolve the current target ID by that code. Custom creation, cloning, derivation,
renaming and association are not supported for this template type. Report a
custom request as unsupported during intake and recommend Not Applicable for
an existing replacement task; preserve the existing seeded association. A missing
seed is a prerequisite failure, never permission to manufacture a substitute.
General Feedback retains the custom Questionnaire provider creation route.

This task owns feedback-template planning and validation: template name,
comments or description, status, template type, questionnaire reference,
specific manager types, performance-goal attributes, availability, and in-use
restrictions. It does not own Questionnaire Templates or Questionnaires
lifecycle/CRUD, Request Feedback runtime transactions, or any other
Performance Management setup object.

For existing-template work, resolve exactly one template using a stable ID or
an exact name. Partial-name matches and multiple matches fail closed. For a
new template, require Name, template type, Status, Specific Manager Types,
and Questionnaire; do not invent defaults.

Validate the questionnaire through its owning provider. When source evidence
contains a questionnaire name but not its portable key, first use the approved
read-only `questionnairesLOV` resolver in
`hcm.hcm-tool.questionnaire.questionnaires` through
`core.fusion-api.rest-api-client`. Match the source name exactly, then obtain
its exact questionnaire identity and eligibility using the alternatives in
`ora-resource/ora_reference_lookups.md`. A complete eligible LOV result is
sufficient for selecting an existing reference; a chained read is conditional
on missing or conflicting evidence, not mandatory questionnaire CRUD preflight. General
feedback requires an eligible questionnaire. For either type, additionally run
the mandatory [association compatibility gate](ora-resource/ora_reference_lookups.md#template-type-association-compatibility)
using `scripts/run_feedback_workflow.py` before creation of a
dependent questionnaire and before a template POST or questionnaire/type-changing
PATCH. Performance-goal feedback needs type-specific association evidence:
active/latest status and subscriber alone are insufficient. Do not hard-code a
questionnaire identifier across environments or substitute an unresolved
questionnaire. A same-family questionnaire template does not make a custom
questionnaire eligible for Performance Goal Feedback.
The task wrapper resolves and reevaluates evidence, produces the provider
handoff or immutable association preview, and gates association dispatch. Use
the entry-point contract in `ora-resource/ora_rest_execution.md`; do not bypass
it with a direct REST write or standalone provider call from this task.

Resolve a supplied Specific Manager Types label as an agent-owned validation:
resolve the canonical code through `core.fusion-api.apps-common.lookups` using the
`PER_SUPERVISOR_TYPE` lookup type. Match the requested display label or code
exactly and retain the returned canonical code and eligibility evidence under
the lookup contract's alternatives; a separate selectable flag is not mandatory.
Do not ask a consultant to manually supply ordinary target-tenant LOV evidence
before these approved read-only routes have been attempted. Escalate only an
actual no-match, multiple-match, authorization failure, or documented provider
contract gap after exhausting the declared evidence alternatives. Read the
configured environment and relevant retained same-target execution evidence
before escalation. Classify an omitted field as unknown rather than false.
Do not invent a route or ask the consultant to collect ordinary technical
evidence. Record a skill limitation when no declared alternative resolves it;
continue independent tasks and ask only for genuinely missing business input
or a required governance decision. Use the resolution procedure in
`ora-resource/ora_reference_lookups.md` before reporting a blocker.

For a template intended for new feedback requests, require Active status and a
questionnaire. When an Active template is in use, only its name or description
may change. Questionnaire replacement and deletion require confirmed
not-in-use state.

Preserve questionnaire readiness, exact identity, in-use state, source evidence,
and the immutable REST preview in the project workspace. Approval applies only
to that exact request and never authorizes a questionnaire provider mutation.

## Best-practice consultation and precedence

For consultant questions, use the [canonical Request Feedback Template
reference](../best-practice-rules/hcm-requested-feedback-template/README.md)
to identify the applicable design, dependency, security, notification,
testing, migration, or diagnostic topic. Consult it only after classifying the
request and loading this task's applicable `ora_*` resources.

The reference is advisory. This task contract and FDOS approval/external-action
safeguards, authorized target-tenant evidence, and current official Oracle
documentation all override it when they conflict. Do not use reference guidance
to infer an API, CSV schema, identifier, privilege, tenant setting, or approved
operation. Record conflicts as a decision or diagnostic and stop when the
active workflow has no authorized route.

For a Performance Goal Feedback activation, treat a change to the intended
active template as consequential: identify the target tenant's current active
template(s), show the potential effect on other goal-feedback templates, and
obtain approval for that exact effect before any supported mutation route.

Keep Feedback Template setup separate from runtime `FeedbackRequest` HDL/HSDL
or REST discussion. Runtime transaction support never authorizes configuration
of Feedback Templates.




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

Use the parent functional-area skill `hcm.performance-management.requested-feedback-template` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Post-write verification

Use the exact-identity GET and field comparison in `ora_rest_execution.md`.
Persist a failed or partial result if verification is unsuccessful; never retry
the mutation automatically. Record sanitized HTTP status, relative path, request
ID/ECID when available, stage, failure class, and next action. Use bounded client
timeouts; an uncertain write outcome requires an exact-identity read before any
new approval. Never persist credentials, access tokens, or sensitive responses.

## Redaction and failure handling

Redact credentials, secrets, tokens, private keys, and sensitive response data
from diagnostics and execution records. Keep only the approved non-sensitive
setup payload and sanitized evidence in the selected project workspace.
Classify failures as input validation, catalog mismatch, auth/authz,
transport/environment, Fusion API, artifact persistence, or approval blocker.
For a timeout, record the target alias, operation, relative path, elapsed time,
last known status, and exact-read next action. Preserve partial outcomes and an
errors array; do not report an unverified write as success. Recovery does not
authorize automatic mutation retries.

## Agent-owned reference resolution

General Feedback custom creation uses the declared HRA eligible-subscriber policy plus current target-bound Questionnaire provider validation. The agent collects subscriber, strict live schema, reference, design, lifecycle and create-identity checks and records a `provider_validation` receipt bound to the complete provider specification. The resolver derives policy provenance from that receipt; do not request ordinary evidence from the user or require an ID/association for a not-yet-created questionnaire. Resolve subscriber/template restrictions and contrary evidence before handoff. This does not waive provider validation, import approval or post-creation content/association readback. Performance Goal Feedback retains its seeded-only rule.

Manager selection All maps to `ShareWithManagers=ALL`; it is not a lookup code and must not be expanded into a snapshot of specific types. Specific selections use the declared commonLookupsLOV lookup for PER_SUPERVISOR_TYPE, complete pagination and exact code/meaning resolution. Keep enabled/effective checks where required. Supply `manager_selection` to the wrapper; it validates the outgoing value without silently changing the payload.
