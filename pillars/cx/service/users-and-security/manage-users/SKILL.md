---
skill_id: "cx.service.users-and-security.manage-users"
name: "Manage Users Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Users under the Users and Security functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
task_code: "PER_MANAGE_USERS"
task_name: "Manage Users"
parent_skill_id: "cx.service.users-and-security"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "CXIMPORT"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/users-and-security/manage-users/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/users-and-security/manage-users/current/"
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
depends_on:
  - "cx.customer-data-management.resources.manage-resources"
---

# Manage Users Setup Task Guidance

## Purpose

Retain the CX Service Manage Users task identity while reusing all supported ResourceUser import, export, direct REST, membership, lifecycle, validation, and post-import use cases from CX Customer Data Management Manage Resources.
## Setup Task Skill Contract

- task_code: `PER_MANAGE_USERS`
- task_name: `Manage Users`
- parent_skill_id: `cx.service.users-and-security`
- pillar: `CX`
- offering: `Service`
- functional_area: `Users and Security`
- functional_area_code: `ORA_ASK_USERS_AND_SECURITY`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `CXIMPORT`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when a Service implementation objective is classified to `Manage
Users` under `Users and Security`. Retain the task identity and reuse all supported
ResourceUser operation use cases from
`cx.customer-data-management.resources.manage-resources`.

## Setup Task Metadata

- Task name: `Manage Users`
- Task code: `PER_MANAGE_USERS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `CXIMPORT`
- Business Object: ``




## Route To

Route to cx.customer-data-management.resources.manage-resources.
## Use Cases

### Resource User Import

Import one or more Resource Users through the CX Import workflow.

1. Route the ResourceUser source and import context unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's Data Loader preview, validation envelope, approval, initiation, and explicit status workflow.

### Resource User Import Status

Review the status, results, counts, or errors of an initiated ResourceUser import.

1. Route the data-load request identity and status request unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's Data Loader status workflow; do not infer import completion.

### Resource User Export

Export ResourceUser data through Export Management.

1. Route the export name, filter, selected columns, output settings, activation choice, and download request unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's export preview, approval, activation, polling, and download workflow.

### Resource User Get

Read one exact existing Resource User.

1. Route the exact ResourceEmail or server-returned ResourcePartyNumber unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's exact identity resolution and authorized read contract.

### Resource User Create

Create one Resource User through the documented direct REST workflow.

1. Route the explicit direct-REST create request and required inputs unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's reference validation, immutable preview, approval, create, and verification workflow.

### Resource User Update

Update one existing Resource User, including promotion, demotion, or transfer when supported by the source contract.

1. Route the exact identity and requested minimal changes unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's exact-item read, preview, approval, PATCH, and verification workflow.

### Resource User End Date

End-date one existing Resource User.

1. Route the exact identity and requested ResourceEndDate unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's lifecycle review, preview, approval, PATCH, and verification workflow.

### Direct Membership Add

Add an eligible Resource Organization membership for one Resource User.

1. Route the binding membership handoff unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's role, organization, hierarchy, preview, approval, PATCH, and verification workflow.

### Direct Membership Update

Update an eligible Resource Organization membership for one Resource User.

1. Route the binding membership handoff unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's role, organization, hierarchy, preview, approval, PATCH, and verification workflow.

### Direct Membership End Date

End-date an eligible Resource Organization membership for one Resource User.

1. Route the binding membership handoff unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's role, organization, hierarchy, preview, approval, PATCH, and verification workflow.

### Post Import Reporting Hierarchy Generation

Evaluate and route eligible Reporting Hierarchy Generation after a successful ResourceUser import.

1. Route the successful import evidence and hierarchy context unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's post-import eligibility, structured handoff, preview, and separately approved execution workflow.

### Post Import Send Pending Ldap Requests

Evaluate and route eligible Send Pending LDAP Requests processing after a successful ResourceUser import.

1. Route the successful import evidence and LDAP context unchanged to cx.customer-data-management.resources.manage-resources.
2. Use the receiving skill's post-import eligibility, preview, and separately approved execution workflow.

### Resource User Delete

Permanently delete a Resource User.

Not supported. Resource Users DELETE is unsupported. Route the caller to resource end-date or organization-membership end-date instead; do not send a DELETE request.
## Guard Rails

1. Do not duplicate the Customer Data Management Manage Resources use cases or its ora-resource contracts in the Service overlay.
2. Do not invoke core.data-loader, core.fusion-api.rest-api-client, or a Resource Users endpoint directly from Manage Users.
3. Pass the original objective, project context, source artifacts, exact identity, export settings, and approval context unchanged to the receiving skill.
4. Treat CX Import, Export Management, direct REST, post-import ESS, approval, retry, diagnostics, and verification behavior as owned by the receiving skill.
## ResourceUser Operation Handoff

`CSVExportImportSupportedFlag` is `N`, so this task is not an FSM CSV
export/import route. ResourceUser operations reuse the separate, existing CX
Customer Data Management `Manage Resources` workflow as the authoritative
source of behavior and its task-local `ora-resource/` contracts.

| Intent | Handoff target |
|---|---|
| ResourceUser CX Import, import preview, initiation, status, results, and errors | `cx.customer-data-management.resources.manage-resources` |
| ResourceUser Export Management creation, activation, polling, and download | `cx.customer-data-management.resources.manage-resources` |
| Eligible post-import Reporting Hierarchy Generation and Send Pending LDAP Requests routing | `cx.customer-data-management.resources.manage-resources` |
| One ResourceUser read, create, update, promotion, demotion, transfer, or end-date operation | `cx.customer-data-management.resources.manage-resources` |
| Direct organization-membership add, update, or end-date operation | `cx.customer-data-management.resources.manage-resources` |
| Resource role, organization, legal-entity, business-unit, person-type, and identity validation | `cx.customer-data-management.resources.manage-resources` |
| Unsupported permanent ResourceUser deletion | `cx.customer-data-management.resources.manage-resources` |

Pass the original implementation objective, project context, ResourceUser
operation, identity or source artifact, requested export settings, and approval
context unchanged. The receiving skill owns current and future supported
ResourceUser use cases, reference lookups, input and dependency validation,
Data Loader or REST route selection, immutable previews, approval gates,
diagnostics, and project execution records.

Do not invoke `core.data-loader`, `core.fusion-api.rest-api-client`, or a
Resource Users endpoint directly from this task. Do not duplicate the receiving
skill's ResourceUser contracts or infer an alternate route.

## Reused Resource Contracts

This Service overlay has no task-local `ora-resource/` package. Use the
authoritative resource contracts in
[`cx.customer-data-management.resources.manage-resources`](../../../customer-data-management/resources/manage-resources/SKILL.md),
including its complete `ora-resource/` package, for every routed operation.



## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `resource_management_handoff`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.service.users-and-security` for
functional-area sequencing and scope decisions. Track token usage for any
generated project artifact or skill-run record using the manifest policy.
