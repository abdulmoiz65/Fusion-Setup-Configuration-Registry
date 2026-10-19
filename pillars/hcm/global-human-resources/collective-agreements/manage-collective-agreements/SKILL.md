---
skill_id: "hcm.global-human-resources.collective-agreements.manage-collective-agreements"
name: "Manage Collective Agreements Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Collective Agreements, including split-aware date-effective deletion through HCM Date Effective Object Changes and Data Loader merge."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Collective Agreements"
functional_area_code: "ORA_COLLECTIVE_AGREEMENTS"
task_code: "ORA_MANAGE_COLLECTIVE_AGGREMENTS"
task_name: "Manage Collective Agreements"
parent_skill_id: "hcm.global-human-resources.collective-agreements"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "CollectiveAgreements"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
oracle_supplied_guidance_files:
  - purpose: "Operation-specific inputs and validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency and reference readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact agreement and shared reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting and omitted-value preservation"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Data Loader route, preview, approval, and reconciliation enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Read and Data Loader failure handling"
    location: "ora-resource/ora_error_handling.md"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/collective-agreements/manage-collective-agreements/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/collective-agreements/manage-collective-agreements/current/"
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

# Manage Collective Agreements Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Collective Agreements` under `Collective Agreements`.

## Task Overview

Use this task to plan and govern `Manage Collective Agreements` configuration in Global Human Resources.

- **Task identity:** `ORA_MANAGE_COLLECTIVE_AGGREMENTS` — Manage Collective Agreements.
- **Scope:** HCM → Global Human Resources → Collective Agreements.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `CollectiveAgreements`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `ORA_MANAGE_COLLECTIVE_AGGREMENTS`
- task_name: `Manage Collective Agreements`
- parent_skill_id: `hcm.global-human-resources.collective-agreements`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Collective Agreements`
- functional_area_code: `ORA_COLLECTIVE_AGREEMENTS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `CollectiveAgreements`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Collective Agreements` under `Collective Agreements`.

## Setup Task Metadata

- Task name: `Manage Collective Agreements`
- Task code: `ORA_MANAGE_COLLECTIVE_AGGREMENTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `CollectiveAgreements`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `CollectiveAgreements` as the BusinessObject.

## CRUD and Reference Routing

- Read only through `collectiveAgreements`. Resolve exact names against `CollectiveAgreementName`; when the caller explicitly requests a contains search, use `q=CollectiveAgreementName like '%term%'`, replacing `term` with the escaped caller-supplied value.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run applicable declared reads and task rules, then invoke `core.data-loader` with the task metadata, project context, business object, operation, and resolved business values. Follow it through immutable preview without stopping at an intermediate step, then wait for standalone `approve`; ask only for unresolved business input.
- Do not issue mutating Fusion REST calls.

## Collective Agreement Authoring Rules

