---
skill_id: "cx.sales.opportunities.manage-sales-task-templates"
name: "Manage Sales Task Templates Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Sales Task Templates under the Opportunities functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "ZBS_MANAGE_SALES_TASK_TEMPLATE"
task_name: "Manage Sales Task Templates"
parent_skill_id: "cx.sales.opportunities"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.1.12"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "set_selection_decision"
  - "reference_data_set_identity"
  - "task_context_path_optional"
  - "task_sequence_optional"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-sales-task-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-sales-task-templates/current/"
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

# Manage Sales Task Templates Setup Task Guidance

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may be generated from the project's resolved setup-task
plan without creating an Oracle Run Book. Never hand-author, infer, or
synthesize a context entry merely to satisfy Data Loader.

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Sales Task Templates` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `ZBS_MANAGE_SALES_TASK_TEMPLATE`
- task_name: `Manage Sales Task Templates`
- parent_skill_id: `cx.sales.opportunities`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Opportunities`
- functional_area_code: `ORA_MOO_OPPORTUNITIES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Sales Task Templates` under `Opportunities`.

## Supported Scenarios

- Create an Opportunity task template with its name, optional description, active state, subtype, and reference-data set.
- Add one or more template tasks with a subject and optional description, lead time, task type, duration, and priority.
- Review or update an existing template or one of its task definitions through the documented setup task.
- Prepare the downstream association of a task template to an opportunity sales stage through `Manage Sales Methods and Sales Stages`.
- Enforce `Automatically generated` when the intended outcome is for generated tasks to appear to users in the opportunity Activities tab.
- Export, validate, import, and verify catalog-supported setup data using the current task-specific CSV package.
- Stop unsupported direct REST mutations and route changes through the guided setup task or the approved Functional Setup Manager CSV import path.

## Set ID Selection

Never default an Opportunity task template to Common Set. If the request does
not identify a template set, ask whether Common Set should be used or a
different exact Set ID or Set Code should be selected. When the requester
supplies a business unit instead, resolve its intended set through the
documented setup path and require one exact result. Preserve the confirmed set
choice in guided setup and every reviewed CSV row. Common Set confirmation is
not mutation approval.

Validate SetId as an integer with exact selected-target setup/package evidence,
not as a positive-only value. An explicitly confirmed Common Set can resolve
to zero; preserve the verified numeric or CSV text zero and never infer Common
Set or default its ID from the number alone.

## Negative Set Scenarios

Reject a malformed or unknown Set ID/Set Code, conflicting Set ID and Set Code,
a confirmed Common Set choice that resolves to a non-Common set, or a template
CSV row whose set differs from the confirmed or fresh-export identity. Do not
substitute Common Set, another environment's set, or a close match. Return the
exact mismatch and request one valid set decision before guided setup or package
review continues.

## Oracle Resource Read Order

For task-specific execution planning, read the generated resource guidance in this order:

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Setup Task Metadata

- Task name: `Manage Sales Task Templates`
- Task code: `ZBS_MANAGE_SALES_TASK_TEMPLATE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Validate the final immutable task package and hand it to `core.data-loader`.
5. Let Core Data Loader persist its immutable upload artifact, preflight
   envelope and Task Hook-bound preview, then own contextual approval, upload
   and initiation under its current contract. Approval applies to that exact
   saved artifact and context; this child does not require a fixed user keyword
   or define a separate submission protocol.

This is the only supported automated route for a setup-data mutation. Use
read-only discovery only to prepare or later verify the package; direct REST
mutation is unsupported for this task.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Opportunities`
- Setup task name: `Manage Sales Task Templates`
- Setup task code: `ZBS_MANAGE_SALES_TASK_TEMPLATE`

## Execution Route Selection

For a supported mutation, default to the CSV/FSM workflow above and
`core.data-loader`. Do not initialize browser control as an alternate import
adapter. Use the guided setup procedure only when the requester explicitly asks
for manual UI. If the task-specific package cannot represent the requested
change, fail closed and report that limitation before any live action. This
task defines no direct REST mutation exception.

For the default FSM route, this child skill owns package validation and handoff
only. It must not request package approval, construct or reconstruct a Task Hook
approval, upload the package, or initiate the import. Bind the exact target,
task identity, final ZIP path and SHA-256, metadata task identity, member and
header receipt, reviewed row delta, and validation result before handoff;
bind persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area. Core
Data Loader owns Task Hook execution, the persisted immutable upload artifact
and preflight envelope, its preview, contextual approval, upload and initiation.
Follow its current contract: after approval, Core verifies the saved artifact's
integrity, selected environment, Run Book context and approved Task Hook
envelope, then submits those exact saved bytes. It does not reopen the original
source, rebuild the artifact, refresh live metadata or rerun Task Hook rules.
Requested material changes require a fresh core validation/preview lifecycle
and approval. This child does not reconstruct or submit the approved load.

An accepted Core Data Loader initiation is terminal for that request. Polling,
ProcessLog retrieval, result inspection, and read-only verification may run
only after a later explicit status or results request.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `set_selection_decision`: explicit confirmation to use Common Set or to use
  a different set
- `reference_data_set_identity`: exact Set ID or Set Code when a different set
  is selected, or the documented business-unit selector used to resolve it

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Offline Validation Evidence

Use [golden-scenarios.md](tests/golden-scenarios.md) for explicit synthetic set
choices, native package handoff, manual review/setup and export/refusal cases.
The suite checks current source/registry equivalence, review/export node
applicability and graph prerequisites/terminals with supplied outcomes:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s pillars/cx/sales/opportunities/manage-sales-task-templates/tests -p 'test_*.py' -v
```

The fixtures require semantic source review for field decisions; they do not
emulate Fusion. Core Data Loader's approved-preflight tests cover saved-artifact
reuse, integrity and environment/Run Book/Task Hook context checks, and approved
submission without reopening the original source or refreshing live metadata.
