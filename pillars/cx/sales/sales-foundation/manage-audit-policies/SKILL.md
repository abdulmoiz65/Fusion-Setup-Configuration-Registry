---
skill_id: "cx.sales.sales-foundation.manage-audit-policies"
name: "Manage Account, Contact, and Household Audit Policies"
description: "Checks and enables Oracle Fusion audit for CX Account, Contact, Household, and their live-resolved child business objects, and additively enables named audit attributes through the shared Audit Setup core capability. Use for parent or child object audit-status checks, object-level audit enablement, audit-attribute inventory validation, requests to identify currently enabled audit attributes, and approved enablement of one or more named attributes without disabling omitted attributes."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Foundation"
functional_area_code: "ORA_ZBS_SALES_FOUNDATION"
task_code: "FND_MANAGE_AUDIT_POLICIES"
task_name: "Manage Audit Policies"
parent_skill_id: "cx.sales.sales-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.5.1"
inputs:
  - "project_context"
  - "fusion_environment_context"
  - "audit_object"
  - "child_audit_object"
  - "audit_operation"
  - "requested_attributes"
  - "execution_approval"
outputs:
  - "object_audit_status"
  - "child_object_inventory"
  - "resolved_audit_object"
  - "auditable_attribute_inventory"
  - "enabled_attribute_result"
  - "immutable_audit_preview"
  - "execution_result"
  - "verification_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.sales.sales-foundation"
  - "core.fusion-api.audit-setup"
uses_core:
  - "core.fusion-api.audit-setup"
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
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-audit-policies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-audit-policies/current/"
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
    - "Oracle Fusion Cloud Applications 26B or newer"
side_effects:
  - "Reads Account, Contact, Household, or a live-resolved child object's audit setup through core.fusion-api.audit-setup."
  - "May enable audit for exactly one Account, Contact, Household, or validated child business object after explicit approval."
  - "May additively enable named audit attributes for exactly one Account, Contact, Household, or validated child business object after explicit approval."
  - "May persist redacted validation, execution, and skill-run evidence in the active project workspace."
required_privileges:
  - "Access to the exact target Oracle Fusion environment and required OAuth scope."
  - "Fusion privileges appropriate to view and manage audit setup."
---

# Manage Account, Contact, and Household Audit Policies

## Purpose

Check and enable audit for CX Account, Contact, Household, and child business
objects that the live Audit Setup inventory binds to one of those roots.
Validate requested attribute names and enable those attributes without
disabling existing audited attributes. Delegate every Fusion operation to
`core.fusion-api.audit-setup`.

## Setup Task Identity

- Task: `Manage Audit Policies` (`FND_MANAGE_AUDIT_POLICIES`)
- Pillar: `CX`
- Offering: `Sales`
- Functional area: `Sales Foundation` (`ORA_ZBS_SALES_FOUNDATION`)
- Parent skill: `cx.sales.sales-foundation`

The catalog reports CSV export/import support for the wider setup task. This
dedicated capability does not export or import FSM setup data; route any
separate task-level CSV request through the parent workflow. Audit reads and
writes in this skill always use `core.fusion-api.audit-setup`.

## Required Read Order

1. Read `references/audit-object-map.json` before resolving an object.
2. Read `core/fusion-api/audit-setup/SKILL.md` before any Fusion operation.
3. For project work, consume the active project context and use the declared
   project-management dependencies for durable evidence.

## Object Boundary

Treat the exact `account`, `contact`, and `household` entries in the object map
as supported root candidates. Before using any mapped root for status, child
resolution, attribute inventory, preview, or mutation, reconcile its complete
identity against a fresh live `get-setup --application sales` response.
Support either a validated root itself or one child resolved from that live
inventory.

Use the map's `application` and `application_module` together: retain rows with
`webApplication=sales` and the exact mapped `amname` before root or child
resolution. The same Account `OrganizationDVO` also appears under `customer`
in ActivityAM without the Account audit hierarchy. That occurrence is not an
alternative inventory for this skill. Keep Account's business-object identity
unchanged; application scope and object identity are distinct.

- Resolve `Account` only to `OrganizationDVO`, `Contact` only to `PersonDVO`,
  and `Household` only to `GroupVO`.
- A root is live-validated only when at least one `objectDetails` row has the
  exact mapped `viewObject` and its `parentObjectList` contains the exact mapped
  `parent_business_object`. Multiple rows are acceptable only when they resolve
  to the same object and parent identity. Fail closed on no match or conflicting
  identities and classify the result as `catalog_or_metadata_mismatch`.
- Never treat `check-status` as proof that a root exists. Fusion can return
  `auditSwitch: NONE` for an unknown object identity; use `get-setup` for
  existence and parent-binding validation before calling `check-status`.
