---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.configure-benefits-feature-preferences"
name: "Configure Benefits Feature Preferences Setup Task Guidance"
description: "Provides task-specific Data Loader guidance for initializing and updating Benefits Feature Preferences under the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "ORA_CONFIGURE_FEATURE_PREFERENCES"
task_name: "Configure Benefits Feature Preferences"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
dataloader_import_mode: "HDL"
businessObjects:
  - "initializeBenefitFeaturePreferences"
  - "benefitFeaturePreferences"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "feature_preference_user_key"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "hdl_preflight_result"
  - "load_diagnostic"
  - "validated_update_dat"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.benefits-configuration.benefits-general-configuration"
  - "core.data-loader"
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
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/configure-benefits-feature-preferences/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/configure-benefits-feature-preferences/current/"
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
  - "Reads selected-environment lookup and territory LOVs for supplied Update preferences values when the active workflow authorizes reference validation."
required_privileges:
  - "Read access to selected-environment commonLookupsLOV and territoriesLOV for supplied fields."
---

# Configure Benefits Feature Preferences Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Benefits Feature Preferences` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `ORA_CONFIGURE_FEATURE_PREFERENCES`
- task_name: `Configure Benefits Feature Preferences`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `UNKNOWN`
- csv_export_import_supported_flag: `UNKNOWN`
- dataloader_import_mode: `HDL`
- businessObjects: `initializeBenefitFeaturePreferences`, `benefitFeaturePreferences`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Benefits Feature Preferences` under `Benefits General Configuration`.

## Setup Task Metadata

- Task name: `Configure Benefits Feature Preferences`
- Task code: `ORA_CONFIGURE_FEATURE_PREFERENCES`
- Available: `Y`
- Export/import supported: `UNKNOWN`
- CSV export/import supported: `UNKNOWN`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Objects: `initializeBenefitFeaturePreferences, benefitFeaturePreferences`

## HDL Object Routing

Use `core.data-loader` for this task. The supplied object route is operation-specific:

| Requested operation | HDL business object | Control point |
| --- | --- | --- |
| Create preferences | `initializeBenefitFeaturePreferences` | Use the fixed parameterless DAT below, preflight it, and submit the HDL load that creates the predefined feature preferences; no user-supplied preference values are required. |
| Update preferences | `benefitFeaturePreferences` | Obtain the current Data Loader sample, prepare an immutable PATCH DAT using its identity rules, and validate it before the Data Loader workflow approval gate. |

Do not substitute one object for the other, infer a DAT schema, or use an alternate import route. `initializeBenefitFeaturePreferences` creates the predefined feature preferences through the fixed parameterless HDL load below. For updates, the current Data Loader sample remains authoritative for headers, required attributes, identity fields, and any date or effective-dating behavior. The supplied object mapping does not define a delete route.

## Update Preferences DAT Standards

For `benefitFeaturePreferences` updates:

- Name the source file exactly `benefitFeaturePreferences.dat`. Data Loader resolves a DAT business object from the case-sensitive filename stem; suffixes such as `-update` cause preflight to reject the file before upload.
- Preserve the current live-sample `METADATA` header and section order. Do not add, remove, or rename attributes based on a previous sample.
- Set `RestAction` to `PATCH`. A change to this action, the source, or any mapped value creates a new immutable artifact and requires fresh preflight and approval.
- When the current sample supports the user key, leave `PreferenceId` blank and derive it from the supplied user-key values. Do not ask for `PreferenceId` merely because it appears in the sample.
- For the confirmed current user-key pattern, supply `FeatureName`, `FeatureTypeMeaning`, and `ApplicabilityMeaning`; retain `Legislation` as a separate value when supplied. Do not replace `ApplicabilityMeaning` with the legislation label or country value.
- Map a supplied status to `PreferenceStatusMeaning` when that current-sample foreign user key is available. Leave `PreferenceStatus` blank unless the current sample or user supplies the required code explicitly.

For each supplied `benefitFeaturePreferences.FeatureTypeMeaning`,
`PreferenceStatusMeaning`, `ApplicabilityMeaning`, or `Legislation`, apply the
read-only [reference lookup rules](ora-resource/ora_reference_lookups.md).
Use `core.fusion-api.rest-api-client` only when the active project workflow
selects this step. The three meaning fields use their declared
`commonLookupsLOV` lookup types; `Legislation` requires an exact
`TerritoryShortName` match from `territoriesLOV`. Preserve the supplied values.
A 403 records `unverified_forbidden` without failing field validation or
stopping independent checks; it does not verify the value. Resolve access or
use another workflow-approved authoritative check before a live load. The
fixed parameterless Create preferences DAT has no lookup-value inputs and
does not run these checks.

## Create Preferences DAT

Use this exact DAT content for Create preferences:

```text
METADATA|initializeBenefitFeaturePreferences|Content-Type|REST-Framework-Version|RestAction
MERGE|initializeBenefitFeaturePreferences|application/vnd.oracle.adf.action+json|9|POST
```

Treat the DAT as immutable through `core.data-loader` preflight and the approval gate. Do not add preference values, change its headers, substitute an object, or reuse it for Update preferences.

## Preflight and Approval Gates

1. Confirm the requested operation is Create preferences or Update preferences and select its mapped HDL business object.
2. For Create preferences, use the fixed parameterless `initializeBenefitFeaturePreferences` DAT and preflight it with `core.data-loader`; do not request user-supplied preference values or retrieve a sample as a prerequisite.
3. For Update preferences, generate or retrieve the current Data Loader sample,
   check each supplied lookup field through the selected read-only client,
   build an exact-name `benefitFeaturePreferences.dat` with `RestAction=PATCH`,
   and preflight the immutable artifact with `core.data-loader`.
4. For either data-changing HDL load, use the Data Loader workflow's current approval gate immediately before upload or initiation. Any target, operation, object, or artifact change invalidates the approval.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `UNKNOWN`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

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

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Load the task-local `ora-resource/ora_input_validation.md`, `ora_reference_lookups.md`, and `ora_error_handling.md` before preflight or live activity. Track token usage for any generated project artifact or skill-run record using the manifest policy.
