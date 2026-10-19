---
skill_id: "cx.sales.opportunities.manage-opportunity-profile-options"
name: "Manage Opportunity Profile Options Setup Task Guidance"
description: "Inventories source-backed Opportunity profile options with explicit discovery coverage and partial results, and reviews exact codes through live Apps Common GETs without export or mutation approval. Updates existing exported Site/User values through FSM and Core Data Loader; export omission or failure selects gated Apps Common REST. Product values are legacy-only by default; new Product values require current Oracle support evidence. Use for Inventory, Review, Set, and BulkSet."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_OPPORTUNITY_PROFILE_OPTIONS"
task_name: "Manage Opportunity Profile Options"
parent_skill_id: "cx.sales.opportunities"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.3.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "fusion_environment_context"
  - "operation"
  - "prior_turn_profile_option_code_optional"
  - "profile_option_code"
  - "profile_option_display_name_optional"
  - "profile_level"
  - "user_name_optional"
  - "product_application_short_name_optional"
  - "expected_current_value_optional"
  - "proposed_value"
  - "bulk_changes_optional"
  - "opportunity_option_identity_evidence_optional"
  - "inventory_scope_optional"
  - "product_creation_support_evidence_optional"
  - "reference_export"
  - "execution_approval"
  - "task_context_path"
  - "task_sequence"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "normalized_operation"
  - "environment_access_evidence"
  - "current_profile_options_export"
  - "profile_option_inventory"
  - "inventory_completion_evidence"
  - "profile_option_candidate_receipt"
  - "inventory_coverage_result"
  - "product_level_support_result"
  - "profile_option_mutation_route"
  - "export_omission_evidence"
  - "export_failure_evidence"
  - "immutable_apps_common_preview"
  - "apps_common_execution_result"
  - "reviewed_package_delta"
  - "validated_fsm_package"
  - "fsm_import_handoff_result"
  - "data_loader_task_validation_result"
  - "data_loader_approval_preview"
  - "task_validation_envelope"
  - "data_load_initiation_result"
  - "post_change_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.apps-common"
  - "core.fusion-api.apps-common.profile-options"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common"
  - "core.fusion-api.apps-common.profile-options"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-opportunity-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-opportunity-profile-options/current/"
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
  - "For Inventory or mutation routing, may submit an approved task-level CSV export; exact-code Review uses Apps Common GETs without creating an export job."
  - "Reads configured profile definitions, levels, and Site/User/Product values through core.fusion-api.apps-common."
  - "After Core Data Loader's separate Task Hook preview and approval lifecycle, may upload and initiate an unchanged export-derived FSM ZIP for a supported existing Site or User value update."
  - "After confirmed export omission may create or update Site/User values through Apps Common, or update an existing legacy Product value. New Product values additionally require current Oracle support evidence; after a failed exact-task export only existing-value updates are allowed. All writes require an immutable preview, explicit approval, and an exact verification read."
  - "Persists export, inventory, package, handoff, verification, diagnostic, and token-usage artifacts in the implementation project workspace."
required_privileges:
  - "Export privileges for Inventory/mutation routing of MOO_MANAGE_OPPORTUNITY_PROFILE_OPTIONS; import privileges only for FSM. Exact-code Review requires neither."
  - "Privileges to read profile options and configured profile values through Apps Common."
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV for Apps Common fallback create or update."
---

# Manage Opportunity Profile Options Setup Task Guidance

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, and target environment
throughout the workflow. Bind export evidence to its archive SHA-256; bind FSM
handoff to the final package SHA-256. REST fallback binds its reason, recorded export
omission or failure evidence, and the canonical request to an immutable preview
digest. Export failure requires no ZIP or omission proof.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may be generated from the project's resolved setup-task
plan without creating an Oracle Run Book. Never hand-author, infer, or
synthesize a context entry merely to satisfy Data Loader.
The Apps Common fallback requires no Data Loader task context or import ZIP.

## Purpose

