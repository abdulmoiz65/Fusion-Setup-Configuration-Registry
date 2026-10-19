---
skill_id: "common.security-console.user-security-common"
name: "User Security Common Manual Tasks"
description: "Classifies common Oracle Fusion Security Console and Functional Setup Manager tasks by execution type, provides manual completion guidance, and routes approved ESS tasks, including LDAP synchronization processes, to the shared ESS Job Submitter."
layer: "pillar"
pillar: "Common"
required_setup_tasks:
  - "ORA_FND_SET_CSM_TARGET_SECURITY"
  - "ATK_MANAGE_HELP_SECURITY_GROUPS"
  - "ORA_ASE_MANAGE_SECURITY_PREFERENCES"
  - "PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS"
  - "ORA_ASE_IMPORT_USERS_AND_ROLES"
  - "ORA_ASE_IMPORT_USER_LOGIN_HISTORY"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "FSCR Security team"
version: "0.1.19"
inputs:
  - "implementation_objective"
  - "project_context"
  - "ess_delegation_contract"
outputs:
  - "task_execution_classification"
  - "manual_completion_guidance"
  - "completion_evidence_checklist"
  - "ess_job_submission_plan"
  - "ess_job_execution_result"
  - "ess_job_diagnostics"
  - "ess_job_audit_summary"
  - "execution_audit"
depends_on:
  - "common.security-console.manage-job-roles"
  - "common.security-console.manage-duties"
  - "common.security-console.manage-data-security-policies"
  - "common.security-console.manage-hcm-role-provisioning-rules"
  - "common.security-console.manage-hcm-ldap-user-account-options"
  - "schemas/ess-delegation-contract.schema.json"
  - "knowledge/setup-task-catalog/effective/setupTasksAll.json"
uses_core:
  - "core.fusion-api.ess-job-submitter"
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
  - "validation_results"
  - "reports"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/common/security-console/user-security-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Writes an ESS job plan and execution audit to the active project workspace when project context is supplied."
  - "Submits or monitors a Fusion ESS request only after explicit user approval and through core.fusion-api.ess-job-submitter."
required_privileges:
  - "Fusion privileges appropriate to submit and monitor the approved ESS job"
---

# User Security Common Manual Tasks

## Purpose

Classify the currently loaded common user-security FSM tasks, direct the
implementor to complete Manual tasks in the Oracle Fusion application, and
route approved ESS tasks to the shared ESS job capability.

## Cross-Pillar Catalog Scope

This is a multi-task Common skill used by all pillars. It intentionally has no
singular `task_code`. The manifest lists its six catalog-backed IDs in
`required_setup_tasks`; the linked flat task metadata below pairs each ID with
its exact name and delegates to this skill. The existing runbook resolver can
discover these files without changes outside Security Console. The **Current
Task Classification** table defines their manual and ESS execution boundaries.
The two named LDAP processes have no verified FSM code in the effective catalog;
their ESS routes remain available by explicit process request.

## Setup Tasks

- [Manage Configuration Set Migration Target Security Policy](manage-configuration-set-migration-target-security-policy.md) (`ORA_FND_SET_CSM_TARGET_SECURITY`)
- [Manage Help Security Groups](manage-help-security-groups.md) (`ATK_MANAGE_HELP_SECURITY_GROUPS`)
- [Manage Applications Security Preferences](manage-applications-security-preferences.md) (`ORA_ASE_MANAGE_SECURITY_PREFERENCES`)
- [Run User and Roles Synchronization Process](run-user-and-roles-synchronization-process.md) (`PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS`)
- [Import Users and Roles into Application Security](import-users-and-roles-into-application-security.md) (`ORA_ASE_IMPORT_USERS_AND_ROLES`)
- [Import User Login History](import-user-login-history.md) (`ORA_ASE_IMPORT_USER_LOGIN_HISTORY`)
- [Retrieve Latest LDAP Changes](retrieve-latest-ldap-changes.md) — FSM task ID unverified.
- [Send Pending LDAP Requests](send-pending-ldap-requests.md) — FSM task ID unverified.

## Dedicated setup-object changes

