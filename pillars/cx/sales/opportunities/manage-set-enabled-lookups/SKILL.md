---
skill_id: "cx.sales.opportunities.manage-set-enabled-lookups"
name: "Manage Set Enabled Lookups Setup Task Guidance"
description: "Maintains the two owned Opportunity set-enabled lookups through exact-task CSV, omitted-parent recovery, or separately approved Apps Common REST, with a final governed fallback when CSV recovery is exhausted."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "FND_MANAGE_SET_ENABLED_LOOKUPS"
task_name: "Manage Set Enabled Lookups"
parent_skill_id: "cx.sales.opportunities"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.7.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "request_mode"
  - "lookup_type"
  - "lookup_operation"
  - "lookup_code"
  - "lookup_attributes"
  - "set_selection_decision"
  - "reference_data_set_identity"
  - "fusion_environment_context"
  - "expected_current_state"
  - "execution_route"
  - "package_task_context"
  - "package_evidence"
  - "business_impact_evidence"
  - "rest_execution_approval_optional"
  - "csv_failure_receipt_optional"
  - "csv_recovery_evidence_optional"
  - "prior_submission_reconciliation_optional"
  - "reviewed_rows_optional"
  - "task_context_path_optional"
  - "task_sequence_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "resolved_lookup_parent"
  - "resolved_reference_group"
  - "resolved_lookup_contract"
  - "catalog_task_code"
  - "record_set_prerequisite_task_code"
  - "execution_task_code"
  - "current_lookup_state"
  - "package_readiness_result"
  - "immutable_change_preview"
  - "data_loader_handoff_result"
  - "lookup_execution_result"
  - "rest_fallback_routing_optional"
  - "post_change_verification"
  - "diagnostics"
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
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-set-enabled-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-set-enabled-lookups/current/"
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
  - "Reads Opportunity set-enabled lookup types, reference data sets, and lookup codes through core.fusion-api.apps-common."
  - "May hand an exact immutable FND_MANAGE_SET_ENABLED_LOOKUPS package to core.data-loader, which owns its approval preview and later standalone approval before import."
  - "May use direct REST only when the requester explicitly selects that route and separately approves its exact immutable REST preview."
  - "May select REST_FALLBACK for Create, Update, or Disable only after applicable CSV recovery is exhausted and prior submissions are reconciled; requires its own immutable preview and immediate approval."
  - "Treats an accepted Core Data Loader initiation as terminal; status, ProcessLog retrieval, and live verification occur only on a later explicit request."
  - "Persists preview, handoff, execution, requested verification, diagnostic, and token-usage artifacts in the implementation project workspace."
required_privileges:
  - "Fusion privileges appropriate to view or manage the selected set-enabled lookup type and reference data set."
  - "Privileges to export or import FND_MANAGE_SET_ENABLED_LOOKUPS when the approved FSM route is selected."
  - "Apps Common REST write privileges for each selected lookup operation; readable parent metadata does not establish write permission."
---

# Manage Set Enabled Lookups Setup Task Guidance

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may be generated from the project's resolved setup-task
plan without creating an Oracle Run Book. Never hand-author, infer, or
synthesize a context entry merely to satisfy Data Loader.

## Purpose

Define the common Opportunity set-enabled lookup inventory, validation,
approved maintenance, verification, and task CSV pattern. This manifest also
owns the exact `FND_MANAGE_SET_ENABLED_LOOKUPS` route for the two generic
Opportunity lookup types listed below.

## Setup Task Skill Contract

- task_code: FND_MANAGE_SET_ENABLED_LOOKUPS
- task_name: Manage Set Enabled Lookups
- parent_skill_id: cx.sales.opportunities
- pillar: CX
- offering: Sales
- functional_area: Opportunities
- functional_area_code: ORA_MOO_OPPORTUNITIES
- available_flag: Y
- export_import_supported_flag: Y
- csv_export_import_supported_flag: Y
- dataloader_import_mode: FSM
- businessObject: blank
- source_catalog: knowledge/setup-task-catalog/effective/setupTasksAll.json

## Common Workflow and Exact Task Dispatch