Inventory, review, and manage Opportunity profile-option values. Establish
current configured values through exact live Apps Common definition, level,
and configured-value reads. Use the task-level FSM export only for package
membership and mutation structure; never present an export value or delivered
default as the latest configured environment value. A successful exact-task
export that omits the requested option selects the declared Apps Common REST
fallback after exact live resolution. A classified failed exact-task export also
continues to Apps Common reads and may update an existing exact live value.
Neither REST path requires a synthetic FSM row.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_OPPORTUNITY_PROFILE_OPTIONS`
- task_name: `Manage Opportunity Profile Options`
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

Use this skill for Inventory, Review, Set, or BulkSet work for `Manage
Opportunity Profile Options`, including requests to list options, check the
current or latest value of an exact code, update an existing exported Site/User
value, set a live Site/Product/User value for an option omitted from export,
or update an existing live value when the task export fails.

## Setup Task Metadata

- Task name: `Manage Opportunity Profile Options`
- Task code: `MOO_MANAGE_OPPORTUNITY_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y`. For options present in the successful
exact-task export, retain the existing FSM workflow:

1. Export populated setup task data with `shared.setup-export.task-level-export`
   using `--data` and no export criteria; its default template/spec output
   cannot establish option membership or omission.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Hand the validated immutable setup package to `core.data-loader`.

For this FSM route, the child skill ends when the exact final package is bound
to the target environment and release, `MOO_MANAGE_OPPORTUNITY_PROFILE_OPTIONS`, exact
`TaskName`, selected skill path, final ASM task identity, final member/header
receipt, reviewed delta and state lock, immutable
path, reopened SHA-256, and validation result and is ready for handoff.
Require persisted `TaskContextPath`, exact `TaskName`, and positive
`TaskSequence` for every Data Loader mutation handoff, and resolve that context
to this exact skill path, `TaskCode`, offering, and functional area.
On the FSM route it must not create an approval preview, request or accept
approval, upload, or initiate the import. `core.data-loader` invokes Task Hook against the unchanged
package and owns its session preview and approval lifecycle. Follow the current
Core Data Loader contract for the later contextual approval and submission.
When Data Loader later returns accepted initiation, resume this child graph at
its `accepted_initiation` terminal and end the request. Status, ProcessLog,
results, and live verification require a later explicit user request.

When the successful export omits the requested definition, or the declared
exact-task export attempt fails, continue through the Apps Common fallback.
After export failure, require an existing exact live child row and use PATCH
only. Invalid cross-target/task evidence, duplicate definitions, or a missing
exported value row for an option that is present do not select REST fallback.

## Read and Export Approval Scope

An exact-code Review is a read-only Apps Common operation. The request to read
the selected environment/code authorizes the declared GET workflow; it requires
read privileges and normal authentication, but no separate mutation approval,
export job, ZIP, Data Loader context, or profile-value write privilege. Read the
exact definition, profileOptionLevels, and Site/User/Product value children
directly; paginate every collection. Record
ExportStatus=not_requested_for_review; never label a skipped export as failed.
Existing valid same-target export evidence may annotate Review but is optional.

A request for current values does not authorize POST setupTaskCSVExports. If a
new export is explicitly requested, run it as a separate declared export step
through the shared skill, with the exact target/task/payload and approval gate
required by repository directives. Inventory and mutation routing retain their
export steps and approval requirements. An unapproved export is an approval
blocker, not export failure; it cannot select failed-export REST mutation.
REST POST/PATCH and Data Loader submission retain their own approval workflows.

## Runtime Interface and Handoff

Normalize list/all/current-values requests to `Inventory`, one exact-code
current/latest/configured-value requests to `Review`, one value change
to `Set`, and multiple value changes to `BulkSet`. A short follow-up
such as "check the latest value" inherits the immediately preceding exact code
only when exactly one code is unambiguous.

Resolve Inventory candidates and Opportunity membership through
`resolve_opportunity_option_candidates` in the task-local lookup rules before
the code-keyed live reads. Its source-backed seed identities supplement the
successful exact-task export; they are not an exhaustive release catalog.
Report the covered source set and every unresolved candidate. A failed export
still continues to live reads for known candidates, but cannot establish a
complete all-options inventory. Return `RETURN_PARTIAL_INVENTORY` when discovery
coverage is incomplete. Review of one supplied exact code still skips export;
display-name-only requests require an exact source-backed code mapping.

For exact-code Review, skip export and proceed to the declared Apps Common
GETs. For Inventory, Set, or BulkSet, attempt the exact populated task export
with `--data` and no criteria after its required approval. Inventory may continue
through live reads after export failure, with the failure disclosed.
Set and BulkSet require a recorded exact-target export attempt:
successful membership selects FSM or omission fallback; classified failure
selects REST lookup and existing-value update readiness. A failed export result
is intermediate: with environment and Apps Common read readiness resolved,
continue DEPENDENCIES via satisfied to LOOKUP rather than returning child
failure. Ignore partial export files and require no successful ZIP fields for
this fallback. Read the exact definition,
its profileOptionLevels rows keyed by LevelName, with EnabledFlag and
UpdateableFlag,
`siteProfileOptionValues`, `userProfileOptionValues`, and
`productProfileOptionValues`; report explicit absence and keep delivered,
effective, exported, and configured values separately labeled.

For FSM Set or BulkSet, hand Data Loader only the unchanged validated package and
task-specific evidence. Require persisted `TaskContextPath`, exact `TaskName`,
and positive `TaskSequence`, resolved to this exact skill path, `TaskCode`,
offering, and functional area. Data Loader owns Task Hook validation, its
immutable session preview and approval lifecycle, authentication, upload, and
initiation. For REST fallback,
use the selected Apps Common profile-options skill and the task-local REST
design and execution gates. The child owns its immutable preview and approval.

## Mutation Route Selection

| Export attempt result | Route | Required behavior |
|---|---|---|
| Requested option definition is present once | FSM | Require an existing exported Site/User value row, matching live state, and final package/task-context validation; retain the existing Data Loader workflow |
| Requested option definition is absent | Apps Common REST | Require the exact live Opportunity definition and eligible Site/Product/User scope; choose Create or Update from exact live child state |
| Exact-task export failed or timed out | Apps Common REST Update | Record classified failure, read exact live definition and child; allow PATCH only if that child exists once and is enabled/updatable |
| Artifact offered as a successful export is incomplete, belongs to another target/task, or contains ambiguous identities | Block mutation | Resolve the artifact or identity issue; do not interpret it as omission |
| BulkSet contains both FSM and REST targets | Split required | Report each row's selected route and require separate route-specific batches and previews before any handoff or write |

Record MutationRoute and FallbackReason per row. For export_omission, bind
successful data-export task/environment/release/timestamp, no-filter evidence,
immutable ZIP path/hash, complete members/headers, and zero exact definitions
in FND_APP_PROFILE_OPTION.csv. Template/spec output, a missing value row, or a
filtered subset cannot prove omission. For export_failure, bind the attempted
exact task and target, timestamp, failure class/message, and available ProcessId,
last status, or request ID; mark unavailable ZIP/hash/member fields explicitly.
Membership remains unknown and omission proof is unnecessary. A reason, route,
or export-evidence change invalidates pending preview, approval, or handoff.

## Apps Common REST Fallback

Load [Apps Common Profile Options](../../../../../core/fusion-api/apps-common/profile-options/SKILL.md)
and its [profile-options contract](../../../../../core/fusion-api/apps-common/profile-options/references/profile-options.md).
Reuse core authentication, the shared REST client, and value-resource keys and
payloads. For every operation in this Opportunity task, the
[task-local lookup rules](ora-resource/ora_reference_lookups.md) define the level
capability preflight, and Read and Export Approval Scope above defines read
authorization. Resolve capabilities from the live profileOptionLevels child;
do not require Site/Product/User enabled/updatable aliases on the parent when
the selected schema omits them. This mapping satisfies the core level check
using live evidence; it does not waive mutation privilege or write approval.
The profileOptions parent and level flags remain read-only.
This fallback supports Set and BulkSet as Create/Update only. Create requires
confirmed omission from a successful complete export. After export failure,
only an existing exact live value can be updated; absence blocks the write.
Delete/Remove remains outside this task's supported operations.

Apply the Product-level policy in `ora_design_enforcement.md` before choosing
the REST request. Oracle's current
[profile-value guidance](https://docs.oracle.com/en/cloud/saas/applications-common/26d/facia/set-profile-option-values.html)
marks Product as deprecated and retained for legacy values. Preserve legacy
reads and existing-row PATCH under the core contract and live capability checks.
A missing Product row is not ordinary creation readiness: require current
Oracle evidence explicitly supporting creation for the selected release and
resource, in addition to all existing omission, identity, privilege, preview,
approval, and verification gates. Neither enabled flags nor user approval is
that support evidence. Export failure remains PATCH-only even with an exception.

| Level | Create endpoint and body | Update endpoint and body |
|---|---|---|
| Site | POST /fscmRestApi/resources/11.13.18.05/profileOptions/{code}/child/siteProfileOptionValues with ProfileOptionValue | PATCH the collection path plus /SITE with only ProfileOptionValue |
| Product | Block by default; only with current creation-support evidence, POST /fscmRestApi/resources/11.13.18.05/profileOptions/{code}/child/productProfileOptionValues with LevelValue={applicationShortName} and ProfileOptionValue | PATCH an existing legacy row at the collection path plus /{applicationShortName} with only ProfileOptionValue |
| User | POST /fscmRestApi/resources/11.13.18.05/profileOptions/{code}/child/userProfileOptionValues with LevelValue={UserGuid} and ProfileOptionValue | PATCH the collection path plus /{UserName} with only ProfileOptionValue |

Resolve one exact UserName to UserGuid through profileUsers for User creates;
use UserName as the item key. Percent-encode every path key. Require exact live profileOptionLevels
EnabledFlag/UpdateableFlag pair for the chosen scope, the mutation privilege, and exact
stored-value dependency evidence. Use SqlValidation to identify a supported
resolver; never execute its SQL. Send stored codes/IDs rather than display labels.

The task-local REST gate builds an immutable preview containing canonical
environment/task, FallbackReason and export omission or failure evidence, exact code/level/key,
POST or PATCH endpoint, current value or explicit not configured, proposed
stored value and meaning, minimal body, dependencies, Product support evidence
and restrictions when applicable, verification plan, and
SHA-256 over the complete preview. Stop for a later standalone approval bound
to that preview. Immediately before each write, re-read definition, capability,
scope identity, current child state, and stored-value dependencies. Drift
requires a fresh preview and approval; approval never transfers between routes.
Changed Product creation-support evidence also invalidates preview and approval.

After approval, invoke Apps Common once and perform a fresh exact child read in
the same run. Success requires the approved stored value on the exact item.
BulkSet preflights all rows, previews the ordered calls together, approves once,
then writes and verifies sequentially, stopping at the first drift, write, or
verification failure and reporting earlier verified successes. Do not retry or
compensate automatically, use Upsert-Mode, synthesize an FSM package, or invoke
Data Loader for this route. At RETURN_APPS_COMMON_READY, persist the preview and
pause. On approved resume, re-enter APPS_COMMON_GATE with refreshed evidence,
use the core executor, and return RETURN_APPS_COMMON_VERIFIED only after exact
verification. Optional effective-session checks do not replace configured-state
verification; follow the core skill's user notification about the next session.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Opportunities`
- Setup task name: `Manage Opportunity Profile Options`
- Setup task code: `MOO_MANAGE_OPPORTUNITY_PROFILE_OPTIONS`




