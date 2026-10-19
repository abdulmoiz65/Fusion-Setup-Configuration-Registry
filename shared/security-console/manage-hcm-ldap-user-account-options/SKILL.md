---
skill_id: "shared.security-console.manage-hcm-ldap-user-account-options"
name: "Manage HCM LDAP User Account Options"
description: "Legacy compatibility alias that immediately redirects every invocation to its matching Common-pillar Security Console skill."
layer: "shared"
pillar: "Common"
type: "orchestration"
execution_mode: "assisted"
owner_team: "FSCR Security team"
version: "0.1.2"
inputs:
  - "project_id"
  - "source_environment"
  - "target_environment"
  - "requested_operation"
  - "hcm_ldap_user_account_option_scope"
  - "setup_archive"
  - "user_input_file"
  - "execution_approval"
outputs:
  - "manage-hcm-ldap-user-account-options-export"
  - "import-template-export"
  - "input-file-conformance-result"
  - "corrected-input-file"
  - "archive-validation-result"
  - "import-approval-preview"
  - "data-load-execution-result"
  - "diagnostics"
  - "skill-run-record"
  - "token-usage-record"
depends_on:
  - "common.security-console.manage-hcm-ldap-user-account-options"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
uses_core:
  - "core.data-loader"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
state_updates:
  - "scope"
  - "exports"
  - "validation_results"
  - "token_usage_records"
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
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/common/security-console/manage-hcm-ldap-user-account-options/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/shared/security-console/manage-hcm-ldap-user-account-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "FSM archive and task identity validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Import dependency and same-environment restore checks"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Immutable preview and Data Loader route enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Approval, retry, and diagnostic controls"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Repository-authored task validation guidance; current Oracle documentation and the active Fusion contract remain authoritative."
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May route an approved task-level export to the shared export skill."
  - "May route an approved immutable FSM archive to core.data-loader for upload and import."
required_privileges:
  - "Verified Functional Setup Manager privileges to export the Manage HCM LDAP User Account Options setup task."
  - "Verified target-environment privileges to upload and initiate the approved FSM archive through Data Loader."
---

# Manage HCM LDAP User Account Options

## Legacy compatibility redirect

This legacy shared skill ID is a compatibility alias. On every invocation,
Tell the caller to use the Common-pillar successor identified below; do not accept
the legacy shared skill as an execution route.
immediately route to `common.security-console.manage-hcm-ldap-user-account-options` at
`pillars/common/security-console/manage-hcm-ldap-user-account-options/SKILL.md`
and use that pillar skill's instructions exclusively. Do not perform validation,
artifact creation, Fusion access, or any other workflow defined below.

## Purpose

Provide a controlled, cross-pillar method to export, validate, and
approval-gate the import of the **Manage HCM LDAP User Account Options** FSM
setup task. Delegate transport and live import execution to the declared shared
and core dependencies; do not design or change account-option values here.

Export and move the FSM setup task **Manage HCM LDAP User Account Options**
only through the declared dependency workflows. The catalog identity is task
code `PER_HCM_LDAP_USER_ACCOUNT_OPTIONS`; require a current catalog or
live-task lookup to confirm that its export/import flags remain supported before
execution.

## Scope and boundaries

- Support only a task-level FSM CSV export and the subsequent import of the
  exact exported (or otherwise supplied) archive for this task.
- Do not create, update, delete, or redesign individual user accounts, job
  roles, role memberships, LDAP integrations, or security policies. Route that
  work to `shared.security-console.user-security-common` or the applicable
  dedicated role-management skill.
- A Job Roles archive is not an archive for this task. Reject it as a
  task-identity mismatch; do not reinterpret or transform it.
- Do not call Fusion, OAuth, UCM, REST, FSM, or loader commands directly.
  `shared.setup-export.task-level-export` owns export; `core.data-loader`
  owns every import preflight, upload, initiation, and monitoring route.
- Treat a changed archive, source scope, target environment, or validation
  result as a new request that must pass all gates again.

## Required preflight