- Normalize the request to `get`, `create`, `edit`, or `delete`. Do not infer a mutation or an effective date; a date-less read may disclose the current effective row only.
- Preserve exact agreement name and identification-code text. For create, require zero exact duplicate name and code matches in the resolved legislative, legal-employer, and effective scope. For edit, require one exact agreement and effective row. For delete, retrieve and display every effective-dated split through hcmDateEffectiveObjectChanges, then require one explicitly selected EffectiveStartDate; never select the first result or treat the agreement as a single record.
- Validate ISO dates, reject an end date before its start date, and accept only explicit, Data Loader-supported fields. Do not accept response-only IDs, audit values, links, generated keys, or display-only reference values as load input.
- Resolve country or legislation before legal employer, union, bargaining unit, status, and other dependent values. Resolve status through `ACTIVE_INACTIVE`; require exactly one compatible active/effective result and do not create, infer, or copy a missing dependency.
- For an extensible-flexfield segment, resolve its current context and value only from the applicable runtime `describe` contract. On create, use the root polymorphic mapping, child describe, and current loader metadata without requiring an existing parent. For an existing agreement, re-read the link-bearing parent and follow its returned EFF links. Complete metadata and value resolution in the same turn; template generation or context identification is not a response boundary. Retain the business label for preview and place only the metadata-declared typed stored value in the Data Loader source.
- Keep the agreement parent and all requested EFF rows in one workbook and ZIP. For each `CollectiveAgreementsExtraInfo` row, resolve the context-specific unique segment and its `DataType` from current loader metadata. On create, assign a distinct positive ordinal per parent/context and serialize it exactly as that type; on edit, preserve the resolved row's existing unique value. Reject blanks, duplicates, decorated or concatenated values, and values that do not round-trip through the declared type. Keep `SequenceNumber` independently distinct, repeat the parent `IdentificationCode`, and leave `CollectiveAgreementId` blank on create when that key resolves the parent.
- Do not default a mutation, status, country/legislation, reference, end date, or omitted field. Preserve omitted edit values and unrelated rows; absence from a request is not deletion.
- Before approval, show the exact target, effective context, resolved reference labels, explicit changes, preserved values, XLSX source fingerprint, Data Loader preview, and post-load reconciliation plan. Any change requires a new preview and approval.
- Data Loader is the only mutation route. For split deletion, use hcmDateEffectiveObjectChanges for split history and impact resolution, then use HDL/Data Loader as a MERGE operation. Do not issue REST deletion for a split record or substitute Fusion REST, FSM CSV, ZAP, permanent deletion, deactivation, or an unapproved retry.
- Do not reject a country-specific EFF context merely because the agreement parent has another legislation. Validate the context and segment independently through current EFF describe metadata and value sets.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Collective Agreements`
- Setup task name: `Manage Collective Agreements`
- Setup task code: `ORA_MANAGE_COLLECTIVE_AGGREMENTS`




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

Use the parent functional-area skill `hcm.global-human-resources.collective-agreements` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)

## Date-effective Split Deletion

- Fetch and display every effective-dated split with hcmDateEffectiveObjectChanges before a deletion preview.
- Process split deletion only through HDL/Data Loader as a MERGE operation; REST deletion is prohibited.
- For a middle split, delete only the selected split and update the preceding EffectiveEndDate to the deleted split former EffectiveEndDate. Preserve every following and unrelated split.
- Use the registered loader date representation `YYYY/MM/DD`, never ISO date strings, in every DAT date column.
- Bind approval to the complete before-and-after split timeline and the one bounded merge change.

## HDL MERGE Date-effective Deletion Algorithm

1. Resolve the target primary object ID at runtime. Use hcmDateEffectiveObjectChanges with HistoryDefClassName oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.CollectiveAgreementHistoryDef and the selected split EffectiveStartDate.
2. Fetch, sort, and display every effective-dated split before source generation. Reject gaps, overlaps, missing boundaries, or a selected date that is not an exact split start.
3. Generate an HDL/Data Loader MERGE source containing only the rows required by the requested deletion. Never issue REST DELETE.
4. One-split agreement: deletion is unsupported by this bounded-purge pattern; stop before source generation and request a supported alternative.
5. Multi-split agreement, first split: deletion is unsupported by this bounded-purge pattern; stop before source generation and request a supported alternative.
6. Multi-split agreement, middle or last split: delete only the selected split and add one predecessor merge update whose EffectiveEndDate equals the deleted split former EffectiveEndDate. Preserve all other splits.
7. For multiple selected splits, process them newest to oldest. Re-resolve the timeline, rebuild the merge source, preview, and obtain approval for each next split; do not combine stale split assumptions or use REST deletion.
8. Submit through Core Data Loader/HDL, wait for a terminal load result, and verify the complete resulting timeline through hcmDateEffectiveObjectChanges.

## Deletion Transport Boundary

- hcmDateEffectiveObjectChanges is read-only history resolution and verification only. It must never perform a Collective Agreement delete, update, or date-effective mutation.
- The sole mutation transport for a Collective Agreement date-effective deletion or effective-date update is HDL/Core Data Loader MERGE with `SET PURGE_FUTURE_CHANGES Y`; an HDL `DELETE` instruction is prohibited for this component.


## Corrected HDL Split-Deletion Contract (Supersedes Earlier Examples)

For a CollectiveAgreements date-effective split deletion, emit exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one retained-predecessor `MERGE` row. Use `YYYY/MM/DD` for EffectiveStartDate and EffectiveEndDate. The MERGE starts on the immediately preceding retained split and ends on the final selected split end date. Do not emit an HDL `DELETE` row, mix DELETE and MERGE instructions, or use REST mutation. First or only split deletion is unsupported by this bounded-purge pattern.
