---
skill_id: "hcm.global-payroll.payroll-balances.balance-exception-reports"
name: "Balance Exception Reports Setup Task Guidance"
description: "Provides task-specific setup guidance for Balance Exception Reports under the Payroll Balances functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Balances"
functional_area_code: "ORA_PAYROLL_BALANCES"
task_code: "PAY_MANAGE_BALANCE_EXCEPTION_REPORTS"
task_name: "Balance Exception Reports"
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
version: "0.1.9"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-exception-reports/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-exception-reports/current/"
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

# Balance Exception Reports Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Balance Exception Reports` under `Payroll Balances`.

## Setup Task Skill Contract

- task_code: `PAY_MANAGE_BALANCE_EXCEPTION_REPORTS`
- task_name: `Balance Exception Reports`
- parent_skill_id: `hcm.global-payroll.payroll-balances`
- pillar: `HCM`
- offering: `Payroll`
- functional_area: `Payroll Balances`
- functional_area_code: `ORA_PAYROLL_BALANCES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Balance Exception Reports` under `Payroll Balances`.

## Setup Task Metadata

- Task name: `Balance Exception Reports`
- Task code: `PAY_MANAGE_BALANCE_EXCEPTION_REPORTS`
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

Use this task metadata when invoking those skills:

- Offering: `Global Payroll`
- Functional area / Setup Object: `Payroll Balances`
- Setup task name: `Balance Exception Reports`
- Setup task code: `PAY_MANAGE_BALANCE_EXCEPTION_REPORTS`


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

For an FSM import that adds included exceptions, read the task's `ora-resource`
validation guidance before preparing the child CSV row. The task-specific
`PAY_EXCEPTION_REPORT_SUFFIX` relationship uses its own view instance and
grouping-key format; copying the parent `PAY_EXCEPTION_REPORT_GROUP` values
into the child row is invalid.

Payroll and Consolidation Group are optional business restrictions. When an FSM
report intentionally has neither restriction, retain blank display-name columns
and encode the corresponding identifier columns as `#null`, matching a current
task data export. `#null` means no restriction; it does not make either
attribute mandatory. An empty CSV identifier field is not equivalent to the
FSM null sentinel.

Users provide the Balance Exception name as shown in the UI; they are not
expected to provide `BalExceptionId`. Before FSM preparation, resolve that
name through the FSM seeded-reference evaluator. It evaluates the exact name,
selected LDG, and legislation applicability; it must distinguish an
LDG-owned exception from a compatible seeded/shared US exception. A seeded
exception remains eligible even when omitted from an LDG-owned FSM export.
This evaluation is not an export of an existing report. Retain the resolved
identity and provenance as validation evidence, use the canonical
`BaseBalExceptionName`, and populate `BalExceptionId` internally only when
the target importer requires that binding.

Use the lookup contract in
`ora-resource/ora_reference_lookups.md` for the seeded-reference step. Invoke
the shared `core/fusion-api/rest-api-client` only when the routed workflow
permits a read-only target lookup. Supply the resolved LDG ID, legislation
code, and exact UI name; accept only one LDG-owned or compatible
seeded/shared binding. Do not substitute an existing report or Balance
Exceptions FSM export for this check. The skill ships no pillar-local resolver
executable.
