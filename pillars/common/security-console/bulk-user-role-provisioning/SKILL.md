---
skill_id: "common.security-console.bulk-user-role-provisioning"
name: "Bulk User Role Provisioning"
description: "Prepares Oracle Fusion User/UserRole HDL sources, resolves missing role codes and person numbers through core REST services, and delegates approved HDL import, status, and LDAP follow-up to the owning core and Common-pillar skills."
layer: "pillar"
pillar: "Common"
type: "import"
execution_mode: "hybrid"
owner_team: "FDOS Security team"
version: "1.0.3"
inputs:
  - "project_id"
  - "target_environment"
  - "user_role_source"
  - "data_set_name"
  - "file_action"
  - "execution_approval"
  - "request_id_for_status"
  - "completion_override"
outputs:
  - "validated_hdl_package"
  - "role_code_resolution"
  - "person_number_resolution"
  - "data_load_execution_result"
  - "data_load_status"
  - "ldap_job_handoff"
  - "final_completion_state"
  - "diagnostics"
depends_on:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "common.security-console.user-security-common"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
state_updates:
  - "validation_results"
  - "reports"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/common/security-console/bulk-user-role-provisioning/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
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
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Creates a staged immutable HDL ZIP from a validated plain-text source after user validation."
  - "Requests read-only role, person, and worker lookups through core.fusion-api.rest-api-client when source identifiers are incomplete."
  - "Requests core.data-loader to execute an explicitly approved HDL import."
  - "Requests user approval for required LDAP jobs after a successful data load."
required_privileges:
  - "Privileges required by core.data-loader for the selected HCM Data Loader operation."
  - "Read access to Fusion role, person, and worker resources when identifier resolution is required."
---

# Bulk User Role Provisioning

## Purpose and service ownership

Use this Common-pillar Security Console skill for controlled bulk User/UserRole HDL
provisioning. It owns source preparation, validation checkpoints, and
cross-skill handoff records. It never calls Fusion REST, a loader script, or an
HDL adapter directly.

Use core.fusion-api.rest-api-client for every read-only role, person, or worker
lookup. That core skill owns the OAuth-backed REST client, REST version header,
query encoding, pagination, retries, and response handling. Use core.data-loader
for every upload, data-set initiation, import/load status, and diagnostics.

## Cross-Pillar Catalog Scope

This Common skill is an HDL provisioning workflow, not a single FSM setup
task. It intentionally has no singular `task_code`; record the User/UserRole
business-object scope in its project artifacts rather than inventing a setup
task identity.

## Change scope and input assistance

Accept create, update and delete requests for User/UserRole records only when
the live HDL business-object contract supports the requested operation.
Removing a user-role assignment is not deletion of the role definition. Route
custom-role creation, updates, deletion and redesign to Manage Job Roles or
Manage Duties through `common.security-console`.

If users do not understand the HDL input, delegate sample/template generation
to `core.data-loader`, explain its User/UserRole fields and map the requested
values. Preserve unspecified fields and unrelated assignments. Use HDL
metadata here; do not substitute an FSM CSV template or invent DELETE support.

## Source preparation

Accept one readable HDL ZIP or plain-text User/UserRole DAT source.

| Source | Required action |
| --- | --- |
| Valid HDL ZIP | Preserve its bytes exactly. Do not unzip, rezip, rename, or recreate it. |
| Valid DAT | Create a separate staged ZIP and retain the original unchanged. |
| Repairable text | Normalize UTF-8, remove a UTF-8 BOM, normalize LF line endings, and retain a DAT member name. |
| Corrupt ZIP or unrecoverable HDL | Stop before upload and state the exact correction required. |

Validate User/UserRole metadata, record field counts, supported operations, and
the required user and role keys. Do not invent, delete, merge, or alter user
identifiers, role identifiers, or operations. Do not perform role membership,
user existence, or User Roles list preflight.

## Role and person resolution

When a source supplies a role display name instead of a role code, ask
core.fusion-api.rest-api-client to retrieve the role metadata. Accept only one
exact display-name match with a nonempty returned role code. For an exact set of
matches, create a staged copy that changes only verified role identifier values
and present the role-name-to-code mapping for user validation. For zero or
multiple matches, present the resolved rows and ask the user for the intended
role code.

When a required person number is absent, use core.fusion-api.rest-api-client to
retrieve the person by exact username. If that response cannot provide a
contract-valid person number, ask the same core client to perform the Workers
fallback linked only by the verified Person ID. Accept one nonempty PersonNumber
only when it belongs to that exact Person ID. Never substitute a Person ID,
partial match, name, email, organization, or closest match for a PersonNumber.
If no exact PersonNumber can be obtained, show the retrieved person details and
ask the user to provide the number.

Never edit the supplied source in place. Keep staged files and identity
responses transient. Do not persist user records, person identifiers, or
user-to-role mappings in project artifacts.

## Approval and core Data Loader handoff

Before import, confirm the target environment, source checksum, source
validation, identifier-resolution result, file action, required privileges, and
user validation of any staged conversion. Pass the validated immutable artifact
to the core.data-loader session for validation and its final preview. The
session owns execution approval, including its supported request-specific
auto-approval behavior; do not request a separate approval before the handoff.

Core data-loader performs the dependent HDL upload and data-set initiation
sequence, carries returned identifiers forward, and returns the accepted data
load result. Retain only a redacted handoff with the environment, checksum,
data-set name, Content ID, and Request ID.

On an explicit status, progress, result, count, or error request, pass the
saved Request ID to core.data-loader and return its complete status report.
Do not poll automatically, infer another request ID, or retry an import.

## LDAP completion handoff

After core.data-loader reports a terminal successful load with no failed
objects, prompt the user to run Send Pending LDAP Requests followed by Retrieve
Latest LDAP Changes through common.security-console.user-security-common. That
skill owns the ESS approval, active-instance check, submission, monitoring, and
diagnostics.

Keep a redacted LDAP handoff containing each job name, returned ESS request ID,
last status, and diagnostic reference. On a later explicit status request,
route those saved identifiers to user-security-common; do not query or poll ESS
directly.

The task is complete only when the HDL load and both LDAP jobs succeed. If a
job is pending, timed out, failed, or not approved, report the task as
incomplete. An explicit user completion override is recorded as manually
overridden, not fully verified.

## Failure behavior

- Stop before side effects on invalid source, ambiguous identity resolution,
  missing privilege, missing approval, or inconsistent target environment.
- Let core services classify authentication, transport, Fusion API, timeout,
  and process failures. Do not add a duplicate retry or polling loop.
- Preserve redacted diagnostics and give the next corrective action.
