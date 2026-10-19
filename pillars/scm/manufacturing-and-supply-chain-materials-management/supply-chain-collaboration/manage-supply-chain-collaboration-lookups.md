---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-collaboration.manage-supply-chain-collaboration-lookups"
name: "Manage Supply Chain Collaboration Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Supply Chain Collaboration Lookups under the Supply Chain Collaboration functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Collaboration"
functional_area_code: "ORA_VCS_SUPPLY_COLLABORATION"
setup_task_code: "ORA_VCS_MANAGE_COMMON_LOOKUPS"
setup_task_name: "Manage Supply Chain Collaboration Lookups"
task_code: "ORA_VCS_MANAGE_COMMON_LOOKUPS"
task_name: "Manage Supply Chain Collaboration Lookups"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-collaboration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/release/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
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
  - "shared.setup-import.task-level-import"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-collaboration/manage-supply-chain-collaboration-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-collaboration/manage-supply-chain-collaboration-lookups/current/"
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

# Manage Supply Chain Collaboration Lookups

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Supply Chain Collaboration Lookups` under `Supply Chain Collaboration`.

## Setup Task Skill Contract

- task_code: `ORA_VCS_MANAGE_COMMON_LOOKUPS`
- task_name: `Manage Supply Chain Collaboration Lookups`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.supply-chain-collaboration`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Supply Chain Collaboration`
- functional_area_code: `ORA_VCS_SUPPLY_COLLABORATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/release/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Supply Chain Collaboration Lookups` under `Supply Chain Collaboration`.

## Setup Task Metadata

- Task name: `Manage Supply Chain Collaboration Lookups`
- Task code: `ORA_VCS_MANAGE_COMMON_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `shared.setup-import.task-level-import`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Supply Chain Collaboration`
- Setup task name: `Manage Supply Chain Collaboration Lookups`
- Setup task code: `ORA_VCS_MANAGE_COMMON_LOOKUPS`

## Lookup API Routing

Route every Supply Chain Collaboration lookup task to
`core.fusion-api.apps-common`. Pass the complete allowed lookup-type list
below in the core request as `lookup_types`, set `lookup_view` to `standard`,
and request the `LookupType`, `Meaning`, and `Description` fields. Do not add
Fusion authentication or REST transport logic to this pillar skill. The
allowed lookup types are:

- `ORA_VCS_AGGREG_LEVEL`, `ORA_VCS_ALL`, `ORA_VCS_BO_LOAD_STATUS`, `ORA_VCS_BUCKET_AGGR_LEVEL`, `ORA_VCS_COLLABORATOR_STATUS`, `ORA_VCS_COLLAB_BOUNDARY_TYPE`, `ORA_VCS_COLLAB_CYCLE_FILTER_OP`, `ORA_VCS_COLLAB_MEASURES_TYPES`
- `ORA_VCS_COLLAB_ORDER_TYPES`, `ORA_VCS_COLLAB_PLAN_STATUS`, `ORA_VCS_COLLAB_UOM_SOURCE_CODE`, `ORA_VCS_COMMIT_PERIOD`, `ORA_VCS_COMMIT_QUANTITY`, `ORA_VCS_COMMIT_SOURCE`, `ORA_VCS_CP_DL_AGGR_LEVEL`, `ORA_VCS_CP_DL_HORIZON`
- `ORA_VCS_CP_DL_LAYOUT`, `ORA_VCS_DATA_RECEIVED_STATUS`, `ORA_VCS_DISPLAYED_PLANS`, `ORA_VCS_DISPLAYED_RELATIONSHIP`, `ORA_VCS_DOC_ACTIONS`, `ORA_VCS_DOC_REQUEST_STATUS`, `ORA_VCS_DWNLD_TMP_OPTIONS`, `ORA_VCS_EDIT_ATTR_ACTION`
- `ORA_VCS_EDIT_FORECAST_SELECT`, `ORA_VCS_EXCEPTION_TYPES`, `ORA_VCS_FILE_DELIMITER`, `ORA_VCS_FORECAST_PROCESS_STATU`, `ORA_VCS_FRCST_REVIEW_TYPES`, `ORA_VCS_INTEGRATION_STATUS`, `ORA_VCS_ITEM_RESOLUTION`, `ORA_VCS_KPI_BADGE_STATUS`
- `ORA_VCS_LASTPUBLISHED`, `ORA_VCS_LVL_CUSTOMER`, `ORA_VCS_LVL_ITEM`, `ORA_VCS_LVL_ORGANIZATION`, `ORA_VCS_MEASURE_ACTIONS`, `ORA_VCS_MEASURE_BOUNDARY_TYPE`, `ORA_VCS_NUM_FORMAT`, `ORA_VCS_PARTY_ORIGIN`
- `ORA_VCS_PLANCYCLE_STARTDAY_ORD`, `ORA_VCS_PLAN_BUCKET_TYPE`, `ORA_VCS_PLAN_CYCLE_FRQ`, `ORA_VCS_PLAN_CYCLE_START_TYPE`, `ORA_VCS_PLAN_EDIT_OPTIONS`, `ORA_VCS_PLAN_WATCHLIST`, `ORA_VCS_PROCESS_STATUS`, `ORA_VCS_PUBLISHER_ORDER_CODE`
- `ORA_VCS_PUB_PARTY`, `ORA_VCS_PUB_SOURCE`, `ORA_VCS_REASON_CODES`, `ORA_VCS_RELATIONSHIP_TYPE`, `ORA_VCS_SECURITY_CONTEXT`, `ORA_VCS_SLA_ACTION`, `ORA_VCS_SOURCE_SYSTEM`, `ORA_VCS_SUPPLYDATA_OBJ_TYPES`
- `ORA_VCS_SUPPLY_COLLAB_OBJECT`, `ORA_VCS_SUPPLY_DATA_STATUS`, `ORA_VCS_SUPPLY_PLAN_SOURCE`, `ORA_VCS_SYNC_PROFILE_STATUS`, `ORA_VCS_UOM_STRATEGY`, `ORA_VCS_UPLOAD_ERROR_TYPES`, `ORA_VCS_UPLOAD_INTENTION`, `ORA_VCS_UPLOAD_TYPE`
- `ORA_VCS_VMI_DWNLD_TMP_OPTIONS`, `ORA_VCS_VMI_EXCEPTION_CONTEXT`, `ORA_VCS_VMI_INV_PLAN_OWNER`, `ORA_VCS_VMI_ITEM_STATUS`, `ORA_VCS_VMI_MIN_MAX_ORIGIN`, `ORA_VCS_VMI_RELATIONSHIP_SCOPE`, `ORA_VCS_VMI_RELATIONSHIP_STATU`, `ORA_VCS_VMI_REPL_LIFE_CYCLE`
- `ORA_VCS_VMI_REQDATE_OPERATOR`, `ORA_VCS_VMI_REQUEST_STATUS`, `ORA_VCS_VMI_REQ_REPL`, `ORA_VCS_VMI_TOP_REQ_REPL`, `ORA_VCS_WEEKDAY`, `ORA_VCS_YES_NO`

Do not omit an allowed lookup type from the core request. For a requested
lookup type outside this list, stop and report that it is not in this task's
approved routing scope. For writes, use the core skill's read-first and
explicit-approval requirements.

## Lookup Results

When listing approved lookup types, include the meaning and description
associated with each type. Return one row per lookup type using these fields:

| Field | Purpose |
| --- | --- |
| `LookupType` | Identifies the approved Supply Chain Collaboration lookup type. |
| `Meaning` | Provides the user-facing label for the lookup type. |
| `Description` | Provides the explanatory text associated with the lookup type. |

Read the standard lookup-type resource through `core.fusion-api.apps-common`
without expanding its lookup codes. Preserve the `Meaning` and `Description`
returned by Fusion; do not infer either value from the lookup type. If a
description is null or absent, report it as `Not provided` rather than
fabricating a description.


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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.supply-chain-collaboration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
