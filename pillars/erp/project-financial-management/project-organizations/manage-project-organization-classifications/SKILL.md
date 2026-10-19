---
skill_id: "erp.project-financial-management.project-organizations.manage-project-organization-classifications"
name: "Manage Project Organization Classifications Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Project Organization Classifications under the Project Organizations functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
task_code: "PJF_MANAGE_PROJECT_ORGANIZATION_CLASSIFICATIONS"
task_name: "Manage Project Organization Classifications"
parent_skill_id: "erp.project-financial-management.project-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "HDL"
businessObject: "Organization"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.6.2"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "organization_name, optional requested_target_classification and optional pto_permissions"
  - "bulk target_environment and organizations array; explicit existing-update opt-in per organization"
  - "fresh target-bound resolver, schema and persisted mapping evidence"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "Organization.dat or verified ALREADY_CONFIGURED"
  - "up to two immutable PEO/PTO Organization archives and per-archive manifest"
  - "load receipt, classification verification and maintenance follow-up status"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.apps-common.lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-organization-classifications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-organization-classifications/current/"
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
  - "Reads declared organization/classification, lookup and HDL metadata through core clients; consumes already registered original PTO row identity only for an explicit existing update."
  - "Submits an authorized immutable Organization archive through core.data-loader."
  - "May create a confirmed-missing source-owner code through core Apps Common Lookups after exact-payload approval."
required_privileges:
  - "Read organization classifications, lookup codes and HDL metadata."
  - "Upload and load Organization HDL when approved."
  - "Create lookup codes only for the approved missing-owner branch."
---

# Manage Project Organization Classifications

## Purpose

Resolve an existing effective organization through governed organizations REST and configure only requested PTO, PEO or both using HCM Data Loader. REST independently determines PA_PROJECT_ORG and PA_EXPENDITURE_ORG existence; exports never determine whether to create classifications.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

For `scripts/resolve_project_organization_baseline.py`, pass
`--rest-framework-version <version resolved from the selected core workflow>`
for both single and bulk execution. There is no numeric default; unresolved
version selection blocks `--execute` before authentication or network access.
The exact-name filter remains a single equality and retains all classifications.

## Permission and Omission Contract

**Omitted classification input means preserve existing state.**

For new PTO, use only the user's permission input: Enable/Enabled/Y is Y, Disable/Disabled/N is N, Boolean values normalize to Y/N and each omitted indirect/capitalization/billing flag defaults N. Do not export to obtain, compare, default or require existing permissions; all-N does not block local preparation under the latest instruction. Preserve PEO unless explicitly requested. Never create a classification that REST proves exists.

For existing PTO with explicit permission input in a legacy single request, or an explicit bulk update opt-in, write only supplied normalized flags directly, without comparing old values. Omitted existing permission columns preserve target state. Original authoritative OrgInformation source keys remain mandatory for an update. Consume already available registered task-export identity evidence only; do not initiate an export to get permission values. Missing update identity blocks that update, never selects new PTO or fabricates keys. No explicit mutation means no DAT, ZIP or mutation approval.

## Catalog and Execution Contract

- task_code: PJF_MANAGE_PROJECT_ORGANIZATION_CLASSIFICATIONS
- dataloader_import_mode: HDL
- businessObject: Organization

HCM Data Loader through core.data-loader is the only write/import route; never FSM import. Bulk processing of existing organizations is supported. Parent creation, removal/declassification, reactivation, date overrides and tree/ESS processing are outside this task.

## Bulk Request and Preparation

The bulk envelope has exactly `target_environment` (the configured target HTTPS origin) and a nonempty `organizations` array. Each entry accepts `organization_name`, optional `requested_target_classification` (`PTO`, `PEO`, `BOTH`, or a unique list of PTO/PEO), optional `pto_permissions` (`indirect`, `capitalization`, `billing`), optional `source_system_owner`, optional `source_system_ids` (new `PTO`, `PTO_INFO`, `PEO` component keys), and optional Boolean `update_existing_pto_permissions` (default false). Reject duplicate exact names and unknown fields. Legacy single-organization requests remain supported.

Bulk creation permissions apply only to REST-confirmed missing PTOs. Set `update_existing_pto_permissions: true` with supplied permission fields only for an explicit existing-PTO update; original authoritative OrgInformation keys remain required. Existing PTOs otherwise remain unchanged even when a BOTH request includes new-PTO permission input. Omitted existing fields are never filled from export or defaulted N.

Use `resolve_project_organization_baseline.py --bulk-request <request.json> --run-id <current-run-id>` with the existing target/project/date/output gates. Collect a separate fully paginated REST baseline per organization; no baseline reuse across names. Complete all identity/state checks before preparing any output. `plan_request` dispatches bulk requests to `plan_bulk_request`; `allocate_bulk_mappings` proposes keys only, which must be registered through declared core project services before generation. Bind each persisted mapping to its organization, target, current validation run, collection timestamp, effective date, baseline reference and normalized delta. Reject repeated parent IDs, baseline references and component keys across the batch and collisions with the complete persisted ledger.

