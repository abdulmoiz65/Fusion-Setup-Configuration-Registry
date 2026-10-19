---
skill_id: "cx.sales.opportunities.manage-win-loss-reasons"
name: "Manage Win/Loss Reasons Setup Task Guidance"
description: "Maintains Win/Loss Reasons through FSM and automatically routes to approved direct Apps Common REST when the same-target FSM export fails, times out, or yields an unusable baseline."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_WIN/LOSS_REASONS"
task_name: "Manage Win/Loss Reasons"
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
version: "0.6.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "request_mode"
  - "lookup_operation"
  - "lookup_code"
  - "lookup_attributes"
  - "set_selection_decision"
  - "reference_data_set_identity"
  - "fusion_environment_context"
  - "expected_current_state"
  - "execution_route_optional"
  - "rest_delete_approval_optional"
  - "rest_execution_approval_optional"
  - "rest_fallback_reason_optional"
  - "fsm_export_failure_evidence_optional"
  - "fsm_export_unavailability_evidence_optional"
  - "lookup_rows_optional"
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
  - "rest_batch_preview_optional"
  - "rest_partial_success_result_optional"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-win-loss-reasons/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-win-loss-reasons/current/"
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
  - "Reads the fixed MOO_SETID_WIN_LOSS_REASON lookup type and its reference-set assignment through core.fusion-api.apps-common."
  - "May hand an immutable FND_MANAGE_SET_ENABLED_LOOKUPS package scoped to MOO_SETID_WIN_LOSS_REASON to core.data-loader, which owns Task Hook validation, its approval preview, the later standalone approval, upload, and accepted initiation result."
  - "On a later explicit status or results request, may read process evidence and verify MOO_SETID_WIN_LOSS_REASON through Apps Common."
  - "Uses direct Apps Common REST for Create, Update, and Disable after a failed, timed-out, or unusable same-target FSM export; Delete remains an explicitly selected direct REST operation. Direct mutations require a separately approved immutable preview."
required_privileges:
  - "Fusion privileges appropriate to view or manage Win/Loss Reason lookup codes and the selected reference data set."
  - "Privileges to export or import FND_MANAGE_SET_ENABLED_LOOKUPS when the FSM route is selected."
  - "Apps Common REST privileges appropriate to create, update, disable, or delete MOO_SETID_WIN_LOSS_REASON codes when the governed direct REST route is selected."
---

# Manage Win/Loss Reasons Setup Task Guidance

## FSM Task Identity Policy

Preserve the exact catalog task code/name and selected task `SKILL.md` for
planning and task validation. Use the separate FSM execution task code
`FND_MANAGE_SET_ENABLED_LOOKUPS` for export/import archive identity because the
catalog code contains `/`. Bind both identities, the target environment, and
the immutable archive SHA-256 throughout review, export, package preparation,
and validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  catalog `TaskCode`, `TaskName`, offering, and functional area. Do not rewrite
  persisted task context to the execution task.

