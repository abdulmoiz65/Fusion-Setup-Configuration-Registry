---
skill_id: "cx.sales.opportunities.manage-sales-stage-phase-codes"
name: "Manage Sales Stage Phase Codes Setup Task Guidance"
description: "Maintains standard Sales Stage Phase Codes through exact-task CSV with omitted-parent recovery and a final approved Apps Common fallback after CSV exhaustion and reconciled prior submissions."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_SALES_STAGE_PHASE_CODES"
task_name: "Manage Sales Stage Phase Codes"
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
version: "0.2.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "request_mode"
  - "lookup_operation"
  - "lookup_code_optional"
  - "lookup_attributes"
  - "reviewed_rows_optional"
  - "fusion_environment_context"
  - "expected_current_state"
  - "execution_route_optional"
  - "csv_failure_receipt_optional"
  - "csv_recovery_evidence_optional"
  - "prior_submission_reconciliation_optional"
  - "rest_execution_approval_optional"
  - "task_context_path_optional"
  - "task_sequence_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "resolved_lookup_parent"
  - "current_lookup_state"
  - "fsm_package_validation"
  - "rest_fallback_routing_optional"
  - "lookup_execution_result"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-sales-stage-phase-codes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-sales-stage-phase-codes/current/"
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
  - "Reads only the exact MOO_STAGE_PHASE_CD standard lookup parent and codes through Apps Common."
  - "May hand an immutable MOO_MANAGE_SALES_STAGE_PHASE_CODES CSV package to Core Data Loader, which owns validation, preview, later approval and accepted initiation."
  - "May route Create, Update or Disable to separately approved Apps Common REST only as the final verified CSV-exhaustion fallback."
  - "After accepted initiation, status, ProcessLog and live verification require a later explicit request."
required_privileges:
  - "Privileges to view/manage MOO_STAGE_PHASE_CD and export/import this exact task."
  - "Standard Lookups REST write privileges appropriate to the operation when final fallback is selected; read permission is not write permission."
---

# Manage Sales Stage Phase Codes Setup Task Guidance

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

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Sales Stage Phase Codes` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_SALES_STAGE_PHASE_CODES`
- task_name: `Manage Sales Stage Phase Codes`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Sales Stage Phase Codes` under `Opportunities`.

## Setup Task Metadata

- Task name: `Manage Sales Stage Phase Codes`
- Task code: `MOO_MANAGE_SALES_STAGE_PHASE_CODES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

The fixed lookup is standard `MOO_STAGE_PHASE_CD`; it has no reference-data set
selector. Never substitute a set-enabled lookup, SetId or SetCode. Use
SingleLookup for one code, Read or Inventory, and Package for multiple reviewed
changes or full-task Export/Import. Delete remains unsupported.

1. Load the local compiled plan and rules. Resolve the exact standard parent
   and fresh per-code state through [Apps Common](../../../../../core/fusion-api/apps-common/SKILL.md),
   its [Lookups skill](../../../../../core/fusion-api/apps-common/lookups/SKILL.md)
   and [Standard Lookups reference](../../../../../core/fusion-api/apps-common/lookups/references/standard-lookups.md).
   Inventory paginates all codes; Create requires exact absence, Update/Disable
   an exact existing item. A failed read or incomplete page is not absence.
2. Prefer a fresh completed full-data MOO_MANAGE_SALES_STAGE_PHASE_CODES export
   through shared.setup-export.task-level-export, then validate setup/reference
   data and the task-local package verifier. Preserve task identity, source ZIP,
   metadata, members, headers and unrelated content; use the recovery below
   when seeded parent/code rows are omitted.
3. For a ready FSM mutation/Import, bind the reopened immutable PackagePath and
   PackageSha256 plus persisted TaskContextPath, exact TaskName and positive
   TaskSequence resolved to this skill/task/offering/functional area. Core Data
   Loader owns Task Hook validation, its immutable preview, later contextual
   approval, upload and one submission. Do not prescribe a literal approval
   keyword, create a child FSM preview, or revalidate outside its lifecycle.
