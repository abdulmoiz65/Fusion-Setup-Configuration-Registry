# Touchpoints implementation workflow

Apply [the deterministic orchestration contract](deterministic-orchestration.md)
for complete task planning, owner task types, context synchronization and
checkpoint classification. Its executable stages replace ad hoc context repair.

## Scope selection before planning

Classify the complete user objective semantically before invoking either planner.
The word Touchpoints alone is not a full-implementation trigger. Persist `scope`
with `mode`, `selected_tasks` (selected mode only), and `source_reference` to the
actual request. Allowed modes are `implementation` and `selected_tasks`.

| Request | Scope / route |
|---|---|
| Enable, configure, or implement Touchpoints generally | implementation; all eight rows |
| Configure Touchpoints Check-Ins, even as the first message | selected_tasks: checkins; existing Performance Management Check-In Templates skill |
| Request Feedback Template | selected_tasks: feedback; existing Requested Feedback parent skill |
| Update a specified profile | selected_tasks: profiles; existing profile provider |
| Submit aggregation, or submit aggregation and update a profile | selected_tasks: full, or profiles and full; standalone ESS route |
| Configure surveys or nudges | selected_tasks: surveys or nudges; UI guidance and customer confirmation |
| Schedule daily Incremental | selected_tasks: daily; verified same-context Full success required, no automatic Full submission |

`full` remains the stable aggregation key for compatibility; in selected mode its
label is Aggregate Oracle Touchpoints Data and the owning ESS skill resolves the
requested Full/Incremental mode for a standalone one-off run. When both full
and daily are selected, full must use Full mode and verified success unlocks the
following daily row. Never infer daily scheduling from one-time ESS.
Owning tasks retain mandatory profile, questionnaire, import and approval checks.
Only actual unmet prerequisites may add owner-managed predecessor work; never
add the unrelated Touchpoints baseline for a specific-task request.

For an approved plan persist `approved_scope` as `{mode, selected_tasks}` from
the planner result. A focused follow-up retains this scope and existing bindings.
An explicit scope amendment requires showing its delta, recording the user's
decision, updating approved_scope and advancing the configuration revision.
Do not silently relabel implementation ESS as standalone to evade its gates.
Legacy state without scope requires classification from its original objective
and subsequent explicit scope decisions; eight existing rows are not proof of intent.

Use optional `session: {overview_shown: true}` only after delivering the generic
overview in this session. The planner emits `publish_overview` for implementation
only; this flag is presentation guidance, never authorization to create tasks.
Start that flag anew for a genuinely new session; do not reset project scope.
Informational questions can show guidance without provisioning a Run Book.

When the user discards a run, persist `run_status: abandoned`, the user decision
and timestamp. The planner rejects that state. Preserve artifacts and remote
history; do not mark unfinished work completed or delete Fusion tasks. A fresh
prompt starts a new project/binding and fresh approvals; never reuse the abandoned
project merely because the core Data Loader runID still references it.

## Scope and ownership

This is the Touchpoints orchestration contract. Reuse the existing profile and
aggregation tasks; do not change shared Run Book code, generated catalogs, or
Performance Management skills. The configuration plan lists the complete scope.
Resolve all selected catalog-backed owner tasks for initial creation, even while
business inputs remain pending. Apply the scoped owner task-type adapter before
creation, and add uncatalogued tracking rows through the existing manual operation.
Run Book order and comments communicate gates; this skill enforces them before
its own external operations. Do not claim that the Fusion UI enforces these gates.

The source is the approved PM requirement and customer-disposition clarification
in this change. Daily frequency is that requirement, not a universal Oracle
default. Oracle's [Touchpoints scheduled-process guidance](https://docs.oracle.com/en/cloud/saas/talent-management/fatau/configure-and-run-scheduled-processes.html)
supports initial Full processing and later Incremental processing.

## Configuration plan

### Executable entry point (required)