For create, update, delete or redesign requests concerning roles, duties,
data-security policies, HCM provisioning rules or LDAP account options,
route through `common.security-console` to that object's focused FSM skill
before applying the Manual/ESS classification below. Do not return an
unconfigured-execution blocker for a change owned by a configured focused skill.
Use [FSM input preparation](../references/fsm-input-preparation.md) when the user cannot
identify, extract or populate the input. This handoff does not authorize an
unsupported delete action or bypass Data Loader approval.

## Canonical ESS Delegation Contract

Validate `schemas/ess-delegation-contract.schema.json` version `1.0` before
processing an ESS request. Pillars send `classification_request` with task
identity, environment, overrides, and polling options; they cannot supply a
job contract or approval. This skill owns classification, configured job
defaults, payload construction, preview, and the approval gate. It emits an
`approved_submission` only after explicit approval, with the normalized
`job_contract`, exact `request_payload`, and approval payload hash. Invoke
`core.fusion-api.ess-job-submitter` only with that approved envelope.

## Execution Boundary

For a task classified as `Manual`, state that it must be completed in the
Oracle Fusion application. Do not call Fusion REST APIs, use FBDI or HDL,
submit an ESS job, run CSV import or export, or change Fusion configuration.

For a task classified as `ESS`, use `core.fusion-api.ess-job-submitter` only
after the user provides the target environment, the exact Oracle
`jobDefinitionId` and request parameters or an applicable configured default,
and explicit approval to submit. Do not derive an ESS job definition or
parameters from an FSM task code.

Do not infer an `ESS` or other execution type from catalog CSV or export/import
flags. Those flags describe catalog support, not an approved FSCR execution
classification.

## Current Task Classification

| Execution type | Task | Task code | Catalog CSV/export-import support | Instruction |
| --- | --- | --- | --- | --- |
| Manual | Manage Configuration Set Migration Target Security Policy | `ORA_FND_SET_CSM_TARGET_SECURITY` | No / No | Complete the task in the Oracle Fusion application. |
| Manual | Manage Help Security Groups | `ATK_MANAGE_HELP_SECURITY_GROUPS` | Yes / Yes | Complete the task in the Oracle Fusion application; this skill does not authorize CSV processing. |
| Manual | Manage Applications Security Preferences | `ORA_ASE_MANAGE_SECURITY_PREFERENCES` | Yes / Yes | Complete the task in the Oracle Fusion application; this skill does not authorize CSV processing. |
| ESS | Run User and Roles Synchronization Process | `PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS` | No / No | Use the configured default contract below unless the user supplies an override; validate parameters and obtain approval before submission. |
| ESS | Import Users and Roles into Application Security | `ORA_ASE_IMPORT_USERS_AND_ROLES` | No / No | Use the configured default contract below unless the user supplies an override; validate parameters and obtain approval before submission. |
| ESS | Import User Login History | `ORA_ASE_IMPORT_USER_LOGIN_HISTORY` | No / No | Use the configured default contract below unless the user supplies an override; validate parameters and obtain approval before submission. |
| ESS | Retrieve Latest LDAP Changes | `TBD` | No / No | Use the configured default contract below unless the user supplies an override; validate parameters and obtain approval before submission. |
| ESS | Send Pending LDAP Requests | `TBD` | No / No | Use the configured default contract below unless the user supplies an override; confirm no active instance, then validate the target environment and obtain approval before submission. |
| Other | None currently loaded | TBD | TBD | Do not infer or execute another method. Add a task only after its approved execution boundary is confirmed. |

## Default ESS Contract: User and Role LDAP Synchronization

For **Run User and Roles Synchronization Process** and **Retrieve Latest LDAP
Changes**, use the following default Scheduler REST metadata unless the user
explicitly provides a replacement value:

| Field | Default value |
| --- | --- |
| `jobDefinitionId` | `JobDefinition://oracle/apps/ess/hcm/users/SyncRolesJob` |
| `application` | `EarHcmEss` |

The default metadata does not supply request parameters, scheduling values, a
target environment, required privileges, or approval. Confirm those inputs
before submission. If the user overrides either default value, treat the
replacement as a new job contract: validate it against the target environment
and present the resulting exact payload for explicit approval immediately
before submission.

## Default ESS Contract: Import User Login History

For **Import User Login History**, use the following default Scheduler REST
metadata unless the user explicitly provides a replacement value:

