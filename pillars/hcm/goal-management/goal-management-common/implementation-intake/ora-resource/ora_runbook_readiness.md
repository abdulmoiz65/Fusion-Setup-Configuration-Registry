# Goal Management Runbook Readiness

Use this resource after source extraction and before project workspace or Run
Book creation.

## Confirmation summary

The readiness summary must include:

| Section | Required content |
|---|---|
| Source coverage | Files/folders read, partial reads, unreadable inputs, and reference-only sources |
| Identified tasks | Goal Management tasks, source references, match status, and owning skill route |
| Data-change candidates | Proposed create/update/delete/inactivate/assign/load intent and affected object |
| Reference-only dependencies | Dependencies needed for validation but not direct changes |
| Blockers and decisions | Missing tenant evidence, conflicting source values, destructive choices, ambiguous route |
| Proposed sequence | Readiness tasks first, object setup next, data loads through Data Loader, verification last |
| Approval model | Run Book creation approval first; each later data change still needs its own preview and approval |

Proposed Library Goal Names belong in this confirmation summary. The consultant
may accept them, edit them, and add optional details in one response. Only
confirmed names flow into a later configuration preview.

When an existing project workspace is in scope, organize multiple annual
cycles as distinct, cycle-named planning artifacts within that workspace. Do
not require a new workspace because a source names a different Review Period
year, and do not overwrite another cycle's current runbook or plan.

For an initial regular Goal Plan create, list population, plan-goal maintenance,
and assignment as separate follow-on operations unless the source explicitly
includes them. An absent complete Goal Plan date pair is not a planning
blocker: note that the later preview may derive both dates from its resolved
Review Period. A named workforce-restriction attribute and value on a Library
Goal are planning evidence; defer exact target-tenant LOV resolution to the
approved preview. If the source supplies a value without an unambiguous
supported attribute, record field confirmation as a planning decision.

Present the review summary in chat before referring the user to generated
artifacts or asking for confirmation. Ask only source-grounded business
decisions; file paths are supporting references. Do not ask for an environment
at this stage when project or Run Book context already configures one, and do
not ask for it at all until an approved external operation needs it. Creating a
local task mapping is not approval to execute Fusion changes.

## Planning-artifact preview and recommendation

When a configuration plan and local runbook have both been prepared or
refreshed, present them together in the same user-facing response. State that
both artifacts are local planning material, then show the configuration delta
and a readable, numbered runbook preview before any execution discussion.
The runbook preview must name the owner route, activity, preflight/approval
gate, and exit criterion for each planned step. It must also distinguish the
local runbook from an Oracle Fusion Run Book.

Close that response with one recommended next action that asks the consultant
to review the preview or request an immutable preview for one named first
step. Do not ask for execution approval in the same response, and do not treat
artifact preparation as authorization for Fusion changes or Fusion Run Book
creation.

This control applies to the exact task set resolved from the current input,
whether it contains one task, two tasks, or any larger positive number. Do not
insert absent example tasks, require the common five-task annual-cycle shape,
or renumber a smaller task list to resemble it.

## Runbook-ready mapping

`identified-task-mapping.json` must:

- contain a non-empty `tasks` array;
- preserve one row per identified executable or validation task;
- include source task name, offering, functional area, source reference, match
  rationale, phase when known, and data paths when relevant;
- keep Performance Library Goal and Development Library Goal as separate rows
  when both are present;
- mark reference-only dependencies as dependency or validation tasks, not as
  object mutations;
- avoid invented catalog task names.

The project initializer performs exact-name catalog validation. If an extracted
task cannot be exact-name matched, return a blocker or ask for user correction
before Run Book creation.

For Goal Management, generate a core-compatible task-context document using
`goal-management-common/implementation-intake/scripts/resolve_goal_management_task_context.py` after
the mapping is confirmed. The document must preserve each row's offering,
functional area, task code, sequence, and exact `skill_path`. A `Goal Library`
row without exactly `Performance Library Goals` or `Development Library Goals`
as its functional area is a blocker; do not use a generic task-name fallback.