- Require `audit_object=account|contact|household` before resolving a child.
  The selected root disambiguates children that are valid beneath multiple
  roots.
- Resolve `child_audit_object` by exact `viewObject` or a unique exact
  `viewObjectDisplayName` within the selected root's live hierarchy, using the
  procedure below. The child `viewObject` must differ from the root.
- For a resolved child, use its live immediate parent on the selected root path
  as `parentBusinessObject`; do not substitute the root for a nested parent.
- The root's `excluded_names` reject alternative root identities only. They
  are not child exclusions: Sales Account is a valid Account child when its
  live parent binding proves membership. Apply only
  `child_resolution.excluded_display_names` to child candidates.
- Permit `audit_object=both` (Account and Contact) or `audit_object=all`
  (Account, Contact, and Household) only for read-only root status checks.
  Require one root and at most one child for every other operation and every
  mutation.

## Supported Operations

| Operation | Support | Core Audit Setup route |
| --- | --- | --- |
| `view-status` | Automated read-only | `check-status` |
| `enable-object` | Approved live mutation | `check-status`, then `update-status`, then `check-status` |
| `list-auditable-attributes` | Automated read-only inventory | `get-setup --application sales` |
| `list-child-objects` | Automated read-only inventory | `get-setup --application sales` |
| `get-enabled-attributes` | Unsupported by the API | No Fusion call; return `UNSUPPORTED_API` |
| `enable-attributes` | Approved live mutation | `get-setup`, `check-status`, `update-status`, then `check-status` |

Do not expose internal operation names when the user's natural-language intent
is unambiguous.

## Core Delegation Boundary

- Use only `core.fusion-api.audit-setup` for Audit Setup reads and writes.
- Do not copy its OAuth flow, REST endpoints, request transport, token refresh,
  response normalization, or retry implementation into this skill.
- Do not invoke Audit Setup endpoints directly, call a generic REST client as a
  substitute, or modify a core skill for Account-, Contact-, or
  Household-specific behavior.
- For root and child attribute enablement, this specialized skill owns the
  additive semantics: an `attributesList` containing only requested
  `isAuditable: true` rows leaves omitted audited attributes unchanged.
- Pass the exact environment, object identity, payload, and execution options
  to the core capability and consume its structured result, diagnostics, and
  audit summary.

## Preflight Checks

Before any Fusion-changing action:

1. Resolve exactly one target environment and confirm it is the environment the
   user intends to change.
2. Resolve exactly one supported root from the object map and reconcile its
   exact `business_object` and `parent_business_object` against a fresh live
   inventory. When a child is requested, resolve it from the same fresh live
   inventory and prove every parent link back to the selected root in the
   mapped application module.
3. Confirm authentication readiness, required OAuth scope, and Audit Setup
   privileges through the core capability.
4. Validate the requested operation, required inputs, and mutually exclusive
   options before building a payload.
5. For attribute enablement, validate every exact attribute against the same
   live inventory row used to resolve the root or child object.
6. Confirm the operation is live, show its side effects, and require the exact
   preview approval defined below.
7. Revalidate the environment, object, payload, and fingerprint immediately
   before execution; stop if any value changed.

## View Object Audit Status

1. Resolve `account`, `contact`, `household`, `both`, or `all` from the object
   map and reconcile every selected root against a fresh live inventory, or
   resolve one requested child beneath exactly one live-validated root. `both`
   means Account and Contact; `all` means Account, Contact, and Household.
2. Invoke core Audit Setup `check-status` separately for each live-validated
   object.
3. Return the exact business object, `auditSwitch`, last-update time when
   present, environment summary, and core diagnostics.
4. Do not interpret `NONE`, `OFF`, or a missing affirmative switch as enabled.

Read-only status checks do not require execution approval.

## Enable Object Audit

1. Complete the preflight checks for exactly one object.
2. Invoke core Audit Setup `check-status` after the fresh live-inventory
   reconciliation. Do not use this status response as object-existence proof.
3. If `auditSwitch` is already `ON`, return `NO_CHANGE_REQUIRED`; do not invoke
   a mutation.
4. Otherwise build a preview that contains the environment, display name,
   business object, parent business object, current status, requested status,
   exact `enable: true` payload, impact, and preview fingerprint.
5. Stop for explicit approval bound to that exact preview. Approval of another
   object, environment, payload, plan, or earlier preview is invalid.
6. Immediately before execution, rerun the applicable preflight checks and
   ensure the preview fingerprint remains unchanged.
7. Invoke core Audit Setup `update-status` exactly once. Never retry a live
   mutation automatically.
8. Verify object status with a separate core `check-status` read.
9. Return `VERIFIED_SUCCESS`, `UNVERIFIED_SUCCESS`, `NO_CHANGE_REQUIRED`, or a
   classified failure.

