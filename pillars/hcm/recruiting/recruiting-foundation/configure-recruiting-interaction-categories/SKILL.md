---
skill_id: "hcm.recruiting.recruiting-foundation.configure-recruiting-interaction-categories"
name: "Configure Recruiting Interaction Categories Setup Task Guidance"
description: "Safely reviews and manages Recruiting interaction categories in the fixed ORA_IRC_INTERACTION_TYPE lookup through the shared Common Lookups capability."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
task_code: "ORA_IRC_CONFIGURE_RECRUITING_INTERACTION_CATEGORIES"
task_name: "Configure Recruiting Interaction Categories"
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
  - "interaction_category_review"
  - "immutable_change_preview"
  - "post_change_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common.lookups"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common.lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/configure-recruiting-interaction-categories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/configure-recruiting-interaction-categories/current/"
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
  - "Delegates one explicitly approved lookup-code create or update to the shared Common Lookups capability."
  - "Delegates one lookup-code deletion only after immutable-preview approval and a second fresh confirmation."
  - "Delegates an explicitly requested, validated, and approved FSM CSV import to core.data-loader."
required_privileges:
  - "Read and applicable mutation access required by core.fusion-api.apps-common.lookups in the selected Fusion environment."
  - "FSM import privileges are required only for an explicitly requested CSV import package."
---

# Configure Recruiting Interaction Categories Setup Task Guidance

## Purpose

Provides a business-first hybrid wrapper for reviewing and managing Recruiting and Candidate Experience interaction categories. All live lookup reads and mutations are delegated to `core.fusion-api.apps-common.lookups`; this skill owns only the narrower task scope, validation, comparison, approval, verification, and project-audit rules.

## Setup Task Skill Contract

- task_code: `ORA_IRC_CONFIGURE_RECRUITING_INTERACTION_CATEGORIES`
- task_name: `Configure Recruiting Interaction Categories`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Recruiting Interaction Categories` under `Recruiting Foundation`.

## Hybrid Wrapper Contract

- Keep every normal review and CRUD request within LookupType `ORA_IRC_INTERACTION_TYPE` and LookupCategory `Common`.
- Use `includeInactive: false` for normal review and discovery.
- Accept business-language requests and resolve technical identity from current configuration; ask for LookupCode only when the user supplies it or multiple valid matches remain.
- Delegate all lookup transport and CRUD to `core.fusion-api.apps-common.lookups`. Never construct REST URLs, call curl, manage OAuth, use browser automation, or duplicate its transport.
- Permit updates only to Meaning, Description, StartDate, and EndDate. Treat every other field as protected unless later approved evidence expands the boundary.
- Require the task-local immutable preview and approval gates before any delegated mutation, then perform the required fresh verification read and persist sanitized run evidence.
- Use task-level CSV export or FSM CSV import only when explicitly requested; neither is the default CRUD route.

## Task-Local Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_reference_lookups.md`
3. `ora-resource/ora_design_enforcement.md`
4. `ora-resource/ora_error_handling.md`
5. `ora-resource/ora_rule_registry.json`

The compiled registry is an execution handoff, not authorization for a Fusion mutation. Follow the exact operation-specific approval gate in the task-local resources immediately before delegating the action.

## Setup Task Metadata

- Task name: `Configure Recruiting Interaction Categories`
- Task code: `ORA_IRC_CONFIGURE_RECRUITING_INTERACTION_CATEGORIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Use these routes only when the user explicitly requests task-level CSV export or an FSM CSV import package; they are not the default route for lookup review or supported create, update, and delete operations:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import only an explicitly requested, validated, and approved FSM CSV package with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Foundation`
- Setup task name: `Configure Recruiting Interaction Categories`
- Setup task code: `ORA_IRC_CONFIGURE_RECRUITING_INTERACTION_CATEGORIES`




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
