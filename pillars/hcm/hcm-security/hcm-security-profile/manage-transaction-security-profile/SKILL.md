---
skill_id: "hcm.hcm-security.hcm-security-profile.manage-transaction-security-profile"
name: "Manage Transaction Security Profile Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Transaction Security Profile under the HCM Security Profile functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Security"
functional_area: "HCM Security Profile"
functional_area_code: "ORA_HCM_SECURITY_PROFILE"
task_code: "ORA_PER_MANAGE_TRANSACTION_SECURITY_PROFILE"
task_name: "Manage Transaction Security Profile"
parent_skill_id: "hcm.hcm-security.hcm-security-profile"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm security pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-security-profile/manage-transaction-security-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-security-profile/manage-transaction-security-profile/current/"
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

# Manage Transaction Security Profile Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Transaction Security Profile` under `HCM Security Profile`.

## Setup Task Skill Contract

- task_code: `ORA_PER_MANAGE_TRANSACTION_SECURITY_PROFILE`
- task_name: `Manage Transaction Security Profile`
- parent_skill_id: `hcm.hcm-security.hcm-security-profile`
- pillar: `HCM`
- offering: `HCM Security`
- functional_area: `HCM Security Profile`
- functional_area_code: `ORA_HCM_SECURITY_PROFILE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Transaction Security Profile` under `HCM Security Profile`.

## Sample Prompt Usage

1. Use manage-transaction-security-profile skill to view all transaction security profiles.
2. Use manage-transaction-security-profile skill to summarize the properties of all transaction security profiles.
3. Use manage-transaction-security-profile skill to create a new transaction security profile called View Talent Profiles with view all disabled for family HCM, category code HRR, and sub-category code HRT.
4. Use manage-transaction-security-profile skill to create a new transaction security profile called View GHR All with view all disabled for family HCM, category value as Global Human Resources, and sub-category code as ALL.
5. Use manage-transaction-security-profile skill to create a new transaction security profile called ExcludeAOREmployment with view all disabled for family HCM, category value as Global Human Resources, and sub-category values as Responsibility,Employment and the subcategories are excluded.
6. Use manage-transaction-security-profile skill to delete transaction security profile New Security Profile.

## Setup Task Metadata

- Task name: `Manage Transaction Security Profile`
- Task code: `ORA_PER_MANAGE_TRANSACTION_SECURITY_PROFILE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `HCM Security`
- Functional area / Setup Object: `HCM Security Profile`
- Setup task name: `Manage Transaction Security Profile`
- Setup task code: `ORA_PER_MANAGE_TRANSACTION_SECURITY_PROFILE`


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

Use the parent functional-area skill `hcm.hcm-security.hcm-security-profile` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Transaction Security Profile Validation

Apply the task-local resource guidance before previewing, exporting, importing, or validating a transaction security profile:

- Supported security-profile operations are read, add, and update only. Deleting an existing security profile is not supported.
- When `View All` is enabled, ignore `Family`, `Category`, and `Subcategory`; do not validate or persist those scoped values for this request.
- When `View All` is not enabled, require `Family`. `Category` and `Subcategory` are optional, but a supplied `Subcategory` requires a supplied `Category`.
- Resolve a supplied Category value to its corresponding Category Code for the selected Family before validating the supported-combination catalog. Resolve each supplied Subcategory value to its corresponding Subcategory Code for the resolved Family and Category Code before validation. A supplied code may be retained when it exactly identifies the same returned value.
- For a scoped request, validate against the task-local supported-combination catalog: a supplied `Family` must match at least one catalog row; supplied `Family` and `Category` must match at least one row; and each supplied comma-separated `Subcategory` must match an exact catalog row for that Family-and-Category combination. An absent match is blocking.
- A case-insensitive `Subcategory` value of `ALL` is valid only with a catalog-supported `Family` and `Category`, and must be the only supplied subcategory value. For a profile created with this value, include every supported subcategory for that Family-and-Category combination.
- The supported-combination catalog is maintained in the task-local reference guidance; validation is fully local to the task guidance.

Read [input validation](ora-resource/ora_input_validation.md), [reference lookups](ora-resource/ora_reference_lookups.md), and [error handling](ora-resource/ora_error_handling.md) as the task-level source of truth.
