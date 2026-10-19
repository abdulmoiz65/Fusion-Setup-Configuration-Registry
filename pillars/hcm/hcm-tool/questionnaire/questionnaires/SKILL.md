---
skill_id: "hcm.hcm-tool.questionnaire.questionnaires"
name: "Questionnaires Setup Task Guidance"
description: "Plan and generate evidence-bound local Questionnaire.dat candidates for HCM Questionnaires, including validated direct questions of all supported types, without performing a live Fusion write."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Questionnaire"
functional_area_code: "CUSTOM_QUESTIONNAIRE"
task_code: "HRT_MANAGE_QUESTIONNAIRES"
task_name: "Questionnaires"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/questionnaires/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/questionnaires/current/"
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
  - "Read access to the target Data Loader metadata, templates, and required Questionnaires reference data when DAT generation is requested."
  - "Write access to the selected local project workspace."
---

# Questionnaires Setup Task Guidance

## Purpose

Plan Questionnaire setup and generate evidence-bound `Questionnaire.dat` candidates for questionnaire headers, sections, reusable-question placements, direct questions, direct choice answers, and answer overrides. This task skill creates local artifacts only and does not upload or initiate a data load; `core.data-loader` must prove the live target evidence before preview or upload.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_QUESTIONNAIRES`
- task_name: `Questionnaires`
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

Use this skill when planning, sequencing, exporting, generating HDL DAT files, or validating setup data for `Questionnaires` under `Questionnaire`.

## Setup Task Metadata

- Task name: `Questionnaires`
- Task code: `HRT_MANAGE_QUESTIONNAIRES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `catalog-supported; read-only baseline evidence in this skill`
- Data Loader import mode: `HDL`
- Business Object: ``

## FSM Evidence and HDL DAT Generation Workflow

`CSVExportImportSupportedFlag` is `Y`, so an Oracle-generated FSM export can provide discovery and read-only baseline evidence. It is not the selected mutation artifact. The pillar-selected route is `HDL`:

Questionnaires is independently executable. Resolve only the reusable Questions and supplied or route-required Templates actually referenced by the approved design. Each reference requires exact active same-subscriber target evidence and may predate or be outside this delivery; a local candidate never satisfies that requirement.

1. Read the parent [HDL DAT Generation Contract](../references/hdl-dat-generation.md).
2. For every applicable dependency, first use current approved target evidence in the project. When it is absent or stale, run the matching declared read-only `resolve_live_questionnaire_*` lookup through `core.fusion-api.rest-api-client`, using only the endpoint and match rule in `ora-resource/ora_reference_lookups.md`. Send `REST-Framework-Version: 9` on every declared `/hcmRestApi` or `/fscmRestApi` request, including pagination and returned-link traversal; do not silently omit or downgrade it. Persist sanitized match evidence. Mark the dependency `MISSING` or ambiguous only after that lookup completes; do not require the user to collect ordinary read-only reference data manually.
   When an eligible user-entered value has zero exact matches, follow the parent [approval-bound suggestion contract](../references/reference-value-suggestions.md), present only task-declared target candidates, and wait for explicit approval before exact revalidation and DAT preparation.
