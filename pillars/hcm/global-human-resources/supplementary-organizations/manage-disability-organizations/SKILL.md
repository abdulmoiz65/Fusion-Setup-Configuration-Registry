---
skill_id: "hcm.global-human-resources.supplementary-organizations.manage-disability-organizations"
name: "Manage Disability Organizations Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Disability Organizations under the Supplementary Organizations functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Supplementary Organizations"
functional_area_code: "ORA_SUPPLEMENTARY_ORGANIZATIONS"
task_code: "PER_MANAGE_DISABILITY_ORGANIZATION"
task_name: "Manage Disability Organizations"
parent_skill_id: "hcm.global-human-resources.supplementary-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "Organization"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.4"
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
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/supplementary-organizations/manage-disability-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/supplementary-organizations/manage-disability-organizations/current/"
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

# Manage Disability Organizations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Disability Organizations` under `Supplementary Organizations`.

## Task Overview

Use this task to plan and govern `Manage Disability Organizations` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_DISABILITY_ORGANIZATION` — Manage Disability Organizations.
- **Scope:** HCM → Global Human Resources → Supplementary Organizations.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `Organization`. The approved mutation source path is an explicitly selected HDL/DAT file through `core.data-loader`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_DISABILITY_ORGANIZATION`
- task_name: `Manage Disability Organizations`
- parent_skill_id: `hcm.global-human-resources.supplementary-organizations`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Supplementary Organizations`
- functional_area_code: `ORA_SUPPLEMENTARY_ORGANIZATIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `Organization`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Prepare an HDL/DAT Source

Use this workflow when the user explicitly selects the DAT route for a Disability Organization mutation. `core.data-loader` remains the executable service; do not invoke a separate loader directly.

1. Confirm that `Organization` is the exact registered Data Loader business object.
2. Generate the editable DAT source through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "Organization" \
     --format dat \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated DAT and its attribute-details workbook together. The DAT is the reviewed source for this explicitly selected route.
4. Write Data Loader dates in `YYYY/MM/DD` format.
5. For a base Disability Organization create or update, retain only the `Organization` and `OrgUnitClassification` metadata and rows. Include `OrgInformation` only when the user supplies a changed EFF context and every required context key and segment has been resolved from live metadata.
6. Preserve the generated metadata order and modify only validated fields; do not add response-only, set, or inferred related-organization attributes.
7. For a Disability Organization create, set `ClassificationCode` to `HCM_DISABILITY_ORGANIZATION`, `ClassificationName` to `Disability Organization`, and apply the requested status only to the `OrgUnitClassification` row. Do not add set attributes or infer related organization values.
8. Review the generated metadata and key fields before preparing source data. Sample generation uses read-only Fusion metadata and doesn't upload data.
9. Bind approval to both the reviewed DAT SHA-256 and generated ZIP SHA-256 before submission.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Disability Organizations` under `Supplementary Organizations`.

## Setup Task Metadata

- Task name: `Manage Disability Organizations`
- Task code: `PER_MANAGE_DISABILITY_ORGANIZATION`
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
- Read disability organizations through `/hcmRestApi/resources/{version}/disabilityOrganizations`.
- For create, edit, or inactivate, run applicable declared reads and task rules, then invoke `core.data-loader` with the task metadata, project context, business object, operation, and resolved business values. For a future date-effective split deletion, read the current Disability Organization as of today and its complete history, show basic details, reject complete delete or the first row, and require user confirmation. Use a reviewed retained-predecessor `Organization` `MERGE` row and its `OrgUnitClassification` association with `SET PURGE_FUTURE_CHANGES Y`; never use an HDL `DELETE` instruction or delete the logical organization. Follow it through immutable ZIP preview, wait for standalone `approve`, then reread the history.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Supplementary Organizations`
- Setup task name: `Manage Disability Organizations`
- Setup task code: `PER_MANAGE_DISABILITY_ORGANIZATION`




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

Use the parent functional-area skill `hcm.global-human-resources.supplementary-organizations` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