`generate_bulk_dats` produces at most two payloads. PEO has one Organization.dat, one OrgUnitClassification METADATA layout and one PEO MERGE per requested missing PEO. PTO has one Organization.dat, one classification layout for new PTO rows and one OrgInformation layout/row per new PTO; verified explicit existing updates emit information rows only. Both files retain the metadata-only Organization anchor and never a parent MERGE. Multiple numeric parent OrganizationIds are allowed. An active effective existing PTO or PEO satisfies the prior-classification requirement; adding the missing other role never requires an unrelated third classification. No-op organizations appear in the plan only; they have no payload, ZIP or approval. A failed organization blocks the entire preparation before any ZIP is written.

One PTO file has one information-column layout. Explicit existing updates can share it when they supply the same fields; when mixed with new PTOs, all three values must be explicitly supplied for those updates. Incompatible partial updates block preparation with guidance to supply compatible explicit fields or use separate compatible requests; never fill omitted existing permissions to combine layouts.

Run the local generator with `--request <request.json> --evidence <trusted-evidence.json> --dry-run`. After mappings are persisted, `--output-dir <existing-project-artifacts-directory> --project-root <project>` writes PEO-Organization.zip and/or PTO-Organization.zip plus bulk-classification-manifest.json, refusing overwrite. Each ZIP has its own SHA-256, organization/baseline bindings and required gates. Validate archives using positional `<archive.zip> --bulk-role PEO` or `PTO`; structural validation alone does not authorize a load.

Apply workflow steps 6–10 independently to each ZIP. Preflight, Task Hook preview, immutable approval, once-only submission and durable acceptance binding belong to the submission request, which ends In Progress. Only a later explicit status/results/verification request selects status checks and requested post-load readback. Approval or success of one ZIP does not authorize or complete the other. Persist separate role/checksum/request-ID/status/readback records, preserve partial successes and never replay failed, timed-out or uncertain submissions.

## Required Workflow