4. Accepted initiation ends its request. Status/errors/ProcessLog and exact
   read-back require a later explicit results request. Do not automatically
   poll or resubmit. Export/Import remain FSM-only.
5. Only after applicable CSV recovery is exhausted may the verifier return
   RETURN_FALLBACK_REQUIRED. The router resumes the unchanged Create/Update/
   Disable request once as REST_FALLBACK, restarts fresh parent/code reads and
   verifies the exhaustion receipt/reconciliation before a separate REST
   preview and immediate approval. Pending, uncertain or partial imports block
   route switching. The final fallback below is the only direct REST write route.

## Execution Safety Contract

Before an external read, export, FSM package handoff, or direct REST preview or
submission, run the preflight checks applicable to that operation:

1. Bind the selected environment, release and project to the exact catalog
   task and standard lookup. Validate Operation, RequestMode and ExecutionRoute
   before resolution; apply code, delta and package requirements only where
   the requested operation needs them. Inventory and Read require no mutation
   ZIP or Data Loader context, and full-task Export requires no code or set.
2. Confirm the privileges required for the selected read, export or mutation
   through the owning core/shared contract. A successful GET is not evidence
   of write permission. Resolve current parent/code state and reviewed impact
   before preparing a change; stop on stale, ambiguous or conflicting evidence.
3. Validate supplied source paths and destination paths under the selected
   workspace. Before FSM handoff, verify safe ZIP shape, exact current-export
   task/member/header identity, reviewed parent-child changes, preserved
   unrelated content and the immutable final package evidence. For REST, check
   the exact method, same-target endpoint, writable body and verification GET.
4. Preserve the selected executor's approval boundary. FSM handoff is validation
   only; Core Data Loader owns its retained-session preview, contextual approval
   and captured-source submission. Do not reread sources or revalidate outside
   its lifecycle after approval. REST requires its separately approved immutable
   preview immediately before submission. A changed preview or uncertain prior
   submission blocks further writes.

Load ora-resource/ora_error_handling.md before preview or execution. Classify
failures, preserve sanitized diagnostics and external identifiers, and use only
the owning core client's bounded read/auth recovery. Do not retry a mutation,
upload or import automatically. Report actual status, elapsed polling and the
safe next-check path on timeout; accepted Data Loader initiation ends the
request until a later explicit status/results request. Redact credentials,
tokens, authorization headers, cookies, private keys and protected payloads.

## Header-Only Baselines and Standard Parent Linkage

A successful full-data export may have header-only CSVs because seeded data is
omitted. Validate exact target/release/task, process result, ASM metadata,
members and headers; zero rows alone are not a failed export or live absence.
A template, unsafe/incomplete ZIP or unproven identity remains a blocker.

Retain the original export and prepare a separate final ZIP. In the current
export's FND_APP_STANDARD_LOOKUP.csv, reuse the exact existing parent when it
matches fresh live metadata; if omitted, add exactly one unchanged
MOO_STAGE_PHASE_CD support row using live LookupType, Meaning, Description,
ModuleId, CustomizationLevel and RestAccessSecured only where those fields are
in the exported header. Leave added system-audit columns blank. Missing or
conflicting required business fields block preparation; never invent parent
metadata or create/change a lookup type.

Every reviewed child in ORA_FND_APP_STANDARD_LOOKUP_CODE.csv must join through
FND_APP_STANDARD_LOOKUP.LookupType to that parent. Use fresh live absence or
existing-state locks, the requested code/meaning and permitted mutable fields.
Keep current CSV field/value conventions and exact spelling/order; display
labels are not assumed to be CSV headers. Do not copy all seeded codes or add
members absent from the current metadata contract. Validate the unchanged
parent separately from the one or many business code changes, preserve all
unrelated rows/members, and refresh exact state before FSM handoff. Child-only
packages block even when the parent exists live.

## Final Apps Common Fallback

