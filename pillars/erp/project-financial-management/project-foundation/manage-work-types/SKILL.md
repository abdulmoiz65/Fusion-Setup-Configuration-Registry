---
skill_id: "erp.project-financial-management.project-foundation.manage-work-types"
name: "Manage Work Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Work Types under the Project Foundation functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_WORK_TYPES"
task_name: "Manage Work Types"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.1.4"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "work_type_use_evidence"
outputs:
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-work-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-work-types/current/"
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
  - "Persists declared task plans, validation evidence, state and token-usage records through the listed core project services."
  - "Delegates scoped exports and approved imports to the declared shared/core workflows under their existing gates."
required_privileges: []
---

# Manage Work Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Work Types` under `Project Foundation`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_WORK_TYPES`
- task_name: `Manage Work Types`
- parent_skill_id: `erp.project-financial-management.project-foundation`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Foundation`
- functional_area_code: `ORA_PJF_PROJECT_FOUNDATION_FA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Work Types` under `Project Foundation`.

## Supported Task Behavior

Create, update, or end-date work types with effective dates, billable/utilizable indicators, cost- or revenue-transfer classification, translations, and optional reference-data-set assignments. Preserve omitted groups and validate downstream billing, cross-charge, utilization, and transaction impacts.

Use task-scoped FSM CSV; the Work Types LOV is read-only and is not a setup-write contract.

Reference data set assignments are optional user input. Do not pause a create or ask for a set merely because assignments are omitted; do not invent a Common Set assignment. Resolve sets only when supplied or explicitly changed, and preserve omitted assignment groups on updates. Validate the current target CSV member/header and omitted-row semantics through verify_work_type_package before preview. A required child CSV member does not itself require an assignment row. If the target package cannot represent the requested omission, report the evidenced package-contract gap through the existing issues path rather than imposing a blanket mandatory-set question or switching execution routes.

## Setup Task Metadata

- Task name: `Manage Work Types`
- Task code: `PJF_MANAGE_WORK_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Apply initial input validation before authentication or export. Record unavailable DFF metadata authority as a nonblocking warning, then continue the selected workflow's supported baseline acquisition and checks.
2. Follow the validated registry graph using the Task Rule Execution instructions below. Resolve supplied translation language identities through the declared languagesLOV read using the existing shared REST client; installation/activation status alone does not prove import eligibility. Retain unresolved warnings while completing all remaining supported checks.
3. Build only explicit base/child diffs using target-validated members.
4. Validate identity/dates, flags/transfer semantics, sets, and translations/DFFs for every change. For an existing identity with an actual billable/utilizable/transfer, availability-date or set-assignment diff, require the `work_type_use_evidence` caller handoff and evaluate it through `resolve_work_type_use`. Its Consumer Impact Evidence Contract owns source traceability, target/identity, freshness, completeness, counts, dates and profile checks. Missing or invalid evidence blocks affected import preparation; no consumer/profile acquisition adapter is declared by this task. Record the workflow gap and stop instead of substituting a lookup, manual snapshot or warning. For a new unique identity, record absence evidence from the complete fresh target baseline; unchanged impact fields require no historical-use check.
5. For an import, delegate the prepared package to `core.data-loader`. After its normal validation produces the final immutable archive and verified persisted preflight, use its `core.data-loader.task-hook` `data-load` route to evaluate the read-only task rules. Return ordered `ruleResults` before the loader's preview and approval gate; keep detailed changes and integrity values internal. Any correction that changes the archive requires fresh preparation, preflight and task validation before preview.
6. Let Data Loader retain the Task Hook preview and display its prescribed approval-required report. Data Loader owns approval, archive verification and submission; do not add a task-local approval or retry automatically. Accepted initiation is terminal for that request and means in progress, not verified setup completion. Only when the user explicitly requests status/results/verification, follow the loader's status workflow and the supported same-task export, read-only LOV and dependent-consumer verification workflow before reporting a successful setup change.