All eight Opportunity set-enabled lookup types use the same Apps Common
parent-first discovery, reference-group-driven set resolution, validation,
preview, approval, execution, diagnostics, and verification discipline. Task
Hook selection is still exact: a named setup task must load its own adapter and
use its own FSM package task code.

| Business value | Lookup type | Exact adapter | FSM execution task code | Record-set prerequisite task code |
|---|---|---|---|---|
| Level of Risk | MOO_SETID_RISK_LEVEL | [manage-levels-of-risk](../manage-levels-of-risk/SKILL.md) | MOO_MANAGE_LEVELS_OF_RISK | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Strategic Value | MOO_SETID_STRATEGIC_VALUE | [manage-strategic-values](../manage-strategic-values/SKILL.md) | MOO_MANAGE_STRATEGIC_VALUES | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Decision Level | MOO_SETID_DECISION_LEVEL | [manage-decision-levels](../manage-decision-levels/SKILL.md) | MOO_MANAGE_DECISION_LEVELS | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Estimated Deal Duration | MOO_SETID_DEAL_HORIZION | [manage-deal-horizons](../manage-deal-horizons/SKILL.md) | MOO_MANAGE_DEAL_HORIZONS | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Win/Loss Reason | MOO_SETID_WIN_LOSS_REASON | [manage-win-loss-reasons](../manage-win-loss-reasons/SKILL.md) | FND_MANAGE_SET_ENABLED_LOOKUPS | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Sales Revenue Type | MOO_SETID_REVENUE_TYPE | [manage-opportunity-revenue-types](../manage-opportunity-revenue-types/SKILL.md) | MOO_MANAGE_REVENUE_TYPES | ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES |

This `FND_MANAGE_SET_ENABLED_LOOKUPS` adapter directly supports only:

| Business value | Lookup type | FSM task code | Record-set prerequisite task code |
|---|---|---|---|
| Opportunity Assessment Override Reason | MOO_SETID_ASSESS_OVRRIDE_RSN | FND_MANAGE_SET_ENABLED_LOOKUPS | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Sales Revenue Category | MOO_SETID_REVN_CATEGORY | FND_MANAGE_SET_ENABLED_LOOKUPS | ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES |

Do not route the named setup tasks through this manifest's catalog identity or
rule graph. Their adapters reuse this common pattern but own their task-local
catalog identity, rule graph, readiness, route gate, diagnostics, and evidence.
`Manage Win/Loss Reasons` is the transport exception: its catalog code remains
`MOO_MANAGE_WIN/LOSS_REASONS`, while its adapter exports and imports an
`FND_MANAGE_SET_ENABLED_LOOKUPS` archive scoped to
`MOO_SETID_WIN_LOSS_REASON` because the catalog code contains `/`. The other
named adapters retain their listed FSM execution task code. A named adapter
owns a REST preview and approval only for its documented REST exception; Core
Data Loader owns every FSM preview and later standalone approval. This FND
adapter supports explicitly selected REST Create, Update, Disable, or Delete
for its two directly owned types. Named adapters normally narrow that exception
to REST Delete only. `Manage Win/Loss Reasons` additionally permits direct REST
Create, Update, and Disable only after its own task-local rules verify that the
same-target FND export failed or timed out; that fallback remains owned by the
named adapter and bypasses Data Loader.

Treat MOO_SETID_DEAL_HORIZION and MOO_SETID_ASSESS_OVRRIDE_RSN as exact Oracle
codes, including their published spelling.

## Explicit Exclusions

Do not route these tasks or lookup types through this skill:

- Manage Sales Status: dedicated sales-status contract and approval workflow.
- Manage Sales Stage Phase Codes: standard lookup MOO_STAGE_PHASE_CD.
- Manage Opportunity Revenue Categories: current task-specific standard lookup
  contract for MOO_REVN_CATEGORY. Do not substitute MOO_SETID_REVN_CATEGORY
  without an explicit generic set-enabled lookup request.
- Manage Sales Methods and Sales Stages: set-assigned master data, not a
  set-enabled lookup-code task.
