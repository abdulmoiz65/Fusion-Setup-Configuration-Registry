---
skill_id: "cx.sales.leads.manage-sales-lead-profile-options"
name: "Manage Sales Lead Profile Options Setup Task Guidance"
description: "Lists and reviews Sales Lead profile options and their configured Fusion environment values through a fresh FSM export plus exact Apps Common reads, and manages Site, Product, and User profile-option value CRUD through core.fusion-api.apps-common. Use for inventory, current/configured-value review, create, update, delete, or bulk-set requests. Never use FSM/Data Loader for profile-option value mutation or substitute Oracle defaults for environment values."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Leads"
functional_area_code: "ORA_LDS_LEADS"
task_code: "MKL_MANAGE_SALES_LEAD_PROFILE_OPTIONS"
task_name: "Manage Sales Lead Profile Options"
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
version: "0.9.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "operation"
  - "prior_turn_profile_option_code_optional"
  - "profile_option_code"
  - "profile_option_display_name_optional"
  - "profile_level"
  - "level_value_optional"
  - "user_name_optional"
  - "product_application_short_name_optional"
  - "expected_current_value"
  - "proposed_value_optional"
  - "bulk_changes_optional"
  - "execution_approval"
outputs:
  - "setup_task_plan"
  - "environment_access_evidence"
  - "current_profile_options_export"
  - "profile_option_inventory"
  - "inventory_completion_evidence"
  - "documented_export_reconciliation"
  - "normalized_operation"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/manage-sales-lead-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/manage-sales-lead-profile-options/current/"
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
  - "Reads configured and effective profile values through core.fusion-api.apps-common."
  - "After an exact immutable preview and explicit approval, may create, update, or delete a configured profile-option value through core.fusion-api.apps-common."
  - "Persists inventory, preview, execution, verification, diagnostic, and token-usage artifacts in the implementation project workspace."
required_privileges:
  - "Privileges to export setup data for MKL_MANAGE_SALES_LEAD_PROFILE_OPTIONS when Inventory or Review requires export reconciliation."
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV for profile-option value create, update, or delete."
  - "Read privileges for referenced Lead assessment templates, assignment rules, users, copy maps, and lookup values."
---

# Manage Sales Lead Profile Options Setup Task Guidance

## Purpose

Inventory and manage documented or environment-discovered Sales Lead profile
option values. Use current Oracle guidance for documented membership, a fresh
task export for reconciliation, and exact Apps Common reads for configured
state. Route every configured-value create, update, or delete through
`core.fusion-api.apps-common`. The `profileOptions` parent definition is
read-only; only Site, Product, and User value children are mutable.

The catalog's FSM and CSV flags describe task setup-data capabilities. They do
not select the mutation route for this skill. Never build or import an FSM ZIP
to change a profile-option value, and never ask the user to provide a reference
ZIP for CRUD.

## Runtime Interface

Apply the parent `cx.sales.leads` runtime-interface guidance. Inventory and
Review use the task export plus read-only Apps Common lookups. Create, Update,
Delete, Set, Remove, and BulkSet load the Apps Common profile-options contract
before preflight and execution. Apps Common owns OAuth and HTTP transport; this
pillar skill owns business identity, dependency, preview, approval, stale-state,
and verification gates.

If a declared interface rejects documented inputs, inspect only its owning
contract and command help. Do not scan implementation scripts broadly or
substitute browser automation, Data Loader, FSM import, or direct HTTP calls.

## Intent Normalization

| User Intent | Operation | Required Behavior |
|---|---|---|
| List all Sales Lead profile options or their configured values | Inventory | Resolve the selected environment, attempt a fresh task export, and complete the documented/exported live-read union |
| Review one exact code or ask its current/configured value | Review | Reuse one exact immediate-context code when unambiguous, attempt the export, and read the exact definition and all value children |
| Create or set a value when the selected child row is absent | Set → Create | Require explicit `not configured` expected state and use child-collection POST after preview and approval |
| Update or set a value when the selected child row exists | Set → Update | Lock the exact current value and use exact child-item PATCH after preview and approval |
| Delete, remove, or reset one configured value | Remove → Delete | Show fallback impact, lock the exact row, and use exact child-item DELETE after preview and approval |
| Set multiple values | BulkSet | Preflight every row, preview the ordered POST/PATCH calls together, approve once, then execute sequentially and stop on first failure |
| Ask only for Oracle's delivered default | Documentation advisory | Label the result as delivered behavior; never call it current or configured |

