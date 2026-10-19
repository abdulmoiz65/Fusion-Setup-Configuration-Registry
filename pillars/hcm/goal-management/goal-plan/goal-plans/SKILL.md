---
skill_id: "hcm.goal-management.goal-plan.goal-plans"
name: "Goal Plans Setup Task Guidance"
description: "Provides task-specific setup guidance for Goal Plans under the Goal Plan functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Plan"
functional_area_code: "ORA_GOAL_PLAN"
task_code: "HRG_MANAGE_GOAL_PLANS"
task_name: "Goal Plans"
parent_skill_id: "hcm.goal-management.goal-plan"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM goal management pillar team"
version: "0.1.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "goal_management_execution_control"
  - "assignment_effective_date"
  - "ess_execution_options"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "immutable_ess_assignment_preview"
  - "ess_assignment_execution_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
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
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/goal-plans/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/goal-plans/current/"
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
  - "After explicit approval, may submit one Assign Goal Plans ESS request through core.fusion-api.ess-job-submitter and poll its status."
required_privileges:
  - "Fusion privileges appropriate to manage the selected Goal Plan."
  - "Fusion privileges appropriate to submit and monitor Manage Goal Scheduled Process."
---

# Goal Plans Setup Task Guidance

## Goal Plan prerequisite

Regular Goal Plan work requires an active Review Period. Validate that
prerequisite and obtain executable order from the shared
implementation-planning services rather than from source-document layout.

## Purpose

For create-status intent and post-create activation decisions, follow
[the lifecycle follow-up contract](../../goal-management-common/lifecycle-follow-up.md).

Before any mutation or ESS preview, require an `allowed` Goal Management
execution control whose exact task identity, Goal Plan functional area,
sequence, skill path, and approved plan fingerprint match this task. A direct
Goal Plan instruction or approval cannot bypass an earlier unfinished task in
the input-specific queue. Missing, stale, stopped, or mismatched control
returns `BLOCKED` before target lookup or payload preparation.

Support `get`, `list`, `search`, `create`, `update`, `activate`, `inactivate`,
`maintain_population`, `manage_plan_goal`, `maintain_document_association`,
`manage_assignees`, `sync_performance_documents`, `prepare_assignment`,
`csv_export`, and `csv_import` as
independent consultant operations. Item and advanced-search reads execute
through the core REST client without write approval. Normalize `goal_plan_kind` to `regular` or
`primary`. Create never implies activation; saving population never implies
assignment.

## Best-practice context

Consult sections 2-7 and 15 of the [HCM Goal Management best-practice
reference](../../goal-management-common/best-practice-rules/hcm-goal-management/README.md)
for route selection, regular-versus-primary design, dates, weighting,
population, Performance Document integration, assignment-rerun behavior, and
lifecycle checklists. The reference is advisory; current Oracle documentation,
target-tenant behavior, and this task's exact REST and approval contract take
precedence. Configuration and assignment remain separate operations.

## Greenfield HDL DAT route

`csv_export` and `csv_import` are FSM setup-data operations. They are not a
route for creating a new Goal Plan or its children. Enter this route only when
the Goal Management router returns `hdl_generate` or `hdl_dat_preflight`.
REST remains the normal-volume default. For `hdl_generate`, first resolve and
validate every Goal Plan business row, apply the same required-field,
defaulting, reference, duplicate, date, key, population, and child rules as the
REST route, then pass those rows to `core.data-loader` to generate a current
target-metadata source and immutable ZIP. The consultant need not supply a DAT.
For `hdl_dat_preflight`, preserve and validate the supplied source. Follow
`pillars/hcm/goal-management/goal-management-common/hdl-source-generation.md`; no validation
failure is waivable in either mode.

