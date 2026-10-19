---
skill_id: "cx.sales.sales-catalog-and-products.manage-product-group-profile-option-values"
name: "Manage Product Group Profile Option Values Setup Task Guidance"
description: "Guides setup of the Sales Products Item Organization through QSC_SALES_PRODUCTS_INVENTORY_ORG_ID, with FSM export/import transport available for other profile options in the setup task."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Catalog and Products"
functional_area_code: "ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS"
task_code: "QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS"
task_name: "Manage Product Group Profile Option Values"
parent_skill_id: "cx.sales.sales-catalog-and-products"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.2.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "fusion_environment_context"
  - "request_intent"
  - "profile_option_code"
  - "profile_level"
  - "item_organization_optional"
  - "expected_current_value_optional"
  - "proposed_value_optional"
  - "reference_export_optional"
  - "execution_approval_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "item_organization_list_optional"
  - "immutable_change_preview_optional"
  - "rest_execution_result_optional"
  - "fsm_import_handoff_result_optional"
  - "post_change_verification_optional"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.offering-export"
  - "core.fusion-api.apps-common"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-product-group-profile-option-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-product-group-profile-option-values/current/"
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
  - "Submits and downloads approved FSM exports at task, functional-area, or offering scope."
  - "Reads QSC profile definitions and Site values through core.fusion-api.apps-common."
  - "Reads Inventory Organizations through core.fusion-api.rest-api-client for the documented one-code validation or requested details."
  - "After exact approval, may create, update, or delete the QSC_SALES_PRODUCTS_INVENTORY_ORG_ID Site child value through core.fusion-api.apps-common."
  - "After exact approval, routes FSM imports through core.data-loader."
required_privileges:
  - "Privileges to export and import setup data for QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS."
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID Site-value writes."
  - "Read access to Inventory Organizations REST data for one-code item-master validation."
---

# Manage Product Group Profile Option Values Setup Task Guidance

## Purpose

The main purpose of this task is to set up the **Sales Products Item Organization**
through profile option `QSC_SALES_PRODUCTS_INVENTORY_ORG_ID`.

This skill does not provide profile-specific configuration, validation, REST,
or organization guidance for other profile options.

## Setup Task Skill Contract

- task_code: `QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS`
- task_name: `Manage Product Group Profile Option Values`
- parent_skill_id: `cx.sales.sales-catalog-and-products`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Sales Catalog and Products`
- functional_area_code: `ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill to set up or review the Sales Products Item Organization.

## Mandatory Task-Control Contract

Classify the user's intent before choosing a route. A request to view the
configured value is a review request. A request to attach, assign, use, change,
or replace a Sales Products Item Organization is a value-change request. A
request to clear, detach, remove, or delete it is a removal request.

For a value-change request for `QSC_SALES_PRODUCTS_INVENTORY_ORG_ID`, the
compiled task graph prepares an approved Apps Common handoff and never
authorizes a write by itself. Core export, import, and read-only lookup
workflows own their own execution gates.

## Supported Profile Options and Routes

Use **Profile Option Code** and the user's intent as the routing key.

| Profile option scope | View configured value | Provide or change organization | Remove organization | FSM request |
|---|---|---|---|---|
| `QSC_SALES_PRODUCTS_INVENTORY_ORG_ID` | Read the profile definition and configured Site value through `core.fusion-api.apps-common`, then always resolve the returned code to its organization name through Inventory Organizations. Do the same before reporting a value sourced from an FSM export. | Accept one exact organization code or name; resolve it to one active master organization, then require the Site level, compiled task graph, immutable preview, and exact approval before the Apps Common handoff. | Use Apps Common to read the Site child. If it exists, present an immutable DELETE preview and require exact approval before deleting that child. If it is absent, report that it is already unset. No item-master validation is required. | Use the requested FSM task, functional-area, or offering scope. An FSM package must not bypass QSC item-master validation before import. |
| Any unsupported QSC profile option in this setup task | FSM-exported values may be reported without task-owned profile or organization validation. | FSM import only through `core.data-loader`; preserve the exported package structure and values. | Not task-specifically supported. | Use `shared.setup-export.task-level-export`, `shared.setup-export.functional-area-export`, or `shared.setup-export.offering-export` for the requested scope. This is transport support, not profile-specific task support. |

