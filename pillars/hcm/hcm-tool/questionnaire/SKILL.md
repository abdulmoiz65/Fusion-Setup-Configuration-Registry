---
skill_id: "hcm.hcm-tool.questionnaire"
name: "Questionnaire Implementation Guidance"
description: "Plan and prepare independently executable HCM Question Library, Questionnaire Templates, and Questionnaires HDL DAT candidates, and optionally orchestrate an explicitly ordered live import through core.data-loader."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Questionnaire"
functional_area_code: "CUSTOM_QUESTIONNAIRE"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.5.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "questionnaire_scope"
  - "target_environment_context"
  - "requested_operation"
  - "approved_business_specification"
  - "setup_data_artifacts"
  - "optional_fsm_baseline"
  - "portable_questionnaire_input"
  - "immutable_data_loader_handoff"
  - "sequential_live_import_request"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "hdl_dat_build_specification"
  - "evidence_bound_hdl_dat_candidates"
  - "hdl_dat_validation_receipt"
  - "immutable_data_loader_handoff"
  - "validation_checkpoints"
  - "canonical_hdl_dat_build_specification"
  - "ordered_data_load_queue"
  - "per_file_data_load_result"
  - "next_pending_data_load"
  - "sequential_data_load_checkpoint"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.task-level-export"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/questionnaire/current/{run_id}/sequential-data-load-checkpoints/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HRT_MANAGE_QUESTIONS"
  - "HRT_MANAGE_QUESTIONNAIRE_TEMPLATES"
  - "HRT_MANAGE_QUESTIONNAIRES"
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
  - "When live import is separately requested, invokes core.data-loader for one independently approved immutable DAT artifact at a time; each accepted invocation uploads content and initiates one Fusion data load."
  - "When task-level export is selected for post-load readback and separately approved, invokes shared.setup-export.task-level-export to create and download one Fusion setup-task export."
required_privileges:
  - "Read access to the target Data Loader metadata, templates, and required Questionnaire reference data when DAT generation is requested."
  - "Read access to Data Loader status and exact Questionnaire target readback when dependency continuation is explicitly requested."
  - "Write access to the selected local project workspace."
  - "For an approved live import, the Fusion and UCM privileges required by core.data-loader to upload content and initiate the registered data load."
  - "For an approved task-level readback export, the Fusion privileges required by shared.setup-export.task-level-export."
---

# Questionnaire Implementation Guidance

## Purpose

Plan Questionnaire setup and prepare exact, evidence-bound HDL DAT candidates.
When the user separately requests live execution, this skill may also coordinate
the validated candidates one at a time through `core.data-loader`. It never
implements upload, initiation, polling, authentication, or retry mechanics
itself. Caller-supplied evidence remains untrusted until `core.data-loader`
revalidates it against the live target.

## When to Use

