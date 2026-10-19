---
skill_id: "cx.customer-data-management.data-quality-foundation.manage-data-quality-lookups"
name: "Manage Data Quality Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Data Quality Lookups under the Data Quality Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Data Quality Foundation"
functional_area_code: "ORA_ZCQ_DATA_QLTY_FOUNDATION"
task_code: "ZCQ_MANAGE_DATA_QUALITY_LOOKUPS"
task_name: "Manage Data Quality Lookups"
parent_skill_id: "cx.customer-data-management.data-quality-foundation"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/data-quality-foundation/manage-data-quality-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/data-quality-foundation/manage-data-quality-lookups/current/"
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

# Manage Data Quality Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Data Quality Lookups` under `Data Quality Foundation`.

## Setup Task Skill Contract

- task_code: `ZCQ_MANAGE_DATA_QUALITY_LOOKUPS`
- task_name: `Manage Data Quality Lookups`
- parent_skill_id: `cx.customer-data-management.data-quality-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Data Quality Foundation`
- functional_area_code: `ORA_ZCQ_DATA_QLTY_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/release/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Data Quality Lookups` under `Data Quality Foundation`.

## Setup Task Metadata

- Task name: `Manage Data Quality Lookups`
- Task code: `ZCQ_MANAGE_DATA_QUALITY_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Data Quality Foundation`
- Setup task name: `Manage Data Quality Lookups`
- Setup task code: `ZCQ_MANAGE_DATA_QUALITY_LOOKUPS`


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

Use the parent functional-area skill `cx.customer-data-management.data-quality-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Task-specific lookup baseline

The exact-task Fusion page establishes this closed 21-type Standard lookup inventory:

| Lookup type | Scope |
|---|---|
| `ZCQ_IIR_MATCH_TOLERANCE` | Match tolerance |
| `ZCQ_ADDR_CLEANSED_STATUS` | Address cleansing status |
| `ZCQ_BATCH_MATCH_MODE` | Batch match mode |
| `ZCQ_PARAMETER_LEVEL` | Parameter level |
| `ZCQ_PARAMETER_TYPE` | Parameter type |
| `ZCQ_SORT_BY_SCORE` | Sort by score |
| `ZCQ_BATCH_PURGE_MODE` | Batch purge mode |
| `ZCQ_BATCH_STATUS` | Batch status |
| `ZCQ_BATCH_TYPE` | Batch type |
| `ZCQ_IIR_ASM_CHARSET` | IIR address cleansing character set |
| `ZCQ_IIR_ASM_FORCE_COUNTRY` | IIR forced country |
| `ZCQ_IIR_ASM_VAL_MODE` | IIR address validation mode |
| `ZCQ_OPERATIONS` | Data quality operations |
| `ZCQ_ORG_MATCH_OPTION_CODE` | Organization match option |
| `ZCQ_ASM_ATTRIBUTES` | Address cleansing attributes |
| `ZCQ_BATCH_REQUESTOR_TYPE` | Batch requestor type |
| `ZCQ_ENTITY` | Data quality entity |
| `ZCQ_IIR_SEARCH_WIDTH` | IIR search width |
| `ZCQ_PARAMETER_CARDINALITY` | Parameter cardinality |
| `ZCQ_PER_MATCH_OPTION_CODE` | Person match option |
| `ZCQ_IIR_ASM_PREF_LANG_TYPE` | IIR preferred language type |

Do not infer additional members from the `ZCQ_` prefix, module, or meaning. A current exact GET must reconfirm Standard category, configuration level, codes, seeded origin, and REST-described fields before a live operation.

## Supported operations and safety contract

- Read-only listing and exact type/code retrieval are supported without approval after task-membership resolution.
- Lookup-type creation/deletion, identity changes, category changes, module changes, configuration-level changes, REST-security changes, and seeded-identity changes are unsupported.
- Custom-code create, update, or delete is conditional on current configuration-level rules, `CreatedBy` seed evidence, and current REST describe. Never silently upsert and reject custom codes beginning with `ORA_`.
- Before a manual mutation, show one exact redacted preview bound to environment, method, endpoint, before/after state, payload, impact, and fingerprint; require explicit approval; send exactly one request through the shared Fusion REST client; never automatically retry; verify separately with GET.
- Export with `shared.setup-export.task-level-export` using exact TaskCode `ZCQ_MANAGE_DATA_QUALITY_LOOKUPS`. Validate with both shared validators and route import only through `core.data-loader`.
- An FSM import must preserve immutable ZIP bytes, contain exactly one safe `ASM_SETUP_CSV_METADATA.xml`, identify only this exact TaskCode, pass the Core Data Loader Task Hook, and retain an approval-bound SHA-256 envelope through submission.

See `ora-resource/` for the executable validation, lookup, design, and error rules.
