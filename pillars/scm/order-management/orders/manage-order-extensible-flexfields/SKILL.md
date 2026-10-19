---
skill_id: "scm.order-management.orders.manage-order-extensible-flexfields"
name: "Manage Order Extensible Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Order Extensible Flexfields under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "DOO_MANAGE_ORCHESTRATION_EXTENSIBLE_FLEXFIELDS"
task_name: "Manage Order Extensible Flexfields"
parent_skill_id: "scm.order-management.orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.1.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "flexfield_deployment_context"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "post_deployment_ess_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-order-extensible-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-order-extensible-flexfields/current/"
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

# Manage Order Extensible Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Order Extensible Flexfields` under `Orders`.

## Setup Task Skill Contract

- task_code: `DOO_MANAGE_ORCHESTRATION_EXTENSIBLE_FLEXFIELDS`
- task_name: `Manage Order Extensible Flexfields`
- parent_skill_id: `scm.order-management.orders`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Orders`
- functional_area_code: `ORA_DOO_ORDER_FULLFILLMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Order Extensible Flexfields` under `Orders`.

## Setup Task Metadata

- Task name: `Manage Order Extensible Flexfields`
- Task code: `DOO_MANAGE_ORCHESTRATION_EXTENSIBLE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Application Common Extensible Flexfield Routing

Route every request for this task through `core.fusion-api.apps-common`. That
core entry point must select
`core.fusion-api.apps-common.extensible-flexfields`; do not invoke a Fusion
REST client, Data Loader, export workflow, or browser workflow directly from
this task skill.

Use only these flexfield codes for this task:

- `DOO_FULFILL_LINES_ADD_INFO`
- `DOO_HEADERS_ADD_INFO`

Pass the exact flexfield code and task context to the core skill. The core EFF
workflow owns read-before-write checks, setup-data export and import routing,
deployment status, and the explicit approval gate immediately before a
mutating operation. Do not infer, substitute, or broaden the code list.

## Oracle Order Management EFF Guidelines

Apply these source-backed rules when designing or changing an Order Management
EFF:

1. Select the entity deliberately. `DOO_HEADERS_ADD_INFO` stores order-header
   data, and `DOO_FULFILL_LINES_ADD_INFO` stores order-line data. Header and
   line EFFs are independent even when they use the same context or segment
   names; use an Order Management extension when values must be dependent.
2. Use a context to group related attributes and add only the minimum number
   of contexts required, because each context can affect performance. Keep the
   context `TranslatableFlag` disabled.
3. Require every new context's display name and code to begin with a letter,
   use only letters, numbers, spaces, periods, commas, hyphens, underscores,
   double quotation marks, colons, or forward slashes, contain no consecutive
   spaces, and have no trailing space. Treat a nomenclature failure during
   publishing as `input_validation`.
4. For a new segment, use the same value for segment code and API name. Do not
   change an existing segment's API name; both the code and API name are
   immutable after creation. Require unique code, name, and description values
   for every segment.
5. Validate segment capacity before import. A context supports at most 20
   varchar attributes, 10 number attributes, 5 date attributes, 5 time
   attributes, and 40 segments in total. Validate the target table column,
   data type, value set, required flag, defaulting, and display sequence before
   building an archive.
6. For `DOO_FULFILL_LINES_ADD_INFO` (Fulfillment Line Information), when the
   requested change supplies more than five distinct contexts, advise that
   minimizing the number of contexts helps achieve optimal performance. Count
   distinct contexts by context code; do not count segments within a context or
   repeated page mappings. Present the guidance and wait for the
   user's explicit acknowledgment before building an archive or continuing to
   import, deploy, or publish the change. After acknowledgment, proceed with
   the normal capacity, duplicate, and approval checks; do not require an
   acknowledgment for five or fewer distinct contexts.
6. For a required segment, require either a supplied value or a default that
   can satisfy every required segment in its context. Otherwise Order
   Management can block draft creation or order submission. Do not assume a
   default context row is created when no required segment can be satisfied.
7. Do not delete a context as a replacement strategy. Revise the existing
   context or create a distinct one. If deletion is unavoidable, remove all
   references first, then deploy and publish; avoid modifying or deleting
   deployed production contexts or segments while sales orders still reference
   them.

## Deployment, Publication, and Consumption

After a successful import, use the core EFF deployment workflow, then validate
the intended Order Management display and consuming integration:

1. Deploy and publish the EFF, then test it in the Order Management work area.
   Header dialog display uses the `DOO_HEADERS_ADD_INFO` category. Direct
   Redwood header or order-line display requires Visual Builder Studio.
2. After deployment status is `DEPLOYED`, follow **Post-Deployment ESS
   Synchronization**. The `SynchEFFAttributes` request is task-specific and
   remains separately approval-gated.
