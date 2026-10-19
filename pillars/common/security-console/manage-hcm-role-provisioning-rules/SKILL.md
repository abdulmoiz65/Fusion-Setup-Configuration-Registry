---
skill_id: "common.security-console.manage-hcm-role-provisioning-rules"
name: "Manage HCM Role Provisioning Rules"
description: "Prepare HCM role-provisioning-rule creation, updates, deletion and redesign from user requirements or FSM templates; validate and import supported changes through Data Loader."
layer: "pillar"
pillar: "Common"
task_code: "PER_MANAGE_HCM_ROLE_PROVISIONING_RULES"
task_name: "Manage HCM Role Provisioning Rules"
parent_skill_id: "common.security-console"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "FSCR Security team"
version: "0.2.0"
inputs:
  - "project_id"
  - "source_environment"
  - "target_environment"
  - "requested_operation"
  - "hcm_role_provisioning_rule_scope"
  - "setup_archive"
  - "user_input_file"
  - "execution_approval"
outputs:
  - "manage-hcm-role-provisioning-rules-export"
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
    default_location: "project/{project_id}/exports/common/security-console/manage-hcm-role-provisioning-rules/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/common/security-console/manage-hcm-role-provisioning-rules/current/"
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
  - "Verified Functional Setup Manager privileges to export the Manage HCM Role Provisioning Rules setup task."
  - "Verified target-environment privileges to upload and initiate the approved FSM archive through Data Loader."
---

# Manage HCM Role Provisioning Rules

## Purpose

Provide a controlled, cross-pillar method to export, validate, and
approval-gate the import of the **Manage HCM Role Provisioning Rules** FSM
setup task. Delegate transport and live import execution to the declared shared
and core dependencies. Prepare user-requested rule changes against the supported template.

Export and move the FSM setup task **Manage HCM Role Provisioning Rules** only
through the declared dependency workflows. The catalog identity is task code
`PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`; require a current catalog or live-task
lookup to confirm that its export/import flags remain supported before execution.

## Scope and boundaries

- Support a task-level FSM CSV export and the subsequent import of either the
  exact export, a user-supplied fresh FSM archive for this task, or a modified
  copy of an export or a verified-template candidate. Revalidate every change.
- This task governs HCM role-provisioning rules. Do not substitute a **Manage
  Job Roles** archive or use this skill to create, update, or redesign job,
  abstract, duty, or data roles, role memberships, security profiles, or data
  security policies. Route individual role changes to Manage Job Roles or
  Manage Duties, and policy changes to Manage Data Security Policies. This skill
  accepts create, update, delete and redesign operations for provisioning rules.
- Do not call Fusion, OAuth, UCM, REST, FSM, or loader commands directly.
  `shared.setup-export.task-level-export` owns export; `core.data-loader`
  owns every import preflight, upload, initiation, and monitoring route.
- Treat a changed archive, source scope, target environment, or validation
  result as a new request that must pass all gates again.

## Required preflight

1. Resolve the project workspace, requested operation, source and target
   environments, and the exact role-provisioning-rule scope. Require source and
   target to be distinct for a migration request; require explicit confirmation
   for a same-environment restore.
2. Confirm the exact task name and code with
   `shared.setup-export.task-level-export` and verify its current
   `CSVExportImportSupportedFlag` is `Y`. If the task is ambiguous, unavailable,
   or unsupported, record a catalog-mismatch diagnostic and stop.
3. Confirm the operator has Functional Setup Manager export access in the
   source and Data Loader import privileges in the target. Do not request or
   expose credentials, access tokens, or tenant secrets.
4. Record the source/target identities, task code, scope, and a redacted
   execution plan in the project workspace before any side effect.

## Export Manage HCM Role Provisioning Rules

1. Route the export to `shared.setup-export.task-level-export` with task name
   `Manage HCM Role Provisioning Rules`, task code
   `PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`, the source environment, and
   project ID.
2. Let that skill perform task lookup, support-flag validation, export process
   creation, polling, download, and project export persistence. Do not
   substitute a template export for a data export.
3. Preserve the returned ZIP unchanged. Register its path, SHA-256, process ID,
   task identity, source environment, and export timestamp as the export record.
4. On an export timeout or failure, preserve the task code, process ID, last
   status, process-log reference, elapsed wait, and next-check path. Do not
   start another export process automatically.

## Create, update, delete and redesign

Accept these operation requests for this task's own setup objects, including
user-specified individual changes. Prepare supported changes using the target's
FSM template and execute them through `core.data-loader`; do not reject a
request merely because the user does not already have an input archive.

Read [FSM input preparation](../references/fsm-input-preparation.md) when preparing a change or helping a user
understand the input. Obtain and safely extract the template, explain its files
and required columns, map supplied business values, and prepare a separate
candidate. Automatically authorize only the necessary template/spec export;
retain Data Loader's validation and actual import approval workflow.

For deletion, verify the explicit supported action for the exact object or
relationship. An omitted CSV row, blank value or unrelated REMOVE action is
not whole-object deletion. If the task has no supported deletion contract,
record that specific operation gap; do not impose a blanket prohibition on all
individual changes or invent a browser/API execution route.

For update or redesign, establish existing keys, preserve unrelated values and
show the intended changes. Intentional changes in the selected target are not
same-environment restores. Apply restore confirmation only to an actual restore.

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

## Validate a fresh or modified archive for import

1. Require a supplied archive to be a non-empty, readable FSM ZIP. Bind its
   SHA-256 to task code `PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`, source
   provenance when known, and target environment. A modified export is a new
   source artifact, not a continuation of the original export validation.
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
   validation result, and expected impact. Stop before the first POST.
4. Proceed only after the user gives a separate, immediate approval for that
   immutable preview. `core.data-loader` revalidates the archive and owns the
   upload, initiation, process monitoring, and diagnostics.
5. Do not retry an upload, initiation, import, overwrite, or replacement
   process without a fresh approval. Preserve returned request IDs,
   process-log references, and redacted diagnostics in the project workspace.

## Failure handling

Classify failures as input validation, catalog mismatch, authorization,
transport/environment, Fusion API, process timeout, process failed, artifact
persistence, or approval blocker. Redact credentials, tokens, customer data,
and sensitive security configuration. For any ambiguity or unsafe path, record
the blocker and recommended next action, then stop.
