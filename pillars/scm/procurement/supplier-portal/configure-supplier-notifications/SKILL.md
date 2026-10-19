---
skill_id: "scm.procurement.supplier-portal.configure-supplier-notifications"
name: "Configure Supplier Notifications Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Supplier Notifications under the Supplier Portal functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Supplier Portal"
functional_area_code: "PO_SUP_PORTAL_DEPLOYED"
task_code: "ORA_POZ_CONFIGURE_SUPPLIER_NOTIFICATIONS_FOR_PROFILE_MGMT"
task_name: "Configure Supplier Notifications"
parent_skill_id: "scm.procurement.supplier-portal"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "supplierOptions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/supplier-portal/configure-supplier-notifications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/supplier-portal/configure-supplier-notifications/current/"
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

# Configure Supplier Notifications Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Supplier Notifications` under `Supplier Portal`.

## Setup Task Skill Contract

- task_code: `ORA_POZ_CONFIGURE_SUPPLIER_NOTIFICATIONS_FOR_PROFILE_MGMT`
- task_name: `Configure Supplier Notifications`
- parent_skill_id: `scm.procurement.supplier-portal`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Supplier Portal`
- functional_area_code: `PO_SUP_PORTAL_DEPLOYED`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `supplierOptions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Supplier Notifications` under `Supplier Portal`.

## Setup Task Metadata

- Task name: `Configure Supplier Notifications`
- Task code: `ORA_POZ_CONFIGURE_SUPPLIER_NOTIFICATIONS_FOR_PROFILE_MGMT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `supplierOptions`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `supplierOptions` as the Business Object.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Supplier Portal`
- Setup task name: `Configure Supplier Notifications`
- Setup task code: `ORA_POZ_CONFIGURE_SUPPLIER_NOTIFICATIONS_FOR_PROFILE_MGMT`

## Shared Business-Object Boundary

`Configure Supplier Notifications` shares the seeded `supplierOptions` row with
`Configure Supplier Registration` and `Configure Supplier Profile Change
Request`. Its setup-data artifact may update only
`NotifyPriorToExpirationDays` and `ReminderFrequencyDays`. It must not include
any registration or profile-change attribute, even when the current row was
read for validation.

Resolve exactly one current Supplier Options row, execute the three tasks
serially, and re-read the row after an earlier shared task succeeds. Preserve
all non-owned attributes unchanged in the Data Loader REST artifact.

Use `core.fusion-api.rest-api-client` for the read-only singleton lookup
declared in `ora-resource/ora_reference_lookups.md`. Do not use the client for
the mutation; `core.data-loader` remains the only import route.




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

Use the parent functional-area skill `scm.procurement.supplier-portal` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
