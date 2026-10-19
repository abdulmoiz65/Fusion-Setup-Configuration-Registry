---
skill_id: "hcm.global-payroll.payroll-balances.balance-groups"
name: "Balance Groups Setup Task Guidance"
description: "Provides task-specific setup guidance for Balance Groups under the Payroll Balances functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Balances"
functional_area_code: "ORA_PAYROLL_BALANCES"
task_code: "ORA_PAY_MANAGE_BALANCE_GROUPS"
task_name: "Balance Groups"
parent_skill_id: "hcm.global-payroll.payroll-balances"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-groups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-groups/current/"
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

# Balance Groups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Balance Groups` under `Payroll Balances`.

## Setup Task Skill Contract

- task_code: `ORA_PAY_MANAGE_BALANCE_GROUPS`
- task_name: `Balance Groups`
- parent_skill_id: `hcm.global-payroll.payroll-balances`
- pillar: `HCM`
- offering: `Global Payroll`
- functional_area: `Payroll Balances`
- functional_area_code: `ORA_PAYROLL_BALANCES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: `""` (no business-object selection)
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Balance Groups` under `Payroll Balances`.

## Setup Task Metadata

- Task name: `Balance Groups`
- Task code: `ORA_PAY_MANAGE_BALANCE_GROUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using the FSM route and the task's setup-data ZIP archive. Do not select or pass a business object.

Use this task metadata when invoking those skills:

- Offering: `Global Payroll`
- Functional area / Setup Object: `Payroll Balances`
- Setup task name: `Balance Groups`
- Setup task code: `ORA_PAY_MANAGE_BALANCE_GROUPS`
- Data Loader import mode: `FSM`

### FSM Import Contract

Use the FSM setup-data archive for `ORA_PAY_MANAGE_BALANCE_GROUPS`. The archive must contain `ASM_SETUP_CSV_METADATA.xml`; preserve the archive unchanged and let `core.data-loader` validate and classify it as FSM with `sourceType: "FSM"`. Keep the task-validation and approval gates required by `core.data-loader`.

Leave `businessObject` empty. Do not request a registered business object, download an HDL business-object template, generate a DAT file, or apply HDL business-object validation to this FSM archive. The task's `ora-resource/` rules validate FSM artifact format, task identity, and complete requested scope. If the FSM archive is missing or invalid, stop and obtain a valid task setup-data archive through the routed export workflow.

Before handing an archive to core.data-loader, this Balance Groups task must inspect its local format, before authentication or live metadata lookup. An FSM XML configuration package containing `ASM_MIG_PROCESS_INFO.xml` and nested `businessObjectData/` or `taskListData/` archives is reference material for this CSV route. Reject it as `FSM_CONFIGURATION_PACKAGE_UNSUPPORTED`, including when a CSV metadata marker has been added. Do not upload it as a task CSV package, inject a CSV metadata marker, or infer a conversion from XML tags. Obtain the actual task CSV template/export through `shared.setup-export.task-level-export` before creating rows. This preparation gate belongs to the Balance Groups task; it does not change generic core Data Loader behavior.

### Task Validation and Child Scope

Load `ora-resource/ora_input_validation.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` through the compiled task registry. The reference rules retain exact read-only LDG and parent-duplicate checks and document the sample's structural evidence. Consult `ora_defaulting_rules.md` before filling omitted values.

Definitions, group inclusions, balance/dimension assignments, and default inclusions are represented in the supplied XML reference. Their CSV fields and relationships must come from the task CSV template; they must not be limited to an existing HDL `AttributeCode`. The sample does not establish restriction-row or usage support. Verify their task-template coverage, and use the separate Balance Group Usages task when its contract is required. Never silently reduce a combined request to parent-only creation.

Refresh persisted planning and task-context `business_objects` from this manifest when resuming an earlier HDL plan. They must be empty for this task. Preserve task identity, sequence, and the active Run Book binding; changed artifacts require the normal task-validation and Data Loader approval workflow.


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

Use the parent functional-area skill `hcm.global-payroll.payroll-balances` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
