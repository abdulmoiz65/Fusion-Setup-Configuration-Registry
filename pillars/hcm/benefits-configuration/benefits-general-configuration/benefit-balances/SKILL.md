---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.benefit-balances"
name: "Benefit Balances Setup Task Guidance"
description: "Provides task-specific setup guidance for Benefit Balances under the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_BENEFIT_BALANCE"
task_name: "Benefit Balances"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitBalances"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
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
  - "hdl_preflight_result"
  - "load_diagnostic"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.benefits-configuration.benefits-general-configuration"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/benefit-balances/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/benefit-balances/current/"
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
  - "Reads selected-environment LOV resources when the active workflow authorizes reference validation."
required_privileges:
  - "Read access to selected-environment LOV resources for supplied reference fields."
---

# Benefit Balances Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Benefit Balances` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_BENEFIT_BALANCE`
- task_name: `Benefit Balances`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `HDL`
- businessObject: `benefitBalances`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Benefit Balances` under `Benefits General Configuration`.

## Setup Task Metadata

- Task name: `Benefit Balances`
- Task code: `BEN_MANAGE_BENEFIT_BALANCE`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `benefitBalances`

## HDL Business Object and Routing

`CSVExportImportSupportedFlag` is `N`; FSM CSV export/import is therefore not a supported route for this task. This does not prohibit the explicitly selected HDL route.

Use `core.data-loader` for Benefit Balances data loads. The supported HDL business object is `benefitBalances`; do not substitute the task label or a guessed REST resource. Generate the DAT structure from current Fusion Data Loader metadata before preparing a file. Do not use FSM CSV export/import, browser entry, REST, or an alternate loader as a substitute route.

The object configures a benefit balance. Validate the balance name, legal employer, and every other identity or prerequisite required by the current Data Loader sample before load preparation. The source DAT header and mandatory/optional attributes are release-sensitive, so the live Data Loader sample is authoritative over this skill.

For each supplied `benefitBalances.BalanceUsageMeaning`, `NonMonetaryUnitsMeaning`,
`LegalEmployerName`, or `CurrencyName`, apply the exact-match, read-only checks
in [reference lookups](ora-resource/ora_reference_lookups.md) before finalizing
the source. Use `core.fusion-api.rest-api-client` only when the active project
workflow selects this lookup step. A 403 records `unverified_forbidden` for that
field and does not fail field validation or stop independent checks; it does
not verify the value. Resolve access or use another workflow-approved
authoritative check before a live load. Keep HDL schema validation and loading
on the `core.data-loader` route.

For a supported date-effective create, update, or correction row whose current
section exposes `EffectiveEndDate`, default an omitted value to the end-of-time
date `4712/12/31`; preserve a supplied value. Serialize the resulting DAT date
in the format required by the current section contract. An End date operation
requires the user's explicit end date and never uses this default.

## HDL CRUD Operations

| Requested operation | HDL route | Control point |
| --- | --- | --- |
| Create or merge | Create a `benefitBalances` DAT using the generated current sample. | Validate the immutable artifact and obtain Data Loader workflow approval before upload. |
| Read / verify | Inspect metadata, load status, or a workflow-selected supported read route. | Read-only inspection does not authorize a subsequent load. |
| Update | Create a corrected or replacement DAT only when the current HDL schema and source identity support it. | Do not guess user keys or action syntax; revalidate and obtain a new approval. |
| Delete | Use an explicitly reviewed delete DAT only when current HDL metadata supports the requested deletion. | Treat as destructive; require explicit approval immediately before upload or initiation. |

## Preflight and Approval Gates

1. Confirm task `BEN_MANAGE_BENEFIT_BALANCE`, the `benefitBalances` business object, intended environment, and active project Run Book.
2. Generate or retrieve the current Data Loader sample; validate the DAT format, balance name, legal employer, and all required source identifiers and configuration facts required by that sample. For every included section, confirm its date-effectivity, `effectiveOf` field availability, and supported row operations independently; stop if any contract is missing or ambiguous.
3. Validate every record and preserve row-level errors. Run the four conditional
   reference lookups through the selected shared REST client; record each
   supplied field as `valid`, `invalid`, `ambiguous`, or `unverified_forbidden`.
   Stop on ambiguous identities, missing dependencies, unsupported action
   semantics, or CSV routing.
   For each included section that exposes `effectiveOf`, derive it per row using the task-local operation mapping. Format every embedded date as `YYYY-MM-DD` before constructing the DAT; reject invalid or ambiguous source dates. Omit `effectiveOf` entirely from a section that does not expose it.
4. Create an immutable load artifact and preflight it through `core.data-loader`.
5. For Create, Update, or Delete, use the Data Loader workflow's current approval gate immediately before upload or initiation. Any artifact, target, or record change invalidates the approval.

## Failure Handling

Load the task-local `ora-resource/ora_input_validation.md`, `ora_dependency_readiness.md`, `ora_reference_lookups.md`, `ora_defaulting_rules.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` before preflight or live activity. Persist sanitized preflight and load diagnostics under the declared project workspace when `project_id` is provided.

Never automatically retry a DAT upload, load initiation, update, or delete. On an uncertain or failed load, preserve the artifact checksum, target environment, task code, object, request or process identifier, status, elapsed wait, and available process log; redact payload values and all credentials. Reconcile the outcome through the workflow-selected read-only status route before any newly approved action.


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

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Benefit Reporting Groups precedes this task in the catalog dependency sequence. Track token usage for any generated project artifact or skill-run record using the manifest policy.
