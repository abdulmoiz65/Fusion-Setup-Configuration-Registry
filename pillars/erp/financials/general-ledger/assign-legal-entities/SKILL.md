---
skill_id: "erp.financials.general-ledger.assign-legal-entities"
name: "Assign Legal Entities Setup Task Guidance"
description: "Provides task-specific setup guidance for Assign Legal Entities under the General Ledger functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "General Ledger"
functional_area_code: "ORA_FIN_GENERAL_LEDGER"
task_code: "GL_ASSIGN_LEGAL_ENTITIES"
task_name: "Assign Legal Entities"
parent_skill_id: "erp.financials.general-ledger"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.0"
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
  - "core.fusion-api.rest-api-client"
  - "shared.setup-export.fsm-csv-export"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/assign-legal-entities/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/assign-legal-entities/current/"
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
  - "Performs declared read-only ledger and legal-entity lookups through core.fusion-api.rest-api-client."
  - "Creates one approved primary-ledger-scoped GL_ASSIGN_LEGAL_ENTITIES export process through core.fusion-api.rest-api-client."
  - "Polls the returned ProcessId and downloads the export package through shared.setup-export.fsm-csv-export."
  - "Writes setup plans, proposed import artifacts, validation evidence, run records, and token usage to the project workspace."
required_privileges:
  - "Read ledger reference data through ledgersLOV in the selected Fusion environment."
  - "Read legal-entity reference data through legalEntitiesLOV in the selected Fusion environment."
  - "Create and retrieve GL_ASSIGN_LEGAL_ENTITIES FSM CSV export processes, packages, and process logs."
---

# Assign Legal Entities Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Assign Legal Entities` under `General Ledger`.

## Setup Task Skill Contract

