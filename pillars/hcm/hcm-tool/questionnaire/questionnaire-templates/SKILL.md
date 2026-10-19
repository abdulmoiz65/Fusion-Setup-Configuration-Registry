---
skill_id: "hcm.hcm-tool.questionnaire.questionnaire-templates"
name: "Questionnaire Templates Setup Task Guidance"
description: "Plan and generate evidence-bound local QuestionnaireTemplate.dat candidates for HCM Questionnaire Templates without performing a live Fusion write."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Questionnaire"
functional_area_code: "CUSTOM_QUESTIONNAIRE"
task_code: "HRT_MANAGE_QUESTIONNAIRE_TEMPLATES"
task_name: "Questionnaire Templates"
parent_skill_id: "hcm.hcm-tool.questionnaire"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "HDL"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.4.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "target_environment_context"
  - "requested_operation"
  - "approved_business_specification"
  - "template_owner_person_number"
  - "setup_data_artifacts"
  - "optional_fsm_baseline"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "hdl_dat_build_specification"
  - "evidence_bound_hdl_dat_candidates"
  - "hdl_dat_validation_receipt"
  - "immutable_data_loader_handoff"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.diagnostics.role-access-check"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/questionnaire-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/questionnaire-templates/current/"
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
  - "Reads supplied source artifacts and current target HDL metadata and reference data through authorized read-only routes."
  - "Writes versioned local HDL build specifications, DAT artifacts, validation results, and immutable handoff metadata under project/{project_id}."
required_privileges:
  - "Read access to the target Data Loader metadata, templates, and required Questionnaire Templates reference data when DAT generation is requested."
  - "Write access to the selected local project workspace."
---

# Questionnaire Templates Setup Task Guidance

## Purpose

Plan Questionnaire Template setup and generate evidence-bound `QuestionnaireTemplate.dat` candidates for template headers, sections, reusable-question placements, and answer rows. This task skill creates local artifacts only and does not upload or initiate a data load; `core.data-loader` must prove the live target evidence before preview or upload.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_QUESTIONNAIRE_TEMPLATES`
- task_name: `Questionnaire Templates`
- parent_skill_id: `hcm.hcm-tool.questionnaire`
- pillar: `HCM`
- offering: `HCM Tool`
- functional_area: `Questionnaire`
- functional_area_code: `CUSTOM_QUESTIONNAIRE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `HDL`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, generating HDL DAT files, or validating setup data for `Questionnaire Templates` under `Questionnaire`.

## Setup Task Metadata

