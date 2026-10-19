---
skill_id: "cx.sales.opportunities.manage-opportunity-revenue-types"
name: "Manage Opportunity Revenue Types Setup Task Guidance"
description: "Maintains Opportunity Revenue Types through exact-task FSM CSV, including header-only baseline recovery, with a final approved Apps Common REST fallback when the CSV route is exhausted and prior writes are reconciled."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_REVENUE_TYPES"
task_name: "Manage Opportunity Revenue Types"
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
version: "0.3.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "request_mode"
  - "lookup_operation"
  - "lookup_code"
  - "lookup_attributes"
  - "reviewed_rows_optional"
  - "set_selection_decision"
  - "reference_data_set_identity"
  - "fusion_environment_context"
  - "expected_current_state"
  - "execution_route_optional"
  - "csv_failure_receipt_optional"
  - "csv_recovery_evidence_optional"
  - "prior_submission_reconciliation_optional"
  - "rest_execution_approval_optional"
  - "rest_delete_approval_optional"
  - "reference_export_optional"
  - "task_context_path"
  - "task_sequence"
  - "package_path_optional"
  - "package_sha256_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "resolved_lookup_contract"
  - "resolved_lookup_parent"
  - "resolved_reference_group"
  - "catalog_task_code"
  - "record_set_prerequisite_task_code"
  - "execution_task_code"
  - "current_lookup_state"
  - "immutable_change_preview"
  - "fsm_package_validation"
  - "rest_fallback_routing_optional"
  - "data_loader_task_validation_result_optional"
  - "data_loader_approval_preview_optional"
  - "task_validation_envelope_optional"
  - "data_load_initiation_result_optional"
  - "lookup_execution_result"
  - "post_change_verification"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.sales.opportunities.manage-set-enabled-lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-opportunity-revenue-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-opportunity-revenue-types/current/"
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
  - "Reads the fixed MOO_SETID_REVENUE_TYPE lookup type and its reference-set assignment through core.fusion-api.apps-common."
  - "May hand an immutable MOO_MANAGE_REVENUE_TYPES package to core.data-loader, which owns Task Hook validation, its approval preview, the later standalone approval, upload, and accepted initiation result."
  - "On a later explicit status or results request, may read process evidence and verify MOO_SETID_REVENUE_TYPE through Apps Common."
  - "May route Create, Update, or Disable to core.fusion-api.apps-common as the final fallback after documented CSV exhaustion and reconciliation, with a separate immutable REST preview and immediate approval. Delete retains its explicitly selected REST exception."
required_privileges:
  - "Fusion privileges appropriate to view or manage Sales Revenue Type lookup codes and the selected reference data set."
  - "Privileges to export or import MOO_MANAGE_REVENUE_TYPES when the FSM route is selected."
  - "Apps Common REST privileges for the selected Sales Revenue Type operation when the final fallback or REST Delete route is selected; read access does not establish write permission."
---

