---
skill_id: "hcm.recruiting.recruiting-content.candidate-selection-process-configuration"
name: "Candidate Selection Process Configuration Setup Task Guidance"
description: "Provides task-specific setup guidance for Candidate Selection Process Configuration under the Recruiting Content functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Content"
functional_area_code: "ORA_RECRUITING_CONTENT"
task_code: "ORA_IRC_CANDIDATE_SELECTION_PROCESS_CONFIGURATION"
task_name: "Candidate Selection Process Configuration"
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
version: "0.2.0"
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
  - "core.auth.fusion-oauth-authentication"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/candidate-selection-process-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/candidate-selection-process-configuration/current/"
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

# Candidate Selection Process Configuration Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Candidate Selection Process Configuration` under `Recruiting Content`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_CANDIDATE_SELECTION_PROCESS_CONFIGURATION`
- task_name: `Candidate Selection Process Configuration`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Candidate Selection Process Configuration` under `Recruiting Content`.

## Reuse for Candidate Pool with `pTypeCode=POOL`

The Candidate Pool task skill `hcm.recruiting.recruiting-content.candidate-pool-management-process-configuration` may invoke this skill with `setup_task_scope.pTypeCode=POOL` to reuse the common collect, export, validate, import, and verification workflow.

For that delegated invocation:

- Retain the caller's task code and task name rather than substituting the Candidate Selection task identity.
- Pass `pTypeCode=POOL` to the task-level export scope.
- Do not apply Candidate Selection task-local `ora-resource` rules, registry nodes, `CSW` defaults, Offer or HR blocks, or candidate-status behavior.
- Return the existing `setup_task_plan`, `setup_data_routing`, and `validation_checkpoints` outputs to the Candidate Pool task skill, which remains responsible for the Pool task identity and Pool-specific readiness.

When `setup_task_scope.pTypeCode=POOL` is absent, preserve the existing standalone Candidate Selection behavior without change.

## Setup Task Metadata

- Task name: `Candidate Selection Process Configuration`
- Task code: `ORA_IRC_CANDIDATE_SELECTION_PROCESS_CONFIGURATION`
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
- Setup task name: `Candidate Selection Process Configuration`
- Setup task code: `ORA_IRC_CANDIDATE_SELECTION_PROCESS_CONFIGURATION`

## Operator Handoff for a New Process

Keep the task-specific design and the execution workflow distinct:

1. Collect the process, custom-phase, custom-state, candidate-status, and Oracle-generated definition-code inputs. Explain in the preview that Fusion also adds the seeded `Rejected by Employer` and `Withdrawn by Candidate` terminal states to each custom phase; they are not additional requested custom states.
2. Complete the export-backed validation and final archive review before execution. Do not weaken the existing uniqueness, identifier, routing, translation, or system-block rules for convenience.
3. Before presenting the final Data Loader submission question, use `core.auth.fusion-oauth-authentication` to confirm the local token cache is usable. If login is needed, complete it before presenting the immutable submission preview. When the default browser is unavailable, use the auth workflow's URL-only mode and show the user the resulting sign-in URL; never expose tokens, authorization codes, or cache contents.
4. After the user approves the exact immutable archive, hand it to `core.data-loader`. Its initiation receipt is not necessarily the FSM import request shown later in Fusion. Preserve and label each identifier by its source; do not report the Data Loader initiation request as the FSM import request.
5. When the user asks for completion evidence, direct them to **Manage Configuration Packages** and the import's **Process Status Details**, then reconcile the supplied ProcessLog or a fresh read-only export. Do not retry an unobservable or failed submission automatically.




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