Treat an active Sales implementation project as environment context. Do not ask
the user to repeat an environment already selected by the project or configured
Fusion context. A current/configured/system request cannot be completed from
documentation or export rows alone.

## Mandatory Task-Control Contract

Load this manifest, compile and plan the task registry, and follow its reachable
nodes. For Inventory, a successful export is intermediate: continue to live
definition, level, Site, User, and Product reads for the documented/exported
candidate union. For Review, require the same exact child evidence for the one
selected code.

For mutation, exact live Apps Common state is authoritative. Export success,
membership, or omission does not authorize or block CRUD. Complete every
validation, dependency, lookup, design, and preview gate before asking for
approval. Bind approval to the canonical environment, method, endpoint, exact
identity, expected state, body or delete effect, and preview digest. Re-read the
target immediately before the write; any drift invalidates approval.

## Supported Operations

- `Inventory`: attempt a fresh task export, refresh the documented candidate
  set, probe every documented and export-only code through exact Apps Common
  reads, and report configured values, enabled/updatable levels, and source
  classification.
- `Review`: resolve one exact code and show configured Site, User, and Product
  values, level flags, stored-value meaning, and optional effective value.
- `Set`: normalize to Create when the exact child row is absent and Update when
  it exists. Use Apps Common POST or PATCH respectively.
- `Remove`: delete the one exact configured child row through Apps Common after
  disclosing the lower-precedence or delivered behavior that will apply.
- `BulkSet`: execute an approved ordered list of independent POST/PATCH calls.
  Stop on the first failure, do not roll back successful earlier rows, and
  report partial completion explicitly.

Site, Product, and User values are eligible only when the selected level is
enabled and updatable. Product uses an exact application short name as
`LevelValue`. User uses an exact `UserName` item key and a separately resolved
`UserGuid` in the create body. Parent profile definitions, validation SQL,
level metadata, descriptions, and audit fields remain read-only.

## Apps Common CRUD Contract

Use relative endpoints through `core.fusion-api.apps-common` and its shared
REST client. Percent-encode every path key. Never form a URL from a display
label.

| Level | Read collection | Create | Update item | Delete item |
|---|---|---|---|---|
| Site | `/fscmRestApi/resources/11.13.18.05/profileOptions/{code}/child/siteProfileOptionValues` | POST collection with `ProfileOptionValue` | PATCH the collection path plus `/SITE` | DELETE the collection path plus `/SITE` |
| Product | `/fscmRestApi/resources/11.13.18.05/profileOptions/{code}/child/productProfileOptionValues` | POST collection with `LevelValue` and `ProfileOptionValue` | PATCH the collection path plus `/{applicationShortName}` | DELETE the collection path plus `/{applicationShortName}` |
| User | `/fscmRestApi/resources/11.13.18.05/profileOptions/{code}/child/userProfileOptionValues` | Resolve `/fscmRestApi/resources/11.13.18.05/profileUsers/{UserName}`, then POST collection with `LevelValue={UserGuid}` and `ProfileOptionValue` | PATCH the collection path plus `/{UserName}` | DELETE the collection path plus `/{UserName}` |

Use only the intended writable fields. Do not send audit columns or parent and
level metadata. Do not use `Upsert-Mode=true` for a normal Create/Update route:
the pre-read must choose POST or PATCH explicitly. Do not retry a mutating call
at the task layer. Allow only the shared client's documented cached-token
refresh behavior; never replay a write independently.

## Preview and Approval

The immutable preview must show:

- canonical environment and task code;
- exact profile-option code, level, and Site/Product/User key;
- normalized CRUD operation, HTTP method, and relative endpoint;
- exact current row or explicit absence;
- proposed stored value and resolved meaning for Create/Update;
- fallback effect for Delete;
- dependency and level-capability evidence;
- canonical request body, or explicit no-body Delete;
- ordered row list and stop-on-first-failure behavior for BulkSet; and
- a SHA-256 digest over the complete canonical preview.

Stop for a later standalone approval. Approval is valid only for that complete
preview digest. Before execution, re-read the definition, level capability,
selected child row, identity dependency, and stored-value dependency. A changed
row, method, endpoint, body, target, or environment requires a new preview and
approval.