Run `scripts/touchpoints_runbook.py --input <state.json> --tasks <snapshot.json>
--dry-run` from the parent skill folder. Persist its full JSON output; never
replace it with a handwritten action list. It wraps the evidence evaluator and
emits the selected rows, missing manual-task inputs and binding/status diagnostics.
It performs no network operations. Delegate every approved action to core.runbook.

For a new project, first run without `--tasks` to generate the selected rows (provisioning
is blocked as expected), then use the canonical initializer with catalog-resolved
supported tasks. Return the initial dashboard, bind those tasks and continue this
entry point. An ESS-only payload is complete only for an explicitly ESS-only scope; it is
incomplete for a full implementation.

Before initial creation, display all selected rows in their intended execution
order, including owner prerequisites and explicit Not Applicable dispositions.
Explain which rows are initially mapped and which are added afterwards. On
creation success, deliver core's complete dashboard unchanged and accompany it
with `Partial provisioning` and the missing-row count. An active Run Book is not
a fully provisioned or execution-ready Run Book. Continue authorized read-only
planning in the same turn after delivering the dashboard; do not end with only
a promise to perform the next available step. If blocked, state the exact gate
and whether work has stopped. Preserve already granted, still-applicable approvals.

State adds `runbook: {status: "active", journey_id: "...", bindings: {...}}`.
Optional `task_requirements` maps those same eight keys to sanitized requested
values and next actions; these are preserved in each generated plan row. Keep
the requested profile code/value and ESS mode in this state rather than a second
independent plan. Do not place credentials or sensitive values in this metadata.
Bindings use the eight stable keys; each contains string `parent_id`, `task_id`
and exact returned `name`. Resolve scope/identity explicitly, not by fuzzy names.
Snapshot fields are the same three context fields as state, `journey_id`, ISO
`captured_at`, `complete: true`, and `items`. Obtain all pages using core.runbook
`list-tasks` and retain only `ParentWorkerJourneyId`, `WorkerJourneyTaskId`,
`Name`, `Status`, `Sequence` in items. Complete means all pages were retrieved;
never set it after a partial read. Refresh this snapshot in the current operation
before a readiness handoff; its timestamp is audit evidence, not a freshness lease.

Use `manual_additions[].input` for each named add-task operation after core's
authorization. Optional sequence/notes/flags must be supplied or approved by the
user; do not infer API permissions from proposed configuration-plan metadata.
The planner now includes explicit `sequence` values in addition inputs and
`proposed_sequence` in rows once a complete snapshot is available. These are
proposals for review, not approval. It preserves existing positions when space
allows and avoids positions occupied by unrelated tasks. If gaps are insufficient
or bound rows are out of order, `sequence_updates` proposes exact bound-task
PATCH inputs and additions are withheld. Present those repairs with current and
proposed positions, dispatch only authorized repairs through core.runbook, then
refresh and regenerate before adding tasks. Do not strip the explicit sequence
from an approved addition: core otherwise appends it after the highest sequence.
Incomplete snapshots, ambiguous bindings and uncertain writes suppress both
addition and repair proposals. `presentation_status` distinguishes partial from
complete provisioning; it does not establish configuration readiness.
Persist `pending_operation` with key, operation and approval reference BEFORE
dispatch. Persist the returned binding immediately after confirmed success, then
clear pending_operation. If dispatch or persistence is uncertain, leave it set,
stop the batch and reconcile read-only. Never re-add a bound task missing from a
snapshot or a same-name task with missing binding without identity reconciliation.
After the batch, refresh tasks and regenerate the plan. Only `runbook_complete:
true` allows reporting provisioning complete; dependency readiness is separate.

Run again with `--require-ready full` or `--require-ready daily` before the owning
ESS preview and immediately before dispatch. Exit 2 blocks the handoff, including
when configuration is confirmed but rows are missing or statuses disagree.
These checks enforce the Touchpoints path; they do not intercept unrelated direct
core invocations or enforce dependencies inside the Fusion UI.

For full implementation, show these rows even when the original source omits
the configuration dependency. For selected-task requests, emit only selected rows.
Include owner, disposition, execution route, blocker/next action, and evidence
basis. Use the same stable local keys in the durable workflow state and task
bindings; they are not Fusion task/action codes.

