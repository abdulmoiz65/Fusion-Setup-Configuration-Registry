---
skill_id: "cx.sales.sales-catalog-and-products.manage-sales-index"
name: "Manage Sales Index"
description: "Independently manages requested Item or Catalog index profiles through delegated Product Management indexing; it can also continue a verified Sales catalog association."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Catalog and Products"
functional_area_code: "ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS"
task_code: "CUSTOM_MANAGE_SALES_INDEX"
task_name: "Manage Sales Index"
parent_skill_id: "cx.sales.sales-catalog-and-products"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.1.2"
inputs:
  - "project_context"
  - "active_runbook_context"
  - "target_fusion_environment"
  - "verified_sales_catalog_association"
  - "requested_index_name"
  - "requested_index_names"
  - "attributes_to_add"
  - "attributes_to_remove"
  - "index_rebuild_requested"
outputs:
  - "sales_index_handoff"
  - "delegated_index_request"
  - "resolved_product_management_index_task"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "scm.product-management.index-management.manage-product-management-indexes"
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
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-sales-index/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/manage-sales-index/current/"
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
  - "Resolves the active Run Book's Manage Product Management Indexes task before persisting an independent or Sales-originated index handoff and delegates one Product Management index request per selected index."
required_privileges: []
---

# Manage Sales Index

## Purpose

Independently manage one or two requested Product Management index operations for Item and Catalog. This skill can also continue a verified Sales functional-area catalog association, but it does not require that association for a standalone index request. [Manage Product Management Indexes](../../../../scm/product-management/index-management/manage-product-management-indexes/SKILL.md) owns index metadata, attribute delta calculation, Data Loader execution, post-load verification, and ESS rebuild approval.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_SALES_INDEX`
- task_name: `Manage Sales Index`
- parent_skill_id: `cx.sales.sales-catalog-and-products`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Sales Catalog and Products`
- functional_area_code: `ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Standalone Preconditions

Use the currently authenticated Fusion environment as `target_fusion_environment` when the request does not explicitly name one, and require one or both selected index profiles. For an Item-only or Catalog-only standalone request, do not require a Sales catalog association.

When `verified_sales_catalog_association` is supplied by Manage Sales Functional Area Catalog, require a durable same-environment verification record containing all of:

- successful catalog-assignment import reference;
- Sales functional area ID `38`;
- resolved Sales catalog code and name; and
- target Fusion environment.

Stop a Sales-originated request when its association is planned, pending, failed, unverified, belongs to another functional area, or targets a different environment. Do not infer verification from a user statement, an import submission, or a Run Book dependency alone.

## Preflight and Execution Safety

Before preparing a delegated handoff, load and apply
`ora-resource/ora_error_handling.md`, then confirm all of the following:

1. The target is explicitly supplied or is the currently authenticated Fusion
   environment, and the target identity is retained in each handoff record.
2. Every selected index is `Item` or `Catalog`, has its complete exact profile,
   and is represented by a separate single-index child request.
3. The active Run Book resolves exactly one `Manage Product Management Indexes`
   task with task code `CUSTOM_EGP_MANAGE_PM_INDEXES`. Retain that resolved task
   as the child execution target for each Item or Catalog request; a repository
   dependency alone is insufficient.
4. The Product Management child contract is available, and the child’s
   canonical-index lookup and current-profile comparison are complete for each
   selected index.
5. A Sales-originated request has same-environment verified association evidence
   with Sales functional-area ID `38`; a standalone request does not require it.

This skill performs no direct Fusion mutation. It does not call Data Loader or
ESS, and it never submits, retries, polls, or replaces a child's external request. The
delegated Product Management skill owns its immutable artifact preview, target
environment confirmation, Data Loader and ESS approvals, bounded retry policy,
timeouts, diagnostics, and token redaction. A child failure, timeout, or
ambiguous lookup is terminal for that child handoff; preserve its sanitized
reference and require a new user request for any retry.

## Delegation Contract

Accept `requested_index_names` containing one or both distinct values: `Item` and `Catalog`. Continue to accept the legacy singular `requested_index_name` as one selected index. Require the complete `attributes_to_add` profile for every selected index and retain any explicit removals unchanged. Persist a separate non-secret handoff record for each selected index with its request origin, selected index, requested attributes, target environment, optional verified Sales-association reference, and `index_rebuild_requested` value.

Invoke `scm.product-management.index-management.manage-product-management-indexes` once per selected index. The delegated skill compares the current index metadata with the supplied profile, adds only missing attributes, and rebuilds that selected index after the resulting attribute state is complete. Do not combine Item and Catalog into one call, calculate attributes locally, or call Data Loader or ESS directly.

For every Item or Catalog request, first resolve the Product Management child
from the active Run Book dashboard by exact task code
`CUSTOM_EGP_MANAGE_PM_INDEXES` and exact task name `Manage Product Management
Indexes`. If the active Run Book does not contain exactly one such task, stop
before index metadata lookup and tell the user to create or select a Run Book
that includes both `Manage Sales Index` and `Manage Product Management Indexes`.
Do not use a skill file's mere repository presence, a task Note, or an unrelated
Run Book as a substitute for this resolution.

Before constructing the child request, apply `resolve_sales_index_attribute_names`
in `ora_reference_lookups.md`. Triplets are selection keys, not child input rows.
Retain the complete ordered profile in `attributes_to_add` as named rows, even
when some attributes already exist; only the child calculates the missing delta.
Preserve explicit removals unchanged. A complete current profile is rebuild-only
only when there are no removals; the child still checks seeded repairs.

The delegated skill owns all mutation approvals. A Sales-association approval does not approve indexed-attribute import or index rebuild.

## Sequencing

When both profiles are requested, queue Item then Catalog in the same project.
Standalone requests do not require association verification. Sales-originated
requests require the verified association described above before starting Item.

The child has one current invocation per project, not per index. Never invoke
both children concurrently or overwrite its current request/delta/state while
an invocation is pending. After Item reaches `ess_submitted` or `ess_skipped`,
retain an immutable version of its request, delta, approvals, result and external
IDs through the declared artifact services. Then re-resolve the active Run Book
child task and delegate Catalog using the child's documented `--start-new`
terminal-state archival lifecycle. Archive evidence before replacing current
artifacts; an archival failure blocks the next invocation. A pending approval,
pending Data Loader operation, failure, or timeout pauses this queue; resumption
uses the same child context, not a new request. A blocked child requires user
direction before moving on.

Do not wait for the submitted Item ESS job to succeed before starting Catalog.
The jobs may run concurrently, but preparation and submission are serialized.
Each child obtains its own approvals; never reuse approval or request IDs.
Report each submitted job separately, and do not equate submission with success.

## Offline Contract Checks

Run `python3 -m unittest discover -s pillars/cx/sales/sales-catalog-and-products/manage-sales-index/tests -v`.
These synthetic checks exercise the unchanged child's delta/state guards; they
do not contact Fusion or establish live environment readiness.
For review cases covering lookup ambiguity and missing Run Book tasks, use
[tests/scenarios.md](tests/scenarios.md).

## Failure Handling

Classify a missing target environment or profile as `input_validation`; classify missing Sales-association evidence only when the request is Sales-originated; classify mismatched environments as `transport_or_environment`; and classify a failed or pending delegated index as `process_failed` or `process_timeout`. Preserve the handoff record and stop; do not retry or bypass the delegated Product Management workflow.

## Implementation Notes

Use the parent functional-area skill `cx.sales.sales-catalog-and-products` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
