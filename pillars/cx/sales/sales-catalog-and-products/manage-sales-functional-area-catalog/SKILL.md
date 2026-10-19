---
skill_id: "cx.sales.sales-catalog-and-products.manage-sales-functional-area-catalog"
name: "manage-sales-functional-area-catalog Setup Task Guidance"
description: "Provides task-specific setup guidance for manage-sales-functional-area-catalog, including an immediate Manage Sales Index invocation prompt when a Sales catalog-assignment import starts."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Catalog and Products"
functional_area_code: "ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS"
task_code: "CUSTOM_MANAGE_SALES_FUNCTIONAL_AREA_CATALOG"
task_name: "Manage Sales Functional Area Catalog"
parent_skill_id: "cx.sales.sales-catalog-and-products"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.1.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "post_association_index_attributes"
  - "verified_sales_catalog_association"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "prepared_sales_assignment_package"
  - "index_invocation_prompt"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "scm.product-management.catalogs.manage-functional-area-catalogs"
  - "cx.sales.sales-catalog-and-products.manage-sales-index"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-sales-functional-area-catalog/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-sales-functional-area-catalog/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-sales-functional-area-catalog/current/index-invocation-prompt.json"
    versioning_policy: "replace-after-confirmation"
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
  - "Prepares a contained, assignment-only FSM package for delegated SCM validation and persists a non-secret Manage Sales Index invocation prompt when the delegated import is accepted."
required_privileges: []
---

# manage-sales-functional-area-catalog Setup Task Guidance

## Purpose