- Sales Status Category Mappings: mapping matrix, not lookup maintenance.
- Manage Opportunity Record Set Values
  (`ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES`): assigns reference data sets
  to Opportunity usage and is not lookup-code maintenance.
- Manage Revenue Record Set Values
  (`ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES`): assigns reference data sets to
  Revenue usage and is not lookup-code maintenance.

This skill may read a record-set assignment to resolve the selected set. If the
required assignment is absent or incorrect, stop and return the exact owning
record-set task code as a prerequisite gap. Do not create or update the
assignment through this skill.

A request outside the supported table is unsupported until current Oracle
documentation or exact target export evidence establishes the Opportunity
lookup type and owning task. Do not infer a lookup type from a display label.

## Supported Operations

| Operation | Behavior |
|---|---|
| Inventory | In single-lookup mode, resolve one exact parent and set, then return all matching codes with sanitized current state |
| Read | In single-lookup mode, resolve one exact lookup code in one exact set without mutation |
| Create | Default to FSM and require an export-derived row delta with an absent-code state lock; direct REST is allowed only when explicitly selected and separately approved |
| Update | Default to FSM and require an export-derived row delta with an exact before-state lock; direct REST is allowed only when explicitly selected and separately approved |
| Disable | Default to FSM and require an export-derived row delta that changes only `EnabledFlag` to `N`; direct REST is allowed only when explicitly selected and separately approved |
| Delete | Never encode deletion in FSM. Permit only an explicitly selected direct REST route when the returned item link, current metadata, impact evidence, immutable preview, and separate approval all support it |
| Export | Export the complete FND_MANAGE_SET_ENABLED_LOOKUPS task through shared.setup-export.task-level-export; a selector or LookupCode isn't required and the result may contain both owned types and multiple rows |
| Import | Validate every changed row and set in one immutable FND_MANAGE_SET_ENABLED_LOOKUPS package, then hand it to core.data-loader for its Task Hook preview and later standalone approval |

Do not silently convert Create to Update, Update to Create, Disable to Delete,
or one lookup type to another.

The default FSM route supports Create, Update, and Disable only; its final
CSV-exhaustion fallback is defined below. An explicit
direct REST route can support one Create, Update, Disable, or Delete when the
documented endpoint and current target evidence pass all REST gates. Delete is
REST-only. Never infer REST from a generic mutation request.

Use `SingleLookup` request mode for Inventory, Read, or one direct REST
mutation. Use `Package` mode for Export, Import, an FSM change package, or the
reviewed ordered row list of an eligible `REST_FALLBACK`. A
package may contain both lookup types owned here and multiple rows. Apply
single-selector and single-code requirements only to `SingleLookup`; validate
the exact type, set, code, operation, current state, and proposed state on every
changed package row instead.

## Execution Safety Contract

Before any external read, export, package handoff, supported direct REST
preview, or mutation, run a preflight that validates the exact environment,
task identity, request mode and route, privileges, selectors, current-state
evidence, package or endpoint shape, destination paths, and route-owned
approval state. Stop before side effects when evidence is missing, stale,
ambiguous, cross-environment, or inconsistent with the task-local resources
and compiled rule plan.

For error handling and failure behavior, load
`ora-resource/ora_error_handling.md`, classify the failure under the governed
taxonomy, preserve sanitized diagnostics and external identifiers, and follow
only the documented recovery path. Retry cached-token authentication at most
once through the owning core client and retry only bounded read-only transport
failures. Never retry a live REST mutation, Data Loader import, upload, or
uncertain result without a fresh immutable preview and explicit approval. On a
timeout or accepted Data Loader initiation, return the current status and safe
next-check path instead of polling or resubmitting automatically.

Redact credentials, bearer tokens, authorization headers, OAuth state,
token-cache contents, cookies, private keys, and sensitive payload values.
Never print or persist those secrets in previews, diagnostics, project
artifacts, skill-run records, or user responses.

## Oracle Resource Read Order

Load these task-local resources before validation, preview, or execution:

