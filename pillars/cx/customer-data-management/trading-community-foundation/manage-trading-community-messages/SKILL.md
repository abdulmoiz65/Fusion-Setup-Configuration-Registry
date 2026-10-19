---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-trading-community-messages"
name: "Manage Trading Community Messages Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Trading Community Messages under the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "ORA_HZ_MANAGE_MESSAGES"
task_name: "Manage Trading Community Messages"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
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
  - "shared.common.manual-tasks"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-trading-community-messages/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-trading-community-messages/current/"
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

# Manage Trading Community Messages Setup Task Guidance

## Purpose

Provide a task-specific entry point for `Manage Trading Community Messages`
under `Trading Community Foundation`, then delegate the manual execution
workflow to `shared.common.manual-tasks`.

## Setup Task Skill Contract

- task_code: `ORA_HZ_MANAGE_MESSAGES`
- task_name: `Manage Trading Community Messages`
- parent_skill_id: `cx.customer-data-management.trading-community-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Trading Community Foundation`
- functional_area_code: `ORA_HZ_CDM_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when a user wants to create, modify, delete, translate, or
validate a Trading Community message or its tokens.

## Setup Task Metadata

- Task name: `Manage Trading Community Messages`
- Task code: `ORA_HZ_MANAGE_MESSAGES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST` (inactive generator compatibility metadata)
- Business Object: ``

## Execution Route

Invoke `shared.common.manual-tasks` with:

- `manual_task_name=Manage Trading Community Messages`
- the user's exact `approved_configuration_change`
- the exact `target_environment`

This authored body route is the task's operative dependency. The generated
frontmatter remains catalog-owned so a later `pillar-skill-gen` refresh
preserves this guidance instead of creating a competing generated route.

The shared skill must tell the user how to perform the approved change manually
in Fusion. It must not open Fusion or perform the change on the user's behalf.

## Automation Boundary

`CSVExportImportSupportedFlag` is `N`. The generated
`dataloader_import_mode: REST` value is non-operative compatibility metadata:
there is no registered `businessObject`, and it does not authorize a REST
call.

Do not route this task through:

- `core.data-loader`
- task-level FSM CSV export or import
- UCM, ESS, HDL, FBDI, CX Import, or spreadsheet loaders
- public, private, or inferred REST or SOAP endpoints
- browser automation or direct UI control

Do not reinterpret `ExportImportSupportedFlag=Y` as proof of an executable
route. No export or import workflow is selected for this skill.

## Manual Message Guidance

Use Oracle's current **Manage Messages** behavior as the field-level guide after
the user opens **Manage Trading Community Messages** through Setup and
Maintenance:

1. Search for the exact existing message, or create a message only when that is
   the approved change.
2. For a new message, use a unique message name and the application/module
   appropriate to the approved Trading Community requirement.
3. For predefined messages, do not change the predefined message number.
4. Preserve seeded messages unless the approved design and documented task
   behavior allow the change. Do not delete a predefined message merely because
   it appears unused.
5. Save the change manually.

Oracle references:

- [Messages](https://docs.oracle.com/en/cloud/saas/sales/oasal/messages.html)
- [Create and Edit Messages](https://docs.oracle.com/en/cloud/saas/applications-common/25d/facia/create-and-edit-messages.html)

## Tokens

When the approved message requires runtime values:

1. Define the token while editing the message.
2. Use a unique uppercase name inside curly braces, with underscores between
   words and no spaces, for example `{PARTY_NUMBER}`.
3. Select the documented token data type: `Text`, `Number`, or `Date`.
4. Add a description explaining the runtime value.
5. Do not edit or delete predefined tokens.
6. Validate that the calling Trading Community flow supplies the value; creating
   a token definition alone does not bind application code to it.

Oracle reference:
[Use of Tokens in Messages](https://docs.oracle.com/en/cloud/saas/procurement/26a/oapro/use-of-tokens-in-messages.html).

## Translations

Use the Translation Editor exposed by the manual message page for enabled
languages. Preserve the intended meaning, tokens, cause, and user action in
each translation. Do not claim translation completion until the user verifies
the applicable language behavior.

## Manual Verification

After the user reports saving the change:

1. Ask for the message identifier or description and the target environment.
2. Have the user reopen the message and confirm the saved fields and tokens.
3. Have the user trigger the relevant Trading Community validation with safe
   test data and verify the rendered text and dynamic values.
4. Check that no unintended validation behavior changed.
5. Report `manual verification pending` until the user confirms the readback
   or runtime result. Never report automated execution success.


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

Use the parent functional-area skill
`cx.customer-data-management.trading-community-foundation` for functional-area
sequencing. Use `shared.common.manual-tasks` for execution guidance. Track
token usage for any generated project artifact or skill-run record using the
manifest policy.
