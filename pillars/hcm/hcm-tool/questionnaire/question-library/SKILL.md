---
skill_id: "hcm.hcm-tool.questionnaire.question-library"
name: "Question Library Setup Task Guidance"
description: "Plan and generate evidence-bound local Question.dat candidates for HCM Question Library setup without performing a live Fusion write."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Questionnaire"
functional_area_code: "CUSTOM_QUESTIONNAIRE"
task_code: "HRT_MANAGE_QUESTIONS"
task_name: "Question Library"
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
version: "0.4.2"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/question-library/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/question-library/current/"
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
  - "Read access to the target Data Loader metadata, templates, and required Question Library reference data when DAT generation is requested."
  - "Write access to the selected local project workspace."
---

# Question Library Setup Task Guidance

## Purpose

Plan Question Library setup and generate evidence-bound `Question.dat` candidates for reusable questions, answers, and supported contexts. This task skill creates local artifacts only and does not upload or initiate a data load; `core.data-loader` must prove the live target evidence before preview or upload.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_QUESTIONS`
- task_name: `Question Library`
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

Use this skill when planning, sequencing, exporting, generating HDL DAT files, or validating setup data for `Question Library` under `Questionnaire`.

## Setup Task Metadata

- Task name: `Question Library`
- Task code: `HRT_MANAGE_QUESTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `catalog-supported; read-only baseline evidence in this skill`
- Data Loader import mode: `HDL`
- Business Object: ``

## FSM Evidence and HDL DAT Generation Workflow

`CSVExportImportSupportedFlag` is `Y`, so an Oracle-generated FSM export can provide discovery and read-only baseline evidence. It is not the selected mutation artifact. The pillar-selected route is `HDL`:

Question Library is independently executable. It does not require a Questionnaire Template or Questionnaire task to be ready before its local candidate and immutable handoff are built.

1. Read the parent [HDL DAT Generation Contract](../references/hdl-dat-generation.md).
2. For every applicable dependency, first use current approved target evidence in the project. When it is absent or stale, run the matching declared read-only `resolve_live_question_*` lookup through `core.fusion-api.rest-api-client`, using only the endpoint and match rule in `ora-resource/ora_reference_lookups.md`. Send `REST-Framework-Version: 9` on every declared `/hcmRestApi` or `/fscmRestApi` request, including pagination and returned-link traversal; do not silently omit or downgrade it. Persist sanitized match evidence. Mark the dependency `MISSING` or ambiguous only after that lookup completes; do not require the user to collect ordinary read-only reference data manually.
   When an eligible user-entered value has zero exact matches, follow the parent [approval-bound suggestion contract](../references/reference-value-suggestions.md), present only task-declared target candidates, and wait for explicit approval before exact revalidation and DAT preparation.
3. Export setup task data with `shared.setup-export.task-level-export` only when a source baseline is needed.
4. Resolve the exact target `Question` business object, fresh UCM template, component/attribute metadata, user keys, mandatory indicators, and registered operations using [HDL Metadata Discovery](../references/hdl-metadata-discovery.md). Send the declared Question business-object filter through `core.fusion-api.rest-api-client`, follow every filtered page until `hasMore=false`, and then apply the exact registration match; do not scan only the first unfiltered 500 rows. Require unchanged `core.data-loader` validation of the same exact registration and complete contract. Do not block solely on the helper's internal product-area filter or ask the user for ProductAreaCode.
5. Resolve every target subscriber, category, `(QuestionType, ResponseTypeName)` pair, owner, rating model, answer, language, and Recruiting context exactly. Bind every emitted response pair to `validation_evidence.response_type_pairs` using the immutable live-lookup evidence ID; never populate that catalog from an FSM `ResponseTypeCode`. Zero or multiple exact matches remain failures; only an explicit run-scoped waiver recorded under the shared contract may carry the named failure into local candidate publication as `overridden`.
6. Validate the approved business data and task-local rules with the shared validators and the FSCR V1.1 resources.
7. For update intent, resolve exactly one existing question/version, prove that update is allowed, read back every emitted current root and affected-child value, bind the approved changed-field set, and preserve every unchanged emitted value. The portable root and child user keys are immutable; a key change is a separately reviewed create/version operation, never an update.
8. Create an `hdl_dat_build_specification`, normalize `Question`, `Answer`, and `QuestionContext` rows into `render_sections` in live parent-before-child order, then invoke `../scripts/questionnaire_dat_serializer.py` with the exact current target template. Never construct pipe-delimited rows manually.
9. Generate `QuestionTranslation.dat` only when the target registers `QuestionTranslation`, its intended operation, and the complete parent key plus installed language.
10. Require the serializer's `hdl-dat-validation-receipt.json` with `status: passed`, exact metadata/value parity, round-trip success, and the same DAT SHA-256 used by the immutable handoff. This builder stops without a live write.
11. Only if a live import is separately requested, pass the unchanged handoff to `core.data-loader`, which owns final validation, preview, standalone approval, upload, and initiation.

