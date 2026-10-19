---
skill_id: "hcm.global-human-resources.departments.manage-departments"
name: "Manage Departments Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Departments under the Departments functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Departments"
functional_area_code: "ORA_DEPARTMENTS"
task_code: "PER_MANAGE_DEPARTMENT"
task_name: "Manage Departments"
parent_skill_id: "hcm.global-human-resources.departments"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "Organization"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
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
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/departments/manage-departments/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/departments/manage-departments/current/"
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

# Manage Departments Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Departments` under `Departments`.

## Task Overview

Use this task to plan and govern `Manage Departments` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_DEPARTMENT` — Manage Departments.
- **Scope:** HCM → Global Human Resources → Departments.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `Organization`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_DEPARTMENT`
- task_name: `Manage Departments`
- parent_skill_id: `hcm.global-human-resources.departments`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Departments`
- functional_area_code: `ORA_DEPARTMENTS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `Organization`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Prepare Fusion Data Loader DAT Source

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `Organization` is the exact registered Data Loader business object.
2. Generate the default Department source as a DAT through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "Organization" \
     --format dat \
     --output-dir "<project-artifact-directory>"
   ```

   When the request includes an Organization Information/EFF row, generate the
   full editable XLSX instead (omit `--format dat`). The XLSX preserves the
   selected context segment columns; `core.data-loader` converts the reviewed
   XLSX internally to DAT/ZIP for validation and submission.

3. Keep the generated DAT and attribute-details workbook together.
4. Set `EFF_CATEGORY_CODE` to `DEPARTMENT` for Department EFF rows.
5. Populate only current-template-supported attributes, then validate the exact generated source with `core.data-loader`. Omit `OrgInformation` unless the user explicitly requests an Organization Information/EFF change and supplies its required context and values; do not add that row merely because the live template exposes it. For an EFF request, populate only the selected context and its required or modified segments in the generated XLSX; do not hand-author a DAT or reuse a source from another environment or template.
6. For a Department read, edit, inactivation, or effective-split deletion, establish identity through one exact current Department lookup using the supplied Department name. Never request, display, or author an internal code or source-system key as a Department selector. Keep source-system columns blank unless the user explicitly asks to set or change that source-system pair.
7. Preserve the generated root discriminator filename, `Organization.dat`; a renamed DAT path cannot be assumed to match the registered business object.
8. Use the validated DAT, or the validated EFF XLSX with its internally converted DAT, as the later Data Loader source. Bind approval to the reviewed source SHA-256, the internal DAT SHA-256 when converted, and the prepared ZIP SHA-256.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Departments` under `Departments`.

## Setup Task Metadata

- Task name: `Manage Departments`
- Task code: `PER_MANAGE_DEPARTMENT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `Organization`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using Organization as the BusinessObject.

## CRUD Routing

- Run export only when explicitly requested.
- Read departments through `/hcmRestApi/resources/{version}/departments`.
- For create, edit, inactivate, or delete one or more future date-effective splits, run applicable declared reads and task rules, then invoke `core.data-loader` with the generated, validated Department source, task metadata, project context, business object, operation, and resolved business values. Use the generated, validated `Organization.dat` path for a base-only request; use the full generated `Organization.xlsx` for an Organization Information/EFF request so Core can convert it internally to DAT/ZIP. For a future-split deletion, use the full generated `Organization.xlsx` with the bounded Organization `MERGE` range, at least one operation-required `OrgUnitClassification` association, and one `Data Loader Directives` row: `SET PURGE_FUTURE_CHANGES Y`. Core converts that reviewed workbook internally to DAT/ZIP; do not put the directive in `Data Loader Map`, use an HDL `DELETE` instruction, or delete the logical Department record. Follow Core through immutable ZIP preview, then wait for standalone `approve`; after execution, reread the history.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Departments`
- Setup task name: `Manage Departments`
- Setup task code: `PER_MANAGE_DEPARTMENT`




## Uniform Authoring and Read Contract

- Interpret each supplied business attribute within its intended parent or child section using the current operation-specific Data Loader metadata and REST `describe`. Match the exact technical name first, then an exact normalized display label or declared alias, then one unique case-, space-, and punctuation-insensitive match. If multiple fields remain plausible, show their business labels and ask the user to choose; if none match, report the field as unsupported. Never guess or copy a value between fields.
- For create or edit, map only resolved user values to the exact business-object section, resolve references through declared task resolvers, preserve omitted existing values, and author only requested or operation-required rows and fields through the existing mutation route.
- Determine mandatory input only from current operation-specific metadata and operation-required business identity. Never require or populate a nonmandatory field merely because it appears in a template, example, or response. EFF or Additional Information contexts and segments are always optional and must never be requested as a prerequisite; emit an EFF row only when the user explicitly requests that change, using only its resolved context, identity, changed values, and any fields current metadata requires for that included row.
- Never hard-code a business value from an example. Apply a fixed default only when the task defaulting rules and current metadata confirm it for the exact operation; otherwise omit an optional field or ask only when current metadata marks it required. Fixed technical discriminators are allowed only where the task contract requires them to identify the exact business-object section.
- For a normal read, present business-facing labels and values. Do not show WHO or history columns such as `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, or `LastUpdateLogin`, or primary/surrogate identifiers, unless the user explicitly asks for them; retain identifiers internally for linking and mutation.
- When the user asks for complete details, read the exact parent without a restrictive field projection, expand every task-supported child or EFF collection by following server-returned links, paginate every collection, and return all current business attributes and child values after the same WHO/ID filtering. State when no supported child collection exists or none is returned; never invent a child path.

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

Use the parent functional-area skill `hcm.global-human-resources.departments` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
