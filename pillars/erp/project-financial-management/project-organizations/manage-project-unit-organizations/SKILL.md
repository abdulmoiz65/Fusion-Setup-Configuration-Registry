---
skill_id: "erp.project-financial-management.project-organizations.manage-project-unit-organizations"
name: "Manage Project Unit Organizations Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Project Unit Organizations under the Project Organizations functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
task_code: "PJF_MANAGE_PROJECT_UNIT_ORGANIZATIONS"
task_name: "Manage Project Unit Organizations"
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
version: "0.7.3"
inputs:
  - "project_id"
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "ProjectUnitName or ExistingOrganizationName"
  - "required ProjectUnitCode; optional EffectiveStartDate, EffectiveEndDate"
  - "optional ExistingClassification, ExistingLocation; selected OrganizationId"
  - "optional ordered Rows of Project Unit requests for bulk intake"
outputs:
  - "Organization.dat and immutable HDL archive"
  - "all-row validation report and one archive per derived action when bulk input is valid"
  - "terminal or resumable Data Loader monitoring result"
  - "routing, eligibility, and post-load evidence"
  - "durable acceptance binding and request-ID resume context"
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-project-unit-organizations/current/execution-receipts/"
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
  - "Routes each explicitly approved immutable Organization HDL archive through core.data-loader."
  - "Performs read-only Data Loader status monitoring and post-load organization verification only on a later explicit status request."
  - "Persists redacted acceptance bindings, run records and token usage through declared core project services, without additional Fusion calls."
required_privileges:
  - "Fusion privileges required by core.data-loader for Organization HDL upload, initiation, status, and diagnostic retrieval."
  - "Read access to organizations, classifications, and Project Unit extra information used by the declared verification route."
---

# Manage Project Unit Organizations

Reviewer group: ERP project financial management pillar reviewers.

## Purpose

Support exactly two actions: `CREATE_NEW` creates a new organization classified as
a Project Unit; `USE_EXISTING_ORGANIZATION` adds the Project Unit classification
and code to an eligible existing organization without creating or renaming it.
The existing flow starts its DAT with an Organization MERGE anchor containing the
selected organization's existing identity and classification; that anchor does
not authorize a new organization or an identity change.
For one organization, generate one `Organization.dat`. For bulk input, normalize
the ordered rows, validate every row, and generate one `Organization.dat` and ZIP
per derived action only when every row passes. Route each approved ZIP through
`core.data-loader`. Direct REST writes, FSM CSV writes, updates to existing
Project Units, deletes, declassification and organization-tree changes are out of scope.

The developer-provided **FSCR input specification: Manage Project Unit
Organizations** supplies the tenant-tested HDL contract. Its findings correct the
previous source-key contract: omit SourceSystemOwner, SourceSystemId, SetCode and
reference-data-set values; use EFF category PRJ_PROJECT_UNIT and context
PRJ_PU_ATTRIBUTES. The current user-approved task policy does not perform a
cross-Project-Unit code uniqueness search before HDL generation. These findings
have not been independently retested in a tenant during authoring.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Required workflow

