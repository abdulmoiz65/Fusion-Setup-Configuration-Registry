---
skill_id: "shared.security-console.manage-data-security-policies"
name: "Manage Data Security Policies"
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
  - "data_security_policy_scope"
  - "setup_archive"
  - "user_input_file"
  - "execution_approval"
outputs:
  - "manage-data-security-policies-export"
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
  - "common.security-console.manage-data-security-policies"
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
    default_location: "project/{project_id}/exports/common/security-console/manage-data-security-policies/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/shared/security-console/manage-data-security-policies/current/"
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
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud release"]
side_effects:
  - "May route an approved task-level export to the shared export skill."
  - "May route an approved immutable FSM archive to core.data-loader for upload and import."
required_privileges:
  - "Verified Functional Setup Manager privileges to export the Manage Data Security Policies setup task."
  - "Verified target-environment privileges to upload and initiate the approved FSM archive through Data Loader."
---

# Manage Data Security Policies

## Legacy compatibility redirect

This legacy shared skill ID is a compatibility alias. On every invocation,
Tell the caller to use the Common-pillar successor identified below; do not accept
the legacy shared skill as an execution route.
immediately route to `common.security-console.manage-data-security-policies` at
`pillars/common/security-console/manage-data-security-policies/SKILL.md` and
use that pillar skill's instructions exclusively. Do not perform validation,
artifact creation, Fusion access, or any other workflow defined below.

## Purpose

Provide a controlled, cross-pillar method to export, validate, and
approval-gate the import of the **Manage Data Security Policies** FSM setup
task. Delegate transport and live import execution to the declared shared and
core dependencies; do not make policy-design decisions in this skill.

Export and move the FSM setup task **Manage Data Security Policies** only through
the declared dependency workflows. Its catalog identity is
`ASXS_MANAGE_DATA_SECURITY_POLICIES`; require a current catalog or live-task
lookup to confirm that export/import remains supported before execution.

## Scope and boundaries

- Support task-level FSM CSV export and subsequent import of either the exact
  exported archive or a user-supplied modified copy.
- Do not create, update, delete, or redesign policies, roles, privileges,
  object grants, attribute-group grants, or conditions. Route design work to
  `shared.security-console.user-security-common`.
- Do not call Fusion, OAuth, UCM, REST, FSM, or loader commands directly.
  `shared.setup-export.task-level-export` owns export; `core.data-loader` owns
  import preflight, upload, initiation, and monitoring.
- A modified archive is a fresh source: calculate a new SHA-256 and repeat
  validation, preview, and immediate-approval gates. An approval for the
  original export does not approve a modified archive.

## Required preflight

1. Resolve the project workspace, requested operation, source and target
   environments, and exact policy scope. For migration, source and target must
   differ; for a same-environment restore, require explicit confirmation.
2. Confirm task name and code with `shared.setup-export.task-level-export` and
   verify `CSVExportImportSupportedFlag` is `Y`. On an ambiguous, unavailable,
   or unsupported task, record a catalog-mismatch diagnostic and stop.
3. Confirm Functional Setup Manager export access in source and Data Loader
   import privileges in target. Never request or expose credentials or tokens.
4. Persist redacted source/target, task-code, scope, and execution-plan details
   before side effects.

## Export

1. Route export to `shared.setup-export.task-level-export` with task name
   `Manage Data Security Policies`, task code
   `ASXS_MANAGE_DATA_SECURITY_POLICIES`, source environment, and project ID.
2. Let that skill complete discovery, support validation, process creation,
   polling, download, and project export persistence. Never substitute a
   template export for a data export.
3. Preserve the returned ZIP unchanged and register its path, SHA-256, process
   ID, task identity, source environment, and timestamp. Preserve timeout or
   failure diagnostics; do not automatically start another export.

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

1. Require a non-empty ZIP and bind its SHA-256 to the task code, source, and
   target. Route archive validation to `shared.validation.setup-data-validator`.
   Fail closed on archive-shape, task-identity, scope, catalog, environment, or
   privilege mismatch.
2. The ZIP must remain unchanged after validation. Do not unpack, repack, merge,
   or transform it. A user-modified copy begins a new validation cycle.
3. Route only the immutable validated archive to `core.data-loader` as an FSM,
   task-routed import, with target environment, task context, SHA-256, and
   validation evidence.
4. Let Data Loader complete source/API validation and create an immutable
   approval preview. Do not replace that route with direct FSM, UCM, REST, CSV,
   or browser operations.
5. Present the exact target, task code, archive name and SHA-256, validation
   result, and expected policy impact. Stop before the first POST. Proceed only
   after a separate, immediate approval for that unchanged preview.
6. Data Loader owns upload, initiation, monitoring, and diagnostics. Do not
   retry uploads, imports, overwrite/replacement operations, or failed jobs
   without fresh approval.

## Failure handling

Classify failures as input validation, catalog mismatch, authorization,
transport/environment, Fusion API, process timeout, process failed, artifact
persistence, or approval blocker. Redact credentials, tokens, customer data,
and sensitive policy details. Persist a redacted blocker and next action, then
stop on ambiguity or unsafe paths.

## Golden scenarios

| Scenario | Expected result |
| --- | --- |
| Export policy setup | Confirm identity and route only to task-level export. |
| Import the unmodified export | Require ZIP hash, shared/core evidence, and separate immediate approval before Data Loader handoff. |
| Import a modified exported file | Treat it as a new archive and repeat validation and approval gates. |
| Request direct FSM/UCM/REST/browser import | Stop; catalog flags do not authorize a replacement route. |
