---
skill_id: "erp.project-financial-management.project-organizations.manage-project-unit-options"
name: "Manage Project Unit Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Project Unit Options under the Project Organizations functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
task_code: "PJF_MANAGE_PROJECT_UNITS"
task_name: "Manage Project Unit Options"
parent_skill_id: "erp.project-financial-management.project-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.1.2"
inputs:
  - "project_id"
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "execution_receipt_record"
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
persists_project_state: true
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-options/current/"
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
  - "Writes task plans, validation/preview evidence, execution receipts and redacted diagnostics to the selected project workspace through core project services."
required_privileges: []
---

# Manage Project Unit Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Project Unit Options` under `Project Organizations`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_PROJECT_UNITS`
- task_name: `Manage Project Unit Options`
- parent_skill_id: `erp.project-financial-management.project-organizations`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Organizations`
- functional_area_code: `ORA_PJF_PROJ_ORG`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Project Unit Options` under `Project Organizations`.

## Supported Task Behavior

Configure one existing classified project unit across the same-task option surfaces:

- general properties: enabled default reference set and project-numbering method/type;
- automatic numbering: next number and optional prefix when the target feature makes this task the owning setup surface;
- related business units: add requested exact business-unit names for Fusion import validation and remove only unused, deletable relationships;
- performance reporting: commitment inclusion/status and planning-amount allocation basis.

Require exact project-unit identity and a fresh target-pod option baseline. Treat an ordinary Default Set value as an exact set name; use an exact set code only when the user explicitly identifies it as a code. Manual numbering requires Numeric or Alphanumeric type. Automatic numbering requires a positive, nonconflicting next number. A selected commitment type requires status `Approved` or `All`; an unselected type cannot carry an active status.

A newly configured project unit is not complete when its implementation and business-unit relationship rows exist but its `PJF_REPORTING_SETUP` row is absent. Require a complete, customer-approved reporting-options row before this task is reported successful or the project unit is handed to Project Plan Type or Project Template setup. Existing reporting values may be preserved on update only when that row actually exists. Do not copy a seeded project unit's values as defaults; they may be proposed explicitly for customer approval when parity is intended.

Keep Manage Project Unit Set Assignments separate. The UI links to that flow and a public REST resource exists for its own contract, but the supplied business-object package for this task does not authorize silently merging set-assignment rows into Manage Project Unit Options.

Use FSM CSV for the composite option write. No exact writable public REST contract was proven for this whole task. Require target feature status, current export, reference-set metadata, relationship usage/deletability evidence for removals, and a validated task package template before import preview. For business-unit additions, pre-import validation checks only nonblank, unique exact names; no independent Project Accounting eligibility evidence is required. Fusion FSM import determines eligibility. Retain any returned Fusion error against the requested relationship and immutable package; never retry a rejected import automatically.

## Setup Task Metadata

- Task name: `Manage Project Unit Options`
- Task code: `PJF_MANAGE_PROJECT_UNITS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export current task data with `shared.setup-export.task-level-export` and join implementation, numbering, reporting, and relationship members for one project unit.
2. Read and execute `ora-resource/ora_rule_registry.json` in sequence; do not bypass an incomplete or failed node.
3. Build a task-scoped FSM package preserving the target-validated option member contracts; never add separate set-assignment rows.
4. Validate setup data with `shared.validation.setup-data-validator` and references with `shared.validation.reference-data-validator`.
5. Produce an immutable preview showing target, project unit, default set, feature status, numbering values, every business-unit addition/removal, every reporting flag/status, allocation basis, whether the reporting row exists before and after, changed fields, row counts, warnings, and checksum.
6. Route the immutable package to `core.data-loader`. A same-request `auto-approve`, `auto approve`, `approve without asking`, or `skip confirmation` instruction authorizes this one load after every validation gate passes; otherwise wait for later approval of the exact preview. Auto-approval never waives validation or authorizes a retry.
7. Before submission, designate a task-local execution-receipt record. Immediately persist the returned UCM Content ID, Data Loader Request ID, submitted checksum, target, and latest status there before any follow-up call. Do not rely on console output as the only receipt. A write with no durable request ID is indeterminate: perform fresh read-only target-state recovery and never submit again under the old approval.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Organizations`
- Setup task name: `Manage Project Unit Options`
- Setup task code: `PJF_MANAGE_PROJECT_UNITS`

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`

## Implementation Notes

Use the parent functional-area skill `erp.project-financial-management.project-organizations` for functional-area sequencing and scope decisions. Complete project-unit organization/classification setup before these options. Do not add a separate Project Accounting enablement prerequisite for requested business-unit additions; Fusion validates their eligibility during the approved FSM import.

Apply numbering defaults only under the new-row, missing-setup, or explicit method-transition conditions in `ora-resource/ora_defaulting_rules.md`; a hidden numbering region alone does not justify a default. Omitted relationship fields mean preserve current state, not delete or clear. Omitted reporting fields preserve current state only when the same project unit already has a complete `PJF_REPORTING_SETUP` row; absence of that row is an incomplete setup condition, not a valid preserved state.

Use a fresh target template for package generation. Keep exact template validation, immutable preview, target disclosure, and approval as runtime gates.

## Durable Artifacts and Review

Resolve `project_id` from the selected existing implementation project before preparation or execution; missing project identity is an input-validation blocker. Persist plans, validation results, immutable previews, approved package references, execution receipts and redacted failure diagnostics under `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-options/current/`. Raw exports belong under `project/{project_id}/exports/project-financial-management/project-organizations/manage-project-unit-options/`. Never persist credentials or tokens there.

Use `core.project-mgmt.artifact-version-manager` for major new versions and confirmed minor updates, `core.project-mgmt.artifact-registry-manager` to register each durable artifact, and `core.project-mgmt.project-state-manager` to update only declared state fields and record the run under `project/{project_id}/state/runs/`. Persist each receipt before the next external call; append later statuses and retain partial failures, environment, operation, external IDs, artifact references and next action. Recover uncertain writes through supported reads; do not resubmit automatically. Record token usage using the manifest policy.

Required reviewers: responsible ERP Pillar Development Lead or SME, FSCR A-Team/core reviewer, and QA for validation/execution changes. Package readiness does not replace merge approval.
## Related Business Unit Validation

For related-business-unit additions, validate only nonblank, unique supplied exact names locally and include every name unchanged in the immutable FSM preview. Do not pre-judge Project Accounting enablement or silently skip an unconfigured business unit. Fusion validates eligibility during import; persist its accepted result or returned error with the requested name and package checksum, and do not retry a rejected package automatically. Relationship removal still requires current usage and deletability evidence.
