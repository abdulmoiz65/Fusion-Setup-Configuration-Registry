---
skill_id: "cx.subscriptions.integration-setup"
name: "Integration Setup Implementation Guidance"
description: "Provides CX Subscriptions implementation guidance for the Integration Setup functional area."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
type: "planning"
execution_mode: "assisted"
owner_team: "CX subscriptions pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "integration_setup_scope"
  - "integration_setup_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.fusion-api.rest-api-client"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS"
  - "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS"
  - "CUSTOM_MANAGE_ALGORITHMS_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS"
  - "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_REVENUE_RECOGNITION"
  - "CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_REVENUE_RECOGNITION"
  - "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_ACCOUNTS_RECEIVABLES"
  - "CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_ACCOUNTS_RECEIVABLES"
  - "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD"
  - "CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD"
  - "CUSTOM_MANAGE_ASSET_LIFECYCLE_MANAGEMENT_DEFAULTS"
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

# Integration Setup Implementation Guidance

## Purpose

Provides CX Subscriptions implementation guidance for the Integration Setup functional area.

## When to Use

Use this functional-area skill after Subscriptions scope is confirmed and the project needs integration setup setup planning, baseline export, import sequencing, or validation checkpoints.

## Execution Controls

This package is advisory until the setup task selects a read-only REST lookup or a
Data Loader route. Route all Fusion REST calls through
`core.fusion-api.rest-api-client`, source validation through
`shared.validation.setup-data-validator`, and workbook/archive generation, upload,
initiation, monitoring, and diagnostics through `core.data-loader`.

### Preflight Checks

Before a side effect, confirm the selected environment, required privileges,
registered business object, current live schema, source mapping, archive checksum,
Task Hook envelope, dependency lookups, and exact target. Present the immutable
archive and target environment, then obtain explicit approval immediately before
upload or initiation. Direct REST mutation and CSV task import are not execution
routes for this package, except the task-declared `PATCH` route for
`subscriptionAssetIntegrationDefaultValues`. That exception must use
`core.fusion-api.rest-api-client` and its task-level GET preflight, immutable
preview, and explicit-approval gates. Grouping-rule publishing is permitted only through the
approved `core.data-loader` route using
`subscriptionGroupingRuleSets_publishGroupingRuleSets`.

For a grouping-rule create that supplies an object display name, invoke the
task-declared metadata lookup exactly as
`{{baseUrl}}/crmRestApi/resources/latest/objectMetadata?q=objectProperties.PropertyCode='GroupingRuleGroupingCriteria'`.
Set `{{baseUrl}}` from the active Fusion connection and send
`REST-Framework-Version: 9`. Match the supplied display name exactly and use
the returned `RestResource` for the subsequent object-specific attribute
lookup; do not substitute the `intelligentCRM` metadata route or infer a
resource name.

### Diagnostics and Redaction

For input, catalog, authorization, transport, Fusion API, Data Loader process, or
artifact-persistence failures, stop and record the failure class, message,
recommended action, environment, artifact references, and available request or
process identifiers in the project workspace. Do not retry a failed or uncertain
upload or initiation without a newly validated archive and explicit approval.

Never print or persist credentials, access tokens, token caches, private keys,
tenant secrets, wallet files, full base64 payloads, or sensitive customer data in
skill output, diagnostics, or project artifacts.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Subscriptions` (`CUSTOM_SUBSCRIPTIONS`)
- Functional area / Setup Object: `Integration Setup` (`CUSTOM_INTEGRATION_SETUP`)

## Setup Tasks

1. [Manage Grouping Rules for Order Management to Subscriptions](manage-grouping-rules-for-order-management-to-subscriptions.md) (`CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS`)
2. [Manage Service Mappings for Order Management to Subscriptions](manage-service-mappings-for-order-management-to-subscriptions/SKILL.md) (`CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS`)
3. [Manage Algorithms for Order Management to Subscriptions](manage-algorithms-for-order-management-to-subscriptions/SKILL.md) (`CUSTOM_MANAGE_ALGORITHMS_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS`)
4. [Manage Service Mappings for Subscriptions to Revenue Recognition](manage-service-mappings-for-subscriptions-to-revenue-recognition/SKILL.md) (`CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_REVENUE_RECOGNITION`)
5. [Manage Algorithms for Subscriptions to Revenue Recognition](manage-algorithms-for-subscriptions-to-revenue-recognition/SKILL.md) (`CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_REVENUE_RECOGNITION`)
6. [Manage Service Mappings for Subscriptions to Accounts Receivables](manage-service-mappings-for-subscriptions-to-accounts-receivables/SKILL.md) (`CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_ACCOUNTS_RECEIVABLES`)
7. [Manage Algorithms for Subscriptions to Accounts Receivables](manage-algorithms-for-subscriptions-to-accounts-receivables/SKILL.md) (`CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_ACCOUNTS_RECEIVABLES`)
8. [Manage Service Mappings for Subscriptions to Maintenance Cloud](manage-service-mappings-for-subscriptions-to-maintenance-cloud/SKILL.md) (`CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD`)
9. [Manage Algorithms for Subscriptions to Maintenance Cloud](manage-algorithms-for-subscriptions-to-maintenance-cloud/SKILL.md) (`CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD`)
10. [Manage Asset Lifecycle Management Defaults](manage-asset-lifecycle-management-defaults.md) (`CUSTOM_MANAGE_ASSET_LIFECYCLE_MANAGEMENT_DEFAULTS`)

## Inputs

- `implementation_objective`
- `project_context`
- `integration_setup_scope`
- `integration_setup_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
