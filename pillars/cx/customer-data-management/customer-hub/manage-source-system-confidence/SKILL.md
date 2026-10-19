---
skill_id: "cx.customer-data-management.customer-hub.manage-source-system-confidence"
name: "Manage Source System Confidence Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Source System Confidence under the Customer Hub functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Customer Hub"
functional_area_code: "ZCH_CUST_HUB_OPT"
task_code: "ORA_ZCH_MANAGE_SOURCE_SYSTEM_CONFIDENCE"
task_name: "Manage Source System Confidence"
parent_skill_id: "cx.customer-data-management.customer-hub"
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
  - "approved_fsm_package"
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.customer-data-management.trading-community-foundation.manage-trading-community-source-systems"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-source-system-confidence/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-source-system-confidence/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-source-system-confidence/current/"
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

# Manage Source System Confidence Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Source System Confidence` under `Customer Hub`.

## Setup Task Skill Contract

- task_code: `ORA_ZCH_MANAGE_SOURCE_SYSTEM_CONFIDENCE`
- task_name: `Manage Source System Confidence`
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

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Source System Confidence` under `Customer Hub`.

## Setup Task Metadata

- Task name: `Manage Source System Confidence`
- Task code: `ORA_ZCH_MANAGE_SOURCE_SYSTEM_CONFIDENCE`
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

For source-system dependency validation, resolve each confidence `OrigSystem` against 
`assets/source-systems.json` first. Invoke `Manage Trading Community Source Systems` and 
require its `HZ_ORIG_SYSTEMS_B.csv` export only when a value is not in the seeded catalog.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Customer Hub`
- Setup task name: `Manage Source System Confidence`
- Setup task code: `ORA_ZCH_MANAGE_SOURCE_SYSTEM_CONFIDENCE`

## Output Files

| Output File                  | Purpose                     | Updateable | Template File                       | Instructions File               | Behavior                                                          |
|------------------------------|-----------------------------|------------|-------------------------------------|---------------------------------|-------------------------------------------------------------------|
| ASM_SETUP_CSV_METADATA.xml   | Metadata used by FSM import | No         | assets/ASM_SETUP_CSV_METADATA.xml   |                                 | copy unchanged from template without considering user input       |
| ORA_ZCH_CONFIDENCE_LEVEL.csv | Attribute confidence levels | Yes        | assets/ORA_ZCH_CONFIDENCE_LEVEL.csv | references/confidence-levels.md | initialize from export or template and update based on user input |

- Store output files in project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-source-system-confidence/current/.
- Display information about the current output state according to the instructions for the corresponding output files.
- Create or update output files based on user input according to the instructions for the corresponding output files.
- Determine the output context as described in this skill before making changes to the output files.
- Assemble the final approved-fsm-package.zip from the output files before data loading.
- Never read or update output files without following the corresponding instructions.

## View Output Files

- Identify the exact requested output type.
- Load its corresponding reference instructions before accessing any current output file.
- Derive the permitted source rows, columns, display labels, ordering, header text, and summary text from those instructions.
- Read the current output only to retrieve the fields authorized by that derived view contract.
- If the output type has no corresponding instructions, or the request maps to multiple output types, stop and ask for clarification.
- Do not use raw CSV columns, rows, technical identifiers, or template defaults as a user-facing view unless the corresponding reference explicitly permits them.

## Update Output Files

- Initialize output file if it does not exist
    - Extract existing file from latest export ZIP file when modifying existing setup data.
    - Create new file with header row from template file when creating new setup data.
- If rows exist when modifying existing setup data
    - Update those existing rows based on the instructions for the output file.
- If rows do not exist when creating new setup data or modifying existing setup data
    - Create new rows by copying template rows from the template file of the output file.
    - Update those new rows based on the instructions for the output file.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `approved_fsm_package`
- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.customer-hub` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