Require `GoalPlan.dat`. Permit `GoalPlanTranslation.dat` and `Goal.dat` only
when their records are actually included. A parent-only `GoalPlan.dat` is
valid. Supported `GoalPlan.dat` children include `GoalPlanDocTypes`,
`MassRequest`, `MassRequestAssignment`, `EligibilityProfileObject`,
`MassRequestHierarchy`, `MassRequestExemption`, `GoalPlanAssignment`, and
`GoalPlanGoal`. Each child must reference a parent earlier in the package or
an exact existing target parent. Validate every `METADATA` and data row,
current-template mandatory fields, supported source or user keys, component
order, operation intent, and delete order. Require exact target-tenant evidence
for the Review Period, worker and assignment, Goal Plan document type when
`IncludeInPerfdocFlag=Y`, and every other referenced value. Accept minimum
business input: derive the configured environment, current timestamps, audit
manifest, source keys for confirmed creates, target-defined defaults, and the
authenticated requester's Person Number internally. If no explicit
`MassRequest` is supplied, add `ReqSubmittedByPersonNumber` and
`RequestSubmissionDate` to the prepared Goal Plan copy. If a `MassRequest` or
template `Goal` is supplied, add the authenticated requester to its applicable
requester/assigned-by field. Never add requester fields to both Goal Plan and
its explicit Mass Request, overwrite supplied data, equate requester with the
target population, or guess Goal Plan name, dates, Review Period, document
type, organization, eligibility profile, or worker assignment. Do not substitute
FSM, REST, a browser workflow, or fabricated business values after explicit HDL intent.
`core.data-loader` owns immutable archive creation,
preflight, preview, approval, upload, and result reconciliation; this task
must not create records directly.

For `hdl_dat_preflight`, before `core.data-loader` can build the immutable preview, run
`pillars/hcm/goal-management/goal-management-common/scripts/hdl_dat_preflight.py` against the
consultant source and internally resolved runtime context. First create a
separate prepared copy with `hdl_dat_enricher.py`, then create the audit-only
manifest with `hdl_manifest_builder.py`. The consultant never supplies or edits
that manifest. It declares the permitted create/update/delete outcome for every
scoped source or user-key identity, current mandatory fields, existing-parent
evidence when needed, and structured target evidence. Include an internally
generated `validationTime`; evidence is
non-waivable when it is later than that time or older than the allowed window
(24 hours by default). Pass the resulting error-free report in
`finalData.hdlValidation` and set `finalData.format=goal-management-hdl-dat`.
After creating the exact immutable archive, `core.data-loader` must add its
SHA-256 as `finalData.archiveSha256` before Task Hook preview. Task preflight
must never fabricate a digest for a future archive.
No validation failure is waivable.

For HDL Goal and GoalPlanGoal rows, resolve the complete worker-goal user key
before enrichment, using the file-specific attribute names and `rowBindings`
contract in `goal-management-common/hdl-source-generation.md` (relative to the Goal Management
offering). The requester is not the ordinary goal owner. Do not substitute
numeric worker IDs for the verified worker-number route. Resolve
EligibilityProfileObject.ObjectId through the selected plan's MassRequest,
retain its relationship evidence, and use GoalPlanExternalId for the applicable
plan reference. If a new MassRequest must first be generated, plan that
dependency before package approval rather than attempting unresolved children.
Library-backed goals retain their resolved library reference; normal goals
remain independent Goal records. These HDL checks do not alter REST or ESS.

## Regular and Primary Goal Plans

- A regular Goal Plan requires one active Review Period. Its dates must be contained
  by that period. When both technical plan dates are omitted, default both from
  the resolved Review Period; a complete explicit pair overrides the default,
  while a partial pair is invalid. It may use included/excluded workers, active Goal
  Management-compatible Eligibility Profiles, plan goals, and the separately
  approved Assign Goal Plans ESS flow. Its exact name must be unique within the
  associated Review Period; dates do not distinguish duplicates. Before create,
  validate that the current HR specialist person
  context is complete because it governs security and assigner attributes.
