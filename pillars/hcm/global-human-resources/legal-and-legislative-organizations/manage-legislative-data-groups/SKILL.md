---
skill_id: "hcm.global-human-resources.legal-and-legislative-organizations.manage-legislative-data-groups"
name: "Manage Legislative Data Groups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Legislative Data Groups under the Legal and Legislative Organizations functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Legal and Legislative Organizations"
functional_area_code: "ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS"
task_code: "PER_MANAGE_LEGISLATIVE_DATA_GROUPS"
task_name: "Manage Legislative Data Groups"
parent_skill_id: "hcm.global-human-resources.legal-and-legislative-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "LegislativeDataGroup"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/manage-legislative-data-groups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/manage-legislative-data-groups/current/"
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

# Manage Legislative Data Groups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Legislative Data Groups` under `Legal and Legislative Organizations`.

## Task Overview

Use this task to plan and govern `Manage Legislative Data Groups` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_LEGISLATIVE_DATA_GROUPS` — Manage Legislative Data Groups.
- **Scope:** HCM → Global Human Resources → Legal and Legislative Organizations.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `LegislativeDataGroup`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_LEGISLATIVE_DATA_GROUPS`
- task_name: `Manage Legislative Data Groups`
- parent_skill_id: `hcm.global-human-resources.legal-and-legislative-organizations`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Legal and Legislative Organizations`
- functional_area_code: `ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `LegislativeDataGroup`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Legislative Data Groups` under `Legal and Legislative Organizations`.

## Setup Task Metadata

- Task name: `Manage Legislative Data Groups`
- Task code: `PER_MANAGE_LEGISLATIVE_DATA_GROUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `LegislativeDataGroup`

## Create Input Contract

For a create operation, `LegislationCode` and `DefaultCurrencyCode` are mandatory Data Loader fields. `TerritoryShortName` is optional. Do not generate a create workbook, preview, upload, or submission when either `LegislationCode` or `DefaultCurrencyCode` is blank.

Resolve the country-derived values through the shared country-localization workflow before validation:

- `TerritoryShortName`: optional territory display value.
- `LegislationCode`: required country code derived by the shared territories skill and stored as the legislation code.
- `DefaultCurrencyCode`: required default currency of the country.

The default currency must match the country-derived currency. Do not infer, substitute, or leave blank either mandatory code.

## Delete Contract

A Legislative Data Group is not date effective. Interpret a delete request as a
zap of the complete logical object; do not ask for a delete mode, effective
date, split history, country, currency, child row, or EFF context.

Resolve the supplied exact Name to one current Legislative Data Group and retain
its returned `LegislativeDataGroupId` internally as the delete locator. Prepare
exactly one root-only Data Loader row whose serialized directive is:

```text
DELETE|LegislativeDataGroup|<LegislativeDataGroupId>
```

The final serialized source must contain `DELETE`, never `MERGE`. Do not use,
request, populate, or preserve `SourceSystemOwner` or `SourceSystemId` for a
delete. Complete the normal immutable Data Loader preflight, Task Hook preview,
standalone destructive-operation approval, submission, status check, and an
exact-Name verification that no Legislative Data Group remains.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Run export only when explicitly requested. For read, execute the declared lookups and return the result. For create, edit, or delete, run applicable declared reads and task rules, then invoke `core.data-loader` with the task metadata, project context, business object, operation, and resolved business values. A delete follows the root-only zap contract; follow every mutation through immutable ZIP preview without stopping at an intermediate step, then wait for standalone `approve`; ask only for unresolved business input.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Legal and Legislative Organizations`
- Setup task name: `Manage Legislative Data Groups`
- Setup task code: `PER_MANAGE_LEGISLATIVE_DATA_GROUPS`




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

Use the parent functional-area skill `hcm.global-human-resources.legal-and-legislative-organizations` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
