---
skill_id: "erp.project-financial-management.project-foundation.manage-project-roles"
name: "Manage Project Roles Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Project Roles under the Project Foundation functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_PROJECT_ROLES"
task_name: "Manage Project Roles"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.1.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "qualification_requirements"
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
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-roles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-roles/current/"
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
  - "Writes declared task planning/validation artifacts, artifact registrations, state updates, skill-run records and token-usage records through the declared core project services."
  - "Delegates task-scoped exports and approved imports to the declared shared/core workflows under their existing gates."
required_privileges: []
---

# Manage Project Roles Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Project Roles` under `Project Foundation`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_PROJECT_ROLES`
- task_name: `Manage Project Roles`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Project Roles` under `Project Foundation`.

## Supported Task Behavior

Create, update, or end-date a custom project role with an optional current job or abstract enterprise-role association, descriptions, effective dates, translations, and—when Project Management is implemented—qualifications and keywords. Accept a qualification by its Requirements display name (for example, Hindi), plus the user's Mandatory Requirement and optional proficiency levels. Resolve its type, content-item identity, and section when applicable through the declared lookups. Protect seeded Project Manager and Project Team Member roles. Omitted enterprise-role and child collections preserve current values; removal must be explicit and pass current-use/access checks.

Use task-scoped FSM CSV; no exact writable public setup REST contract is declared.

## Setup Task Metadata

- Task name: `Manage Project Roles`
- Task code: `PJF_MANAGE_PROJECT_ROLES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Call `shared.setup-export.task-level-export` once in data-export mode for each validation package/run of `PJF_MANAGE_PROJECT_ROLES`; do not export per CSV row or use a blank template as a baseline. Extract the current PJF_PROJECT_ROLE.csv, PJF_PROJECT_ROLE_TRANSLATION.csv, and PJT_PROJECT_MANAGEMENT_PROJECT_ROLE_QUALIFICATION.csv members.
2. Perform [Task Plan Validation and Execution](#task-plan-validation-and-execution) using this skill, the shipped registry and its reachable source rules. Record a `planned` / `ready` plan without an override before evaluating the graph or preparing the package.
3. Use exported PJF_PROJECT_ROLE.csv as the local `find_project_role` baseline. Join qualification rows by ProjectRoleName. Treat a supplied Requirements name as a predefined item search, never as an implicit keyword. Resolve a unique active content item and, when section-aware selection applies, reuse an exact same-target qualification section from any role in the fresh task export. Ask for a choice only when multiple eligible items or sections remain. A new section with no proven target evidence remains blocked. Reconcile existing children by resolved parent, ContentItemId and Keyword. No public read REST contract is declared for project-role qualification membership.
4. Build only explicit base/child diffs using target-validated members.
5. Validate role identity, seeded state, enterprise role, Project Management implementation, qualifications, translations, dates, and active use.
6. Produce an immutable preview and checksum.
7. Delegate the final immutable archive to `core.data-loader`, including its read-only Task Hook validation before its own approval gate. The loader owns approval and submission; do not add a second approval. Accepted initiation is terminal for that request and means in progress, not verified setup completion. Do not automatically poll, retrieve logs, export again, or persist loader result/failure artifacts.
8. Only when the user explicitly requests status/results/verification, follow the loader's status workflow. For requested setup reconciliation, obtain a fresh same-task export through the shared exporter and compare the approved diff. On uncertain or partial results, reconcile before considering a separately authorized resubmission; never replay automatically.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Foundation`
- Setup task name: `Manage Project Roles`
- Setup task code: `PJF_MANAGE_PROJECT_ROLES`

## Task Plan Validation and Execution

At workflow step 2, build `setup_task_plan` locally from
[the shipped registry](ora-resource/ora_rule_registry.json) and its six owning
`ora-resource/ora_*.md` files. This assisted check requires no authoring tool,
planner script or external call; it does not repeat step 1's export.

- Select exactly one `PJF_MANAGE_PROJECT_ROLES` / `Manage Project Roles` entry
  in the nested schema `3.0` registry. Require task and reachable-node readiness
  `ready` with no blocking reasons; a stored readiness flag alone is insufficient.
- Confirm unique node IDs, start node `PROLE.VALIDATE_INPUT`, existing prerequisite
  and transition targets, and paths ending at the declared terminal nodes.
  Resolve each source file inside this task's resource folder and its heading;
  match each node to one source Task Nodes row by Rule ID. Check node type,
  sequence, action type, transitions, prerequisites, failure behavior and
  applicability against that row. Source line numbers are navigation hints.
- Read each reachable node's owning rules and named resolver definitions,
  requiring exactly one definition per resolver, with declared inputs, sources,
  match rules, outputs and failure behavior.
  Missing, ambiguous, inconsistent or unresolved required contracts block the
  plan; do not repair the registry or invent a resolver during execution.

Only after these checks pass, record `status: planned`, `validation.status: ready`,
exact task identity, start node, validated nodes and checked source references
in the existing task-owned plan artifact using the declared project services.
On failure, stop before subsequent lookups or package preparation and use
[the task-owned diagnostic contract](ora-resource/ora_error_handling.md#task-owned-diagnostic-contract)
with `input_validation` or `catalog_or_metadata_mismatch` as applicable. No
readiness override is permitted. Revalidate for each new run or changed task
source; a prior plan is not evidence that the current rules passed.

During the remaining workflow, start at `PROLE.VALIDATE_INPUT`, satisfy every
prerequisite, evaluate applicability and apply only the reached source rule.
Record sanitized evidence and the observed outcome; follow its declared
transition and stop at a terminal. Do not execute all nodes by sequence number
or treat an undeclared outcome as success. Live reads retain the declared core
client and their existing gates. `PROLE.RETURN_SUCCESS` means validation and
preparation only. This early check neither replaces final-artifact Task Hook
validation nor supplies Data Loader approval or submission authority.

In task-owned preparation evidence, retain the normalized request fingerprint,
current node, completed path/outcomes, sanitized resolver/default evidence,
missing requirements and safe resume stage. Follow the existing diagnostic and
redaction contract; do not add fields to the skill-run schema or create copies
of delegated loader records. Return task identity, actual stage, blockers and
one safe next action. On resume, compare request fingerprints and refresh
changed evidence; changed input, target or artifact requires fresh validation
and approval. Reconcile uncertain submissions only through workflow step 8.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `qualification_requirements`: one or more Requirements display names; each row may also give Mandatory Requirement (Yes/No), Proficiency Level, and Reading/Speaking/Writing levels. An explicit `Keyword` is a separate free-text form.

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent skill for sequencing. CSV column mappings are a working contract inherited from this task's resources; they are not evidence of a target's blank template or serialization. `verify_project_role_package` must prove the target-specific members, headers and conditional child wrapper before preparation/import. Track token usage for task-owned planning/validation using the manifest policy; delegated Data Loader reporting and persistence restrictions take precedence during its execution.

The UI labels **From Date** and **To Date** map to `StartDateActive` and `EndDateActive`. Name and From Date are required for creation; Enterprise Role and To Date are optional. Existing dates shown in the reference image do not establish a create default.

Oracle/ADE references and evidence limits are retained with their owning rules: [input and CSV provenance](ora-resource/ora_input_validation.md#input-and-csv-source-evidence), [lookup references](ora-resource/ora_reference_lookups.md#source-references-and-evidence-limits), and [design source](ora-resource/ora_design_enforcement.md#design-source-reference). Use [golden scenarios](../../noship/tests/project-foundation/manage-project-roles/golden-scenarios.md) for offline domain-rule and graph review. These resources do not authorize live execution.