| Field | Default value |
| --- | --- |
| `jobDefinitionId` | `JobDefinition://oracle/apps/ess/hcm/users/AseInactiveUsersDataLoadJob` |
| `application` | `EarHcmEss` |
| `requestParameters` | `[]` |

The default metadata does not supply scheduling values, a target environment,
required privileges, or approval. Use the empty parameter array unless the
user explicitly supplies replacement request parameters. Validate any
replacement job definition, application, or parameters against the target
environment and present the resulting exact payload for explicit approval
immediately before submission.

## Default ESS Contract: Import Users and Roles into Application Security

For **Import Users and Roles into Application Security**, use the following
default Scheduler REST metadata unless the user explicitly provides a
replacement value:

| Field | Default value |
| --- | --- |
| `jobDefinitionId` | `JobDefinition://oracle/apps/ess/hcm/applicationsSecurity/AseImportUsersAndRolesJob` |
| `application` | `EarHcmEss` |

The default metadata does not supply request parameters, scheduling values, a
target environment, required privileges, or approval. Confirm those inputs
before submission. If the user overrides either default value, treat the
replacement as a new job contract: validate it against the target environment
and present the resulting exact payload for explicit approval immediately
before submission.

## Default ESS Contract: Send Pending LDAP Requests

For **Send Pending LDAP Requests**, use the following default Scheduler REST
metadata unless the user explicitly provides a replacement value:

| Field | Default value |
| --- | --- |
| `jobDefinitionId` | `JobDefinition://oracle/apps/ess/hcm/users/ProcessLdapRequests` |
| `application` | `EarHcmEss` |
| `requestParameters` | `[]` |

The default metadata does not supply scheduling values, a target environment,
required privileges, or approval. Use the empty parameter array unless the
user explicitly supplies replacement request parameters. Validate any
replacement job definition, application, or parameters against the target
environment. Before submission, confirm that no Send Pending LDAP Requests
instance is active and present the resulting exact payload for explicit
approval immediately before submission.

## Scheduled ESS Request Example

For a job whose confirmed contract supports scheduling, use a `schedule`
object only when the user explicitly approves the recurring schedule. Resolve
the placeholder values when preparing the exact payload; do not submit the
placeholders literally.

```json
"schedule": {
  "timezone": "{current_iana_timezone}",
  "recurrences": [
    {
      "icalString": "FREQ=DAILY;INTERVAL=1;",
      "startDate": "{current_timestamp_in_current_timezone}",
      "endDate": "{current_timestamp_in_current_timezone_plus_10_calendar_years}"
    }
  ]
}
```

Validate the resolved IANA time zone, recurrence, start and end dates, and the
job's scheduling support before submission. Do not include both `schedule` and
`scheduleId` in the same request. This is an input example, not a default
schedule; in particular, do not create a recurring Send Pending LDAP Requests
schedule unless separately approved.

## ESS Submitter Result Handoff

For every ESS invocation, collect the complete structured outputs returned by
`core.fusion-api.ess-job-submitter`:

- `execution_result`, including `requestId`, submission state, and status;
- `diagnostics`, including the polling window, poll interval, and timeout
  result; and
- `audit_summary`, including the target environment and any returned external
  identifiers.

For a live submission, invoke the core skill with the approved polling timeout
and interval and a unique `--output` path in the active project workspace. Do
not use `--submit-only` for an execution initiated by this skill. Wait for the
core invocation to finish, then collect and parse the structured output at that
path before deciding whether an ESS `requestId` or returned `processId` exists.
A launched command or quiet console output is not evidence that the job was
submitted.

If the invoking client reports completion but the expected output artifact is
not immediately available, perform a bounded local collection reconciliation:
check for and parse the artifact for up to 30 seconds after client completion.
This is a filesystem-read wait only; it must not resubmit the request,
reauthenticate, make another ESS status call, or add another polling loop.
Capture the core client's exit code and parse any artifact it wrote before
classifying the result, because the core submitter writes its structured result
before returning its timeout or terminal-failure exit code. Only after this
collection window expires with no artifact and no captured ESS identifier may
the outcome be treated as indeterminate.

