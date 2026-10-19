---
skill_id: "hcm.hcm-tool.touchpoints-aggregate-data-process"
name: "Touchpoints Aggregate Data Process Implementation Guidance"
description: "Plans Touchpoints implementation dependencies, records customer confirmations, delegates Performance Management setup and manual UI tasks through existing Run Book operations, and gates Full aggregation followed by daily Incremental scheduling."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Touchpoints Aggregate Data Process"
functional_area_code: "CUSTOM_TOUCHPOINTS_AGGREGATE_DATA_PROCESS"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.7.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "touchpoints_aggregate_data_process_scope"
  - "touchpoints_aggregate_data_process_requirements"
  - "touchpoints_profile_option_request"
  - "execution_approval"
  - "touchpoints_workflow_state"
  - "runbook_task_snapshot"
  - "dependent_tasks"
  - "task_outcomes"
  - "feedback_profile_evidence"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "profile_option_result"
  - "diagnostics"
  - "audit_summary"
  - "touchpoints_configuration_plan"
  - "runbook_task_bindings"
  - "runbook_provisioning_plan"
  - "configuration_readiness"
  - "ordered_owner_handoffs"
  - "execution_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "hcm.hcm-tool.touchpoints-aggregate-data-process.aggregate-oracle-touchpoints-data"
  - "core.fusion-api.apps-common.profile-options"
  - "hcm.performance-management.check-in-template.check-in-templates"
  - "hcm.performance-management.requested-feedback-template"
  - "core.runbook"
uses_core:
  - "core.runbook"
  - "core.fusion-api.apps-common.profile-options"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Synchronizes local generated task contexts and owner handoffs from verified Run Book bindings; no Fusion write in this step."
  - "After operation-specific authorization, delegates manual task additions and task comments/status updates to core.runbook."
  - "May read effective or configured Touchpoints profile-option values."
  - "Reads mandatory Request Feedback SITE profiles through the declared profile provider when Feedback is selected; delegates required approved updates and readback."
  - "After an exact preview and explicit approval, may create or update a selected Touchpoints profile-option value through core.fusion-api.apps-common.profile-options."
required_privileges:
  - "Run Book task read, add, and update privileges for the selected operations."
  - "Access to read the selected Touchpoints profile option definition and value."
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV for profile-option value mutations."
---

# Touchpoints Aggregate Data Process Implementation Guidance

## Purpose

Owns Touchpoints implementation orchestration and routes these technical capabilities:

1. Aggregate Oracle Touchpoints Data ESS submission through the nested catalog task,
   with Full aggregation followed by a separately approved daily Incremental schedule.
   Daily is a manual tracking row owned by the same ESS skill; it cannot execute
   until same-context Full success is verified. The scoped
   `scripts/touchpoints_ess_handoff.py` coordinates the unchanged core dependency,
   explicit readback fields and durable identity checkpoints.
2. Read or update source-confirmed Touchpoints profile-option values through the shared Apps Common provider.

## Touchpoints Implementation Workflow

Use [the deterministic orchestration contract](references/deterministic-orchestration.md)
for task identity, ordering, prerequisite closure, owner handoffs and outcome
classification. That contract governs orchestration when older examples differ.
`scripts/touchpoints_runbook.py` generates the authoritative ordered plan.
After provisioning, `scripts/touchpoints_orchestrator.py --project-root
project/{project_id} --sync-context` automatically reconciles local task contexts
and owner handoffs before selecting task work. For read-only reviews use
`--dry-run`. Never resume a stopped run as part of a source-code review or repair.
No local planner output authorizes a Fusion mutation.

Whenever Feedback is selected, use [automatic Feedback profile prerequisites](references/feedback-profile-prerequisites.md).
The planner supplies the mandatory profile-provider task without requiring user
input. During execution, refresh both SITE values through the declared read
adapter before task mapping and template write handover. Delegate non-Y/absent
values to the existing profile provider with its exact-write approval and
readback gates. Route Feedback through its parent prerequisite contract before
the nested template task. Profile evidence never proves template POST capability
or template privileges.