## Negative Scenarios

| Scenario | Required result |
|---|---|
| Exact-code Review has no export or export approval | Continue through definition and complete Site/User/Product GETs; record not_requested_for_review and do not ask approval to create an export job |
| Inventory export fails, or a documented candidate has no resolvable exact code | Read known source-backed candidates, disclose unknown coverage and unresolved identities, and return partial inventory without claiming all options were found |
| Display name has no unique code mapping, or a supplied code has no Opportunity membership evidence | Request exact missing identity/source evidence; never infer a code or membership from a prefix |
| REST Product row is absent and no current Oracle creation-support evidence is supplied | Block creation before preview; legacy Product reads and eligible existing-row PATCH remain available |
| Exact profile-option code is unknown, misspelled, absent, or belongs to another product area | Return exact-code not found and stop Review/Set/BulkSet; do not select a similar code or delivered default |
| Profile-option code and display name resolve to different definitions | Reject the conflicting identity and request one exact code |
| A short follow-up has no exact prior code or more than one candidate code | Do not inherit context; request one exact code |
| FSM target has an unsupported Site/User level or lacks an existing exported value row | Block the FSM update; a present option with a missing value row does not select REST fallback |
| Export omits the exact option and its live child row is absent | Select REST Create after omission, identity, capability, stored-value, preview, and approval gates |
| Exact-task export fails but the exact live child exists | Continue to Apps Common PATCH preview after capability, dependency, and privilege checks; bind the classified failure and exact current state |
| Export fails and live definition or requested child is absent | Block the update; export-failure fallback does not create a value |
| REST target has a disabled/read-only level, ambiguous row, unresolved scope identity, stale state, or invalid approval | Block before POST/PATCH and require corrected evidence or a fresh preview |
| New value fails SqlValidation or the current stored-value contract | Reject before package preparation or REST preview and return sanitized validation evidence |
| Export, live definition, package row, or task context refers to a different profile option, target, task, or value level | Reject as an identity mismatch and require fresh exact-target evidence |

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
uncertain result without reconciliation, a fresh immutable preview, and
explicit approval. On a process timeout or accepted Data Loader initiation,
return the current status and safe next-check path instead of polling or
resubmitting automatically. REST success requires same-run exact child
verification under its separate contract.