# Manage Opportunity Revenue Types Setup Task Guidance

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

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Opportunity Revenue Types` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_REVENUE_TYPES`
- task_name: `Manage Opportunity Revenue Types`
- parent_skill_id: `cx.sales.opportunities`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Opportunities`
- functional_area_code: `ORA_MOO_OPPORTUNITIES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Opportunity Revenue Types` under `Opportunities`.

## Setup Task Metadata

- Task name: `Manage Opportunity Revenue Types`
- Task code: `MOO_MANAGE_REVENUE_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Opportunities`
- Setup task name: `Manage Opportunity Revenue Types`
- Setup task code: `MOO_MANAGE_REVENUE_TYPES`




## Set ID Selection

Never default this task to Common Set. For `SingleLookup` without an exact set
selector, ask whether Common Set should be used or a different exact Set ID or
Set Code should be selected. Resolve confirmed Common Set through the
documented read-only set resolver rather than hard-coding its ID. For package
mutations, preserve each exported row's set and require an explicit choice for
every new row without one. Set confirmation is not mutation approval.

Validate SetId as an integer resolved in the selected environment, rather than
requiring it to be positive. A confirmed Common Set may legitimately resolve
to zero; use the returned ID and SetCode without hard-coding an ID or inferring
Common Set from a numeric value.

## Negative Set Scenarios

Reject a malformed or unknown Set ID/Set Code, selectors that resolve to
different sets, a confirmed Common Set choice that resolves to a non-Common
set, a business-unit assignment whose ReferenceGroupName or set differs from
the exact parent, or a package row whose set differs from its confirmed or
fresh-export identity. Do not substitute Common Set, a close match, a generic
lookup type, or another environment's set. Return the exact mismatch and
require one valid set decision before continuing.

## Fixed Set-Enabled Lookup Adapter

| Contract item | Fixed value |
|---|---|
| Business value | Sales Revenue Type |
| Lookup type | MOO_SETID_REVENUE_TYPE |
| Catalog and FSM task code | MOO_MANAGE_REVENUE_TYPES |
| Record-set prerequisite task | ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES |
| Default mutation route | FSM through core.data-loader |
| Final fallback route | core.fusion-api.apps-common after documented CSV exhaustion and reconciled prior submissions |

The lookup type and FSM task code are immutable for this adapter. Reject a
request that supplies a different lookup type or package task code. If the
record-set assignment is missing or incorrect, return ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES as the
prerequisite gap; do not change that assignment here.

## Common Workflow Contract

Load [Manage Set Enabled Lookups](../manage-set-enabled-lookups/SKILL.md) for
the shared Apps Common discovery, validation, preview, approval, mutation,
diagnostics, retry, and verification discipline. Reuse its behavior only; do
not inherit its FND task identity or its two generic lookup types.

For the final fallback, load [Apps Common](../../../../../core/fusion-api/apps-common/SKILL.md),
then its [Lookups skill](../../../../../core/fusion-api/apps-common/lookups/SKILL.md)
and [Set-Enabled Lookups reference](../../../../../core/fusion-api/apps-common/lookups/references/set-enabled-lookups.md). This adapter's final-fallback condition
selects that route; its separate REST approval and verification rules apply.
Core Data Loader retains ownership of the FSM preview and submission lifecycle.

This adapter owns the exact task boundary:

1. Load the task-local resources and compiled registry listed below.
2. Resolve the exact MOO_SETID_REVENUE_TYPE parent first and capture its returned nonblank ReferenceGroupName. For SingleLookup, use it to resolve one exact set and any requested business-unit assignment before reading code state. For Package work, validate set and state per changed row; full-task Export has no set selector or code.
3. For the preferred FSM route, require exactly one reviewed SingleLookup Create, Update, or Disable code change in a fresh, validated, immutable MOO_MANAGE_REVENUE_TYPES package, plus its unchanged parent linkage row. Apply the header-only baseline procedure below when seeded data is omitted. For native Package Create, Update, Disable, or Import, validate every changed code and its parent linkage atomically. Both FSM modes require exact task identity, package hash binding, state locks, and business-impact evidence before Data Loader handoff; persisted Data Loader task context is required for every Data Loader handoff.
4. Let core.data-loader own Task Hook validation, its immutable preview, the later standalone approve, upload, and accepted initiation result. Accepted initiation ends the request; status, ProcessLog, and read-back verification require a later explicit request.
5. Exhaust the applicable CSV recovery below before considering Apps Common. The verifier may return RETURN_FALLBACK_REQUIRED with a same-target failure receipt; the invoking router resumes this request once as REST_FALLBACK, preserves its business intent and confirmed sets, and restarts parent/set/code resolution. After an accepted import, this evaluation occurs only on a later explicit status or results request, after terminal process evidence and exact state reconciliation. Pending, uncertain, or partially applied requests block route switching.
6. For an eligible REST_FALLBACK Create, Update, or Disable, or an explicitly selected REST_DELETE, require editability and impact evidence, a separate immutable REST preview, immediate approval, one submission per displayed request, and exact read-back verification. Never reuse export or Data Loader approval.
7. Never substitute FND_MANAGE_SET_ENABLED_LOOKUPS or another named Opportunity task code.

## Supported Operations

Inventory and Read are read-only. Create, Update, and Disable use the exact FSM
task code first and may use the final Apps Common fallback below. Export and
Import remain FSM-only; an Import request is not converted to REST writes.
Delete fails closed on FSM and retains its explicitly selected REST exception.

## Header-Only FSM Baselines and Parent Linkage

A completed data export can contain header-only CSVs because FSM excludes
Oracle seeded data. Zero exported rows alone do not invalidate a baseline or
prove that the live lookup is empty. Validate the exact target, release,
`MOO_MANAGE_REVENUE_TYPES` task, successful process result, metadata, members,
and headers first. A template export, failed or incomplete process, wrong-task
archive, or missing metadata remains a blocker.

For a Create against an existing lookup omitted from the valid data export:

1. Resolve the live `MOO_SETID_REVENUE_TYPE` parent, its returned reference
   group and editability, the confirmed set, and the new code's absence through
   the existing read-only resolvers. An export omission is not absence evidence.
2. Preserve the source ZIP and construct a separate final package. Keep
   `ASM_SETUP_CSV_METADATA.xml`, member names, header spelling/order, and all
   unrelated rows and members unchanged. Use only the current export's schema.
3. In `FND_APP_SET_ENABLED_LOOKUP.csv`, reuse the exact exported parent when
   present. If omitted, add one existing-parent linkage row whose `LookupType`,
   `ReferenceGroupName`, `Meaning`, `Description`, `ModuleId`,
   `CustomizationLevel`, and `RestAccessSecured` come from the fresh exact
   parent response. Include only fields present in the exported header; leave
   audit columns blank on this added row. Do not invent values, create a new
   lookup type, or change the existing parent's configuration. Missing required
   parent fields or conflicting exported/live parent values block preparation.
4. In `ORA_FND_APP_SET_ENABLED_LOOKUP_CODE.csv`, add the reviewed new code with
   `FND_APP_SET_ENABLED_LOOKUP.LookupType` equal to the parent `LookupType`,
   `SetCode` equal to the resolved set, and the requested meaning and permitted
   mutable fields. Do not copy all seeded codes into the package.
5. Validate the parent-child join for every changed child. One lookup-code
   change plus its unchanged support parent is one business change, although
   both CSVs contain a row. A child-only package is not ready even when its
   parent exists live. Re-read the exact code state before Data Loader handoff.

Keep FSM as the execution route. Data Loader still owns Task Hook validation,
the immutable preview, approval, and submission. This procedure does not
authorize an import or by itself qualify the request for REST fallback.

Oracle source: [Export and import of CSV file packages, page 29](https://docs.oracle.com/en/cloud/saas/applications-common/26d/oafsm/using-functional-setup-manager.pdf#page=37).

## Final Apps Common Fallback

For Create, Update, or Disable, use this order: exact-task FSM export and CSV
preparation; applicable header-only/unchanged-parent recovery; Core Data Loader
validation and approved submission; Apps Common only if the CSV route cannot
complete the requested change. Do not submit a known-invalid package or repeat
a live import merely to demonstrate exhaustion. Record which recovery was
applied or why it was unavailable; a repairable missing parent row must be
corrected before fallback, and a valid header-only baseline stays on FSM.

Require a fresh failure receipt bound to the exact environment, release,
MOO_MANAGE_REVENUE_TYPES, MOO_SETID_REVENUE_TYPE, operation, reviewed rows,
and confirmed sets. Include the failed stage, classified reason, actual status,
timestamps, sanitized error or ProcessLog evidence, available artifact hashes,
and every returned process/request/content ID. Permitted reasons are:

- `EXPORT_FAILED` or `EXPORT_TIMEOUT`: the approved same-target export failed
  or exceeded its declared polling window; retain the actual last status and
  elapsed wait. A running export inside that window does not qualify.
- `UNUSABLE_EXPORT`: the verified exact-task export attempt cannot supply a
  safe, usable data baseline and documented CSV recovery cannot resolve the
  defect. A wrong-target source file is not an attempted export receipt.
- `CSV_IMPORT_FAILED` or `CSV_IMPORT_NO_EFFECT`: on a later explicit results
  request, all related import jobs are terminal, status/errors and ProcessLog
  have been retrieved, and fresh reads show every requested row remains at its
  reviewed pre-import state (or absent for Create). Document why further CSV
  recovery cannot resolve the failure; do not retry an import automatically.

Input, catalog identity, set/assignment, authentication/authorization, missing
workflow/context, and declined or missing approval failures remain blockers.
So do explicit FSM-only constraints, unknown upload/initiation outcomes,
pending import jobs, incomplete diagnostics, concurrent state changes, or
partial business changes. If all requested values are already applied, return
the verified result without another write. Partial results require a new
reviewed request for the remaining changes; never replay the original batch.

The route verifier first returns a candidate, then `RestFallbackEligible=true`
only after fresh exact parent, set/assignment, and per-code reads pass and prior
submissions are reconciled. Preserve RequestMode and row scope. For Package
Create, Update, or Disable, use the reviewed ordered row list, validate every
distinct case-sensitive LookupCode/SetId pair, and reject duplicates. This
route uses no Data Loader session, archive, task context, or approval; missing
Data Loader context cannot itself trigger it.

Prepare one immutable REST preview showing the failure/recovery evidence,
target, operation, lookup/set identity, current and proposed values, impact,
exact method/endpoint/body, verification GET, and request fingerprint for every
row. For Create, POST to the fixed lookup's child collection with LookupCode,
the resolved integer SetId (including a live-resolved zero), Meaning, and only
reviewed writable fields; send `Upsert-Mode: false`. SetCode is read-only and
is not sent. For Update or Disable, PATCH the same-target canonical child link
returned by the fresh read; Update contains only reviewed mutable fields and
Disable only `EnabledFlag=N`. Never write the parent, reference-set assignment,
lookup identity, audit fields, or unrelated codes.

Obtain explicit approval of this exact REST preview immediately before execution.
Submit each approved request once through the Apps Common Lookups skill's core
REST client and verify it immediately through the disclosed exact GET. A changed
or stale preview invalidates approval. Stop at the first failed, uncertain, or
unverified row; retain prior successes and unattempted rows without automatic
retry, rollback, or another fallback. A new write needs fresh reconciliation,
a rebuilt preview, and new approval.

Oracle source: [26D Set-Enabled Lookup Codes REST operations](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/api-set-enabled-lookups-lookup-codes-adf.html).

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

1. [ora_input_validation.md](ora-resource/ora_input_validation.md)
2. [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
3. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
4. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
5. [ora_error_handling.md](ora-resource/ora_error_handling.md)
6. [ora_rule_registry.json](ora-resource/ora_rule_registry.json)

Use the rule planner before consuming the registry. The local graph owns this
adapter's exact task identity; the common workflow is not a substitute for the
local registry or approval gate.

## Runtime Interface

Use the manifest `inputs` and `outputs` as the canonical interface. In
addition to the standard project and setup-data fields, preserve this
adapter's RequestMode, fixed lookup type, exact catalog/FSM task code, returned
reference group, SingleLookup set or per-row package sets, package validation
result, Data Loader handoff evidence, and route-specific approval state.
Preserve CSV failure/recovery receipts, prior-submission reconciliation, and
the fallback eligibility decision when REST_FALLBACK is selected. Do not
maintain a second reduced interface
or reinterpret a generic approval as Data Loader upload authorization.

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