3. Confirm exact target readback for every reusable Question and supplied or route-required Template actually referenced by the design. A prior Question Library or Questionnaire Templates task is required only when the same delivery must first create that referenced target object.
4. Export setup task data with `shared.setup-export.task-level-export` only when a source baseline is needed.
5. Resolve the exact target `Questionnaire` business object, fresh UCM template, component/attribute metadata, user keys, mandatory indicators, and registered operations using [HDL Metadata Discovery](../references/hdl-metadata-discovery.md). Send the declared Questionnaire business-object filter through `core.fusion-api.rest-api-client`, follow every filtered page until `hasMore=false`, and then apply the exact registration match; do not scan only the first unfiltered 500 rows. Require unchanged `core.data-loader` validation of the same exact registration and complete contract. Do not block solely on the helper's internal product-area filter or ask the user for ProductAreaCode.
6. Resolve every target subscriber, category, owner, reusable question/version, answer, language, and supplied or route-required template exactly. Bind every emitted `QuestionType`/`ResponseTypeName` pair to `validation_evidence.response_type_pairs` using the immutable exact reusable-question or live response-type evidence ID; never populate that catalog from an FSM `ResponseTypeCode`. `TemplateQstnrCode` is not a universal product requirement; require it only when supplied or when the selected target HDL operation/subscriber contract marks it mandatory.
7. Validate the approved business data and task-local rules with the shared validators and the FSCR V1.1 resources.
8. For update intent, resolve exactly one authoritative full questionnaire and hierarchy by its versioned key. Prove root and per-field/per-component mutability, current latest/in-use/seeded/locked/response state, and template-linkage behavior for the target release. Read back every emitted current root and affected child value and bind the approved changed-field set.
9. Classify every submitted Section, reusable or direct Question, and Answer row as `existing` or `new`. Existing rows must resolve by their complete live user keys; new rows must have zero key collisions. Root and existing-child keys are immutable. Omitted children are preserved and never interpreted as removal, movement, resequencing, or replacement.
10. Create an `hdl_dat_build_specification`, normalize supported `Questionnaire`, `Section`, `Question`, and `Answer` rows into `render_sections`, then invoke `../scripts/questionnaire_dat_serializer.py` with the exact current target template. The executable supports reusable placements and validated version-1 direct Questions of type `TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE`; `QuestionnaireAttachment` remains blocked until content packaging is implemented. Never construct pipe-delimited rows manually.
11. Generate `QuestionnaireTranslation.dat` only when the target registers its business object and operation. Resolve the complete ordinary-questionnaire identity and include `TemplateFlag=N` when the target contract requires it. Existing translation update remains unsupported without exact translation readback and update-specific registration.
12. Require the serializer's `hdl-dat-validation-receipt.json` with `status: passed`, exact metadata/value parity, round-trip success, and the same DAT SHA-256 used by the immutable handoff. This builder stops without a live write.
13. Only if a live import is separately requested, pass the unchanged handoff to `core.data-loader`, which owns final validation, preview, standalone approval, upload, and initiation.

Use the shared executable HDL generation contract in `../references/hdl-dat-generation.md` with `task: questionnaires`. Its safe scope is create or explicit update intent using a target-registered `MERGE`, with existing reusable-question placements (`mode: reference`) and direct questions (`mode: direct`) of type `TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE`. `mode: direct-text` is retained only as a compatibility alias for `TEXT`. Read [direct-text-question-serializer.md](../references/direct-text-question-serializer.md) when a direct question is supplied. Update requires one authoritative full questionnaire and hierarchy readback, proven root and per-field/per-component mutability, current latest/in-use/seeded/locked/response state, immutable root and child keys, explicit existing/new child intent, a non-empty aggregate changed-field set, and preservation of every unchanged emitted value and omitted child. Template linkage is preserved unless current target evidence explicitly proves the requested change safe. For an in-use or response-bearing questionnaire, partial lifecycle evidence blocks hierarchy, scoring, template-linkage, or lifecycle mutation. The contract blocks implicit create-to-update conversion, key changes, child removal/movement/resequencing, attachments, destructive instructions, copied IDs, source references, existing translation update, and component contracts that differ from the documented portable keys. Evidence provenance and freshness remain required upstream live-metadata gates.

`QstnrQstnResponseTypeName` is an optional placement override; blank means inherit. Do not populate it with an FSM response code, a guessed English label, or the reusable-question field `ResponseTypeName`. Consumer linkage remains a separate downstream task and is never written into `Questionnaire.dat`.

When the selected target create contract requires reusable-question response context on a placement, emit the exactly resolved `QuestionType` and reusable-question `ResponseTypeName` together. They describe the referenced question and are not a `QstnrQstnResponseTypeName` placement override. The deterministic builder rejects a partial pair. For `mode: direct`, follow the direct-question normalization procedure and executable serializer only after the target component, category, response type, template capability, Answer-component applicability, and exact current metadata order have been proven.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Questionnaire`
- Setup task name: `Questionnaires`
- Setup task code: `HRT_MANAGE_QUESTIONNAIRES`




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

Use the compiled task-local plan only when its readiness is `ready` and it does not conflict with a higher-precedence current target contract. The generated artifacts are `Questionnaire.dat` and, only when registered, `QuestionnaireTranslation.dat`. FSM exports remain read-only baseline evidence. These resources and the DAT builder authorize neither REST writes nor Data Loader submission. Any requested live import must cross the unchanged-hash preview and separate approval gates owned by `core.data-loader`.