Redact credentials, bearer tokens, authorization headers, OAuth state,
token-cache contents, cookies, private keys, and sensitive payload values.
Never print or persist those secrets in previews, diagnostics, project
artifacts, skill-run records, or user responses.

## Oracle Resource Read Order

1. [ora_input_validation.md](ora-resource/ora_input_validation.md)
2. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
3. [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
4. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
5. [ora_error_handling.md](ora-resource/ora_error_handling.md)
6. [ora_rule_registry.json](ora-resource/ora_rule_registry.json) for the compiled task-node graph

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `fusion_environment_context`
- `operation`
- `prior_turn_profile_option_code_optional`
- `profile_option_code`
- `profile_option_display_name_optional`
- `profile_level`
- `user_name_optional`
- `product_application_short_name_optional`
- `expected_current_value_optional`
- `proposed_value`
- `bulk_changes_optional`
- `opportunity_option_identity_evidence_optional`
- `inventory_scope_optional`
- `product_creation_support_evidence_optional`
- `reference_export`
- `execution_approval`
- `task_context_path`
- `task_sequence`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `normalized_operation`
- `environment_access_evidence`
- `current_profile_options_export`
- `profile_option_inventory`
- `inventory_completion_evidence`
- `profile_option_candidate_receipt`
- `inventory_coverage_result`
- `product_level_support_result`
- `profile_option_mutation_route`
- `export_omission_evidence`
- `export_failure_evidence`
- `immutable_apps_common_preview`
- `apps_common_execution_result`
- `reviewed_package_delta`
- `validated_fsm_package`
- `fsm_import_handoff_result`
- `data_loader_task_validation_result`
- `data_loader_approval_preview`
- `task_validation_envelope`
- `data_load_initiation_result`
- `post_change_verification`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
