---
skill_id: "cx.sales.opportunities.manage-sales-methods-and-sales-stages"
name: "Manage Sales Methods and Sales Stages Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Sales Methods and Sales Stages under the Opportunities functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES"
task_name: "Manage Sales Methods and Sales Stages"
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
version: "0.1.14"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-sales-methods-and-sales-stages/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-sales-methods-and-sales-stages/current/"
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

# Manage Sales Methods and Sales Stages Setup Task Guidance

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
synthesize a context entry merely to satisfy Data Loader. This task-local
policy aligns with the Opportunities parent contract.

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Sales Methods and Sales Stages` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES`
- task_name: `Manage Sales Methods and Sales Stages`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Sales Methods and Sales Stages` under `Opportunities`.

## Setup Task Metadata

- Task name: `Manage Sales Methods and Sales Stages`
- Task code: `MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES`
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
4. Import setup task data with `core.data-loader`.

This is the only supported automated route for a setup-data mutation. Use
read-only discovery only to prepare or later verify the package; direct REST
mutation is unsupported for this task.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Opportunities`
- Setup task name: `Manage Sales Methods and Sales Stages`
- Setup task code: `MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES`




## Review-First Drafting

When the user asks Codex to perform this task without supplying every field,
Codex must create a complete review-only proposal instead of stopping for
field-by-field clarification. Use explicit user values first, preserve values
from an exact current-state target second, apply documented defaults third, and
use the synthetic sample below for every remaining applicable field. Mark every
sample-derived value as `assumed for review`.

Set selection is the exception to synthetic completion. Never default a new
sales method to Common Set. If the request omits its set, ask whether Common
Set should be used or a different exact Set ID or Set Code should be selected.
When a business-unit or organization selector is supplied, resolve it through
the documented set workflow and require exactly one result. Record the user's
choice in the review draft; confirmation of Common Set is not import approval.

Present the complete proposal and ask the user to approve it or list changes.
Review approval confirms the business design only. It does not approve a live
import. After the final package passes task-local validation, hand it to
`core.data-loader` without requesting package approval here. Core Data Loader
creates the Task Hook-bound immutable upload preview, stops, and requests the
later standalone `approve` that alone authorizes upload and initiation.

## Negative Set Scenarios

Reject a malformed or unknown Set ID/Set Code, a Set ID and Set Code that map
to different sets, a confirmed Common Set choice paired with a non-Common set,
or a sales-method package row whose set differs from the confirmed or baseline
identity. Do not replace an invalid set with Common Set, a close match, or a set
from another environment. Return the exact mismatch and ask the user to confirm
Common Set or supply one different exact set before continuing.

## Sample User Input

The user may provide plain text, YAML, a Markdown table, CSV, or a spreadsheet.
This synthetic YAML example shows the complete business input shape:

```yaml
operation: create
sales_method:
  name: Enterprise Opportunity Method
  description: Synthetic example for review
  set_selection_decision: confirm_common_set_or_specify_different_set
  set_id_or_code: required_when_not_using_common_set
  close_window_days: 90
  sales_motion: Redwood
stages:
  - name: Prospecting
    description: Initial account and opportunity discovery
    status: Open
    order: 1
    quota_factor: 0.10
    disabled: false
    win_probability: 10
    PhaseCd: QUALIFICATION-DISCOVERY
    duration_days: not_applicable
    additional_required_fields: none
  - name: Qualification
    description: Confirm need, authority, timing, and budget
    status: Open
    order: 2
    quota_factor: 0.25
    disabled: false
    win_probability: 25
    PhaseCd: QUALIFICATION-DISCOVERY
    duration_days: not_applicable
    additional_required_fields: none
  - name: Solution
    description: Validate the proposed solution
    status: Open
    order: 3
    quota_factor: 0.50
    disabled: false
    win_probability: 50
    PhaseCd: WORKING-DEAL
    duration_days: not_applicable
    additional_required_fields: none
  - name: Negotiation
    description: Finalize commercials and terms
    status: Open
    order: 4
    quota_factor: 0.75
    disabled: false
    win_probability: 75
    PhaseCd: CLOSING
    duration_days: not_applicable
    additional_required_fields: none
  - name: Closed Won
    description: Opportunity completed successfully
    status: Won
    order: 5
    quota_factor: 1.00
    disabled: false
    win_probability: 100
    PhaseCd: CLOSING
    duration_days: not_applicable
    additional_required_fields: none
  - name: Closed Lost
    description: Opportunity closed without a sale
    status: Lost
    order: 6
    quota_factor: 0.00
    disabled: false
    win_probability: 0
    PhaseCd: LOST-DEAL
    duration_days: not_applicable
    additional_required_fields: none
  - name: Closed No Sale
    description: Opportunity ended without a sales decision
    status: No Sale
    order: 7
    quota_factor: 0.00
    disabled: false
    win_probability: 0
    PhaseCd: CLOSING
    duration_days: not_applicable
    additional_required_fields: none
```

