---
skill_id: "cx.sales.opportunities.manage-levels-of-risk"
name: "Manage Levels of Risk Setup Task Guidance"
description: "Provides the exact MOO_MANAGE_LEVELS_OF_RISK adapter for Level of Risk set-enabled lookup maintenance while reusing the common Opportunities lookup workflow."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Opportunities"
functional_area_code: "ORA_MOO_OPPORTUNITIES"
task_code: "MOO_MANAGE_LEVELS_OF_RISK"
task_name: "Manage Levels of Risk"
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
version: "0.2.9"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "request_mode"
  - "lookup_operation"
  - "lookup_code"
  - "lookup_attributes"
  - "set_selection_decision"
  - "reference_data_set_identity"
  - "fusion_environment_context"
  - "expected_current_state"
  - "execution_route_optional"
  - "rest_delete_approval_optional"
  - "reference_export_optional"
  - "task_context_path"
  - "task_sequence"
  - "package_path_optional"
  - "package_sha256_optional"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "resolved_lookup_contract"
  - "resolved_lookup_parent"
  - "resolved_reference_group"
  - "catalog_task_code"
  - "record_set_prerequisite_task_code"
  - "execution_task_code"
  - "current_lookup_state"
  - "immutable_change_preview"
  - "fsm_package_validation"
  - "data_loader_task_validation_result_optional"
  - "data_loader_approval_preview_optional"
  - "task_validation_envelope_optional"
  - "data_load_initiation_result_optional"
  - "lookup_execution_result"
  - "post_change_verification"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.sales.opportunities.manage-set-enabled-lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-levels-of-risk/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/opportunities/manage-levels-of-risk/current/"
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
  - "Reads the fixed MOO_SETID_RISK_LEVEL lookup type and its reference-set assignment through core.fusion-api.apps-common."
  - "May hand an immutable MOO_MANAGE_LEVELS_OF_RISK package to core.data-loader, which owns Task Hook validation, its approval preview, the later standalone approval, upload, and accepted initiation result."
  - "On a later explicit status or results request, may read process evidence and verify MOO_SETID_RISK_LEVEL through Apps Common."
  - "May use only the documented direct REST Delete exception when explicitly selected and separately approved under the common workflow contract."
required_privileges:
  - "Fusion privileges appropriate to view or manage Level of Risk lookup codes and the selected reference data set."
  - "Privileges to export or import MOO_MANAGE_LEVELS_OF_RISK when the FSM route is selected."
---

# Manage Levels of Risk Setup Task Guidance

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

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Levels of Risk` under `Opportunities`.

## Setup Task Skill Contract

- task_code: `MOO_MANAGE_LEVELS_OF_RISK`
- task_name: `Manage Levels of Risk`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Levels of Risk` under `Opportunities`.

## Setup Task Metadata

- Task name: `Manage Levels of Risk`
- Task code: `MOO_MANAGE_LEVELS_OF_RISK`
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
- Setup task name: `Manage Levels of Risk`
- Setup task code: `MOO_MANAGE_LEVELS_OF_RISK`




## Set ID Selection

Never default this task to Common Set. For `SingleLookup` without an exact set
selector, ask whether Common Set should be used or a different exact Set ID or
Set Code should be selected. Resolve confirmed Common Set through the
documented read-only set resolver rather than hard-coding its ID. For package
mutations, preserve each exported row's set and require an explicit choice for
every new row without one. Set confirmation is not mutation approval.

## Negative Set Scenarios

Reject a malformed or unknown Set ID/Set Code, selectors that resolve to
different sets, a confirmed Common Set choice that resolves to a non-Common
set, a business-unit assignment whose ReferenceGroupName or set differs from
the exact parent, or a package row whose set differs from its confirmed or
fresh-export identity. Do not substitute Common Set, a close match, a generic
lookup type, or another environment's set. Return the exact mismatch and
require one valid set decision before continuing.

## Fixed Set-Enabled Lookup Adapter

| Contract item | Fixed value |
|---|---|
| Business value | Level of Risk |
| Lookup type | MOO_SETID_RISK_LEVEL |
| Catalog and FSM task code | MOO_MANAGE_LEVELS_OF_RISK |
| Record-set prerequisite task | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| Default mutation route | FSM through core.data-loader |

The lookup type and FSM task code are immutable for this adapter. Reject a
request that supplies a different lookup type or package task code. If the
record-set assignment is missing or incorrect, return ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES as the
prerequisite gap; do not change that assignment here.

## Common Workflow Contract

Load [Manage Set Enabled Lookups](../manage-set-enabled-lookups/SKILL.md) for
the shared Apps Common discovery, validation, preview, approval, mutation,
diagnostics, retry, and verification discipline. Reuse its behavior only; do
not inherit its FND task identity or its two generic lookup types.

This adapter owns the exact task boundary:

1. Load the task-local resources and compiled registry listed below.
2. Resolve the exact MOO_SETID_RISK_LEVEL parent first and capture its returned nonblank ReferenceGroupName. For SingleLookup, use it to resolve one exact set and any requested business-unit assignment before reading code state. For Package work, validate set and state per changed row; full-task Export has no set selector or code.
3. For SingleLookup Create, Update, or Disable, require exactly one matching reviewed row in a fresh, validated, immutable MOO_MANAGE_LEVELS_OF_RISK package. For Package Create, Update, Disable, or Import, validate every changed row atomically. Both routes require exact task identity, package hash binding, state locks, and business-impact evidence before Data Loader handoff. Require persisted Data Loader task context before every Data Loader handoff: persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area. Never hand-author or synthesize task context.
4. Let core.data-loader own Task Hook validation, its immutable preview, the later standalone approve, upload, and accepted initiation result. Accepted initiation ends the request; status, ProcessLog, and read-back verification require a later explicit request.
5. Permit only Delete as an explicitly selected direct REST exception with editability and impact evidence, a separate immutable preview, immediate approval, one submission, and exact read-back verification.
6. Never substitute FND_MANAGE_SET_ENABLED_LOOKUPS or another named Opportunity task code.

## Supported Operations

Inventory and Read are read-only. Create, Update, and Disable use the exact FSM
task code by default. Export and Import route through the generated catalog
workflow. Delete fails closed on FSM and is available only through the common
workflow's documented direct REST exception.

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
3. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
4. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
5. [ora_error_handling.md](ora-resource/ora_error_handling.md)
6. [ora_rule_registry.json](ora-resource/ora_rule_registry.json)

Use the rule planner before consuming the registry. The local graph owns this
adapter's exact task identity; the common workflow is not a substitute for the
local registry or approval gate.

## Runtime Interface

Use the manifest `inputs` and `outputs` as the canonical interface. In
addition to the standard project and setup-data fields, preserve this
adapter's RequestMode, fixed lookup type, exact catalog/FSM task code, returned
reference group, SingleLookup set or per-row package sets, package validation
result, Data Loader handoff evidence, and route-specific approval state. Do
not maintain a second reduced interface
or reinterpret a generic approval as Data Loader upload authorization.

## Implementation Notes

Use the parent functional-area skill `cx.sales.opportunities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
