---
skill_id: "erp.project-financial-management.project-organizations.configure-project-accounting-business-function"
name: "Configure Project Accounting Business Function Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Project Accounting Business Function under the Project Organizations functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
task_code: "PJF_CONFIGURE_PROJECT_ACCOUNTING_BUSINESS_FUNCTION"
task_name: "Configure Project Accounting Business Function"
parent_skill_id: "erp.project-financial-management.project-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.2.2"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/configure-project-accounting-business-function/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/configure-project-accounting-business-function/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/configure-project-accounting-business-function/current/"
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

# Configure Project Accounting Business Function Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Project Accounting Business Function` under `Project Organizations`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_CONFIGURE_PROJECT_ACCOUNTING_BUSINESS_FUNCTION`
- task_name: `Configure Project Accounting Business Function`
- parent_skill_id: `erp.project-financial-management.project-organizations`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Organizations`
- functional_area_code: `ORA_PJF_PROJ_ORG`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Project Accounting Business Function` under `Project Organizations`.

## Supported Task Behavior

Configure one existing active Project Accounting business unit: owning and expenditure organization hierarchies, project costing/calendar/conversion options, project-unit relationships, and cross-charge defaults or receiver overrides. Create a missing task implementation row only under the source-backed `createBUIfNeeded` condition; this task does not create the enterprise business unit or enable its business function.

Require a fresh business-unit baseline and proof that the existing active business unit has Project Accounting enabled. Resolve primary ledger/legal entity/currency and calendar/period compatibility only when creating the implementation row or changing a financial-dependent group such as calendar/period, costing/conversion, or cross-charge. Resolve hierarchy evidence only for hierarchy changes and removal evidence only for project-unit removals. For a project-unit relationship-only addition, validate the exact business unit, Project Accounting enablement, project unit, authorization, current relationships, and package delta; preserve unrelated financial settings without requiring separate financial-context evidence. Omitted groups preserve current values. Project-unit removals are blocked when used downstream. A project accounting calendar cannot change after its periods are copied.

Use the task-scoped FSM CSV `PJF_INSTALLATION` package for writes. No exact writable public REST contract is declared for the composite task. The rule registry governs package normalization before preview or import.

After each exact fndTrees resolution, validate the supplied version through
its resolved tree's FndTreeVersionVO child resource. Require one exact version
name, Status = ACTIVE, and EffectiveStartDate <= current configuration date
<= EffectiveEndDate before ZIP generation, preview or submission. Missing,
ambiguous, inactive, ineffective, incomplete or failed version results block.
The version nodes use scripts/validate_hierarchy_tree_versions.py on trusted
core receipts and may reuse one verified version response only for the same
resolved tree and exact version in the same target/configuration date. A
version name never supplies a technical tree code.

For supplied hierarchy start organizations, execute the two dedicated
projectOrganizationsLOV lookup nodes through core.fusion-api.rest-api-client
using the configured target restBaseUrl and validated target effective date.
Collect all pages, retain exact OrganizationName matches, and require one
active effective OrganizationId. Validate PROJECTS for ProjStartOrgName and
EXPENDITURES for ExpStartOrgName separately. Identical names may share one
complete response; two role rows for the same ID are not ambiguity. Use
scripts/validate_hierarchy_start_organizations.py to process trusted core
receipts; it performs no HTTP, authentication, ZIP generation or mutation.
Missing/ambiguous identities, missing roles, inactive/ineffective rows and
failed/incomplete reads block ZIP generation. These checks prove organization
identity and role, not membership in the selected hierarchy; retain the
documented membership warning, approval and post-import verification gates.

## Setup Task Metadata

