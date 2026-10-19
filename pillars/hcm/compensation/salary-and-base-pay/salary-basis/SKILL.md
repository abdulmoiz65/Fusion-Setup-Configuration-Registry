---
skill_id: "hcm.compensation.salary-and-base-pay.salary-basis"
name: "Salary Basis Setup Task Guidance"
description: "Provides task-specific setup guidance for Salary Basis under the Salary and Base Pay functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Salary and Base Pay"
functional_area_code: "ORA_SALARY_AND_BASE_PAY"
task_code: "CMP_MANAGE_SALARY_BASIS"
task_name: "Salary Basis"
parent_skill_id: "hcm.compensation.salary-and-base-pay"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "HDL"
businessObject: "SalaryBasis"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/salary-and-base-pay/salary-basis/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/salary-and-base-pay/salary-basis/current/"
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

# Salary Basis Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Salary Basis` under `Salary and Base Pay`.

## Setup Task Skill Contract

- task_code: `CMP_MANAGE_SALARY_BASIS`
- task_name: `Salary Basis`
- parent_skill_id: `hcm.compensation.salary-and-base-pay`
- pillar: `HCM`
- offering: `Compensation`
- functional_area: `Salary and Base Pay`
- functional_area_code: `ORA_SALARY_AND_BASE_PAY`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `HDL`
- businessObject: `SalaryBasis`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download HDL Data Loader Sample

Use this workflow when `dataloader_import_mode: "HDL"` and a SalaryBasis HDL sample is needed.

1. Confirm that `SalaryBasis` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "SalaryBasis" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Salary Basis` under `Salary and Base Pay`.

## Setup Task Metadata

- Task name: `Salary Basis`
- Task code: `CMP_MANAGE_SALARY_BASIS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `HDL`
- Business Object: `SalaryBasis`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using SalaryBasis as the BusinessObject.

## Data Loader Payload Preparation

For a create or update that includes `ElementName`, run the task-owned payload
assembler after `resolve_salary_basis_input_value_id` has produced successful,
exact resolver evidence and before the approval preview is created:

```bash
python pillars/hcm/compensation/salary-and-base-pay/salary-basis/scripts/prepare_salary_basis_payload.py \
  --source "<reviewed-SalaryBasis.dat>" \
  --resolver-evidence "<successful-resolver-evidence.json>" \
  --output "<prepared-SalaryBasis.dat>"
```

The assembler verifies the evidence identity against `ElementName` and
`InputValueName` (defaulting the omitted source value to `Amount`), then writes
the exact resolved `InputValueId` into the output `SalaryBasis` row. It does
not call Fusion, resolve IDs itself, or submit an import. A missing, ambiguous,
or mismatched evidence record blocks payload preparation. Use only the
immutable prepared output for the later preview and approved Data Loader handoff.

## Read and Query Workflow

For a read-only request to list, search, or retrieve existing Salary Bases,
use `core.fusion-api.rest-api-client` with the HCM REST resource:

```text
GET /hcmRestApi/resources/latest/salaryBases
```

1. Before the first query in an execution, verify the resource contract with
   `GET /hcmRestApi/resources/latest/salaryBases/describe`.
2. Use only supported read query parameters established by that describe
   response. Apply a caller-supplied name filter only when its field and query
   syntax are confirmed by the metadata; otherwise return the paginated
   collection without inferring a filter.
3. Follow Fusion pagination until the requested result set is complete. Return
   only the fields needed for the request and redact internal IDs unless they
   are required for an approved follow-on operation.
4. Treat `401` or `403` as an authentication or privilege failure; treat an
   unavailable or incompatible describe response as a REST metadata validation
   gap. Do not substitute the Data Loader business-object endpoint for record
   reads.

Keep export and import on the existing task-level export and `core.data-loader`
routes using the `SalaryBasis` Data Loader Business Object. The HCM
`salaryBases` resource is read/query-only in this task contract; it does not
authorize create, update, delete, upload, or import operations.

Use this task metadata when invoking those skills:

- Offering: `Compensation`
- Functional area / Setup Object: `Salary and Base Pay`
- Setup task name: `Salary Basis`
- Setup task code: `CMP_MANAGE_SALARY_BASIS`

## Create and Change Routing

- For a create, update, delete, or import, execute every applicable task rule in graph order. When the graph returns `SALB.LOADER_READY`, invoke `core.data-loader` with the task metadata, project context, `SalaryBasis`, operation, and resolved business values. Keep control until Core returns the immutable ZIP preview, then wait for a standalone `approve`.
- Resolve a supplied Grade Rate by its exact active effective name using the documented Grade Rates read contract. Include it only when the current SalaryBasis schema declares a supported field or child association; do not infer a loader attribute, identifier, or row shape.
- Do not issue a mutating Fusion REST call. `core.data-loader` is the only mutation route and owns any required Data Loader transport. The task may use REST only for read-only describe, lookup, validation, and retrieval operations.




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

Use the parent functional-area skill `hcm.compensation.salary-and-base-pay` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
