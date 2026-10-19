---
skill_id: "scm.product-management.items.manage-attachment-categories-for-product-management"
name: "Manage Attachment Categories for Product Management Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Attachment Categories for Product Management under the Items functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "ORA_EGP_MANAGE_ATTACH_CAT_FOR_PIM"
task_name: "Manage Attachment Categories for Product Management"
parent_skill_id: "scm.product-management.items"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
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
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-attachment-categories-for-product-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-attachment-categories-for-product-management/current/"
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
  - "May delegate a read-only task-level CSV baseline export, which writes an export artifact under the selected project workspace."
required_privileges:
  - "Fusion privileges required by the selected task-level export workflow for a new category preflight"
---

# Manage Attachment Categories for Product Management Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Attachment Categories for Product Management` under `Items`.

## Setup Task Skill Contract

- task_code: `ORA_EGP_MANAGE_ATTACH_CAT_FOR_PIM`
- task_name: `Manage Attachment Categories for Product Management`
- parent_skill_id: `scm.product-management.items`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Items`
- functional_area_code: `ORA_EGP_FA_ITEMS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Attachment Categories for Product Management` under `Items`.

## Setup Task Metadata

- Task name: `Manage Attachment Categories for Product Management`
- Task code: `ORA_EGP_MANAGE_ATTACH_CAT_FOR_PIM`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Route attachment-category setup through `core.fusion-api.apps-common`, which selects its `attachments` nested skill.
2. Export setup task data with `shared.setup-export.task-level-export`.
3. Validate setup task data with `shared.validation.setup-data-validator`.
4. Validate reference data with `shared.validation.reference-data-validator`.
5. Import setup task data with `core.data-loader` through the approved FSM CSV import workflow.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Attachment Categories for Product Management`
- Setup task code: `ORA_EGP_MANAGE_ATTACH_CAT_FOR_PIM`

## Apps Common Attachment Routing

Route attachment-category requests for this task through
`core.fusion-api.apps-common`. It selects the `attachments` nested skill, which
owns attachment-category task-family routing and preserves the declared
task-level export and approved FSM CSV import boundaries.

Do not select a direct Fusion endpoint or substitute another transport route
from this task skill. Before an import, follow the selected workflow's target,
artifact, and approval requirements.

## New Category Preflight

Before running the task-local validation nodes for a **new** attachment
category, require `Category Name`. If it is missing, return a structured
`input_validation` failure identifying that field and stop.

Route through `core.fusion-api.apps-common.attachments` and
`shared.setup-export.task-level-export` to obtain a fresh, complete CSV setup
data baseline for `ORA_EGP_MANAGE_ATTACH_CAT_FOR_PIM`. Apply the selected export
workflow's task identity, support-flag, environment, privilege, process-status,
and artifact checks. Do not use an attachment REST endpoint for this check.
Read every category row in `FND_APP_ATTACHMENT_CATEGORY.csv` and
`ORA_FND_APP_ATTACHMENT_CATEGORY.csv` from that baseline and compare
`CategoryName` exactly to the supplied `Category Name`, independent of
`EntityName`. Never use a partial baseline, fuzzy match, or first-row match.

- One or more exact matches: return a structured duplicate-category failure
  identifying `Category Name` and stop. Do not convert the create request to
  an update.
- No exact matches in a complete baseline: record the export artifact reference
  and zero-match result, then start `VALIDATE_ATTACHMENT_CATEGORY_INPUTS`.
- Export failure, incomplete baseline, missing expected CSV member or
  `CategoryName` column, or ambiguous task identity: stop before validation,
  preview, package preparation, or import. Preserve a sanitized diagnostic and
  request a new baseline after the cause is fixed.

This preflight is owned by this task skill and runs before the local resource
graph. The resource graph does not perform or route the baseline export. On
resume, refresh the baseline before claiming the category name is available.

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

## Output and Validation Requirements

Represent the task identity in `setup_task_plan` using the existing
`schemas/setup-task.schema.json` contract. Record validation outcomes in
`validation_checkpoints` using `schemas/validation-result.schema.json`.
`setup_data_routing` is task-routing guidance: identify the selected export,
validation, and approved FSM CSV import skills from this document rather than
creating a task-local contract.

Store generated artifacts in the matching declared `configuration_blueprint`
or `validation_result` project location, then register and validate them
through the declared project-management and validation skills. Do not include
customer values in reusable guidance. A missing or invalid required value must
produce a structured failure with `status: failed`, an FSCR failure class,
error code, field identifier, and recommended action. For a new attachment
category, complete the New Category Preflight and stop on a duplicate or
incomplete baseline. Only after the name is available, default an omitted
Entity Name to `ITEM_ENTITY` and request user approval of that value before
preview or submission. Stop affected output generation or validation until
the required correction or approval is received; do not continue with a
partial success.

## Implementation Notes

Use the parent functional-area skill `scm.product-management.items` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