- Task name: `Questionnaire Templates`
- Task code: `HRT_MANAGE_QUESTIONNAIRE_TEMPLATES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `catalog-supported; read-only baseline evidence in this skill`
- Data Loader import mode: `HDL`
- Business Object: ``

## FSM Evidence and HDL DAT Generation Workflow

`CSVExportImportSupportedFlag` is `Y`, so an Oracle-generated FSM export can provide discovery and read-only baseline evidence. It is not the selected mutation artifact. The pillar-selected route is `HDL`:

Questionnaire Templates is independently executable. For each reusable-question placement, resolve one exact active same-subscriber Question/version from the target; it may predate or be outside the current Question Library task. Do not use a local candidate as that evidence.

1. Read the parent [HDL DAT Generation Contract](../references/hdl-dat-generation.md).
2. For every applicable dependency, first use current approved target evidence in the project. When it is absent or stale, run the matching declared read-only `resolve_live_template_*` lookup through `core.fusion-api.rest-api-client`, using only the endpoint and match rule in `ora-resource/ora_reference_lookups.md`. Send `REST-Framework-Version: 9` on every declared `/hcmRestApi` or `/fscmRestApi` request, including pagination and returned-link traversal; do not silently omit or downgrade it. Persist sanitized match evidence. Mark the dependency `MISSING` or ambiguous only after that lookup completes; do not require the user to collect ordinary read-only reference data manually.
   When an eligible user-entered value has zero exact matches, follow the parent [approval-bound suggestion contract](../references/reference-value-suggestions.md), present only task-declared target candidates, and wait for explicit approval before exact revalidation and DAT preparation.
3. Confirm the exact target readback for each reusable-question placement actually included in the template design. A prior Question Library task is required only when the same delivery must first create that referenced target Question.
4. Export setup task data with `shared.setup-export.task-level-export` only when a source baseline is needed.
5. Resolve the exact target `QuestionnaireTemplate` business object, fresh UCM template, component/attribute metadata, user keys, mandatory indicators, and registered operations using [HDL Metadata Discovery](../references/hdl-metadata-discovery.md). Send the declared Questionnaire Template business-object filter through `core.fusion-api.rest-api-client`, follow every filtered page until `hasMore=false`, and then apply the exact registration match; do not scan only the first unfiltered 500 rows. Require unchanged `core.data-loader` validation of the same exact registration and complete contract. Do not block solely on the helper's internal product-area filter or ask the user for ProductAreaCode.
6. Require `OwnerPersonNumber` as the sole portable owner key for every template header before any service lookup or DAT rendering. If it is absent, stop and request that value; do not issue a template-service lookup with an ownerless request. Do not accept, request, or emit `Owner`, `OwnerPersonId`, or any other owner/person ID in place of `OwnerPersonNumber`. Resolve the supplied person number, target subscriber, reusable question/version, category for a newly embedded question, response-format value, placement override, rating model, answer, language, and attachment reference exactly.
7. Validate the approved business data and task-local rules with the shared validators and the FSCR V1.1 resources.
8. For update intent, resolve exactly one full template—not only its LOV row—and prove root mutability, current in-use/seeded/locked state, and the exact editable attributes and child operations for the target release. Read back every emitted current root and affected child value, bind the approved changed-field set, and preserve every unchanged emitted value.
9. Classify every submitted Section, Question placement, and Answer row as `existing` or `new`. Existing rows must resolve by their complete live user keys; new rows must have zero key collisions. Root and existing-child keys are immutable. Omitted children are preserved and never interpreted as removal, movement, resequencing, or replacement.
10. Create an `hdl_dat_build_specification`, normalize the supported `QuestionnaireTemplate`, `Section`, `Question`, and `Answer` rows into `render_sections`, then invoke `../scripts/questionnaire_dat_serializer.py` with the exact current target template. Never construct pipe-delimited rows manually. `TemplateAttachment` remains blocked until content packaging is implemented.
11. Record `QuestionnaireTemplateTranslation.dat` as `UNSUPPORTED` in the current procedure even when the target registers it. Do not generate it until an exact target parent-version readback can be bound to the translation `VersionNumber`.
12. Require the serializer's `hdl-dat-validation-receipt.json` with `status: passed`, exact metadata/value parity, round-trip success, and the same DAT SHA-256 used by the immutable handoff. This builder stops without a live write.
13. Only if a live import is separately requested, pass the unchanged handoff to `core.data-loader`, which owns final validation, preview, standalone approval, upload, and initiation.

Use the shared executable HDL generation contract in `../references/hdl-dat-generation.md` with `task: questionnaire-templates`. Its safe scope is create or explicit update intent using a target-registered `MERGE`, with existing reusable-question placements (`mode: reference`). Update requires exactly one authoritative full-template readback, proven root and per-field/per-component mutability, current usage state, immutable root and child keys, explicit existing/new child intent, a non-empty aggregate changed-field set, and preservation of every unchanged emitted value and omitted child. A lightweight LOV match proves identity only and cannot authorize update. For an in-use template, update is allowed only for the exact fields and child operations proven editable by current target/source evidence; partial downstream-usage evidence blocks lifecycle or hierarchy mutation. The contract blocks implicit create-to-update conversion, key changes, child removal/movement/resequencing, embedded-question creation, attachments, destructive instructions, copied IDs, source references, and component contracts that differ from the documented portable keys. Evidence provenance and freshness remain required upstream live-metadata gates.

For an existing reusable-question placement, `QstnResponseTypeName` is an optional override; blank means inherit. Require embedded-question category and definition fields only when current target behavior confirms that the hierarchy is creating a missing question. Do not put response-format codes into the individual HDL allow/deny fields.

For create, validate the current target's registered service prerequisites before reference lookups: `QuestionnaireCode`, `SubscriberName`, `Name`, `Status`, `PrivacyFlag`, `OwnerPersonNumber`, `AllowFormatChg`, `AllowIntroChg`, `AllowQstnOrderChg`, `AllowRespOrderChg`, and `AllowSectionChg`. `OwnerPersonNumber` is required; `Owner`, `OwnerPersonId`, and other owner/person IDs are internal values and cannot satisfy this prerequisite. For each Section require its name and positive `SectionSeqNum`; for each existing-question placement require `QuestionCode`, `QstnVersionNum`, positive `SeqNum`, and `AdhocQstn`. The live template marks generated IDs as mandatory internally, but its registered user keys resolve them from these portable keys; never request or emit those IDs.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Questionnaire`
- Setup task name: `Questionnaire Templates`
- Setup task code: `HRT_MANAGE_QUESTIONNAIRE_TEMPLATES`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `target_environment_context`
- `requested_operation`
- `approved_business_specification`
- `setup_data_artifacts`
- `optional_fsm_baseline`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `hdl_dat_build_specification`
- `evidence_bound_hdl_dat_candidates`
- `immutable_data_loader_handoff`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.hcm-tool.questionnaire` for functional-area sequencing, source-of-truth precedence, deterministic serialization, and the immutable upload boundary. Track token usage for every generated project artifact or skill-run record using the manifest policy.

## FSCR V1.1 Resource Workflow

Read the task-local resources in this order before preparing an import:

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_reference_lookups.md`
3. `ora-resource/ora_dependency_readiness.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

Use the compiled task-local plan only when its readiness is `ready` and it does not conflict with a higher-precedence current target contract. The executable procedure generates and round-trip validates `QuestionnaireTemplate.dat`; it records `QuestionnaireTemplateTranslation.dat` as `UNSUPPORTED` until exact parent-version binding is implemented. FSM exports remain read-only baseline evidence. These resources and the DAT procedure authorize neither REST writes nor Data Loader submission. Any requested live import must cross the unchanged-hash preview and separate approval gates owned by `core.data-loader`.
