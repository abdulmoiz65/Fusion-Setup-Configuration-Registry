---
skill_id: "cx.customer-data-management.customer-hub.manage-customer-data-management-options"
name: "Manage Customer Data Management Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Customer Data Management Options under the Customer Hub functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Customer Hub"
functional_area_code: "ZCH_CUST_HUB_OPT"
task_code: "ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS"
task_name: "Manage Customer Data Management Options"
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
  - "requested_option_changes"
  - "execution_approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "fsm_export_package"
  - "profile_option_change_preview"
  - "profile_option_change_result"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-customer-data-management-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-customer-data-management-options/current/"
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
  - "Creates and downloads a task-scoped FSM CSV export through shared.setup-export.task-level-export."
  - "After Core Data Loader validation and approval, may import an immutable FSM ZIP containing reviewed profile-value changes."
  - "After an exact direct-update preview and approval, may create or update one supported site-level profile value through core.fusion-api.apps-common."
required_privileges:
  - "Fusion privileges to export and import setup task CSV data."
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV for a direct site-level profile-value update."
---

# Manage Customer Data Management Options

## Purpose

Export, review, change, import, and validate only the profile-option-backed settings exposed by `Manage Customer Data Management Options` under `Customer Hub`.

## Setup Task Skill Contract

- task_code: `ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS`
- task_name: `Manage Customer Data Management Options`
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

## Supported Operations

1. `export`: Export this exact task with `shared.setup-export.task-level-export` and preserve the returned ZIP as an immutable baseline.
2. `prepare_import`: Copy the baseline, change only existing `FND_APP_PROFILE_VALUE.csv` SITE rows for supported codes, validate the package, and produce an exact before/after preview.
3. `import`: Submit the reviewed immutable ZIP only through `core.data-loader` in FSM mode and use its approval workflow unchanged.
4. `view`: Read one supported profile definition and configured SITE value through `core.fusion-api.apps-common`.
5. `update_one`: Create or update one supported SITE value through `core.fusion-api.apps-common` after an exact preview and explicit approval. Use this route when a supported profile is omitted from an otherwise successful task export; never synthesize an absent FSM row.
6. `validate` or `status`: Validate the artifact or continue an existing export/import process without creating another mutation.

Reject arbitrary profile-option codes, product or user levels, profile-option definition changes, loose CSV imports, and edits to audit columns or unrelated task rows.

## Supported Option Inventory

The inventory is closed. UI labels are aliases; runtime validation and CSV edits use the stored codes below. Lookup-backed values must also be active in the target environment when the preview is built.

### Duplicate Identification

| Setting | Profile Option Code | Stored Values |
|---|---|---|
| Enable Real-Time Key Generation | `ORA_ZCQ_ENABLE_REALTIME_KEYGEN` | `Y`, `N` |
| Number of Batch Key Generation Jobs | `ZCQ_BATCH_KEYGEN_NUMJOBS` | Positive integer; Oracle publishes no maximum |
| Number of Batch Matching Jobs | `ZCQ_BATCH_MATCH_NUMJOBS` | Positive integer; Oracle publishes no maximum |
| Number of Real-Time Possible Duplicates | `ORA_ZCQ_MAX_CANDIDATES` | Positive integer; documented default `20` |
| Batch Duplicate Identification Debug Level | `ORA_ZCQ_BATCHMATCH_DEBUG_LEVEL` | `DEBUG`, `INFO` |
| Enable Fine Logging for Match Value Conversion | `ORA_ZCQ_CONVERTER_FINEST_LOGGING` | `Y`, `N` |

### Duplicate Resolution