Do not use a browser LOV, raw SQL, profile-option SQL validation, or the QSC
item-master route for the FSM-only codes.

## QSC Item-Master Rules

For `QSC_SALES_PRODUCTS_INVENTORY_ORG_ID`, use Apps Common only for profile
definition and Site-value operations. Use
`core.fusion-api.rest-api-client` for the read-only Inventory Organizations
lookup. Require exactly one active master-organization record whose
`OrganizationCode` and `MasterOrganizationCode` both equal the supplied code.

| Situation | Required behavior |
|---|---|
| List all valid organizations | Explain that the complete list requires a read-only `Manage Item Organizations` (`EGP_MANAGE_ITEM_ORGANIZATIONS`) FSM export in the target environment, then ask the user for approval before running it. Only after approval, derive the complete code-and-name list from `ORA_INV_ORG_PARENT_FOR_ITEMORG.csv` and `INV_ITEM_ORG_PARAMETER.csv`. If approval is declined, stop and explain that the complete export-backed list cannot be provided. Do not use Inventory Organizations to retrieve the names for this list, or substitute a REST list, browser LOV, or SQL. |
| ProfileOptions REST or FSM export returns a code | Always resolve the exact `OrganizationCode` through Inventory Organizations and report both the code and organization name. This display lookup does not establish item-master validity unless validation is separately requested. |
| REST configured-value read returns `V1` | Resolve and report the organization name, then validate `V1` as exactly one active master organization before reporting it as valid. |
| Organization name or details are requested | Resolve the exact organization code and return the requested fields from Inventory Organizations. This does not establish item-master validity unless the validation route is also selected. |
| A QSC import or Site PATCH proposes a code or name | Resolve the supplied code or name as exactly one active master organization before the approved mutation or import. When a value is supplied without identifying whether it is a code or name and it matches multiple rows, ask which it is and rerun that exact field match. When both code and name are supplied, require them to resolve to that same record. |

On zero matches, multiple matches, or REST access/data-security failure, stop
the required validation. Report a configured value as unverified when
applicable; do not create prerequisite setup or substitute another source.

## Direct QSC Site-Value Requests

When a request supplies a Sales Products Item Organization, require
`QSC_SALES_PRODUCTS_INVENTORY_ORG_ID`, the `Site` level, and one proposed item
master organization code or name. Before the Apps Common handoff:

1. Read the exact profile definition and configured Site value; confirm the
   Site level is enabled and updatable.
2. Resolve and validate the proposed item master through the task-local rule
   graph; use the resolved organization code as the profile value.
3. Present a user-facing preview containing the target environment, task and
   profile codes, Site level, expected current value or absence, proposed code,
   resolved organization identity, and validation time. Record the preview hash
   internally to bind approval to this unchanged preview; do not display it to
   the user unless requested.
4. Obtain approval bound to that unchanged preview. Re-read the Site value
   immediately before the write; a changed value or absence invalidates the
   preview and approval.
5. If the Site child exists, update it through Apps Common. If it is absent,
   create that Site child through Apps Common with the approved resolved code.
   Then re-read the configured value. Do not retry a failed or indeterminate
   write.

When a request asks to remove the Sales Products Item Organization, require
only `QSC_SALES_PRODUCTS_INVENTORY_ORG_ID` and the `Site` level. Do not perform
an item-master lookup. Read the Site child through Apps Common:

1. If no Site child exists, report that the value is already unset; do not send
   a DELETE request.