- A Primary Goal Plan sets `PrimaryGoalPlanFlag=true` and
  `ReviewPeriodId=null`. It has no worker, Eligibility Profile, or plan-goal
  sections, is not assigned through ESS, and is available to all active Review
  Periods while active. Only one Primary Goal Plan may be active per
  organization. It is available to all users and its access design permits
  them to update goals. Weighting defaults to enabled; enforcing a 100-percent
  total defaults to disabled. A Primary plan cannot accept plan goals during
  create or edit.
- The public resource requires technical start/end dates on create. Obtain
  Primary-plan technical bounds from current metadata or an owner-approved
  Primary Goal Plan template. Never copy tenant capture values or change the
  existing bounds during update unless explicitly requested and supported.

## Dependency boundary

### Basic-details resolution

Before a Goal Plan preview, resolve explicit basic-details requirements using
the offering-owned Goal Setup Field Resolution support package at
`pillars/hcm/goal-management/goal-management-common/goal-setup-field-resolution/README.md`. Validate every LOV
selection against current metadata. Access language may resolve to one of the
advertised update-access values; when omitted, use the advertised all-role
default and disclose it. Goal Plans contain performance goals, so a stated
maximum performance-goal count maps directly to
`MaximumGoalsNumberInGoalPlan`; never ask whether it applies to development or
other goal types. Treat `EnforceMaximumGoalsInGpFlag` as tri-state. Omit it and
preserve returned `null` when enforcement is not explicitly requested; set it
to `true` only for restrictive language such as prevent, must not exceed, or no
more than; set `false` only for an explicit no-enforcement instruction. A
purpose or audience statement does not create an Eligibility Profile, worker,
population, or assignment route.

Require one Review Period only for a regular plan and validate its dates within
the period envelope.
Resolve an existing active Eligibility Profile when eligibility is requested;
its owning setup task is `BEN_MANAGE_ELIGIBILITY_PROFILES`. Do not create or
edit that object here. Use the current environment's validated
`eligibilityProfilesLOV` lookup and require an
active profile whose usage is compatible with Goals Management. Read every
LOV page before deciding. When the consultant or a prior project artifact
supplies an exact profile business name, match it exactly and
case-insensitively: resolve one match and keep its ID internal, present the
business-facing candidates when more than one match remains, and report a
missing profile only after the complete lookup returns none. Never ask for an
ID when a business name can be resolved.

When the source supplies only semantic population criteria, such as a Legal
Entity, search the active Goal Management-compatible profiles and verify the
stored profile criteria through an authoritative read capability when one is
available. Resolve directly only when exactly one profile's verified criteria
matches the requirement. Present candidates for consultant selection when
more than one match remains or when the LOV exposes names but not enough
criteria to prove the match; never choose from lexical similarity alone. An
unavailable `BEN_MANAGE_ELIGIBILITY_PROFILES` mutation provider does not block
this read-only discovery. Invoke that provider path only after no existing
profile matches and profile creation or maintenance is actually required. Resolve
Performance Document Types only for integrated performance-document use cases;
each type must be active and cover the plan date range. Resolve existing workers by exact person,
active assignment, and effective date. If a test worker must be created, stop
and route to GHR/HDL with synthetic non-production data and separate approval.

If Eligibility Profile creation or maintenance is requested, discover the
canonical provider for `BEN_MANAGE_ELIGIBILITY_PROFILES`. When no executable
provider skill is available, return `PROVIDER_SKILL_UNAVAILABLE` with the task
code, missing provider capability, and resume context; do not invent a provider
ID or emit a mutation payload. After the provider becomes available, its own
validation and approval rules govern the profile mutation. Re-resolve the
saved active profile before resuming the Goal Plan operation.

## Independent operations

For explicit REST batch intent, read [REST batch workflow](../../goal-management-common/rest-batch.md).
Reuse this skill's validated bodies and prerequisites for every plan; activation
requires each plan to be ready. Resolve parent CRUD batch eligibility through the
maintained Goal Management capability resolver plus current Goal Plan describe
methods. Do not require a `batchEnabled` collection field or use an unrelated
custom-action flag. HDL batch upload remains separate.

