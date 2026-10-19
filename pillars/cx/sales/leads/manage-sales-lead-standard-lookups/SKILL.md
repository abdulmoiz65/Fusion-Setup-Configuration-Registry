---
skill_id: "cx.sales.leads.manage-sales-lead-standard-lookups"
name: "Manage Sales Lead Standard Lookups Setup Task Guidance"
description: "Inventories Sales Lead standard lookup types and codes through exact Apps Common reads plus task-export reconciliation, and manages supported lookup-code create, update, disable, delete, and bulk-set operations through core.fusion-api.apps-common. Use for current code inventories and standard lookup-code CRUD. FSM export is never a mutation prerequisite, and Set ID lookup types remain outside this task."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Leads"
functional_area_code: "ORA_LDS_LEADS"
task_code: "MKL_MANAGE_SALES_LEAD_STANDARD_LOOKUPS"
task_name: "Manage Sales Lead Standard Lookups"
parent_skill_id: "cx.sales.leads"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.5.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "operation"
  - "lookup_type_optional"
  - "lookup_code_optional"
  - "proposed_code_attributes_optional"
  - "expected_current_state_optional"
  - "bulk_changes_optional"
  - "execution_approval_optional"
outputs:
  - "setup_task_plan"
  - "current_standard_lookup_export"
  - "standard_lookup_inventory"
  - "inventory_completion_evidence"
  - "documented_export_live_reconciliation"
  - "immutable_apps_common_preview"
  - "apps_common_execution_result"
  - "post_change_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/manage-sales-lead-standard-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/manage-sales-lead-standard-lookups/current/"
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
  - "Submits and downloads a task-level CSV export for Inventory and Review reconciliation."
  - "Reads standard lookup types, codes, and translations through core.fusion-api.apps-common."
  - "After an immutable preview and explicit approval, may create, update, disable, or delete a standard lookup code through core.fusion-api.apps-common."
  - "Persists inventory, preview, execution, verification, diagnostic, and token-usage artifacts in the implementation project workspace."
required_privileges:
  - "Privileges to export setup data for MKL_MANAGE_SALES_LEAD_STANDARD_LOOKUPS when Inventory or Review requires reconciliation."
  - "Oracle Applications Common privileges to read and manage standard lookup codes."
---

# Manage Sales Lead Standard Lookups Setup Task Guidance

## Purpose

Inventory and manage standard lookup codes surfaced by `Manage Sales Lead
Standard Lookups`. Use Oracle Sales guidance for candidate membership, a fresh
task export for Inventory/Review reconciliation, and exact live Apps Common
reads for current state. Route every supported lookup-code create, update,
disable, or delete through `core.fusion-api.apps-common`.

The catalog's FSM and CSV flags describe setup-data capabilities; they do not
select this task's lookup-code mutation route. Never require an exported parent,
build an FSM ZIP, invoke Data Loader, or request a reference ZIP for code CRUD.

## Runtime Interface

Apply the parent `cx.sales.leads` runtime guidance. Inventory and Review use the
task export plus read-only Apps Common lookups. AddCode, UpdateCode, DisableCode,
RemoveCode, and BulkSet load the Apps Common standard-lookups contract before
preflight and execution. Apps Common owns OAuth and HTTP transport; this task
owns business scope, exact identity, duplicate, state-lock, preview, approval,
safety, and verification gates.

Do not inspect or reproduce shared-client implementation during normal runtime.
If a documented interface fails, inspect only its owning contract and command
help. Do not substitute browser automation, Data Loader, a setup import, direct
curl, or task-local scripts.

## Sources and Scope