The core submitter writes a redacted failure artifact whenever its `--output`
path is supplied, including failures before a request ID is available. Parse
that artifact first and persist its failure class and message. Treat a missing
artifact after the reconciliation window as `artifact_persistence` or client
handoff failure; it is not evidence that the ESS request was not submitted and
must never trigger an automatic resubmission.

## Unidentified Submission Recovery

When a completed submission handoff has no request ID or process ID, do not
retry or automatically query Fusion. Return this user-facing response after
persisting the redacted failure artifact: **“I couldn't find a request ID. I
can check whether a matching job ran in the target environment during the last
few minutes. Do you want me to check?”**

If the user explicitly asks to check, use the core submitter's read-only
`--find-recent-job-definition` and `--since-minutes` route with the exact
approved job definition, target environment, and user-requested window (for
example, two or three minutes). Persist every matching request ID and status.
If exactly one candidate matches, return its ID and offer read-only status
tracking. If zero candidates, multiple candidates, inaccessible history, or a
lookup failure occurs, do not submit again. Tell the user: **“I couldn't find
an unambiguous matching job. Please open Scheduled Processes in the target
Fusion application and check for this job before trying again.”**

Treat `execution_result.requestId` as the Oracle Scheduler request/process
identifier. If Fusion returns a separate `processId` in a full status payload,
preserve it as an additional external identifier; do not invent one when it is
absent. Persist the returned result in the project execution audit, redacting
credentials, tokens, secrets, and sensitive parameter values. Include at least
the request ID, job definition, application, target environment, poll settings,
last or terminal status, process phase, cause, elapsed time, ECID when present,
and references to available diagnostics.

Use `core.fusion-api.ess-job-submitter` as the sole authority for submitting,
tracking, OAuth refresh-once behavior for HTTP 401 or 403, polling, timeout,
and terminal-status handling. Do not add a second polling loop, refresh, or
live retry in this skill. Apply the core skill's result rules as follows:

- On its successful result, persist the returned request ID and structured
  outputs.
- On its exit code `3`, classify the result as `process_timeout`, retain the
  returned request ID and last status, and do not retry.
- On its exit code `4`, classify the result as `process_failed`, retain the
  returned request ID and terminal status, and do not retry.
- If the completed core invocation returns no ESS `requestId` or `processId`,
  classify the outcome as `indeterminate`. Preserve the structured result and
  available diagnostics, and do not retry the live request until its status is
  confirmed and fresh approval is received.

## ESS Input Confirmation Gate

Before every ESS submission, resolve and display the complete submission input
to the user once. The display must include the target environment, operation,
full payload (including defaults and overrides), request parameters, schedule
or on-demand mode, polling timeout and interval, and any relevant preflight
condition such as the no-active-instance check for Send Pending LDAP Requests.

Ask the user to confirm that displayed submission. Run the job only after that
confirmation is received. A confirmation of the displayed submission is the
single user-confirmation gate for those inputs; do not ask the user to confirm
the same unchanged inputs again. If an input, target, payload, schedule, or
polling setting changes after confirmation, display the revised submission and
obtain a new confirmation before running it.

## Required Response: Manage Configuration Set Migration Target Security Policy

When the user asks to set **Manage Configuration Set Migration Target Security
Policy**, respond with the following message, adapting only the project and
environment names when they are known:

> **Manage Configuration Set Migration Target Security Policy**
> (`ORA_FND_SET_CSM_TARGET_SECURITY`) is a **Manual** FSM task. Complete it in
> the Oracle Fusion application; this FSCR skill must not use REST APIs, CSV
> import/export, FBDI, HDL, or ESS to set the policy.
>
> Before making the change, confirm the target Fusion environment, the
> configuration set and migration target in scope, and the approved security
> policy values from the implementation security design. Do not infer policy
> values or widen user access.
>
> In the Oracle Fusion application, open the relevant Setup and Maintenance
> task from the implementation project, review the current target security
> policy, apply the approved values, and save the change. Follow the project's
> approval process before applying a policy that changes access to migrated
> setup data.
>
> After completion, provide sanitized evidence: the environment, configuration
> set or migration-target identifier, completion status, completion time, and
> reviewer/approver. Do not include credentials, tokens, customer data, or
> sensitive policy values in the evidence.
>
> **TBD:** Exact page fields, allowed policy values, and validation criteria
> must come from approved Oracle product guidance and the project security
> design.

