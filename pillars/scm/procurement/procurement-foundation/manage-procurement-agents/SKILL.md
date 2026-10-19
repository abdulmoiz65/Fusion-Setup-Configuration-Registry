---
skill_id: "scm.procurement.procurement-foundation.manage-procurement-agents"
name: "Manage Procurement Agents Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Procurement Agents under the Procurement Foundation functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Procurement Foundation"
functional_area_code: "ORA_PO_PROC_FOUNDATION_FA"
task_code: "PO_MANAGE_PROCUREMENT_AGENTS"
task_name: "Manage Procurement Agents"
parent_skill_id: "scm.procurement.procurement-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "procurementAgents"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/procurement-foundation/manage-procurement-agents/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/procurement-foundation/manage-procurement-agents/current/"
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

# Manage Procurement Agents Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Procurement Agents` under `Procurement Foundation`.

## Setup Task Skill Contract

- task_code: `PO_MANAGE_PROCUREMENT_AGENTS`
- task_name: `Manage Procurement Agents`
- parent_skill_id: `scm.procurement.procurement-foundation`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Procurement Foundation`
- functional_area_code: `ORA_PO_PROC_FOUNDATION_FA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `procurementAgents`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Procurement Agents` under `Procurement Foundation`.

## Setup Task Metadata

- Task name: `Manage Procurement Agents`
- Task code: `PO_MANAGE_PROCUREMENT_AGENTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Registered Data Loader business object: `procurementAgents`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `procurementAgents` as the registered Business Object.
Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Procurement Foundation`
- Setup task name: `Manage Procurement Agents`
- Setup task code: `PO_MANAGE_PROCUREMENT_AGENTS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s parent business object.

1. Confirm that `procurementAgents` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "procurementAgents" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbook set together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook, including its `DFF` child section where applicable, as the starting point for the later Data Loader preparation and approval workflow.

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

Every `setup_task_plan`, `setup_data_routing`, and `validation_checkpoints`
artifact must be a JSON document with this contract. One document is produced
per output, with `artifact_type` set to the corresponding output name.

```json
{
  "artifact_type": "setup_task_plan | setup_data_routing | validation_checkpoints",
  "task_code": "PO_MANAGE_PROCUREMENT_AGENTS",
  "task_name": "Manage Procurement Agents",
  "status": "passed | blocked | failed",
  "generated_at": "RFC-3339 timestamp",
  "source_evidence": [{"source": "string", "description": "string"}],
  "validation": {"status": "passed | blocked | failed", "checks": [{"name": "string", "status": "passed | blocked | failed", "message": "string"}]},
  "payload": {
    "steps": [{"name": "string", "status": "ready | blocked | not_applicable", "depends_on": ["string"]}],
    "routes": [{"business_object": "procurementAgents", "route": "declared dependency skill ID", "purpose": "string"}],
    "checkpoints": [{"name": "string", "required": true, "owner": "string"}]
  },
  "errors": [{"code": "string", "message": "string"}]
}
```

`payload.steps`, `payload.routes`, and `payload.checkpoints` apply respectively
to the three artifact types; the relevant array must be present and non-empty.
`source_evidence` and `validation.checks` must be non-empty. A passed artifact
must have a passed validation status and an empty `errors` array. Downstream
skills must fail closed on an identity mismatch, unsupported artifact type,
missing required field, or non-passed result where a passed result is required.
Register the durable artifact with `schemas/project-artifact.schema.json`; use
`schemas/validation-result.schema.json` for its validation result.

## Implementation Notes

Use the parent functional-area skill `scm.procurement.procurement-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
