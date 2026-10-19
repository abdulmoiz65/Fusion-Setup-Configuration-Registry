---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.receiving.receiving-document-output-preferences"
name: "Receiving Document Output Preferences Setup Task Guidance"
description: "Provides task-specific setup guidance for Receiving Document Output Preferences under the Receiving functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Receiving"
functional_area_code: "WSH_ENABLE_RECEIVING"
task_code: "ORA_RECEIVING_DOCUMENT_OUTPUT_PREFERENCES"
task_name: "Receiving Document Output Preferences"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.receiving"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "configureDocumentOutputPreferences"
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
  - "shared.setup-import.task-level-import"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/receiving/receiving-document-output-preferences/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/receiving/receiving-document-output-preferences/current/"
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

# Receiving Document Output Preferences Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Receiving Document Output Preferences` under `Receiving`.

## Setup Task Skill Contract

- task_code: `ORA_RECEIVING_DOCUMENT_OUTPUT_PREFERENCES`
- task_name: `Receiving Document Output Preferences`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.receiving`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Receiving`
- functional_area_code: `WSH_ENABLE_RECEIVING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST` (registered alternate route)
- businessObject: `configureDocumentOutputPreferences`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Receiving Document Output Preferences` under `Receiving`.

## Setup Task Metadata

- Task name: `Receiving Document Output Preferences`
- Task code: `ORA_RECEIVING_DOCUMENT_OUTPUT_PREFERENCES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- FSM CSV import: supported through task-level export/import
- REST/Data Loader import: supported through the registered `configureDocumentOutputPreferences` business object

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Select one approved route for a given operation; FSM support does not remove the registered REST/Data Loader route.

1. For FSM, export setup task data with `shared.setup-export.task-level-export`, validate it with the setup-data and reference-data validators, then import the approved CSV ZIP through `shared.setup-import.task-level-import`.
2. For REST/Data Loader, validate inputs and reference data, then use `core.data-loader` with the registered `configureDocumentOutputPreferences` business object. Data Loader owns its runtime metadata preflight and approval workflow.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Receiving`
- Setup task name: `Receiving Document Output Preferences`
- Setup task code: `ORA_RECEIVING_DOCUMENT_OUTPUT_PREFERENCES`


## FSM CSV Template and Import

Use the task-level FSM CSV template export as the canonical source structure for the FSM route. It does not replace the registered REST/Data Loader route.

1. Export the task CSV template through `shared.setup-export.task-level-export`.
2. Preserve the returned `ASM_SETUP_CSV_METADATA.xml`, header CSV, and line CSV without changing their schema.

   ```bash
   python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
     --task-code ORA_RECEIVING_DOCUMENT_OUTPUT_PREFERENCES \
     --template-only --project-id "<project_id>"
   ```

3. Populate only the exported CSV rows, normalize effective dates to `YYYY-MM-DD`, then package the unchanged metadata and CSV files as the task ZIP.
4. Obtain approval for the exact ZIP before invoking task-level import.

## REST/Data Loader Alternate Route

Use `core.data-loader` when the approved operation selects the registered REST-backed route:

- Business object: `configureDocumentOutputPreferences`
- Scope: parent document-output preference and its child output-preference lines
- Preconditions: Data Loader metadata preflight, task-input validation, reference resolution, and the Data Loader approval workflow

Do not synthesize direct Fusion REST calls. If FSM export/import diagnostics fail, report that route-specific blocker; the user may select the REST/Data Loader route as a separate approved operation.



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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.receiving` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