3. When the EFF is used by business rules, constraints, business events,
   service mappings, integrations, or web services, run the documented Publish
   Extensible Flexfield Attributes scheduled process through its routed
   workflow and update any affected payload or schema contracts. An EFF cannot
   be used in an approval rule.
4. When the EFF is BI-enabled and reporting is required, run Import Oracle
   Fusion Data Extensions for Transactional Business Intelligence through its
   routed workflow before expecting it in OTBI subject areas.

## Integration and Extension Guardrails

- Refer to a context by its context code and a segment by its API name. If an
  API name is absent on an existing segment, use the segment code with spaces
  replaced by underscores.
- For Order Management extensions, check that the context and segment exist
  and have a value before using them. Use `getOrCreateContextRow` only to
  create or update a row; use `getContextRow` only to retrieve one.
- For file-based order import, map header EFF values to
  `DOO_ORDER_HDRS_ALL_EFF_B_INT` and line EFF values to
  `DOO_ORDER_LINES_ALL_EFF_B_INT`. Keep the delivered worksheet and column
  names unchanged, and map each segment to its designated attribute column.
- Do not update an EFF through import, REST, web services, or ADF on a closed
  sales order or closed order line; update it only in the Order Management work
  area.

## Post-Deployment ESS Synchronization

For either approved flexfield code, after the core EFF deployment-status call
confirms the exact deployment completed successfully with `DEPLOYED`, pass the
following task-specific post-deployment action to
`core.fusion-api.apps-common.extensible-flexfields`. Do not invoke Fusion REST
directly from this task skill.

| Field | Required value |
| --- | --- |
| Method | `POST` |
| Endpoint | `/fscmRestApi/resources/11.13.18.05/erpintegrations` |
| OperationName | `submitESSJobRequest` |
| JobPackageName | `oracle/apps/ess/scm/doo/decomposition/receiveTransform/transformSalesOrder` |
| JobDefName | `SynchEFFAttributes` |

Use this immutable payload; do not add an `ESSParameters` value unless a later
task-specific requirement supplies one:

```json
{
  "OperationName": "submitESSJobRequest",
  "JobPackageName": "oracle/apps/ess/scm/doo/decomposition/receiveTransform/transformSalesOrder",
  "JobDefName": "SynchEFFAttributes"
}
```

The core EFF workflow must obtain a separate explicit approval immediately
before submitting this ESS request; approval for the flexfield deployment does
not authorize the ESS request. Submit it once only after `DEPLOYED`, capture
the returned `ReqstId`, and, when tracking is requested, use the core workflow
to record the ESS status. Do not retry the POST without a new explicit
approval. If deployment is pending, failed, timed out, or otherwise not
`DEPLOYED`, skip the ESS submission and return that deployment status.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Route EFF setup-data export and import through `core.fusion-api.apps-common`
   using one of the approved flexfield codes.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Orders`
- Setup task name: `Manage Order Extensible Flexfields`
- Setup task code: `DOO_MANAGE_ORCHESTRATION_EXTENSIBLE_FLEXFIELDS`
- Flexfield code: `DOO_FULFILL_LINES_ADD_INFO` or `DOO_HEADERS_ADD_INFO`

## Archive Parent Rows for Page and Usage Changes

When an import adds or updates any usage- or page-level object, build the
application flexfield-usage parent row; never leave
`ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_USAGE.csv` header-only on that route.

1. Export the current setup data for the exact approved flexfield code and
   application ID. Copy the exact matching row from
   `ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_USAGE.csv` into the immutable import
   archive. For Order Management EFFs, retain the exported
   `FlexfieldUsageCode`; do not invent or substitute it.
2. Include the matching `FND_APP_DESCRIPTIVE_FLEXFIELD.csv` root row with the
   usage row. Validate the root code and application ID match every child row.
3. For a context usage change, include the usage parent plus the exact
   `ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_CONTEXT_USAGE.csv` row. Include the
   context-category association when the context must be associated to the
   category.
4. For a page or page-context association change, include the usage parent,
   the required context usage/category rows, the
   `ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_PAGE.csv` row, and the
   `ORA_FND_APP_DESCRIPTIVE_FLEXFIELD_PAGE_TASK_FLOW.csv` row. Preserve the
   exported category and usage codes, and validate page and context sequence
   values before archive creation.
5. Check the live export for the exact usage, page code, and page/context
   association first. If it already matches the requested values, return a
   no-change result instead of importing a duplicate. If the usage parent is
   missing or ambiguous, stop with `catalog_or_metadata_mismatch`; do not build
   an orphan page or context-usage row.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `flexfield_deployment_context`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `post_deployment_ess_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.order-management.orders` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Sources

- [Overview of Setting Up Extensible Flexfields in Order Management](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/overview-of-setting-up-extensible-flexfields-in-order-management.html#s20063869)
- [Guidelines for Setting Up Extensible Flexfields in Order Management](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/guidelines-for-setting-up-extensible-flexfields-in-order.html#s20065854)
