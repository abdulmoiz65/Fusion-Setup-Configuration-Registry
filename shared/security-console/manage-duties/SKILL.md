---
skill_id: "shared.security-console.manage-duties"
name: "Manage Duties"
description: "Legacy compatibility alias that immediately redirects every invocation to its matching Common-pillar Security Console skill."
layer: "shared"
pillar: "Common"
type: "orchestration"
execution_mode: "assisted"
owner_team: "FSCR Security team"
version: "0.1.2"
inputs: ["project_id", "source_environment", "target_environment", "requested_operation", "duty_scope", "setup_archive", "user_input_file", "execution_approval"]
outputs: ["manage-duties-export", "import-template-export", "input-file-conformance-result", "corrected-input-file", "archive-validation-result", "import-approval-preview", "data-load-execution-result", "diagnostics", "skill-run-record", "token-usage-record"]
depends_on: ["common.security-console.manage-duties"]
uses_core: ["core.data-loader", "core.project-mgmt.artifact-registry-manager", "core.project-mgmt.project-state-manager"]
persists_project_state: true
state_updates: ["scope", "exports", "validation_results", "token_usage_records"]
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields: ["activity_start_time", "skill_id", "task", "trigger", "artifacts_written", "files_read", "estimated_input_tokens", "estimated_output_tokens", "estimated_total_tokens", "estimation_method", "notes"]
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/common/security-console/manage-duties/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/shared/security-console/manage-duties/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud release"]
side_effects: ["May route an approved task-level export to shared.setup-export.task-level-export.", "May route an approved immutable FSM archive to core.data-loader for upload and import."]
required_privileges: ["Functional Setup Manager privileges to export Manage Duties.", "Target-environment privileges to upload and initiate the approved FSM archive through Data Loader."]
---

# Manage Duties

## Legacy compatibility redirect

This legacy shared skill ID is a compatibility alias. On every invocation,
Tell the caller to use the Common-pillar successor identified below; do not accept
the legacy shared skill as an execution route.
immediately route to `common.security-console.manage-duties` at
`pillars/common/security-console/manage-duties/SKILL.md` and use that pillar
skill's instructions exclusively. Do not perform validation, artifact creation,
Fusion access, or any other workflow defined below.

## Purpose

Provide a controlled, cross-pillar method to export, validate, and
approval-gate the import of the **Manage Duties** FSM setup task. Delegate
transport and live import execution to the declared shared and core
dependencies; do not redesign duties or role hierarchies in this skill.

Export and move FSM task **Manage Duties** only through declared dependencies.
Its catalog identity is `ASXS_MANAGE_DUTIES`; before execution, confirm a
current catalog or live-task lookup reports `CSVExportImportSupportedFlag=Y`.

## Boundaries

- Support a task-level CSV export and import of the exact export or a
  user-supplied modified derivative. A modified archive is a new artifact:
  validate, hash, preview, and approve it separately.
- Cover duty-role groupings and their provisioning to abstract, job, or other
  duty roles. Do not redesign duties, privileges, data-security policies, or
  role hierarchies; route design work to
  `shared.security-console.user-security-common`.
- Do not call Fusion, OAuth, UCM, REST, FSM, or loader commands directly.
  Task Level Export owns export; Data Loader owns import preflight, upload,
  initiation, monitoring, and diagnostics.

## Preflight

1. Resolve project, operation, source and target environments, and duty scope.
   Require separate environments for migration or explicit confirmation for a
   same-environment restore.
2. Confirm `Manage Duties` / `ASXS_MANAGE_DUTIES` and current CSV support with
   `shared.setup-export.task-level-export`. On ambiguity or unsupported status,
   record a catalog-mismatch diagnostic and stop.
3. Confirm source export and target import privileges. Never request or expose
   credentials, tokens, or tenant secrets.
4. Persist source/target identity, task code, scope, and a redacted plan before
   any side effect.

## Export

1. Route to `shared.setup-export.task-level-export` with task name `Manage
   Duties`, code `ASXS_MANAGE_DUTIES`, source environment, and project ID.
2. Let that skill discover the task, validate support, create/poll/download the
   export, and persist it. Do not substitute a template export for setup data.
3. Preserve the returned ZIP unchanged and register its path, SHA-256, process
   ID, task identity, source environment, and timestamp.
4. On timeout/failure preserve task code, process ID, last status, process-log
   reference, elapsed wait, and next-check path; do not automatically re-export.

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

## Validate and import

1. Accept a non-empty export ZIP or a user-modified derivative. Bind its
   SHA-256 to `ASXS_MANAGE_DUTIES`, source, and target. Never call it a Manage
   Job Roles archive.
2. Route validation to `shared.validation.setup-data-validator`; fail closed on
   archive shape, task identity, scope, catalog, environment, or privilege
   mismatch. Preserve validation evidence.
3. Do not alter, unpack/repack, merge, or transform the archive after
   validation. Any modification starts a new validation cycle.
4. Route the immutable validated archive to `core.data-loader` as an FSM,
   task-routed import with target identity, SHA-256, and validation evidence.
5. Let Data Loader build its immutable approval preview. Do not substitute a
   direct FSM API, UCM upload, REST call, CSV utility, or browser action.
6. Present target, task code, archive name/SHA-256, validation result, and
   expected impact; stop before the first POST. Proceed only after separate,
   immediate approval. Data Loader revalidates and owns execution thereafter.
7. Do not retry upload, import, overwrite, or replacement without fresh
   approval. Persist returned IDs, process-log references, and redacted
   diagnostics in the project workspace.

## Failures

Classify failures as input validation, catalog mismatch, authorization,
transport/environment, Fusion API, process timeout, process failed, artifact
persistence, or approval blocker. Redact credentials, tokens, customer data,
and sensitive duty or role configuration; record the blocker and safe next step.
