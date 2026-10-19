---
skill_id: "erp.project-financial-management.project-organizations.manage-organization-hierarchies-and-classifications"
name: "Manage Organization Hierarchies and Classifications Setup Task Guidance"
description: "Provides customer-FSCR-only assisted setup guidance for Manage Organization Hierarchies and Classifications under Project Organizations."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
task_code: "PJF_MANAGE_ORGANIZATION_HIERARCHIES_AND_CLASSIFICATIONS"
task_name: "Manage Organization Hierarchies and Classifications"
parent_skill_id: "erp.project-financial-management.project-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.2.1"
inputs:
  - "project_id"
  - "target_environment"
  - "approved_organization_hierarchy_scope"
  - "current_target_state"
  - "setup_data_artifacts"
outputs:
  - "organization_hierarchy_readiness_review"
  - "template_gated_import_preview"
  - "target_state_verification"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-organization-hierarchies-and-classifications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-organization-hierarchies-and-classifications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-organization-hierarchies-and-classifications/current/"
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

# Manage Organization Hierarchies and Classifications Setup Task Guidance

## Purpose

Provide customer-FSCR-only assisted guidance to select the enterprise organization-hierarchy model, maintain the organization classifications used by Project Financial Management, and verify the resulting target state. A controlled FSM import is available only after the customer supplies or freshly exports the exact target-pod template and its import metadata.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_ORGANIZATION_HIERARCHIES_AND_CLASSIFICATIONS`
- task_name: `Manage Organization Hierarchies and Classifications`
- parent_skill_id: `erp.project-financial-management.project-organizations`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Organizations`
- functional_area_code: `ORA_PJF_PROJ_ORG`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, maintaining, importing, or validating setup data for `Manage Organization Hierarchies and Classifications` under `Project Organizations`.

## Customer Inputs

- Target environment and an accountable owner for the enterprise hierarchy decision.
- Approved current and desired hierarchy type, selected organization classifications, business impact, deployment window, and rollback expectation.
- For a non-None hierarchy, the approved target-visible tree, active tree version, and starting organization.
- Current target-task state or a fresh current-data export for update reconciliation.
- For FSM import, the customer-provided or freshly exported target-pod template, metadata, package contract, and process-log access.

## Supported Task Behavior

The task owns the Projects hierarchy type, selected organization classifications, and the default tree/version/starting-organization combination. Adding, moving, or removing organization-tree nodes is a manual `PER_MANAGE_ORGANIZATION_TREE` prerequisite boundary on this branch. Obtain a same-target handoff with tree structure, tree code, tree version, saved relationship/change evidence, and validation/activation state. Do not invoke an unavailable Workforce Structures skill or substitute an HDL import from this task.

Use a target-template-gated FSM import to set the hierarchy type only when the target does not already have one and to add validated classification values. Do not use the proven import contract to replace a different existing hierarchy type or remove classifications. Those operations remain unsupported for automated execution unless a fresh target contract directly proves them; do not redirect them to UI maintenance.

No direct customer REST write or internal application-module invocation is supported by this skill. Internal source behavior informs validation and sequencing only.

## Assisted Workflow

1. Confirm the exact target, owner, approved hierarchy outcome, selected classifications, impact, deployment window, and rollback expectation.
2. Reconcile the current target-visible hierarchy type, classifications, and applicable default-tree selection. Treat supplied current-data reports as guidance, not as a universal required value set.
3. Select the route by operation:
   - Use template-gated FSM import only when the exact target-pod template and metadata prove the required package contract and the proposed change is supported by that contract.
   - Return an operation-specific unsupported result for replacement or removal when the target contract does not prove it. Continue unrelated supported additive work.
   - Return the manual `PER_MANAGE_ORGANIZATION_TREE` prerequisite handoff for node placement and stop affected work until its saved same-target evidence is supplied. This handoff is outside this task's execution and does not approve the subsequent ESS sequence.