For an implementation objective (including create, extend, or resume a Touchpoints
Run Book), first read [the implementation workflow](references/implementation-workflow.md).
First classify the request using the scope contract in that reference. Only a
full Touchpoints enable/configure/implement objective includes Check-In Templates,
Request Feedback Template, Pulse Surveys and Nudges when omitted by the user.
A request for specific tasks routes to their owning skills and includes only
those tasks plus their actual mandatory prerequisites.
Accept explicit already-configured and Not Applicable confirmations as described
there; never require new configuration merely because a dependency was inferred.

Use `scripts/touchpoints_runbook.py --input <state.json> --tasks <snapshot.json>
--dry-run` as the implementation entry point before presenting a plan, creating,
repairing or resuming a Run Book. Read the executable-entry-point section in the
workflow reference. Persist its complete output as the configuration plan; do not
hand-author a separate two-action plan from the user's explicitly named tasks.
The underlying evidence evaluator alone is insufficient for a Run Book handoff.
Show the complete ordered scope before initial creation. Label the returned
initial dashboard as partial provisioning until `runbook_complete` is true;
creation order does not establish execution order. Continue authorized planning
after displaying the dashboard. Present generated `manual_additions` with their
explicit sequences and any `sequence_updates` for operation-specific approval.
Apply approved sequence repairs first, refresh the snapshot, and regenerate
additions; never rely on core's append-by-default sequence for configuration tasks.
Scope is required: missing scope must not default to full implementation.
Resolve ordinary owner technical evidence as agent-owned work. Ask only for
business choices, exact writes, or governance decisions explicitly required by
policy. Missing technical evidence is `technical_failure`/skill limitation,
never a request for customer privilege or route justification. Preserve actual
owner preflight gates; never assert unverified checks to avoid a blocker.
For selected standalone ESS use --require-ready standalone; for selected daily
scheduling use --require-ready daily, which still requires verified Full success.
Before implementation Full/daily preview AND dispatch, rerun with `--require-ready full` or
`--require-ready daily`; a nonzero exit blocks the handoff. Readiness never grants
execution approval. Standalone read/tracking requests remain read-only.

Keep cross-task gates here, not in shared Run Book code. Existing mapped tasks
use the canonical initializer/create route. Additional manual tasks use the
existing explicitly authorized `core.runbook` add/update operations. Never patch
the canonical generated plan to smuggle in an unmatched task or invented code.

Standalone profile reads, status checks and tracking an existing ESS request do
not create or expand a Run Book. For a new submission associated with this
implementation, the nested ESS task must consume current workflow readiness;
opening the child skill directly does not bypass the implementation gates.

## When to Use