## Required Response: ESS Tasks

When the user asks to run one of the ESS tasks in the Current Task
Classification table, respond with the following message, adapting only the
task name and code:

> **{Task Name}** (`{Task Code}`) is an **ESS** task. FSCR will use
> `core.fusion-api.ess-job-submitter` to submit and monitor the process only
> after you provide the target Fusion environment, request parameters, and
> explicit approval to submit. For **Run User and Roles Synchronization
> Process** and **Retrieve Latest LDAP Changes**, FSCR defaults to
> `JobDefinition://oracle/apps/ess/hcm/users/SyncRolesJob` and `EarHcmEss`
> unless you explicitly override either value. For **Import Users and Roles
> into Application Security**, FSCR defaults to
> `JobDefinition://oracle/apps/ess/hcm/applicationsSecurity/AseImportUsersAndRolesJob`
> and `EarHcmEss` unless you explicitly override either value.
> For **Import User Login History**, FSCR defaults to
> `JobDefinition://oracle/apps/ess/hcm/users/AseInactiveUsersDataLoadJob`, `EarHcmEss`, and
> `requestParameters: []` unless you explicitly override a value.
>
> The FSM task code is not an ESS job definition and must not be used as one.
> **TBD:** scheduling requirements and completion criteria must be confirmed
> from Oracle product guidance or target-environment metadata before
> submission. Any job definition, application, or request-parameter override
> must also be confirmed before submission.
>
> After approval, FSCR will submit the request, record the returned request ID,
> monitor it within the approved timeout, and persist a redacted execution
> audit. It will not retry a failed or timed-out ESS submission without a new
> approval or an idempotency-safe recovery path.

## Required Response: Send Pending LDAP Requests

When the user asks to run **Send Pending LDAP Requests**, respond with the
following message, adapting only known project and environment details:

> **Send Pending LDAP Requests** is an **ESS** process. It sends pending bulk
> and future-dated user-account and role-provisioning or deprovisioning
> requests to LDAP. FSCR will use `core.fusion-api.ess-job-submitter` only
> after you provide the target Fusion environment, required privileges, and
> explicit approval immediately before submission. FSCR defaults to
> `JobDefinition://oracle/apps/ess/hcm/users/ProcessLdapRequests`,
> `EarHcmEss`, and `requestParameters: []` unless you explicitly override a
> value.
>
> The display name is not an ESS job definition ID. **TBD:** Confirm any
> parameter override, batch-size rules, scheduling requirements, and completion
> criteria from approved Oracle product guidance or target-environment metadata
> before submission. Do not infer them from an FSM task code.
>
> Before submission, confirm that no existing instance of Send Pending LDAP
> Requests is running. Only one instance may run at a time. Submit an
> on-demand request unless the user explicitly approves a schedule; do not
> create a recurring schedule by default.
>
> After approval, FSCR will submit and monitor the request, record the request
> ID, target environment, redacted parameters, terminal status or timeout,
> elapsed time, and diagnostic references in the project workspace. It will
> not retry a failed or timed-out request without fresh explicit approval.

## Workflow

1. First route dedicated setup-object changes as described above. For the remaining common controls, match the task to the Current Task Classification table.
2. For Manage Configuration Set Migration Target Security Policy, use the
   Required Response section exactly.
3. For either of the other two Manual tasks, respond: `This task is Manual.
   Complete it in the Oracle Fusion application.`
4. For an ESS task, use the Required Response: ESS Tasks section. For Run User
   and Roles Synchronization Process, Retrieve Latest LDAP Changes, Import
   Users and Roles into Application Security, Import User Login History, or
   Send Pending LDAP Requests, apply the applicable Default ESS Contract
   unless the user provides an override. For Send Pending LDAP Requests, use
   the Required Response: Send Pending LDAP Requests section. Validate the
   task, target environment,
   `jobDefinitionId`, application, request parameters, privileges, timeout,
   and polling interval. Display the complete resolved submission inputs once
   and obtain the user's confirmation of that display before invoking
   `core.fusion-api.ess-job-submitter`.
   For a scheduled request, also validate the schedule's resolved time zone,
   recurrence, start and end dates, and explicit schedule approval; do not use
   both `schedule` and `scheduleId`.