- Create inactive after checking the exact Goal Plan name within the associated
  Review Period. Plan dates remain independently validated. Use a supplied
  immutable external ID when present; when current metadata has server default
  expressions for both `GoalPlanId` and `GoalPlanExternalId`, omit both IDs,
  disclose that Fusion derives the External ID from the generated Goal Plan ID
  in the approval preview, and retain the returned identity after creation.
- Materialize the complete minimum create contract: name, regular/primary
  flag, inactive `GoalPlanActiveCode=I`, valid plan dates, and Review Period
  for a regular plan. Reject active create or a missing minimum field before
  preview. Bind the internal approval fingerprint to environment, operation,
  request path, business identity, and exact steps; verify every approved
  create field after POST.
- Update only explicitly requested fields and preserve omitted collections.
- For a create with an explicit maximum but no enforcement requirement, include
  `MaximumGoalsNumberInGoalPlan` and omit
  `EnforceMaximumGoalsInGpFlag`. For explicit enforcement, use
  `build_goal_plan_create_execution_plan`: create inactive with the maximum and
  no enforcement field, verify that the maximum persisted, then patch only
  `EnforceMaximumGoalsInGpFlag=true` and verify again. Present the complete
  conditional sequence in one immutable preview; one approval may cover both
  exact writes because the generated item ID is resolved from the approved
  stable business key. Stop without retry on a failed, uncertain, or mismatched
  stage.
- Activate or inactivate only after a fresh read and separate approval.
- Maintain one explicit population child at a time: include worker, exclude
  worker, associate Eligibility Profile, or remove a returned child row.
- For a Goal Plan Eligibility Profile association, resolve the active
  Goal-usage profile from the population requirement and build only the
  `perfGoalEligibilityProfiles` child body. Tenant-validated runtime evidence
  confirms `TalentObjectType="GOAL"` for this Goal Management child contract;
  derive it inside the skill and do not ask the consultant to supply it. This
  mapping is not reusable for Check-In, Performance Management, or any other
  eligibility-profile association unless that product's own contract is
  verified separately. Derive `RequiredFlag=true` only from explicit
  requirement language such as required, mandatory, or must be enforced;
  otherwise preview `RequiredFlag=false`.
- An included-worker create requires the selected worker's `PersonId`, one
  confirmed active `AssignmentId`, and an explicit `CascadingLevel` normalized
  from the local domain contract.
  Omitted CascadingLevel defaults to string `"0"` (Self); a supplied value must
  match the local contract in `ora-resource/ora_defaulting_rules.md` and any
  non-Self scope requires current advertised hierarchy evidence.
  `ManagerAssignmentId` is never an included-worker payload field: it is only
  an optional assignee-search filter.
- Reject population and assignment operations for Primary Goal Plans.
- For a template goal on an **existing** regular plan, resolve the logged-in
  HR/admin `PersonId` and confirmed active primary `AssignmentId` only as
  request context; they are not final assignee values. Fetch that exact plan's
  `MassRequestId` immediately before the create using an item GET with an
  explicit `fields` projection that includes `MassRequestId`; validate the
  result with `resolve_goal_plan_mass_request_id`. An omitted key means the
  projection is incomplete, not that Fusion returned null. Never require or send
  `MassRequestId` while creating a new Goal Plan.
- Adding a Goal Plan goal to an existing regular Goal Plan is a governed Goal
  Plan update flow from the consultant's point of view. For a create, prefer
  the current public `POST goalPlans/{GoalPlanId}/child/performanceGoals`
  collection when Goal Plans metadata advertises it. Use an ADF batch only
  when that create operation is not advertised and a current batch contract is
  independently resolved; never invent either route. A request for one
  approval over multiple Goal Plan updates does not select that batch route:
  approval grouping and transport selection remain independent.