Use this functional-area skill after HCM Tool scope is confirmed and the project needs Touchpoints aggregation processing or a governed Touchpoints profile-option operation.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Touchpoints Aggregate Data Process` (`CUSTOM_TOUCHPOINTS_AGGREGATE_DATA_PROCESS`)

## Setup Tasks

1. [Aggregate Oracle Touchpoints Data](aggregate-oracle-touchpoints-data/SKILL.md) (`CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA`)

## Capability Routing

| Request | Route | Execution boundary |
|---|---|---|
| Create, repair, resume a Touchpoints implementation or submit its new aggregation | This skill's `scripts/touchpoints_runbook.py`, then nested ESS skill | Scope-aware plan and verified bindings precede ESS preview/approval; implementation also requires full readiness. Do not route directly to generic creation or ESS. |
| Review job metadata or track an existing ESS request | `hcm.hcm-tool.touchpoints-aggregate-data-process.aggregate-oracle-touchpoints-data` | Read-only; does not expand a Run Book. |
| Read a supported Touchpoints profile option | `core.fusion-api.apps-common.profile-options` | Read the definition and configured or effective value; do not infer a level or value. |
| Create or update a supported Touchpoints profile-option value | This implementation workflow when part of a Run Book; then `core.fusion-api.apps-common.profile-options` | Preserve the approved selected scope. Read the definition/current level-specific value, present an exact preview, and obtain write approval. |

Do not submit Scheduler REST requests or implement profile-option REST calls in
this skill. Delegate those technical operations to the declared core skills.

## Touchpoints Profile-Option Scope

The following codes are source-confirmed Touchpoints references:

- `ORA_HRE_ENABLE_TOUCHPOINTS`
- `ORA_HRE_OVERDUE_CHECKIN_THRESHOLD`
- `ORA_HRE_SUPPORTED_MANAGER_TYPES`
- `ORA_HRE_UPCOMING_CHECKIN_THRESHOLD`

Treat this list as known references, not as proof of a requested value, allowed
level, or current environment configuration. Pass an exact requested code to
the core provider and validate the live definition before use. An arbitrary
`ORA_HRE_*` prefix match does not authorize a write. For another exact code,
allow a read-only definition lookup; block mutation until product-owned source
evidence confirms that the code is part of Touchpoints scope.

## Profile-Option Mutation Gate

Before every profile-option state change:

1. Confirm the configured Fusion environment and active project Run Book.
2. Read the profile definition and current level-specific value through
   `core.fusion-api.apps-common.profile-options`.
3. Verify that the exact requested level is enabled and updatable. Do not
   default the level to site, product, or user scope.
4. Validate the requested value from live metadata or approved product
   guidance. The profile names and descriptions do not establish an allowed
   value contract.
5. Present an immutable preview containing the environment, profile code,
   level and level key, current value, requested value, operation, privilege,
   and audit-artifact destination.
6. Require an affirmative response to that preview immediately before the
   mutation. Accepted approval wording includes `Approved`, `yes`, or
   `go ahead`, matched case-insensitively after trimming whitespace, provided
   the response contains no conflicting or changed instruction.
7. Perform the write once, then re-read the same level-specific value. Never
   retry an uncertain or failed POST, PATCH, or DELETE automatically.

An approval is bound to the exact preview. Any change to the environment,
profile code, level, level key, current value, requested value, or operation
invalidates it and requires a new preview and approval. A request that merely
mentions an approval phrase before the preview is not approval for the write.

When one user request includes multiple profile-option changes, present each
change as a separate immutable item. One approval may authorize the displayed
batch only when every item, order, and target is fixed; stop the batch on the
first failed or indeterminate write. ESS submission remains a separate state
change with its own exact preview and approval.

## Preflight Checks

Before either routed capability can change Fusion state, verify the exact
environment identity, active project Run Book, authenticated session, required
catalog task or profile-option identity, requested values, unique
artifact destination, and whether the operation is read-only or live. Fail
closed as `input_validation`, `catalog_or_metadata_mismatch`,
`authorization_or_privilege`, `artifact_persistence`, or `approval_blocker`
before invoking a mutation when any check is unresolved.

The nested ESS task performs its own job-specific preflight. It does not require
a separate submit-privilege check or pass privilege evidence in the ESS handoff.
Fusion's response to the approved submission/monitoring operation is authoritative;
never use a recent-request lookup or role/UI probe as an ESS submission gate.
For a profile
option, also verify the live definition, enabled level, current value, requested
value contract, required profile privilege, exact preview, and current-turn approval described above.

## Retry, Timeout, and Recovery

Profile-option reads may use the bounded read-only recovery behavior of the
core provider. Do not automatically repeat an uncertain profile-option write.
Reconcile the exact level-specific value read-only, preserve the result and
diagnostics, and require a rebuilt preview plus fresh approval before any new
write. ESS timeout and recovery behavior belongs to the nested task and the
declared ESS core provider.

## Error Redaction

Redact credentials, OAuth tokens, authorization headers, cookies, token-cache
content, private keys, full response bodies, and sensitive profile values from
previews, diagnostics, audit records, and project artifacts. Retain only the
minimum sanitized status, endpoint or operation, environment alias, profile
code and level, external identifier or ECID, failure class, and safe next
action needed for review and recovery.

## Diagnostics and Audit

Persist sanitized profile-option planning, execution, and verification results
under the declared project artifact path. Record the environment, profile code,
level, operation, approval fingerprint, HTTP result summary, verification
outcome, ECID or request identifier when returned, failure class, and safe next
action. Never persist credentials, OAuth tokens, authorization headers,
token-cache content, or sensitive profile values.

## Inputs

- `implementation_objective`
- `project_context`
- `touchpoints_aggregate_data_process_scope`
- `touchpoints_aggregate_data_process_requirements`
- `touchpoints_profile_option_request`
- `execution_approval`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `profile_option_result`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skill for ESS execution. Keep profile-option
domain rules in this functional-area skill and technical CRUD in
`core.fusion-api.apps-common.profile-options`. Track token usage for every
generated project artifact or skill-run record using the manifest policy.
