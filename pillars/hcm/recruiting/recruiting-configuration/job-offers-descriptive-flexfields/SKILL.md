---
skill_id: "hcm.recruiting.recruiting-configuration.job-offers-descriptive-flexfields"
name: "Job Offers Descriptive Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Job Offers Descriptive Flexfields under the Recruiting Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
task_code: "ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD"
task_name: "Job Offers Descriptive Flexfields"
parent_skill_id: "hcm.recruiting.recruiting-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/job-offers-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/job-offers-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Job Offers Descriptive Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Job Offers Descriptive Flexfields` under `Recruiting Configuration`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD`
- task_name: `Job Offers Descriptive Flexfields`
- parent_skill_id: `hcm.recruiting.recruiting-configuration`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Configuration`
- functional_area_code: `ORA_RECRUITING_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for Job Offer DFF / `Job Offers Descriptive Flexfields` under `Recruiting Configuration`. Resolve the fixed internal DFF code `IRC_OFFERS_DFF`; do not require a requester to supply it.

## Setup Task Metadata

- Task name: `Job Offers Descriptive Flexfields`
- Task code: `ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

### Read-only retrieval route

When the requester only asks to view, show, retrieve, or summarize the current Job Offer DFF configuration, execute the shared task-level exporter directly. Do not create a project workspace, initialize or activate a Run Book, write a plan, create a preview artifact, or invoke an import workflow before that export. Authenticate only as needed, perform one fresh export for `ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD`, retrieve the exact completed package, validate its task metadata, and return the global segments, contexts, and context-sensitive segments in business-friendly language.

Project workspace and Run Book controls apply only after a requester asks to create, update, preview, import, or deploy a DFF change. A missing or unavailable Run Book checklist category must not block a read-only export.

### Change, preview, and import route

For this task's exact DFF create or update flow, route directly through the fresh task export, task-local validation, immutable package preview, and `core.data-loader` import workflow. Do not require a project workspace or Run Book as a prerequisite for preparing or importing this task's FSM package. When the requester explicitly asks to import in the original request, treat that instruction as authorization for the validated candidate from that same run: do not pause for a second approval prompt. Preserve the required safeguards: stop on missing export evidence or ambiguous identity; record the candidate ZIP and SHA-256 in the result; reconcile the import; and require separate approval for manual Flexfield deployment.

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Configuration`
- Setup task name: `Job Offers Descriptive Flexfields`
- Setup task code: `ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.recruiting.recruiting-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

Read the relevant task-local resource before acting:

- `ora-resource/ora_input_validation.md` for request scope and target identity.
- `ora-resource/ora_dependency_readiness.md` for export, approval, deployment, and Transaction Design Studio prerequisites.
- `ora-resource/ora_reference_lookups.md` before resolving a DFF target or a value set.
- `ora-resource/ora_design_enforcement.md` and `ora-resource/ora_defaulting_rules.md` before preparing a candidate package.
- `ora-resource/ora_error_handling.md` for safe stop and disclosure behavior.
- `ora-resource/ora_rule_registry.json` when executing the task rule flow.

## Functional Boundary

This task governs only the Job Offer DFF (`IRC_OFFERS_DFF` internally) on the Job Offers Descriptive Flexfields task. It can plan and validate changes to global segments, contexts, and context-sensitive segments. Use a fresh task-level FSM export as the package authority and use FSM import only after export, preview, immutable candidate ZIP, and explicit import approval gates are satisfied.

Do not use the generic Manage Descriptive Flexfields task. Do not infer context codes, segment codes, CSV members, headers, storage columns, sequence values, value sets, translations, privileges, or deployment behavior.

Treat the following as separate operations:

- Import requires an immutable, validated candidate ZIP and an explicit import instruction for its target environment, DFF identity, operation, and target identity. When that instruction is in the original request, complete the import in the same run and report its SHA-256 fingerprint.
- Deploy Flexfield is manual intervention unless a supported automated route is separately proven; require separate approval after import reconciliation.
- Transaction Design Studio is outside this skill. A separately approved TDS rule may be required to expose Additional Info and selected DFF attributes on an Offer page.

## Supported Outcomes

Potentially supported after a fresh target export proves the package contract: retrieve the DFF definition; create or update one global segment, context, or context-sensitive segment; validate and preview an FSM package; import an explicitly approved immutable package; and reconcile the imported DFF definition.

Unsupported without a separately proven contract: generic or unrelated DFF changes, direct database or DFF REST operations, deleting a context, deleting or disabling a segment, changing protected definitions, maintaining value-set values, TDS changes through the DFF package, and automatic retry after a failed or uncertain outcome.

Return business-facing result categories such as `ALREADY_EXISTS`, `NOT_FOUND`, `AMBIGUOUS_TARGET`, `INVALID_VALUE_SET`, `STALE_PREVIEW`, `AUTH_REQUIRED`, `BLOCKED`, `PROCESS_FAILED`, `OUTCOME_UNCERTAIN`, or `MANUAL_INTERVENTION_REQUIRED` as applicable. Do not expose paths, ZIP members, server IDs, request IDs, raw diagnostics, or credentials.

## Evidence and Approval Gates

Before any Create, Update, Import, or Deploy path is executable, require one exact effective-catalog match, a fresh successful export from the exact target environment and release, validated package metadata and member inventory, proven CSV identities and keys, and a rule that preserves unrelated package content unchanged. An Import path also requires that the original request explicitly directs import to the selected environment; it does not require a second approval after validation.

Authoring or preview alone does not authorize a live mutation. Follow core.data-loader approval rules and the requester's explicit execution instructions for the current validated load. Stop on missing evidence, target drift, an access failure, a failed process, or an uncertain result; do not retry automatically. If export submission did not yield a durable process ID, reconcile the matching completed task export and its metadata before reporting an error or creating another export.
## Fresh-export recovery

OAuth success without a returned ProcessId is not a completed export. Retain the
original submission receipt and use the shared task-level export workflow and its
FSM engine to reconcile the original task process. Download the exact completed
package and verify its task, environment and timestamp before continuing.

Do not submit a second export to recover a missing local result. If no unique
original process can be established, return OUTCOME_UNCERTAIN with the retained
evidence. Existing-process polling/download belongs to the shared exporter; this
pillar must not add an alternate export client or a mandatory per-run export helper.

## Package preparation and verification

Use the existing reference lookups to interpret the export, defaulting rules for
new-row defaults, and design enforcement for exact candidate comparisons. These
are agent-assisted steps in the shared export/validation/core Data Loader workflow;
no skill-local runtime or custom package helper is required.

During core.data-loader Task Hook validation, evaluate the existing completed
baseline and final candidate locally using internal validate_import. Do not start
another export or make value-set calls when the value set is unchanged. For a new
context-sensitive character segment, retain the explicit context, identity, column,
sequence and exact value set; disclose any presentation defaults from a verified
compatible peer. Reconcile import and re-export before reporting success.
