---
skill_id: "core.getting-started.implementation-users"
name: "Implementation Users"
description: "Creates or guides creation of greenfield Oracle Fusion Cloud 26B implementation users with the minimum Functional Setup Manager role grant."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "project_context"
  - "username"
  - "user_email"
  - "execution_approval"
outputs:
  - "implementation_user_plan"
  - "role_assignment_summary"
  - "execution_audit"
  - "write_gate_summary"
  - "validation_results"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
persists_project_state: true
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/core/getting-started/implementation-users/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/core/getting-started/implementation-users/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Oracle Fusion Cloud Applications 26B"
side_effects:
  - "Creates or updates Fusion users and the configured implementation-user job-role assignments only after explicit user approval."
required_privileges:
  - "Oracle HCM Cloud service administrator or TechAdmin-equivalent user"
  - "IT Security Manager"
  - "Application Implementation Consultant"
  - "IT Security Manager"
  - "Application Diagnostic Administrator"
---

# Initial Fusion Implementation Users

## Purpose

Use this skill to create an initial implementation user in a greenfield
Oracle-managed Fusion 26B SaaS environment. The default role plan is grounded in
Oracle's Functional Setup Manager Roles and Allowed Activities mapping and
assigns only the role necessary for the listed activities.

## Required Inputs

For every run, prompt for:

- `username`
- `user_email`
- `project_id`, unless a project is already selected

## Required Reference

Before planning or executing, read:

- `references/oracle-26b-hcm-implementation-users.md`
- Oracle 26B `Mapping of Setup Activities and Required Roles`, section
  `Roles and the Allowed Activities`, for the minimum role required to perform
  the listed activities.

## Workflow

1. Generate a plan with `scripts/prepare_implementation_user_plan.py`.
2. Run read-only preflight against the target pod before any write:
   - verify the target user does not already exist, or get update approval
   - resolve the required job role
   - resolve every planned implementation-user job role
3. Ask for explicit write approval with the resolved plan.
4. Execute the setup sequence:
   - run `Retrieve Latest LDAP Changes`
   - run `Import Users and Roles into Application Security`
   - create the implementation user with associated person type `None`, user
     category `DEFAULT`, active status, email, and username
   - assign the planned implementation-user job roles
5. Validate Security Console role membership and implementation user access.

## REST Execution Support

Use `scripts/execute_implementation_user_plan.py` to execute supported REST
steps through `core.fusion-api.rest-api-client`.

The executor creates users through:

- `/hcmRestApi/scim/Users`

The executor assigns roles through:

- `/hcmRestApi/scim/Roles/`

The executor is conservative:

- dry-run is the default
- `--live-preflight` resolves the target user and every planned role without writing; execution repeats that role-resolution gate before creating a user
- `--execute` requires `--confirm-create-user`
- if the user already exists, execution stops instead of overwriting it
- final role assignments are resolved through the SCIM Roles endpoint and added
  to the role membership after the user is created
- roles with a planned `ORA_` identifier are resolved by SCIM role `name` using
  that planned role code, not by display name
- every planned job role must pass the `ORA_` planned-identifier check using
  the SCIM role `name`
- if the user already exists, use `--assign-roles-to-existing` to assign the
  planned roles to that user without recreating it
- use `--include-roles-in-user-body` only for pods that explicitly accept SCIM
  `roles` values in the `/Users` create body
- Security Console-only or environment-specific setup remains listed as manual
  follow-up in the audit

## Role Policy

Oracle 26B Functional Setup Manager `Roles and the Allowed Activities`
grounding establishes the minimum role necessary to perform the listed
activities:

- `Application Implementation Consultant` (`Job`)

Role-selection logic:

- Use the Oracle `Roles and the Allowed Activities` section as the controlling
  source for the minimum Functional Setup Manager role grant.
- Select `Application Implementation Consultant` because that role covers the
  full listed activity set for an implementation user: reviewing and
  configuring offering features, performing all setup tasks, managing setup
  data through offerings, functional areas, and implementation projects,
  export/import, comparison, setup data reports, export/import process
  submission and monitoring, implementation project management, and managing
  integration of additional applications.
- Do not add `Application Implementation Manager`; Oracle lists it for a
  smaller activity set and it does not cover all setup tasks and setup data
  management.
