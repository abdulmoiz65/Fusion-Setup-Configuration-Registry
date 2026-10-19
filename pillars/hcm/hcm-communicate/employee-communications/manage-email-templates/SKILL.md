---
skill_id: "hcm.hcm-communicate.employee-communications.manage-email-templates"
name: "Manage Email Templates Setup Task Guidance"
description: "Provides task-specific setup guidance and controlled FSM creation and status-transition routing for Campaign Communication Templates under the Employee Communications functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Communicate"
functional_area: "Employee Communications"
functional_area_code: "ORA_IRC_EMPLOYEE_CAMPAIGNS"
task_code: "ORA_IRC_DESIGN_EMP_CAMPAIGN_EMAIL_TEMPLATES"
task_name: "Manage Email Templates"
parent_skill_id: "hcm.hcm-communicate.employee-communications"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM hcm communicate pillar team"
version: "0.3.9"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "lifecycle_action"
  - "target_template_evidence"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "lifecycle_change_preview"
  - "status_verification"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-email-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-email-templates/current/"
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
  - "May prepare one FSM import archive that creates Campaign Communication Templates and/or changes only DesignStatusCode for one or more exact existing Campaign Communication Templates; Core Data Loader owns its mandatory execution gate."
required_privileges:
  - "Fusion privileges to create and retrieve Manage Email Templates FSM imports and exports."
---

# Manage Email Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Email Templates` under `Employee Communications`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_DESIGN_EMP_CAMPAIGN_EMAIL_TEMPLATES`
- task_name: `Manage Email Templates`
- parent_skill_id: `hcm.hcm-communicate.employee-communications`
- pillar: `HCM`
- offering: `HCM Communicate`
- functional_area: `Employee Communications`
- functional_area_code: `ORA_IRC_EMPLOYEE_CAMPAIGNS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Email Templates` under `Employee Communications`.

## Setup Task Metadata

- Task name: `Manage Email Templates`
- Task code: `ORA_IRC_DESIGN_EMP_CAMPAIGN_EMAIL_TEMPLATES`
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

Use the FSM import route to create a new **Campaign Communication Template**
or to make controlled status transitions for one or more existing Campaign templates,
only after the task-local archive, parent/dependent relationships, editor/type
baseline, target environment, and the core Data Loader execution gate have passed the
`ora-resource/` gates. Do not use the Template UI to create the template as
part of this automated route. Express and Survey templates remain outside the
supported FSM import scope.

For status transitions, require a fresh task-level export that identifies every
requested Campaign template and its current `DesignStatusCode`. Build the
candidate with `scripts/build_status_transition_archive.py` from that archive,
retain every archive member and every field unchanged except each selected
template's `DesignStatusCode`, and allow only
`ORA_ACTIVE` or `ORA_INACTIVE` as each new value. Each selected
`MessageDesignCode` must identify exactly one target row. Route the immutable
candidate through
`core.data-loader` and its Task Hook workflow. The task does not collect a
separate confirmation. One immutable archive covers every status transition
and new-template row it contains. Do not retry a status import. After
submission, this task polls the returned request through the Data Loader
status helper until it reaches a terminal result. After terminal import
success, obtain a fresh task-level
export to verify every selected
`MessageDesignCode` and resulting status.

For standard Campaign-template creation, use the hardcoded Campaign editor
defaults in `ora-resource/ora_defaulting_rules.md`: Basic and Advanced Block
use the declared minimal layout JSON; HTML uses blank `DesignMetadata` with
`MessageLanguage` `US` and `DefaultLanguageFlag` `Y`. Do not use
Agent-specific metadata as the general Advanced Block Editor default. A fresh
preflight export is required only once per immutable candidate for target
`DesignName` and `MessageDesignCode` conflict comparison, status transitions,
post-import verification, and cross-environment archive handling. Reuse that
same preflight export for both creation conflict checks; do not re-export solely
to generate or retry a `MessageDesignCode`;
do not compare a target template's editor metadata with these creation defaults.

## Post-Import Content Design Handoff

After a Campaign template is successfully created through FSM import, or a
Campaign template FSM archive is successfully imported, first report the
terminal import result and the fresh verification evidence. Then explicitly ask
the requester to open Fusion **Setup and Maintenance → HCM Communicate →
Employee Communications → Manage Email Templates**, select the template, and
review and design its email content. Content design is manual Fusion UI work;
do not alter the imported archive or attempt UI automation as part of this
workflow.

## Creation Request Intake

When a requester asks to create an HCM Communicate email template and has not
provided the needed business choices, ask exactly:

To create an HCM Communicate email template, please provide:

**Required**

- **Template name**
- **Email Editor:** Basic, Advanced Block, or HTML
- **Template Type:** Campaign Communication Template

**Optional**

- **Description**

