---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-customer-account-profile-options"
name: "Manage Customer Account Profile Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Customer Account Profile Options under the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_CUSTOMER_ACCOUNT_PROFILE_OPTIONS"
task_name: "Manage Customer Account Profile Options"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "profile_option_code"
  - "profile_option_level"
  - "profile_option_level_key"
  - "proposed_profile_option_value"
  - "profile_option_operation"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "profile_option_view_result"
  - "profile_option_update_preview"
  - "profile_option_update_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-customer-account-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-customer-account-profile-options/current/"
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
  - "Reads profile option definitions and configured values through core.fusion-api.apps-common when view is selected."
  - "After exact approval, core.fusion-api.apps-common may create or update one profile option value at the approved level."
  - "Export and import use the declared shared FSM and Core Data Loader workflows with their validation and approval gates."
required_privileges:
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV to create or update profile option values through core.fusion-api.apps-common"
  - "Fusion privileges to view the selected profile option"
---

# Manage Customer Account Profile Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Customer Account Profile Options` under `Trading Community Foundation`.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_CUSTOMER_ACCOUNT_PROFILE_OPTIONS`
- task_name: `Manage Customer Account Profile Options`
- parent_skill_id: `cx.customer-data-management.trading-community-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Trading Community Foundation`
- functional_area_code: `ORA_HZ_CDM_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Customer Account Profile Options` under `Trading Community Foundation`.

## Setup Task Metadata

- Task name: `Manage Customer Account Profile Options`
- Task code: `HZ_MANAGE_CUSTOMER_ACCOUNT_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Supported Operations

1. `view`: Read the exact profile definition, configured value at the requested level, and effective authenticated-session value through `core.fusion-api.apps-common`.
2. `manual_update`: Provide the supported Setup and Maintenance procedure. The user performs the save in Fusion.
3. `update`: Create or update one explicitly approved site, product, or user-level profile value through `core.fusion-api.apps-common`.
4. `export`, `import`, and `validate`: Use the catalog-backed CSV/FSM routes declared below.

Do not use this skill to create or alter profile-option definitions, infer an undocumented valid value, or bulk-update unrelated profile options.

## Supported Profile Options

This task owns exactly this profile option in the validated `cptcpuwqy` task inventory:

| Profile Option Code | Display Name |
|---|---|
| `HZ_GENERATE_CUSTOMER_NUMBER` | Customer Account Number Generation |

For `view`, `manual_update`, or `update`, require this exact code. For FSM validation, reject profile-option rows owned by another task. If a completed export omits this code, report `export_content_discrepancy`; do not call a structurally valid ZIP corrupt and do not invent the omitted row.

## Oracle Documentation

Use Oracle's [Foundation Profile Options](https://docs.oracle.com/en/cloud/saas/sales/oasal/trading-community-model-profile-options.html) as the current public reference for customer and account foundation profile options and the supported administrator profile-value procedure. Confirm the exact option code and allowed value in the selected task or through the read-only profile definition before preparing a change.

## View and Change Profile Option Values

For `view`, use `core.fusion-api.apps-common` to read the exact profile definition and its level-specific configured value. Read the authenticated-session `profileValues` resource only to verify the effective value; it is not a configured-value write route.

For `manual_update`, instruct the user to open **Setup and Maintenance**, search for the exact setup task named by this skill, select the exact profile option code, enter the intended level-specific value, and save. Use **Manage Administrator Profile Values** only when the cited Oracle documentation explicitly directs that route. Re-read the configured and effective values afterward when verification is required.

For `update`, display the target environment, profile option code, level and level key, current value, proposed value, and whether that level is enabled and updatable. Require `FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV` and explicit approval bound to those exact values immediately before invoking `core.fusion-api.apps-common`. Let the core skill own the internal profile-options child-resource request, including whether it creates a missing value or updates an existing one. Do not retry a write automatically. Re-read the configured value after a successful response.

Treat an unavailable internal profile-options CRUD resource, a privilege rejection, a non-updatable level, or an invalid value as a stop condition. Do not substitute a browser, direct REST client, or FSM import as a workaround.

For an import, hand the exact immutable FSM ZIP and confirmed target environment to `core.data-loader`. Consume its existing FSM validation, approval, adapter, execution, and error contract unchanged. This task skill must not add its own package-origin check, release-compatibility policy, adapter option, or FSM metadata rewrite.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Trading Community Foundation`
- Setup task name: `Manage Customer Account Profile Options`
- Setup task code: `HZ_MANAGE_CUSTOMER_ACCOUNT_PROFILE_OPTIONS`




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

Use the parent functional-area skill `cx.customer-data-management.trading-community-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
