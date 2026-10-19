---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-data-format-profile-options"
name: "Manage Data Format Profile Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Data Format Profile Options under the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_DATA_FORMAT_PROFILE_OPTIONS"
task_name: "Manage Data Format Profile Options"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.2.0"
inputs:
  - "operation"
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "profile_option_name"
  - "profile_level"
  - "profile_level_key"
  - "proposed_profile_value"
  - "execution_approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-data-format-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-data-format-profile-options/current/"
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
  - "Reads profile option definitions and configured values through core.fusion-api.apps-common when the view operation is selected."
  - "After an exact approval, core.fusion-api.apps-common may create or update one profile option value at the approved level."
  - "Export and import are routed through their declared FSM and Data Loader skills, each with its own validation and approval gates."
required_privileges:
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV to create or update profile option values through core.fusion-api.apps-common"
  - "Fusion privileges to view the selected profile option"
---

# Manage Data Format Profile Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Data Format Profile Options` under `Trading Community Foundation`.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_DATA_FORMAT_PROFILE_OPTIONS`
- task_name: `Manage Data Format Profile Options`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Data Format Profile Options` under `Trading Community Foundation`.

## Supported Operations

1. `view`: Read the profile definition, configured value at the requested level, and the effective authenticated-session value through `core.fusion-api.apps-common`.
2. `manual_update`: Provide the supported Setup and Maintenance procedure for a user to update a profile value manually. The user performs the save in Fusion; this skill does not treat UI navigation as a REST update.
3. `update`: Create or update one explicitly approved site, product, or user-level profile value through `core.fusion-api.apps-common`.
4. `export`, `import`, and `validate`: Use the CSV/FSM routing declared below.

Do not use this skill to create or alter profile-option definitions, infer a valid value, or bulk-update unrelated profile options.

## Supported Profile Options

This task owns exactly these profile options in the validated `cptcpuwqy` task inventory:

| Profile Option Code | Display Name |
|---|---|
| `HZ_DEFAULT_ADDR_STYLE` | Address Style Default |
| `HZ_DEFAULT_NAME_STYLE` | Name Style Default |

For `view`, `manual_update`, or `update`, require an exact code from this table. For FSM validation, reject profile-option rows owned by another task. If a completed export omits an expected code, report `export_content_discrepancy` with the missing codes; do not call a structurally valid ZIP corrupt and do not invent the omitted rows.

## Setup Task Metadata

- Task name: `Manage Data Format Profile Options`
- Task code: `HZ_MANAGE_DATA_FORMAT_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Oracle Documentation

Use Oracle's [Foundation Profile Options](https://docs.oracle.com/en/cloud/saas/sales/oacdm/trading-community-model-profile-options.html) as the source-aligned reference for this task. It documents the `HZ_DEFAULT_NAME_STYLE` and `HZ_DEFAULT_ADDR_STYLE` profile options, their default values, impacts, and the supported Setup and Maintenance procedure for changing administrator profile values. Confirm the applicable profile-option code and the intended value against the current Oracle documentation before preparing or importing setup data.

## View and Change Profile Option Values

For `view`, use `core.fusion-api.apps-common` to read the exact profile definition and its level-specific configured value. Read the authenticated-session `profileValues` resource only to verify the effective value; it is not a configured-value write route.

For `manual_update`, instruct the user to open **Setup and Maintenance > Manage Administrator Profile Values**, search by the exact profile option code, select the required level, enter the intended value, and save. Re-read the configured and effective values afterward when verification is required.

For `update`, first resolve and display the target environment, profile option code, level and level key, current value, proposed value, and whether that level is enabled and updatable. Require `FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV` and explicit approval bound to those exact values immediately before invoking `core.fusion-api.apps-common`. The core skill owns the internal `profileOptions` child-resource request, including whether it must create a missing value or update an existing one. Do not retry a write automatically. Re-read the configured value after a successful response and return the HTTP outcome plus ECID or request ID when available.

Treat an unavailable internal profile-options CRUD resource, a privilege rejection, a non-updatable level, or an invalid value as a stop condition. Do not substitute a browser, direct REST client, or an FSM import as a workaround.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

For an import, hand the exact immutable FSM ZIP and confirmed target environment
to `core.data-loader`. Consume its existing FSM validation, approval, adapter,
execution, and error contract unchanged. This task skill must not add its own
source-environment equality check, release-compatibility policy, adapter option,
or FSM metadata rewrite.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Trading Community Foundation`
- Setup task name: `Manage Data Format Profile Options`
- Setup task code: `HZ_MANAGE_DATA_FORMAT_PROFILE_OPTIONS`

## Preflight and Error Handling

Before any view, preview, update, export, validation, or import, load the
task-local `ora_input_validation.md`, `ora_dependency_readiness.md`, and
`ora_error_handling.md` guidance. Confirm the exact task code, target
environment, requested operation, required privilege, and immutable artifact or
approved value before any side effect.

Classify and report every failure using the task-local error guidance and the
selected shared or core workflow contract. Do not automatically retry a live
profile-value write or FSM import. Preserve returned request IDs, ProcessIds,
ECIDs, status, and ProcessLog references when available.

Redact credentials, access tokens, token-cache contents, client secrets, full
base64 payloads, and sensitive configuration values from output and persisted
diagnostics.




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
