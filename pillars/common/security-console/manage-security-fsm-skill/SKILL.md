---
skill_id: "common.security-console.manage-security-fsm-skill"
name: "Manage Security FSM Skill"
description: "Plans and safely routes cross-pillar Oracle Fusion Security Console role management and Manage Job Roles setup-data export or import. Use for validated role-design assessment, manual Security Console guidance, and approval-gated FSM routing."
layer: "pillar"
pillar: "Common"
task_code: "ASXS_MANAGE_JOB_ROLES"
task_name: "Manage Job Roles"
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
version: "0.2.1"
inputs:
  - "implementation_objective"
  - "project_id"
  - "target_environment"
  - "requested_operation"
  - "role_design_artifact"
  - "role_scope"
  - "setup_data_artifact"
  - "execution_approval"
outputs:
  - "security-role-management-plan"
  - "role-design-validation-result"
  - "fsm-export-routing-plan"
  - "validated-fsm-import-plan"
  - "approval-preview"
  - "execution-audit"
  - "diagnostics"
  - "skill-run-record"
  - "token-usage-record"
depends_on:
  - "common.security-console.user-security-common"
  - "common.security-console.manage-job-roles"
  - "common.security-console.manage-duties"
  - "common.security-console.manage-data-security-policies"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
uses_core:
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
state_updates:
  - "scope"
  - "design_decisions"
  - "validation_results"
  - "exports"
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
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/common/security-console/manage-security-fsm-skill/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/common/security-console/manage-security-fsm-skill/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Role-management input and scope validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency, documentation, defaulting, design, and error controls"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Official reference lookup boundaries"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Fail-closed defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Role-design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Diagnostics and recovery rules"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Repository-authored routing guidance; current Oracle documentation must be verified by the active approved workflow."
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May route approved export or import execution to owning shared/core skills; this skill performs no direct Fusion mutation."
required_privileges:
  - "Verified Security Console access appropriate to the requested role-management scope."
  - "Verified Functional Setup Manager export/import access when export or import is requested."
---

# Manage Security FSM Skill

## Purpose and routing

Provide cross-pillar planning, assessment, and controlled routing for Security Console role management and the FSM catalog task **Manage Job Roles**. Read `ora-resource/ora_*.md` before producing a preview or handoff. Route Security Console common controls through `common.security-console.user-security-common`, task-level export only through `shared.setup-export.task-level-export`, validation only through `shared.validation.setup-data-validator`, and task-level FSM CSV input preparation and import through `common.security-console.manage-job-roles`, with `core.data-loader` as its executor.

## Catalog identity and scope

Use `knowledge/setup-task-catalog/effective/setupTasksAll.json` only as a dependency and reference. Catalog identity: task name `Manage Job Roles`; task code `ASXS_MANAGE_JOB_ROLES`; `AvailableFlag`, `ExportImportSupportedFlag`, and `CSVExportImportSupportedFlag` are `Y`. Its purpose is to review, create, or update enterprise-wide abstract and job roles and create role hierarchies. These facts do not authorize an endpoint, transport, loader, or mutation route.

## Supported operations

- Assess a supplied role design; produce a role hierarchy and duty-role mapping plan; identify segregation-of-duties, excessive-privilege, and least-privilege concerns.
- Accept role creation, update, deletion and redesign requests and delegate supported FSM preparation/execution to the focused owner: Manage Job Roles for custom job/abstract roles, Manage Duties for duty roles, and Manage Data Security Policies for policy changes.
- Use [FSM input preparation](../references/fsm-input-preparation.md) to help extract a template and map plain-language requirements. Provide manual guidance only when the user requests it or no supported FSM operation exists; do not default supported changes to manual completion.
- Route export, archive validation, and import only through the declared dependency workflows. Import requires their validation evidence, immutable archive, and separate approval.

## Explicit execution boundaries

This planning skill delegates creation, updates, deletion, redesign and import to the focused FSM/Data Loader workflow; it does not perform direct mutations itself. Never infer REST, HDL, SCIM, FBDI, ESS, direct API, OAuth, HTTP, CSV parsing, polling, or loader behavior from catalog flags. Do not invent a role name, code, privilege, duty assignment, data-security policy, scope, archive content, or mutation route. Mark unsupported, ambiguous, or undocumented paths `TBD` and stop safely. Treat seeded roles and privileges as protected unless current Oracle guidance and the approved design explicitly permit the action.