Require a same-target/release/task/lookup/operation/row failure receipt with
actual statuses, timestamps, classified failure, available artifact hashes and
returned external IDs, plus applicable CSV recovery outcomes and why recovery
cannot finish. Valid reasons are EXPORT_FAILED, EXPORT_TIMEOUT after the
polling window, UNUSABLE_EXPORT after recovery, CSV_IMPORT_FAILED or
CSV_IMPORT_NO_EFFECT. Header-only exports and repairable missing parent rows
stay on CSV; do not submit invalid packages or repeat writes to prove failure.

After an accepted import, evaluation occurs only on a later explicit results
request using Core Data Loader status/errors/ProcessLog. All related import
jobs must be terminal and every requested code must remain at the reviewed
pre-state or absent for Create. Pending jobs, unknown upload/initiation,
incomplete diagnostics, partial changes or concurrent state drift block.
All-applied returns verified state without writing; partial results require a
new reviewed remaining-change request. Input/catalog/auth/approval/workflow/
context gaps and explicit FSM-only constraints cannot trigger fallback.

The dedicated verifier sets RestFallbackEligible=true only after exhaustion,
reconciliation and fresh exact standard-parent/per-code reads. Reject duplicate
case-sensitive LookupCode identities. REST supports Meaning, Description,
EnabledFlag, StartDateActive, EndDateActive, DisplaySequence and Tag only; a
Lookup_DFF change remains on FSM and blocks fallback rather than being dropped
or guessed. Normalize reviewed Enabled Yes/No to REST EnabledFlag Y/N.

Prepare one immutable REST preview containing failure/recovery evidence,
environment, ordered operations/codes, current/proposed state, impact, exact
method/endpoint/body, verification GET and fingerprint. Create uses POST to
standardLookups/MOO_STAGE_PHASE_CD/child/lookupCodes with LookupCode, Meaning
and reviewed writable fields and Upsert-Mode=false. Update/Disable PATCH only
the fresh same-target canonical child link; Disable sends only EnabledFlag=N.
No SetId, SetCode, parent, audit or identity fields are written. Any changed or
stale preview invalidates approval.

Obtain separate explicit approval immediately before Apps Common Lookups uses
its core REST client. Submit each displayed request once in preview order and
verify immediately. Stop on the first failure/uncertainty/unverified row;
retain successes and unattempted rows without retry, rollback or another
fallback. REST uses no Data Loader session/ZIP/context/approval; missing loader
context is never an eligibility reason. No Delete route is introduced.

Oracle sources: [26D CSV export/import](https://docs.oracle.com/en/cloud/saas/applications-common/26d/oafsm/using-functional-setup-manager.pdf#page=37)
and [26D Standard Lookup Codes](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/api-standard-lookups-lookup-codes-adf.html).

## Oracle Resource Read Order

1. [ora_input_validation.md](ora-resource/ora_input_validation.md)
2. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
3. [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
4. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
5. [ora_error_handling.md](ora-resource/ora_error_handling.md)
6. [ora_rule_registry.json](ora-resource/ora_rule_registry.json) for the compiled task-node graph

Use the rule planner before consuming the registry and load its execution guide.
The local graph owns CSV recovery, final-fallback eligibility and approval gates.

## Runtime Interface

Use manifest inputs/outputs; retain RequestMode, fixed standard lookup/task,
reviewed ordered rows, live locks, immutable CSV evidence or failure/recovery/
reconciliation receipts, and route-owned preview/approval. No reference-set
selection applies. Classify and redact errors through the local error rules.

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Offline Validation Evidence

Use [golden-scenarios.md](tests/golden-scenarios.md) for synthetic requests and
source-reviewed outcomes. The suite checks current source/registry equivalence,
all-operation entry applicability, graph prerequisites and terminal boundaries:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s pillars/cx/sales/opportunities/manage-sales-stage-phase-codes/tests -p 'test_*.py' -v
```

These checks do not execute Fusion or evaluate natural-language field rules.