| Setting | Profile Option Code | Stored Values |
|---|---|---|
| Maximum Concurrent Resolution Request Jobs | `ORA_ZCH_MERGE_MAX_REQUEST_LIMIT` | Positive integer or blank; documented default `10` |
| Merge Mode | `ORA_ZCH_OPTIMIZE_LOAD` | `Y` optimized, `N` standard |
| Resolution Request Job Size | `ORA_ZCH_MERGE_REQUEST_BATCH_SIZE_LIMIT` | Positive integer or blank; documented default `100` |
| Merge Scope | `ORA_ZCH_MERGE_SCOPE` | `ALL`, `CDM`, `CRM`, `CDM_HV` |
| Merge Request Notifications | `ZCH_REQUEST_NOTIFICATIONS` | `ORA_ZCH_NOTIFICATION_DEF_YES`, `ORA_ZCH_NOTIFICATION_DEF_NO`, `ORA_ZCH_NOTIFICATION_DISABLED` |
| Automerge Threshold | `ZCH_AUTO_MERGE_THRESHOLD` | Integer `0` through `101`; `101` disables automerge |
| Customer Center Merge Requests | `ZCA_MERGE_REQUEST` | `Y`, `N` |
| Default Resolution Type | `ZCH_DEDUP_REQUEST_TYPE_OPTION` | `MERGE`, `CHOICE`, `LINK`, `LINK_DUP` |
| Data Steward Resolution Request Handling | `ORA_ZCH_DS_MERGE_REQUESTS` | `ZCH_PROCESS_WITHOUT_APPROVAL`, `ZCH_SUBMIT_FOR_APPROVAL` |
| User Resolution Request Handling | `ZCH_USER_MERGE_REQUESTS` | `ZCH_PROCESS_WITHOUT_APPROVAL`, `ZCH_SUBMIT_FOR_APPROVAL` |
| Agreement Rules Type | `ZCH_AGREEMENT_TYPE` | `ORA_ZCH_DEFAULT`, `ORA_ZCH_GROOVY`, `ORA_ZCH_RULE` |
| Attribute Selection Type | `ZCH_SETATTRIBUTE_TYPE` | `ORA_ZCH_NONE`, `ORA_ZCH_SC_OLDEST`, `ORA_ZCH_SC_NEWEST`, `ORA_ZCH_RULE` |
| Enable Attribute Source Tracking | `ZCH_ENABLE_SURVIVORSHIP` | `Y`, `N`; once enabled, do not disable |
| Master Record Selection | `ORA_ZCH_SETMASTER_TYPE` | `RULE`, `OLDEST`, `NEWEST`, `ANY`, `ORA_ZCH_GROOVY` |
| Merge Identical Child Records | `ORA_ZCH_MERGE_IDENTICAL` | `Y`, `N` |
| Add Groovy to Attribute Selection | `ZCH_GROOVY_RULE` | `Y`, `N` |
| Main Record Selection for Link | `ORA_ZCH_LINK_SETMAIN_TYPE` | `ANY`, `NEWEST`, `OLDEST`, `ORA_ZCH_GROOVY`, `ORA_ZCH_QUALITY_SCORE` |
| Autolink Threshold | `ZCH_AUTO_LINK_THRESHOLD` | Integer `0` through `101`; `101` disables autolink |

The exact UI meaning for each lookup code is resolved through the lookup type named by the live profile definition. Do not replace a stored code with its display label.

## FSM CSV Change Workflow

1. Export exact TaskCode `ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS` and retain the original ZIP and SHA-256.
2. Require exactly one safe `ASM_SETUP_CSV_METADATA.xml` and the task identity in its metadata. For a profile-value edit, require `FND_APP_PROFILE_VALUE.csv`.
3. Match an existing row by profile code, application id, `LevelName=SITE`, and `LevelValue=SITE`. Modify only `ProfileOptionValue` in a copied package.
4. Never add an absent row. Report `export_content_discrepancy` and use `update_one` only after the live definition confirms SITE is enabled and updatable.
5. Validate every requested value against this inventory and, for lookup-backed values, against the current active lookup codes.
6. Show target environment, task, option code, UI meaning, current stored value, proposed stored value, ZIP path, and SHA-256. Any change invalidates approval.
7. Route the immutable reviewed ZIP to `core.data-loader`; do not duplicate its Task Hook, adapter, approval, submission, polling, or retry logic.
8. After import, re-export or read every affected configured SITE value and run the task's `Validate Setup` process. Never report success from submission alone.

