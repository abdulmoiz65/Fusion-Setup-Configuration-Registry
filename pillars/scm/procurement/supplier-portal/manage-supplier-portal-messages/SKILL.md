---
skill_id: "scm.procurement.supplier-portal.manage-supplier-portal-messages"
name: "Manage Supplier Portal Messages Setup Task Guidance"
description: "Provides manual guidance for Manage Supplier Portal Messages under the Supplier Portal functional area; no automated export or import."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Supplier Portal"
functional_area_code: "PO_SUP_PORTAL_DEPLOYED"
task_code: "ORA_POZ_MANAGE_SUPPLIER_PORTAL_MESSAGES"
task_name: "Manage Supplier Portal Messages"
parent_skill_id: "scm.procurement.supplier-portal"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "N"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/supplier-portal/manage-supplier-portal-messages/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/supplier-portal/manage-supplier-portal-messages/current/"
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

# Manage Supplier Portal Messages Setup Task Guidance

**Manual task — guidance only.** State this up front. The user makes approved
changes in Fusion; no automated export/import, API calls, or browser actions.
Catalog flags and generated loader metadata do not authorize automation.

## Purpose

Provides task-specific manual setup planning, routing, and validation guidance for `Manage Supplier Portal Messages` under `Supplier Portal`.

## Setup Task Skill Contract

- task_code: `ORA_POZ_MANAGE_SUPPLIER_PORTAL_MESSAGES`
- task_name: `Manage Supplier Portal Messages`
- parent_skill_id: `scm.procurement.supplier-portal`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Supplier Portal`
- functional_area_code: `PO_SUP_PORTAL_DEPLOYED`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `N`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, or validating the approved manual change for `Manage Supplier Portal Messages` under `Supplier Portal`.

## Setup Task Metadata

- Task name: `Manage Supplier Portal Messages`
- Task code: `ORA_POZ_MANAGE_SUPPLIER_PORTAL_MESSAGES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`

## Applications Core Messages Routing

Use `shared.common.manual-tasks` with the approved change, target environment,
and [Manage Applications Core Messages](../../../../../shared/common/manual-tasks/manage-applications-core-messages.md)
guidance. That shared skill owns the manual workflow.

Give navigation, task-specific steps, and validation directly. Reuse supplied
context; clarify only an ambiguous task or scope. Do not request configuration
values, credentials, or completion confirmation in chat. The implementer obtains
missing approved values from the administrator and enters them in Fusion.
Do not invent defaults or create separate guides to repeat these steps.

To access this task, open **Navigator** > **Setup and Maintenance** >
**Setup: Procurement** > **Supplier Portal**, set **Show** to **All Tasks**, and
open **Manage Supplier Portal Messages**, or search for that exact name.
Use Applications Core Messages guidance without substituting another task.

The implementer must manually review and edit only the approved Supplier
Portal message. Capture the message identifier or description changed and the
validation outcome as implementation evidence. Do not use Data Loader, FSM,
or a direct REST route for this task.

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