Do not ask the requester for, display, or explain `MessageDesignCode` during
this intake. For a standard Campaign-template creation, generate it internally
using the declared 32-character rule in `ora-resource/ora_defaulting_rules.md`.
run `scripts/generate_message_design_code.py` against the same target FSM
export already obtained for the visible-name conflict check, and reuse the resulting value in each linked
archive row. Do not offer Express Communication Template or Survey
Template: they are unsupported by the FSM import route and require a manual
Fusion UI handoff.

When a requester explicitly asks to create an Express Communication Template
or Survey Template, respond that FSM import does not support that template
type and direct them to create it in the **Manage Email Templates** Fusion UI.
Do not generate an FSM archive, infer template codes or metadata, or offer an
FSM execution preview for that request.

## Template Listing Scope

When listing email templates from an FSM export, explicitly state that the
list contains **Campaign Communication Templates only**. For Express
Communication Templates or Survey Templates, direct the requester to Fusion
**Setup and Maintenance → HCM Communicate → Employee Communications → Manage
Email Templates**, then to the **Templates** page. Do not claim an FSM export
is a complete inventory of those template types.

## Cross-Environment FSM Import

Support importing a `Manage Email Templates` FSM ZIP exported from another
Fusion environment. Preserve the original source ZIP as evidence and obtain one
fresh target-environment export for name/key comparison. When a source parent
has a target `DesignName` or `MessageDesignCode` conflict, present the exact
conflicts and require the requester to select **Import only new templates** or
**Replace existing templates** before building the immutable execution
candidate. Do not silently replace, skip, or rename a template.

For **Import only new templates**, run
`scripts/filter_new_campaign_templates.py` to build a derived ZIP that retains
only source parents whose name and key are both absent from the target and only
their linked metadata/type rows; preserve every other source member unchanged.
For **Replace existing templates**, use an immutable verified copy of the
source ZIP without regenerating, renaming, or dropping its linked rows. If no
source templates remain after a new-only filter, report that there is nothing
to import.

Accept any supplied document format as read-only analysis input. Extract only
source-backed template facts, identify missing parent, metadata, type, or FSM
archive information, and report them without guessing a mapping. A document is
never itself import-eligible unless it is already a valid task-level FSM ZIP or
has been transformed into one through a separately validated mapping workflow.

Use this task metadata when invoking those skills:

- Offering: `HCM Communicate`
- Functional area / Setup Object: `Employee Communications`
- Setup task name: `Manage Email Templates`
- Setup task code: `ORA_IRC_DESIGN_EMP_CAMPAIGN_EMAIL_TEMPLATES`

## Source-Specific Scope and Boundaries

- Use `commonLookupsLOV` only for read-only lookup resolution needed by the
  template workflow. Route any common-lookup create, update, or delete request
  to the applicable Common Lookup skill; do not treat this task as the owner of
  the lookup UI or data.
- FSM export and import support the Campaign Communication Template route.
  The source runbook states that **Express Communication Template** and
  **Survey Template** are not supported by this FSM route. Do not infer an
  Express or Survey `DesignTypeCode`, `DesignEditorTypeCode`, or
  `DesignMetadata` baseline from Campaign export data.
- When a request includes Express or Survey template data, record the scope
  gap in the project diagnostic and provide a manual Fusion UI handoff. Do not
  use a Campaign export or import package to claim that those template types
  were migrated or validated.
- UI-only design editing, deletion, and send actions remain manual Fusion UI
  work. Activation and inactivation of an existing Campaign Communication
  Template are permitted only through the controlled FSM status-transition
  route described above; no other template field or archive member may change.
  Use a fresh task export for read-only evidence and post-import verification.

## Safety, Preflight, Failure, and Redaction

Before creating an archive, previewing an import, or submitting an FSM import,
run a preflight that confirms the target environment, task code, required
privileges, source ZIP shape, exact Campaign template identity, current
`DesignStatusCode`, permitted requested status, and the absence of target
name/key conflicts. Confirm whether the operation is read-only, preview, or
live; stop before any live action when the immutable core Data Loader execution gate
is absent.

On a preflight or execution failure, classify the result as `input_validation`,
`catalog_or_metadata_mismatch`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `execution_blocker`. Stop without
side effects for invalid input, unsupported template types, ambiguous template
identity, incomplete execution gate, or a nonrecoverable Fusion error. Record safe
diagnostics under the project workspace when applicable, including the stage,
failure class, a redacted message, target environment, artifact references,
and any ProcessId, requestId, or ECID. Do not retry a live import; after a
timeout or terminal process failure, report the last known status and require
fresh direction before another attempt.

Redact sensitive material from all output and durable diagnostics. Never print
or persist credentials, access tokens, cookies, token caches, private keys,
tenant secrets, full base64 content, or sensitive customer data. Retain only
the minimum archive, response, and diagnostic summaries needed to explain the
failure or verify the resulting status.




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

Use the parent functional-area skill `hcm.hcm-communicate.employee-communications` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
