---
task_code: "ORA_SVC_MANAGE_MILESTONE_CONFIG"
task_name: "Manage Service Milestone Configuration"
parent_skill_id: "cx.service.service-entitlements"
pillar: "CX"
offering: "Service"
functional_area: "Service Entitlements"
functional_area_code: "ORA_SVC_ENTITLEMENTS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
route_to: "core.data-loader"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Service Milestone Configuration

## Setup Task Metadata

- Task name: `Manage Service Milestone Configuration`
- Task code: `ORA_SVC_MANAGE_MILESTONE_CONFIG`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## Purpose

Manage Service Request milestone configurations, including their milestone and threshold result columns, business-unit scope, agent controls, time-zone source, and start, pause, and completion criteria.

## Use Cases

### Review Service Milestone Configuration

Review the current Service Request milestone configuration and its business-unit scope, controls, and criteria.

1. Export the Manage Service Milestone Configuration setup data with shared.setup-export.task-level-export.
2. Review the exported milestone code, threshold code, business-unit scope, milestone type, agent controls, time-zone source, and start, pause, and completion criteria.

### Create Service Milestone Configuration

Create a Service Request milestone configuration with the approved milestone and threshold result columns, business-unit scope, controls, and criteria.

1. Export the Manage Service Milestone Configuration setup data with shared.setup-export.task-level-export.
2. Use the completed export of the same setup task as the package baseline; preserve its package structure and modify only task-owned rows required for the approved change.
3. Provide the approved milestone code, object name, milestone type, and start, pause, and completion criteria; provide threshold code, business-unit scope, agent controls, and time-zone source when applicable.
4. Verify that the milestone and threshold result columns are configured in the matrix class and that the business-unit scope is valid.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the created milestone configuration with a fresh export.

### Update Service Milestone Configuration

Update an existing Service Request milestone configuration without changing its identity or unrelated configuration.

1. Export the Manage Service Milestone Configuration setup data with shared.setup-export.task-level-export.
2. Use the completed export of the same setup task as the package baseline; retain the selected milestone configuration identity and change only approved task-owned fields.
3. Provide the milestone configuration identity and approved changes to its label, criteria, threshold code, business-unit scope, agent controls, or time-zone source.
4. Verify that changed milestone and threshold result columns are configured in the matrix class and that the business-unit scope is valid.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the updated milestone configuration with a fresh export.

### Delete Service Milestone Configuration

Delete a Service Request milestone configuration.

1. Retrieve the approved temporary milestone configuration by MilestoneConfigId with core.fusion-api.rest-api-client.
2. Present the exact DELETE target and require explicit approval immediately before execution.
3. Delete the approved temporary milestone configuration through the documented Milestones REST DELETE operation.
4. Verify with a fresh read that the deleted MilestoneConfigId has DeletedFlag set to true.
5. Restore the retained temporary milestone configuration through the documented Milestones REST PATCH operation with DeletedFlag set to false.
6. Verify with a fresh read that the restored MilestoneConfigId has DeletedFlag set to false.

## Custom Execution

- `delete_service_milestone_configuration`: Route to `core.fusion-api.rest-api-client` with `DELETE /crmRestApi/resources/11.13.18.05/milestones/{MilestoneConfigId}`.
- `restore_deleted_service_milestone_configuration`: Route to `core.fusion-api.rest-api-client` with `PATCH /crmRestApi/resources/11.13.18.05/milestones/{MilestoneConfigId}` and `{"DeletedFlag": false}`.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Service Entitlements`
- Setup task name: `Manage Service Milestone Configuration`
- Setup task code: `ORA_SVC_MANAGE_MILESTONE_CONFIG`


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Service Milestone Configuration` under `Service Entitlements`.
