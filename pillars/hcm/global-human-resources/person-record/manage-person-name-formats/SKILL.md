---
skill_id: "hcm.global-human-resources.person-record.manage-person-name-formats"
name: "Manage Person Name Formats Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Person Name Formats under the Person Record functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Person Record"
functional_area_code: "ORA_PERSON_RECORD"
task_code: "PER_MANAGE_PERSON_NAME_FORMATS"
task_name: "Manage Person Name Formats"
parent_skill_id: "hcm.global-human-resources.person-record"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "NameFormat"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.2"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "human_readable_format_layout"
  - "created_name_format_details"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/manage-person-name-formats/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/manage-person-name-formats/current/"
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

# Manage Person Name Formats Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Person Name Formats` under `Person Record`.

## Task Overview

Use this task to plan and govern `Manage Person Name Formats` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_PERSON_NAME_FORMATS` — Manage Person Name Formats.
- **Scope:** HCM → Global Human Resources → Person Record.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `NameFormat`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_PERSON_NAME_FORMATS`
- task_name: `Manage Person Name Formats`
- parent_skill_id: `hcm.global-human-resources.person-record`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Person Record`
- functional_area_code: `ORA_PERSON_RECORD`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `NameFormat`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Person Name Formats` under `Person Record`.

## Setup Task Metadata

- Task name: `Manage Person Name Formats`
- Task code: `PER_MANAGE_PERSON_NAME_FORMATS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `NameFormat`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `NameFormat` as the BusinessObject.

## CRUD and Reference Routing

- Read only through `nameFormats`. Resolve exact format codes against `FormatName` and display names against `FormatNameMeaning`; when the caller explicitly requests a display-name contains search, use `q=FormatNameMeaning like '%term%'`, replacing `term` with the escaped caller-supplied value. Use `CountryName` or `LegislationCode` for country-scoped searches; never assume a generic `Name` field. For every returned format, convert the returned `FormatMask` to the human-readable layout defined in [Reference Lookups](ora-resource/ora_reference_lookups.md#read-response-presentation), preserving its proven separators and component order. Retain `FormatMask` only as internal lookup and validation evidence; do not return it in user-facing results.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run every applicable declared read and task rule in graph order. When one request contains multiple NameFormat operations, build one `NameFormat.dat` containing all resolved rows in the requested order, with one immutable ZIP and one Core Data Loader initiation; do not split the request into separate DAT files or loads. When the graph returns `PNF.LOADER_READY`, invoke `core.data-loader` with the task metadata, project context, `NameFormat`, operation, and resolved business values. Keep control until Core returns the immutable ZIP preview; do not pause at an intermediate step. Then wait for standalone `approve`; ask only for unresolved business input.
- When a create is confirmed as completed (by an explicit Data Loader status request or by the caller's UI confirmation), always return the created Name Format details: format name, scope, legislation or country, and human-readable layout. Base the response on the authoritative read when that verification route is active; otherwise use the confirmed submitted values and identify them as submitted values. Never return `FormatMask`, runtime IDs, or the Data Loader source row in this user-facing result.
- When a delete is confirmed as completed (by an explicit Data Loader status request that proves the deletion or by the caller's UI confirmation), state that the Name Format was deleted successfully and identify the deleted format by name, scope, and legislation or country. Do not make that success claim from the asynchronous initiation response alone.
- Do not issue mutating Fusion REST calls.
- For DAT source generation, prefer a validated alternate or surrogate identity over `NameFormatId`: use an explicitly supplied source-system identity when the live contract accepts it, otherwise use the unique natural scope key (`FormatName`, `LegislationCode`, and `UserFormatChoice`). Include `NameFormatId` only when the current live Data Loader template or validation proves that the selected operation cannot use the alternate identity. Never invent, retain from a stale read, or substitute a primary-key value merely to satisfy source generation.
- Build every `DELETE` row with exactly one value for each attribute in the current `METADATA` line, in that same order. `DELETE` and `NameFormat` are control fields, not metadata attributes. For the current six-attribute header (`FormatName`, `LegislationCode`, `UserFormatChoice`, `FormatMask`, `SourceSystemId`, `SourceSystemOwner`), a France local Order Name delete is exactly `DELETE|NameFormat|ORDER_NAME|FR|L|||`: the final three delimiters represent the three blank attributes. Do not append a fourth trailing delimiter. Before immutable-preview generation, verify the field count of every non-`MERGE` row against its `METADATA` definition.
- Build `FormatMask` only from proven tokens. A replacement component uses `<$preferred$$fallback$>`: the first proven core name token is used when populated, otherwise the second is used. Keep the replacement component free of punctuation and separators, and do not nest replacement components. Write backslash-escaped pipes in the source value: use `\|` at the outer boundaries and `\|\|` between layout groups. A leading quote is not an escape. Preserve token order and continue to Core Data Loader after validation.
- Convert a supplied human-readable layout into a mask before source generation: map each whitespace separator to the proven space token, a comma to the proven comma token, `(` to the proven opening-parenthesis token, `)` to the proven closing-parenthesis token, and every other literal character to its exact proven separator token. Do not emit arbitrary punctuation as raw mask text or infer a token abbreviation. For example, global `LIST_NAME` requested as `Prefix Lastname` resolves to `Prefix`, space, `Last Name`; its stored mask is `|$PNA$$SPA$||$LAS$|` and its Data Loader source is `\|$PNA$$SPA$\|\|$LAS$\|`.
- For a Data Loader create row, write `SourceSystemId` and `SourceSystemOwner` as blank unless the caller explicitly supplies nonblank values. Preserve blank values through source generation and validation; never invent a source identity or replace an explicit blank value. The exact immutable source must pass current live Data Loader validation before approval.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Person Record`
- Setup task name: `Manage Person Name Formats`
- Setup task code: `PER_MANAGE_PERSON_NAME_FORMATS`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `created_name_format_details`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.global-human-resources.person-record` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
