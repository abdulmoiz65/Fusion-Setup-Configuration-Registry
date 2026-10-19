---
skill_id: "hcm.workforce-absence-management.absence.absence-reasons"
name: "Absence Reasons Setup Task Guidance"
description: "Provides task-specific setup guidance for Absence Reasons under the Absence functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absence"
functional_area_code: "ORA_ABSENCE"
task_code: "ORA_ANC_MANAGE_ABSENCE_REASONS"
task_name: "Absence Reasons"
parent_skill_id: "hcm.workforce-absence-management.absence"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "absenceReasons"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce absence management pillar team"
version: "1.0.0"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-reasons/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-reasons/current/"
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

# Absence Reasons Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Absence Reasons` under `Absence`.

## Setup Task Skill Contract

- task_code: `ORA_ANC_MANAGE_ABSENCE_REASONS`
- task_name: `Absence Reasons`
- parent_skill_id: `hcm.workforce-absence-management.absence`
- pillar: `HCM`
- offering: `Workforce Absence Management`
- functional_area: `Absence`
- functional_area_code: `ORA_ABSENCE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `absenceReasons`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when viewing, searching, reading details, planning, sequencing, exporting, importing, or validating setup data for `Absence Reasons` under `Absence`.

## Read Order and Operation Routing

Read `ora-resource/ora_input_validation.md`, `ora-resource/ora_reference_lookups.md`,
`ora-resource/ora_defaulting_rules.md`, `ora-resource/ora_design_enforcement.md`, and
`ora-resource/ora_error_handling.md` before executing the selected task workflow. The
compiled `ora-resource/ora_rule_registry.json` supplies the task-local transitions; it is
not a substitute for the source rules.

For AC1 view/list/search requests, use `search_absence_reasons_advanced` through
`core.fusion-api.rest-api-client`. This specific search action is a read-semantic
POST, not reason creation. Follow its documented action URL, headers,
request body, filters, pagination, and display mapping in
`ora-resource/ora_reference_lookups.md`. Use the signed-in consultant's access
and the routed project's environment, authentication, and redacted read-evidence
workflow; do not claim that a successful search proves write privileges.

Default an omitted search date to the current system date and an omitted status
filter to Active, and disclose that search context. An explicit all-status
request removes the status filter. Do not apply the create-only US legislation
default to a general search. Inactive reasons and rows effective on a requested
historical date are valid view results; association eligibility rules do not
exclude them from viewing. A search date never supplies a later mutation date.

Return all requested result pages with Name, Legislation, Status, Effective
Start Date, and Effective End Date. Preserve null cells and returned dates;
do not invent descriptions, substitute "open ended", shift columns, or expose
technical pagination in the business response. For a selected reason's
Description, use `read_absence_reason_details`; the captured search response
does not contain that field. Verify the selected ID and dated row before
presenting the detail. If the exact dated row cannot be read, return the search
result with the precise detail limitation, not another row's Description.

The read branch terminates at `AR.RETURN_VIEW_RESULTS`, including empty search
results. It does not generate a DAT/ZIP, fetch a Data Loader template, request
load approval, or submit a load. A later change request separately enters the
existing mutation workflow. Existing find-or-create requests for Absence Types
retain their exact-name lookup and `AR.REASON_FOUND` handoff.

## Setup Task Metadata

- Task name: `Absence Reasons`
- Task code: `ORA_ANC_MANAGE_ABSENCE_REASONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `absenceReasons`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route export/import setup data work through the relevant skills below. AC1 view/search/detail reads use the separate read route above, not this Data Loader workflow:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using absenceReasons as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Workforce Absence Management`
- Functional area / Setup Object: `Absence`
- Setup task name: `Absence Reasons`
- Setup task code: `ORA_ANC_MANAGE_ABSENCE_REASONS`

## Date-Effective Data Loader Contract

The registered `absenceReasons` DAT template exposes `effectiveOf` on the
parent, `AbsenceReasonsDDFFlex`, and `AbsenceReasonsFlex` sections. For every
date-effective create, update, correction, end-date, delete-changes, or ZAP
request, derive and include the matching `effectiveOf` value on the parent and
on each included flexfield row. Do not create a flexfield row solely to carry
the value.

Validate the current registered Data Loader template before preparation. Do not
infer `effectiveOf` support from REST `describe` metadata or from a reduced DAT
sample. The detailed operation-to-value mapping, identity requirements, and
approval gates are in `ora-resource/ora_defaulting_rules.md` and
`ora-resource/ora_input_validation.md`. Continue to route every mutation only
through `core.data-loader` and its immutable preview and approval lifecycle.

For this REST-backed business object, preserve physical `EffectiveStartDate`
and `EffectiveEndDate` values in `YYYY-MM-DD` format in the final DAT, including
`AbsenceReasonsDDFFlex` and `AbsenceReasonsFlex` rows. Do not convert these
task-specific dates to the generic sample-workbook `YYYY/MM/DD` representation.

When a flexfield `MERGE` row is included, include an `absenceReasons` parent
`MERGE` row with the same resolved `AbsenceReasonId` and matching `effectiveOf`.
A parent `METADATA` header alone does not establish the REST parent-child
relationship. For a flex-only update or retry, the parent may be a key-only
`PATCH`; do not replay unrelated parent attributes.

Before selecting `RestAction` for an `AbsenceReasonsFlex` or
`AbsenceReasonsDDFFlex` row, run `resolve_absence_reason_flex_item` for the exact
parent and effective period. Use `PATCH` only when that lookup returns one exact
child item, and retain its returned identity. Use `POST` only when the child is
missing and the target parent effective slice already exists. If the requested
update first creates a new parent effective slice, submit and verify a
parent-only archive, then re-read the child and prepare a separately validated
flex archive. Never assume that a flex child created by parent propagation is
available to a child `PATCH` in the same load.

After any partial or failed flex load, re-read both parent and child state before
preparing another archive. Do not replay the prior archive or rely only on the
aggregate loaded/failed counts when a data-set object error is present.

For every date-effective source, derive Task Hook evidence from the final
immutable DAT member that Data Loader will upload. A caller-provided
rule-result record is not evidence that `effectiveOf` was serialized. Block the
preview when the parent or any included `AbsenceReasonsDDFFlex` or
`AbsenceReasonsFlex` `METADATA` header or `MERGE` row omits the derived
`effectiveOf` value.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `absenceReasons` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "absenceReasons" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Required Portable Source Preparation and Verification

For REST Data Loader source preparation, read
[Portable Source Preparation](../references/portable-source-preparation.md)
and use `pillars/hcm/workforce-absence-management/absence/scripts/prepare_absence_source.py`.
Supply current registered metadata and resolved business decisions; do not
create ad hoc project or temporary generators. Verify the exact final DAT or
ZIP with `--verify` and `--model` before the existing Data Loader preview.
This local check does not replace task rules, live lookups, target-key collision
checks, immutable approval, submission, or post-load verification.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `absence_reason_search_results`
- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.workforce-absence-management.absence` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

When interacting with a requester, identify inputs, missing values, and validation errors by their business-facing labels rather than raw Data Loader or REST attribute names. For example, say `Absence Reason Name` and `Effective Start Date`, not `Name` and `EffectiveStartDate`. Keep raw attribute names only in technical artifacts, loader-source previews, or when the requester explicitly asks for them.
