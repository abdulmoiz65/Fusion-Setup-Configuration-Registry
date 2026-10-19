---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.manage-third-party-administrators"
name: "Manage Third-Party Administrators Setup Task Guidance"
description: "Prepare, validate, and route third-party-administrator master setup through the Organization HDL business object."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_THIRD_PARTY_ADMINISTRATOR"
task_name: "Manage Third-Party Administrators"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "Organization"
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
  - "fusion_environment_context"
  - "requested_operation"
  - "third_party_administrator_values"
  - "execution_approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "validation_result"
  - "data_load_execution_result"
  - "data_load_status"
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
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
  - purpose: "Task contract"
    location: "references/organization-hdl.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/manage-third-party-administrators/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/manage-third-party-administrators/current/"
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
  - "Reads live Organization metadata and organization references through shared core services."
  - "Prepares local loader artifacts; uploads and initiates only the approved artifact through core.data-loader."
required_privileges:
  - "Access to selected-environment Organization metadata and required organization references."
  - "Fusion UCM upload and HCM Data Loader import/load privileges for approved execution."
---

# Manage Third-Party Administrators Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Third-Party Administrators` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_THIRD_PARTY_ADMINISTRATOR`
- task_name: `Manage Third-Party Administrators`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `HDL`
- businessObject: `Organization`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Third-Party Administrators` under `Benefits General Configuration`.

## Setup Task Metadata

- Task name: `Manage Third-Party Administrators`
- Task code: `BEN_MANAGE_THIRD_PARTY_ADMINISTRATOR`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `Organization`

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

## HDL workflow and validation

Read [the task contract](references/organization-hdl.md) before intake,
validation, preview, or submission. It owns the field checks, conditional
requirements, identity rules, defaulting, failure classes, and recovery policy.
Read its standards in this order: [input validation](ora-resource/ora_input_validation.md),
[reference resolution](ora-resource/ora_reference_lookups.md),
[dependency readiness](ora-resource/ora_dependency_readiness.md),
[defaulting](ora-resource/ora_defaulting_rules.md),
[design enforcement](ora-resource/ora_design_enforcement.md), and
[error handling](ora-resource/ora_error_handling.md).

1. Establish the operation, target environment, and task context. Collect the
   organization name, effective start date, and either `LocationCode` plus
   `LocationSetCode`, or Task Location Name plus Location Set Name. Do not
   solicit `ClassificationCode` or `ClassificationName`.
2. Use [core.data-loader](../../../../../core/data-loader/SKILL.md) for live
   schema validation and file preparation. Resolve references through [the
   shared REST client](../../../../../core/fusion-api/rest-api-client/SKILL.md).
   Resolve `ClassificationName` through `organizationClassificationsLOV` using
   `ClassificationCode='BEN TPA'`; resolve name-based locations through
   `locationsLov` effective on the organization start date. Include
   `REST-Framework-Version: 9` on both LOV requests.
3. Apply every contract preflight check to all rows. Block preview for missing
   or invalid fields, uncertain identity, unsupported operations, or unresolved
   dependencies. Do not report Task Hook automation as passed when task rules
   are not available.
4. Follow core's immutable-artifact and Task Hook approval workflow. A prior
   upload approval does not authorize a new load. Never bypass core with a
   direct REST write.
5. Report initiation separately from completion. When status monitoring is
   requested, use core's status and error queries until a terminal status or the
   contract observation deadline. Preserve partial successes.

The catalog CSV-support flag is not a ban on core's metadata-validated
spreadsheet-to-HDL conversion. Do not claim FSM export/import support from a
successful native HDL load. Native `Organization` source uses only the
`Organization` and `OrgUnitClassification` sections; exclude `OrgInformation`
from every generated DAT file. Use `YYYY/MM/DD` dates.

## Failure handling and execution boundaries

Stop before upload on every blocking check. Corrected submissions need fresh
validation and approval. Never automatically retry uncertain writes or roll
back successful rows. For input, metadata, authentication, authorization,
transport, API, timeout, process failure, persistence, or approval errors,
record the environment, operation, stage, class, redacted message, artifact
reference, and one safe next action. Core's retry and diagnostic policies are
authoritative.

Keep source records, secrets, and test-environment data out of tracked files.
For delegated Data Loader operations, core's report and persistence policies
take precedence over generated planning-artifact defaults; do not create extra
run records or token logs for a loader-only operation.

## Verification and review

- Run [offline contract tests](tests/test_third_party_administrator_contract.py).
- Exercise [workflow scenarios](tests/third-party-administrator-scenarios.md)
  with synthetic inputs and mocked results; they are manual, not proof of live
  validation.
- A fresh live upload requires separate authorization.
