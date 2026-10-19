---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.year-periods-and-billing-calendars"
name: "Year Periods and Billing Calendars Setup Task Guidance"
description: "Provides task-specific setup guidance for Year Periods and Billing Calendars under the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_PROGRAMS_PLAN_YEARS"
task_name: "Year Periods and Billing Calendars"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitYearPeriods"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM benefits configuration pillar team"
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
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
  - "shared.validation.setup-data-validator"
uses_core:
  - "core.data-loader"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/year-periods-and-billing-calendars/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/year-periods-and-billing-calendars/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/year-periods-and-billing-calendars/current/"
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
  - "Creates local validation, preview, and diagnostic artifacts."
  - "Reads selected-environment commonLookupsLOV when the active workflow authorizes PeriodTypeMeaning validation."
  - "An approved HDL import is uploaded and initiated only through core.data-loader."
required_privileges:
  - "Access to the target Fusion environment and privileges for the registered benefitYearPeriods Data Loader business object."
  - "Read access to selected-environment commonLookupsLOV for supplied PeriodTypeMeaning values."
---

# Year Periods and Billing Calendars Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Year Periods and Billing Calendars` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_PROGRAMS_PLAN_YEARS`
- task_name: `Year Periods and Billing Calendars`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `HDL`
- businessObject: `benefitYearPeriods`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Year Periods and Billing Calendars` under `Benefits General Configuration`.

## Setup Task Metadata

- Task name: `Year Periods and Billing Calendars`
- Task code: `BEN_MANAGE_PROGRAMS_PLAN_YEARS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `benefitYearPeriods`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export`. For an HDL source whose registered top-level business object is `benefitYearPeriods`, route local validation, immutable preview, approval, upload, initiation, and diagnostics through `core.data-loader`. Do not replace this route with direct REST calls, browser entry, or another loader.

## HDL Workflow

1. Confirm the task code, target environment, requested operation, and `benefitYearPeriods` object.
2. Format every populated `StartDate`, `EndDate`, `LimitationYearStartDate`, and `LimitationYearEndDate` as a valid calendar date in `YYYY-MM-DD` format before validation; reject ambiguous or invalid dates rather than silently converting them.
3. Treat `PeriodType` as a current-metadata foreign key. The live
   `benefitYearPeriods` contract exposes `PeriodTypeMeaning` as its user-key
   alternative. For each supplied `PeriodTypeMeaning`, use the read-only
   [reference lookup](ora-resource/ora_reference_lookups.md) to require an exact
   `Meaning` match from `commonLookupsLOV` with
   `LookupTypeFinder;LookupType=BEN_PERD_TYP`. Use
   `core.fusion-api.rest-api-client` only when the active project workflow
   selects that lookup step. Preserve the supplied meaning and use the
   metadata-supported key form. A 403 records `unverified_forbidden` without
   failing field validation or stopping independent checks; it does not
   verify the value. Resolve access or use another workflow-approved
   authoritative check before live load. Do not load a display label such as
   `Calendar` into `PeriodType` unless current metadata or lookup evidence
   identifies it as the accepted key.
4. Validate the exact source against current Data Loader metadata through `core.data-loader`; the current contract requires `RestAction` and exposes `EndDate`, `StartDate`, and `PeriodType` as the primary user-key components. Do not infer HDL attributes, user keys, or supported operations.
5. Save the validated immutable preview and task diagnostics in the project workspace when `project_id` is supplied.
6. Obtain the Data Loader workflow's approval for the exact artifact and target before any upload or initiation.
7. After submission, use the Data Loader status and diagnostics workflow. Do not automatically retry an uncertain, failed, or timed-out live load.

Read the task-local `ora-resource/` guidance before preview or live execution.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `diagnostics`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
