---
skill_id: "cx.sales.opportunities.manage-opportunity-revenue-categories"
name: "Manage Opportunity Revenue Categories Setup Task Guidance"
description: "Manages Opportunity revenue-category codes under standard lookup MOO_REVN_CATEGORY through guarded read-only discovery and validated export-derived FSM packages handed to Core Data Loader; direct REST mutation is unsupported."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_REVENUE_CATEGORIES"
task_name: "Manage Opportunity Revenue Categories"
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
version: "0.3.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "fusion_environment_context"
  - "request_mode"
  - "lookup_operation"
  - "lookup_code"
  - "lookup_attributes"
  - "expected_current_state"
  - "reference_export_optional"
  - "task_context_path"
  - "task_sequence"
  - "package_path_optional"
  - "package_sha256_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "current_revenue_category_state"
  - "immutable_change_preview"
  - "fsm_package_validation"
  - "data_loader_task_validation_result_optional"
  - "data_loader_approval_preview_optional"
  - "task_validation_envelope_optional"
  - "data_load_initiation_result_optional"
  - "accepted_initiation_result_optional"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-opportunity-revenue-categories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-opportunity-revenue-categories/current/"
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
  - "Reads standard lookup MOO_REVN_CATEGORY through core.fusion-api.apps-common."
  - "May hand an exact immutable MOO_MANAGE_REVENUE_CATEGORIES FSM package to core.data-loader, which owns Task Hook validation, its approval preview, the later standalone approval, upload, and accepted initiation result."
  - "On a later explicit status or results request, may read Data Loader process evidence and verify MOO_REVN_CATEGORY through Apps Common."
  - "Persists preview, execution, verification, diagnostic, and token-usage artifacts in the implementation project workspace."
required_privileges:
  - "Fusion privileges to view or manage standard lookup MOO_REVN_CATEGORY."
  - "Privileges to export or import MOO_MANAGE_REVENUE_CATEGORIES when the approved FSM route is selected."
---

# Manage Opportunity Revenue Categories Setup Task Guidance

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

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Opportunity Revenue Categories` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_REVENUE_CATEGORIES`
- task_name: `Manage Opportunity Revenue Categories`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Opportunity Revenue Categories` under `Opportunities`.

## Supported Operations and Routes

| Operation | Route | Required behavior |
|---|---|---|
| Read | Core Apps Common Standard Lookups REST | Resolve exactly one code under MOO_REVN_CATEGORY and return sanitized current state without mutation approval. |
| Create | Task-level export and Core Data Loader FSM only | Require an absent exact code, a fresh exact-target/release completed export, exactly one reviewed package row, and complete package readiness before handoff. |
| Update | Task-level export and Core Data Loader FSM only | Require one existing exact code, a reviewed mutable delta, fresh state lock, impact evidence, and complete immutable package readiness before handoff. |
| Disable | Default: task-level export and Core Data Loader FSM | Set EnabledFlag to N in the package only; do not translate disablement to DELETE. |
| Export | Shared task-level export | Export and validate the complete MOO_MANAGE_REVENUE_CATEGORIES task for the exact target and release; do not require a LookupCode. |
| Import | Core Data Loader FSM only | Validate every changed MOO_REVN_CATEGORY row, preserve every unrelated member and row, and hand the unchanged final ZIP to Data Loader. |

Delete is unsupported by this task contract. Do not create or rename the parent
lookup type, substitute `MOO_SETID_REVN_CATEGORY`, or add reference-set context.
Read-only discovery delegates transport and authentication to
`core.fusion-api.apps-common`. Direct REST mutation is unsupported even though
the core adapter documents generic standard-lookup writes. Refuse POST, PATCH,
PUT, and DELETE for this task and use the exact FSM package route for Create,
Update, Disable, or Import.

## Setup Task Metadata

- Task name: `Manage Opportunity Revenue Categories`
- Task code: `MOO_MANAGE_REVENUE_CATEGORIES`
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
- Setup task name: `Manage Opportunity Revenue Categories`
- Setup task code: `MOO_MANAGE_REVENUE_CATEGORIES`

## Default FSM Package Workflow

1. Load `core/fusion-api/apps-common/SKILL.md` and its standard-lookups
   reference contract for read-only parent and code discovery.
2. Select `SingleLookup` for Read or one-code Create, Update, or Disable, and
   `Package` for full-task Export or Import.
3. Resolve the exact `MOO_REVN_CATEGORY` parent. Resolve one exact code for
   SingleLookup; for Package Import, validate every changed row independently.
4. Obtain a fresh completed export for the exact target, release, and
   `MOO_MANAGE_REVENUE_CATEGORIES` task. Preserve it as the baseline and build
   a separate final ZIP for a mutation or Import.
5. Before design gating, validate exact task identity/name/code, one ASM
   identity, metadata-derived members and headers,
   reviewed row deltas, fresh current-state locks, impact, unrelated-content
   preservation, and the SHA-256 of the reopened final ZIP.
6. For a mutation or Import handoff, resolve persisted `TaskContextPath`, exact
   `TaskName`, and positive `TaskSequence` to this exact skill path, `TaskCode`,
   offering, and functional area. Hand that context with the exact environment,
   immutable package path, SHA-256, member summary, proposed rows, current
   state, impact evidence, and verification read to `core.data-loader`.
7. Let Data Loader validate the unchanged package, invoke Task Hook, and build
   its immutable approval preview. Stop until the user later replies exactly
   `approve`; no other approval text authorizes the FSM upload.
8. After that approval, let Data Loader revalidate and submit once. Accepted
   initiation is terminal for that request; do not monitor, retrieve ProcessLog,
   or re-read the lookup automatically.
9. On a later explicit status or results request, use Data Loader status
   handling and then re-read the exact item to compare it with the approved
   result. On a failed or uncertain result, preserve sanitized diagnostics and
   reconcile before proposing another package.

For the FSM route, Data Loader owns the approval preview and later standalone
`approve`. This child hands off package evidence without requiring, creating,
or interpreting Data Loader-owned approval evidence.

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
3. [ora_defaulting_rules.md](ora-resource/ora_defaulting_rules.md)
4. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
5. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
6. [ora_error_handling.md](ora-resource/ora_error_handling.md)
7. [ora_rule_registry.json](ora-resource/ora_rule_registry.json) for the compiled task-node graph

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `fusion_environment_context`
- `request_mode`
- `lookup_operation`
- `lookup_code`
- `lookup_attributes`
- `expected_current_state`
- `reference_export_optional`
- `task_context_path`
- `task_sequence`
- `package_path_optional`
- `package_sha256_optional`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `current_revenue_category_state`
- `immutable_change_preview`
- `fsm_package_validation`
- `data_loader_task_validation_result_optional`
- `data_loader_approval_preview_optional`
- `task_validation_envelope_optional`
- `data_load_initiation_result_optional`
- `accepted_initiation_result_optional`
- `lookup_execution_result`
- `post_change_verification`
- `diagnostics`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
