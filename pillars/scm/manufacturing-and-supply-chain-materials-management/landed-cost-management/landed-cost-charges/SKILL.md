---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.landed-cost-management.landed-cost-charges"
name: "Landed Cost Charges Setup Task Guidance"
description: "Provides task-specific setup guidance for Landed Cost Charges under the Landed Cost Management functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Landed Cost Management"
functional_area_code: "ORA_CML_LANDED_COST_MGMT"
task_code: "ORA_CML_LANDED_COST_CHARGES"
task_name: "Landed Cost Charges"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.landed-cost-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "landedCostCharges"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
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
  - "core.data-loader"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/landed-cost-management/landed-cost-charges/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/landed-cost-management/landed-cost-charges/current/"
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

# Landed Cost Charges Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Landed Cost Charges` under `Landed Cost Management`.

## Setup Task Skill Contract

- task_code: `ORA_CML_LANDED_COST_CHARGES`
- task_name: `Landed Cost Charges`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.landed-cost-management`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Landed Cost Management`
- functional_area_code: `ORA_CML_LANDED_COST_MGMT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `landedCostCharges`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Landed Cost Charges` under `Landed Cost Management`.

## Setup Task Metadata

- Task name: `Landed Cost Charges`
- Task code: `ORA_CML_LANDED_COST_CHARGES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `landedCostCharges`
- Optional child resources: `chargeDefaultReferenceTypes`, `chargeAnalysisCodes`, `Attachments`

## Landed Cost Charge Data Loader Contract

Use `landedCostCharges` as the parent REST business object for Data Loader preparation and import. `chargeDefaultReferenceTypes` and `chargeAnalysisCodes` are optional child resources. `Attachments` is optional and remains empty unless the user supplies attachment data.

Route every preview, import, and child-association mutation through `core.data-loader`; this skill never submits a direct REST write. The current generated Data Loader attribute-details workbook is authoritative for the parent/child serialization and required fields.

| Requested operation | Parent action | Optional child action |
|---|---|---|
| Landed Cost Charge only | Create the `landedCostCharges` parent. | Do not include a child association or attachment. |
| Charge with default reference type | Create the parent as the first section in one Data Loader archive. | Add the selected `chargeDefaultReferenceTypes` row after the parent section, with resolved `ChargeReferenceTypeId` and `DefaultAutoAssociateFlag`. |
| Charge with cost analysis association | Create the parent as the first section in one Data Loader archive. | Add the selected `chargeAnalysisCodes` row after the parent section, with resolved `AnalysisGroupId` and `AnalysisCodeId`. |
| Association for an existing charge | Identify the existing parent charge. | Add only the selected child association; do not recreate the parent. |
| Remove an existing analysis association | Keep the parent unchanged. | Resolve the exact `ChargeAnalysisCodeId`, then submit only that child-association deletion. |

### Parent and Child Change Controls

- Default Charge Reference Types and Cost Analysis Group/Code associations are optional. A missing or unresolved optional selection must not block creation of an otherwise valid primary charge.
- For a new charge, place the primary `landedCostCharges` row first and then the requested child rows in the same Data Loader archive. Link child rows with the current template's parent key fields; do not infer a `LandedCostChargeId`, `ChargeReferenceTypeId`, `AnalysisGroupId`, `AnalysisCodeId`, or `ChargeAnalysisCodeId`.
- For an existing-charge association or deletion request, obtain the exact parent and child identifiers through the approved task route before source generation. The generated Data Loader workbooks remain authoritative for child-row fields and action representation.
- Do not send `ChargeBasisUOMCode` unless the resolved `ChargeBasisCode` is `PER_UNIT`.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `landedCostCharges` as the parent BusinessObject and the current generated workbook for any requested child association.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Landed Cost Management`
- Setup task name: `Landed Cost Charges`
- Setup task code: `ORA_CML_LANDED_COST_CHARGES`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `landedCostCharges` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "landedCostCharges" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

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

## Machine-Readable Output Contract

This skill reuses repository contracts; it does not define a task-local schema.

- Persist `setup_task_plan` and `setup_data_routing` as
  `configuration_blueprint` artifacts conforming to
  `schemas/project-artifact.schema.json` at the manifest's
  `configuration_blueprint` workspace location.
- Persist `validation_checkpoints` as a `validation_result` conforming to
  `schemas/validation-result.schema.json` and its `project-artifact` envelope
  at the manifest's `validation_result` workspace location.
- Persist `skill_run_record` as a `skill_run` conforming to
  `schemas/skill-run.schema.json`; persist `token_usage_record` using the
  manifest's append-only token-usage location.
- Treat `ora-resource/ora_rule_registry.json` as the compiled V3
  machine-readable routing contract. Its graph records validation, lookup,
  successful completion, and fail-closed return paths.
- Include the task identity, artifact type, schema version, routing decision,
  sanitized lookup-evidence reference or failure reason, and terminal
  checkpoint in each durable output. Consumers must reject unsupported artifact
  types or schema versions, task-identity mismatches, and non-terminal states.

## Implementation Notes

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.landed-cost-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
