---
skill_id: "scm.procurement.supplier-portal.manage-supplier-user-role-usages"
name: "Manage Supplier User Role Usages Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Supplier User Role Usages under the Supplier Portal functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Supplier Portal"
functional_area_code: "PO_SUP_PORTAL_DEPLOYED"
task_code: "POZ_MANAGE_SUPPLIER_USER_ROLE_USAGES"
task_name: "Manage Supplier User Role Usages"
parent_skill_id: "scm.procurement.supplier-portal"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "supplierUserRoles"
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
  - "scm.procurement.supplier-portal.manage-supplier-user-roles"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/supplier-portal/manage-supplier-user-role-usages/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/supplier-portal/manage-supplier-user-role-usages/current/"
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

# Manage Supplier User Role Usages Setup Task Guidance

## Purpose

Records the catalog identity for `Manage Supplier User Role Usages` under `Supplier Portal`.
This task intentionally shares its implementation guidance with `Manage Supplier
User Roles`; it does not define a second, diverging procedure.

## Setup Task Skill Contract

- task_code: `POZ_MANAGE_SUPPLIER_USER_ROLE_USAGES`
- task_name: `Manage Supplier User Role Usages`
- parent_skill_id: `scm.procurement.supplier-portal`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Supplier Portal`
- functional_area_code: `PO_SUP_PORTAL_DEPLOYED`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `supplierUserRoles` (inherited from Manage Supplier User Roles)
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Delegated Guidance

For planning, sequencing, export/import preparation, validation, and any
Data Loader work, follow [Manage Supplier User Roles](../manage-supplier-user-roles/SKILL.md).

This task inherits that skill's `supplierUserRoles` Data Loader REST route; its
own catalog code distinguishes the task record but does not authorize a second
payload, workflow, or mutation path.

Apply the same controls and artifacts, while recording this task's own catalog
code, `POZ_MANAGE_SUPPLIER_USER_ROLE_USAGES`, in the task sequence and any
resulting project records. Do not create a separate payload, workflow, or
resource set unless the two tasks later require different Oracle guidance.