1. [ora_input_validation.md](ora-resource/ora_input_validation.md)
2. [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
3. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
4. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
5. [ora_error_handling.md](ora-resource/ora_error_handling.md)
6. [ora_rule_registry.json](ora-resource/ora_rule_registry.json) for the compiled task-node graph

Load the mandatory task-node execution guide returned by the rule planner
before consuming the registry. Treat the Markdown resources as the source of
validation, lookup, design, and error behavior; never hand-edit the registry.

## Set ID Selection

Never default a set-enabled Opportunity request to Common Set. For a
`SingleLookup` request without an exact set selector, stop and ask whether the
Common Set should be used or a different set should be selected. If Common Set
is confirmed, resolve its current `SetId` and `SetCode` through the documented
read-only set resolver; do not hard-code them. Otherwise require a different
exact Set ID or Set Code, or a business-unit/organization selector that resolves
to exactly one set. For Package mutations, preserve each exported row's set and
require an explicit decision for every new row that lacks one. Common Set
confirmation is a scope decision, not REST or Data Loader approval.

Validate SetId as an integer resolved in the selected environment. A confirmed
Common Set can resolve to zero; use the returned SetId and SetCode without
hard-coding an ID or inferring a set from its number.

## Negative Set Scenarios

| Scenario | Required result |
|---|---|
| Set ID or Set Code is malformed, unknown, or not found in the selected environment | Stop before code lookup or preview; request a valid exact set identity |
| Set ID and Set Code resolve to different sets, or multiple supplied selectors are not proven equivalent | Reject the conflicting identity; never choose one selector silently |
| Common Set is confirmed but the resolver returns another set | Reject and ask the user to reconfirm Common Set or provide one different exact set |
| Business-unit/organization assignment has a different ReferenceGroupName or set | Block and return the exact record-set prerequisite gap; do not repair the assignment here |
| Lookup type, set, code, package row, or fresh-export identity disagree | Reject the request/package as a catalog or scope mismatch; do not substitute a generic task, close match, or Common Set |

## Required Request

Collect or derive all fields applicable to the selected request mode and route:

- `request_mode` (`SingleLookup` or `Package`), exact target environment, and
  supported `lookup_operation`;
- for `SingleLookup`, one exact supported `lookup_type`, an explicit decision
  to use Common Set or another set, one resolvable set selector, and
  `lookup_code` for every code-specific operation;
- for Create or Update, only the intended mutable attributes; apply the
  universal field constraints and preserve lookup type, lookup code, set, and
  other immutable identity fields;
- catalog and execution task code fixed to
  `FND_MANAGE_SET_ENABLED_LOOKUPS`, plus the owning record-set prerequisite for
  every affected lookup type;
- for Package Export, exact task and target context only; do not demand a
  single selector or code;
- for Package Import or an FSM Create, Update, or Disable, a fresh same-target
  export baseline, immutable package path and SHA-256, exact metadata task
  identity, member inventory, exact exported headers, per-row type and set,
  proposed row delta, business impact, and a fresh current-state lock for every
  changed row; and
- for direct REST, the explicit REST route, exact method, returned item link
  when the item exists, exact request body or bodyless Delete, `Upsert-Mode:
  false` for Create, current-state and impact evidence, immutable preview
  fingerprint, and approval bound to every displayed value.

For FSM, hand the completed immutable package to `core.data-loader`. Data
Loader owns Task Hook validation, the upload preview, and the later standalone
`approve`. `rest_execution_approval_optional` applies only to a direct REST
preview; never reinterpret it as Data Loader approval.

Apply `ora_input_validation.md` and stop on every missing or invalid required
value. Use only FND_MANAGE_SET_ENABLED_LOOKUPS for an FSM package.

## Execution Route

### Read-Only Discovery

1. Load core/fusion-api/apps-common/SKILL.md and
   core/fusion-api/apps-common/lookups/SKILL.md and its
   references/set-enabled-lookups.md.
2. GET each affected lookup parent first and capture its returned nonblank
   `ReferenceGroupName`. Never assume that `ReferenceGroupName` equals
   `LookupType`.
3. Resolve every set and any requested business-unit assignment by using that
   returned `ReferenceGroupName`. Stop when the parent omits it or the set or
   assignment is absent, ambiguous, or inconsistent.
4. For each code, resolve zero or one exact child item in that set. Use the
   returned child identifier or item URL; never guess an item key from
   LookupCode.
5. Apply the compiled validation, reference-lookup, dependency, and design
   rules from the task-local resources. Read-only calls must not mutate the
   lookup.

### Default FSM Route for Mutations

Use this route for Create, Update, and Disable only. Stop a Delete request
before package preparation and offer Disable or the explicitly selected direct
REST exception when its requirements can be satisfied.

1. Use FND_MANAGE_SET_ENABLED_LOOKUPS as the only package task code.
2. Obtain a fresh completed export from the exact target and release. Preserve
   its package bytes, exact task identity, SHA-256, metadata descriptor, member
   names, and exact header spelling and order. This export step does not require
   Data Loader task context.
3. Build the smallest package delta without changing metadata, headers,
   unrelated members, unrelated rows, or immutable identity columns. A package
   may contain both owned lookup types and multiple rows, but each changed row
   must independently resolve to an owned type, returned reference group,
   exact set, supported Create/Update/Disable operation, fresh state lock, and
   reviewed impact. Apply the omitted-parent recovery below before handoff;
   header-only or partially omitted seeded lookup data is not an export failure.
4. Reopen the final package and validate safe ZIP shape, exact case-sensitive
   `ASM_SETUP_CSV_METADATA.xml`, one metadata task identity, member inventory,
   headers, row counts and row delta, same-target task identity, and SHA-256.
5. For the mutation handoff, resolve persisted `TaskContextPath`, exact
   `TaskName`, and positive `TaskSequence` to this exact skill path, `TaskCode`,
   offering, and functional area. Hand that context with the exact environment,
   task identity, immutable package path and hash,
   member/header summary, proposed rows, state locks, and impact evidence to
   `core.data-loader`.
6. Let Data Loader validate the unchanged package, invoke Task Hook, and build
   its immutable approval preview. Follow its current later contextual approval
   lifecycle; this child does not prescribe a literal approval keyword.
7. After that approval, let Data Loader submit the approved immutable source once. A Fusion
   accepted initiation result is terminal for that request. Do not poll, fetch
   a ProcessLog, or verify live state in the same request.
8. Run status, ProcessLog retrieval, or exact live verification only after a
   later explicit user request. Never reuse a Data Loader approval for REST or
   vice versa.

### Header-Only or Partially Omitted CSV Baselines

Validate a completed full-data FND_MANAGE_SET_ENABLED_LOOKUPS export's exact
target, release, task, process result, ASM metadata, members, and headers.
Seeded lookup rows can be omitted even when other lookup types are exported;
zero rows or omission of an owned type alone does not invalidate that baseline
or prove live absence.

For each affected owned type, resolve its exact live parent and returned
reference group, confirmed sets, editability, and each requested code state.
Preserve the original ZIP and build a separate final package. Reuse an existing
exported parent when it matches fresh live metadata. If omitted, add exactly
one unchanged parent linkage row per affected type in
FND_APP_SET_ENABLED_LOOKUP.csv, using live LookupType, ReferenceGroupName,
Meaning, Description, ModuleId, CustomizationLevel, and RestAccessSecured only
where present in the exported header; leave added audit fields blank.

Every changed ORA_FND_APP_SET_ENABLED_LOOKUP_CODE.csv row must join through
FND_APP_SET_ENABLED_LOOKUP.LookupType to its matching parent and use the exact
resolved SetCode. The two-type case needs two support parents and the reviewed
code additions, not copies of all seeded codes. Support rows are disclosed as
unchanged linkage, not parent configuration changes. Preserve unrelated
exported parents/codes, ASM metadata, archive members, and exact headers. A
child-only package or conflicting live/exported parent fields blocks handoff.

### Final Apps Common Fallback

Keep exact-task CSV and applicable omitted-parent recovery first. The
dependency verifier returns RETURN_FALLBACK_REQUIRED only when Create, Update,
or Disable cannot complete through that route. The invoking router resumes
the unchanged request once as REST_FALLBACK, restarts fresh parent/set/code
resolution, and uses verify_set_lookup_rest_fallback before preview. This does
not replace the separately requester-selected SingleLookup REST route.

Require a same-target/release/task/type/row/set failure receipt, recovery
outcomes and why further CSV recovery is unavailable, actual statuses,
timestamps, safe artifact refs/hashes and all returned external IDs. Permitted
reasons are EXPORT_FAILED, EXPORT_TIMEOUT after the declared polling window,
UNUSABLE_EXPORT after applicable recovery, CSV_IMPORT_FAILED, or
CSV_IMPORT_NO_EFFECT. Do not submit an invalid ZIP or repeat an import to prove
exhaustion. Missing input, catalog/workflow/context, set/assignment, auth/authz,
approval, explicit FSM-only constraints, and repairable CSV remain blockers.

After an accepted import, evaluate failure only on a later explicit results
request through Core Data Loader status/errors/ProcessLog retrieval. Every
related import job must be terminal and every requested row must still match
its reviewed pre-state or be absent for Create. Pending jobs, uncertain upload
or initiation, incomplete diagnostics, partial application and concurrent
state changes block fallback. Return verified state without another write when
all requested values are applied; partial results need a new reviewed request
for the remaining changes.

An eligible fallback uses Apps Common -> Lookups with the existing exact
set-enabled resolvers. Preserve each reviewed row's owned type and confirmed
set, reject duplicate type/code/set identities, and retain preview order.
Prepare one immutable REST preview containing the failure/recovery evidence,
target, every operation/type/code/set, before/after state, impact, exact method,
endpoint/body, verification GET and fingerprint. For Create use collection
POST with resolved integer SetId, LookupCode, Meaning and reviewed writable
fields, Upsert-Mode=false, and no read-only SetCode or audit fields. For Update
or Disable use the fresh same-target canonical child link and minimal PATCH;
Disable changes only EnabledFlag=N. Never write parents or assignments.

Obtain separate explicit approval immediately before REST execution. No FSM
approval, Data Loader session, ZIP, task context, or loader capability lookup
is reused or required for an already eligible fallback; a missing context is
never its trigger. Submit each request once through the core REST client,
verify immediately, and stop at the first failure, uncertainty or unverified
result. Preserve successes and unattempted rows without retry or rollback.
Export/Import remain FSM-only and Delete retains its explicit REST contract.

Oracle sources: [26D CSV export/import](https://docs.oracle.com/en/cloud/saas/applications-common/26d/oafsm/using-functional-setup-manager.pdf#page=37)
and [26D Set-Enabled Lookup Codes](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/api-set-enabled-lookups-lookup-codes-adf.html).

### Explicit Direct REST Route

Use direct REST only when the requester explicitly selects REST and the
current task contract and target metadata support the named operation. This is
the only route that may perform Delete.

1. Resolve the parent, returned `ReferenceGroupName`, set or business-unit
   assignment, and exact current child state through fresh GET requests.
2. Bind one immutable preview to the target environment, task and lookup
   identities, set, operation, before and after states, business impact,
   verification GET, and exact method, returned item link, and body.
3. For Create, use collection POST with the exact code, set, and intended
   mutable fields and explicitly send `Upsert-Mode: false`; never silently
   upsert. For Update or Disable, PATCH the returned child item link and include
   only intended mutable fields. For Delete, DELETE the returned item link with
   no body.
4. Reject any attempt to change `LookupType`, `LookupCode`, `SetId`, `SetCode`,
   `ReferenceGroupName`, module, audit, seed, or returned resource identity.
5. Obtain separate explicit approval immediately before execution, verify that
   every preview value and its fingerprint are unchanged, submit exactly once
   without automatic retry, and perform the disclosed exact GET verification.

Never infer REST from a generic mutation request, reuse an FSM approval, guess
an item URL from `LookupCode`, or set upsert mode to true.

The FND_MANAGE_SET_ENABLED_LOOKUPS task may package both lookup types owned by
this adapter only when every row has an exact type and set and the complete
package is reviewed. It must not package rows owned by one of the six named
task adapters.

## Execution Result

Return a machine-readable result containing:

- skill_id;
- task_code and task_name;
- catalog_task_code and execution_task_code, both fixed to
  FND_MANAGE_SET_ENABLED_LOOKUPS, plus record_set_prerequisite_task_code
  derived for each affected lookup type;
- lookup_type and business value;
- operation and execution route;
- target environment, resolved parent, returned reference group, and resolved
  set identity;
- current state and proposed state;
- package-readiness result or REST preview fingerprint and route-specific
  approval status;
- Data Loader handoff or direct REST execution outcome and safe request
  identifier when available;
- accepted initiation as the terminal FSM result, or post-change verification
  only when direct REST completed or a later explicit verification was
  requested;
- diagnostics, partial or uncertain side effects, and one safe next action;
- durable artifact and skill-run references when project_id is supplied.

## Failure Discipline

Load `ora_error_handling.md` before preview or execution and apply its
classification, disclosure, refusal, and retry rules.

Classify failures as input validation, catalog mismatch, authentication or
authorization, transport or environment, Fusion API, process timeout, process
failed, artifact persistence, or approval blocker.

Refresh a rejected cached OAuth token at most once through the core client.
Do not treat 401 or 403 as proof that a lookup is absent. Do not retry a live
mutation or import after a failure or uncertain result. Reconcile a direct
REST result with one exact read when safe. For an accepted Data Loader
initiation, return immediately and do not call status or verification in the
same request.

On a later explicit FSM status or results request, use Data Loader's status
workflow. If that later request times out, report the environment,
FND_MANAGE_SET_ENABLED_LOOKUPS, ProcessId or requestId, last status, elapsed
wait, and next-check path. Retrieve a sanitized ProcessLog or status payload
only in that later workflow when available. Represent partial progress with a
non-success status and an errors array. Any replacement mutation requires a
new immutable preview or package and fresh route-specific approval.

Never print or persist credentials, bearer tokens, authentication headers,
opaque protected URLs, or sensitive payload values.

## Setup Task Metadata

- Coordinator task name: Manage Set Enabled Lookups
- Coordinator task code: FND_MANAGE_SET_ENABLED_LOOKUPS
- Offering: Sales
- Functional area: Opportunities
- Export/import supported: Y
- CSV export/import supported: Y
- Data Loader mode: FSM

## Source References

- [Set-ID-Enabled Predefined Data for Opportunities](https://docs.oracle.com/en/cloud/saas/sales/fabus/business-units-and-opportunity-attributes.html)
- [Set-Enabled Lookups REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-set-enabled-lookups.html)
- [Apps Common](../../../../../core/fusion-api/apps-common/SKILL.md)
- [Set-Enabled Lookup Contract](../../../../../core/fusion-api/apps-common/lookups/references/set-enabled-lookups.md)

## Inputs

- implementation_objective
- project_context
- setup_task_scope
- setup_data_artifacts
- request_mode
- lookup_type
- lookup_operation
- lookup_code
- lookup_attributes
- set_selection_decision
- reference_data_set_identity
- fusion_environment_context
- expected_current_state
- execution_route
- package_task_context
- package_evidence
- business_impact_evidence
- rest_execution_approval_optional

## Outputs

- setup_task_plan
- setup_data_routing
- validation_checkpoints
- resolved_lookup_parent
- resolved_reference_group
- resolved_lookup_contract
- catalog_task_code
- record_set_prerequisite_task_code
- execution_task_code
- current_lookup_state
- package_readiness_result
- immutable_change_preview
- data_loader_handoff_result
- lookup_execution_result
- post_change_verification
- diagnostics
- skill_run_record
- token_usage_record

## Implementation Notes

Use the parent functional-area skill cx.sales.opportunities for cross-task
sequencing. Track token usage for generated project artifacts and skill-run
records. Keep the Oracle task identity, lookup types, set identities,
approval fingerprints, and diagnostics sanitized and explicit.