Before common Run Book handoff, the Goal Management intake must persist its
exact product task context, then invoke the shared offering task-map builder
and task-dependency resolver. Every selected route must match one Goal
Management manifest by task code, task name, offering, and functional area.
Use the shared resolver's persisted `setup_task_sequence`, dependency
provenance, sequence source, and diagnostics for downstream planning. Do not
create Goal Management-local execution groups or sequence defaults. Ambiguous
routes, unresolved sequence, and unresolved date-confirmation findings block
only their affected executable actions.

Reconcile the exact task context with that persisted sequence before rendering.
Pass the reconciled context separately using the preview renderer's required
`--resolved-context` argument; do not reconstruct it from the proposed preview.
The renderer rejects task identity, route, sequence and operation drift. Use the
same reconciled context for the downstream core handoff. Do not renumber the
remaining tasks when presenting a continuation. A changed sequence or operation
requires a regenerated preview and invalidates approval of the previous plan.
The renderer validates this handoff; it does not replace the shared resolver or
establish provenance for a caller-fabricated context.

After the required Core project Run Book refresh has written
`setup-task-plan.json`, `task-context.json`, and `runbook-plan.json`, and before
binding a plan checksum or requesting Run Book creation, run
`scripts/reconcile_goal_management_runbook.py --project-root project/{project_id} --apply`.
This Goal Management-owned local handoff recomputes exact routes from
the confirmed mapping and checks each generated task's code, name, offering,
functional area, sequence, candidate evidence, and business objects. It
reconciles the three artifacts together, persists the exact context and an
audit, updates the project artifact index, and makes no Oracle request. A rerun
of Core's refresh requires a new
reconciliation. The local plan is not ready while either step is incomplete.

The handoff may replace a `LEXICOGRAPHIC_PATH` selection only when the current
candidate evidence contains one unique manifest matching all four task
identity fields. Missing, ambiguous, non-lexical conflicting, reordered, or
otherwise inconsistent results remain blockers. Never create or submit the
Oracle Fusion Run Book from an unreconciled plan. Preserve the last exact local
review plan and record any unreconciled mismatch as a planning diagnostic.

For a semantic Profile Options request, persist the profile-resolution report
with the mapping. The review package must show profile code, owning product,
level, value meaning, stored value, and provenance for each resolved fact.
Declared defaults must be visible. A non-unique code, ownership, value, or
non-defaultable required level requires one focused consultant question;
target-tenant profile metadata verification is instead an execution preflight.
Map definition-only reads to `FND_MANAGE_PROFILE_OPTIONS`. Map a resolved
profile-value create or update to `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES` and
use the standard Apps Common profile-options provider; never substitute the
definition task for value maintenance.

## Execution sequence guidance

Use this recommended sequence as dependency guidance. Preserve a supplied
source order as traceability, but derive executable order through the shared
implementation-planning services:

1. Confirm scope and source coverage. Reuse configured environment context when
   an approved external operation reaches its preflight; do not solicit it
   during design review.
2. Resolve only source-requested prerequisites and prerequisites required by a
   selected object field: offering/features, security, profile options,
   lookups, value sets, flexfields, notifications, approvals, TDS/VBS, and
   Performance Management dependencies. Record absent approval/notification
   requirements as not in scope.
3. Prepare or validate Performance Library Goals.
4. Prepare or validate Development Library Goals and target outcomes.
5. Prepare or validate Review Period setup.
6. Prepare or validate Goal Plan setup. A regular Goal Plan requires an active
   Review Period before preview.
7. Keep REST as the normal-volume default. For Goal Plan or Library Goal,
   select HDL when explicitly requested or when at least 25 root rows are
   resolved. Use object-specific preflight for a supplied DAT/ZIP; otherwise
   select `hdl_generate`, validate the business rows, and have
   `core.data-loader` generate the current-metadata source and immutable ZIP.
   Review Period remains REST-only. Resolve environment, caller, safe defaults,
   target evidence, timestamps, operation classification, and audit manifest
   internally before immutable preview.