- When adding a selected Performance Library Goal, re-read its current source
  details and map its runtime identity as `ReferenceContentItemId`. Copy only
  supported source fields. If both template-goal dates are omitted, default
  them from the existing Goal Plan dates; preserve a complete explicit pair and
  reject a partial pair.
- Goal additions have two exclusive modes. A library-backed addition requires
  a fresh non-null `ReferenceContentItemId` for the selected Library Goal. An
  independently authored non-library goal must not carry a non-null Library
  Goal identity; omit the field or retain explicit null only when current
  runtime metadata requires it. Never infer or silently switch the mode.
- A consultant can change object context at any time. Before every Goal Plan
  goal preview, bind `object=goal_plan_template_goal` and the operation's
  current advertised payload contract. Discard any preceding Library Goal
  resource root, item key, string-weight rule, ETag/header rule, DFF part, or
  payload fields. Re-read the selected Goal Plan, its MassRequestId, and
  current HR-admin context after the bind; do not carry them from another flow.
- The skill owns current-contract and current-admin discovery. It must use the
  published Goal Plans metadata when it advertises the child-create route and
  resolve the authenticated caller through the owning worker route. Never ask
  a consultant to supply REST paths, runtime revisions, or administrator IDs.
- A basic Goal Plan create must not be paused for HR-specialist person or
  assignment context when its current create metadata has no caller fields.
  Invoke authenticated-caller resolution only for template-goal work or when
  current metadata explicitly requires those fields. When it is required,
  resolve it from the active authenticated Fusion session and fail only after
  that route cannot return one active primary assignment.
- Use existing Chrome only for the documented OAuth handoff or when a selected
  operation has no published REST contract. It is never a substitute for a
  published Goal Plan REST create/read route.
- When a consultant supplies Goal Plan HDL DAT files, use the declared
  `core.data-loader` route. If its executable HDL provider/contract is absent,
  return `HDL_ROUTE_GAP`; do not ask the consultant to identify an API route
  or substitute a REST mutation.
- Plan-goal duplication is a create-from-source operation, not a REST
  `duplicate` action: resolve the source goal, show the copied-field diff, and
  use the current advertised child-create contract. Import and
  performance-document synchronization use their documented action contracts.
  Goal Plan goal reorder is unsupported because VBCS itself does not persist it;
  return `UNSUPPORTED_UI_BEHAVIOR` and do not treat it as a pending REST gap.
- Assignee search and deletion are independent from population maintenance.
  Use the goal-plan-assignee resource for an exact, read-only search. A
  GoalPlanId is required; a department (OrganizationId) and manager are
  independent optional filters. When a consultant supplies a manager PersonId,
  resolve its current active assignment before mapping the action's advertised
  manager-assignment filter. Batch deletion is a separately previewed,
  approved consequential operation.

## Functional design and lifecycle rules

- When Goal Setting Info is requested, explain that its post-end controls apply
  to workers only and are additive to `GoalAccessLevelCode`. Validate the
  goal-setting start/end dates and the two independent post-end restrictions:
  workers adding goals, and workers editing/canceling/deleting goals. If either
  date is absent, propose the corresponding Goal Plan boundary for explicit
  consultant confirmation before preview. Run this resolution before generic
  access/evaluation lookup discovery; date-bound Goal Setting Info language
  must not be routed to `CanDelHRGoal`.
- Validate evaluation type, HR-assigned-goal delete/cancel access, weighting,
  enforced weight total, optional minimum/maximum performance-goal counts, and
  explicitly requested maximum enforcement against current metadata before
  activation. Preserve a raw returned `null` enforcement value; do not
  normalize it to `false` in a preview or approval fingerprint.
- A plan goal's start and target completion dates must be within the Goal Plan
  dates. Library-goal selection, measurements, tasks, task measurements, target
  outcomes, and assignee definition editing are conditional capabilities and
  must be advertised by current setup/metadata. Import Goals copies goals from
  another Goal Plan and is distinct from FSM CSV import.