1. Select existing project, configured target, task/catalog identity and privileges. Perform [Task Plan Validation and Execution](#task-plan-validation-and-execution) using the shipped registry and its six owning resource files; record a `planned` / `ready` plan without an override before consuming the graph.
2. Validate single input or all bulk entries, supplied names/permission types, explicit PTO/PEO/both scope and bulk existing-update opt-in. Do not require old flags.
3. Run scripts/resolve_project_organization_baseline.py through the governed core GET route. Complete exact-name/effective-date pagination, select one effective identity, retain all classification rows. Missing, ambiguous, incomplete, inactive or conflicting REST results stop. Resolve PTO/PEO independently before defaults; never use export absence to create duplicates.
4. CHECK_PERMISSION_UPDATE determines from REST plus explicit supplied permissions whether an existing PTO update is requested; bulk additionally requires update_existing_pto_permissions=true on that entry. Resolve only flagged existing updates. Additions/no-op bypass RESOLVE_UPDATE_IDENTITY entirely. The former PORGCLASS.RESOLVE_EXPORT_BASELINE node and pre-import task-export execution are removed.
5. plan_request computes only explicitly requested missing classifications. New PTO defaults omitted flags N and writes supplied normalized values. PEO-only and new PTO need neither ClassificationsExport nor current permissions nor existing PTO keys. Existing updates verify already registered original OrgInformation keys/target/date/run/provenance only, without reading Permissions or triggering export.
6. For mutation, verify enabled/effective source owner and complete core Organization metadata through build_schema_evidence. Original update owner is preserved; confirmed missing new owner creation is separately approved.
7. Allocate and persist keys only for new components, bound to the REST baseline and normalized delta. generate_dat emits the legacy single payload; generate_bulk_dats groups all active organizations into PEO/PTO payloads. Both use Organization METADATA only, new classification rows only for REST-confirmed missing requested targets and original-key information rows only for explicit existing updates. Validate all entries before writing any artifact. No matching-value comparison/no-op is claimed.
8. Validate exact request/evidence/header/identity equality. Show target, additions, supplied/defaulted new permissions, partial existing update fields, preserved state, DAT/ZIP/checksum. Retain core Data Loader's Task Hook and immutable approval gates.
9. Submit each nonempty role ZIP once via core.data-loader after its own gates; register the returned ID/checksum/approval and target/project/task/role binding per ZIP. Return In Progress without polling, logs, exports or post-load reads. A persistence failure preserves any known ID and stops; repair local evidence without submitting again. No-op organizations have no artifact or approval request.
10. Only on a later explicit status/results/verification request, resume from matching registered per-ZIP bindings through PORGCLASS.STATUS_REQUEST_GATE. Missing/mismatched context blocks; never repeat preparation, approval or submission. Delegate status/count/error checks to core.data-loader. A status-only request returns that status; active status or timeout returns In Progress and waits for another request. Terminal failure stops. For requested setup verification after terminal success, verify all included classifications and parents through fresh governed reads; a fresh same-task export may verify permissions/preservation but never supplies pre-import flags. Missing readback blocks completion without changing route or replaying writes. All requested ZIPs must verify before task completion; retain partial success.
11. Persist artifacts/run/token usage through declared core project services; report Maintain Project Organizations as separately scoped follow-up, never invoke it implicitly.

## Task Plan Validation and Execution

Build `setup_task_plan` by local assisted inspection of
[the shipped registry](ora-resource/ora_rule_registry.json) and its six owning
`ora-resource/ora_*.md` files. This check requires no authoring tool, planner
script, external call or new task export.

- Select exactly one `PJF_MANAGE_PROJECT_ORGANIZATION_CLASSIFICATIONS` / `Manage
  Project Organization Classifications` entry in the nested schema `3.0`
  registry. Require task and reachable-node readiness `ready` without blocking
  reasons; do not trust stored flags alone.
- Confirm unique node IDs, start node `PORGCLASS.VALIDATE_INPUT`, supported
  actions, existing prerequisite/transition targets and terminating paths. Resolve
  each source file inside this task's resource folder and its heading. Match each
  node to one source Task Nodes row by Rule ID; compare type, sequence, action,
  transitions, prerequisites, failure behavior and applicability. Source line
  numbers are navigation hints. Read each owning rule and named resolver's one
  definition, including inputs, authority, matching, outputs and failure behavior.
- Missing, unresolved, ambiguous or inconsistent required contracts block the
  plan. Do not repair the registry or invent identity, permission, source-key or
  acquisition evidence. Record `status: planned`, `validation.status: ready`,
  exact task identity, start node, checked sources and validated nodes through
  the declared project services and task workspace paths only after checks pass.
  Recheck for each new run or changed rule source; no readiness override is allowed.

On failure, stop before further acquisition, preparation or status handling and
persist a redacted diagnostic with stage, failure class, task/target, blockers
and one safe next action. Use `input_validation` or `catalog_or_metadata_mismatch`
for input or rule-contract gaps; retain actual delegated-operation failure classes.

Begin at `PORGCLASS.VALIDATE_INPUT`, satisfy prerequisites, evaluate applicability,
apply only reached rules and follow each observed declared outcome to a terminal.
Record sanitized evidence and path/outcomes. Never run all nodes by sequence or
invent an outcome. Preserve the conditional update-identity guard, no-op exit,
all-entry preparation gate and per-ZIP lifecycle. A later explicit status request
uses its registered binding and `status_requested`, without new preparation.

For Data Loader's read-only Task Hook on each final immutable ZIP, evaluate only
applicable preparation rules; `PORGCLASS.EXECUTION_GATE` returns `prepared` to
`PORGCLASS.RETURN_PREPARED` after complete preparation and verified preflight.
This phase requires no upload approval, accepted request or readback. A missing
source owner blocks this phase; never create one or seek its approval inside
Task Hook. Outer workflow step 6 retains the separately approved missing-owner
route before artifact preparation. Data Loader then owns upload preview, approval
and submission; `initiated` still requires actual acceptance and registration.

Retain the normalized request fingerprint, current node, path/outcomes, sanitized
resolver/default evidence, missing requirements and safe resume stage in task-owned
preparation evidence. Return task identity, actual stage/outcome, blockers and one
safe next action. Resume preparation with matching fingerprints and refreshed
changed evidence; changed intended inputs, target or upload artifact require fresh
validation/approval. Later approved submission uses Data Loader's retained-artifact
integrity checks without original-source rereads or live revalidation. Status and
recovery use saved per-ZIP bindings; never copy loader artifacts or replay a write.

## Offline Helpers and Evidence

scripts/validate_project_organization_classifications_hdl.py resolves trusted evidence, plans and serializes locally; no network/export/load call. resolve_classification_state is the REST existence authority. requires_existing_pto_update_identity is the conditional graph guard. plan_request reports export_required=false and update_identity_required. Structural ZIP checks alone cannot prove metadata, identity or approval.

scripts/resolve_classification_export.py remains a read-only parser for already registered identity evidence or post-load verification, not a mandatory permission baseline. Target filenames/headers/keys must be proven, never inferred. See ora_reference_lookups.md#execution-evidence-contract.

```bash
python3 pillars/erp/project-financial-management/project-organizations/manage-project-organization-classifications/scripts/validate_project_organization_classifications_hdl.py --request <request.json> --evidence <trusted-evidence.json> --dry-run
```

## Durable Artifacts and Review

Use the manifest's selected project paths and declared artifact-version, artifact-registry and project-state services for plans, immutable preview/approval, mappings, original identity evidence, acceptance/status/readback, skill runs and token usage. Preserve request IDs and partial diagnostics. Never persist credentials/tokens. Required reviewers: ERP Pillar Lead/SME, FSCR A-Team/core and QA.
