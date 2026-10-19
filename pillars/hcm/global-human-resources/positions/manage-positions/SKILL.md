---
skill_id: "hcm.global-human-resources.positions.manage-positions"
name: "Manage Positions Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Positions under the Positions functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Positions"
functional_area_code: "ORA_POSITIONS"
task_code: "PER_MANAGE_POSITION"
task_name: "Manage Positions"
parent_skill_id: "hcm.global-human-resources.positions"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "HDL"
businessObject: "Position"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.1"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.fusion-api.ess-job-submitter"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/manage-positions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/manage-positions/current/"
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
  - "May enable the required Oracle Search profile values through their owning task."
  - "May submit and monitor the declared Oracle Search ESS processes."
required_privileges: []
---

# Manage Positions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Positions` under `Positions`.

## Task Overview

Use this task to plan and govern `Manage Positions` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_POSITION` — Manage Positions.
- **Scope:** HCM → Global Human Resources → Positions.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `HDL` with `Position`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_POSITION`
- task_name: `Manage Positions`
- parent_skill_id: `hcm.global-human-resources.positions`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Positions`
- functional_area_code: `ORA_POSITIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `HDL`
- businessObject: `Position`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

1. Confirm `Position` as the registered Data Loader business object.
2. Generate and review the editable XLSX through `core.data-loader`.
3. Let `core.data-loader` convert the frozen XLSX to DAT internally.
4. Follow its validation, immutable preview, and approval guidance; never populate or modify source-system keys.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Positions` under `Positions`.

## Setup Task Metadata

- Task name: `Manage Positions`
- Task code: `PER_MANAGE_POSITION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `HDL`
- Business Object: `Position`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `Position` as the BusinessObject.

## CRUD Routing

- Run export only when explicitly requested.
- Read and name-fragment searches use `/hcmRestApi/resources/{version}/positionsV2`.
- In user-facing Position read results, omit WHO audit columns (`CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, and `LastUpdateLogin`) and identifier fields unless the user explicitly requests them; retain identifiers internally when needed for the workflow.
- For create, edit, or delete, run applicable declared reads and task rules, then invoke `core.data-loader` in `HDL` mode with the task metadata, project context, business object, operation, and resolved business values. Follow it through immutable ZIP preview without stopping at an intermediate step, then wait for standalone `approve`; ask only for unresolved business input.
- Never populate, modify, default, or use `SourceSystemOwner` or `SourceSystemId`; leave them blank on create and omit and preserve them for edits and deletions. Identify records only with supported business keys.
- For a name-fragment search, pass the user-supplied value to the documented `like` filter; never hardcode a search term.

## Oracle Search Ingestion

When Oracle Search setup or re-ingestion is explicitly requested, perform these steps in order:

1. Resolve site-level `HRC_ELASTIC_SEARCH_ENABLED` through `hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values` and site-level `ORA_PER_ORACLE_SEARCH_POSITIONSLOV_ENABLED` through the same task.
2. Before any side effect, prepare an immutable execution plan containing the target environment; each profile option's current and requested site value (include a profile write only when the current value is not `Y`); the initial-ingestion payload `JobDefinition://oracle/apps/ess/fnd/applcore/FndOSCSIndexIngestJob`, `application=FscmEss`, and `submit.argument1=fa-hcm-position`; the ACL payload `JobDefinition://oracle/apps/ess/hcm/users/ComputeUsersACL`, `application=EarHcmEss`, `submit.argument1=LOGGED_IN_USERS`, and `submit.argument2=N`; polling window and interval; and the `/hcmRestApi/resources/latest/positionsLovV2` verification.
3. Obtain one explicit batch approval immediately before the first profile write or ESS submission. That approval authorizes only the immutable plan's required profile updates, the two named ESS submissions, their polling, and final verification. Do not ask again between those approved steps.
4. Execute continuously: update and re-read each included profile value; submit **ESS job to create index definition and perform initial ingest to OSCS**, then poll its exact request ID at the approved interval until a terminal status; only after a successful terminal status, submit **Compute Users ACL** and poll its exact request ID at the approved interval until a terminal status; only after both terminal statuses are successful, read `/hcmRestApi/resources/latest/positionsLovV2` and require returned results.

The batch approval satisfies delegated profile-value and ESS approval gates only for the exact plan. Stop on a rejected, failed, timed-out, or uncertain profile update or ESS process; do not continue, substitute another route, or retry automatically. A changed payload, a new mutation, or any retry requires a fresh approval. Persist both ESS request IDs and terminal results.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Positions`
- Setup task name: `Manage Positions`
- Setup task code: `PER_MANAGE_POSITION`




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

Use the parent functional-area skill `hcm.global-human-resources.positions` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
