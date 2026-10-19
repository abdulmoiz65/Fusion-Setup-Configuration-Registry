---
skill_id: "hcm.recruiting.recruiting-content.candidate-pool-management-process-configuration"
name: "Candidate Pool Management Process Configuration Setup Task Guidance"
description: "Provides task-specific setup guidance for Candidate Pool Management Process Configuration under the Recruiting Content functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Content"
functional_area_code: "ORA_RECRUITING_CONTENT"
task_code: "ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION"
task_name: "Candidate Pool Management Process Configuration"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/candidate-pool-management-process-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/candidate-pool-management-process-configuration/current/"
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

# Candidate Pool Management Process Configuration Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Candidate Pool Management Process Configuration` under `Recruiting Content`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION`
- task_name: `Candidate Pool Management Process Configuration`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Candidate Pool Management Process Configuration` under `Recruiting Content`.

## Candidate Selection Workflow Reuse

For the shared Candidate Selection workflow, invoke `hcm.recruiting.recruiting-content.candidate-selection-process-configuration` with:

```yaml
setup_task_scope:
  task_code: ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION
  task_name: Candidate Pool Management Process Configuration
  pTypeCode: POOL
```

Reuse only its common export, validation, import, and verification workflow. Retain the Candidate Pool task identity on every result. Do not apply Candidate Selection task-local registry nodes, `CSW` defaults, Offer or HR blocks, or candidate-status behavior.

## Pool package-authoring boundary

Use a completed, fresh, unscoped `ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION` export as the only source for package assembly. The target code must be unique under a case-insensitive comparison of exported `ORA_IRC_LC.Code` values.

For every requested phase, resolve the display name to exactly one exported `ORA_IRC_LC` identity with `TypeCode=POOL_BASIC_PHASE`, then resolve exactly one `ORA_IRC_LC_ROUTING` `PHASE` row owned by the selected source Pool process. Resolve each requested state beneath that phase identity from its exported `STATE` routing rows. A display label is a lookup input, not an identity; stop on zero or multiple matches. Do not create a phase or state definition that the export does not prove reusable.

For each resolved root phase route, clone its source settings graph to a new `SETTING_CODE_` and new `SETTING_ITEM_CODE_` values, after validating the fresh export's identifier pattern and collision-free dictionaries. Rebind the generated settings rows, setting items, and root phase route to the new `POOL` process; retain the exported phase and state identities. Include source-language process translations, `ASM_SETUP_CSV_METADATA.xml`, and header-only non-target CSV members. Validate every join before handing the immutable archive to `core.data-loader`.

## Setup Task Metadata

- Task name: `Candidate Pool Management Process Configuration`
- Task code: `ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION`
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

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Content`
- Setup task name: `Candidate Pool Management Process Configuration`
- Setup task code: `ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION`




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