| Key | Task label | Owner and route | Dependency |
|---|---|---|---|
| profiles | Touchpoints Profile Options | Existing Touchpoints profile provider | Requested values and levels resolved |
| checkins | Check-In Templates | Performance Management; Touchpoints template type | Business inputs if configuration is needed |
| feedback | Request Feedback Template | Performance Management Requested Feedback workflow | Its own profile/questionnaire prerequisites if configuration is needed |
| surveys | Pulse Surveys | User performs creation and assignment in UI | Separate customer applicability decision |
| nudges | Nudges | User performs setup in UI | Separate customer applicability decision |
| readiness | Confirm Touchpoints Configuration Readiness | User confirms the displayed configuration revision | All five preceding dependencies resolved |
| full | Aggregate Oracle Touchpoints Data — Full | Existing aggregation task via core ESS | Readiness confirmed and exact Full payload approved |
| daily | Schedule Aggregate Oracle Touchpoints Data — Daily Incremental | Manual Run Book row; nested ESS skill performs scheduling | Verified Full success and separate exact schedule approval |

For feedback mapping retain the canonical name `Feedback Templates`, code
`ORA_HRA_FEEDBACK_TEMPLATES`, functional area `Requested Feedback Template`,
and offering `Performance Management`. `Request Feedback Template` is the
Touchpoints-facing label, not a new catalog identity. Use it directly for an
ad hoc manual row. For an existing mapped row, use the existing `update-task`
taskName operation only with explicit user authorization; preserve its action
code and persisted owner mapping. Never feed the display alias to exact-name
catalog matching. Check-Ins use `ORA_MANAGE_CHECK_IN_TEMPLATES`.

## Dependency decisions

Ask first whether each of Check-Ins, Request Feedback, Surveys and Nudges needs
configuration, is already configured, or is Not Applicable. Reuse explicit
same-target answers already supplied; do not ask again without a scope change.
Ask about surveys and nudges independently. Source silence is not exclusion.

| Disposition | Display / Run Book status | Readiness treatment |
|---|---|---|
| unknown | Awaiting confirmation / open | Unresolved |
| configure | Pending configuration / open or in-progress | Unresolved until outcome evidence exists |
| already_configured | Completed — user confirmed / completed | Resolved by explicit customer attestation |
| completed | Completed — verified / completed | Resolved by owning workflow evidence |
| not_applicable | Not Applicable — user confirmed / not-applicable | Resolved exclusion; never label as configured |

Already-configured confirmations must identify the target and intended scope,
confirming person, timestamp and the user-message/evidence reference. Ask for a
template name only when needed to disambiguate the confirmation or to execute
a requested change. Do not demand configuration fields for accepted existing
setup. A Check-In exclusion is an explicit customer scope exception to the PM's
required baseline and must be recorded as such. Profile options remain governed
by their existing provider: verify current values or perform the approved update;
do not silently waive profile prerequisites using this exception mechanism.

Surveys must cover creation AND assignment. Nudges must cover the selected nudge
scope. UI confirmations are `already_configured`, not system-verified `completed`;
screenshots are optional. Do not browse the UI or invent REST checks to verify
these unsupported tasks. Explain that completion is user-confirmed. A statement
about one feature never resolves the other.

An explicit request to mark a specific task complete or Not Applicable can
authorize the corresponding core Run Book update. A general discussion or
configuration attestation alone is not a PATCH authorization; retain the local
decision and request the exact update through core.runbook. A failure to persist
or synchronize the decision leaves a visible blocker; never claim the remote
task was updated when only local state changed.

## Performance Management handoff

Delegate only `configure` work. Read the owning skill before preparing its data.
Keep the same project, environment and Run Book. Pass the local dependency key,
operation intent (create/update/reuse), supplied requirements, missing business
inputs, source references and the task binding. Preserve its execution route:

- Check-In Templates: use the existing Performance Management task and its
  FSM/Data Loader route. Resolve Touchpoints type. Collect only missing business
  choices for template identity/purpose, workforce population, manager roles,
  topics and optional questionnaires. Disclose documented defaults; technical
  IDs and ordinary LOV resolution belong to the owning skill.
