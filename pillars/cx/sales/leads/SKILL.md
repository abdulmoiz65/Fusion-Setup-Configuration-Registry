---
skill_id: "cx.sales.leads"
name: "Leads Implementation Guidance"
description: "Routes CX Sales Leads implementation work to qualification-template, profile-option, and standard-lookup setup tasks. Use for Lead setup and for requests to inventory, review, create, update, or delete Sales Lead profile-option values or standard lookup codes in a configured Fusion environment."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Leads"
functional_area_code: "ORA_LDS_LEADS"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.7.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "leads_scope"
  - "leads_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE"
  - "MKL_MANAGE_SALES_LEAD_PROFILE_OPTIONS"
  - "MKL_MANAGE_SALES_LEAD_STANDARD_LOOKUPS"
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

# Leads Implementation Guidance

## Purpose

Provides CX Sales implementation guidance for the Leads functional area.

## When to Use

Use this functional-area skill after Sales scope is confirmed and the project needs leads setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Sales` (`ORA_MIDSIZE_SALES`)
- Functional area / Setup Object: `Leads` (`ORA_LDS_LEADS`)

## Setup Tasks

1. [Manage Sales Lead Qualification Template](manage-sales-lead-qualification-template/SKILL.md) (`MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE`)
2. [Manage Sales Lead Profile Options](manage-sales-lead-profile-options/SKILL.md) (`MKL_MANAGE_SALES_LEAD_PROFILE_OPTIONS`)
3. [Manage Sales Lead Standard Lookups](manage-sales-lead-standard-lookups/SKILL.md) (`MKL_MANAGE_SALES_LEAD_STANDARD_LOOKUPS`)

## Task Routing

- Route Lead qualification-template creation, copying, inventory, review, or
  deployment-readiness requests to
  [Manage Sales Lead Qualification Template](manage-sales-lead-qualification-template/SKILL.md).
- Route any request to list Sales Lead profile options, return current or
  configured values, review an exact profile-option code, or create, update,
  set, remove, or delete configured profile-option values
  to
  [Manage Sales Lead Profile Options](manage-sales-lead-profile-options/SKILL.md).
  This includes short follow-ups such as "what is the current value?" when the
  immediately preceding context contains one exact profile-option code. Do not
  answer these requests from Oracle documentation or delivered defaults.
- Route Sales Lead lookup inventory, code review, or lookup-code create,
  update, disable, or safe delete to
  [Manage Sales Lead Standard Lookups](manage-sales-lead-standard-lookups/SKILL.md).

After routing, load and execute the selected nested task skill and its compiled
task graph. Do not return a functional-area summary as the terminal response to
a task-specific environment request.

## Runtime Interface Efficiency

Prefer the declared skill interfaces during routine execution. Treat existing
`core` and `shared` utilities as callable implementations: use the owning
`SKILL.md` contract first and the utility's `--help` output when invocation
syntax remains unclear. Avoid proactively enumerating implementation scripts,
searching for alternative execution paths, or reading implementation and test
source to rediscover an interface that the selected skills already document.

Load task-local rule sources as their graph nodes become relevant. Load only the
executor declared by the selected child task. Profile-option value CRUD uses
`core.fusion-api.apps-common`; Sales Lead standard lookup-code CRUD uses the
same core route. Do not load Data Loader or build FSM packages for either task.
Other nested tasks may still declare Data Loader for their own mutations.
Inventory and Review do not need mutation-executor details.

When a declared command fails unexpectedly, rejects documented inputs, or
returns an undocumented shape, keep source inspection available as a diagnostic
step. Inspect the smallest relevant function or module, use tests only when the
framework behavior itself is under diagnosis, record the resolved interface,
and reuse it for the remainder of the run instead of rereading the same code.

Nested Sales Lead tasks provide business evidence and documented handoff fields
only. Leave authentication, HTTP/loader transport, and executor-specific
representations to the owning core skill instead of reconstructing them from
source.

## Inputs

- `implementation_objective`
- `project_context`
- `leads_scope`
- `leads_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