2. If it exists, present a user-facing preview containing the target
   environment, task and profile codes, Site level, current value, and
   requested DELETE operation. Record the preview hash internally to bind
   approval to this unchanged preview; do not display it to the user unless
   requested.
3. Obtain approval bound to the unchanged preview. Re-read the Site child
   immediately before deletion; any change or absence invalidates the preview
   and approval.
4. Delete only the returned Site child through Apps Common, then re-read to
   confirm its absence. Do not retry a failed or indeterminate DELETE.

After an approved delete, a later request that supplies an organization follows the normal validation and
approval flow. Because the Site child is absent, Apps Common creates it before
storing the approved resolved organization code.

Never modify the profile definition, level metadata, SQL validation,
descriptions, audit fields, or another profile option.

## Setup Task Metadata

- Task name: `Manage Product Group Profile Option Values`
- Task code: `QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Route the currently
FSM-only profile options through the requested FSM scope:

| Requested scope | Export route | Import route |
| --- | --- | --- |
| Task | `shared.setup-export.task-level-export` | `core.data-loader` |
| Functional area | `shared.setup-export.functional-area-export` | `core.data-loader` |
| Offering | `shared.setup-export.offering-export` | `core.data-loader` |

1. Preserve the values as exported; do not run task-owned profile-value or
   item-organization validation for the FSM-only profile options.
2. Before any import, confirm the exact target environment, selected scope,
   immutable package, package hash, and import approval. Preserve the selected
   scope's export structure and all non-intended rows; do not add unrelated
   setup records or change definitions, metadata, headers, or audit fields.
   These are package-integrity controls, not business-value validation.
   `core.data-loader` remains the mandatory import orchestrator.

For `QSC_SALES_PRODUCTS_INVENTORY_ORG_ID`, use the validated profile-option
route. An FSM package must not bypass item-master validation and approval
requirements before import.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Sales Catalog and Products`
- Setup task name: `Manage Product Group Profile Option Values`
- Setup task code: `QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS`

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `fusion_environment_context`
- `request_intent`: what the user wants to accomplish, expressed in their own words
- `profile_option_code`
- `profile_level`: `Site` for the direct QSC route
- `item_organization_optional`
- `expected_current_value_optional`
- `proposed_value_optional`
- `reference_export_optional`
- `execution_approval_optional`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `item_organization_list_optional`
- `immutable_change_preview_optional`
- `rest_execution_result_optional`
- `fsm_import_handoff_result_optional`
- `post_change_verification_optional`
- `skill_run_record`
- `token_usage_record`

## Preflight and Error Handling

Before a side-effecting export, import, or direct QSC Site-value operation,
load `ora-resource/ora_input_validation.md` and
`ora-resource/ora_error_handling.md`, then verify the target environment,
request intent, required privileges, catalog task and support flags, selected
route, and all required inputs. For FSM imports, also verify the immutable
package, package hash, requested scope, and explicit import approval. For a
direct QSC Site-value mutation or deletion, verify the exact profile code,
`Site` level, current value or absence, item-master validation where required,
immutable preview, and approval bound to that unchanged preview.

Classify failures using `governance/error-handling-guidelines.md`. Stop before
side effects on invalid or ambiguous inputs, catalog mismatches, missing
privileges, unavailable dependencies, changed previews, or missing approval.
Do not retry a live PATCH, DELETE, or import after failure or an indeterminate
result without a new exact approval and idempotency review. Preserve the
available redacted status and external identifiers for diagnostics, and route
durable diagnostics through the declared project workspace outputs.

## Redaction and Sensitive Data

Never print or persist OAuth tokens, token caches, credentials, client
secrets, private keys, wallet files, full base64 payloads, or sensitive
customer data in plans, previews, skill-run records, token-usage records, or
diagnostics. When an Apps Common or REST response contains sensitive material,
retain only the minimum redacted error summary and any safe identifiers such
as ECID or request ID needed for follow-up.

## Implementation Notes

Use the parent functional-area skill `cx.sales.sales-catalog-and-products` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
