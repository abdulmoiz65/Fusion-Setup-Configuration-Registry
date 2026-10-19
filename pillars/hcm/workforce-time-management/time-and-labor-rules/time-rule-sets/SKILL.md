---
skill_id: "hcm.workforce-time-management.time-and-labor-rules.time-rule-sets"
name: "Time Rule Sets Setup Task Guidance"
description: "Provides task-specific setup guidance for Time Rule Sets under the Time and Labor Rules functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Rules"
functional_area_code: "ORA_TIME_AND_LABOR_RULES"
task_code: "ORA_HWM_MANAGE_RULE_SETS"
task_name: "Time Rule Sets"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-rules"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/time-rule-sets/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/time-rule-sets/current/"
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

# Time Rule Sets Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Time Rule Sets` under `Time and Labor Rules`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_MANAGE_RULE_SETS`
- task_name: `Time Rule Sets`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-rules`
- pillar: `HCM`
- offering: `Time and Labor`
- functional_area: `Time and Labor Rules`
- functional_area_code: `ORA_TIME_AND_LABOR_RULES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Time Rule Sets` under `Time and Labor Rules`.

## Setup Task Metadata

- Task name: `Time Rule Sets`
- Task code: `ORA_HWM_MANAGE_RULE_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

## Approved New Rule Set Orchestration

Treat an approved new Rule Set and its approved member list as one logical
configuration request. State before the first import that a new Rule Set with
members requires two Fusion imports:

1. A parent-only `ORA_HWM_RULE_SET` import.
2. A member-only `ORA_HWM_RULE_SET_MBR` import built after Fusion commits the
   parent and assigns `RuleSetUnqId`.

Drive the request through both stages without asking the user to restate the
member association:

1. Prepare and present the immutable parent archive preview. Stop for the
   exact Data Loader `approve` required for that archive. Before asking, show
   a clickable link to that exact validated parent FSM ZIP outside the business
   summary.
2. After parent approval, upload and initiate the parent import through
   `core.data-loader`.
3. Treat verification of that parent import as a required continuation of the
   already approved end-to-end request. Monitor or resume status verification
   until it reaches a terminal state; do not wait for the user to ask whether
   the member should be associated.
4. If the parent import fails, stop. Report the failure and do not prepare or
   upload a member archive.
5. If the parent import succeeds, refresh the authoritative Time Rule Sets
   export, resolve the committed `RuleSetUnqId`, and immediately prepare the
   member archive in approved `ProcessingOrder` sequence.
6. Present the immutable member archive preview automatically. Stop only for
   the separate exact Data Loader `approve` required for that archive. Before
   asking, show a clickable link to that exact validated member FSM ZIP outside
   the business summary.
7. Never treat parent-archive approval as approval to upload the member
   archive. After member approval, import it through `core.data-loader` and
   verify the exact relationships in a refreshed authoritative export.

If the approved Rule Set has no members, perform and verify only the parent
stage. Do not invent a member stage.

When parent verification or the authoritative refresh is still running at the
end of one bounded polling slice, continue polling the same process
automatically under `shared.setup-export.task-level-export`. Do not hand control
back merely to ask the user for `check`, `check now`, or `retry`. A polling
slice expiry does not end the approved logical request and does not authorize a
new import or export submission.

Use this task metadata when invoking those skills:

- Offering: `Time and Labor`
- Functional area / Setup Object: `Time and Labor Rules`
- Setup task name: `Time Rule Sets`
- Setup task code: `ORA_HWM_MANAGE_RULE_SETS`

## Staged FSM Package Preparation

For a Time Rule Set create or update, treat each approved parent or member
stage as an FSM import. After the required fresh Time Rule Sets export, prepare
the minimal stage-specific CSV package from normalized Rule Set intent. Use the
fresh export to retain the exact current headers and metadata for that stage;
never select, copy, or mutate an existing Rule Set row as a template.

- Prepare the parent package as a parent stage; it contains only
  `ORA_HWM_RULE_SET.csv` and metadata and leaves `RuleSetUnqId` blank.
- After the parent succeeds and a refreshed export supplies the committed ID,
  prepare the member package as a member stage; it contains only
  `ORA_HWM_RULE_SET_MBR.csv` and metadata.
- Normalized intent may supply any supported baseline header.
  Preserve an explicit blank string, `0`, or `#null` literally; do not replace
  it through truthy defaulting or introduce an unsupported field.
- Before preview or approval, validate the package through `core.data-loader`
  and the task package contract: stage membership, unchanged metadata, UTF-8
  BOM-free encoding, exact headers and row widths, stage linkage, processing
  order, and committed-parent use.

Validation failure is an approval blocker. Rebuild and validate a new archive;
never relabel an invalid ZIP as approved.


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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-rules` for functional-area sequencing and scope decisions. Preserve the complete approved parent-and-member intent across the two imports, including across turns or asynchronous processing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
