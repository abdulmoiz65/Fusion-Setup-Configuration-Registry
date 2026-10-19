---
skill_id: "hcm.recruiting.recruiting-content.candidate-selection-process-reasons"
name: "Candidate Selection Process Reasons Setup Task Guidance"
description: "Authors and validates FSM CSV create and exact-code update packages for Candidate Selection Process Reasons; use for reasons, groups, translations, associations, lifecycle changes, and result reconciliation, not CSV deletion or unrelated Recruiting setup."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Content"
functional_area_code: "ORA_RECRUITING_CONTENT"
task_code: "ORA_IRC_MANAGE_CSP_REASONS"
task_name: "Candidate Selection Process Reasons"
parent_skill_id: "hcm.recruiting.recruiting-content"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
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
oracle_supplied_guidance_files:
  - purpose: "CSP reason, group, translation, association, and package validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Task-wide export and exact-code reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Active-reason, existing-group, and export readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Lifecycle, identity, package, omission, and scope enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure classification, reconciliation, and terminal routing"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/candidate-selection-process-reasons/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/candidate-selection-process-reasons/current/"
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

# Candidate Selection Process Reasons Setup Task Guidance

## Purpose

Authors and validates task-scoped FSM CSV packages for reasons and reason groups used when rejecting or withdrawing candidate job applications. It supports exact-code create and update behavior, lifecycle changes, installed-language translations, reason-to-group associations, replay validation, and post-import reconciliation.

## Runtime Boundary

- Use a current approved task-wide export as the local authority for identity, status, translations, associations, metadata, and package shape.
- This skill may produce a validated authoring package and immutable handoff. It does not itself upload, submit, retry, or replay an FSM import.
- Route an approved live import through `core.data-loader`, which owns its preview, approval, submission, polling, diagnostics, and reconciliation gates.
- Never generate CSV deletion or code rename. Draft deletion is an authorized manual UI action only.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MANAGE_CSP_REASONS`
- task_name: `Candidate Selection Process Reasons`
- parent_skill_id: `hcm.recruiting.recruiting-content`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Content`
- functional_area_code: `ORA_RECRUITING_CONTENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Candidate Selection Process Reasons` under `Recruiting Content`.

Supported authoring operations are:

- create a reason or reason group as Draft or Active;
- update non-code fields by exact persisted code;
- apply Draft to Active, Active to Inactive, or Inactive to Active;
- maintain explicit installed-language translations by targeting the exact `Language` row and preserving the `SourceLang` evidenced in the current target export; the FSM migration view treats `SourceLang` as non-updateable, so never derive or change it from translation authorship;
- add or replay an exact reason-to-group association after resolving an Active reason and existing group;
- verify a supplied export or sanitized ProcessLog after an import attempt.

Unsupported operations include CSV code rename, CSV deletion, association deletion by omission, translation deletion by omission, any CSV `SourceLang` change, individual-item export assumptions, and changes to candidate-selection-process states or other downstream consumers.

## Setup Task Metadata

- Task name: `Candidate Selection Process Reasons`
- Task code: `ORA_IRC_MANAGE_CSP_REASONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

The task package uses this order:

1. `ORA_IRC_CSP_REASON` with nested `ORA_IRC_CSP_REASON_TRANSLATION`.
2. `ORA_IRC_CSP_REASON_GROUP` with nested `ORA_IRC_CSP_REASON_GROUP_TRANSLATION`.
3. `ORA_IRC_CSP_REASON_USAGE`.

Preserve `ASM_SETUP_CSV_METADATA.xml` and all five CSV members. Unrelated members may be header-only; omission of unrelated rows is not deletion.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Content`
- Setup task name: `Candidate Selection Process Reasons`
- Setup task code: `ORA_IRC_MANAGE_CSP_REASONS`




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

Use the parent functional-area skill `hcm.recruiting.recruiting-content` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

The source-backed task graph and rule details are compiled from the files below:

- [Input validation](ora-resource/ora_input_validation.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
