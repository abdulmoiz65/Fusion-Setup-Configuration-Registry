---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.benefit-reporting-groups"
name: "Benefit Reporting Groups Setup Task Guidance"
description: "Validates Benefit Reporting Groups and its child records before a routed HDL load."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_BENEFIT_REPORTING_GROUPS"
task_name: "Benefit Reporting Groups"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitReportingGroups"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM benefits configuration pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "benefit_reporting_groups_payload"
  - "fusion_environment_context"
  - "requested_operation"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "validation_result"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/benefit-reporting-groups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/benefit-reporting-groups/current/"
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
  - "Reads selected-environment LOV resources when the active workflow authorizes reference validation."
  - "Prepares local HDL artifacts; an approved load is submitted only through core.data-loader."
required_privileges:
  - "Read access to selected-environment LOV resources for supplied reference fields."
  - "HCM Data Loader privileges for an approved load."
---

# Benefit Reporting Groups Setup Task Guidance

## Purpose

Guides the Manage Reporting Groups task, cataloged as `Benefit Reporting Groups`, using the requested `benefitReportingGroups` object and its child records.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_BENEFIT_REPORTING_GROUPS`
- task_name: `Benefit Reporting Groups`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `HDL`
- businessObject: `benefitReportingGroups`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Benefit Reporting Groups` under `Benefits General Configuration`.

## Child Object Scope

The requested record tree contains `regulatoryBodies`, its nested `regulatoryPurposes`, `regulations`, `reportingGroupForProgramsOrPlans`, and `translations`. Preserve all supplied rows and their parent-child relationships. Validate each supplied row independently. Current target-environment HDL metadata must confirm exact object and child section names, keys, date-effectivity, `effectiveOf` availability, and supported operations before a row control is derived or an artifact is built or loaded; the names in this request alone do not establish an executable HDL schema.

## Read Order and Routing

1. Read [input validation](ora-resource/ora_input_validation.md) for shape and presence checks.
2. Read [dependency readiness](ora-resource/ora_dependency_readiness.md) for metadata and Run Book gates, then [reference lookups](ora-resource/ora_reference_lookups.md) for the nine conditional field checks.
3. Read [defaulting rules](ora-resource/ora_defaulting_rules.md), [design enforcement](ora-resource/ora_design_enforcement.md), and [error handling](ora-resource/ora_error_handling.md).
   For every row in a section confirmed to expose `effectiveOf`, derive it from that row's operation and serialize each embedded date as `YYYY-MM-DD`; reject invalid or ambiguous source dates. Omit `effectiveOf` entirely from a section that does not expose it, including `translations` unless current metadata explicitly says otherwise.
4. Use the active project workflow and `core.fusion-api.rest-api-client` only when it selects the read-only LOV step. Validate current HDL metadata and artifact shape through `core.data-loader` before preview or submission. Require the active Run Book and the loader's approval workflow for a live load.

An HTTP 403 from a conditional LOV check produces `unverified_forbidden` for that field and does not throw a field-validation error. It does not establish that the value is valid. Retain that status in the validation result and resolve access or obtain another workflow-approved authoritative check before a live load.

## Setup Task Metadata

- Task name: `Benefit Reporting Groups`
- Task code: `BEN_MANAGE_BENEFIT_REPORTING_GROUPS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `benefitReportingGroups`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.




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

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