- Task name: `Configure Project Accounting Business Function`
- Task code: `PJF_CONFIGURE_PROJECT_ACCOUNTING_BUSINESS_FUNCTION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export the current task row and project-unit relationships with `shared.setup-export.task-level-export`.
2. Execute `ora-resource/ora_rule_registry.json` in sequence.
3. Build the exact target-validated `PJF_INSTALLATION` package while preserving omitted groups.
4. Validate the business unit and Project Accounting enablement for every write, then validate only the references required by each explicitly changed group. A relationship-only addition does not require separate ledger, legal-entity, currency, or accounting-calendar evidence.
5. Produce an immutable preview showing target, business unit, every changed group, additions/removals, warnings, row counts, and checksum.
6. Route the immutable package to `core.data-loader`. A same-request `auto-approve`, `auto approve`, `approve without asking`, or `skip confirmation` instruction authorizes this one load after every validation gate passes; otherwise wait for later approval of the exact preview. Auto-approval never waives validation or authorizes a retry.
7. Before submission, designate a task-local execution-receipt record and preflight its safe writable destination. After accepted initiation, register the returned UCM Content ID, Data Loader Request ID, approved checksum, target, project, task and latest status through the declared core project services. Return In Progress without automatic status checks, process logs or exports. If receipt persistence fails, preserve any known ID in the response, stop and repair only local evidence; never resubmit under the old approval.
8. Only on a later explicit status/results/verification request, validate the registered target/project/task/request ID and approved-archive binding, then select core.data-loader's status/count/error workflow. Missing or mismatched context blocks before external calls. Never repeat preparation, approval or submission. Return a status-only request with that status; active status or a bounded timeout returns In Progress and waits for another request; terminal failure stops. If setup verification is requested, require terminal success before a fresh `PJF_INSTALLATION` same-task export and compare requested fields and preserved groups with the approved preview. Missing or mismatched readback prevents task completion without authorizing another write.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Organizations`
- Setup task name: `Configure Project Accounting Business Function`
- Setup task code: `PJF_CONFIGURE_PROJECT_ACCOUNTING_BUSINESS_FUNCTION`


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`

## Implementation Notes

Use the parent functional-area skill for sequencing. The Project Accounting business function must already be enabled. The supplied report proves observed members, not a blank template. Feature-gated simplified/legacy surfaces must follow current target state.

The task-rule graph evaluates preparation before the loader's own approval and submission. BUFUNC.RETURN_SUCCESS means validation/preparation completed; it does not certify a load or authorize automatic result queries. The later requested lifecycle in step 8 uses the saved receipt rather than rerunning the preparation graph.

## Refined Best-Practice Control Contract

Before producing a design recommendation, validation result, import preview, or completion claim, execute [ora-resource/ora_rule_registry.json](ora-resource/ora_rule_registry.json) and apply the refined controls from the standard `ora_input_validation.md`, `ora_defaulting_rules.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` resources selected by that graph.

- Treat every **Blocking control** as a stop gate. Do not preview or approve a configuration that violates it.
- Treat every **Required evidence** item as mandatory decision evidence. Return `needs_input` with the missing fields instead of silently defaulting.
- Treat every **Operational control** as a required readiness output. A one-time setup can be technically valid without the report, but the skill must not claim operational readiness until the report or reconciliation is defined.
- Preserve documented exceptions only where the control explicitly allows one; capture rationale, owner, approval reference, effective dates, and review date.
- Recalculate source-document population counts from the current target. Historical counts in the source are context, not validation constants.

## Durable Artifacts and Review

Resolve `project_id` from the selected existing implementation project before preparation or execution; missing project identity is an input-validation blocker. Persist plans, validation results, immutable previews, approved package references, execution receipts and redacted failure diagnostics under `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/configure-project-accounting-business-function/current/`. Raw exports belong under `project/{project_id}/exports/project-financial-management/project-organizations/configure-project-accounting-business-function/`. Never persist credentials or tokens there.

Use `core.project-mgmt.artifact-version-manager` for major new versions and confirmed minor updates, `core.project-mgmt.artifact-registry-manager` to register each durable artifact, and `core.project-mgmt.project-state-manager` to update only declared state fields and record the run under `project/{project_id}/state/runs/`. Persist each receipt before the next external call; append later statuses and retain partial failures, environment, operation, external IDs, artifact references and next action. Recover uncertain writes through supported reads; do not resubmit automatically. Record token usage using the manifest policy.

Required reviewers: responsible ERP Pillar Development Lead or SME, FSCR A-Team/core reviewer, and QA for validation/execution changes. Package readiness does not replace merge approval.
