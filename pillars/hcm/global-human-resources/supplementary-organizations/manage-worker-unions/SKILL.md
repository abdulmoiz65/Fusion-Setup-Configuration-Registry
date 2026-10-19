---
skill_id: "hcm.global-human-resources.supplementary-organizations.manage-worker-unions"
name: "Manage Worker Unions Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Worker Unions under the Supplementary Organizations functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Supplementary Organizations"
functional_area_code: "ORA_SUPPLEMENTARY_ORGANIZATIONS"
task_code: "ORA_PER_MANAGE_WORKER_UNIONS"
task_name: "Manage Worker Unions"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/supplementary-organizations/manage-worker-unions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/supplementary-organizations/manage-worker-unions/current/"
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

# Manage Worker Unions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Worker Unions` under `Supplementary Organizations`.

## Task Overview

Use this task to plan and govern `Manage Worker Unions` configuration in Global Human Resources.

- **Task identity:** `ORA_PER_MANAGE_WORKER_UNIONS` — Manage Worker Unions.
- **Scope:** HCM → Global Human Resources → Supplementary Organizations.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `Organization`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `ORA_PER_MANAGE_WORKER_UNIONS`
- task_name: `Manage Worker Unions`
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

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task's business object.

1. Confirm that `Organization` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "Organization" \
     --output-dir "<project-artifact-directory>"
   ```

3. Populate and review the generated XLSX before any DAT is produced; do not hand-author a DAT as the source for agent-authored changes.
4. Include `OrgInformation` only when the user explicitly specifies an Additional Information change and supplies the resolved context and values. Otherwise remove the `OrgInformation` worksheet and its `Data Loader Map` row before DAT generation so no `OrgInformation` DAT section is emitted.
5. Follow `core.data-loader` source-key, validation, preview, and approval guidance before submission.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Worker Unions` under `Supplementary Organizations`.

## Setup Task Metadata

- Task name: `Manage Worker Unions`
- Task code: `ORA_PER_MANAGE_WORKER_UNIONS`
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
- Read worker unions through `/hcmRestApi/resources/{version}/workerUnions`.
- For create or edit, run every applicable declared read and task rule. When the graph returns `UNION.LOADER_READY`, invoke `core.data-loader` as a task-routed request with task metadata, project context, business object `Organization`, operation, and resolved business values. Keep control with Core until it returns the immutable ZIP preview; do not pause at an intermediate rule, mapping, template, or source step, and ask only for unresolved business input.
- For a future date-effective split deletion, read the current Worker Union as of today and its complete history, show the retained predecessor and bounded future range, reject logical-record deletion or the first row, and use the same `UNION.LOADER_READY` handoff only after the user confirms the eligible range. The generated XLSX source includes the reserved `Data Loader Directives` sheet with its one allowlisted `Directive` value, `SET PURGE_FUTURE_CHANGES Y`, plus a reviewed `Organization` `MERGE` row and at least one operation-required `OrgUnitClassification` association; never use an HDL `DELETE` instruction. Follow Core through immutable ZIP preview, wait for standalone `approve`, then reread the history.
- A standalone `approve` resumes the same pending Core request for the unchanged preview through submission; do not return or pause for a Core-internal step.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Supplementary Organizations`
- Setup task name: `Manage Worker Unions`
- Setup task code: `ORA_PER_MANAGE_WORKER_UNIONS`




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