For a later explicit status request, PUORG.VALIDATE_INPUT validates the retained
same-target task, request identity and approved archive context from the durable
acceptance binding in [ora-resource/ora_dependency_readiness.md#execution-persistence-and-resume-contract](ora-resource/ora_dependency_readiness.md#execution-persistence-and-resume-contract), then takes
`status_requested` directly to PUORG.STATUS_REQUEST_GATE and step 9 below. Do not
rerun organization discovery, defaults, generation, approval or submission.
Missing or conflicting prior context blocks this resume route.

For bulk input, run the routed validation, lookup, routing, defaults, dependency
and design gates for each row. A row's terminal issue ends that row's path while
the other rows are still checked. Hold every `PUORG.EXECUTION_GATE` until the
whole batch is ready; then run the execution, completion and verification gates
per action archive, with verification for each member row. Any blocked row
prevents all archives and all loader calls for that batch.

1. Resolve project context, exact target and catalog flags. Perform
   [Task Plan Validation and Execution](#task-plan-validation-and-execution)
   against the shipped registry and its six owning resource files before
   consuming the graph. Record a `planned` / `ready` plan without an override.
   Resolve `project_id` and the append-only receipt destination, artifact
   registration, run-record and token-log paths before execution. Missing project
   identity, unavailable core project services or an unsafe/unwritable destination
   blocks submission. Read the execution-persistence contract before preparation
   or status handling.
2. Accept one request or an ordered table/CSV/JSON batch. Normalize a batch to
   `Rows` with stable 1-based row numbers and preserve every supplied name/code.
   Present all input issues in one row report. A blank name or code blocks its
   row. When a code is missing, show a suggested code derived from the requested
   organization name and ask whether to use that suggestion or enter a code
   manually. For an existing organization, derive the suggestion from the
   requested name, which must later match the exact selected name. Form the
   suggestion by trimming and uppercasing the name,
   replacing characters outside A–Z, 0–9 and underscore with underscores,
   collapsing repeated underscores, and limiting it to 150 characters. If
   that yields only underscores, offer manual entry alone. For bulk input, show
   all missing-code rows and suggestions
   together and ask for all choices in one request. Do not place a suggestion
   into the request without the user's explicit choice, silently drop invalid
   rows, or submit a valid subset.
   For each row, validate the requested organization name and code. Dates are
   optional. Select
   read-only lookups through `core.fusion-api.rest-api-client` at
   PUORG.FIND_ORGANIZATION only after identity, privilege, catalog, metadata,
   artifact destination and client preflight passes. Discover the tenant version
   and metadata, then derive Action from the organization-search outcome; never
   ask the user to select it. Lookup contracts are in `ora_reference_lookups.md`.
3. Run the routed lookup and eligibility steps for every row, collecting row
   outcomes before packaging. For CREATE_NEW, exclude existing organization-name collisions to prevent HDL
   MERGE from updating a parent. For USE_EXISTING_ORGANIZATION, resolve optional
   location/classification filters, group results by OrganizationId and select an
   exact ID and classification record. Duplicate names or locations require user
   selection. Retrieve all classifications for the selected ID without narrowing
   filters; preserve returned names and intentional whitespace. After selection,
   resolve the exact display label for the selected returned ClassificationCode
   through organizationClassificationsLOV. Do not generate the existing action's
   Organization anchor until both lookups are exact and target-bound.
4. Default an omitted start date to `0001/01/01` only for CREATE_NEW; existing flow derives
   the selected organization's relevant start date. Require a user-supplied
   or explicitly accepted Project Unit Code for both actions and preserve it
   exactly. A suggestion is not a default. Validate dates
   and eligibility, including
   absence of active PRJ_PROJECT_UNIT classification on the requested date.
5. Validate Project Unit Code as a nonblank string of at most 150 characters.
   Preserve the supplied code exactly, do not impose an unverified
   business regex, and apply configured value-set validation when available. Do
   not perform or require a cross-Project-Unit code uniqueness search.
6. Check duplicate organization names and Project Unit codes across the entire
   batch. Report every row's outcome
   together. If any row has an issue, stop before creating or submitting any
   archive. Once all rows pass, group them by derived action. A DAT has one
   METADATA header per component and one MERGE line per row for that component;
   the new and existing actions have different component headers/order, so a
   mixed batch produces two ZIPs. ZIP each DAT at root with no other members;
   validate structure and exact agreement with normalized request/evidence.
7. Produce an immutable preview showing target, every row number/action/name/code,
   selected ID and exact parent classification when applicable, dates, every
   component/field, lookup evidence, warnings, archive membership and SHA-256.
   Pass each archive to `core.data-loader`; its approval workflow is authoritative.
   Approval never waives validation or authorizes a retry.
8. Submit each approved archive exactly once through `core.data-loader`. Treat an
   accepted initiation response as `In Progress`, not load completion, and take
   PUORG.EXECUTION_GATE's `initiated` transition directly to PUORG.RETURN_IN_PROGRESS.
   Return the core `Data Load In Progress` report with its exact Data Set Name and
   `Content ID(Request ID)` values. Before leaving the execution gate, retain the
   server-issued request ID and its approved-archive binding through the declared
   core project services, as specified in the execution-persistence contract.
   This local handoff creates no extra Fusion calls or user-facing reports.
   Do not query status, counts or errors, run post-load
   verification, or mark the task complete in this submission request. A missing
   usable request ID is indeterminate: report the issue without resubmitting or
   starting automatic recovery calls. Use `ora_error_handling.md` for failures.
   A persistence failure takes `persistence_failed` to PUORG.RETURN_ISSUES;
   preserve the known request ID in the response, stop and repair local state
   without submitting again. Accepted initiation remains accepted even when
   persistence fails.
9. Only on a later explicit user request for status, progress, results, counts or
   errors, resume PUORG.STATUS_REQUEST_GATE using its `status_requested` transition to
   PUORG.LOAD_COMPLETION_GATE. Load the registered acceptance binding from the
   selected project and bind the Request ID to the same target, task and approved
   archive context; a missing or mismatched identity blocks
   monitoring. Do not repeat preparation, approval or submission on this route.
   Delegate the requested check to `core.data-loader` and follow its complete
   request-ID reporting contract, including status, counts and applicable
   diagnostics. A nonterminal result or bounded polling timeout returns
   `In Progress`; return the last status and next-check path, and wait for another
   explicit status request rather than automatically starting another polling
   slice. Terminal failure stops without post-load verification or resubmission.
10. Only after PUORG.LOAD_COMPLETION_GATE accepts the Core Data Loader terminal
   success evidence, run PUORG.VERIFY_POST_LOAD through the declared read-only
   route for every row in that archive. Require an active PRJ_PROJECT_UNIT
   classification on the effective date and a sequence-1 PRJ_PU_ATTRIBUTES row
   containing the exact requested Project Unit Code for each row.
   Terminal loader success alone is not task success. On a missing or mismatched
   record, preserve the receipt, report failed verification and do not resubmit.
   Mark the requested setup task complete only after both checks pass; an
   already-defined no-load outcome remains a separate terminal result.
11. Persist preparation artifacts and explicitly required verification deliverables
   under the manifest's project paths using the declared core project services.
   Record the acceptance handoff, each later status result and partial failures
   in append-only project evidence, with skill-run and token-usage records.
   Keep core Data Loader's concise response and restrictions on unsolicited
   user-facing reports; project continuity records belong to the declared
   project services. Never depend on chat history as the sole durable store.
   Maintain Project Organizations remains a separate downstream task.

## Task Plan Validation and Execution

Build `setup_task_plan` locally by assisted inspection of
[the shipped registry](ora-resource/ora_rule_registry.json) and its six owning
`ora-resource/ora_*.md` files. No authoring tool, planner script, external call or
repeat organization discovery is needed for this graph-contract check.

- Select exactly one `PJF_MANAGE_PROJECT_UNIT_ORGANIZATIONS` / `Manage Project
  Unit Organizations` entry in the nested schema `3.0` registry. Require task and
  reachable-node readiness `ready` without blocking reasons; stored flags alone
  are insufficient.
- Confirm unique node IDs, start node `PUORG.VALIDATE_INPUT`, supported actions,
  existing prerequisite/transition targets and terminating paths. Resolve each
  source file inside this task's resource folder and its heading. Match each node
  to exactly one source Task Nodes row by Rule ID; compare type, sequence, action,
  transitions, prerequisites, failure behavior and applicability. Source line
  numbers are navigation hints. Read owning rules and each named resolver's one
  definition, including inputs, authority, matching, outputs and failure behavior.
- Missing, unresolved, ambiguous or inconsistent required contracts block the
  plan. Do not repair the registry, invent evidence or bypass the declared client.
  After these checks pass, record `status: planned`, `validation.status: ready`,
  task identity, start node, checked sources and validated nodes through the
  declared project services and task workspace paths. Recheck the current graph
  for each new run or changed rule source; no readiness override is allowed.

On a failed local check, stop before further acquisition/preparation or status
handling. Record a redacted diagnostic with stage, failure class, task/target,
blockers and one safe next action; use `input_validation` or
`catalog_or_metadata_mismatch` for input or rule-contract gaps, preserving actual
delegated-operation failures. Graph inspection is not a new approval or evidence
that an organization or accepted load has been verified.

Begin at `PUORG.VALIDATE_INPUT`, satisfy prerequisites, evaluate applicability,
apply only reached rules and follow each observed declared outcome to a terminal.
Record sanitized path/outcomes and evidence; never run all nodes by sequence or
invent an outcome. Preserve the per-row/batch execution hold above. A later
explicit status request follows `status_requested` with its registered binding;
it never repeats preparation or submission.

For Data Loader's read-only Task Hook on the final immutable HDL archive, evaluate
applicable preparation rules and use `PUORG.EXECUTION_GATE`'s `prepared` outcome
to `PUORG.RETURN_PREPARED`. This phase requires complete preparation and verified
preflight, not upload approval, server acceptance or post-load evidence. It
authorizes no submission. Data Loader then owns its normal preview, approval and
submission; the outer workflow records `initiated` only after actual acceptance
and successful local persistence. Never mark lifecycle checks passed early.

Retain the normalized request fingerprint, current node, path/outcomes, sanitized
resolver/default evidence, missing requirements and safe resume stage in the
task's preparation evidence. Return task identity, actual stage/outcome, blockers
and one safe next action. Resume preparation with matching fingerprints and
refreshed changed evidence. Changed intended inputs, target or upload artifact
require fresh validation/approval. Later approved submission follows Data Loader's
retained-artifact integrity checks without original-source rereads or live
revalidation. Status/recovery uses only the existing acceptance-binding contract;
do not copy loader artifacts or replay an uncertain write.

## Offline helper

`scripts/validate_project_unit_organization_hdl.py` generates the two documented
templates and validates ZIPs. It makes no network calls and never loads data.

```bash
python <skill>/scripts/validate_project_unit_organization_hdl.py \
  --request request.json --evidence evidence.json --dry-run
python <skill>/scripts/validate_project_unit_organization_hdl.py \
  --request request.json --evidence evidence.json --output <workspace>/Organization.dat
python <skill>/scripts/validate_project_unit_organization_hdl.py \
  <workspace>/Organization.zip --action USE_EXISTING_ORGANIZATION
python <skill>/scripts/validate_project_unit_organization_hdl.py \
  --batch --request batch-request.json --evidence batch-evidence.json \
  --output-dir <existing-workspace-dir> --report <workspace>/row-report.json
python <skill>/scripts/validate_project_unit_organization_hdl.py \
  <workspace>/ProjectUnitCreate.zip --batch --action CREATE_NEW
```

Batch request JSON has `TargetEnvironment` and a nonempty ordered `Rows` array.
Each row requires `ProjectUnitCode` and uses the other fields of a single
request, without `Action` or
`OrganizationId`. Batch evidence JSON has the same target and a `Rows` array in
the exact same order, with one complete resolver evidence object per request
row. The helper reports each row's derived action, name, supplied code, evidence
reference and issues; missing-code rows include `SuggestedProjectUnitCode` when
a usable name-derived suggestion exists. The suggestion is never written to HDL
until the user accepts it and the chosen value is supplied as `ProjectUnitCode`.
`Status: blocked` yields no ZIP; `Status: ready` yields
`ProjectUnitCreate.zip`, `ProjectUnitExisting.zip`, or both. Each ZIP contains
only `Organization.dat`. Preserve row order within each action; the report maps
archive action back to input rows. Use `--batch --dry-run` to preview without
writing archives. The helper does not perform lookups; use the routed workflow
to establish and verify evidence for every row.

Generation refuses overwrite. ZIP-only validation establishes structure, not
tenant eligibility, evidence freshness or approval. Always pass the expected
action when validating an import; compare its DAT to regenerated output.

Internal Request JSON uses `TargetEnvironment`, one requested organization name
(`ProjectUnitName` or `ExistingOrganizationName`), optional `ProjectUnitCode`,
`EffectiveStartDate`, `EffectiveEndDate`, `ExistingClassification`,
`ExistingLocation`, and optional `RequiredTreePlacement` (`TreeCode` and
`ParentOrganizationName`). It must not contain `Action` or `OrganizationId`: the
offline validator derives the action from target-bound organization-search
evidence, and keeps IDs in that evidence and the preview only. Neither appears
in generated HDL.

Evidence JSON is an internal, normalized resolver contract:
- Common: matching `TargetEnvironment`, `EvidenceRef`, and `Fresh: true`.
  `CodeValueSetValidation` is `passed` or `unavailable`; passed evidence includes
  exact `ValidatedProjectUnitCode`. Code-search completeness and a global list of
  Project Unit Codes are not required.
- Routing: `OrganizationSearchComplete: true` and complete
  `ActiveOrganizationMatches`. No matches derives `CREATE_NEW`; exactly one
  exact active match, with complete classification evidence, derives
  `USE_EXISTING_ORGANIZATION`; an active `PRJ_PROJECT_UNIT` classification is
  an already-defined stop outcome; multiple matches require explicit selection.
  Preserve the complete distinct-ID match list and set `SelectionConfirmed=true`
  only after the user selects an exact matching OrganizationId. The validator
  accepts that confirmed selection without discarding the other matches.
- Existing: the selected matched `SelectedOrganization` with OrganizationId, exact Name,
  ClassificationCode, optional exact returned ClassificationName, LocationId,
  EffectiveStartDate, EffectiveEndDate and normalized `Active: true`;
  `ResolvedOrganizationClassification` with the exact ClassificationCode,
  organizationClassificationsLOV ClassificationName and resolver EvidenceRef;
  `ClassificationsComplete: true` and `Classifications` containing every
  returned classification for that ID with code, exact display name, status
  and effective dates. REST dates may be retained as YYYY-MM-DD evidence and are
  normalized to YYYY/MM/DD for HDL; normalized YYYY/MM/DD evidence is also
  accepted. Active classification status is A. Selected parent classification
  must also be active on the date, and any returned display name must agree with
  the LOV result.
- Tree placement: when `RequiredTreePlacement` is supplied for an existing
  organization, `TreePlacementEvidence` must be fresh and contain the exact
  tree code, active tree-version ID, parent and child IDs/names, effective
  dates, and `PlacementExists`. The validator returns
  `REUSE_EXISTING_TREE_PLACEMENT` only for an exact effective relationship;
  otherwise it returns `MANAGE_ORGANIZATION_TREES_REQUIRED`. A newly created
  project unit returns `MANAGE_ORGANIZATION_TREES_REQUIRED_AFTER_POST_LOAD`.
  This is a read-only routing decision, never an organization-tree write.
- When location is supplied: `SelectedLocation` contains LocationId,
  exact LocationName and normalized `Active: true`.

Completeness/freshness booleans are resolver attestations, not raw REST fields
or user substitutes for evidence. The workflow must verify provenance, target,
timestamp, pagination, unfiltered classification scope and selection before
setting them. Never fabricate these flags to unblock generation.

## HDL contract

| Action | Exact component order | Parent reference |
|---|---|---|
| CREATE_NEW | Organization, OrgInformation, OrgUnitClassification | New name and Project Unit Classification |
| USE_EXISTING_ORGANIZATION | Organization anchor, OrgUnitClassification, OrgInformation | Exact returned existing name, classification code, and LOV display name |

Each component has exactly one METADATA header and one MERGE row per organization;
the script's HEADERS defines the exact headers from specification section 7.
Create sections share
YYYY/MM/DD dates. Existing child sections share their requested/defaulted dates;
the Organization anchor always uses the selected organization's returned start
date normalized to YYYY/MM/DD and a blank end date. SequenceNumber is 1, active status is A,
FLEX:PER_ORGANIZATION_INFORMATION_EFF is PRJ_PU_ATTRIBUTES, EFF_CATEGORY_CODE is
PRJ_PROJECT_UNIT, OrgInformationContext is PRJ_PU_ATTRIBUTES, and the code alias is
`projectUnitCode(PER_ORGANIZATION_INFORMATION_EFF=PRJ_PU_ATTRIBUTES)`.

Organization.ClassificationCode in create and OrgUnitClassification.ClassificationCode
in existing flow are PRJ_PROJECT_UNIT. The existing Organization anchor instead
uses the exact selected non-PRJ_PROJECT_UNIT ClassificationCode and its exact LOV
display label:

```text
METADATA|Organization|EffectiveStartDate|EffectiveEndDate|Name|ClassificationCode|ClassificationName
MERGE|Organization|{{existingEffectiveStartDate}}||{{existingOrganizationName}}|{{existingClassificationCode}}|{{existingClassificationName}}
```

Never put PRJ_PROJECT_UNIT or Project Unit Classification in that anchor; those
values belong only to the later Project Unit classification/EFF additions. The
existing ClassificationName is a parent key, not the classification being added.
User names/classification labels have a 240-character limit; codes have a
150-character limit. No tenant-independent business regex is imposed on supplied
codes. Raw HDL delimiters/control characters block serialization until a supported
escaping contract is supplied.