- [Sales Lead Lookups](https://docs.oracle.com/en/cloud/saas/sales/oasal/sales-lead-lookups.html)
  defines the Lead and Deal Registration candidate types.
- [Standard Lookups REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html)
  defines standard lookup type and code REST resources.
- `core/fusion-api/apps-common/references/lookups/standard-lookups.md` defines
  the shared execution contract.

This task manages codes only under an existing standard lookup type. It does
not create, update, or delete the lookup type definition. It does not write
translations because the Apps Common standard-lookups reference documents
translation reads only.

The eight Set ID types listed in `ora_reference_lookups.md` belong to Manage Set
Enabled Lookups and remain outside this graph.

## Intent Normalization

| User Intent | Operation | Required Behavior |
|---|---|---|
| List Sales Lead lookup types or current codes | Inventory | Attempt a fresh task export, then read the documented/exported live union and paginate every code collection |
| Review one exact type or code | Review | Attempt the export, then read the exact live type, code, and requested translations |
| Add a code | AddCode | Require exact parent existence and exact code absence, then preview a minimal child-collection POST |
| Change code attributes | UpdateCode | Require one exact current code and preview an exact child-item PATCH containing only changed mutable fields |
| Disable or end-date a code | DisableCode | Normalize to PATCH with an explicit EnabledFlag and/or EndDateActive delta and disclosed availability impact |
| Delete a code | RemoveCode | Require one exact customer-created code and deletion-impact evidence, then preview exact child-item DELETE; otherwise refuse and offer DisableCode |
| Change multiple codes | BulkSet | Preflight all Add/Update/Disable rows, preview ordered POST/PATCH calls together, approve once, execute sequentially, and stop on first failure |

Creating a lookup code supplies a value for an existing Lead field. It does not
create a new Lead attribute or page field.

## Mandatory Task-Control Contract

Load this manifest, compile and plan the task registry, and follow its reachable
nodes. Inventory and Review attempt the current-environment export before live
reconciliation. A successful export is intermediate, and omission does not
prove a type or code is absent.

For mutation, exact live Apps Common state is authoritative. Export success,
membership, customization state, or omission does not authorize or block a
write. Complete every validation, dependency, lookup, design, preview, and
approval gate before execution. Bind approval to the canonical environment,
exact type/code, normalized operation, method, relative endpoint, expected
state, body or delete effect, and complete preview digest. Re-read the target
immediately before the call; any drift invalidates approval.

Stop on systemic authentication, authorization, transport, pagination, or
response-shape failure. Never treat 401/403 as not-found and never retry a
mutating request at the task layer.

## Apps Common Lookup-Code CRUD Contract

Use relative paths through `core.fusion-api.apps-common`. Percent-encode
`LookupType` and `LookupCode`; use a returned item URI when Fusion supplies a
different canonical item path.

| Operation | Method | Endpoint | Body |
|---|---|---|---|
| Read codes | GET | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes` | None |
| Read one code | GET | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}` | None |
| AddCode | POST | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes` | `LookupCode`, `Meaning`, and only approved optional mutable fields |
| UpdateCode or DisableCode | PATCH | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}` | Only approved changed mutable fields; never resend keys |
| RemoveCode | DELETE | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}` | None |

Supported mutable code fields are `Meaning`, `Description`, `EnabledFlag`,
`StartDateActive`, `EndDateActive`, `DisplaySequence`, and `Tag`. `LookupCode`
is identity: include it only for POST and never change it. Never send
`LookupType`, `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`,
`LastUpdateLogin`, `ModuleId`, `CustomizationLevel`, `RestAccessSecured`, BOSS
fields, translation fields, or unrecognized attributes.

Do not use `Upsert-Mode=true` for normal CRUD. Exact pre-read state must choose
POST or PATCH deterministically. Allow only the shared client's documented
cached-token refresh behavior; never replay a write independently.

## Mutation Safety

- `AddCode` requires one exact existing standard parent and zero exact code
  matches immediately before preview and execution.
- `UpdateCode` and `DisableCode` require one exact current code and an unchanged
  expected-state fingerprint.
- `RemoveCode` requires positive evidence that the code is customer-created,
  not delivered or seeded, plus explicit disclosure of historical-reference,
  reporting, integration, and UI impact. Absence of delivered evidence is not
  proof of custom ownership. When positive evidence is unavailable, refuse
  DELETE and offer a reviewed DisableCode PATCH.
- A Meaning change requires translation inventory and disclosure that the base
  meaning is language-sensitive. Translation writes remain unsupported.
- Effective dates must be ordered. A past EndDateActive is allowed only when the
  preview clearly shows that the resulting code is already inactive.
- DisplaySequence is optional. When supplied, require a positive integer and
  disclose collisions without claiming the consuming UI must use that order.

Routine AddCode and UpdateCode do not require the user to supply a business
owner, affected-field narrative, or historical-use assessment. Ask for impact
evidence only when the requested DisableCode, RemoveCode, Meaning change, or
other availability change can affect existing references.

## Preview and Approval

The immutable preview must show the environment, task code, exact type/code,
source classification, normalized operation, method, relative endpoint, exact
current item or absence, proposed delta, availability/translation/delete impact,
minimal request body or bodyless DELETE, verification plan, ordered BulkSet
rows, stop-on-first-failure behavior, and a SHA-256 digest over the complete
canonical preview.

Stop for a later standalone approval bound to that digest. Immediately before
each call, re-read the parent, exact code or absence, and applicable impact
evidence. A changed type, code, state, body, method, endpoint, environment, or
preview requires a new approval.

## Inventory and Review

Inventory must reconcile the de-duplicated documented baseline plus exact
export-only types, excluding Set ID types. For every candidate, record exactly
one of resolved, not_found, or lookup_error; paginate every resolved code
collection and report attempted/resolved/not-found/error counts. Never return
the single-type export fixture as the complete inventory.

Review requires one exact type and optional exact code. Return current code
attributes and requested translations from live Apps Common reads. Export
failure is a disclosed reconciliation condition and does not block live Review.

## Export Boundary

Attempt automatic task export only for Inventory and Review reconciliation.
Use it to discover export-only types and annotate customization evidence. It is
not the authority for live existence or code CRUD and is never required for
AddCode, UpdateCode, DisableCode, RemoveCode, or BulkSet.

Do not build CSV rows or FSM packages, invoke `core.data-loader`, call shared
setup import, `setupTaskCSVImports`, UCM, or an import/initiation endpoint for
lookup-code mutation. A user-supplied ZIP is optional offline reconciliation
evidence only after an Inventory/Review export failure.

## BulkSet

Validate all rows before approval. Each row must have one unique
`LookupType`/`LookupCode` target and normalize to POST or PATCH from exact live
state. Execute approved rows sequentially in displayed order. Re-read and
verify each row around its call. Stop on the first stale-state, write, or
verification failure; never roll back earlier verified successes or continue
with later rows. Report verified successes, the failed row, and unattempted rows.

## Verification

After an Apps Common response, read the exact code immediately:

- AddCode succeeds only when the exact item exists and all approved fields
  match.
- UpdateCode and DisableCode succeed only when every approved changed field
  matches and immutable identity remains unchanged.
- RemoveCode succeeds only when the exact item is absent; use the parent code
  collection to disambiguate a 404 when necessary.
- BulkSet reports verification per attempted row.

HTTP acceptance without exact read-back is not completion.

## Failure and Recovery

Classify failures as input validation, task scope mismatch, authentication or
authorization, transport/environment, Fusion API, duplicate, ambiguous result,
stale state, approval blocker, delivered/custom safety, verification mismatch,
partial bulk completion, or artifact persistence.

Never retry POST, PATCH, or DELETE at the task layer. For an uncertain write,
reconcile the exact code before considering a new preview. Never issue an
automatic compensating write.

Apply the disclosure and refusal rules in
`ora-resource/ora_error_handling.md`. Redact and never print or persist
credentials, bearer tokens, authorization headers, client secrets, token-cache
content, private keys, full base64 payloads, unneeded protected identifiers,
or sensitive customer values. Persist only sanitized relative endpoints,
status, request ID or ECID, failure classification, and one safe next action.

## Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_design_enforcement.md`
5. `ora-resource/ora_error_handling.md`
6. `ora-resource/ora_rule_registry.json`

Use the parent `cx.sales.leads` skill for functional-area scope decisions.
Persist durable artifacts according to the manifest and never store credentials
or access-token contents.