8. Preview each state-changing operation and require approval before execution.
9. Verify target-tenant state after each approved execution step.

## Approval boundaries

| Action | Approval needed before action? | Owner |
|---|---:|---|
| Read local input files | No | Intake skill |
| Create source inventory and readiness summary | No | Intake skill |
| Create or refresh local project/runbook planning artifacts | No; these are local read-only planning artifacts | Project workspace initializer |
| Create Fusion Run Book | Yes | `core.runbook` |
| Upload or initiate HDL/Data Loader archive | Yes, only after DAT/ZIP plus explicit HDL intent, error-free task preflight, and immutable preview | `core.data-loader` |
| REST-backed setup create/update/delete | Yes, after object preview | Owning task skill |
| Destructive delete or replacement | Separate explicit approval | Owning task skill |

## Catalog tasks and nested operations

The local Run Book must contain one row for each exact catalog setup task, not
one row per API call or business operation. For the common annual-cycle source
pack this normally means the source-requested subset of Manage Administrator
Profile Values, Performance Goal Library, Development Goal Library, Review
Periods, and Goal Plans. Keep the exact catalog name, code, offering,
functional area, stable task identity, and owner route on every row.

Store the task's ordered creates, updates, activation, population association,
plan-to-library-goal association, ESS submission, verification, and conditional
Run Book completion as nested `operations`. A metadata lookup, field resolver,
duplicate check, or target-tenant read is preflight and must not become a Run
Book task. Reject duplicate stable task identities rather than allowing the
same catalog task to appear multiple times with one operation per row.

## Queue continuation

For a confirmed source-pack queue, complete applicable read-only task detail,
metadata, lookup, duplicate, and current-state checks without pausing at those
intermediate results. Present the next immutable write preview automatically.
Every external state change remains approval-gated.

Before the first mutation and before every transition to another task, call
`resolve_controlled_next_task` with the complete resolved task list, current
statuses, approved configuration-plan fingerprint, Run Book creation evidence,
and proof that the returned dashboard was presented. Only the earliest
unfinished applicable task may continue. A task-specific approval cannot
override an earlier unfinished task. Draft, changed, stale, duplicate,
ambiguous, or dashboard-missing state blocks before payload preparation.

After approval of an unchanged preview, retain control through submission,
terminal monitoring, fresh verification, and any Run Book update included in
the preview, then present the next task preview. Approval is a temporary gate,
not task completion. Stop for a changed target or payload, unresolved business
input, terminal failure, timeout, verification failure, unsupported route, or
an explicit consultant stop. Do not retry an uncertain mutation automatically.

Group operations under one approval only when the complete ordered plan is
fully resolved and the preview shows every environment, target, payload or
immutable artifact, verification, and conditional Run Book update. When a
later operation depends on state generated by an earlier write, verify the
earlier result and issue a new preview unless the owning task declares a safe
stable-key batch contract.

An approval group is not an API batch. Resolve transport separately for every
operation. If current metadata supports item PATCH but not an ADF batch, one
approval may cover the displayed ordered PATCH requests. If any transport is
unresolved, block the whole group before execution.

## Stop conditions

Stop before Run Book creation when:

- the supplied source files cannot be read sufficiently to identify tasks;
- task mapping would omit known source coverage;
- the offering or functional area remains ambiguous;
- a task name cannot be exact-name matched and no safe manual route is
  acceptable;
- a prompt-versus-source cycle identity conflict remains unresolved;
- the user has not approved the exact Oracle Fusion Run Book creation preview.

Stop before execution when:

- target-tenant evidence is missing or stale;
- source data changed after preview;
- validation has error-level issues;
- approval is stale, conditional, ambiguous, or applies to a different task;
- destructive intent is implied but not explicitly approved.
