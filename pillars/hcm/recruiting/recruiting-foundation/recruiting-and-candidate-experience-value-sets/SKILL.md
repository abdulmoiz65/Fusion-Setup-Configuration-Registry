---
skill_id: "hcm.recruiting.recruiting-foundation.recruiting-and-candidate-experience-value-sets"
name: "Recruiting and Candidate Experience Value Sets Setup Task Guidance"
description: "Reviews Recruiting-owned value sets and safely manages supported child values through the shared Common Value Sets capability."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
task_code: "ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_VALUE_SETS"
task_name: "Recruiting and Candidate Experience Value Sets"
parent_skill_id: "hcm.recruiting.recruiting-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "requested_business_change"
  - "target_environment"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "recruiting_value_set_review"
  - "immutable_child_change_preview"
  - "post_change_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.rest-api-client"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common.value-sets"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/recruiting-and-candidate-experience-value-sets/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/recruiting-and-candidate-experience-value-sets/current/"
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
side_effects:
  - "Delegates one explicitly approved supported child-value create, update, or delete to core.fusion-api.apps-common.value-sets."
  - "May use the shared REST client for the restricted read-only root-pagination fallback when Common Value Sets lacks a safe continuation contract."
  - "Delegates an explicitly requested, validated, and approved FSM CSV import to core.data-loader."
required_privileges:
  - "Read and applicable child-value mutation access required by core.fusion-api.apps-common.value-sets in the selected Fusion environment."
  - "FSM import privileges are required only for an explicitly requested CSV import package."
---

# Recruiting and Candidate Experience Value Sets Setup Task Guidance

## Purpose

Provides a business-first hybrid wrapper for reviewing Recruiting and Candidate Experience value sets and managing supported child value rows. The shared Common Value Sets skill owns normal transport and CRUD; this wrapper owns Recruiting ModuleId scope, exact-code routing, root-definition boundaries, pagination safeguards, approval, verification, and project audit rules.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_VALUE_SETS`
- task_name: `Recruiting and Candidate Experience Value Sets`
- parent_skill_id: `hcm.recruiting.recruiting-foundation`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Foundation`
- functional_area_code: `ORA_RECRUITING_FOUNDATION_DATA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Recruiting and Candidate Experience Value Sets` under `Recruiting Foundation`.

## Hybrid Wrapper Contract

- Begin with the desired Recruiting outcome, affected experience, intended users, timing, and policy or list-of-values change.
- For a particular value set, require one exact user-provided ValueSetCode and pass it unchanged as `valueSets_Id` to `core.fusion-api.apps-common.value-sets`; do not require prior numeric-ID discovery.
- Use Common Value Sets first for root reads, validation-table metadata, and child-value reads and supported CRUD.
- Use the restricted read-only root-collection pagination fallback only when Common Value Sets returns `hasMore=true` without a safe continuation contract. Never guess offset or limit.
- Authorize a value set only when its current API ModuleId matches the complete task-local Recruiting ModuleId allowlist.
- Treat root value-set definitions as read-only. Permit only response-supported child-value changes after exact identity, validation behavior, protection, preservation, immutable-preview, and approval checks pass.
- Never use direct REST, UI automation, FSM, export/import, or another route to bypass an unsupported root or child request.
- Persist only sanitized run, approval, diagnostic, and token-usage evidence in the active project workspace.

## Task-Local Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_reference_lookups.md`
3. `ora-resource/ora_design_enforcement.md`
4. `ora-resource/ora_error_handling.md`
5. `ora-resource/ora_rule_registry.json`

The compiled registry is an execution handoff, not mutation authorization. Follow its exact task-specific approval gate immediately before delegating one child-value mutation.

## Setup Task Metadata

- Task name: `Recruiting and Candidate Experience Value Sets`
- Task code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_VALUE_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Use these routes only when the user explicitly requests task-level CSV export or an FSM CSV import package; they are not the default route for root review or supported child-value CRUD:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import only an explicitly requested, validated, and approved FSM CSV package with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Foundation`
- Setup task name: `Recruiting and Candidate Experience Value Sets`
- Setup task code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_VALUE_SETS`




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

Use the parent functional-area skill `hcm.recruiting.recruiting-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