5. Invoke `core.fusion-api.ess-job-submitter` using its approved polling
   options and a unique project-workspace `--output` path. After the client
   returns, collect its `execution_result`, `diagnostics`, and `audit_summary`
   from that artifact. If the artifact is not immediately available, use the
   bounded local collection reconciliation in ESS Submitter Result Handoff
   before classifying the result. Require its returned ESS request ID or
   process ID before treating the submission as identified, and apply its
   polling, timeout, and terminal failure rules without adding a second poll
   or retry. Record the request ID or returned process ID, target environment,
   job definition, application, polling settings, terminal or last status, and
   redacted diagnostics in the project workspace when project context is
   supplied. Treat the invocation as indeterminate only after the collection
   window expires with no structured result or ESS identifier; do not retry
   without a confirmed status and fresh approval.
6. Before submitting Send Pending LDAP Requests, confirm that no existing
   instance is running. Allow an on-demand request or an explicitly approved
   schedule only; do not create a recurring schedule by default.
7. Identify the task name and code, and request completion evidence appropriate
   to the implementation process, such as a reviewer-confirmed completion
   status or sanitized screenshot.
8. If the task is listed as Other, state its configured boundary. Do not
   invoke a job, API, loader, or another skill unless the user explicitly asks
   for an approved capability.
9. If the task is not listed, report `TBD: execution type is not configured for this skill.` Do not infer a manual, ESS, or automated route.

## Completion Guidance

For the currently loaded Manual tasks, the implementor must use the relevant
Oracle Fusion setup or Security Console page and follow approved product and
project procedures. This skill provides task classification only; it does not
define product-field values, make design decisions, or verify that a manual
configuration is correct.

## Preflight Checks

Before providing manual-completion guidance, confirm that the requested task
has an unambiguous classification in the Current Task Classification table.
For an ESS task, before invoking `core.fusion-api.ess-job-submitter`, confirm:

- target Fusion environment identity;
- exact Oracle `jobDefinitionId`, application, and request parameters; use an
  applicable Default ESS Contract only for its named task and only until the
  user explicitly overrides it;
- required Fusion privileges and the approved timeout and polling window;
- project workspace destination, when project context is supplied; and
- one user confirmation of the displayed complete submission input, including
  the exact target environment, operation, payload, and polling settings.

Fail closed when the task, job contract, target environment, or approval is
missing, ambiguous, or mismatched. Do not use an FSM task code or display name
as a substitute for an ESS job definition. For Send Pending LDAP Requests,
also confirm no instance is already running before submission.

## Failure Handling

Classify and report failures as `input_validation`,
`catalog_or_metadata_mismatch`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

- For an invalid or incomplete ESS contract, environment mismatch, missing
  privilege, or approval blocker, stop before any side effect and state the
  required correction.
- For Fusion API failures, record the endpoint path, response summary, and
  request ID or ECID when available; redact credentials, tokens, customer data,
  and sensitive configuration values.
- For a timeout or failed ESS process, persist the target environment, job
  definition, request ID, last status, elapsed wait, and available diagnostics
  in the project workspace when project context is supplied.
- Do not supplement the core submitter's polling, authentication refresh, or
  timeout behavior with a separate request loop. Preserve the core result and
  use its returned request ID to resume tracking only after the required
  approval gate is satisfied.
- Do not retry a failed, timed-out, or indeterminate ESS submission without a
  confirmed request status and fresh explicit approval, unless an
  idempotency-safe recovery path is confirmed.
- If audit or diagnostic persistence fails, return an
  `artifact_persistence` failure and identify the intended artifact location
  without exposing sensitive values.

## Safety Rules

- Do not expose credentials, tokens, secrets, customer data, or sensitive
  security configuration in completion evidence.
- For a common control classified Manual, hand off to the implementor.
  Dedicated FSM setup changes use their focused skill and Data Loader approval.
- Do not submit Send Pending LDAP Requests while another instance is running.
- Do not create a recurring Send Pending LDAP Requests schedule without
  explicit user approval.
- Do not retry a failed or timed-out Send Pending LDAP Requests request without
  fresh explicit approval.
- Mark unavailable task types, product behavior, and source guidance as `TBD`
  rather than inventing a route.