1. Resolve the project workspace, requested operation, source and target
   environments, and the exact HCM LDAP user-account-options scope. Require
   source and target to be distinct for a migration request; require explicit
   confirmation for a same-environment restore.
2. Confirm the exact task name and code with
   `shared.setup-export.task-level-export` and verify its current
   `CSVExportImportSupportedFlag` is `Y`. If the task is ambiguous, unavailable,
   or unsupported, record a catalog-mismatch diagnostic and stop.
3. Confirm the operator has Functional Setup Manager export access in the
   source and Data Loader import privileges in the target. Do not request or
   expose credentials, access tokens, or tenant secrets.
4. Record the source/target identities, task code, scope, and a redacted
   execution plan in the project workspace before any side effect.

## Export Manage HCM LDAP User Account Options

1. Route the export to `shared.setup-export.task-level-export` with task name
   `Manage HCM LDAP User Account Options`, task code
   `PER_HCM_LDAP_USER_ACCOUNT_OPTIONS`, the source environment, and project ID.
2. Let that skill perform the task lookup, support-flag validation, export
   process creation, polling, download, and project export persistence. Do not
   substitute a template export for a data export.
3. Preserve the returned ZIP unchanged. Register its path, SHA-256, process ID,
   task identity, source environment, and export timestamp as the export record.
4. On an export timeout or failure, preserve the task code, process ID, last
   status, process-log reference, elapsed wait, and next-check path. Do not
   start another export process automatically.

## Template-first import preparation

1. Unless the user explicitly overrides this sequence, export the task first
   and provide that export as the import template before asking for import
   content. Explain that the template establishes the supported archive and
   file structure; it is not approval to import.
2. When the user provides an input file, compare it with the export template
   for file names, headers, column order, encoding, required values, and
   task-specific references. Help correct structural defects in a separate
   candidate file; preserve the supplied original and do not silently alter
   business values.
3. Give the user a concise change summary and identify any unresolved values
   or references. Use the corrected file only after it conforms to the export
   structure and has been assembled into a new candidate archive using the
   supported archive shape. That candidate is a new artifact and must pass the
   validation and approval gates below.
4. The user may override the export-first sequence, template choice, or
   proposed file corrections at any time. Honor that direction, while retaining
   the required task-identity, validation, and immediate import-approval gates.

## Validate the archive for import

1. Require the supplied archive to be a non-empty ZIP and bind its SHA-256 to
   task code `PER_HCM_LDAP_USER_ACCOUNT_OPTIONS`, source environment, and target
   environment.
2. Route setup-data validation to `shared.validation.setup-data-validator` and
   preserve the resulting validation evidence. Fail closed on archive-shape,
   task-identity, scope, catalog, environment, or privilege mismatch.
3. Do not alter, unpack-and-repack, merge, or otherwise transform the archive
   after validation. Any change invalidates the evidence and approval preview.

## Import the validated archive

1. Route the immutable validated archive to `core.data-loader` as an FSM,
   task-routed import. Provide the task context, target environment, archive
   SHA-256, and validation evidence.
2. Let `core.data-loader` complete its required source and API validation and
   produce its immutable approval preview. This skill must not bypass or replace
   the Data Loader route with a direct FSM API, UCM upload, REST call, CSV
   utility, or browser action.
3. Present the exact target environment, task code, archive name and SHA-256,
   validation result, and expected import impact. Stop before the first POST.
4. Proceed only after the user gives a separate, immediate approval for that
   immutable preview. `core.data-loader` revalidates the archive and owns the
   upload, initiation, process monitoring, and diagnostics.
5. Do not retry an upload, initiation, import, overwrite, or replacement
   process without a fresh approval. Preserve returned request IDs, process-log
   references, and redacted diagnostics in the project workspace.

## Failure handling

Classify failures as input validation, catalog mismatch, authorization,
transport/environment, Fusion API, process timeout, process failed, artifact
persistence, or approval blocker. Redact credentials, tokens, customer data,
and sensitive security configuration. For any ambiguity or unsafe path, record
the blocker and recommended next action, then stop.