- task_code: `GL_ASSIGN_LEGAL_ENTITIES`
- task_name: `Assign Legal Entities`
- parent_skill_id: `erp.financials.general-ledger`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `General Ledger`
- functional_area_code: `ORA_FIN_GENERAL_LEDGER`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Assign Legal Entities` under `General Ledger`.

In assisted mode, route reference reads, the approved scoped export, and package download through the declared core/shared services, then prepare the proposed import artifact for review. Import execution and its approval workflow remain delegated to `core.data-loader`.

## Read Order

1. Read the Task-Local Plan Validation and Node Execution sections below. They define this task's runtime contract.
2. Read [the task registry](ora-resource/ora_rule_registry.json) and select exactly one entry for `GL_ASSIGN_LEGAL_ENTITIES` / `Assign Legal Entities`.
3. Read each reachable node's source heading and owning rule tables in this skill's `ora-resource/` folder, including every named resolver definition in [reference lookups](ora-resource/ora_reference_lookups.md). Complete Task-Local Plan Validation before starting any node.
4. Read [error handling](ora-resource/ora_error_handling.md) before preview or external execution, and read the owning source rules again before performing each reached node.
5. Load `core.fusion-api.rest-api-client` when a node reaches a declared live resolver or the scoped-export create step.
6. Load `shared.setup-export.fsm-csv-export` only after that create step returns a ProcessId.

## Task-Local Plan Validation

Build `setup_task_plan` directly from the shipped registry and its local source tables. This is an LLM validation step; it requires no authoring tool or planner script. Before any external request, require all of the following:

| Check | Required result |
|---|---|
| Task identity and readiness | Registry schema is `3.0`, representation is `nested`, and the selected task matches this manifest's code and name. Task and reachable-node readiness are `ready`, with empty `blocking_reasons`. |
| Graph integrity | Node IDs are unique; `start_node` is `ALE.VALIDATE_INPUT`; every prerequisite and transition target exists in this task; the graph is acyclic; every reachable nonterminal has declared outcomes and every path ends at a terminal with no outgoing transitions. |
| Source integrity | Every `source.file` resolves inside this skill's `ora-resource/` folder and its heading exists. Match each node by Rule ID to exactly one source `Task Nodes` row; node type, sequence, action type, transitions, prerequisites, failure behavior, and applicability must agree. Treat source line numbers as navigation hints, not proof of agreement. |
| Rule and resolver completeness | Read the owning validation, dependency, lookup, defaulting, design, and error rules for every reachable node. Each named resolver has exactly one local or live definition with its source, match rule, outputs, and failure behavior. Missing definitions, unresolved `TBD` values, or contradictions block the plan. |
| Supported actions and routes | This task uses `validate_input`, `reference_lookup`, `resolve_dependency`, `apply_default`, `design_enforcement`, `execution_gate`, and `terminal`. Live resolvers use the declared REST client; local rules stay local. `ALE.ACQUIRE_SCOPED_EXPORT` coordinates only the scoped-export operation explicitly defined in [dependency readiness](ora-resource/ora_dependency_readiness.md). A node's action or route label alone does not authorize an external operation. |
| Request boundary | The normalized request is direct legal-entity assignment to a primary ledger. Removal, reassignment, ledger-child authoring, and balancing-segment assignment are unsupported. Validate supplied inputs at `ALE.VALIDATE_INPUT` before any lookup. |

Only after these checks pass, record a machine-readable `setup_task_plan` with `status: planned`, `validation.status: ready`, exact task identity, start node, the validated graph, and checked source references. A ready plan permits entry into the graph; each node still requires current evidence and its operation-specific gates.

For a missing, stale, inconsistent, or incomplete graph or source, stop with `FAILED` before external execution. Record the failed check, Rule ID/source when available, failure class, and corrective action in the project's diagnostics. Use `input validation` for malformed or incomplete contracts and `catalog mismatch` for task identity disagreement. Request correction of the ALE resources and registry; do not repair the graph during execution or substitute an undeclared route.

## Node Execution

1. Start at `ALE.VALIDATE_INPUT`. Follow declared transition outcomes; sequence numbers do not authorize skipping a node. Every listed prerequisite must have succeeded in the current run before a node can execute.
2. Apply only the reached node's owning source rules and named resolvers. Record the observed outcome and sanitized evidence, then follow its exact transition target. An unlisted outcome stops with `FAILED`; never invent a transition, lookup, default, retry, or cross-task action.
3. Complete the active workflow's environment, identity, privilege, catalog, payload, artifact, and approval checks before each external operation. Obtain approval for the exact target environment, operation, and scoped-export payload immediately before the create request. Submit at most once in the run and pass its returned ProcessId to the declared polling/download skill.
4. At `ALE.PREVIEW_GATE`, use the immutable artifact and approval workflow owned by `core.data-loader`; carry that approval into the declared handoff without requesting the same approval twice. The ALE graph does not execute the import. `ALE.READY_FOR_IMPORT` means ready for that handoff, not that an assignment was imported or verified. `RETURN_ISSUES` means stop and disclose the blocker.
5. Maintain a task-local run record with the normalized request fingerprint, current node, completed path and outcomes, sanitized evidence references, missing requirements, preview/approval fingerprints, verified side effects, and safe resume stage. Persist it and token usage under the manifest's project locations; exclude credentials, tokens, sensitive payloads, and protected response data.
6. On resume, compare the request fingerprint and refresh changed or time-sensitive evidence. A material input, environment, package, or delta change invalidates preview and approval. Reconcile any uncertain mutation through the declared safe verification route before considering a retry; never replay it automatically.

The handoff must report task code and name, status, current or terminal Rule ID and action type, completed path and outcomes, sanitized validated facts, blockers, verified side effects, and one safe next action with resume context. Use `MISSING` for an unresolved required fact or approval, `UNSUPPORTED` for an out-of-scope request, and `FAILED` for contract or execution failures. Do not claim assignment success from a ready plan, a successful lookup, an export receipt, or the import-readiness terminal.

## Setup Task Metadata

- Task name: `Assign Legal Entities`
- Task code: `GL_ASSIGN_LEGAL_ENTITIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y`, but this task requires a primary-ledger-scoped export. The task-local compiled `ora-resource` plan selects scoped REST creation followed by ProcessId-based polling and download.

1. Execute the task-local plan only after Task-Local Plan Validation succeeds against `ora-resource/ora_rule_registry.json` and its current source rules; do not use prior run outcomes as current evidence.
2. At `ALE.ACQUIRE_SCOPED_EXPORT`, use the route and exact scope values declared in `ora-resource/ora_dependency_readiness.md`. Use this declared scoped REST-create route; do not substitute `shared.setup-export.task-level-export`.
3. Use `core.fusion-api.rest-api-client` for the read-only GETs defined by `resolve_primary_ledger` and `resolve_legal_entity_exact_identifier`, plus exactly one separately approved scoped export-process POST after the primary-ledger gate passes. Do not submit additional POSTs. Follow the exact root-sibling JSON structure in `ora-resource/ora_dependency_readiness.md`; never nest the criteria array inside the process row. Then pass only the returned ProcessId to `shared.setup-export.fsm-csv-export` for polling and download.
4. Validate the returned package and requested mapping through the remaining reached task nodes, `shared.validation.setup-data-validator`, and `shared.validation.reference-data-validator`.
5. Route any eventual import through `core.data-loader`; preserve its immutable-preview and explicit-approval gates.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `General Ledger`
- Setup task name: `Assign Legal Entities`
- Setup task code: `GL_ASSIGN_LEGAL_ENTITIES`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `erp.financials.general-ledger` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
