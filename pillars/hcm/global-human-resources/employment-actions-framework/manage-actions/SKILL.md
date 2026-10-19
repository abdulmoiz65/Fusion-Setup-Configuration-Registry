---
skill_id: "hcm.global-human-resources.employment-actions-framework.manage-actions"
name: "Manage Actions Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Actions under the Employment Actions Framework functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Employment Actions Framework"
functional_area_code: "ORA_EMPLOYMENT_ACTIONS_FRAMEWORK"
task_code: "PER_MANAGE_ACTIONS_AND_REASONS"
task_name: "Manage Actions"
parent_skill_id: "hcm.global-human-resources.employment-actions-framework"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "Actions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
oracle_supplied_guidance_files:
  - purpose: "Operation-specific action and association validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Action, association, and reference readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact action and related reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting and omitted-value preservation"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Data Loader route, preview, approval, and reconciliation enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Read and Data Loader failure handling"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/employment-actions-framework/manage-actions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/employment-actions-framework/manage-actions/current/"
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

# Manage Actions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Actions` under `Employment Actions Framework`.

## Task Overview

Use this task to plan and govern `Manage Actions` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_ACTIONS_AND_REASONS` — Manage Actions.
- **Scope:** HCM → Global Human Resources → Employment Actions Framework.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `Actions`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_ACTIONS_AND_REASONS`
- task_name: `Manage Actions`
- parent_skill_id: `hcm.global-human-resources.employment-actions-framework`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Employment Actions Framework`
- functional_area_code: `ORA_EMPLOYMENT_ACTIONS_FRAMEWORK`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `Actions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Actions` under `Employment Actions Framework`.

## Setup Task Metadata

- Task name: `Manage Actions`
- Task code: `PER_MANAGE_ACTIONS_AND_REASONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `Actions`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `Actions` as the BusinessObject.

## CRUD and Reference Routing

- Read `hrActions` by `ActionCode` for a supplied code and by `ActionName` for a supplied display name. For an explicit name contains search, use `q=ActionName like '%term%'`. After one exact match, include its current `actionReasonUsages` for full details.
- For a read, complete every applicable resolver and return the final result in the same turn; do not pause at an intermediate lookup.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run every applicable declared read and task rule in graph order. When the graph returns `ACT.LOADER_READY`, invoke `core.data-loader` with the task metadata, project context, `Actions`, operation, and resolved business values. Keep control until Core returns the immutable ZIP preview; do not pause at an intermediate step. Then wait for standalone `approve`; ask only for unresolved business input.
- Do not issue mutating Fusion REST calls.

## Action and Association Authoring Rules

- Require explicit `read`, `create`, `edit`, or `delete` intent. For create, collect Action Code, Action Type, name, effective dates, applicable country, and only those requested action-reason, role, or assignment-status associations. For edit or delete, resolve one exact current action or association and require an explicit delta or delete intent.
- Require a unique Action Code for create, one exact current action or association for edit or delete, and dates where End Date does not precede Start Date. Use only fields, keys, and row shapes supported by the registered `Actions` Data Loader object.
- Resolve Country, Action Type, Action Reason, assignment status, and role references exactly before XLSX preparation. Retain only the transient stored values needed by the registered object; do not infer a Country code or select by result position.
- Change an action-reason effective date only on its matching action-reason usage row. Preserve unrelated rows, omitted fields, and unchanged associations.
- For a copy request, create a new Action Code and copy only the explicitly requested parent values and child associations. Do not clone omitted source associations, translations, DFF rows, generated IDs, or audit values; place the new parent and requested usage rows in the same reviewed workbook.
- For an action-reason role mapping, require the exact action and action-reason parents, a compatible Action Type, and one active exact role. Use the registered-object-supported mapping shape; do not invent generated IDs, grouping keys, or field values.
- Before Data Loader submission, show the exact target, requested delta, preserved rows, resolved references, XLSX source fingerprint, immutable preview, and reconciliation plan. Any changed target, source, metadata subset, or preview requires renewed approval.
- Data Loader is the only mutation route. Do not substitute Fusion REST, FSM import, CSV omission, or an automatic retry for create, edit, or delete.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Employment Actions Framework`
- Setup task name: `Manage Actions`
- Setup task code: `PER_MANAGE_ACTIONS_AND_REASONS`




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

Use the parent functional-area skill `hcm.global-human-resources.employment-actions-framework` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