- Request Feedback Template: use the parent Requested Feedback workflow, which
  owns mandatory SITE profile prerequisites and conditional questionnaire tasks.
  New template intake requires name, template type, status, specific manager
  types and questionnaire selection. Templates use their REST-only route, not
  Data Loader. Reuse the parent's restrictions on seeded goal-feedback
  questionnaires and its exact approval/verification gates.

Add any required profile/questionnaire configuration as separate predecessor
tasks using the owning workflow's supported Run Book operations. Do not merge
Touchpoints profiles and Requested Feedback profiles merely because their setup
task names match. Bind each to its scope and owner.

After all selected rows are bound, run `scripts/touchpoints_orchestrator.py
--project-root project/{project_id} --sync-context` before owner handoffs. This
automatically synchronizes every mapped Data Loader/ESS context and every REST
or manual owner handoff from the same ordered plan. Repeat after sequence repair.
The legacy Check-In helper delegates to this complete synchronization contract.

Missing required business input is `Blocked — input needed`, naming the missing
decision, responsible user and dependent task. Continue independent work. The
owning Requested Feedback intake blocks executable creation when required
source values are missing: represent that dependency as a manual requirements
handoff until it is ready; do not bypass its intake gate. Afterwards, execute
through that owning skill and record its verified result on the existing manual
row. A manual row is a tracking item, not authorization to change the owning
skill's transport, mandatory prerequisites or approval rules.

## Existing Run Book operations only

Read `core/runbook/SKILL.md` and its REST reference before each selected operation.

1. Present the complete configuration plan and exact proposed additions/status
   updates. For a new project use the canonical initializer and Run Book creation
   flow for supported mapped tasks. Return its full dashboard before proceeding.
2. Read the existing tasks and bind each local key to exactly one existing task
   using canonical identity, scope and persisted mapping. Reuse the two existing
   profile/ESS tasks. An ambiguous same-name match blocks that item; do not guess.
3. Obtain explicit authorization for each named ad hoc task addition under
   core.runbook. An explicit request naming a fixed list may cover that list;
   planning approval alone does not. Run `add-task` once per missing manual row,
   persist each returned binding immediately, and stop on failure/unknown outcome.
   Do not send manual rows through the canonical plan generator or forge codes.
4. Resolve Check-In catalog identity initially even when business intake is pending.
   For Request Feedback Template, preserve its canonical identity and apply the
   scoped creation-plan adapter to assign manual tracking rather than the shared
   generator's Data Loader default. Execute it through the owning REST workflow.
   On an existing Run Book reuse its verified manual binding and owner handoff.
   Already-configured and excluded dependencies still remain visible as rows.
5. Notes identify the stable local key, owner, scope, evidence basis, missing
   inputs and dependency reason. Supply desired positive sequences only as
   explicitly authorized. Inspect actual existing sequences: place configuration
   and readiness before Full, and daily after Full. If no sequence gap exists,
   propose explicit sequence updates through core.runbook. Never renumber silently.
6. Every completion, exclusion, comment, rename or sequence PATCH uses the
   existing operation-specific authorization. A core status `open` can display
   `Blocked — awaiting Full success` in notes; do not invent a `blocked` API enum.
7. Resume by stored bindings and current task reads. Never replay an uncertain
   add/update POST, recreate a Run Book, duplicate a completed dependency, or
   treat a row's percentage/status as evidence that an ESS job succeeded.

Manual additions occur after initial creation, so report partial provisioning
honestly. Do not claim a complete Run Book until every planned row is bound.

## Readiness, evidence and persistence

Persist `touchpoints-workflow-state.json`, `touchpoints-configuration-plan.json`
and task bindings under the parent skill's declared project artifact directory.
Use project registry/state services, append durable runs and token usage as
required. No customer state belongs in this skill's source folder.

