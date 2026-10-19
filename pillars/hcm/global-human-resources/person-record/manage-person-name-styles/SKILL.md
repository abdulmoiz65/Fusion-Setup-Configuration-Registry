---
skill_id: "hcm.global-human-resources.person-record.manage-person-name-styles"
name: "Manage Person Name Styles Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Person Name Styles under the Person Record functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Person Record"
functional_area_code: "ORA_PERSON_RECORD"
task_code: "ORA_PER_MANAGE_PERSON_NAME_STYLES"
task_name: "Manage Person Name Styles"
parent_skill_id: "hcm.global-human-resources.person-record"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM global human resources pillar team"
version: "0.1.3"
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
  - "core.fusion-api.rest-api-client"
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
oracle_supplied_guidance_files:
  - purpose: "Country, style, and component validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency and reference readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact style and lookup resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting and preservation rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "CSV/XLSX route enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Read, Data Loader, approval, and reconciliation failure handling"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/manage-person-name-styles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/manage-person-name-styles/current/"
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
required_privileges:
  - "Fusion privileges appropriate to read the requested person name style and import approved FSM setup data"
---

# Manage Person Name Styles Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Person Name Styles` under `Person Record`.

## Task Overview

Use this task to plan and govern `Manage Person Name Styles` configuration in Global Human Resources.

- **Task identity:** `ORA_PER_MANAGE_PERSON_NAME_STYLES` — Manage Person Name Styles.
- **Scope:** HCM → Global Human Resources → Person Record.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `FSM` with no declared Data Loader business object.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `ORA_PER_MANAGE_PERSON_NAME_STYLES`
- task_name: `Manage Person Name Styles`
- parent_skill_id: `hcm.global-human-resources.person-record`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Person Record`
- functional_area_code: `ORA_PERSON_RECORD`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Person Name Styles` under `Person Record`.

## Setup Task Metadata

- Task name: `Manage Person Name Styles`
- Task code: `ORA_PER_MANAGE_PERSON_NAME_STYLES`
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
4. Import the exported FSM setup CSV ZIP with `core.data-loader`; retain `ASM_SETUP_CSV_METADATA.xml` so Fusion executes `submitTaskCSVImport`.

## Supported Operations and Authoring

- For a country read, resolve its legislation code, then read the bounded `managePersonNameStyles` collection with `expand=nameSetups` and match the exact `LegislationCode`; do not filter by country name.
- For a read, complete country resolution, the parent read, and expanded `nameSetups` in the same turn; do not stop after the first bounded page or an intermediate lookup.
- **Mandatory component-output rule:** Every Person Name Style component presentation—whether from a read, export, or validation—must show **every available component column** in source order, including `ColumnName`. Do not omit, summarize away, or substitute a display label for a returned field. A prompt or display label may supplement the result but must not replace `ColumnName`. If multiple approved sources provide different columns, present their union and identify the source for every field not returned by the live REST response. Do not report the component result as complete until this rule is satisfied.
- **Completion gate:** Before reporting any component read, export, or validation as complete, verify that the presentation includes every available component column in source order, with `ColumnName`, `component_field_order`, and `field_sources`. Treat missing columns, field-order changes, missing source labels, duplicate or missing `ColumnName` values, or values that conflict with the live response as blockers.
- For create or edit, run every applicable declared read and task rule in graph order. In the same turn, populate and validate the current FSM export from the resolved business values; do not stop after resolution, export, or package preparation. When the graph returns `PNS.LOADER_READY`, invoke `core.data-loader` with that source and keep control until Core returns the immutable ZIP preview. Then wait for standalone `approve`, import through `submitTaskCSVImport`, and reconcile the completed load. Retain the exact metadata and CSV names; do not convert the package into an HCM Data Loader business-object ZIP.
- For a country-specific style, resolve the country context before preparation. Create the parent before child rows; preserve blank generated IDs and use only fields supported by the reviewed source.
- Preserve the requested style name instead of deriving it from the country display name. Build the parent `GroupingKey` from the resolved `LegislationCode`; build each child key as `LegislationCode,ColumnName`, and keep the parent row before all children.
- Resolve each supplied Name Component through [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md), using `PER_NAME_STYLE_ATTRIBUTES`; use the returned code rather than a display label or inferred value.
- Preserve unchanged values, do not add translation rows unless explicitly requested, retain the required last-name component, and verify a supplied Prompt after load because Fusion can normalize it.
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- Create and ordinary field edits use only the FSM import route through Core
  Data Loader. The REST client is for read-only requests in this skill.
- **Deletion is unsupported:** block deletion of an entire Name Style and
  removal of any child component, including requests worded as an edit or
  update to keep only a subset of existing components. Classify the requested
  effect before reading targets, resolving components, exporting data, or
  preparing a load. Return: "Person Name Styles deletion and component removal
  are not supported by this skill because the FSM import route does not delete
  existing records. No records were changed."
- Do not build a deletion plan or payload, request deletion approval, or invoke
  REST, Core Data Loader, a browser, or another route to perform deletion.
  Approval does not enable an unsupported operation. Do not treat omitted CSV
  rows or a smaller submitted component set as removal. Do not substitute
  deactivation for deletion. Explicitly requested ActiveFlag edits remain
  ordinary field edits, subject to existing component eligibility checks.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Person Record`
- Setup task name: `Manage Person Name Styles`
- Setup task code: `ORA_PER_MANAGE_PERSON_NAME_STYLES`




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

Use the parent functional-area skill `hcm.global-human-resources.person-record` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Preflight, Failure, and Redaction

Before a mutation, complete the applicable exact-read, input, dependency,
approval, and task-local error-guidance checks. Classify failures, preserve only
the required sanitized diagnostics, and stop before retry or route substitution.
Never print or persist credentials, tokens, token caches, secrets, full payloads,
or sensitive customer data.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
