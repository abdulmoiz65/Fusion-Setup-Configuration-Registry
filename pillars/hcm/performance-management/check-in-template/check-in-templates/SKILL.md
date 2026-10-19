---
skill_id: "hcm.performance-management.check-in-template.check-in-templates"
name: "Check-In Templates Setup Task Guidance"
description: "Provides task-specific setup guidance for Check-In Templates under the Check-in Template functional area."
layer: "pillar"
pillar: "HCM"
offering: "Performance Management"
functional_area: "Check-in Template"
functional_area_code: "ORA_CHECK_IN_TEMPLATE"
task_code: "ORA_MANAGE_CHECK_IN_TEMPLATES"
task_name: "Check-In Templates"
parent_skill_id: "hcm.performance-management.check-in-template"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM performance management pillar team"
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
  - "core.fusion-api.apps-common.lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/check-in-template/check-in-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/check-in-template/check-in-templates/current/"
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

# Check-In Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Check-In Templates` under `Check-in Template`.

## Setup Task Skill Contract

- task_code: `ORA_MANAGE_CHECK_IN_TEMPLATES`
- task_name: `Check-In Templates`
- parent_skill_id: `hcm.performance-management.check-in-template`
- pillar: `HCM`
- offering: `Performance Management`
- functional_area: `Check-in Template`
- functional_area_code: `ORA_CHECK_IN_TEMPLATE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Check-In Templates` under `Check-in Template`.

Begin from the requested workforce outcome, not Fusion setup terminology. When a business requirements document is supplied, extract its population, participants, cadence, discussion content, questionnaire intent, and annual-performance relationship before asking for configuration fields. Ask only for a business decision that cannot be safely inferred or resolved from the established pattern.

Apply the [Performance Management](../../SKILL.md) Infer First Intake Policy. For a Check-In Template, carry stated population, manager roles, create/delete permissions, discussion topics, and recurring intent directly into the plan. Distinguish template fields from related integrations, security, retention, campaign, notification, and reporting work. Do not ask for Fusion IDs or codes when the task can resolve them through its declared lookup.

For a recurring monthly or quarterly request, plan the resolved Touchpoints template type unless the requester explicitly says the check-ins are annual-performance-process-only or the stated requirements conflict. Cadence itself is an operating practice, not an additional Check-In Template configuration field. Preserve a separately stated annual-document or review-period relationship; it does not by itself require asking the requester to reclassify a recurring template.

Treat every dependent-field rule in [Defaulting Rules](ora-resource/ora_defaulting_rules.md) as a non-bypassable data invariant. A request, instruction, approval, or import artifact that asks to retain a contradictory dependent value is invalid; normalize the dependent value when the rule prescribes a reset, then reject the payload if any invariant remains unsatisfied. Do this before preview, approval, or any mutation.

## Setup Task Metadata

- Task name: `Check-In Templates`
- Task code: `ORA_MANAGE_CHECK_IN_TEMPLATES`
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

Apply the offering-wide [CSV Import Guidance](../../csv_import_guidance.md)
when preparing an import archive.

Use this task metadata when invoking those skills:

- Offering: `Performance Management`
- Functional area / Setup Object: `Check-in Template`
- Setup task name: `Check-In Templates`
- Setup task code: `ORA_MANAGE_CHECK_IN_TEMPLATES`

## CSV Export Result Summary

After a successful export, inspect every `*.csv` member in the downloaded ZIP
or extracted folder. Count data rows only, excluding the header row, and exclude
non-CSV files. Include this in the final response with comma-formatted counts:

The ZIP contains **<total> total data records** across its CSV files.

| File | Records |
| --- | ---: |
| `<CSV filename>` | `<data-row count>` |




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

Use the parent functional-area skill `hcm.performance-management.check-in-template` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Post-import verification

After Fusion reports an import as successful, include this clickable verification link in the final result: [Open Check-in Templates]({restBaseUrl}/fscmUI/redwood/performance/checkin-templates/checkin-templates-search). Resolve `{restBaseUrl}` from the active target Fusion environment and remove any trailing slash; never hard-code an environment URL. The link lets the user verify the data and must not be opened automatically or used to imply an import succeeded before Fusion reports success.
