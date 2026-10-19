---
skill_id: "scm.procurement.suppliers.manage-certifying-agencies"
name: "Manage Certifying Agencies Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Certifying Agencies under the Suppliers functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "ORA_POZ_MANAGE_CERTIFYING_AGENCIES"
task_name: "Manage Certifying Agencies"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "certifyingAgencies"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-certifying-agencies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-certifying-agencies/current/"
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

# Manage Certifying Agencies Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Certifying Agencies` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `ORA_POZ_MANAGE_CERTIFYING_AGENCIES`
- task_name: `Manage Certifying Agencies`
- parent_skill_id: `scm.procurement.suppliers`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Suppliers`
- functional_area_code: `ORA_EGP_SUPPLIERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `certifyingAgencies`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `certifyingAgencies` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "certifyingAgencies" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

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

Before preparing a loader artifact, read the [input and workbook contract](ora-resource/ora_input_validation.md), [reference lookups](ora-resource/ora_reference_lookups.md), and [execution/error gates](ora-resource/ora_error_handling.md). Resolve supplied classification codes or names through the documented read-only REST lookup; send the validated code, not the name used for server-side foreign-key derivation.

### Exported CSV Mapping

When preparing task-export CSV data for the current Core Data Loader workbook, use these explicit mappings:

| Source file | Export field | Loader field |
|---|---|---|
| ORA_POZ_CERTIFYING_AGENCY.csv | Name | CertifyingAgency |
| ORA_POZ_CERTIFYING_AGENCY.csv | Description | CertifyingAgencyDescription |
| ORA_POZ_CERTIFYING_AGENCY.csv | EndDate | EndDate |
| ORA_POZ_CERT_AGENCY_BUS_CLASS exported.csv | ORA_POZ_CERTIFYING_AGENCY.Name | CertifyingAgency |
| ORA_POZ_CERT_AGENCY_BUS_CLASS exported.csv | ClassificationCode | BusinessClassificationCode |

Validate each classification through the reference lookup before populating the executable workbook. Preserve blank export cells; do not turn a blank EndDate into a clear operation. The exported CSV pair is not itself a native Core Data Loader input: prepare a supported combined workbook using the live template, then use Core's preparation, preview, and approval workflow. Do not rename CSV files as loader artifacts or bypass Core orchestration.

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Certifying Agencies` under `Suppliers`.

## Setup Task Metadata

- Task name: `Manage Certifying Agencies`
- Task code: `ORA_POZ_MANAGE_CERTIFYING_AGENCIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `certifyingAgencies`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using REST business object `certifyingAgencies`.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Manage Certifying Agencies`
- Setup task code: `ORA_POZ_MANAGE_CERTIFYING_AGENCIES`
- Data Loader import mode: `REST`
- Business Object: `certifyingAgencies`




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
