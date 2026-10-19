---
skill_id: "erp.risk-and-security.assign-initial-users"
name: "Assign Initial Users Implementation Guidance"
description: "Orchestrates Risk Administrator coverage and ERP Risk and Security implementation guidance for the Assign Initial Users functional area."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Assign Initial Users"
functional_area_code: "ORA_GTG_RM_INITIAL_USERS"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "ERP risk and security pillar team"
version: "0.2.2"
inputs:
  - "implementation_objective"
  - "project_id"
  - "project_context"
  - "fusion_environment_context"
  - "assign_initial_users_scope"
  - "assign_initial_users_requirements"
  - "risk_administrator_coverage_mode_optional_prerequisite_or_standalone"
  - "authenticated_runner_access_approval_when_required"
  - "live_execution_approval"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "risk_administrator_coverage_result"
  - "authenticated_runner_access_result"
  - "risk_administrator_coverage_report"
  - "risk_administrator_assignment_plan"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run_and_artifact"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/risk-administrator-coverage/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/risk-administrator-coverage/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_GTG_ASSIGN_DEFAULT_PROCESS_OWNERS"
  - "ORA_GTG_ASSIGN_RISK_POWER_USER_ROLE"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Reads Fusion SCIM role memberships and user records during Risk Administrator coverage verification."
  - "Writes redacted verification, report, run, and token-usage artifacts to the selected project workspace."
  - "Adds Risk Administrator membership by Fusion SCIM PATCH only after explicit approval of the exact selected user and immutable assignment plan."
required_privileges:
  - "Read access to Fusion SCIM Roles and Users resources."
  - "Privilege to update membership of the Risk Administrator role."
---

# Assign Initial Users Implementation Guidance

## Purpose

Orchestrate the Assign Initial Users functional area. Establish Risk Administrator coverage first, then route a parent-only invocation through Assign Default Process Owners followed by Assign Risk Power User Role. Each routed task retains its own input, customer-decision, approval, and live-execution gates.

## Consultant-facing behavior

Follow the offering [Consultant Interaction Contract](../references/consultant-interaction-contract.md).
Present coverage results, mappings, owner decisions, access decisions, and
exceptions as compact Markdown tables. Ask for a clear chat or table
confirmation and retain any machine-readable decision record internally. Do not
ask an implementation consultant to open, edit, or approve a JSON file.

## When to Use

