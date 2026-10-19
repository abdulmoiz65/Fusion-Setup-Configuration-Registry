---
skill_id: "erp.project-financial-management.project-foundation.manage-project-types"
name: "Manage Project Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Project Types under the Project Foundation functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_PROJECT_TYPES"
task_name: "Manage Project Types"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.2.5"
inputs:
  - "project_id"
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "execution_receipt_record"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"

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
persists_project_state: true
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-types/current/"
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
  - "Writes task plans, validation/preview evidence, execution receipts and redacted diagnostics to the selected project workspace through core project services."
required_privileges: []
---

# Manage Project Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Project Types` under `Project Foundation`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_PROJECT_TYPES`
- task_name: `Manage Project Types`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Project Types` under `Project Foundation`.

## Supported Task Behavior

Create or update a set-enabled project type with effective dates, work type, billing, burdening, capitalization, sponsored-project behavior, translations, and class-category children. Enforce burdening and capitalization conditional options and protect identity/set/semantic fields after project or template use. Omitted groups preserve current values.

Use task-scoped FSM CSV for the Project Type base, translation, and class-category members. No exact writable public setup REST contract is declared.

For a minimal create, collect Name, Set, and an explicit From Date for each row, plus the intended inherited financial behavior for the request. Accept a business-labelled table; resolve it through [input validation](ora-resource/ora_input_validation.md#minimal-create-and-multiple-rows). Optional fields and conditional financial groups need not be supplied when their features remain disabled. The current-target package still determines which internal columns must be serialized.

The October 12 screenshots show burdening and billing enabled, separate-item burdening selected, and the component-item checkbox and destination Project/Task fields disabled. For that create, default omitted BurdenAccountFlag to N and leave the destination fields blank; do not ask for a disabled component choice or destination. The earlier blank-create screenshots have a different feature state. Use the [screenshot default boundaries](ora-resource/ora_defaulting_rules.md#create-page-observations) to distinguish displayed UI defaults from the import contract. If no classifications are requested, create no category assignments. This skill's execution route remains FSM CSV through `core.data-loader`.

For task-scoped creation, the requested flags, accounting method, schedule and override choice document intended inherited behavior. Separate supporting billing-design documents and per-burden-code expenditure-type mappings are operational-readiness recommendations, not required inputs for this setup task. Disclose missing readiness evidence without blocking a valid package or claiming downstream accounting/billing readiness.

## Setup Task Metadata

- Task name: `Manage Project Types`
- Task code: `PJF_MANAGE_PROJECT_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export the current Project Type task package.
2. Perform [Task Plan Validation and Execution](#task-plan-validation-and-execution) using this skill, the shipped registry and its reachable source rules. Record a `planned` / `ready` plan without an override before evaluating the graph or preparing the package.
3. Build exact target-validated base, translation, and class-category members while preserving omitted groups.
4. Validate setup data and set, work type, burden schedule/project/task, capitalization, interest schedule, class-category, translation, and use-state references.
5. Produce an immutable before/after preview with child-row diff and checksum.
6. Route the immutable package to `core.data-loader`. A same-request `auto-approve`, `auto approve`, `approve without asking`, or `skip confirmation` instruction authorizes this one load after every validation gate passes; otherwise wait for later approval of the exact preview. Auto-approval never waives validation or authorizes a retry.
7. Before submission, designate a task-local execution-receipt record owned by the pillar's core project services. After `core.data-loader` returns accepted initiation, persist its returned UCM Content ID, Data Loader Request ID, approved package reference/checksum, target, and latest status through those project services. Do not ask the loader to write a report or run record. Return `in_progress`; do not poll, retrieve process logs, call `dataLoaderDataSets` or `dataSetErrors`, or export target state automatically. Accepted initiation does not prove import completion or validate deferred fields.
8. Resume only on a later request in which the user explicitly asks for status, progress, results, counts, errors, or verification for this load. Use the persisted receipt to select the same target and request, then invoke `core.data-loader`'s status workflow with its required result/error checks. A status-only request ends with that status; a request to verify the resulting setup also selects a fresh same-task data export through `shared.setup-export.task-level-export`, after successful load completion and its export prerequisites. Compare the export with the approved changes and preserved groups/children before claiming verified completion. Append observed statuses and evidence to the existing receipt. An active or failed load, incomplete receipt, missing export, or uncertain result cannot be reported as verified; do not resubmit under the old approval.

If submission or receipt persistence fails, record the available identifiers and failure as indeterminate through project services and stop. Do not invent a request ID or replay the write. A later explicit recovery request selects supported read/status routes using the available request or UCM identifier, or a fresh target-state export when identity cannot be recovered. Recovery never authorizes another submission.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Foundation`
- Setup task name: `Manage Project Types`
- Setup task code: `PJF_MANAGE_PROJECT_TYPES`

## Task Plan Validation and Execution

At workflow step 2, build `setup_task_plan` locally from
[the shipped registry](ora-resource/ora_rule_registry.json) and its six owning
`ora-resource/ora_*.md` files. This assisted check requires no authoring tool,
planner script or external call; it does not repeat step 1's export.

- Select exactly one `PJF_MANAGE_PROJECT_TYPES` / `Manage Project Types` entry
  in the nested schema `3.0` registry. Require task and reachable-node readiness
  `ready` with no blocking reasons; a stored readiness flag alone is insufficient.
- Confirm unique node IDs, start node `PTYPE.VALIDATE_INPUT`, existing prerequisite
  and transition targets, and paths ending at the declared terminal nodes.
  Resolve each source file inside this task's resource folder and its heading;
  match each node to one source Task Nodes row by Rule ID. Check node type,
  sequence, action type, transitions, prerequisites, failure behavior and
  applicability against that row. Source line numbers are navigation hints.
- Read each reachable node's owning rules and named resolver definitions,
  requiring exactly one definition per resolver, with declared inputs, sources,
  match rules, outputs and failure behavior. Missing, ambiguous, unresolved or inconsistent
  required contracts block the plan; do not repair the registry or invent a
  resolver during execution. The explicit runtime dispositions in
  [PT-POL-001](ora-resource/ora_reference_lookups.md#dynamic-validation-policy)
  are complete contracts, not missing definitions. Preserve their non-blocking
  `deferred_to_fusion` outcomes; they do not waive static plan validation.

Only after these checks pass, record `status: planned`, `validation.status: ready`,
exact task identity, start node, validated nodes and checked source references
in the existing task-owned plan artifact using the declared project services.
On failure, stop before subsequent lookups or package preparation; persist a
redacted diagnostic with stage, failure class, task/target, blockers and one safe
next action. Use `input_validation` or `catalog_or_metadata_mismatch` as applicable.
No readiness override is permitted. Revalidate for each new preparation run or
changed task source; a prior plan is not evidence that the current rules passed.

During the remaining workflow, start at `PTYPE.VALIDATE_INPUT`, satisfy every
prerequisite, evaluate applicability and apply only the reached source rule.
Record sanitized evidence and the observed outcome, including permitted
`deferred` transitions; stop at a terminal. Do not execute all nodes by sequence
number or treat an undeclared outcome as success. Live reads retain the declared
core client and their existing gates. Missing required inputs, baseline/package
evidence, known violations and failed auth/privilege checks remain blockers.
`PTYPE.RETURN_SUCCESS` means pre-upload checks only, with deferred fields still
unverified. This early check neither replaces final-artifact Task Hook validation
nor supplies Data Loader approval or submission authority.

In task-owned preparation evidence, retain the normalized request fingerprint,
current node, completed path/outcomes, sanitized resolver/default evidence,
deferred fields, missing requirements and safe resume stage. Use the existing
task artifact and redaction rules; do not extend the skill-run schema or copy
delegated loader records. When resuming preparation, compare request fingerprints
and refresh changed evidence; changed intended business inputs, target or upload
artifact require fresh validation and approval. A later submission of an approved
artifact follows Data Loader's persisted-artifact integrity checks: changes only
to the original source do not invalidate intact approved bytes or trigger live
revalidation. Reconcile uncertain submissions only through workflow step 8.


## Inputs

- `project_id`
- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `execution_receipt_record`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill for cross-task sequencing. Source references and evidence limitations are indexed in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md#source-evidence-index). Authored historical verification notes without retained receipts are context only.

## Refined Best-Practice Control Contract

Before producing a design recommendation, validation result, import preview, or completion claim, follow [Task Plan Validation and Execution](#task-plan-validation-and-execution) to traverse [ora-resource/ora_rule_registry.json](ora-resource/ora_rule_registry.json) and apply the refined controls from the standard `ora_input_validation.md`, `ora_defaulting_rules.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` resources selected by that graph.

- Treat every **Blocking control** as a stop gate. Do not preview or approve a configuration that violates it.
- Treat every **Required evidence** item as mandatory decision evidence. Return `needs_input` with the missing fields instead of silently defaulting.
- Treat every **Operational control** as a required readiness output. A one-time setup can be technically valid without the report, but the skill must not claim operational readiness until the report or reconciliation is defined.
- Treat **Readiness recommendations** as non-blocking for task-scoped setup. Record missing evidence as `readiness_not_assessed`; do not turn it into `needs_input`, invent evidence, or claim production readiness. An explicitly requested readiness assessment still reports the evidence gap.
- Preserve documented exceptions only where the control explicitly allows one; capture rationale, owner, approval reference, effective dates, and review date.
- Recalculate source-document population counts from the current target. Historical counts in the source are context, not validation constants.

## Durable Artifacts and Review

Resolve `project_id` from the selected existing implementation project before preparation or execution; missing project identity is an input-validation blocker. Persist plans, validation results, immutable previews, approved package references, execution receipts and redacted failure diagnostics under `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-types/current/`. Raw exports belong under `project/{project_id}/exports/project-financial-management/project-foundation/manage-project-types/`. Never persist credentials or tokens there.

Use `core.project-mgmt.artifact-version-manager` for major new versions and confirmed minor updates, `core.project-mgmt.artifact-registry-manager` to register each durable artifact, and `core.project-mgmt.project-state-manager` to update only declared state fields and record the run under `project/{project_id}/state/runs/`. These pillar-owned services persist the executor's returned receipt before any separately requested external follow-up; they do not extend the loader's initiation request. Append later observed statuses and retain partial failures, environment, operation, external IDs, approved artifact references/checksum and next action. Reconcile uncertain writes only in the explicitly requested recovery stage above; do not resubmit automatically. Record token usage using the manifest policy.

Required reviewers: responsible ERP Pillar Development Lead or SME, FSCR A-Team/core reviewer, and QA for validation/execution changes. Package readiness does not replace merge approval.

## Package Validation Evidence

Use the synthetic [offline rule-review cases](../../noship/tests/project-foundation/manage-project-types/manage-project-types-rule-review.json) and their [source-trace review](../../noship/tests/project-foundation/manage-project-types/manage-project-types-rule-review.md) for package review. They exercise preservation, protected changes, conditional financial options, deferrals, and approval integrity without touching Fusion. They are hypothetical authoring fixtures, never a current-target export, runtime reference catalog, approval, or proof of a successful import.

The [functional suite](../../noship/tests/project-foundation/manage-project-types/manage-project-types-test.yaml) retains separately declared live read/create coverage and offline review scenarios. Its structure and the rule registry must validate before handoff. Re-run source-trace review after a relevant resource change; a schema or compiler pass alone does not prove business-rule correctness. Human SME/core/QA review and a committed-HEAD merge audit remain external merge gates.
