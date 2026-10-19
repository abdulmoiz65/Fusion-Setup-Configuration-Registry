---
skill_id: "hcm.workforce-time-management.time-and-labor-rules.time-rule-templates"
name: "Time Rule Templates Setup Task Guidance"
description: "Provides task-specific setup guidance for Time Rule Templates under the Time and Labor Rules functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Rules"
functional_area_code: "ORA_TIME_AND_LABOR_RULES"
task_code: "ORA_HWM_MANAGE_RULE_TEMPLATES"
task_name: "Time Rule Templates"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/time-rule-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/time-rule-templates/current/"
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

# Time Rule Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Time Rule Templates` under `Time and Labor Rules`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_MANAGE_RULE_TEMPLATES`
- task_name: `Time Rule Templates`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Time Rule Templates` under `Time and Labor Rules`.

## Setup Task Metadata

- Task name: `Time Rule Templates`
- Task code: `ORA_HWM_MANAGE_RULE_TEMPLATES`
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

## Common Applications Provider Contract

For a lookup-dependent proposal, route the read-only check through
`hcm.workforce-time-management.time-and-labor-common.manage-common-lookups`.
For a value-set-dependent proposal, route the read-only check through
`hcm.workforce-time-management.time-and-labor-common.manage-value-sets`.
These pillar skills delegate to the available Common Applications provider
skills. Supply the exact applicable `lookupType` or `ValueSetCode` resolved
from authorized product or current-environment evidence. `Time & Labor
Lookups`, `Workforce Management Lookups`, `Manage Common Lookups`, `Time and
Labor Value Sets`, and `Manage Value Sets` are scope labels, not API
identifiers. Do not pass them as identifiers or invoke an unrelated provider
when the proposal has no such dependency.

Retain provider evidence, compare the current provider state with the
product-recommended state, and show the comparison before a proposal. Do not
implement lookup or value-set CRUD in this skill. Apply a dependent
configuration change only when it is required by the implementation outcome
and explicitly confirmed by the user. If an applicable exact identifier
cannot be resolved, record the missing-input gap before the dependent proposal.

Use this task metadata when invoking those skills:

- Offering: `Time and Labor`
- Functional area / Setup Object: `Time and Labor Rules`
- Setup task name: `Time Rule Templates`
- Setup task code: `ORA_HWM_MANAGE_RULE_TEMPLATES`

## FSM Package Preparation

For a Time Rule Template create or update, treat the prepared CSV ZIP as an
FSM setup-data import. After the required fresh Time Rule Templates export,
prepare a minimal package using its current object headers and unchanged
metadata. For a create, generate the parent, input, usage, and applicable
translation rows from normalized intent. For an update, use the verified
current template graph and explicit before-and-after change set to retain
unchanged fields. Never copy an existing template record as a create template.

Before the Data Loader preview, validate the package against the fresh export
and the task rules: permitted members, exact headers and metadata, UTF-8
without a BOM, parsed row widths, unique parent names, and parent-child links.
Preserve explicit blank strings, `0`, and `#null` in supported fields. Reject
unknown fields and unresolved or orphan child rows. Validate the immutable ZIP
through `core.data-loader` and bind that ZIP to its approval preview.

Before requesting approval, display a clickable link to the exact validated
FSM ZIP outside the business proposal. Any package change requires a rebuild,
revalidation, and a new link.

## Business-only Approval Summary

After the package has passed validation and before displaying its link or
requesting approval, generate one business-only `Complete Summary` and
`Defaults Applied` section. The summary must contain every verified
user-provided business value and every default actually applied, using only
business labels and populated child sections. Omit blank, null, unused, and
metadata-only values. Do not include CSV fields, identifiers, archive paths,
hashes, diagnostics, or other technical details; the ZIP link remains outside
the summary as its own approval artifact.


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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-rules` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
