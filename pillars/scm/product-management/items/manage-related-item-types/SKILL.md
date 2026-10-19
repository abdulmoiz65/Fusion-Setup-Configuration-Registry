---
skill_id: "scm.product-management.items.manage-related-item-types"
name: "Manage Related Item Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Related Item Types under the Items functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "ORA_MANAGE_RELATED_ITEM_TYPES"
task_name: "Manage Related Item Types"
parent_skill_id: "scm.product-management.items"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "relatedItemTypes"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "SCM product management pillar team"
version: "0.4.2"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-related-item-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-related-item-types/current/"
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

# Manage Related Item Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Related Item Types` under `Items`.

## Setup Task Skill Contract

- task_code: `ORA_MANAGE_RELATED_ITEM_TYPES`
- task_name: `Manage Related Item Types`
- parent_skill_id: `scm.product-management.items`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Items`
- functional_area_code: `ORA_EGP_FA_ITEMS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `relatedItemTypes`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Related Item Types` under `Items`.

## Setup Task Metadata

- Task name: `Manage Related Item Types`
- Task code: `ORA_MANAGE_RELATED_ITEM_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `relatedItemTypes`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `relatedItemTypes` as the Business Object. For this PATCH contract, resolve the supplied relationship-type meaning through lookup type `EGP_RELATIONSHIP_TYPES`, map the returned `LookupCode` into the `relatedItemType` source field, and set `RestAction` to `PATCH`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Related Item Types`
- Setup task code: `ORA_MANAGE_RELATED_ITEM_TYPES`


## Lookup-Code PATCH Data Loader Contract

For an existing related item type update, resolve the supplied relationship-type meaning through lookup type `EGP_RELATIONSHIP_TYPES`. Use the returned `LookupCode` as the value of the Data Loader `relatedItemType` source field.

1. Use `resolve_relationship_type_code_by_meaning` in `ora-resource/ora_reference_lookups.md`.
2. Replace the supplied meaning with the resolver-returned `LookupCode` when preparing the `relatedItemType` source column. Do not generate, alter, or reuse a code.
3. Set `RestAction` to `PATCH` and send only the normalized Boolean `cyclicRelationshipFlag` as the changed field.
4. Obtain a fresh immutable Data Loader preview and explicit approval immediately before submission.

For this task, `dataloader_import_mode: REST` and `businessObject: relatedItemTypes` use the lookup-code mapping from `EGP_RELATIONSHIP_TYPES`. Do not use the supplied meaning as the Data Loader source identity.

## Execution Safety

Preflight checks before any Fusion-changing action: confirm the target environment and privileges; resolve the supplied relationship-type meaning to exactly one `EGP_RELATIONSHIP_TYPES` LookupCode; confirm exactly one existing related item type; normalize `cyclicRelationshipFlag` to Boolean `true` or `false`; and validate the immutable Data Loader archive, including its SHA-256. Use the Task Hook preview and require explicit approval immediately before upload and initiation.

Classify durable failures using the repository failure taxonomy. Stop on invalid inputs, ambiguous lookups, catalog or schema mismatches, insufficient privileges, transport failures, Fusion API errors, or missing approval. Retry only a cached-token 401 or 403 once through the core authentication service and bounded read-only transport failures. Never automatically retry a live PATCH, upload, initiation, or other loader operation; after any source or archive change, rebuild the preview and obtain new approval.

For a timeout or failed data load, persist sanitized diagnostics under the active project workspace with the stage, failure class, environment, artifact references, request ID, last known status, and next action. Never print or persist credentials, OAuth tokens, token-cache contents, private keys, tenant secrets, or full sensitive payloads.

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `relatedItemTypes` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "relatedItemTypes" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. For this PATCH contract, replace the editable sample's `relatedItemType` business-label value with the exact resolved `LookupCode` before validation and approval.



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

Use the parent functional-area skill `scm.product-management.items` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
