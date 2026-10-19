---
skill_id: "scm.order-management.channel-revenue-management.manage-channel-claim-reasons"
name: "Manage Channel Claim Reasons Setup Task Guidance"
description: "Provides task-specific create and update guidance for Manage Channel Claim Reasons, including operation-specific writable fields, existing-record resolution, and approved Data Loader submission."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
task_code: "ORA_CJM_MANAGE_CLAIM_REASONS"
task_name: "Manage Channel Claim Reasons"
parent_skill_id: "scm.order-management.channel-revenue-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "channelClaimReasons"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.2.1"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/manage-channel-claim-reasons/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/manage-channel-claim-reasons/current/"
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

# Manage Channel Claim Reasons Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Channel Claim Reasons` under `Channel Revenue Management`.

## Setup Task Skill Contract

- task_code: `ORA_CJM_MANAGE_CLAIM_REASONS`
- task_name: `Manage Channel Claim Reasons`
- parent_skill_id: `scm.order-management.channel-revenue-management`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Channel Revenue Management`
- functional_area_code: `ORA_FOM_CHANNEL_REV_MGMT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `channelClaimReasons`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Claim Reasons` under `Channel Revenue Management`.

## Setup Task Metadata

- Task name: `Manage Channel Claim Reasons`
- Task code: `ORA_CJM_MANAGE_CLAIM_REASONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `channelClaimReasons`

## CSV Export, Import, and Validation Workflow

For create or update preparation, read the task resources in this order: [input validation and update fields](ora-resource/ora_input_validation.md), [dependency readiness](ora-resource/ora_dependency_readiness.md), [reference lookups](ora-resource/ora_reference_lookups.md), [create-only defaults](ora-resource/ora_defaulting_rules.md), and [gates and errors](ora-resource/ora_error_handling.md). Use the compiled task graph through core.data-loader Task Hook; do not invoke Fusion writes from these resources.

Before mapping or rejecting renamed CSV/XLSX headers, read the [task-scoped date-header mapping rules](ora-resource/ora_input_validation.md#date-header-mapping). Apply these aliases through the existing core.data-loader mapping options after confirming the target attributes in live metadata. Mapping does not replace final-artifact Task Hook validation or upload approval.

Accept `SetId`, `SetCode`, or `SetName` as alternative set identifiers for create and update identity. Follow [set identity preparation](ora-resource/ora_input_validation.md#set-identity-preparation) before loader mapping: verify supplied identifiers, including COMMON's `SetId = 0`, and prepare supported code/name fields without changing the user's workbook. SetId is intake-only, not a writable update field.

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using channelClaimReasons as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Claim Reasons`
- Setup task code: `ORA_CJM_MANAGE_CLAIM_REASONS`

## Update Existing Claim Reasons

1. Require explicit update intent. Identify the existing reason by `ClaimReasonCode` and at least one of `SetId`, `SetCode`, or `SetName`, resolved to one consistent set; an optional `ClaimReasonId` must agree with the lookup. These are identity values, not fields to rename or reassign.
2. Accept every field in the operation-specific [Update Fields contract](ora-resource/ora_input_validation.md#update-fields), not only description and end date. Confirm live loader support before preparation. Response fields and create fields do not automatically become update fields.
3. Keep preparation separate from final Task Hook validation. Resolve needed keys/current values through the declared read-only lookup in the selected workflow, prepare only requested changes with verified identity/control columns and `RestAction=PATCH`, then run Data Loader preflight and Task Hook on the final immutable artifact. If final validation discovers required corrections, restart preparation rather than edit the archive.
4. Preserve omitted values; do not apply create defaults. Validate effective dates using current Fusion values, distinguish explicit nullable clears from blank cells, and block missing/ambiguous targets, duplicate targets, unsupported changes, and unverified loader semantics. No upsert, delete, or direct PATCH fallback is authorized.
5. Return a before/after preview for the exact existing record and changes. Task rules return validation readiness first; Task Hook then builds the preview, records the user's approval, and verifies the archive. A rule registry or ready terminal is never upload approval. Continue only through the existing core.data-loader submission workflow.
6. Do not refresh lookups or mutate the archive after approval; follow core.data-loader's immutable-preflight contract. If fresh evidence is needed, invalidate the pending preview and restart. Do not promise concurrency protection the loader does not provide. Initiation is not row-level success; retrieve status/errors only when requested through the normal loader workflow.

This is assisted task support using existing core services, not a new REST client. Public API update fields unsupported by the selected environment's loader remain explicit route blockers rather than silently omitted changes.

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `channelClaimReasons` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "channelClaimReasons" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

For an update workbook, add `--operation update` to the same command. A generic sample can contain first-record values or POST fallback rows when no live sample record is available; it is not an approved update artifact. Resolve the intended record and retain only intended writable changes plus verified identity/control columns, with PATCH on every update row, before preflight. Never upload untouched sample values.



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

Use the parent functional-area skill `scm.order-management.channel-revenue-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
