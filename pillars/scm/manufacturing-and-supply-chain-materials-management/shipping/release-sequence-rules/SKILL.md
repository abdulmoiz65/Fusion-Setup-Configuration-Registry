---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping.release-sequence-rules"
name: "Release Sequence Rules Setup Task Guidance"
description: "Provides task-specific setup guidance for Release Sequence Rules under the Shipping functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Shipping"
functional_area_code: "WSH_ENABLE_SHIPPING"
task_code: "ORA_RELEASE_SEQUENCE_RULES"
task_name: "Release Sequence Rules"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "releaseSequenceRules"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/release-sequence-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/release-sequence-rules/current/"
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
required_privileges:
  - "Fusion read access to standard lookups when a friendly priority or sort value requires resolution."
---

# Release Sequence Rules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Release Sequence Rules` under `Shipping`.

## Setup Task Skill Contract

- task_code: `ORA_RELEASE_SEQUENCE_RULES`
- task_name: `Release Sequence Rules`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.shipping`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Shipping`
- functional_area_code: `WSH_ENABLE_SHIPPING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `releaseSequenceRules`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Release Sequence Rules` under `Shipping`.

## Setup Task Metadata

- Task name: `Release Sequence Rules`
- Task code: `ORA_RELEASE_SEQUENCE_RULES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `releaseSequenceRules`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using releaseSequenceRules as the BusinessObject.

When a supplied priority or sort requires reference lookup, invoke
`core.fusion-api.rest-api-client` with the selected Fusion environment context.
The core client owns authentication, environment resolution, request execution,
token refresh, and response diagnostics; task resources own only the lookup
type, requested fields, exact-match rule, and mapped business fields.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Shipping`
- Setup task name: `Release Sequence Rules`
- Setup task code: `ORA_RELEASE_SEQUENCE_RULES`

## Explicit FSM Package Contract

Apply this section only after an explicit FSM Export or FSM Import request. The default Data Loader route remains REST-backed.

- Export and import the exact task `ORA_RELEASE_SEQUENCE_RULES` through the governed FSM route.
- Preserve the exported package members, names, headers, encoding, and metadata XML unchanged: `ASM_SETUP_CSV_METADATA.xml`, `WSH_PICK_SEQUENCE_RULE.csv`, and `WSH_PICK_SEQUENCE_RULE_TRANSLATION.csv`.
- For an FSM create, add one matching root row and translation row using the exported CSV headers and column order. Do not synthesize, drop, or rename template columns.
- Use the exact `StartDateActive` and `EndDateActive` representation evidenced by the current same-environment FSM export in `WSH_PICK_SEQUENCE_RULE.csv`; do not apply a format derived from another task.
- Use backend priority/sort values in the exported priority columns and preserve the matching `Priority1Rule` through `Priority5Rule` and `Priority1Sort` through `Priority5Sort` representation. Resolve friendly values only through approved lookups or an exact same-environment exported row; never guess a code.
- Keep DFF/attribute columns blank when no DFF value is supplied. A populated DFF or attribute value requires a fresh task-specific template that evidences its context and segment contract.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `releaseSequenceRules` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "releaseSequenceRules" \
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

## Implementation Notes

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.shipping` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
