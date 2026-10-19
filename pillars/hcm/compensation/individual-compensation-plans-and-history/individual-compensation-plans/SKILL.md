---
skill_id: "hcm.compensation.individual-compensation-plans-and-history.individual-compensation-plans"
name: "Individual Compensation Plans Setup Task Guidance"
description: "Provides task-specific setup guidance for Individual Compensation Plans under the Individual Compensation Plans and History functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Individual Compensation Plans and History"
functional_area_code: "ORA_INDIVIDUAL_COMPENSATION_PLANS_AND_HISTORY"
task_code: "CMP_MANAGE_INDIVIDUAL_COMPENSATION_PLANS"
task_name: "Individual Compensation Plans"
parent_skill_id: "hcm.compensation.individual-compensation-plans-and-history"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "individualCompensationPlans"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
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
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.apps-common"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/individual-compensation-plans-and-history/individual-compensation-plans/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/individual-compensation-plans-and-history/individual-compensation-plans/current/"
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

# Individual Compensation Plans Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Individual Compensation Plans` under `Individual Compensation Plans and History`.

## Setup Task Skill Contract

- task_code: `CMP_MANAGE_INDIVIDUAL_COMPENSATION_PLANS`
- task_name: `Individual Compensation Plans`
- parent_skill_id: `hcm.compensation.individual-compensation-plans-and-history`
- pillar: `HCM`
- offering: `Compensation`
- functional_area: `Individual Compensation Plans and History`
- functional_area_code: `ORA_INDIVIDUAL_COMPENSATION_PLANS_AND_HISTORY`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `individualCompensationPlans`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Individual Compensation Plans` under `Individual Compensation Plans and History`.

## Setup Task Metadata

- Task name: `Individual Compensation Plans`
- Task code: `CMP_MANAGE_INDIVIDUAL_COMPENSATION_PLANS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `individualCompensationPlans`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `individualCompensationPlans` as the exact Business Object.

## Live Metadata Contract

Use the registered Data Loader object `individualCompensationPlans` (UI name
and description: `Individual Compensation Plans`) and its live
`individualCompensationPlans.dat` template as the authoritative contract. Do
not infer a field, child relationship, lookup, or REST collection from its
display name.

Before validating a create, update, import, or source file, resolve the exact
registered object, download its current template, and retrieve its child-object
and attribute metadata through `core.data-loader`. The current hierarchy is:

1. `individualCompensationPlans` — the parent plan.
2. `Option` — plan options.
3. `AttributeElement` — an option's payroll element configuration.
4. `OptionEligibility` — eligibility for an option.
5. `PlanAccess` and `PlanPeriod` — plan access and its evaluation periods.
6. `PlanEligibility` — eligibility for the plan.

Use [ora-resource/ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
for the exact registered-object, schema, and payroll-element resolver rules.
Use [ora-resource/ora_input_validation.md](ora-resource/ora_input_validation.md)
for schema-derived field and child-lineage checks.

## Field Resolution and Validation

1. Accept only exact fields returned for the relevant live template section.
   Preserve the template's parent-child linkage; never substitute an ID or
   name based solely on a similar label.
2. Validate `RestAction` in every supplied parent or child section. Apply the
   live mandatory, data type, length, precision, user-key, reference, and
   lookup metadata only to the selected operation.
3. Resolve a supplied `AttributeElement.ElementName` through
   `payrollElementDefinitionsLOV`; require one effective exact match. Populate
   `LegislativeDataGroupName` from the returned record and populate `Country`
   from its nonblank `LegislationCode`. Also populate `ClassificationName` from
   `PrimaryClassificationName` and `ProcessingTypeCode` from `ProcessingType`.
   A caller-supplied LDG, country, classification, or processing type code must
   agree with the resolved value. Resolve that code through the enabled
   `PROCESSING_TYPE` common lookup and populate
   `ProcessingTypeMeaning` from its exact returned meaning; a caller-supplied
   meaning must agree. If Fusion omits `LegislationCode`, stop for a country
   input rather than inferring one from the LDG name. These read-only resolvers
   do not create or change the element.
4. Treat plan, action, period, and access-level values as schema-declared
   dependencies. `DocumentType`, `GrantType`, `NonMonetaryUOMMeaning`,
   `RequiresAttachmentMeaning`, and `PlanAttributeId` are optional Option
   values: omit them when absent and validate them only when supplied.
   Resolve `AllowStartDateOverride` and `AllowEndDateOverride` from enabled
   standard lookup `YES_NO`; when omitted, use `N` (`No`) and fill each paired
   meaning. Resolve `PaymentEndDate` from enabled `CMP_END_DATE`; when omitted,
   use `ONGOING_OR_USER_CHOOSE_DATE` and fill `PaymentEndDateMeaning`. Supplied
   codes must be enabled exact lookup codes and supplied meanings must agree.
   Eligibility profiles are also optional: omit `OptionEligibility` and
   `PlanEligibility` sections when none is supplied; validate their parent
   linkage and fields only for supplied rows. Use a live resolver only when the
   current metadata exposes one; otherwise retain the supplied exact template
   value and stop on an unresolved dependency rather than inventing an endpoint
   or a matching rule.
5. `StartDate`, `EndDate`, `PeriodStartDate`, and `PeriodEndDate` are Date
   fields. Validate their supplied values against the live template's date
   contract. Do not apply date validation to similarly named String fields.
6. Resolve the parent plan's `Status` from the enabled `CMP_PLAN_STATUS`
   common lookup. When it is omitted, select the one enabled code whose
   meaning is exactly `Active`. When supplied, require an enabled exact lookup
   code before retaining it; do not substitute a display meaning for a code.
7. Resolve the parent plan's `DefaultVisibility` from the enabled
   `ORA_CMP_IC_PLANINFO_VISIBILITY` common lookup. When it is omitted, select
   the one enabled code whose meaning is exactly `People see after clicking
   show plan info`; when supplied, require an enabled exact lookup code. Fill
   the code and returned meaning, and require any caller-supplied meaning to
   agree with the lookup result.
8. Resolve `PaymentStartDate` from the enabled `CMP_START_DATE` common lookup.
   When it is omitted, use `APPRVL_DT_OR_USER_CHOOSE_DATE`. When supplied,
   require an enabled exact lookup code before retaining it. This selection is
   separate from a literal `StartDate` value.
9. Resolve the parent plan's `RestrictPlanAccess` from the enabled standard
   `YES_NO` lookup. When it is omitted, use code `N` (meaning `No`). When
   supplied, require an enabled exact `YES_NO` lookup code; do not use the
   display meaning as a substitute for the code.

## Read and Query Boundary

The registered Data Loader object supports metadata/template validation and
the Data Loader import route. It does not by itself establish a query route for
existing Individual Compensation Plan records. Do not use a generic
`/fscmRestApi` collection for plan reads unless a separate verified REST
resource and task read contract are added.

Use this task metadata when invoking those skills:

- Offering: `Compensation`
- Functional area / Setup Object: `Individual Compensation Plans and History`
- Setup task name: `Individual Compensation Plans`
- Setup task code: `CMP_MANAGE_INDIVIDUAL_COMPENSATION_PLANS`




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

Use the parent functional-area skill `hcm.compensation.individual-compensation-plans-and-history` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