4. Validate that at least one approved classification remains selected. For a non-None hierarchy, resolve one valid tree, active version, and starting organization from the target task.
5. Preserve every current value outside the approved scope. Never use the source-observed first-visit None initialization as a customer design default.
6. Validate the customer's template and current export, preserve template metadata and translations, prepare only the supported delta, and run the shared setup-data and reference-data validations.
7. Create an immutable preview showing the target, route, current and desired hierarchy state, classifications added or preserved, default-tree selection when applicable, package members and row counts, warnings, and checksum.
8. Route the immutable package to `core.data-loader`. A same-request `auto-approve`, `auto approve`, `approve without asking`, or `skip confirmation` instruction authorizes this one load after every validation gate passes; otherwise wait for later approval of the exact preview. Auto-approval never waives validation or authorizes a retry.
9. Before submission, designate a safe writable task-local execution-receipt record. Immediately register the returned UCM Content ID, Data Loader Request ID, approved checksum, target/project/task and latest status through the declared core project services. Accepted initiation ends the submission request In Progress without status, process-log or export calls. If persistence fails, preserve any known ID and stop; repair local evidence without resubmitting or changing route.
   Only on a later explicit status/results/verification request, use OHCL.STATUS_REQUEST_GATE to validate the registered receipt and exact project/target/task/request/archive binding before the core status/count/error workflow. Never repeat preparation, approval or submission. A status-only request returns that status without setup reads. Active status or timeout returns Processing/In Progress and waits for another request; terminal failure stops. For requested setup verification after terminal success, compare a fresh same-task target export with the approved changes and preserved values. Missing or mismatched evidence blocks completion, not a reason to replay an import.
10. When the task reports that Maintain Project Organizations is required, hand off to its separately scoped setup task. Do not submit that process implicitly from this skill.

## Runtime Readiness

- The operator needs authorized target-task access and permission to review, maintain, and verify the hierarchy configuration.
- The accountable owner must approve the hierarchy model, selected classifications, non-None default-tree selection, impact, and rollback expectation.
- Before package generation or import, the customer must provide or freshly export the exact target-environment FSM template and current data. Exact mappings, package names, metadata, member headers, translations, identity behavior, and process-log interpretation are resolved from that target evidence.
- A conflicting existing hierarchy type or a requested classification removal is not supported by the proven additive import contract. Report only that operation as unsupported unless current target evidence proves a non-UI contract.
- No supported direct REST mutation contract is evidenced.

## Refined Best-Practice Control Contract

Before producing a design recommendation, validation result, import preview, or completion claim, execute [ora-resource/ora_rule_registry.json](ora-resource/ora_rule_registry.json) and apply the refined controls from the standard `ora_input_validation.md`, `ora_defaulting_rules.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` resources selected by that graph.

- Treat every **Blocking control** as a stop gate. Do not preview or approve a configuration that violates it.
- Treat every **Required evidence** item as mandatory decision evidence. Return `needs_input` with the missing fields instead of silently defaulting.
- Treat every **Operational control** as a required readiness output. A one-time setup can be technically valid without the report, but the skill must not claim operational readiness until the report or reconciliation is defined.
- Preserve documented exceptions only where the control explicitly allows one; capture rationale, owner, approval reference, effective dates, and review date.
- Recalculate source-document population counts from the current target. Historical counts in the source are context, not validation constants.

## Durable Artifacts and Review

Resolve `project_id` from the selected existing implementation project before preparation or execution; missing project identity is an input-validation blocker. Persist plans, validation results, immutable previews, approved package references, execution receipts and redacted failure diagnostics under `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/manage-organization-hierarchies-and-classifications/current/`. Raw exports belong under `project/{project_id}/exports/project-financial-management/project-organizations/manage-organization-hierarchies-and-classifications/`. Never persist credentials or tokens there.

Use `core.project-mgmt.artifact-version-manager` for major new versions and confirmed minor updates, `core.project-mgmt.artifact-registry-manager` to register each durable artifact, and `core.project-mgmt.project-state-manager` to update only declared state fields and record the run under `project/{project_id}/state/runs/`. Persist each receipt before the next external call; append later statuses and retain partial failures, environment, operation, external IDs, artifact references and next action. Recover uncertain writes through supported reads; do not resubmit automatically. Record token usage using the manifest policy.

Required reviewers: responsible ERP Pillar Development Lead or SME, FSCR A-Team/core reviewer, and QA for validation/execution changes. Package readiness does not replace merge approval.
