---
skill_id: "scm.order-management.channel-revenue-management.manage-channel-claim-types"
name: "Manage Channel Claim Types Setup Task Guidance"
description: "Provides create and update guidance for Channel Claim Types and existing business-unit mappings, with operation-specific validation and approved Data Loader submission."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
task_code: "ORA_CJM_MANAGE_CLAIM_TYPES"
task_name: "Manage Channel Claim Types"
parent_skill_id: "scm.order-management.channel-revenue-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "channelClaimTypes"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.2.2"
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
  - "erp.financials.organization-structures"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/manage-channel-claim-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/manage-channel-claim-types/current/"
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

# Manage Channel Claim Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Channel Claim Types` under `Channel Revenue Management`.

## Setup Task Skill Contract

- task_code: `ORA_CJM_MANAGE_CLAIM_TYPES`
- task_name: `Manage Channel Claim Types`
- parent_skill_id: `scm.order-management.channel-revenue-management`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Channel Revenue Management`
- functional_area_code: `ORA_FOM_CHANNEL_REV_MGMT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `channelClaimTypes`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Claim Types` under `Channel Revenue Management`.

## Setup Task Metadata

- Task name: `Manage Channel Claim Types`
- Task code: `ORA_CJM_MANAGE_CLAIM_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `channelClaimTypes`

## CSV Export, Import, and Validation Workflow

For create or update preparation, read the task resources in order: [input and update contracts](ora-resource/ora_input_validation.md), [dependencies](ora-resource/ora_dependency_readiness.md), [lookups](ora-resource/ora_reference_lookups.md), [defaults](ora-resource/ora_defaulting_rules.md), [design gates](ora-resource/ora_design_enforcement.md), and [errors and approval gates](ora-resource/ora_error_handling.md). Evaluate the compiled graph through core.data-loader Task Hook, not direct REST writes.

Accept SetId, SetCode or SetName as alternative parent set inputs for create and update identity. Resolve and cross-check them using the task lookup; SetId is intake-only, not a writable loader field. Updates cannot move a claim type to another set.

Before Data Loader mapping/preflight, read [Input Validation](ora-resource/ora_input_validation.md), including its task-scoped date aliases and worksheet/column identity rules. Apply documented aliases through the existing core.data-loader mapping mechanism after verifying the target attributes against live metadata. This preparation does not replace Task Hook validation of the final immutable artifact or upload approval.

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using channelClaimTypes as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Claim Types`
- Setup task code: `ORA_CJM_MANAGE_CLAIM_TYPES`


## Update Existing Claim Types

1. Require explicit update intent. Resolve the existing parent by ClaimTypeCode plus SetId, SetCode or SetName resolved to one set; optional ClaimTypeId must agree. Resolve each existing child under that parent by its existing BUMappingCode or BusinessUnitLevelMappingId, cross-checking both when supplied. Missing or ambiguous targets block; never create or upsert a missing target.
2. Accept only the operation-specific [parent and child Update Fields](ora-resource/ora_input_validation.md#parent-update-fields). Confirm every requested field, identity/control column, child linkage, and PATCH operation against live Data Loader metadata. API support alone is not proof of loader support. Report unsupported fields without dropping them or substituting another route.
3. Use the declared read-only lookups through the shared REST client during preparation to obtain existing identities and current values. Prepare only requested changes, verified keys, and RestAction=PATCH. Parent-only, child-only, and combined existing-record updates are supported when the loader supports their exact shape. For child-only updates, retain the root worksheet for structure but no fabricated parent change; require verified child keys/linkage. Nested businessUnitLevelMappings is represented by child rows, never a JSON string cell.
4. Preserve omitted values and unrelated children. Separate sources when rows have different change columns unless per-row omission is documented. Apply no create defaults; blank cells are not explicit clears. Compare effective dates using current values and reject duplicate targets. A complete no-op returns NO_CHANGE without submission; remove partial no-ops only during preparation and restart preflight.
5. Complete normal Data Loader mapping, schema validation, and immutable archive preparation, then invoke Task Hook and evaluate its rules for that archive. Build the exact before/after preview only after validation succeeds. Obtain approval and verify the archive through Task Hook before core.data-loader submission. Readiness is not upload approval. Never edit or refresh an approved artifact; changed inputs or stale evidence require a new cycle.
6. Keep the existing AR dependency-validation limitation visible. Initiation is not completion; retrieve status/errors only when requested. Do not retry uncertain writes or promise unsupported concurrency protection.

This is assisted task support using existing core services. It does not add a REST writer or authorize adding/deleting child mappings as an update fallback. Review ownership remains with the SCM Pillar Lead/SME and A-Team/core reviewer.

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `channelClaimTypes` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "channelClaimTypes" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

For an update workbook, add `--operation update`. Sample rows can use an unrelated first record or POST fallback; resolve the intended parent/child targets and require PATCH on every actual update row before validation. Never upload untouched sample values.



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