Provides Sales-specific setup planning, validation, and delegation guidance for `manage-sales-functional-area-catalog` under `Sales Catalog and Products`.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_SALES_FUNCTIONAL_AREA_CATALOG`
- task_name: `Manage Sales Functional Area Catalog`
- parent_skill_id: `cx.sales.sales-catalog-and-products`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Sales Catalog and Products`
- functional_area_code: `ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill to identify the current Sales functional-area catalog or to plan and validate a Sales catalog assignment before delegating supported export and import work to `EGP_MANAGE_DEFAULT_CATALOGS`.

## Setup Task Metadata

- Task name: `Manage Sales Functional Area Catalog`
- Task code: `CUSTOM_MANAGE_SALES_FUNCTIONAL_AREA_CATALOG`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## Sales Functional Area Catalog Assignment

This task delegates the actual catalog assignment to the SCM Product Management task [Manage Functional Area Catalogs](../../../../scm/product-management/catalogs/manage-functional-area-catalogs/SKILL.md) (`EGP_MANAGE_DEFAULT_CATALOGS`). That task owns the FSM export, package validation, approval, import, and post-import validation workflow.

For a current-assignment inquiry, export `EGP_MANAGE_DEFAULT_CATALOGS` through `shared.setup-export.task-level-export`, validate the fresh same-task package through the delegated SCM task, and resolve exactly one Sales functional-area assignment. Return both Catalog Code and Catalog Name from the resolved assignment and catalog rows.

Provide the exact catalog code, functional area `Sales`, the applicable Sales rule values, and a validated same-task FSM baseline package to the SCM task. Do not use this custom task as a standalone REST or CSV import.

The delegated SCM task uses FSM through `core.data-loader` and requires an immutable preview and approval immediately before import.

## Local Artifact Preflight and Package Preparation

Before preparing an assignment package, require an initialized non-symlink
`project/{project_id}` workspace, a fresh validated `EGP_MANAGE_DEFAULT_CATALOGS`
baseline inside that workspace, a nonblank target Catalog Code, and a new output
path beneath that same project. Reject a path escape, symlinked path component,
baseline/output alias, missing required CSV member, ambiguous Sales assignment,
or unconfirmed overwrite. Do not prepare an artifact when any preflight fails.

Use `scripts/build_sales_assignment_package.py` to create the assignment-only
FSM package. It retains only the required metadata, one FunctionalAreaId `38`
assignment row with the requested Catalog Code, and header-only unrelated CSV
members. Validate the staged package's member set and row shape, persist its
immutable preview under the project workspace, then hand that artifact to
Manage Functional Area Catalogs for its normal package validation, target
binding, approval, import, and verification. The builder never imports to
Fusion and cannot replace an existing output unless the user explicitly
confirms replacement with `--replace-after-confirmation`.

Do not retry a failed local build automatically. Preserve the baseline and any
existing output, report the `artifact_persistence` or `input_validation`
failure, and require a corrected request. The delegated SCM task retains sole
ownership of Fusion import approvals, submission, monitoring, diagnostics and
retries.

## Catalog-Assignment Index Invocation Prompt

### Immediate Notification

As soon as the delegated SCM assignment workflow reports an accepted catalog-assignment import request, emit a durable prompt to invoke [Manage Sales Index](../manage-sales-index/SKILL.md). Do not wait for import polling, terminal status, or post-import Sales-association verification before emitting this prompt.

Use `scripts/prepare_index_invocation_prompt.py` with the non-secret import acceptance record. It requires the same initialized non-symlink project workspace and writes `index-invocation-prompt.json` containing the target environment, accepted import reference, and optional requested catalog identity. It rejects symlinked artifact paths and refuses to replace an existing prompt unless the user explicitly confirms replacement with `--replace-after-confirmation`.

Present this exact message after the prompt is written: **"The Sales catalog-assignment import has started. You can now invoke Manage Sales Index for Item and/or Catalog indexing in the same Fusion environment. The catalog association has not yet been verified."**

This is a notification only. It neither invokes Manage Sales Index nor implies the catalog association succeeded. Manage Sales Index remains independently invocable and owns its delegated Product Management workflow. Preserve the import reference and target environment in the prompt; do not include credentials or catalog data beyond the user-supplied catalog identity.

If post-import verification later fails, preserve the notification artifact and report the failure. Do not retract the prompt, retry the catalog import, or claim that an index job ran.

### Subsequent CX Follow-Up Trigger

When the user asks to **continue**, asks **what to do next**, or otherwise resumes the Sales catalog-assignment workflow after an accepted import, load the durable `index-invocation-prompt.json` and display its exact message before taking any separately requested CX action. If the artifact is absent but the durable assignment record contains an accepted import reference and target environment, create it with `prepare_index_invocation_prompt.py` before displaying the message. If a different prompt already exists, preserve it and request explicit confirmation before replacement.

When the user asks to **check status**, run the required core Data Loader status workflow first. Its result must remain the exact core status report. Do not append the indexing prompt to that report. On the user's next CX workflow request, load and display the durable prompt before continuing.

The Product Management child alone determines whether the complete seeded,
requested-addition, and requested-removal delta is empty. Only after that child
verification may it skip Data Loader and prepare a rebuild-only request. It
must still obtain fresh explicit ESS approval for the exact rebuild payload; an
earlier catalog-assignment approval or the other index's approval is not reusable.

### Item Index Attribute Profile

Pass the following identities as `attributes_to_add` for the single `Item` index invocation:

```text
ITEM_NUMBER#Main#ITEM
DESCRIPTION#Main#ITEM
ORGANIZATION_CODE#Main#ITEM
PRIMARY_UOM_CODE#Main#ITEM
CUSTOMER_ORDER_ENABLED_FLAG#OrderManagement#ITEM
CATEGORY_NAME#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES
CATALOG_NAME#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES
START_DATE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES
END_DATE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES
SALES_PRODUCT_TYPE#OrderManagement#ITEM
SERV_REQ_ENABLED_CODE#Service#ITEM
CSS_ENABLED_FLAG#Service#ITEM
INVENTORY_ITEM_STATUS_CODE#Main#ITEM
BOM_ITEM_TYPE#BillofMaterials#ITEM
LONG_DESCRIPTION#Main#ITEM
CATEGORY_CODE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES
CATALOG_CODE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES
```

### Catalog Index Attribute Profile

Pass the following identities as `attributes_to_add` for the separate `Catalog` index invocation:

```text
FUNCTIONAL_AREA_ID#CATALOG_SEEDED#ES_CATALOG_CATEGORY
CATEGORY_NAME#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
CATALOG_NAME#CATALOG_SEEDED#ES_CATALOG_CATEGORY
TERRITORY#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
CATALOG_CODE#CATALOG_SEEDED#ES_CATALOG_CATEGORY
START_DATE#CATALOG_SEEDED#ES_CATALOG_CATEGORY
END_DATE#CATALOG_SEEDED#ES_CATALOG_CATEGORY
CONTROL_LEVEL#CATALOG_SEEDED#ES_CATALOG_CATEGORY
DEFAULT_CATEGORY_ID#CATALOG_SEEDED#ES_CATALOG_CATEGORY
DESCRIPTION#CATALOG_SEEDED#ES_CATALOG_CATEGORY
MULT_ITEM_CAT_ASSIGN_FLAG#CATALOG_SEEDED#ES_CATALOG_CATEGORY
CATALOG_CONTENT_CODE#CATALOG_SEEDED#ES_CATALOG_CATEGORY
CATEGORY_CODE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
START_DATE_ACTIVE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
END_DATE_ACTIVE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
DESCRIPTION#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
CATEGORY_CONTENT_CODE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
CATEGORY_SHARED_FLAG#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
PARENT_HIERARCHY_LEVEL#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
PARENT_HIERARCHY_CATEGORY_CODE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
PARENT_HIERARCHY_CATEGORY_ID#CATEGORY_SEEDED#ES_CATALOG_CATEGORY
```

## Assignment Scope Validation

Use this custom task only for a default catalog assignment to the `Sales` functional area.

Before package preview or import, resolve the supplied functional-area name and/or ID against `EGP_CATALOG_FUNCTIONAL_AREAS`. Continue only when the resolved entry is exactly `Sales` and the assignment row uses that resolved functional-area ID. Reject a missing, ambiguous, mismatched, or non-Sales functional area; do not use this task for Service or any other functional-area assignment.

Treat a rejected non-Sales assignment as terminal for this skill. Do not look up, preview, import, or delegate it. A request for another functional area requires a separate, independently routed workflow.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `post_association_index_attributes`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `prepared_sales_assignment_package`
- `index_invocation_prompt`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.sales-catalog-and-products` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Offline Contract Checks

Run `python3 -m unittest discover -s pillars/cx/sales/sales-catalog-and-products/manage-sales-functional-area-catalog/tests -v`. These tests use only temporary synthetic package and project fixtures; they do not contact Fusion.