- Multiple Eligibility Profiles use required-profile semantics: a worker must
  meet every profile marked required. Supported population scopes are selected
  employee, direct reports, all reports, selected plus direct reports, and
  selected plus all reports; exclusions are evaluated separately.
- Performance Document Types must be active, start no later than the Goal Plan,
  and end no earlier than the Goal Plan. Matching evaluation types support
  performance-document synchronization.
- An assigned Goal Plan cannot be deleted. A Review Period cannot be changed
  while assignees remain. Pending-approval plans cannot be updated, and no
  requested change is final until its approval completes. Goal Plan deletion
  and assignee deletion remain guided-UI operations unless current
  authoritative REST metadata advertises an exact governed contract.

## Primary Goal Plan integrations

- When active, Talent Review performance goals are added to the Primary Goal
  Plan for the selected Review Period.
- When a Primary Goal Plan is associated with the document type used by a
  performance template, creating the performance document creates the Primary
  plan for that document's Review Period without associating the Primary plan
  itself to one Review Period. Template goals and goals copied from the
  performance document are added to the Primary plan.

## ESS assignment handoff

Goal Plan definition does not require population or assignment inputs. When
assignment is not requested, classify omitted assignment details as
`not_in_scope`; show assignment as an optional next action at task review, not
a configuration blocker. When assignment is requested, retain actual selector,
active-plan, metadata, and approval checks for that operation only.

An omitted assignment effective date defaults to today's date in the user/project
timezone (execution-host local date if no timezone is known). Resolve it once
at preview with `resolve_assignment_effective_date`, disclose the concrete date
and its default provenance, and bind it into the payload, impact evidence and
approval. Pass that same explicit date at submission, even across midnight;
never recompute an approved date. Honor supplied dates and reject malformed
ones. This ESS default does not change worker-resolution date requirements.

Call `build_assign_goal_plan_ess_payload` with `environment` and mandatory
`impact_evidence`. Preflight validates the fresh configured population selector,
environment/plan/MassRequestId/effective-date binding and execution approval.
`population_verified` and `population_evidence_ref` describe that configuration,
not a precomputed employee list. ESS evaluates eligibility during execution.
Do not request measured_count, approved_maximum, employee IDs or an eligibility
export as prerequisites. Record actual assignee counts after execution.
`argument17=1` is an option flag, not a one-person selector or cap. If a hard cap
is required, stop until an owner-supported bounded route is verified. Profile
names alone do not prove geographic scope (Outside US does not imply Canada).
For an exact named existing profile, resolve its current identity, active state,
and configured association through the existing route. A consultant's explicit
confirmation of its intended criteria can be recorded as consultant-confirmed
scope at review; do not demand a screenshot/export solely because criteria are
not exposed. Do not label those criteria independently verified. Unconfirmed
semantic-only selection, ambiguous/inactive profiles, or contradictory evidence
still require resolution before assignment, not before independent definition.