Use the shared executable HDL generation contract in `../references/hdl-dat-generation.md` with `task: question-library`. Its safe scope is create or explicit update intent using a target-registered `MERGE` for `Question`, `Answer`, and `QuestionContext`, plus a separately registered translation DAT. Update requires one exact current target, an allowed mutable state, complete readback for every emitted root and affected-child value, immutable portable keys, an explicit changed-field set, and preservation of unchanged emitted values. Omitted children are preserved and never interpreted as deletion. The contract rejects implicit create-to-update conversion, key changes, incomplete or stale readback, attachments/content fields, destructive instructions, copied IDs, source references, or component contracts that differ from the documented portable keys. Evidence provenance and freshness remain required upstream live-metadata gates.

The only lifecycle exception is the task-local **status-only question inactivation route** in `ora-resource/ora_reference_lookups.md`. It applies only when the requested intent is `inactivate`, the exact active latest Question is updateable, `Status` is the only changed root attribute, no child rows are emitted, every declared visible downstream lookup completes with zero matches, and no returned current-state evidence reports a seeded, locked, or in-use conflict. The visible dependency evidence remains partial: it cannot be treated as complete dependency proof or used for a template/questionnaire update, a Question create/change/new-version/remove operation, or a hierarchy mutation. It requires a separate impact-bound business approval before DAT generation and the normal immutable Data Loader preview/approval after generation.

For this narrow route, an independently verified application-release label and
a stable non-secret principal fingerprint are optional provenance. Record either
as explicitly unavailable when the declared workflow cannot prove it; do not
infer a release, hash a token or credential, or claim complete Fusion data-access
scope. Their absence alone is not a blocker because the exact live template,
operation/component contract, target/request scopes, identity, lifecycle state,
and partial-coverage limitation remain mandatory and approval-bound.

For this inactivation route, read [Inactivation review comparison](references/inactivation-review.md) and invoke `scripts/compare_inactivation_review.py` after refreshing the declared lookups. Use its material approval fingerprint for business approval; scanned catalog totals are diagnostics. Keep the normal Data Loader artifact hash and upload approval unchanged. This comparison is not used by other operations.

For an explicit run-scoped validation waiver, use only the documented
`overridden` path in that shared contract. Retain the original failed evidence
and the waiver reason, keep live HDL schema and operation checks non-waivable,
and carry every exception into Data Loader Task Hook validation. A waiver may
permit candidate publication for the reviewed run, but it never proves a
reference exists or a create key is absent and never authorizes upload.

Do not guess an HDL `ResponseTypeName` from an FSM `ResponseTypeCode` or English label. Do not populate source-pod IDs. Treat Recruiting-only fields as inapplicable until the subscriber is resolved exactly.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Questionnaire`
- Setup task name: `Question Library`
- Setup task code: `HRT_MANAGE_QUESTIONS`




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

Use the compiled task-local plan only when its readiness is `ready`, or when the current run has an explicit recorded readiness override, and it does not conflict with a higher-precedence current target contract. An override remains a warning and must never be reported as passed readiness. The generated artifacts are `Question.dat` and, only when registered, `QuestionTranslation.dat`. FSM exports remain read-only baseline evidence. These resources and the DAT builder authorize neither REST writes nor Data Loader submission. Any requested live import must cross the unchanged-hash preview and separate approval gates owned by `core.data-loader`.
