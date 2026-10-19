---
skill_id: "scm.product-management.change-orders.manage-change-order-and-new-item-request-line-descriptive-flexfields"
name: "Manage Change Order and New Item Request Line Descriptive Flexfields Setup Task Guidance"
description: "Guides Change Line DFF setup and disabling existing Contexts, Global Segments or Context Sensitive Segments for EGO_CHANGE_LINE through Apps Common; excludes deletion, header DFFs and unsupported new item request line DFFs."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Change Orders"
functional_area_code: "EGO_CHANGE_ORDERS"
task_code: "EGO_MANAGE_CHANGE_ORDER_LINES_DFFS"
task_name: "Manage Change Order and New Item Request Line Descriptive Flexfields"
parent_skill_id: "scm.product-management.change-orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.1.13"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-order-and-new-item-request-line-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-order-and-new-item-request-line-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Conversational, runbook and optional spreadsheet input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Change type Context Code lookup contract"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Required verified setup dependencies"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Context Segment display and derivation defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Change Line DFF design constraints"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Task-specific diagnostics and rule-result handoff"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Scoped conversational/runbook/spreadsheet inputs, Oracle naming checks, Context Code lookup, Context Segment display default and shared baseline/import/deployment routes defined. Shared preflight, approval and live verification remain required."
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Manage Change Order and New Item Request Line Descriptive Flexfields Setup Task Guidance

## Purpose and Scope

Manage Change Line DFF `EGO_CHANGE_LINE` through Apps Common for change orders, change requests, problem reports and corrective actions. Support creating and updating Global Segments, Contexts and Context Sensitive Segments, configuring the Context Segment selector, and disabling existing segments or ordinary Contexts.

Retain the catalog task name and code `EGO_MANAGE_CHANGE_ORDER_LINES_DFFS`. Despite that name, new item request line DFFs are unsupported. Header DFFs, transaction edits, deletion, whole-DFF disable and selector disable are outside this task.

## Inputs and Intake

Accept ordinary prompts, runbook tasks and optional spreadsheets through the declared inputs. Questions and corrections can arrive in any order; request only facts needed for the next operation. Input-only feedback does not require execution bindings or establish target-state validation. Use the stage-specific contract in [input validation](ora-resource/ora_input_validation.md).

Use these distinct objects when resolving ambiguous terminology:

| Object | Meaning |
|---|---|
| Global Segment | Attribute independent of the selected Context |
| Context Segment | Controlling selector with its own value set, defaults and display settings |
| Context | Definition identified by Context Code, containing Context Sensitive Segments |
| Context Sensitive Segment | Attribute within a particular Context |

Keep Name, Code, API Name, Prompt, Context Code and change type InternalName distinct. Clarify ambiguous wording rather than fuzzy-matching identifiers. Confirmed corrections replace only the affected intended values and invalidate affected evidence or approvals; preserve unrelated confirmed details.

## Task Rules

Use the resources declared in `oracle_supplied_guidance_files` as the task's runtime contract. Read each before formal task-rule validation and apply only its applicable rules; load error handling before preview or live execution:

| Resource | Responsibility |
|---|---|
| [Input validation](ora-resource/ora_input_validation.md) | Required inputs, naming, value shape and source consistency |
| [Reference lookups](ora-resource/ora_reference_lookups.md) | Read-only lookup retrieval and result mapping |
| [Dependency readiness](ora-resource/ora_dependency_readiness.md) | Applicable reference prerequisites |
| [Defaulting](ora-resource/ora_defaulting_rules.md) | Eligible selector defaults and override behavior |
| [Design enforcement](ora-resource/ora_design_enforcement.md) | Context membership, selector policy, candidate preservation and disable constraints |
| [Error handling](ora-resource/ora_error_handling.md) | Task-specific diagnostics and result interpretation |

For a task-routed load, Data Loader's single [Task Hook](../../../../../core/data-loader/task-hook/SKILL.md) owns resolution and evaluation of the [task registry](ora-resource/ora_rule_registry.json), using its returned execution guide and applicable resources on the final immutable artifact. Follow its preview, approval and archive-verification lifecycle; do not invoke Task Validator directly or add a second evaluator or import approval. A ready plan is not evaluated rules or permission to mutate. An empty shared artifact-helper guidance list does not establish that these declared resources are absent.

## Shared Execution Route

Delegate to [Apps Common Descriptive Flexfields](../../../../../core/fusion-api/apps-common/descriptive-flexfields/SKILL.md) and its [export, FSM import, and REST Deployment and Status workflow](../../../../../core/fusion-api/apps-common/descriptive-flexfields/references/descriptive-flexfields.md).

- Supply the exact task code/name, Product Management offering, Change Orders functional area, positive task sequence and confirmed environment. Keep flexfield code EGO_CHANGE_LINE distinct from the task code.
- Use `shared.setup-export.task-level-export` in current-data mode for a baseline. Template/spec mode is only for an explicit template request. A successful job without the affected setup rows is not a usable baseline.
- Delegate generic artifact and reference comparisons to `shared.validation.setup-data-validator` and `shared.validation.reference-data-validator`. Shared artifact validation excludes Ora Resource rules; retain the candidate evidence for Task Hook's task-rule evaluation.
- Import the validated immutable FSM ZIP through `core.data-loader`. Preserve its verified Run Book binding and artifact envelope; do not rebuild the archive or reuse an incompatible envelope after approval.
- After verified import success, perform requested deployment through core's REST Deployment and Status route, including its separate deployment approval. Core owns preflight, transport, polling, retries and diagnostics; do not substitute a manual click, task-local browser or direct import route.

### Baseline and Target Identity

Create, update and disable require a successful current-data export for the exact task and confirmed environment. Resolve EGO_CHANGE_LINE and the affected definitions from it. The task export requires neither an application ID nor a deployment-job record as input. Establish the target application ID from authoritative metadata before an operation that needs it; do not reuse another pod's identity or infer it from a table owner.

Do not add a deployment-job lookup as a pre-export gate. A missing job is not evidence that saved metadata is undeployed, and an earlier DEPLOYED result does not prove a populated baseline. Follow the task-specific interpretations in [error handling](ora-resource/ora_error_handling.md). Independently established migration or metadata problems remain subject to the shared workflow; never deploy pending changes automatically to obtain a baseline.

## Disable and Verification

Disable changes only the selected existing object's EnabledFlag from Y to N under the design resource's identity, editability, impact and preservation rules. Resolve segment flags on attribute rows and Context flags on Context rows using the current FSM export; neither deletion by row omission nor disabling all children substitutes for Context disable. Historical member names are not a contract: verify current members, scope keys and any multiple representations before packaging.

Present the exact delta, impact findings, recovery plan and preservation evidence in the normal Data Loader preview. A recovery plan does not authorize restoration, re-enabling or automatic rollback. An already-disabled target is a verified no-op, not a reason to repeat import/deployment.

After execution, read back the selected definitions through the supported current-data workflow. Verify the intended settings and preservation of unrelated setup. Disabled rows must remain present with EnabledFlag N and unchanged other properties; a disabled Context must retain its child definitions and flags. Report import, deployment, setup read-back and any authorized runtime checks separately. Job completion alone proves neither preservation nor UI/integration behavior or historical-data accessibility. Reconcile partial or uncertain outcomes through the selected core workflow before a separately approved next action.

## Outputs and Persistence

Return the declared setup task plan, routing, validation checkpoints and run evidence. Use the parent `scm.product-management.change-orders` for functional-area scope and sequencing. Persist project artifacts and token-usage records through the services and locations declared in the manifest.