## Child Object Inventory and Resolution

Use core Audit Setup `get-setup --application sales` as the source of live
child-object identity and parent membership. Read all `objectDetails` rows from
the core result, then restrict them to the mapped application and module.

1. Resolve and live-validate the selected root from
   `references/audit-object-map.json` in that scoped inventory.
2. Build parent-to-child links from each row's `parentObjectList`, ignoring
   self-parent entries. Each non-self entry is a possible parent binding, not
   an ordered ancestor path. Traverse from the selected root to include direct
   children and nested descendants. Use visited identities per path to stop
   cycles; never cross application-module boundaries or infer a link by name.
3. Apply only `child_resolution.excluded_display_names` to child candidates.
   Keep live-bound Sales Account children; the root's `excluded_names` do not
   apply here. Shared children may belong to several roots; retain only paths
   reachable from the user-selected root.
4. For `list-child-objects`, return `viewObject`, `viewObjectDisplayName`, the
   full `parentObjectList`, application, module, depth, and root-to-child paths.
   Collapse identical rows, preserving distinct parent bindings. Do not persist
   the result as a release-independent catalog.
5. For a requested child, require an exact view-object match or one unique exact
   display-name match in that hierarchy. Reject zero matches, conflicting rows,
   missing parent metadata, and disconnected objects. If several immediate
   parents or paths remain, list the choices and require selection before a
   status check, attribute lookup, preview, or mutation.
6. Record `root_object_key`, `child_business_object`,
   `child_object_display_name`, full `parent_object_list`, `application`,
   `application_module`, `root_to_child_path`, and the live immediate parent as
   `parent_business_object`. For a direct child that parent is the selected
   root. For a descendant it is the preceding object on the validated path.
   Revalidate every link and this exact parent before any mutation.

An empty child inventory is not proof that Account has no auditable children.
If the mapped module/root is absent or no children are discovered, return
`INCOMPLETE_INVENTORY` with `catalog_or_metadata_mismatch`, the queried scope,
and a next action to check metadata exposure and Audit Setup privileges. Do
not silently fall back to `customer`, report unsupported children, or permit a
mutation against an unresolved identity.