Use this functional-area skill after Risk and Security scope is confirmed and the project needs Risk Administrator coverage validation, assign-initial-users setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Risk and Security` (`ORA_RISK_AND_CONTROLS`)
- Functional area / Setup Object: `Assign Initial Users` (`ORA_GTG_RM_INITIAL_USERS`)

## Setup Tasks

In `prerequisite` mode, run [Risk Administrator Assignment
Verification](#risk-administrator-assignment-verification) first. Do not route
to either task until it reports verified organization coverage **and** ready
authenticated-user access for the same project and environment.

A request that names either nested task directly is still an **Assign Initial
Users** request. Re-enter this parent in `prerequisite` mode before the nested
task starts. Do not treat a direct child request as evidence that the
prerequisite completed, and do not begin a child inventory while the access
decision is pending. Once the parent records the verified same-environment
result, continue the requested child as the sole active workflow.

1. [Assign Default Process Owners](assign-default-process-owners/SKILL.md) (`ORA_GTG_ASSIGN_DEFAULT_PROCESS_OWNERS`)
2. [Assign Risk Power User Role](assign-risk-power-user-role/SKILL.md) (`ORA_GTG_ASSIGN_RISK_POWER_USER_ROLE`)

After the verification reports coverage, continue the parent workflow:

1. Run [Assign Default Process Owners](assign-default-process-owners/SKILL.md)
   (`ORA_GTG_ASSIGN_DEFAULT_PROCESS_OWNERS`).
2. Run [Assign Risk Power User Role](assign-risk-power-user-role/SKILL.md)
   (`ORA_GTG_ASSIGN_RISK_POWER_USER_ROLE`) only when **Assign Default Process
   Owners** has completed and verified one or more current default `USER`
   owners, or when the consultant explicitly deferred **Assign Default Process
   Owners** and selected **Assign Risk Power User Role** as the next task.

Do not start **Assign Risk Power User Role** if **Assign Default Process
Owners** is awaiting mapping, customer decisions, or approval; is blocked or
fails; or does not verify a current default `USER` owner, unless the consultant
explicitly deferred **Assign Default Process Owners** and selected **Assign
Risk Power User Role**. That switch does not assert owner readiness or bypass
**Assign Risk Power User Role**'s own upstream, approval, or side-effect gates.

The same stop rule applies to the offering-level handoff. While **Assign
Default Process Owners** is awaiting a coverage selection, mapping
confirmation, candidate decision, or approval, return only that task's
business decision table. Do not begin audit-policy, active-module, or
algorithm work until the process-owner task reaches a terminal result and the
offering workflow explicitly routes onward. An explicit deferral is a terminal
handoff only for the requested next task.

When the durable workflow re-invokes **Assign Default Process Owners**, it may
provide that child’s [Phase Evidence Handoff](../references/phase-evidence-handoff.md)
only while its input and environment remain unchanged. Do not start **Assign
Risk Power User Role** merely because a process-owner read batch or internal
request plan has been prepared.

## Implementation Notes

Use generated setup-task metadata files for task-level planning and sequencing.
Track token usage for every generated project artifact or skill-run record
using the manifest policy.

## Risk Administrator Assignment Verification

Run this gate first. `risk_administrator_coverage_mode` defaults to
`prerequisite`. When the gate reports verified organization coverage and
authenticated-user readiness, continue with [Setup Tasks](#setup-tasks). In
`standalone` mode, execute only this verification and its durable evidence
workflow; do not continue with [Setup Tasks](#setup-tasks) or create a setup
plan.

Confirm two independent conditions before routing onward: at least one active
Fusion user has effective Risk Administrator coverage, and the authenticated
Fusion user running this workflow has that same effective access. IT Security
Manager includes Risk Administrator, so direct assignment of either role
qualifies a user; the same user does not need both roles.

Resolve the authenticated Fusion user through `selfDetails`, then require one
exact, active SCIM User result. Check that user against both role memberships
while retaining the broader active-coverage review. Do not substitute a known
administrator, a guessed account, or a different source of identity.

When the authenticated user lacks both roles, present a final approval table
for that exact active person to receive Risk Administrator access. Do not
change access merely because organization coverage already exists. After fresh
approval, recheck the exact user and Risk Administrator membership, submit one
SCIM membership addition through Core, then verify the returned membership.
Never retry the change automatically.

Present completion as a table with **Coverage result**, **Business impact**,
and **Next action**. When an assignment is needed, use **Person**,
**Requested access**, **Current result**, and **Approval**. State whether the
organization is covered and whether the authenticated user is ready, but do not
disclose role identifiers, member counts, user IDs, request details, or the
internal search path to the consultant.

Do not perform process-owner work, Risk Power User provisioning, audit-policy activation, active-module identification, or algorithm publication while in `standalone` mode.

### Core execution delegation

Use [`scripts/risk_administrator_precondition.py`](scripts/risk_administrator_precondition.py)
to expand and evaluate the deterministic prerequisite from returned Core
results. It only plans Core requests and interprets SCIM results; it does not
call Fusion, manage OAuth, or select a substitute user. Prepare its SCIM role,
membership, user-status, and approved assignment requests through
`core.fusion-api.rest-api-client`. Do not import, launch, or reproduce the
Core REST client, its OAuth flow, token cache, retry behavior, or HTTP
transport from this pillar skill.

Use Core results only for coverage evaluation, approval checks, task routing, and durable reporting.

### Preflight checks

Before any Fusion-changing request, complete these checks through the declared Core skills and stop on the stated failure class. Read-only coverage verification may begin only after the required project and environment context are present and the prescribed project artifact destination is safe and writable.

- Confirm the resolved Fusion environment identity is the intended target and that the reusable OAuth session and required SCIM read privileges are usable through `core.fusion-api.rest-api-client`. A rejected cached session may be refreshed once; after that, stop with `auth_expired_or_invalid` or `authorization_or_privilege`.
- Validate one or more exact Risk Administrator and IT Security Manager role
  records before reporting authenticated-user readiness. Membership in any
  matching accepted-role record establishes readiness. A missing or malformed
  role result stops with `catalog_or_metadata_mismatch`; require a unique Risk
  Administrator record only before preparing an assignment.
- Before a live PATCH, reconfirm that the authenticated user is uniquely
  resolved and active, the user is not already a Risk Administrator member,
  and the assignment role resolves uniquely. Treat a missing, ambiguous, or
  inactive identity as `input_validation`.
- Validate the one-member JSON PATCH payload, live target environment, and durable report/run/token-usage destinations before execution. An unsafe or unwritable project path stops with `artifact_persistence`.
- Confirm that the explicit approval names the exact selected user, target environment, and immutable assignment-plan digest. Absent or mismatched approval stops with `approval_blocker`.

This skill has no long-running operation or polling stage. It uses plan-first behavior for assignment and never automatically retries a live PATCH.

### Early-exit coverage verification

Run the deterministic planner in these stages. Its request-plan output is
internal; execute every entry only through Core and rerun the planner with the
saved Core results.

1. In discovery, resolve the signed-in user, that user's exact active SCIM
   account, and both accepted-role result sets. If the authenticated user
   belongs to either role in any matching record, both organization coverage
   and runner access are proven without additional member lookups.
2. If the authenticated user lacks both roles, evaluate other members in the
   existing role-membership order, one SCIM user read at a time, until broader
   active coverage is proven or all members are exhausted. Do not read a member
   twice when it belongs to both roles.
3. When the authenticated user lacks access, return the approval table even if
   another active user already establishes organization coverage. The approved
   discovery result is the only input that may begin preflight.
4. In preflight, reread the exact authenticated user and Risk Administrator
   role. If the user already gained access, finish with no change; otherwise
   produce one approved membership-addition request. In verification, require
   a successful Core assignment result and a fresh role membership result that
   contains that user.

An unreadable, inactive, or ambiguous authenticated user blocks the workflow
before a role change. An unreadable or inactive other member does not establish
organization coverage; retain that exception and continue only until coverage
is proven or the ordered review is complete.

### Assignment and approval

If the authenticated user lacks access, that exact user is the only candidate
for this workflow. Require one active exact SCIM account; never silently select
a different account. Present the person in the approval table without exposing
retained assignment-integrity data.

Only after explicit confirmation of that exact assignment, bind the internally
retained approval to the exact authenticated user, environment, and target role
before preflight. Immediately before the request, the planner rereads the
authenticated user and Risk Administrator membership. If access now exists,
stop without a change. Afterwards, defer the fresh membership verification read
to Core. Never retry the assignment.

```http
PATCH /hcmRestApi/scim/Roles/{riskAdministratorRoleId}
Content-Type: application/json

