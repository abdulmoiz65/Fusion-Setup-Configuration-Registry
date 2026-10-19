---
skill_id: "hcm.recruiting.recruiting-foundation.recruiting-and-candidate-experience-lookups"
name: "Recruiting and Candidate Experience Lookups Setup Task Guidance"
description: "Reviews and safely manages approved Recruiting Common Lookup types and codes through the shared Common Lookups capability."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
task_code: "ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_LOOKUPS"
task_name: "Recruiting and Candidate Experience Lookups"
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
  - "recruiting_common_lookup_review"
  - "immutable_lookup_change_preview"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/recruiting-and-candidate-experience-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/recruiting-and-candidate-experience-lookups/current/"
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
  - "Delegates one explicitly approved supported Common Lookup type or lookup-code create, update, or delete."
  - "Delegates an explicitly requested, validated, and approved FSM CSV import to core.data-loader."
required_privileges:
  - "Read and applicable lookup mutation access required by core.fusion-api.apps-common.lookups in the selected Fusion environment."
  - "FSM import privileges are required only for an explicitly requested CSV import package."
---

# Recruiting and Candidate Experience Lookups Setup Task Guidance

## Purpose

Provides a business-first hybrid wrapper for reviewing and managing approved Recruiting and Candidate Experience Common Lookup types and codes, with read-only translation access. The shared Common Lookups skill owns all live transport; this wrapper owns Recruiting prefix scope, business intake, field protection, approval, verification, and project audit rules.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_LOOKUPS`
- task_name: `Recruiting and Candidate Experience Lookups`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Recruiting and Candidate Experience Lookups` under `Recruiting Foundation`.

## Hybrid Wrapper Contract

- Accept business-language Recruiting outcome, experience, policy, and terminology requests; resolve the technical operation internally.
- Treat a Common Lookup type as task-owned only when its exact LookupType starts with `ORA_JA`, `ORA_IRC`, `ORA_OM`, `IRC_HCO`, or `ORA_LI`.
- Use only the Common Lookup view of `core.fusion-api.apps-common.lookups` for type/code reads and supported CRUD and for read-only translations.
- Never construct REST URLs, call curl, manage OAuth, use browser automation, or duplicate Common Lookups transport.
- Read the exact current parent and code as applicable; prove create absence; preserve identity, ownership evidence, seed identity when returned, protected fields, and every unrequested value.
- Permit only field deltas established by current documented response metadata. Never infer ModuleId filters, API ownership discovery, module details, protection attributes, or translation mutation.
- Require the task-local immutable preview and exact approval immediately before one delegated mutation, then freshly verify the affected resource and persist only sanitized evidence.
- Use CSV export or FSM CSV import only when explicitly requested; neither is a fallback for review or CRUD.

## Task-Local Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_reference_lookups.md`
3. `ora-resource/ora_design_enforcement.md`
4. `ora-resource/ora_error_handling.md`
5. `ora-resource/ora_rule_registry.json`

The compiled registry is an execution handoff, not authorization. Apply its task-specific approval gate immediately before delegating one Common Lookup mutation.

## Setup Task Metadata

- Task name: `Recruiting and Candidate Experience Lookups`
- Task code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Use these routes only when the user explicitly requests task-level CSV export or an FSM CSV import package; they are not the default route for Common Lookup review or CRUD:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import only an explicitly requested, validated, and approved FSM CSV package with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Foundation`
- Setup task name: `Recruiting and Candidate Experience Lookups`
- Setup task code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_LOOKUPS`




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
