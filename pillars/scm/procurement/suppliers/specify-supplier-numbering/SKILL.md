---
skill_id: "scm.procurement.suppliers.specify-supplier-numbering"
name: "Specify Supplier Numbering Setup Task Guidance"
description: "Provides task-specific setup guidance for Specify Supplier Numbering under the Suppliers functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "POZ_SPECIFY_SUPPLIER_NUMBERING"
task_name: "Specify Supplier Numbering"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "supplierNumberingInitializeSetup"
  - "supplierNumbering"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/specify-supplier-numbering/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/specify-supplier-numbering/current/"
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

# Specify Supplier Numbering Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Specify Supplier Numbering` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `POZ_SPECIFY_SUPPLIER_NUMBERING`
- task_name: `Specify Supplier Numbering`
- parent_skill_id: `scm.procurement.suppliers`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Suppliers`
- functional_area_code: `ORA_EGP_SUPPLIERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `supplierNumberingInitializeSetup`, `supplierNumbering`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `supplierNumberingInitializeSetup` and `supplierNumbering` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "supplierNumberingInitializeSetup" \
     "supplierNumbering" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbooks together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the initialization workbook only for the no-row branch and the `supplierNumbering` workbook only after the row is present.

## Supplied Task Inputs

Reuse clearly mapped requirements and answers from supplied spreadsheets,
CSVs, images, tables, and text, retaining source references without requiring
repetition or reformatting. Distinguish requested changes from current-state
examples; group only missing, unreadable, conflicting, ambiguous, or unsupported
in-scope values into one prompt. Preserve unrequested settings and explicit
Preserve choices; blanks do not mean Clear or false. Supplied snapshots do not
replace fresh lookups. Keep the task's validation, prerequisite checks, execution
route, and approval gates; do not ask twice for the same operation's approval.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Specify Supplier Numbering` under `Suppliers`.

## Setup Task Metadata

- Task name: `Specify Supplier Numbering`
- Task code: `POZ_SPECIFY_SUPPLIER_NUMBERING`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `supplierNumberingInitializeSetup` for the no-row initialization branch and `supplierNumbering` for the existing-row update branch.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Specify Supplier Numbering`
- Setup task code: `POZ_SPECIFY_SUPPLIER_NUMBERING`

## Supplier Numbering Data Loader Execution Requirements

Use `core.data-loader` for all Supplier Numbering mutations. Do not substitute a direct REST call.

1. Generate and inspect both live samples before preparing an artifact. `supplierNumberingInitializeSetup` is the no-row initialization business object; `supplierNumbering` is the existing-row update business object.
2. Use the read-only Supplier Numbering lookup to establish whether exactly one row exists. Do not accept a manually supplied row identifier.
3. When the lookup returns zero rows, prepare the minimal `supplierNumberingInitializeSetup` Data Loader artifact with `RestAction=POST`. Do not provide an invented `SupplierNumberingId`, `Content-Type`, `REST-Framework-Version`, or other optional value. Validate, preview, obtain approval, and submit this initialization artifact through `core.data-loader`.
4. After a successful initialization load, re-read the collection and require exactly one returned row. The initialization outcome must establish the row before a numbering update can be prepared. A failed or unresolved initialization blocks the run; do not retry it automatically.
5. For an existing or initialized row, use the sample-confirmed key fields to identify the row and update only `NextSupplierNumber`. `SupplierNumberingId` is the row identity supplied by the read result; do not include service-specific URI fields in the Data Loader artifact.
6. Preview the exact Data Loader artifact, obtain approval bound to that preview, submit once, and verify with a fresh read-only lookup.

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

Use the parent functional-area skill `scm.procurement.suppliers` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