For `update_one`, perform the same membership, level, value, dependency, preview, approval, and verification gates, then let `core.fusion-api.apps-common` own the profile-value child-resource operation. Do not retry a POST or PATCH automatically.

## Design Constraints

- Source-confidence attribute selection requires `ZCH_ENABLE_SURVIVORSHIP=Y`.
- Once attribute source tracking is enabled, block a request to set it to `N`.
- `CDM_HV` merge scope is incompatible with business-rule or Groovy-based master, attribute, or agreement selection.
- `ZCH_GROOVY_RULE=Y` is incompatible with `ZCH_SETATTRIBUTE_TYPE=ORA_ZCH_RULE`.
- Autolink threshold applies to link resolution; automerge threshold applies to merge resolution.
- Blank handling is supported only for options whose Oracle contract explicitly permits no value. Do not translate blank, null, and an empty quoted CSV field interchangeably without target evidence.

## Sources and Runtime Evidence

Use current Oracle Customer Data Management documentation for setting purpose, UI grouping, defaults, and dependency rules. Treat the target profile definition, profile levels, active lookup codes, and fresh task export as runtime authority for stored codes, eligibility, current values, and package shape. A mismatch is a blocker, not permission to broaden the inventory.

Oracle documentation:

- [Getting Started with Your Customer Data Management Implementation](https://docs.oracle.com/en/cloud/saas/customer-data-management/fagcd/getting-started-with-your-customer-data-management-cdm-implementation.pdf)
- [Manage Customer Data Management Options](https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/Chunk106261974.html)
- [Implementing Applications](https://docs.oracle.com/en/cloud/saas/applications-common/26b/facia/implementing-applications.pdf)

## Golden Scenarios

1. **Existing exported row:** Export the exact task, change `ORA_ZCH_MERGE_SCOPE` from one active stored lookup code to another in its existing SITE row, produce a ZIP/hash-bound preview, and import only through Core Data Loader after its approval gate.
2. **Profile omitted from export:** When `ORA_ZCQ_MAX_CANDIDATES` is absent from `FND_APP_PROFILE_VALUE.csv`, report `export_content_discrepancy`; verify its live SITE definition and use `update_one` only after an exact direct-update preview and approval.
3. **Display label supplied:** If a user supplies `All functional areas` instead of stored code `ALL`, resolve and display the mapping but require the exact code in the reviewed change. Never write the UI label to CSV or the profile-value REST resource.
4. **Unsafe dependency:** Block `ZCH_ENABLE_SURVIVORSHIP=N` after source tracking has been enabled, and block a `CDM_HV` merge scope combined with incompatible business-rule or Groovy selections.

## Setup Task Metadata

- Task name: `Manage Customer Data Management Options`
- Task code: `ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS`
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
- Setup task name: `Manage Customer Data Management Options`
- Setup task code: `ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS`

For import, provide the exact immutable ZIP and target environment to Core Data Loader. Do not rewrite `ASM_SETUP_CSV_METADATA.xml` or construct a replacement package from loose CSV files.

## Preflight and Error Handling

Load the task-local `ora-resource` files before preview or execution. Confirm the fixed task identity, environment, requested operation, closed inventory membership, SITE eligibility, current value, allowed stored value, dependencies, immutable artifact, and required approval. Classify and persist failures using the task-local error contract. Redact credentials, tokens, client secrets, token-cache contents, Authorization headers, full base64 packages, and sensitive values.




## Inputs

- `operation`
- `implementation_objective`
- `project_context`
- `fusion_environment_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `requested_option_changes`
- `execution_approval`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `fsm_export_package`
- `profile_option_change_preview`
- `profile_option_change_result`
- `execution_result`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.customer-hub` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
