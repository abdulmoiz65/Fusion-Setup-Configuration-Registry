---
skill_id: "erp.project-financial-management.project-foundation.manage-rate-schedules"
name: "Manage Rate Schedules Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Rate Schedules under the Project Foundation functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_LABOR_RATE_SCHEDULES"
task_name: "Manage Rate Schedules"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.2.7"
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
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-rate-schedules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-rate-schedules/current/"
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
  - "Reads workflow-selected rate-schedule baselines, operation metadata and supported references through the shared REST/export services."
  - "Writes task plans, validation evidence and run records through the declared core project services."
  - "Delegates approved imports to core.data-loader and its selected adapter; this pillar does not submit writes itself."
required_privileges:
  - "Rate Schedules and requested subtype/reference REST read access for the selected workflow"
  - "Public Workers REST read access when resolving a Person display name to PersonNumber and WorkEmail"
  - "Standard Lookups PJF_UNIT and Units of Measure REST read access when resolving rate-unit names to codes"
  - "FSM setup-task export access when the selected workflow requires a baseline or template export"
  - "Task-specific create/update/import privileges for the selected Data Loader adapter before approved execution"
---

# Manage Rate Schedules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Rate Schedules` under `Project Foundation`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_LABOR_RATE_SCHEDULES`
- task_name: `Manage Rate Schedules`
- parent_skill_id: `erp.project-financial-management.project-foundation`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Foundation`
- functional_area_code: `ORA_PJF_PROJECT_FOUNDATION_FA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Rate Schedules` under `Project Foundation`.

## Supported Task Behavior

Create, update, copy, end-date, validate, or explicitly delete project rate schedules for Person, Job, Project Role, Nonlabor, and Resource Class types. Validate immutable header attributes, subtype-specific line keys, effective-date overlap, reference effectiveness, rate/markup/UOM rules, specificity precedence, and active use. Omitted lines preserve current rows.

Accept a Person display name as business input. Before building a Person CSV line, resolve that name to `PersonNumber` and `WorkEmail` using the read-only `publicWorkers` contract in [ora-resource/ora_reference_lookups.md](ora-resource/ora_reference_lookups.md#person-name-to-person-number-and-email). Do not require the user to supply either value when this lookup resolves one person with both values and the email resolves back to that one person. Serialize both on the Person line: this target's observed FSM import rejects a missing `EmailAddress` with `JBO-27035` and rejects a shared email with `PJF_FSM_DUPL_PERSON_EMAIL`. This directory lookup establishes identity only; retain separate eligibility findings and the existing Data Loader approval workflow.

Accept unit-of-measure names or codes and resolve supplied UOM intent through [Rate Unit Name to Code](ora-resource/ora_reference_lookups.md#rate-unit-name-to-code) before serializing `RateUnit`. That contract combines project `PJF_UNIT` lookup meanings/codes with inventory UOM names/codes. Do not ask the user for a code when the lookup resolves it uniquely.

Prefer the exact writable `rateSchedules` REST resource per operation when target discovery confirms all requested fields. Otherwise select the evidenced FSM CSV route before preview. Never switch routes after approval.

For REST, separate schedule-header creation from rate-line creation. A successful GET or a field in a published response is not writable-field evidence. Apply the endpoint/subtype contract and payload examples in `ora-resource/ora_input_validation.md` and the capability ledger in `ora-resource/ora_reference_lookups.md` before declaring `direct_writable_rest`. In particular, do not flatten Resource Class rate-line fields into the schedule-header POST based only on the public discriminator schema.

## Setup Task Metadata

- Task name: `Manage Rate Schedules`
- Task code: `PJF_MANAGE_LABOR_RATE_SCHEDULES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Route the documented read-only baseline and capability lookups through `core.fusion-api.rest-api-client`, with exact target identity, privileges and pagination evidence. Record operation-specific header, subtype-line and DFF methods, paths, fields and runtime context; observed write capability is not execution authorization.
2. Execute `ora-resource/ora_rule_registry.json` in sequence.
3. Select the evidenced REST-backed or exact FSM CSV import contract through `core.data-loader` before building the diff. Every import, including a REST-backed create/update, must use Data Loader's selected adapter and Task Hook route. If that adapter is unavailable or unproven for the requested operation, return the exact workflow gap and stop the affected write; do not call the REST client as an import shortcut.
4. Validate identity, immutable attributes, subtype line keys, dates/overlap, references, values, precedence, and use.
5. Produce an immutable route-specific preview and checksum. For a staged REST create, preview both the header POST and each Rates child POST, including the returned-ID binding and partial-success behavior, before executing either stage.
6. Before submission, preflight a safe writable receipt destination in the selected project's task artifacts. Submit the immutable approved payload/package through the selected `core.data-loader` adapter and its approval workflow; do not retry or change route automatically. Register returned UCM/request identifiers, approved artifact reference/checksum, target, project, task and latest status through the declared core project services. Return the loader's complete In Progress report without automatic status checks, process logs, exports or readback. Acceptance means initiated, not completed or verified. Capability discovery alone never selects a direct write route. If submission is uncertain or receipt persistence fails, preserve known identifiers, record the failure and stop; repair only local evidence and never resubmit under the old approval.
7. Only on a later explicit status/results/verification request, validate the registered target, project, task, request ID and approved-artifact binding before external calls. Missing or mismatched context blocks. Delegate status/count/error checks to `core.data-loader`; never repeat preparation, approval or submission. A status-only request returns that status without target readback. An active status or bounded timeout returns In Progress and waits for another request; terminal failure stops. For requested setup verification, require terminal success before using the already selected read-only REST or same-task export route. Compare every requested header and subtype line, canonical identity, dates, qualifiers, UOM and amounts with the approved preview, including preserved rows. Retain partial successes and diagnostics; incomplete or mismatched readback prevents verified completion and does not authorize another write.