For documented support questions or a discrepancy, consult Oracle's current
[Sales audit hierarchy](https://docs.oracle.com/en/cloud/saas/sales/oasal/use-auditing-to-monitor-sales-application-changes.html).
Distinguish documented support from live discovery; documentation supplies
business labels, not executable view-object or parent identities. Never use
it to invent a mutation target. The
[Audit Setup contract](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-fndauditrestservice-audittrail-get-auditsetup-post.html)
defines parent identities through application-module view links.

## Auditable Attribute Inventory

Use core Audit Setup `get-setup --application sales` only to obtain the
available/auditable field inventory for the selected root or resolved child.
Filter by the mapped application/module, exact resolved `viewObject`, and
selected parent binding; do not merge attributes from other occurrences of
the same view object. Return attribute names and display names that the
response identifies as selectable and auditable.

Never describe this inventory as the currently enabled selection.

## Enabled Attribute Read Limitation

For `get-enabled-attributes`, return a structured result with:

```json
{
  "status": "UNSUPPORTED_API",
  "reason": "Fusion Audit Setup does not expose the current enabled-attribute selection through REST.",
  "manual_location": "Setup and Maintenance > Manage Audit Policies > Sales > selected Account, Contact, Household, or child object > Attributes",
  "enhancement_request": "ER 34232448"
}
```

Do not inspect the UI, request UI evidence, accept a manually supplied current
selection, or attempt to verify the current selection. Do not infer it from
`get-setup`, `check-status`, audit history, a prior skill run, or an
`update-status` response.

## Enable Attributes

Enabling named attributes is additive. Submit only the attributes the user asks
to enable with `isAuditable: true`; attributes omitted from the request remain
unchanged. Do not request the current enabled-attribute selection and do not ask
the user for a complete replacement list.

1. Require exactly one resolved root or child object, a non-empty unique list
   of exact attribute names, and the target environment.
2. Complete the preflight checks, including live inventory validation for every
   requested attribute. Reject unknown, ambiguous, duplicate, or cross-object
   names.
3. Invoke core Audit Setup `check-status` and record the object audit state.
4. Sort the unique attribute names deterministically and build the complete
   request payload with `enable: true` and one `isAuditable: true` row per
   requested attribute. Do not add negative rows or rows for omitted
   attributes.
5. Present one immutable preview containing the exact environment, object,
   additive semantics, requested attribute list, exact payload, impact, and
   SHA-256 fingerprint of the canonical payload.
6. For a child, include the selected root, child identity, full live
   `parentObjectList`, application/module, validated root-to-child path, and
   chosen immediate `parentBusinessObject` in the preview.
7. State prominently: `This enables only the requested attributes; existing
   audited attributes that are omitted from this payload remain enabled.`
8. Stop for separate explicit approval for this one resolved object and exact
   fingerprint. Any environment, object, attribute, payload, or fingerprint
   change invalidates approval.
9. Immediately before execution, rerun the applicable preflight checks,
   including every live parent link on the selected path when applicable, and
   confirm the preview remains unchanged. Invoke core Audit Setup
   `update-status` exactly once. Never retry the live mutation automatically.
10. Verify with core Audit Setup `check-status` that the resolved root or child
    object auditing is `ON`.
11. Return `FIELD_ENABLEMENT_SUBMITTED_NOT_READ_BACK` for field verification.
    Treat the successful core response as evidence for the submitted update
    only, never as an independent read of the current enabled selection.

## Approval Contract

- Require a separate preview and approval for every resolved root or child.
- Bind approval to the exact environment, root context, resolved object,
  operation, payload, and fingerprint.
- Require approval immediately before the core mutation step.
- Never retry a live mutation automatically.
- Do not treat approval of a plan, another object, another environment, a
  prior payload, or a read-only call as mutation approval.
- Do not combine roots or children into one mutation or continue from one
  approved mutation to another without a separate preview and approval.

## Machine-Readable Outputs

Return applicable fields in a structured result:

- `operation`
- `root_object_key`, `object_scope`, `object_display_name`, `business_object`,
  `parent_business_object`, `parent_object_list`, `application`,
  `application_module`, `root_to_child_path`, and `inventory_status`
- `child_object_inventory` and `resolved_audit_object`
- `environment`
- `object_audit_status`
- `auditable_attribute_inventory`
- `enabled_attribute_result`
- `requested_attributes`
- `attribute_update_semantics`
- `preview_fingerprint`
- `execution_result`
- `verification_result`
- `diagnostics`
- `errors`

Redact tokens, authorization headers, client secrets, token-cache contents, and
sensitive environment configuration.

## Error and Recovery Contract

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `artifact_persistence`, or
`approval_blocker`.

- Fail before side effects for an unsupported root, unbound or ambiguous child,
  missing live `parentObjectList`, unsupported operation, empty attribute list,
  ambiguous or invalid attribute, stale preview, or missing approval.
- Permit the core capability to refresh a cache-managed token once after a
  rejected cached token. Do not replace an explicit token silently.
- Retry only bounded read-only transport failures through the core capability.
- Never retry `update-status` without a new preview and explicit approval.
- On an indeterminate mutation response, stop and report the environment,
  object, operation, payload fingerprint, known response details, and manual
  reconciliation path. Do not resubmit automatically.
- Do not attempt rollback by reconstructing a prior attribute selection; the
  API cannot retrieve that selection authoritatively. If a requested attribute
  must later be disabled, handle it as a separate explicit operation and
  approval rather than as compensation for this additive enablement.

## Persistence

When project context is supplied, persist the redacted preview, validation
result, execution result, verification result, diagnostics, and append-only
skill-run record under the declared workspace paths. Record the core skill run
reference and payload fingerprint. Do not persist attribute selections as an
authoritative baseline because later changes can occur outside this skill.

Append token usage using the manifest policy. Never persist OAuth tokens,
authorization headers, token-cache contents, client secrets, or raw sensitive
environment properties.

## Hierarchy Review Evidence

Review [the synthetic hierarchy scenarios](references/hierarchy-resolution-review.md)
when changing resolution rules. The linked inventories and structured expected
outcomes cover direct, nested, shared, cyclic, ambiguous, disconnected,
module-isolated, and incomplete hierarchies. This is reviewed evidence for the
declarative workflow; text-contract tests do not execute a resolver.

## Natural Prompts

- `Is audit enabled for Account?`
- `Check audit for Account and Contact.`
- `Check audit for Account, Contact, and Household.`
- `Enable audit for Contact.`
- `Enable audit for Household.`
- `Show attributes available for Account auditing.`
- `Which Contact attributes are currently enabled for audit?`
- `Enable audit for Account CEO Name.`
- `Enable DUNSNumberC and StockSymbol auditing for Account.`
- `List child objects available for Account auditing.`
- `Enable audit for Email Address on the Email child object of Contact.`
- `List child objects available for Household auditing.`

## Ownership and Review

- Owner: CX Sales pillar team.
- Functional reviewer: CX Sales Pillar Lead or Accounts, Contacts, and
  Households SME.
- Framework reviewer: FDOS A-Team/core reviewer.
- QA reviewer: required for root and child resolution, status, approval,
  attribute enablement, failure, and persistence behavior.