## Required inputs and validation

Require only the manifest inputs applicable to the selected operation; a user need not supply an archive or understand its CSV template to request a change. Before planning a mutation preview or an FSM import, require an approved role-design artifact, exact role identity and classification, requested scope and hierarchy impact, target-environment identity, required Security Console privileges, and any applicable duty, privilege, or data-security changes. Validate import archives only through approved shared/core workflow; require the immutable ZIP hash and exact task identity `ASXS_MANAGE_JOB_ROLES`.

## Preflight

Before any delegated export, validation, or import action, confirm the project
workspace, requested operation, task identity, target environment, required
privileges, and all applicable dependency inputs. For an import handoff, confirm
the immutable archive hash and validation evidence. The focused owner and Core
Data Loader then validate and display the final session preview; missing
execution approval must not prevent that validation-only handoff. Core Data
Loader owns approval immediately before live import. Fail closed on an ambiguous
role scope, task identity, environment, archive, or validation result and record
a redacted diagnostic. Missing approval blocks execution at the owning session.

## Role-design safeguards

Classify each role as job, abstract, duty, or data role; document inheritance, duty mapping, data-security scope, owners, and affected users. Flag duplicate-role risk, excessive privilege, unsupported duty or privilege changes, missing SoD review, and violations of least privilege. This skill may recommend manual review, never synthesize missing security design details.

## FSM export and import workflow

1. Confirm catalog identity and exact requested scope; route export to `shared.setup-export.task-level-export`.
2. Preserve the returned setup-data artifact and use `shared.validation.setup-data-validator` plus the import workflow’s checks.
3. For role input preparation or import, delegate to `common.security-console.manage-job-roles`; its shared validator and Core Data Loader own archive checks, Task Hook validation, approval, transport and diagnostics.
4. Require shared/core validation evidence bound to an immutable ZIP hash, exact task identity, target environment, and explicit import preview. A changed archive, scope, environment, or validation result restarts the gate.

## Approval gates

Core Data Loader owns the import execution approval and its supported
request-specific auto-approval behavior. Do not add an approval before its
validation/preview handoff. Its preview identifies the exact target environment,
operation, immutable archive, validation evidence and impact. Retry, replacement,
overwrite and deletion follow the owning workflow's approval and recovery rules;
prior approval never authorizes a changed payload. Export follows the owning
workflow's approval rules.

## Error handling and diagnostics

Classify failures as `input_validation`, `catalog_mismatch`, `auth/authz`, `transport/environment`, `Fusion API`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`. Do not retry a mutation, import, or failed background process without idempotency evidence or fresh approval. On timeout or failure, preserve permitted redacted status evidence, task code, process/request identifier, last status, elapsed time, artifact references, and safe next action. Redact credentials, tokens, customer data, sensitive role assignments, and security-policy details.

## Workspace persistence and token tracking

Persist plans, validation results, previews, audits, and diagnostics under `project/{project_id}/artifacts/pillars/common/security-console/manage-security-fsm-skill/current/`; register/version them through the declared project-management dependencies. Persist every durable run under `project/{project_id}/state/runs/`. Append token usage only to `project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md` using the manifest fields. Repository authoring alone does not create a project workspace.

## Golden scenarios

| Scenario | Expected result |
|---|---|
| Assess supplied job-role design | Return hierarchy, duty mapping, least-privilege and SoD findings; identify missing evidence without inventing mappings. |
| Request role creation, update, deletion or redesign | Route to the focused owner; prepare supported FSM input and use Data Loader validation and approval. |
| User cannot fill an input template | Obtain and safely extract the task template, explain fields and map the supplied requirements. |
| Explicitly request manual guidance | Provide guidance; do not execute a browser change. |
| Export Manage Job Roles setup data | Confirm task identity and route only to `shared.setup-export.task-level-export`. |
| Import an immutable validated archive | Verify task identity, ZIP hash and shared/core evidence; hand off to Manage Job Roles and Core Data Loader, which owns final preview and execution approval. |
| Request a direct REST/SCIM route | Mark `TBD` and stop; catalog flags do not establish that route. |
