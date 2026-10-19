---
skill_id: "cx.customer-data-management.customer-hub.manage-customer-hub-profile-options"
name: "Manage Customer Hub Profile Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Customer Hub Profile Options under the Customer Hub functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Customer Hub"
functional_area_code: "ZCH_CUST_HUB_OPT"
task_code: "ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS"
task_name: "Manage Customer Hub Profile Options"
parent_skill_id: "cx.customer-data-management.customer-hub"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "operation"
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "profile_option_code"
  - "profile_level"
  - "profile_level_key"
  - "proposed_profile_value"
  - "execution_approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "profile_option_view_result"
  - "profile_option_update_preview"
  - "profile_option_update_result"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-customer-hub-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-customer-hub-profile-options/current/"
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
  - "After exact approval, core.fusion-api.apps-common may create or update one supported Customer Hub profile option value at site level."
  - "Export and import use the declared shared FSM and Core Data Loader workflows with their validation and approval gates."
required_privileges:
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV to create or update profile option values through core.fusion-api.apps-common"
  - "Fusion privileges to view the selected profile option"
---

# Manage Customer Hub Profile Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Customer Hub Profile Options` under `Customer Hub`.

## Setup Task Skill Contract

- task_code: `ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS`
- task_name: `Manage Customer Hub Profile Options`
- parent_skill_id: `cx.customer-data-management.customer-hub`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Customer Hub`
- functional_area_code: `ZCH_CUST_HUB_OPT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Customer Hub Profile Options` under `Customer Hub`.

## Supported Operations

1. `view`: Read the exact profile definition, configured site-level value, and effective authenticated-session value through `core.fusion-api.apps-common`.
2. `manual_update`: Provide the supported Setup and Maintenance procedure. The user performs the save in Fusion.
3. `update`: Create or update one explicitly approved site-level profile value through `core.fusion-api.apps-common` after confirming that the definition is site-enabled and updatable.
4. `export`, `import`, and `validate`: Use the catalog-backed CSV/FSM routes declared below.

Do not use this skill to create or alter profile-option definitions, infer an undocumented valid value, configure product or user levels, or bulk-update unrelated profile options.

## Primary Customer Hub Profile Options

Oracle documents these profile options directly under **Customer Data Management > Customer Hub > Manage Customer Hub Profile Options**. They are configurable at site level only.

| Profile Option Code | Display Name | Documented Default |
|---|---|---|
| `ZCH_CLNS_PROC_BT_SIZE` | Data Cleansing Process Batch Size | `10000` |
| `ZCH_DEDUP_REQUEST_TYPE_OPTION` | Resolution Request Type Default | `Merge` |
| `ZCH_DI_PROC_BT_SIZE` | Duplicate Identification Process Batch Size | `100` |
| `ZCH_USER_MERGE_REQUESTS` | User Merge Requests | Unspecified / null |
| `ZCH_ENABLE_SURVIVORSHIP` | Survivorship Enabled | `Yes` |
| `ZCH_AUTO_LINK_THRESHOLD` | Auto Link Threshold | `0` |
| `ZCH_AUTO_MERGE_THRESHOLD` | Auto Merge Threshold | `100` |
| `ZCH_DI_MERGEREQ_REC_SIZE` | Duplicate Set Record Number | `10` |

For `view`, `manual_update`, or `update`, require an exact code. Treat documented defaults as reference values, not automatic replacements for a user's intended value. Do not infer numeric ranges or enumerations that the current profile definition does not expose.

`ZCH_USER_MERGE_REQUESTS` has three documented states: `Allow Processing Without Approval`, `Process Subject to Approval`, and unspecified/null. Warn that data-steward review requires `Process Subject to Approval`; otherwise flows that require steward review can fail.

## Additional Guarded Customer Hub Profile Options

Oracle documents the following options on the Customer Hub profile-options page but directs administrators to **Manage Profile Options** for definition details and **Manage Administrator Profile Values** for changes. Support `view` and `manual_update`. Permit `update` only after an exact definition read confirms site-level enablement, updateability, and the intended value.

| Profile Option Code | Display Name | Guardrail |
|---|---|---|
| `ORA_ZCH_AGREEMENT_EVALUATION` | Evaluate Agreement Rules | Do not recommend disabling agreement-rule checking; doing so can create orphan data and disrupt application flows. |
| `ORA_ZCH_DEBUG` | Customer Hub Debug Mode | Do not enable unless Oracle Support specifically requests it. |
| `ORA_ZCH_ENABLE_DEFAULT_SOURCE` | Calculate Default Source System for Survivorship Rules | Require confirmation that historical source-system default calculation is intended. |
| `ORA_ZCH_SETATTRIBUTE_OPTIONS` | Attribute Survivorship Null Value Options | Confirm whether null propagation is intended before changing `IGNORE_NULL_VALUE`. |
| `ORA_ZCH_ALLOW_REMOVE_FEATURE` | Remove Records From Merge Processing | Do not recommend changing the documented default `N`; removal can create orphan records. |
| `ORA_ZCH_ACCOUNT_BATCH_ENRICHMENT_IMPORT_MAP` | Account Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |
| `ORA_ZCH_ADDITIONAL_NAME_BATCH_ENRICHMENT_IMPORT_MAP` | Additional Name Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |
| `ORA_ZCH_ADDITIONAL_IDENTIFIER_BATCH_ENRICHMENT_IMPORT_MAP` | Additional Identifier Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |
| `ORA_ZCH_CLASSIFICATION_BATCH_ENRICHMENT_IMPORT_MAP` | Classification Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |
| `ORA_ZCH_ADDRESS_BATCH_ENRICHMENT_IMPORT_MAP` | Address Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |
| `ORA_ZCH_CONTACT_BATCH_ENRICHMENT_IMPORT_MAP` | Contact Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |
| `ORA_ZCH_CONTACT_POINT_BATCH_ENRICHMENT_IMPORT_MAP` | Contact Point Enrichment Map | Resolve the selected Import Management mapping; do not invent a mapping name. |

If the exact task inventory in the target environment disagrees with this documented inventory, stop with `catalog_or_metadata_mismatch`, report the discrepancy, and do not write the disputed option.

## Oracle Documentation

Use Oracle's [Customer Hub Profile Options](https://docs.oracle.com/en/cloud/saas/sales/oacdm/customer-hub-profile-options.html) as the source-aligned reference for the option inventory, site-level constraint, documented defaults, special warnings, and supported Setup and Maintenance procedures. Use Oracle's [Automerge](https://docs.oracle.com/en/cloud/saas/sales/oacdm/automerge.html) when validating the interaction among the auto-merge threshold, duplicate-set record size, and survivorship options. Confirm current documentation and the live profile definition before preparing a change.

## View and Change Profile Option Values

For `view`, use `core.fusion-api.apps-common` to read the exact profile definition and its configured site-level value. Read the authenticated-session `profileValues` resource only to verify the effective value; it is not a configured-value write route.

For `manual_update`, direct the user to the exact `Manage Customer Hub Profile Options` setup task for the primary options. For an additional guarded option, use **Manage Profile Options** to inspect its definition and **Manage Administrator Profile Values** to change its value. Re-read the configured and effective values afterward when verification is required.

For `update`, display the target environment, profile option code, site-level key, current value, proposed value, definition updateability, and all applicable guardrails. Require `FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV` and explicit approval bound to those exact values immediately before invoking `core.fusion-api.apps-common`. Let the core skill own the internal `profileOptions` child-resource request, including whether it creates a missing site value or updates an existing one. Do not retry a write automatically. Re-read the configured value after success and return the HTTP outcome plus ECID or request ID when available.

Treat an unavailable internal profile-options CRUD resource, a privilege rejection, a non-updatable or non-site definition, an invalid value, or an unresolved enrichment mapping as a stop condition. Do not substitute a browser, direct REST client, or FSM import as a workaround.

## Setup Task Metadata

- Task name: `Manage Customer Hub Profile Options`
- Task code: `ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Customer Hub`
- Setup task name: `Manage Customer Hub Profile Options`
- Setup task code: `ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS`

For an import, hand the exact immutable FSM ZIP and confirmed target environment to `core.data-loader`. Consume its existing FSM validation, approval, adapter, execution, and error contract unchanged. This task skill must not add its own package-origin check, release-compatibility policy, adapter option, or FSM metadata rewrite.

## Preflight and Error Handling

Before any view, update, export, validation, or import, load the task-local `ora_input_validation.md`, `ora_dependency_readiness.md`, `ora_reference_lookups.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` guidance. Load `ora_defaulting_rules.md` when a documented default or override decision is relevant.

Confirm the exact task code, target environment, requested operation, site-level constraint, required privilege, profile-option membership, and immutable artifact or approved value before any side effect. Classify failures using the task-local error guidance and the selected shared or core workflow contract. Do not automatically retry a live profile-value write or FSM import. Preserve returned request IDs, ProcessIds, ECIDs, status, and ProcessLog references when available.

Redact credentials, access tokens, token-cache contents, client secrets, full base64 payloads, and sensitive configuration values from output and persisted diagnostics.

For FSM polling and timeout behavior, consume `core.data-loader` without redefining its wait interval or timeout. On timeout, preserve the target, TaskCode, ProcessId, last status, elapsed wait, and status-only next action.

## Golden Scenarios

| Scenario | Expected Result |
|---|---|
| View `ZCH_AUTO_MERGE_THRESHOLD` at SITE | Return the exact definition, configured SITE value, and effective session value without mutation. |
| Update `ZCH_ENABLE_SURVIVORSHIP` with an unchanged approved preview | Execute one Apps Common write, re-read SITE, and return verified evidence. |
| Request a USER-level Customer Hub value | Stop during input validation; do not select another level. |
| Enable `ORA_ZCH_DEBUG` without stated Oracle Support direction | Stop at the guarded-option design gate before preview. |
| Import an exact-task FSM ZIP whose bytes changed after approval | Reject stale approval and require validation of the new SHA-256. |
| Receive an uncertain direct-write or import response | Reconcile by read-only lookup; do not replay the mutation automatically. |




## Inputs

- `operation`
- `implementation_objective`
- `project_context`
- `fusion_environment_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `profile_option_code`
- `profile_level`
- `profile_level_key`
- `proposed_profile_value`
- `execution_approval`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `profile_option_view_result`
- `profile_option_update_preview`
- `profile_option_update_result`
- `execution_result`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.customer-hub` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