Before invoking `core.fusion-api.ess-job-submitter`, preview the population
selector, environment, job definition,
process type `Assign goal plans`, process name equal to the Goal Plan name, and
the resolved effective date (supplied or defaulted to today). The Goal Plan route passes the dependent skill its
declared inputs: `fusion_environment_context`, a complete current verified
`request_payload`, and approved `execution_options`; it retains the fresh Goal
Plan ID/name, MassRequestId, impact evidence, and ESS approval as audit
evidence. Assign Goal Plans uses **Manage Goal Scheduled Process** through ESS
job definition
`JobDefinition://oracle/apps/ess/hcm/goals/core/ScheduleProcessJobDef`,
application `EarHcmEss`, product `HRG`, and mode value
`ASSIGN_GOAL_PLANS`. Build the Scheduler body dynamically from the selected
fresh active regular Goal Plan: one plan name, its Start Date, End Date, and
MassRequestId, plus the explicitly approved effective date. Current evidence
supports one Goal Plan per submission because the Scheduler argument contract
contains a single process/plan name and one MassRequestId; do not batch multiple
Goal Plans into one request unless a separate verified contract is added. The
verified numeric option flag for this Assign Goal Plans contract is passed only
as its own positional argument and must not be interpreted as purge days or
reused by unrelated Goal Management scheduled processes. Bind a separate
approval to the final handoff, submit once, retain only sanitized request
ID/status, poll within the configured timeout, and never replay an ambiguous
submission. Execute the approved request in two durable phases. First invoke
the Goal Management adapter `scripts/goal_plan_ess_handoff.py` with the approved
`--payload-file`, `--environment` (REST host), stable project-local `--run-dir`,
and `--approved` after all existing readiness and approval gates pass. The
adapter owns recovery records and calls the unchanged Core submitter with
`--submit-only --retries 0` and a separate submission-result `--output`.
Core does not support a `--submission-checkpoint` argument. Retain
and poll the same local command session until it exits when the execution tool
reports that the process is still running or returns no incremental output;
that state is not a missing ESS result. Require the checkpoint to contain the
accepted request ID and the approved payload digest before starting phase two.
Then invoke Core with only `--request-id <captured-id>` and a bounded polling
window, writing the terminal or timeout result to a separate execution-result
artifact. The adapter saves the environment and effective payload digest before
starting Core, excludes concurrent attempts with a local lock, and checkpoints
the accepted request ID from Core's saved result. On continuation, reuse the
same run directory: recover from a valid saved submission result if checkpoint
finalization was interrupted; otherwise an attempted submission without a
recoverable request ID is `UNKNOWN_AFTER_SUBMISSION`. Never create another run
directory or repeat phase one to recover it. `--retries 0` is an ESS request
setting, not a local deduplication mechanism. One approval covers the exact submission and its read-only
monitoring. A timeout leaves the task pending with its request ID. Mark the
Goal Plan operation and dependent Run Book task complete only after a persisted
terminal-success result and fresh assignment reconciliation for the approved
plan, environment and population. Call `verify_assignment_outcome` with the
normalized core read evidence. A SUCCEEDED job alone is `verification_pending`,
not business-result completion. Proven scope errors or processing failures require a
diagnostic and review, never automatic resubmission or deletion. Likewise, do
not claim the overall Run Book is closed solely from completed child tasks when
the owning workflow's current overall status is unavailable.

Redact access tokens, refresh tokens, authorization headers, client secrets,
credentials, and token-cache contents from previews, diagnostics, execution
results, and audit artifacts. Persist only the approved business payload,
sanitized target-environment identity, ESS request ID, job definition, polling
status, and error details that contain no secrets.

Assignment reruns are additive: they assign newly included goals to selected
workers and existing included goals to newly selected workers, but do not
change already assigned goals. Excluding a worker later does not remove goals
assigned by an earlier run; removal is a separate, explicitly approved action.

## Outcomes

Return exactly one of `READ`, `CREATED_INACTIVE`, `UPDATED`, `ACTIVATED`,
`INACTIVATED`, `POPULATION_SAVED`, `ASSIGNMENT_READY`,
`ASSIGNMENT_SUBMITTED`, `ASSIGNMENT_PENDING`, `ASSIGNMENT_VERIFIED`, `CSV_READY`, `NO_CHANGE`,
`MISSING`, `PROVIDER_SKILL_UNAVAILABLE`, `BLOCKED`, `FAILED`, or
`UNKNOWN_AFTER_SUBMISSION`.

## Business duplicate comparison

Before any HDL or standard create, follow [the shared duplicate identity contract](../../goal-management-common/duplicate-identity.md). Use its executable helper for candidate comparison and incoming-row checks. A name search returns candidates; an exact Goal Plan name is a duplicate only when its associated Review Period also matches.