## Inventory and Review Completion

Inventory is complete only when the artifact records documented candidates,
export-only candidates, live attempted/resolved/not-found/error counts, one
result or explicit status for every candidate, complete paginated Site/User/
Product child reads, level flags, timestamps, and
`ORA_MKL_LEAD_CONVERT_TO_EXISTING_OPTY` whenever its definition resolves.

Review is complete only with canonical environment identity, exact code, export
attempt status, live definition, live level capabilities, complete Site/User/
Product rows or explicit absence, and lookup timestamps. Never infer User or
Product values from Site or substitute `profileValues` for configured rows.

## CSV Export and Reconciliation

For Inventory and Review, attempt automatic export with
`shared.setup-export.task-level-export` before asking for any offline evidence.
Use the export to discover export-only codes and reconcile task scope, not as
the authority for configured values. Export failures do not block exact live
Inventory or Review; disclose them and continue. A user-supplied ZIP is optional
offline reconciliation evidence only after automatic export fails.

Do not run task export, construct CSV rows, build an FSM ZIP, invoke
`core.data-loader`, or call a setup import for Create, Update, Delete, Set,
Remove, or BulkSet. Mutation readiness depends on exact live Apps Common
evidence, not FSM customization state.

## Stored-Value Dependencies

- For assessment-template options, resolve the name to one active/deployed Lead
  `AssessTemplateId`; store the numeric ID, never the template name.
- For lookup-backed options, resolve an exact active stored code or one exact
  active meaning to its code; show both and send only the code.
- For assignment rules, require the exact published Lead rule-set-group code.
- For Copy Maps, require the exact map name for the intended route.
- For approver values, require the exact valid user or role identifier.
- For User scope, resolve one exact `UserName` to one `UserGuid`; never use the
  display name or Site key as the GUID.

## Verification

After a successful Apps Common mutation response, perform a fresh exact child
read in the same run:

- Create/Update succeeds only when the exact item exists and its stored value
  equals the approved proposed value.
- Delete succeeds only when the exact item is absent; a collection read may be
  used to disambiguate a 404.
- BulkSet reports each verified row and stops on the first write or verification
  failure without retry or compensation.

Read `profileValues` only as optional effective-session verification. Report
configured success separately because session-effective behavior can require a
new sign-in and the effective resource can omit secured categories.

## Failure and Recovery

Classify failures as input validation, catalog mismatch, authentication or
authorization, transport/environment, Fusion API, stale state, approval
blocker, verification mismatch, partial bulk completion, or artifact
persistence. A 401/403 is not absence; a 404 on an exact pre-read is absence
only when the collection and expected operation make that interpretation
unambiguous.

Never retry POST, PATCH, or DELETE at the task layer. For an uncertain write,
reconcile the exact child item before considering a new preview. Never issue a
compensating write automatically.

Apply the disclosure and refusal rules in
`ora-resource/ora_error_handling.md`. Redact and never print or persist
credentials, bearer tokens, authorization headers, client secrets, token-cache
content, private keys, full base64 payloads, user GUIDs when they are not
required for review, or sensitive customer values. Persist only sanitized
relative endpoints, status, request ID or ECID, failure classification, and one
safe next action.

## Task-Local Rule Workflow

Compile and follow `ora-resource/ora_rule_registry.json`. The task graph may
return an environment-backed Inventory/Review result or a validated Apps Common
CRUD preview. The graph never authorizes an unapproved write, FSM/Data Loader
mutation, browser fallback, profile-definition change, or cross-task action.

## Oracle and Repository Sources

- [Sales Lead Profile Options](https://docs.oracle.com/en/cloud/saas/sales/oasal/sales-lead-profile-options.html)
- [Overview of Profile Options](https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-profile-options.html)
- [Why Aren't All Ready-to-Use Setup Data Exported?](https://docs.oracle.com/en/cloud/saas/applications-common/25c/oafsm/why-aren-t-all-ready-to-use-setup-data-exported.html)
- [Profile Values REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-profile-values.html)
- `core/fusion-api/apps-common/references/profile-options.md`
- `shared/setup-export/task-level-export/SKILL.md`

## Implementation Notes

Use `cx.sales.leads` for functional-area sequencing. Track token usage for any
generated project artifact or skill-run record using the manifest policy.