An indeterminate submission with no recoverable request ID requires a later
explicit recovery request. The active workflow selects supported read/status
reconciliation from known identifiers or the declared task baseline route;
it must not invent an adapter or switch execution routes. Recovery does not
select preparation or authorize resubmission. A corrected or genuinely new
load still requires fresh validation, an immutable preview and approval through
Data Loader. These lifecycle boundaries also govern post-load reconciliation
and partial-success guidance in the task resources: retain available failure
evidence now, and perform further external reads only in the later requested
workflow.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Foundation`
- Setup task name: `Manage Rate Schedules`
- Setup task code: `PJF_MANAGE_LABOR_RATE_SCHEDULES`


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

Use the parent skill for sequencing. Supplied reports are observed exports, not blank templates. Track token usage using the manifest policy.

## Local Validation Evidence

Task tests and synthetic review fixtures are in
[noship/tests/project-foundation/manage-rate-schedules](../../noship/tests/project-foundation/manage-rate-schedules/).
The golden cases review the source-owned domain decisions. Python tests exercise
the actual registry branches, ordered evidence, warning/error precedence and
core preview refusal; they do not evaluate rates or simulate a live import.
The live YAML's limited coverage and omitted behaviors remain explicit.
Read handoff and shared executor checks are at
[the functional-area test level](../../noship/tests/project-foundation/test_project_foundation_executor_contract.py).

Before any live write, independently establish the selected adapter, target
operation schema, required privileges, references, immutable artifact and
approval through the existing workflow. Offline evidence does not prove those
runtime facts. Required reviewers are the ERP Pillar Development Lead or SME,
FSCR A-Team/core reviewer and QA for behavior/coverage changes.

## Refined Best-Practice Control Contract

Before producing a design recommendation, validation result, import preview, or completion claim, execute [ora-resource/ora_rule_registry.json](ora-resource/ora_rule_registry.json) and apply the refined controls from the standard `ora_input_validation.md`, `ora_defaulting_rules.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` resources selected by that graph.

- Treat every **Blocking control** as a stop gate. Do not preview or approve a configuration that violates it.
- Treat every **Required evidence** item as mandatory decision evidence. Return `needs_input` with the missing fields instead of silently defaulting.
- Treat every **Operational control** as a required readiness output. A one-time setup can be technically valid without the report, but the skill must not claim operational readiness until the report or reconciliation is defined.
- Ownership and purpose under BP-075/BP-076 are optional advisory context, not required Fusion setup inputs or execution gates. Reuse supplied names, descriptions, and business intent without asking for separate purpose confirmation; do not block creation because ownership or purpose is absent. Retain the selected core workflow's technical validation and execution approval gates.
- Preserve documented exceptions only where the control explicitly allows one; capture rationale, owner, approval reference, effective dates, and review date.
- Recalculate source-document population counts from the current target. Historical counts in the source are context, not validation constants.
