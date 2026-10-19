---
skill_id: "hcm.global-payroll.payroll-balances.balance-exceptions"
name: "Balance Exceptions Setup Task Guidance"
description: "Provides task-specific setup guidance and read-only ID resolution for Balance Exceptions under the Payroll Balances functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Balances"
functional_area_code: "ORA_PAYROLL_BALANCES"
task_code: "PAY_MANAGE_BALANCE_EXCEPTIONS"
task_name: "Balance Exceptions"
parent_skill_id: "hcm.global-payroll.payroll-balances"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
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
  - "core.auth.fusion-oauth-authentication"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-exceptions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-exceptions/current/"
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
  - "Read-only reference GET requests to the configured Fusion pod when live resolution is selected."
  - "Writes redacted resolution evidence to the active project workspace."
required_privileges:
  - "Fusion privileges to view the selected LDG, defined balances, or balance groups."
---

# Balance Exceptions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Balance Exceptions` under `Payroll Balances`.

## Setup Task Skill Contract

- task_code: `PAY_MANAGE_BALANCE_EXCEPTIONS`
- task_name: `Balance Exceptions`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Balance Exceptions` under `Payroll Balances`.

## Setup Task Metadata

- Task name: `Balance Exceptions`
- Task code: `PAY_MANAGE_BALANCE_EXCEPTIONS`
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
- Setup task name: `Balance Exceptions`
- Setup task code: `PAY_MANAGE_BALANCE_EXCEPTIONS`


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

## Reference ID Resolution

Before preparing an FSM import, use the read-only resolver in
`scripts/resolve_balance_reference.py` only after the router, active project/run
book, target environment, OAuth, and a workflow-approved current UI runtime
context have been checked. For a user-supplied HAR from the exact target pod,
`--har-source` may select one successful GET route captured within 24 hours as
a candidate for this run. Require a fresh exact LDG GET through that candidate
before any dependent lookup; do not persist or reuse the context as a stable
endpoint. Reject a wrong-host, stale, or ambiguous HAR. Do not obtain a context
through an undeclared browser route.
Oracle's documented public payrollGenericLOV collection returned no selectable
Current period option for the BalanceExceptionUI comparison provider in
`cptczmdqy` QA, so it is not a validated substitute. If neither a current
workflow context nor a recent same-pod HAR candidate passes the fresh LDG
check, record a catalog mismatch and stop. Select exactly one source:
`--balance-name` with `--dimension-name`, or `--balance-group-name`. Pass the
exact LDG name, expected environment label, token cache, and an evidence path
under the active project's `artifacts` directory. The resolver uses the shared
Fusion OAuth client and only GET requests; it does not create an exception.

```text
py -3 pillars/hcm/global-payroll/payroll-balances/balance-exceptions/scripts/resolve_balance_reference.py \
  --ldg-name "<exact LDG name>" \
  --balance-name "<exact balance name>" \
  --dimension-name "<exact dimension name>" \
  --comparison-type "<exact selectable comparison label or code>" \
  --variance-type "<exact variance type label or code>" \
  --variance-operator "<exact operator label or code>" \
  --severity-level "<exact severity label or code>" \
  --har-source "<user-supplied same-pod HAR path>" \
  --expect-environment "<configured environment>" \
  --token-cache .fusionaim_token.json \
  --output project/<project_id>/artifacts/pillars/hcm/global-payroll/payroll-balances/balance-exceptions/current/defined-balance-reference.json
```

Use `--runtime-context` instead only when the active UI workflow supplied a
current context independently. Both routes require the fresh LDG and dependent
provider GET checks before an ID is accepted.

For a group, replace `--balance-name` and `--dimension-name` with
`--balance-group-name` and use a separate `balance-group-reference.json` output.
Omit `--variance-type` for a group source until the group ID is resolved;
its available variance choices depend on the selected group.
The returned `DefinedBalanceId` or `BalanceGroupId` is an internal target-pod
identifier, never a value inferred from display text. Require exactly one
positive numeric ID in the same LDG. The resolver uses the harvested
`BalanceExceptionUI` comparison, balance, dimension, and group providers;
the current target response must confirm their contract. If the target service does not return the
ID, reports an ambiguous match, or cannot prove complete paging, stop before
building the import ZIP. Preserve the FSM template and all existing preflight
evidence. See `ora-resource/ora_reference_lookups.md` for the precise request
and matching contract.