Use this functional-area skill after HCM Tool scope is confirmed when the
project needs Questionnaire setup planning, an FSM baseline export, HDL DAT
generation, dependency sequencing, validation checkpoints, or an explicitly
requested sequential live import of the resulting immutable DAT handoff. For
any DAT generation or review, read [HDL DAT Generation Contract](references/hdl-dat-generation.md)
before loading a child task skill. For live execution, also read
[Sequential DAT Upload Orchestration](references/sequential-dat-upload.md).

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Questionnaire` (`CUSTOM_QUESTIONNAIRE`)

## Setup Tasks

1. [Question Library](question-library/SKILL.md) (`HRT_MANAGE_QUESTIONS`)
2. [Questionnaire Templates](questionnaire-templates/SKILL.md) (`HRT_MANAGE_QUESTIONNAIRE_TEMPLATES`)
3. [Questionnaires](questionnaires/SKILL.md) (`HRT_MANAGE_QUESTIONNAIRES`)

Each setup task can start, validate, and produce its own local handoff independently. Apply the listed order only when an artifact in the approved design explicitly references another artifact being delivered in the same sequence. A referenced reusable Question or Template must still resolve to exactly one current active same-subscriber target object; a local candidate is not target evidence. A Questionnaire Template may be skipped when it is not requested and the current target HDL/subscriber contract permits a questionnaire without one. Never create a template merely to satisfy a product-wide assumption.

Translations follow their successfully validated parent task and use a separate DAT only when the target registers that translation business object and operation.

The task resources document broader create, change, version, inactivate, and impact-analysis behavior. The current executable procedure supports create and explicit update for Question Library, Questionnaire Templates, and Questionnaires. Every update requires exact current-object and affected-child readback, a target-registered `MERGE`, immutable portable keys, an approved changed-field set, and preservation of unchanged values and omitted children. Template and Questionnaire updates additionally require authoritative full-hierarchy readback and exact in-use and per-operation mutability evidence. Questionnaire update also binds latest/version, response-existence, template-linkage, reusable/direct-question, and consumer-boundary state. Destructive operations and existing template/questionnaire translation updates remain `UNSUPPORTED` until their complete target readback contracts can be bound and revalidated executablely.

## Inputs

- `implementation_objective`
- `project_context`
- `questionnaire_scope`
- `target_environment_context`
- `requested_operation`
- `approved_business_specification`
- `setup_data_artifacts`
- `optional_fsm_baseline`
- `portable_questionnaire_input` when source data is supplied as a business-oriented JSON document rather than the canonical builder request
- `immutable_data_loader_handoff` containing the exact eligible DAT identities and SHA-256 values for sequential execution
- `sequential_live_import_request` explicitly selecting the target environment,
  one-file-at-a-time Data Loader execution, whether status monitoring is
  requested, and the selected post-load readback source

## Portable Input Conversion

Use this conversion path when the user supplies questionnaire definitions as
portable JSON and requests HDL DAT output. It is an assisted transformation:
prepare the canonical build specification in the project workspace, normalize
its approved rows into `render_sections`, then use the pillar-local executable
builder in [HDL DAT Generation Contract](references/hdl-dat-generation.md).
Do not create a separate converter executable or bypass the builder.

The portable root must contain `contract_version: 1`, one supported `task`, a
supported `intent`, `operation: MERGE`, `validation_evidence`, and `data`.
Use `intent: create` for all three tasks. `intent: update` is supported for all
three tasks and must include the task-specific complete `update_contract`
defined in the HDL DAT generation reference.
`target_environment` and `translations` are optional. Reject unknown root
fields, empty collections, non-object attribute sets, and a supplied evidence
bundle hash that does not bind the completed canonical request.

Map the portable data into the builder's `records` array without inventing
values:

| Task | Portable collection and root attributes | Child mapping |
|---|---|---|
| `question-library` | `data.questions[]`; `question` becomes `attributes` | `answers[]` and `contexts[]` each become wrappers with `attributes` |
| `questionnaire-templates` | `data.templates[]`; `template` becomes `attributes` | `sections[].section` becomes section `attributes`; `sections[].questions[].placement` becomes question `attributes`; answers use wrappers with `attributes` |
| `questionnaires` | `data.questionnaires[]`; `questionnaire` becomes `attributes` | `sections[].section` becomes section `attributes`; `sections[].questions[].placement` becomes question `attributes`; answers use wrappers with `attributes` |

For a template or questionnaire placement, carry `mode` only when it is
provided and require it to be `reference`. Do not convert attachments,
embedded questions, copied identifiers, source-reference fields, nulls,
delimiter-bearing values, or implicit sequences into a DAT. Preserve every
explicit section, placement, and answer sequence. Forward translations only in
the canonical translation shape; retain the existing template-translation
blocker.

After mapping, calculate `validation_evidence.evidence_bundle_sha256` from the
complete canonical request using the canonical UTF-8 JSON and SHA-256 procedure
in [HDL DAT Generation Contract](references/hdl-dat-generation.md). Run that
reference's no-write preflight against the exact supplied target DAT header
template before publishing any local DAT artifacts. Invoke
`scripts/questionnaire_dat_serializer.py`; require its
`hdl-dat-validation-receipt.json` with `status: passed` and a SHA-256 matching
the candidate handed downstream. A failed conversion or executable validation
is an input-validation blocker; return the field path and do not write a
partial artifact set.

## Executable DAT Boundary

Never assemble or repair pipe-delimited rows in prose. The only supported local
rendering route is:

```bash
python3 scripts/questionnaire_dat_serializer.py \
  --spec <canonical-build-specification.json> \
  --template <exact-live-template-path> \
  --output-dir <new-versioned-run-directory>