- Do not add `Functional Setups User`; Oracle positions it for specific setup
  tasks and requires a separate role with task-specific privileges.
- Do not add `Export Import Functional Setups User`; Oracle positions it for
  export/import, comparison, and report activities and requires the
  `Functional Setups User` role plus task-specific setup data privileges.
- Add the configured IT Security Manager and Application Diagnostic
  Administrator job roles because this implementation-user policy explicitly
  requires them. Do not add further product, HCM, payroll, compensation,
  data, security-profile, or role-mapping grants unless a later, separate
  project-specific scope analysis explicitly identifies them as necessary.

Do not treat listed privileges, such as `Manage Setup Migration Settings` or
`Manage Third Party Applications`, as roles. Capture them as possible
task-specific privilege requirements if the project later narrows the
implementation user's scope.

At execution time, enforce planned `ORA_` role identifiers from the plan. Any
role with a planned identifier such as `roleCode`, `code`, `name`, or `value`
starting with `ORA_` must be resolved from `/hcmRestApi/scim/Roles` with
`filter=name eq "{ORA_ROLE_CODE}"`. Do not resolve those roles by display name
because Fusion can expose different non-ORA roles with the same display name.
Roles without a planned `ORA_` identifier may be resolved by display name.

Role grants assigned when creating the implementation user:

- `Application Implementation Consultant` (`ORA_ASM_APPLICATION_IMPLEMENTATION_CONSULTANT_JOB`)
- `IT Security Manager` (`ORA_FND_IT_SECURITY_MANAGER_JOB`)
- `Application Diagnostic Administrator` (`ORA_FND_DIAG_ADMINISTRATOR_JOB`)

`Application Implementation Consultant` remains the minimum Functional Setup
Manager role. The IT Security Manager and Application Diagnostic Administrator
grants are explicit implementation-user role-policy additions and must be
preflighted and approved with the same user-create payload.

## Stop Conditions

Stop before write when:

- the user exists and update behavior is not approved
- any required role cannot be resolved in the target pod
- the user has not approved the resolved write plan

## Commands

Preview plan:
```bash
python3 core/getting-started/implementation-users/scripts/prepare_implementation_user_plan.py \
  --username "{username}" \
  --email "{email}" \
  --project-id "{project_id}" \
  --output project/{project_id}/artifacts/core/getting-started/implementation-users/current/{username}_implementation_user_plan.json
```

Execution plan:

```bash
python3 core/getting-started/implementation-users/scripts/prepare_implementation_user_plan.py \
  --username "{username}" \
  --email "{email}" \
  --project-id "{project_id}" \
  --execution-mode execute \
  --output project/{project_id}/artifacts/core/getting-started/implementation-users/current/{username}_implementation_user_plan.json
```

Dry-run the REST executor against a generated plan:

```bash
python3 core/getting-started/implementation-users/scripts/execute_implementation_user_plan.py \
  --plan project/{project_id}/artifacts/core/getting-started/implementation-users/current/{username}_implementation_user_plan.json
```

Execute supported REST calls after explicit approval:

```bash
python3 core/getting-started/implementation-users/scripts/execute_implementation_user_plan.py \
  --plan project/{project_id}/artifacts/core/getting-started/implementation-users/current/{username}_implementation_user_plan.json \
  --execute \
  --confirm-create-user
```

Only the documented relative `/hcmRestApi/scim/Users` and `/hcmRestApi/scim/Roles`
collections are allowed; absolute endpoint overrides are rejected even on the
standard host. The wrapper selects standard-Fusion context and `--scim-only`,
validates destinations before login and sending, and rejects write redirects.
Lookup failures stop execution; `--allow-create-after-preflight-error` is rejected.
Passwords stay in Fusion reset/enrollment and must never enter a plan, body or log.
The managed token cache stays outside the checkout. SCIM field mappings remain
configurable through:

- `--user-query-field`
- `--user-key-field`
- `--role-query-field`
- `--role-key-field`

## Validation

Report:

- setup task codes used
- user creation status
- assigned `Application Implementation Consultant`, `IT Security Manager`, and `Application Diagnostic Administrator` roles
- active user status