{
  "members": [{"value": "<selectedUserId>", "operation": "ADD"}]
}
```

An approval for discovery or a different selected user is not approval for the assignment.

### Role and user resolution

Resolve the exact SCIM role records for each code:

- `GET /hcmRestApi/scim/Roles?filter=name eq "ORA_GTG_RISK_ADMINISTRATOR_JOB"`
- `GET /hcmRestApi/scim/Roles?filter=name eq "ORA_FND_IT_SECURITY_MANAGER_JOB"`

One or more exact matching records are valid for the readiness review; a user
needs membership in only one accepted role. Risk Administrator must resolve
uniquely only when it becomes the assignment target. For each unexamined
member, use one SCIM user read sequentially until broader coverage is found.

### Reporting and persistence

Persist redacted JSON and Markdown coverage verification/report artifacts under:

```text
project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/risk-administrator-coverage/current/
```

Record the run under `project/{project_id}/state/runs/` and append the required token-usage record. For a coverage result, report organization-coverage status, authenticated-runner readiness, number of user-status checks, early-exit status, remaining members skipped, and inactive or unreadable-member exception counts. When runner access is assigned, record only its redacted assignment outcome and verification.

Record the preflight stage and outcome; on failure, record the failure class, redacted message, recommended action, environment, and safe artifact references. Do not persist access tokens, credentials, authorization headers, usernames, user IDs, membership lists, or raw SCIM payloads.

### Validation scenarios

Use synthetic SCIM fixtures or mocked Core results to validate:

1. The authenticated user is directly assigned Risk Administrator: both role records resolve, runner access and organization coverage complete without member lookups.
2. The authenticated user is directly assigned IT Security Manager: one or more exact matching role records may be returned; membership in any one of them completes runner access and organization coverage without member lookups.
3. Another active user establishes broader coverage while the authenticated user lacks both roles: return a final approval table for the authenticated user and make no PATCH before approval.
4. A post-approval preflight finds the user already assigned: finish without a duplicate change.
5. A successful assignment must be followed by a fresh membership result containing the authenticated user; a failed assignment or absent membership is a verification failure with no retry.
6. Coverage artifacts contain only prescribed redacted counts and role outcome; they contain no usernames, user IDs, memberships, or OAuth data.
7. Missing project or environment context blocks the workflow before a SCIM request with `input_validation`; unsafe or unwritable artifact paths stop with `artifact_persistence`.
8. A rejected reusable OAuth session is refreshed once for a read, then stops with the applicable auth or authorization failure class; no live PATCH is retried.
9. An ambiguous or inactive authenticated user, stale role state, or missing/mismatched approval blocks PATCH without mutation.
10. `standalone` mode produces only coverage-gate outputs; a parent-only `prerequisite` invocation verifies both coverage conditions, starts **Assign Default Process Owners**, and routes to **Assign Risk Power User Role** only after **Assign Default Process Owners** verifies current default `USER` owners. Each child task retains its own gates.

### Failure handling

- Missing or ambiguous role codes: stop with `catalog_or_metadata_mismatch`.
- Authenticated read failure: allow one token-refresh retry, then stop with `auth_expired_or_invalid` or `authorization_or_privilege`.
- Authenticated user missing, ambiguous, or inactive: stop before PATCH with `input_validation` and ask the user to resolve the authenticated Fusion identity.
- Target-environment mismatch or an unavailable read-only Core request: stop with `transport_or_environment` and record the target environment.
- PATCH error or failed post-assignment verification: record a redacted `fusion_api_error` diagnostic and require new approval before another attempt.
- Artifact-writing failure: preserve redacted diagnostics in a safe temporary location when available, report `artifact_persistence`, and do not continue to PATCH.