```

The output directory must be new. The serializer refuses overwrite, validates
the live template filename and SHA-256, emits one value per metadata attribute,
round-trips the resulting DAT, and writes a hash-bound validation receipt.
Missing, failed, stale, or mismatched receipt evidence blocks immutable handoff
and `core.data-loader` routing. `questionnaire_dat_validator.py` may review an
existing candidate, but validation never repairs or rewrites it.

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `hdl_dat_build_specification`
- `evidence_bound_hdl_dat_candidates`
- `immutable_data_loader_handoff`
- `validation_checkpoints`
- `canonical_hdl_dat_build_specification`
- `ordered_data_load_queue`
- `per_file_data_load_result`
- `next_pending_data_load`
- `sequential_data_load_checkpoint`
- `skill_run_record`
- `token_usage_record`

## HDL Generation and Handoff

1. Use the approved business specification as the source of intended values and current target readback as the source of existing values for an update.
2. Resolve the exact target business object, current UCM template, components, attributes, user keys, mandatory indicators, and registered operations before rendering any DAT. Follow [HDL Metadata Discovery](references/hdl-metadata-discovery.md): pillar discovery uses the declared read-only REST client without a product-area predicate; unchanged shared-loader validation must resolve the same exact registration and complete contract.
3. Resolve target subscribers, categories, response types, owners, questions, answers, templates, languages, rating models, and Recruiting contexts with exact read-only target evidence. Zero or multiple exact matches block generation.
   When an eligible user-entered reference has zero exact matches, read [Approval-Bound Reference Value Suggestions](references/reference-value-suggestions.md) and use only the task-declared candidate catalog. A suggestion remains pending until explicitly approved and then passes the original exact resolver again.
4. Build each task's normalized `hdl_dat_build_specification` and render only the exact filename, sections, attributes, hierarchy, and operation validated for the target. FSM CSV exports may be used as read-only baseline evidence, never as the current mutation artifact or as proof of HDL display values.
5. Produce local `evidence_bound_hdl_dat_candidates` and an `immutable_data_loader_handoff` containing file identities and hashes. The task builder performs no live write, labels caller evidence as an attestation rather than proven provenance, and marks every result as awaiting `core.data-loader` live revalidation.
6. If a live import is separately requested, follow
   [Sequential DAT Upload Orchestration](references/sequential-dat-upload.md).
   Pass exactly one unchanged handoff artifact at a time to `core.data-loader`.
   That core workflow owns final revalidation, immutable preview, the
   standalone approval for that file, upload, and initiation. Any artifact
   change invalidates that file's handoff and approval.

## Sequential Live Import

Treat the generated Questionnaire DAT set as a dependency-ordered queue, not a
bulk Data Loader source. Build the queue only from the current immutable
handoff; do not recursively discover `.dat` files or include schema templates,
samples, blocked outputs, or stale candidates. Invoke `core.data-loader`
separately for each ready file so it cannot combine the files into one ZIP.

Each queue entry has one of `pending_dependency`, `ready`, `previewed`,
`approved`, `submitted`, `verified`, `declined`, or `blocked`. A later entry may
enter the candidate queue before its predecessor is ready, but it cannot become
`ready` until every required predecessor has terminal success and exact
readback evidence.

The first file requires its own immutable preview and Data Loader approval.
After an accepted upload and successful dependency verification, present the
next file's immutable preview and stop for its separate approval. Approval for
one file never authorizes any later file, and this pillar skill must not add a
second approval for the same upload. Stop the queue on a declined or stale
approval, changed bytes, validation failure, nonterminal or failed dependency,
readback mismatch, upload or initiation failure, or uncertain outcome. Never
retry a live mutation automatically.

Persist a sanitized `sequential_data_load_checkpoint` before each approval
pause and after every accepted, verified, declined, or blocked transition. The
checkpoint records the target identifier, ordered logical filenames, source
hashes, task codes, safe queue states, current item, next pending item, request
ID when available, and blocker summary. Do not persist a raw core response,
hidden Fusion identifiers, approval text, credentials, tokens, or payload
content. `core.data-loader` remains responsible for its own no-artifact output
contract; this checkpoint belongs to the parent project workflow.

## Execution Safety and Error Handling

Before every live side effect, let `core.data-loader` complete its current
preflight, live-schema validation, Task Hook validation, immutable preview, and
approval checks. Classify failures as input validation, catalog or metadata
mismatch, authentication, authorization, transport or environment, Fusion API,
process timeout, process failure, artifact persistence, or approval blocker.
Stop the queue at the first failed or uncertain entry and preserve successful
earlier loads; do not retry, skip a dependency, or submit a later entry.

Use only the bounded status behavior selected by the sequential workflow. On a
timeout, stop with the current file, target, request ID, last status, elapsed
wait, and safe next-check path. Never print or persist OAuth tokens, token-cache
contents, credentials, private keys, full Base64 payloads, or sensitive
business data. Keep technical execution and redaction behavior delegated to
`core.data-loader`; do not reproduce its transport implementation here.

Use the nested setup-task skills for task-specific build rules. Track token usage for every generated project artifact or skill-run record using the manifest policy.