The evaluator input is a JSON object with `project_id`, `environment`,
`configuration_revision` (non-empty strings), and `dependencies` keyed by
profiles/checkins/feedback/surveys/nudges. Each entry has `disposition`, optional
`missing_inputs`, and `evidence`. Evidence for a resolved entry contains the
same three context fields plus `actor`, ISO `recorded_at`, and non-secret
`reference`; exclusions also require `reason`. Verified outcomes additionally
require `verification_reference` from the owning workflow. Bind multiple
templates to one scope only after all in-scope templates are resolved.

`readiness_confirmation` uses the same evidence shape plus `confirmed: true`.
It records approval of configuration readiness, not execution approval.
`full_run` uses the context fields plus `request_id`, `job_definition_id`,
`run_type`, `cause`, `completed_at` and `verification_reference`, derived from
the nested task's approved submission and core ESS tracking evidence. The agent
must inspect those referenced records; the pure local evaluator does not fetch
them or authenticate a user statement. Map completed_at from completedTime and
copy any errorType/errorWarningMessage/errorWarningDetail to error_type,
error_warning_message/error_warning_detail; contradictory diagnostics block
scheduling. Never manufacture or omit adverse evidence to pass the evaluator.

Before Full, require all dependencies resolved, all rows bound/synchronized and
readiness explicitly confirmed for the current revision. Always require fresh
exact ESS preview/approval afterwards. Before daily scheduling, additionally
require Full terminal success for the same project/environment/revision, not
submission, HTTP success, an exit code, percentage, or a user's assertion.
Warnings, errors, missing evidence and unknown outcomes block scheduling.

Changing target, configuration scope, reopening a dependency or modifying setup
advances the configuration revision and invalidates affected attestations,
readiness, Full evidence for scheduling and approvals. Do not cancel an existing
schedule automatically; flag the impact and require a separately supported,
authorized action. Preserve prior evidence as history.

The local evaluator never submits jobs or updates tasks. Its `ready_for_preview`
result is necessary but not sufficient: task provisioning, evidence inspection,
exact preview, approval and the owning execution preflight remain agent-owned
checks. Profile/template owners retain their declared privilege rules; ESS
uses Fusion's execution response without a separate submit-privilege check.
Standalone reads or existing-request tracking do not create tasks or require
configuration intake. Selected-task work never expands into full implementation.

## Failures

Use the repository failure classes: input validation, catalog mismatch,
auth/authz, transport/environment, Fusion API, process timeout, process failed,
artifact persistence and approval blocker. Persist stage, environment, safe
artifact references, request IDs when available, and one next action. Never
automatically retry writes, including manual-task additions. Resume tracking
existing ESS requests read-only through the core provider when authorized.

## ESS handoff and audit ownership

Both Full and daily rows have execution_route ess and the same nested ESS owner.
Daily is a separate manually provisioned tracking row after Full, with its own
exact schedule approval. Owner handoffs identify operation_intent and the scoped
scripts/touchpoints_ess_handoff.py coordination module. That module delegates
technical submission/read/wait to the existing core functions; source edits stay
inside Touchpoints. Use the nested daily-schedule contract for immutable envelope
validation, exact target checks, read fields and identity checkpoints. ESS
authorization is enforced by Fusion during submission and monitoring, without
a separate submit-privilege probe or evidence field.

Retain the request-ID journal before monitoring. A monitoring/authentication or
audit failure cannot authorize another POST. Keep pending/uncertain-operation
state until core-only read reconciliation resolves it; the helper journal is
additional audit evidence, not a replacement for project run records, token usage,
artifact registry, approvals or authorized core.runbook updates.

After inspecting a verified schedule result, persist it as daily_schedule in the
workflow state. Its context, request_id, job_definition_id, Incremental run_type,
RECUR_PARENT request_type, full_request_id, schedule_verified, errors_present,
verified_at, approval_reference and verification_reference must agree with the
current Full evidence and approved schedule. Missing or stale evidence leaves
daily unresolved. Schedule completion covers configuration only; future runs
still require their own tracking evidence. Completed Full/daily checkpoints are
recognized in selected-task scope, so resuming cannot select them for creation.