The persisted context may be generated from the project's resolved setup-task
plan without creating an Oracle Run Book. Never hand-author, infer, or
synthesize a context entry merely to satisfy Data Loader.

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Win/Loss Reasons` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_WIN/LOSS_REASONS`
- task_name: `Manage Win/Loss Reasons`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Win/Loss Reasons` under `Opportunities`.

## Setup Task Metadata

- Task name: `Manage Win/Loss Reasons`
- Task code: `MOO_MANAGE_WIN/LOSS_REASONS`
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
- Setup task name: `Manage Win/Loss Reasons`
- Catalog task code: `MOO_MANAGE_WIN/LOSS_REASONS`
- FSM export/import execution task code: `FND_MANAGE_SET_ENABLED_LOOKUPS`
- FSM export/import execution task name: `Manage Set Enabled Lookups`
- Export/import row scope: `MOO_SETID_WIN_LOSS_REASON`




## Set ID Selection

Never default this task to Common Set. For `SingleLookup` without an exact set
selector, ask whether Common Set should be used or a different exact Set ID or
Set Code should be selected. Resolve confirmed Common Set through the
documented read-only set resolver rather than hard-coding its ID. For package
mutations, preserve each exported row's set and require an explicit choice for
every new row without one. Set confirmation is not mutation approval.

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
| Business value | Win/Loss Reason |
| Lookup type | MOO_SETID_WIN_LOSS_REASON |
| Catalog task code | MOO_MANAGE_WIN/LOSS_REASONS |
| FSM export/import execution task code | FND_MANAGE_SET_ENABLED_LOOKUPS |
| FSM export/import execution task name | Manage Set Enabled Lookups |
| Record-set prerequisite task | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Default mutation route | FSM through core.data-loader |
| Automatic fallback route | Direct Apps Common REST after an unavailable or unusable same-target FSM export |

The lookup type, catalog task code, and FSM execution task code are immutable
for this adapter. Reject a request that supplies a different lookup type,
catalog task code, or package task code. Never construct an export/import path
from the slash-containing catalog code and never URL-encode the slash as a
workaround. If the record-set assignment is missing or incorrect, return
ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES as the prerequisite gap; do not
change that assignment here.

## Common Workflow Contract

Load [Manage Set Enabled Lookups](../manage-set-enabled-lookups/SKILL.md) for
the shared Apps Common discovery, validation, preview, approval, mutation,
diagnostics, retry, and verification discipline. Reuse its behavior and its
`FND_MANAGE_SET_ENABLED_LOOKUPS` FSM transport identity only. Do not inherit
either of its two generic lookup-type ownership boundaries; this adapter
remains scoped exclusively to `MOO_SETID_WIN_LOSS_REASON` and retains its own
catalog identity and rule graph.

This task's local set-validation rules govern its set selectors. For current
discovery and reference loading, follow [Apps Common](../../../../../core/fusion-api/apps-common/SKILL.md)
and its [Set-Enabled Lookups reference](../../../../../core/fusion-api/apps-common/lookups/references/set-enabled-lookups.md).
For FSM imports, [Core Data Loader](../../../../../core/data-loader/SKILL.md)
owns its current Task Hook, immutable artifact, approval, and submission
lifecycle. These task-local and core contracts take precedence over inherited
coordinator wording. Do not impose a literal approval keyword or repeat live
validation after approval outside the current Data Loader contract.

For Create, Update, and Disable, this adapter's declared automatic export
fallback replaces the coordinator's request-selected direct REST condition.
Its exact-preview approval and verification discipline still applies.

This adapter owns the exact task boundary:

1. Load the task-local resources and compiled registry listed below.
2. Resolve the exact MOO_SETID_WIN_LOSS_REASON parent first and capture its returned nonblank ReferenceGroupName. For SingleLookup, use it to resolve one exact set and any requested business-unit assignment before reading code state. For Package work, validate set and state per changed row; full-task Export has no set selector or code.
3. For the preferred FSM route, export the complete
   `FND_MANAGE_SET_ENABLED_LOOKUPS` package, then select
   `MOO_SETID_WIN_LOSS_REASON` rows locally by exact lookup type and Set ID. For
   SingleLookup Create, Update, or Disable, require exactly one matching
   reviewed row. For Package Create, Update, Disable, or Import, validate every
   changed Win/Loss Reason row atomically. Preserve all unrelated members and
   rows unchanged and never treat them as adapter-owned changes. Both native FSM modes
   require catalog and execution task identities, package hash binding, state
   locks, and business-impact evidence before Data Loader handoff; persisted
   Data Loader task context is required for every Data Loader handoff.
4. If that same-target export fails, exceeds its declared polling window, or
   produces an unusable baseline, preserve its unavailability receipt. The
   verifier returns `OPP.WIN_LOSS.RETURN_FALLBACK_REQUIRED`.
   The invoking router continues the same request once as `REST_FALLBACK`,
   using the unchanged business intent, requested rows, and confirmed sets.
   Restart the task graph to perform fresh REST resolution before preview.
   This route change needs no repeated export approval or loader capability
   lookup. Direct Apps Common REST owns the separate mutation preview,
   approval, submission, and immediate verification.
5. Let core.data-loader own Task Hook validation, its immutable preview, its
   current approval lifecycle, upload, and accepted initiation result for the FSM
   route. REST fallback does not use Data Loader or require its task context,
   session, source, import archive, or approval.
6. Permit Delete as an explicitly selected direct REST operation without an
   export-failure prerequisite. Every REST route requires editability and
   impact evidence, a separate immutable preview, immediate approval, one
   submission per displayed request, and exact read-back verification.
7. Never use `MOO_MANAGE_WIN/LOSS_REASONS` in an FSM export/import request or
   package identity. Never substitute another named Opportunity task code for
   either the catalog or execution identity.

## Supported Operations

Inventory and Read are read-only. Create, Update, and Disable prefer the
`FND_MANAGE_SET_ENABLED_LOOKUPS` FSM execution task and restrict changed rows to
`MOO_SETID_WIN_LOSS_REASON`. When a same-target export fails, exceeds its
declared polling window, or yields an unusable baseline, those operations
continue through direct Apps Common REST for one or many reasons. Export and
Import remain FSM-only. The slash-containing catalog task code is used only for
catalog selection, project planning, and task-local validation. Delete fails
closed on FSM and remains an explicitly selected direct REST operation.

## REST Fallback for an Unavailable or Unusable FND Export

Use `REST_FALLBACK` only for Create, Update, or Disable with a same-target
`FND_MANAGE_SET_ENABLED_LOOKUPS` unavailability receipt. Use the following
classified reasons:

- `EXPORT_REQUEST_FAILED`: the exact-target export request failed before a
  process identifier was returned; retain its request fingerprint and sanitized
  failure evidence instead of inventing an identifier.
- `PROCESS_FAILED`: the export process returned a terminal failure.
- `PROCESS_TIMEOUT`: the declared polling window elapsed; retain the actual
  last status and elapsed time rather than relabeling the job as failed.
- `COMPLETED_LOOKUP_OMISSION`: a valid complete data export omitted both the
  exact lookup parent and its codes.
- `COMPLETED_UNUSABLE_EXPORT`: the completed result cannot provide a usable
  baseline, for example a missing download, malformed archive/metadata,
  incorrect returned task/release, template-only or narrowed data, or an
  incomplete exported parent/code population. Preserve the actual defect and
  never use that result as an FSM baseline or as lookup-omission proof.

The receipt must prove an export attempt for the exact selected environment,
release, and execution task; an arbitrary old or other-environment file is not
an export attempt. The complete evidence contract is owned by
`verify_win_loss_reason_fsm_package` in
[ora_reference_lookups.md](ora-resource/ora_reference_lookups.md).

For a completed omission, retain the actual `COMPLETED` process status and the
baseline path/hash; classify the content mismatch as `catalog_mismatch`.
For any other unusable result, retain its own failure class and artifact
reference/hash when available; do not parse an unsafe archive to prove a gap.
Return a fallback candidate before REST confirmation, then
`RestFallbackEligible=true` only after all required fresh reads succeed.
For completed lookup omission, additionally confirm complete nonempty existing
inventory in every selected set. For the other reasons, ordinary exact-row
reads suffice and an empty selected set remains a valid Create candidate.
REST readability establishes lookup availability. Direct REST operation,
privilege, business-impact, and approval checks still govern the
mutation. Do not synthesize an FSM package from REST data.

A still-running export within its polling window does not trigger fallback.
Absence of a requested new code from an otherwise usable baseline is normal
for Create. Stale or cross-environment receipt evidence blocks fallback; an
unusable result from a verified same-target attempt uses its classified reason.
Do not reroute after an upload, import, or lookup mutation was submitted or became
uncertain, or when the user explicitly requires FSM-only execution. Export
and Import remain FSM-only; Delete retains its separate REST_DELETE route.

## Automatic Direct REST Routing

`ExecutionRoute=REST_FALLBACK` always selects direct Apps Common REST. Do not
discover a registered loader object or require proof of loader non-support.
Preserve the exact lookup, catalog identity, requested rows, and confirmed sets.
The invoking router continues the existing mutation request once through this
declared route after the verifier returns fallback required. If FSM-only or
Data Loader-only execution was explicitly required, return the export gap and
the incompatible-route constraint instead of changing that scope.

Data Loader remains the executor for a usable native FSM package. Do not
switch routes after an upload, import, or mutation was submitted or became
uncertain, and never reuse export or Data Loader approval for a REST write.

## Direct REST Executor

The following request and approval rules apply to REST_FALLBACK and the
separately selected REST_DELETE route.

For a single reason, apply the existing `SingleLookup` state and set rules. For
multiple reasons, use `Package` request mode as a normalized ordered row list;
this is a REST request collection, not an FSM package. Before previewing any
write, resolve the exact parent and reference set and read the current state of
every distinct case-sensitive LookupCode and SetId pair. Reject duplicate row
identities and validate Create, Update, or Disable independently for each row.

Build one immutable REST preview containing the fallback evidence, target,
ordered row count, and for every row the operation, lookup and set identities,
before/after state, impact, exact method, endpoint, request body, verification
GET, and request fingerprint. For Create, use the collection endpoint and
`Upsert-Mode: false`. For Update or Disable, PATCH only the canonical child
item link returned by the fresh read. Disable changes only `EnabledFlag` to
`N`. Any changed, added, removed, or reordered row invalidates approval.

After explicit approval, submit requests once in preview order through
`core.fusion-api.apps-common` and verify each successful request immediately.
Stop on the first failed or uncertain request. Preserve and report prior
successful rows, the failed or uncertain row, and all unattempted rows; never
retry, continue past uncertainty, or automatically delete/reverse successful
rows. A fresh read, rebuilt preview, and new approval are required to resume.

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
adapter's RequestMode, fixed lookup type, exact catalog and execution task
codes, returned reference group, SingleLookup set or per-row package/REST sets,
package validation or export-unavailability evidence and fallback reason,
Data Loader handoff or REST batch outcome, and route-specific approval state. Do
not maintain a second reduced interface
or reinterpret a generic approval as Data Loader upload authorization.

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Offline Validation Evidence

Use [golden-scenarios.md](tests/golden-scenarios.md) for synthetic inputs and
expected outcomes. The task-specific offline suite validates source/registry
equivalence, route contracts, scenario transition paths, and failure terminals:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s pillars/cx/sales/opportunities/manage-win-loss-reasons/tests -p 'test_*.py' -v
```