Updates preserving translations/DFFs do not require their optional lookups.
Required consumer-impact evidence is a separate gate: unresolved acquisition,
missing or invalid evidence cannot be classified as `REFERENCE_UNRESOLVED`,
cleared by execution approval, or reported as successful preparation. A
Description-only or translation/DFF-only change records this gate as not
applicable when the compared baseline/diff proves flags, dates and sets unchanged.
Missing supported DFF metadata authority or unverified reference eligibility is
`REFERENCE_UNRESOLVED`, severity Warning, `blocking=false`. Preserve supplied
values in their proven CSV representation, list skipped checks and next evidence
needed, and continue supported validation/preview without a waiver or manual
metadata snapshot. Do not claim full validation, invent codes or segment mappings,
or use developer tools or undeclared exports as runtime fallbacks. Ask only when
actual ambiguity or a missing representation prevents constructing the payload.
Language resolution establishes catalog identity, not all translation-import
eligibility. Proven invalid values, malformed packages and failed supported reads
(including incomplete pagination) remain errors. No setup mutation is needed for
lookup or preview; the normal Data Loader approval gate remains authoritative.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Foundation`
- Setup task name: `Manage Work Types`
- Setup task code: `PJF_MANAGE_WORK_TYPES`


## Task Rule Execution

Before the graph's preparation checks, build `setup_task_plan` by assisted
inspection of [the shipped registry](ora-resource/ora_rule_registry.json) and its
six owning `ora-resource/ora_*.md` files. This is a local check of task rules,
not an external operation or a call to an authoring tool or planner script.

- Select exactly one `PJF_MANAGE_WORK_TYPES` / `Manage Work Types` entry in the
  nested schema `3.0` registry. Require task and reachable-node readiness `ready`
  without blocking reasons; do not trust stored readiness flags alone.
- Confirm unique node IDs, start node `WTYPE.VALIDATE_INPUT`, supported action
  types, existing prerequisites/transition targets and terminating paths. Resolve
  each source file inside this task's resource folder and its heading. Match each
  node to exactly one source Task Nodes row by Rule ID; compare type, sequence,
  action, transitions, prerequisites, failure behavior and applicability. Source
  line numbers are navigation hints, not proof of source agreement.
- Read the reached rules and each named resolver's one definition, including
  inputs, authority, match rule, outputs and failure behavior. Missing, unresolved,
  ambiguous or inconsistent required contracts block planning. The documented
  `REFERENCE_UNRESOLVED` disposition is a complete optional-reference contract;
  retain it without weakening required impact/collision checks or failed reads.

After those checks pass, record `status: planned`, `validation.status: ready`,
task identity, start node, checked sources and validated nodes in the task-owned
plan using the declared project services and workspace paths. No readiness
override is allowed. On failure, stop before subsequent acquisition/preparation;
record a redacted diagnostic with stage, failure class, target/task, blockers and
one safe next action. Use `input_validation` or `catalog_or_metadata_mismatch`
for invalid input or rule-contract gaps, preserving actual acquisition failure
classes. Recheck for each new preparation run or changed rule source; never
repair the registry or invent a resolver at runtime.

Begin at `start_node`. Before each node, check its `applies_when` and ensure its prerequisites completed successfully, including a supported completion carrying nonblocking warnings. Execute only the declared action, record its sanitized evidence and declared outcome, and follow exactly `transitions[outcome]`. Sequence numbers describe the graph; they do not authorize running all nodes. Stop at the selected terminal. An undeclared outcome, failed prerequisite or failed supported acquisition is a failure, never a successful validation.

Carry `REFERENCE_UNRESOLVED` warnings along declared warning transitions without skipping supported checks or inventing values. `WTYPE.RETURN_SUCCESS` means that the selected validation/preparation completed with its disclosed limitations; approval or a preview does not prove an import completed. Retain the normal `core.data-loader` approval gate for execution, followed by the explicitly requested supported verification workflow before reporting a successful setup change.

Keep task-owned preparation evidence with the normalized request fingerprint,
current node, completed path/outcomes, sanitized resolver/default results,
warnings, missing requirements and safe resume stage. Return task identity,
actual stage/outcome, blockers and one safe next action. Resume preparation only
after comparing fingerprints and refreshing changed evidence; preserve the
captured create date for the same frozen preview. Changed intended business
inputs, target or upload artifact require fresh validation and approval. Later
approved submission follows the retained-artifact rules below, without a live
refresh or original-source reread. Do not copy loader-owned artifacts.

For a Data Loader import, follow [Data Loader Task Hook](../../../../../core/data-loader/task-hook/SKILL.md) after the loader has verified preflight for the final immutable archive. Evaluate the returned rule plan against that prepared package and retained input/evidence context. Aggregate one ordered `ruleResults` item per planned resource with `source`, `status`, `issues`, and `changes`. `WTYPE.EXECUTION_GATE` checks completed task validation/preparation and must allow `WTYPE.RETURN_SUCCESS` before upload approval. Its declined outcome is for a declined task-preparation request, not a second loader approval prompt.

Data Loader calls `build-data-load-preview` with the evaluated results and final archive SHA-256. Under its approval policy, it then uses `approve-data-load-preview` and `verify-approved-data-load-archive`; the returned `taskValidationEnvelope` is persisted and passed unchanged to the loader. Do not construct or modify preview, approval or envelope objects manually. Keep hashes, detailed previews and approval objects internal; follow Task Hook's prescribed evidence persistence without creating task-local copies of loader artifacts. Later submission verifies the retained artifact's approval-bound integrity and context; it does not reopen the original source, rebuild the archive or rerun task rules. A missing/changed approved artifact or context/envelope mismatch requires fresh validation and approval.

Review [synthetic golden scenarios](../../noship/tests/project-foundation/manage-work-types/golden-scenarios.md) when changing task rules. Their graph and expected-evidence checks are offline review evidence; they do not authorize Fusion operations.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `work_type_use_evidence`: conditional captured caller handoff for existing-identity impact diffs; supplied only by a completed supported operation selected by the active workflow. The resolver owns its contract. Absence blocks affected imports; it does not authorize a new acquisition route.

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent skill for sequencing. Supplied reports are observed exports, not blank templates. Track token usage using the manifest policy.
