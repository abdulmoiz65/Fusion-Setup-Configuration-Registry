---
skill_id: "shared.data-conversion.setup-data-task-matching"
name: "Setup Data Task Matching and Extraction"
description: "Uses supplied implementation evidence to identify setup tasks, or matches tabular setup data to catalog tasks and task-scoped extracts."
layer: "shared"
type: "planning"
execution_mode: "assisted"
owner_team: "FSCR Shared Data Conversion"
version: "1.0.0"
inputs:
  - "User-supplied implementation evidence, such as a workbook, document, CLI output, or pasted content."
  - "Optional instructions identifying expected tasks, source conventions, offering, or functional area."
  - "knowledge/setup-task-catalog/offering-functional-area-task-catalog.json"
outputs:
  - "A selective identified-task mapping when preparing a project workspace."
  - "A CSV map with Task, Functional Area, Offering, and Data columns."
  - "One task-scoped CSV extract per matched input section, preserving supplied headers."
  - "A run record and diagnostics when the project workspace is supplied."
depends_on:
  - "knowledge/setup-task-catalog/offering-functional-area-task-catalog.json"
uses_core:
  - "core.project-mgmt"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run_and_artifact"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "characters/4"
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
persists_project_state: true
state_updates:
  - "requirements"
  - "setup_task_sequence"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/shared/setup-data-task-matching/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/shared/setup-data-task-matching/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
applicability:
  fusion_releases:
    - "Current catalog release"
side_effects:
  - "Creates project-local CSV extracts, a mapping CSV, and run metadata; does not change Fusion."
required_privileges: []
---

# Setup Data Task Matching and Extraction

## Purpose and boundary

Use this shared skill to interpret user-supplied implementation evidence and identify the setup tasks it requires. For tabular setup data, it can additionally produce a task-to-data map that a downstream setup skill can consume. It performs no Fusion import, API call, or configuration change.

## Project-initialization task selection

When the user asks to create an implementation project from supplied evidence, the LLM selects the required setup tasks before project initialization. It evaluates all relevant evidence together; source format, document section, worksheet name, and prior task lists are evidence rather than scope rules.

Write one selective `identified-task-mapping.json` for the project initializer. Each selected task must retain its source task name plus any available ID and phase, and include concise evidence references or notes when the source provides them. Each matched row must include catalog-resolved `Offering`, `Pillar`, and `Functional Area`, plus a normalized `Source Reference`: use the input filename for file input, `CLI input` for direct command-line values, `Standard input` for stdin, or the artifact filename for a persisted artifact. Do not copy a source task list wholesale. Do not add unrelated tasks. Include prerequisite tasks only when they are required by the selected implementation scope.

Resolve the row's offering context using `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`. Match the source task together with the user-provided implementation intent and data; use an identified pillar as supporting scope evidence. A task can occur under multiple offerings, so do not select an offering from the task name alone. If the evidence leaves multiple offering contexts plausible, ask the user to provide the current offering for that task. Do not guess or create a separate offering-mapping artifact.

Before writing the mapping, the LLM must match each selected source task against the current `knowledge/setup-task-catalog/effective/setupTasksAll.json` catalog. Each row must include `Match Status`, `Match Method`, `Confidence`, `Matched Task Code`, `Matched Task Name`, `Match Rationale`, and `Data Paths`. Initialize `Data Paths` as an empty array when the source has no extracted data.

Use `matched` only when one catalog entry is selected. Use `unmatched` with a null confidence and diagnostic rationale for ambiguity or insufficient evidence; do not guess.

Use `project/_template/artifacts/shared/runbook/identified-task-mapping.example.json` as the mapping shape. It is illustrative only: select tasks from the user's evidence and do not carry its example task into a project.

The mapping carries the LLM's proposed catalog identity. The later Run Book task-context workflow independently validates catalog identity and resolves the FSCR `skill_path`; do not add `skill_path` fields during initial matching.

Fail closed when the evidence does not support a confident task selection. Report the ambiguity and request the smallest necessary user decision.

The project initializer persists the mapping without interpreting it. Do not create a Run Book while initializing the project; Run Book creation remains an explicit later workflow.

## Method

The following extraction method applies when task-scoped data extracts are requested.

1. Preflight the input path, file type, readable sections (for example, workbook tabs), and the target project workspace. Read the current workspace catalog before matching.
2. Use explicit user mapping instructions first. If they are absent, analyze all relevant file evidence using the best applicable method, including section or tab names, declared task columns, table names, headers, representative values, formulas, structure, relationships, business terminology, and data semantics. Do not impose an artificial restriction on which evidence may be decisive.
3. Resolve each candidate only against the current setup-task catalog. Select an exact task code/name match where possible; otherwise use semantic matching across task name, functional area, offering, descriptions, and all available file evidence. The output task name, code, and sequence must come from the catalog; never invent them from source wording or use a previous run as matching authority. Prefer a workspace task with an existing skill path when candidates otherwise tie.
4. Fail closed when the best candidate is ambiguous. Emit a diagnostic containing the source section, candidates, evidence, and the requested user decision; do not write a misleading mapping row.
5. Export every matched section to a distinct UTF-8 CSV under `project/{project_id}/artifacts/shared/setup-data-task-matching/current/data/`. Preserve source column headers exactly. If a source section has no headers, emit `column-1`, `column-2`, and so on, and record `inferred_headers` in the run metadata. Append each exported absolute CSV path to the corresponding authoritative `identified-task-mapping.json` row's `Data Paths` array; preserve its source reference, match, confidence, rationale, candidates, and reviewer fields. Every mapping row retains its `Data Paths` array even when it remains empty.
6. Write `setup-task-data-map.csv` with exactly these columns: `Task`, `Functional Area`, `Offering`, `Data`. `Data` is the absolute path of the corresponding exported CSV. This CSV is a derived compatibility handoff, not a matching or review record. Repeat Task rows when distinct source sections resolve to the same approved task; do not merge different shapes of data.
7. Register artifacts, update project state, record the run, and append the token-use log. Use a new `v{major}` directory for a major rerun; seek confirmation before replacing a current minor version.

## Matching evidence and confidence

- Record the source section, matching method (`explicit`, `exact-name`, `exact-code`, or `semantic`), matched catalog task code, confidence, and any inference in the run record.
- Exact tab/table code matches such as `INV_UNIT_OF_MEASURE` take precedence over lexical similarity.
- A task name that occurs in several offerings is not enough by itself. Use the user’s supplied offering/functional area, source codes, header vocabulary, and workspace skill hierarchy to disambiguate.
- A tab representing a configuration entity may map to the setup task that owns that entity; record this as semantic matching.

## Validation and failure handling

- Validate that all mapping paths exist, are unique per source section, and that every CSV has one header row and at least its extracted rows.
- Validate the map header and catalog identity before persistence.
- Failure classes: `input validation`, `catalog mismatch`, `artifact persistence`, and `approval blocker` (ambiguous match or an existing output requiring replacement).
- Do not retry a catalog mismatch or an ambiguous match without changed input or user direction. Filesystem persistence failures may be retried once after path validation.
- Redact credentials, tokens, and sensitive values from diagnostics. Do not persist the original input file unless the user explicitly asks.

## Downstream handoff

Provide the mapping CSV to a setup skill. That skill must use the `Data` path for the matching task and perform its own data validation before any import or live execution.
