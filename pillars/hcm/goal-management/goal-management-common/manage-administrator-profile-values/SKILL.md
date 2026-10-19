---
skill_id: "hcm.goal-management.goal-management-common.manage-administrator-profile-values"
name: "Manage Administrator Profile Values Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Administrator Profile Values under the Goal Management Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Management Common"
functional_area_code: "ORA_GOAL_MANAGEMENT_COMMON"
task_code: "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
task_name: "Manage Administrator Profile Values"
parent_skill_id: "hcm.goal-management.goal-management-common"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "goal_management_execution_control"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-administrator-profile-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-administrator-profile-values/current/"
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

# Manage Administrator Profile Values Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Administrator Profile Values` under `Goal Management Common`.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- task_name: `Manage Administrator Profile Values`
- parent_skill_id: `hcm.goal-management.goal-management-common`
- pillar: `HCM`
- offering: `Goal Management`
- functional_area: `Goal Management Common`
- functional_area_code: `ORA_GOAL_MANAGEMENT_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Administrator Profile Values` under `Goal Management Common`.

## Setup Task Metadata

- Task name: `Manage Administrator Profile Values`
- Task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is catalog metadata only in this Goal Management
facade. It does not authorize this skill to export, construct, validate, or import
a dependency mutation package. Route any dependency maintenance to the owning
provider named in [Dependent Setup Routing](../../goal-management-common/dependent-setup-routing.md);
that provider chooses its supported single-record or bulk/setup-import workflow.

Use this task metadata when invoking those skills:

- Offering: `Goal Management`
- Functional area / Setup Object: `Goal Management Common`
- Setup task name: `Manage Administrator Profile Values`
- Setup task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`




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

Use the parent functional-area skill `hcm.goal-management.goal-management-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Goal Management profile-value routing

Before a profile-value mutation preview or provider handoff, require an
`allowed` result from the Goal Management parent
`resolve_controlled_next_task` guard whose exact task code, Common functional
area, skill path, sequence, and approved plan fingerprint match this task. A
request or approval for this profile value cannot skip an earlier task in the
resolved input-specific Run Book. Missing, stale, stopped, or mismatched
control returns `BLOCKED` without invoking the provider.

Use this task for a resolved profile-value create or update, including a proposed
value for `HRG_ALLOW_DECIMALS_IN_WEIGHTS`. Preserve the exact profile code,
owning product, level, requested meaning, stored value, and semantic-catalog
provenance from intake.

Invoke the standard `core.fusion-api.apps-common.profile-options` provider for
definition and effective-value reads and for its declared update workflow. Do
not implement a pillar-local connection or REST client. Before any update, the
provider must verify the target-tenant definition, supported level, permitted
stored value, and current effective value, then present its immutable preview
and obtain explicit approval. This planning route does not itself authorize or
perform a Fusion change.

This skill is a delegation facade and owns no REST mutation. One configured
value change executes only through the canonical provider after its own
preview and approval. Multiple value changes require the provider's supported
bulk/setup-import route; do not loop POST or PATCH requests from Goal
Management.

Keep definition-only maintenance under
`hcm.goal-management.goal-management-common.manage-profile-options`; do not map a value update
to `FND_MANAGE_PROFILE_OPTIONS`.
