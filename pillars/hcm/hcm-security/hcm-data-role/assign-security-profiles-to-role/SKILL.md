---
skill_id: "hcm.hcm-security.hcm-data-role.assign-security-profiles-to-role"
name: "Assign Security Profiles to Role Setup Task Guidance"
description: "Provides task-specific setup guidance for Assign Security Profiles to Role under the HCM Data Role functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Security"
functional_area: "HCM Data Role"
functional_area_code: "ORA_HCM_DATA_ROLE"
task_code: "ORA_PER_ASSIGN_SECURITY_PROFILES_TO_ROLE"
task_name: "Assign Security Profiles to Role"
parent_skill_id: "hcm.hcm-security.hcm-data-role"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
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
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-data-role/assign-security-profiles-to-role/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-data-role/assign-security-profiles-to-role/current/"
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

# Assign Security Profiles to Role Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Assign Security Profiles to Role` under `HCM Data Role`.

## Setup Task Skill Contract

- task_code: `ORA_PER_ASSIGN_SECURITY_PROFILES_TO_ROLE`
- task_name: `Assign Security Profiles to Role`
- parent_skill_id: `hcm.hcm-security.hcm-data-role`
- pillar: `HCM`
- offering: `HCM Security`
- functional_area: `HCM Data Role`
- functional_area_code: `ORA_HCM_DATA_ROLE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Assign Security Profiles to Role` under `HCM Data Role`.

## Setup Task Metadata

- Task name: `Assign Security Profiles to Role`
- Task code: `ORA_PER_ASSIGN_SECURITY_PROFILES_TO_ROLE`
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
- Functional area / Setup Object: `HCM Data Role`
- Setup task name: `Assign Security Profiles to Role`
- Setup task code: `ORA_PER_ASSIGN_SECURITY_PROFILES_TO_ROLE`

## Mandatory Live Mapping and Defaulting Gate

Before preparing or reviewing a CSV package, resolve the exact target RoleId
through rolesLOV, including `JobRole`, `AbstractRole`, `DataRole`, and
`ActiveFlag`, then call getSecurityProfileMappingsForRole. For a data role
create or update, accept the resolved inherited role only when `JobRole=true`
and `ActiveFlag=true`; otherwise stop before preview and tell the user that a
data role requires an active job role as its basis. For a direct
security-profile assignment to an existing role, the target is that role
itself and this data-role-basis restriction does not apply. Do not infer
applicable security-profile types from a predefined role, an existing data
role, or a prior CSV export.

Use the returned types as the complete list of profile rows for the package:

1. Retain an explicit user-selected profile for a returned type.
2. For every other returned type, select the matching current View All profile.
3. Stop before preview or import if a requested type is not returned, or if the
   matching View All profile is missing or ambiguous in the current
   security-profile catalog.

Persist a redacted record of the returned types, explicit selections, defaulted
View All selections, and blocked types in the project run artifact.


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

Use the parent functional-area skill `hcm.hcm-security.hcm-data-role` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
