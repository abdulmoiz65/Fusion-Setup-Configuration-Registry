# Requested Feedback Template Runbook Readiness

Use this resource after source extraction and before project workspace or Run
Book creation.

## Confirmation summary

The readiness summary must include:

| Section | Required content |
|---|---|
| Source coverage | Files/folders read, partial reads, unreadable inputs, and reference-only sources |
| Identified tasks | Requested Feedback Template tasks, source references, match status, and owning skill route |
| Data-change candidates | Proposed create/update/inactivate or unsupported delete/import intent and affected object |
| Reference-only dependencies | Dependencies needed for validation but not direct changes |
| Blockers, decisions, and validation gates | Real intake blockers, pending agent-owned target validations, conflicting source values, destructive choices, ambiguous route |
| Proposed sequence | Evaluate both mandatory Request Feedback SITE profiles first; add one leading Manage Administrator Profile Values task unless both are verified as `Y`; then classify template type, resolve or create the supported questionnaire, configure Feedback Templates, and verify each approved change |
| Approval model | Run Book creation approval first; each later data change still needs its own preview and approval |

Ask the user to confirm before creating or refreshing project/runbook planning
artifacts. Creating a local task mapping is not approval to execute Fusion
changes. Do not ask the consultant to supply tenant evidence as an intake
blocker when a source value is present and the active workflow can validate it;
instead, present the validation in the runbook and run declared read-only
validation without consultant approval. Obtain approval immediately before a
state-changing external step only.

## Runbook-ready mapping

`identified-task-mapping.json` must:

- contain a non-empty `tasks` array;
- preserve one row per identified executable or validation task;
- include source task name, offering, functional area, source reference, match
  rationale, phase when known, and data paths when relevant;
- evaluate `HRA_REQUEST_FEEDBACK_ENABLED` and
  `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED` for every mapping, independent of
  whether the supplied source names them;
- when both exact SITE values are verified as `Y`, record verified no-change
  and omit the profile task;
- when either value is non-`Y`, absent, or not yet verifiable, add exactly one
  first row for `Manage Administrator Profile Values`
  (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`) under offering `Performance
  Management` and functional area `Performance Management Common`; put both profile codes, current
  evidence, and desired value `Y` in its task notes and do not add duplicate
  setup-task rows;
- keep Feedback Templates separate from questionnaire lifecycle, runtime
  feedback, participant feedback, and other Performance Management setup;
- add `HRT_MANAGE_QUESTIONNAIRES` before `ORA_HRA_FEEDBACK_TEMPLATES` only for a supported General Feedback custom-creation request, and carry a generic questionnaire dependency specification rather than example-specific logic;
- for Performance Goal Feedback, resolve the seeded `PERF_GOAL_QSTNR_V1` questionnaire; record custom creation/replacement as unsupported with no executable questionnaire task;
- mark reference-only dependencies as dependency or validation tasks, not as
  object mutations;
- avoid invented catalog task names.

The project initializer performs exact-name catalog validation. If an extracted
task cannot be exact-name matched, return a blocker or ask for user correction
before Run Book creation.

## Execution sequence guidance

Use this default sequence unless the supplied source or tenant dependency graph
requires a different order:

1. Confirm scope and source coverage.
2. Read configured project/environment sources before declaring the target
   environment missing.
3. Read the exact definitions and SITE values for
   `HRA_REQUEST_FEEDBACK_ENABLED` and
   `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED` through the declared profile provider.
   Omit the profile task only when both values are verified as `Y`; otherwise
   place one `Manage Administrator Profile Values` task first.
4. Present the configuration plan and runbook with validation steps for the
   mandatory profiles, questionnaire resolution, LOV checks, REST route evidence,
   immutable previews, and verification.
5. Run declared read-only validation and verification automatically. Ask for
   approval immediately before a create, update, activation, or other
   state-changing external action.
6. At execution, re-read both mandatory profiles. Send no write for a verified
   `Y`; for each remaining profile, use its separately approved exact SITE POST
   or PATCH to `Y` and verify readback. Do not continue a dependent external
   mutation until both profiles are verified as `Y`.
7. For a supported General Feedback new-questionnaire request, hand the generic specification to
   `hcm.hcm-tool.questionnaire.questionnaires`, complete its independently
   approved Data Loader flow, and verify exact active/latest target readback.
   For Performance Goal Feedback, perform only seeded questionnaire lookup and
   verification; missing seed data blocks the dependent template setup.
8. Resolve remaining prerequisites: questionnaire provider evidence, security,
   notifications, goal-feedback activation impact, and relevant Performance
   Management dependencies.
9. Prepare or validate Feedback Templates setup.
10. Route General and Performance Goal Feedback Templates through the task-declared
   REST contract only. Reject template FSM/CSV import/export and HDL/HSDL.
   Record the external catalog discrepancy; stop an incompatible loader handoff.
11. Preview each state-changing operation and require approval before execution.
12. Verify target-tenant state after each approved execution step.

## Existing unsupported replacement tasks

Propose **Not Applicable — seeded questionnaire required** for an existing
task asking to replace a Performance Goal Feedback template's questionnaire
with a custom questionnaire. Explain: "This replacement cannot be performed.
Performance Goal Feedback templates require the seeded Performance Goal
Feedback questionnaire (PERF_GOAL_QSTNR_V1)." If current readback already shows
the seed, record that no association change is needed and preserve the other
template fields. Do not mark the requested custom replacement completed or
leave it as retryable pending implementation. Keep already-created custom
questionnaires intact; deletion is outside this correction. Applying a live
runbook status/comment uses the authorized core.runbook operation separately.

## Approval boundaries

| Action | Approval needed before action? | Owner |
|---|---:|---|
| Read local input files | No | Intake flow in this functional-area skill |
| Create source inventory and readiness summary | No | Intake flow in this functional-area skill |
| Declared read-only target-tenant validation or verification (GET) | No | Active task skill/provider |
| Create or refresh local project/runbook planning artifacts | Yes, after summary | Project workspace initializer |
| Create Fusion Run Book | Yes | `core.runbook` |
| Mandatory Request Feedback profile SITE POST/PATCH | Yes, for each exact preview | `core.fusion-api.apps-common.profile-options` |
| Feedback Template POST/PATCH | Yes, after immutable REST preview | Feedback Templates task via REST client |
| Questionnaire lifecycle mutation | Yes, after provider preview | Owning questionnaire provider |
| Destructive delete or replacement | Separate explicit approval | Owning task skill |

## Stop conditions

Stop before Run Book creation when:

- the supplied source files cannot be read sufficiently to identify tasks;
- task mapping would omit known source coverage;
- the offering or functional area remains ambiguous;
- a task name cannot be exact-name matched and no safe manual route is
  acceptable;
- a required source value is missing or conflicts with another source value;
- ambiguous destructive intent appears in the source and cannot be separated
  into a non-destructive plan;
- configured target environment discovery has been checked and no target can be
  identified;
- the user has not confirmed the proposed task set.

Do not stop before Run Book creation solely because questionnaire readiness,
manager-type LOV resolution, profile current value, profile updatability,
target-tenant read evidence, route supportability, immutable
REST preview, or optional project renaming is still pending. These are
runbook validation or approval gates unless the validation has already failed
or no authorized workflow can perform it.

Stop before execution when:

- target-tenant evidence is missing or stale;
- source data changed after preview;
- validation has error-level issues;
- approval is stale, conditional, ambiguous, or applies to a different task;
- destructive intent is implied but not explicitly approved.
