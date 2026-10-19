---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-additional-identifier-types"
name: "Manage Additional Identifier Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Additional Identifier Types under the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES"
task_name: "Manage Additional Identifier Types"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-additional-identifier-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-additional-identifier-types/current/"
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
side_effects:
  - "After explicit approval, creates one task-scoped FSM CSV import process that can change Fusion configuration."
required_privileges:
  - "Fusion privileges to submit and inspect setup task CSV imports."
---

# Manage Additional Identifier Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Additional Identifier Types` under `Trading Community Foundation`.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`
- task_name: `Manage Additional Identifier Types`
- parent_skill_id: `cx.customer-data-management.trading-community-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Trading Community Foundation`
- functional_area_code: `ORA_HZ_CDM_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Additional Identifier Types` under `Trading Community Foundation`.

## Setup Task Metadata

- Task name: `Manage Additional Identifier Types`
- Task code: `HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`
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

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Trading Community Foundation`
- Setup task name: `Manage Additional Identifier Types`
- Setup task code: `HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`

## Native FSM Import Contract

The mandatory `core.data-loader` workflow validates the immutable FSM ZIP and
creates the Task Hook approval envelope. After one explicit approval for the
exact environment, ZIP path, and SHA-256, it may release only this task-local
adapter:

```text
cx.customer-data-management.trading-community-foundation.manage-additional-identifier-types.native-fsm-import
```

The adapter verifies one `ASM_SETUP_CSV_METADATA.xml` member with
`ObjectShortName=HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`, validates the approved
path and archive hash, then creates exactly one import process at:

```text
/fscmRestApi/resources/11.13.18.05/setupTaskCSVImports/
HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES/child/SetupTaskCSVImportProcess
```

Its JSON payload contains `TaskCode`, Base64 `FileContent`, and
`SourceTargetDiffOkFlag=Y` for the normal cross-environment migration route.
The adapter records the returned `ProcessId`, polls the process, and downloads
the `ProcessLog`. It never uses `uploadDataLoaderFile` or
`dataLoaderDataSets/action/initiateDataLoad`, and never retries an uncertain
POST.

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/manage-additional-identifier-types/scripts/import_manage_additional_identifier_types.py \
  --zip-file <approved-zip> \
  --task-validation-envelope <approved-envelope> \
  --token-cache auto \
  --output-dir project/<project_id>/artifacts/shared/setup-import/task-level-import/manage-additional-identifier-types/
```




## Execution Safety

### Preflight

Before releasing the native FSM adapter, verify the target Fusion environment,
the caller's setup-task import privileges, and that the output directory stays
under `project/<project_id>/`. Verify that the ZIP contains exactly one
`ASM_SETUP_CSV_METADATA.xml` member whose `ObjectShortName` is
`HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`, and that the Task Hook approval
envelope matches the exact ZIP SHA-256. Stop before any Fusion request when a
check fails.

### Failure Handling

Classify failures as input validation, authentication or authorization,
transport or environment, Fusion API, process timeout, process failed, or
artifact persistence. Do not retry an uncertain import-process POST. When the
process fails or times out, retrieve and persist the ProcessLog when available,
report the process ID with a sanitized diagnostic, and require fresh approval
before any resubmission.

### Redaction

Never print or persist access tokens, authorization headers, client secrets,
Base64 ZIP content, or sensitive configuration payloads. Redact these values
from diagnostics, project artifacts, and user-facing results.

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

Use the parent functional-area skill `cx.customer-data-management.trading-community-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