`PhaseCd` is required for every sales-stage row that will be written to
`MOO_SALES_STAGE.csv`, for both Redwood and Classic sales motions. Do not infer
that `PhaseCd` may be blank because the business Phase field is not applicable
or visible in Redwood. Preserve an exact target-baseline value when one exists;
otherwise use a user-approved value from the review profile. Use
`sales_motion: Classic` when Classic Sales is intended and then also supply or
review `duration_days`. For Redwood Sales, only `duration_days` is
`not_applicable`; never omit `PhaseCd` from the review or package.

## Review Output

The review must include:

- operation and exact target identity;
- sales-method name, description, set, close window, and sales motion;
- every stage field shown in the sample;
- provenance for each value: `user supplied`, `current baseline`, `documented default`, or `assumed for review`;
- design warnings and blockers;
- one explicit question asking the user to approve the proposal or provide corrections.

## Import Validation

Build the import ZIP from a fresh, same-target task CSV export. Preserve the
exported `ASM_SETUP_CSV_METADATA.xml` unchanged, including its complete
business-object metadata and migration-object graph. Preserve the complete
exported member list, exact file names, and CSV headers; keep unused child CSV
members header-only after removing unrelated rows. Do not hand-author,
minimize, or replace the metadata XML, and do not submit a ZIP that omits an
exported task member. The metadata graph is the FSM import contract that maps
`MOO_SALES_METHOD.csv` and `MOO_SALES_STAGE.csv` to their business objects.

Before handing the immutable package to Core Data Loader, inspect every row in
`MOO_SALES_STAGE.csv`. `PhaseCd` must be present and nonblank on every stage
row. Each create-stage row must also have a nonblank `StageNumber`, and the
`StageNumber` values must be unique within the package. Missing or duplicate
values are package-validation blockers: show the source file, stage name or row
identifier, and invalid field; do not hand off the package until it is corrected
and revalidated.

Before Core Data Loader handoff, record the exact target environment, fixed
`TaskCode` and `TaskName`, ZIP path, reopened SHA-256, package member list, CSV
headers, method row, all stage rows, reviewed delta, current-state lock and
unrelated-row preservation, and validation result. Confirm that the metadata
XML retains the same-target export's complete object graph, contains exactly
one `ObjectShortName` equal to
`MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES`, and that every exported member is
present with its exact header. Before every Core Data Loader handoff, require a
persisted project `TaskContextPath`, exact `TaskName`, and positive
`TaskSequence`; resolve that entry and require it to select this exact skill
path, `TaskCode`, `TaskName`, offering, and functional area. Missing or
mismatched task context is a blocker and must not be hand-authored or
synthesized. Treat a missing object graph,
absent member, changed header, hand-authored metadata, stale or cross-target
baseline, incomplete state lock, or hash mismatch as a package-validation
blocker. This child skill validates and hands off only; it does not build or
approve the upload preview. Core Data Loader must bind Task Hook validation to
the unchanged archive, create the immutable upload preview, and wait for the
user's later standalone `approve` before upload or initiation.

Accepted Data Loader initiation is terminal for that request. Retrieve status
and ProcessLog and perform read-only verification of the method and requested
stages only after a later explicit status or results request. FSM
object-category totals alone do not demonstrate that every stage row succeeded.

## Failure Summary

If any step fails, give the user a detailed, sanitized summary containing the
exact environment, task code and name, operation, failed workflow stage,
failure classification, package path and SHA-256 when applicable, process ID,
request or ESS ID, last status, elapsed wait, object and row counts, affected
CSV file and object, stage or entity identifier, message code and text,
available ProcessLog or status artifacts, partial successes, whether Fusion may
have changed, retry status, corrective action, and one safe next step. If a
value is unavailable, state that it was unavailable rather than omitting the
field silently. Never automatically retry a live import after failure or an
uncertain outcome.

## Oracle Resource Read Order

1. [ora_input_validation.md](ora-resource/ora_input_validation.md)
2. [ora_defaulting_rules.md](ora-resource/ora_defaulting_rules.md)
3. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
4. [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
5. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
6. [ora_error_handling.md](ora-resource/ora_error_handling.md)
7. [ora_rule_registry.json](ora-resource/ora_rule_registry.json) for the compiled task-node graph

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `set_selection_decision`: explicit confirmation to use Common Set or to use
  a different set
- `reference_data_set_identity`: exact Set ID or Set Code when a different set
  is selected, or a documented business-unit/organization selector that
  resolves to one exact set

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
