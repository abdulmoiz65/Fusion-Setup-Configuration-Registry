---
skill_id: "erp.project-financial-management"
name: "Project Financial Management"
description: "Provides ERP Project Financial Management offering context, domain guidance and catalog-backed functional-area references to the active implementation workflow."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP Project Financial Management pillar team"
version: "0.1.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "erp_scope"
  - "project_financial_management_requirements"
outputs:
  - "project_financial_management_scope"
  - "functional_area_skill_plan"
  - "project_financial_management_work_products"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.artifact-version-manager"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/current/"
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
  - "Writes offering-owned project artifacts, artifact registrations, declared state updates, skill-run records and token-usage records through the existing core project services."
required_privileges: []
---

# Project Financial Management

## Purpose

Provide offering-specific context, domain guidance and catalog-backed functional-area references after the implementation router and shared scope-definition workflow have established Project Financial Management scope. The active workflow owns route selection, ordered task execution, approvals and cross-functional-area handoffs.

## When to Use

Use this offering-level skill after Project Financial Management is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `ERP`
- Pillar slug: `erp`
- Offering code: `PJF_PROJ_MNG`
- Offering slug: `project-financial-management`
- Offering folder: `pillars/erp/project-financial-management`
- Offering mapping source: `knowledge/setup-task-catalog/release/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/release/offering-functional-area-task-catalog.json`

## Functional-Area References and Ownership

Before any child workflow executes a REST request, require the offering's
[REST version and query compatibility preflight](references/rest-query-compatibility.md).
The selected core client or workflow owns framework-version selection; pillar
queries and the outgoing header must agree with it. This check does not authorize
external execution or replace the child's declared workflow gates.

This skill supplies matching functional-area references to the active workflow; it does not start, sequence or own an implementation program. Functional-area references use the catalog-backed path pattern:

```text
pillars/erp/project-financial-management/{functional-area-slug}/
```

When the catalog matches a task but its skill is absent, retain the exact task identity and report the missing capability to the active workflow. Do not invent a path, generate a skill during setup execution, or substitute a live integration. The workflow selects any declared manual-task route and its prerequisites, or records a blocker. Skill generation is a separate developer authoring activity.

## Cross-Functional Task Discovery

Resolve every requested or next runbook task through `shared.implementation-planning.offering-task-map-builder` and use its catalog-backed `task_code`, `functional_area`, and `skill_path`. Do not infer a task-code prefix, functional area, or filesystem path from the preceding task: an ordered implementation can hand off between functional areas within this offering.

Before declaring a task skill absent or recording a workflow gap:

1. Resolve the exact task name against `knowledge/setup-task-catalog/effective/setupTasksAll.json`.
2. Use the resolved task code to search all descendant task manifests under `pillars/erp/project-financial-management`, not only the preceding functional-area folder.
3. Follow the matched manifest's declared `parent_skill_id` and confirm it in that functional-area skill's Setup Tasks list.

A failed guessed path is not evidence of a missing skill. If an ad hoc diagnostic is still needed, search manifest contents or full paths; do not combine a task-name basename predicate with `-name SKILL.md`, because both predicates test the same basename and can incorrectly return no matches.

Known cross-functional handoff: `Manage Project Types` is under Project Foundation, while the subsequent `Manage Project Plan Types` task is under Project Control with code `PJO_MANAGE_PROJECT_PLAN_TYPES` and skill `erp.project-financial-management.project-control.manage-project-plan-types`.

The catalog lists the whole offering; it does not promise that every functional-area skill is implemented in this checkout. Return the resolved facts and missing capability to the workflow without changing its current step or approvals.

## Inputs

- `implementation_objective`
- `project_context`
- `erp_scope`
- `project_financial_management_requirements`

## Outputs

- `project_financial_management_scope`
- `functional_area_skill_plan`
- `project_financial_management_work_products`
- `skill_run_record`
- `token_usage_record`

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/release/offering-functional-area-task-catalog.json`
Offering code: `PJF_PROJ_MNG`
Functional area count: `20`
Setup task count: `292`

- `ORA_ASK_INITIAL_USER`: Initial Users
- `ORA_ASK_ENTERPRISE_PROFILE`: Enterprise Profile
- `ORA_ASK_LEGAL_STRUCTURES`: Legal Structures
- `ORA_ASK_FIN_REPORTING_STRUCT`: Financial Reporting Structures
- `ORA_ASK_ORGANIZATION_STRUCTURE`: Organization Structures
- `ORA_ASK_WORKFORCE_STRUCTURE`: Workforce Structures
- `ORA_PJF_PROJ_ORG`: Project Organizations
- `ORA_ASK_USERS_AND_SECURITY`: Users and Security
- `ORA_PJF_PROJECT_FOUNDATION_FA`: Project Foundation
- `PJF_BURDENING`: Burdening
- `PJF_PJO_DEPLOYED`: Project Control
- `ORA_PJC_PROJ_COSTING_BASE_FA`: Project Costing Base
- `PJC_CAPITAL_PROJECTS`: Capital Projects
- `OKC_PROJECT_CONTRACTS`: Project Contracts
- `ORA_PJB_PROJ_BILLING_BASE_FA`: Project Billing Base
- `PJB_INTERCOMPANY_BILLING`: Internal Project Billing
- `FIN_APPLICABILITY_ZX`: Transaction Tax
- `PJF_PJS_DEPLOYED`: Project Performance Reporting
- `ORA_PJC_PROJECT_ACCOUNTING`: Project Accounting
- `ORA_ASK_APPLICATION_EXTENSIONS`: Application Extensions

## Implementation Notes

- Summarize the approved offering scope and applicable domain guidance here. The existing output names remain compatible: `project_financial_management_scope` summarizes shared scope decisions, and `functional_area_skill_plan` supplies catalog-backed recommendations, not an authoritative execution sequence.
- Delegate scope decisions to `shared.project-intake.scope-definition`, route selection to the implementation router, and instantiated sequencing and cross-functional-area handoffs to the active workflow. Do not update their authoritative scope, skill path or setup-task sequence from this pillar.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.

## Durable Artifacts and Review

For offering-owned durable outputs, resolve the selected `project_id` from the
existing `project_context` and active workflow. Reuse prior project artifacts.
If no implementation project exists, follow the repository project-initialization
policy before writing; do not add a new required caller input or infer a different
project. An ambiguous project identity is an `input_validation` blocker.

1. Save the offering scope summary, functional-area recommendations and applicable
   work products under the declared offering artifact location. These outputs
   describe the approved scope and recommendations; they do not change the
   workflow's authoritative scope, route, current step or setup-task sequence.
2. Use `core.project-mgmt.artifact-version-manager` for new major versions and
   confirmed minor updates. Register durable artifacts through
   `core.project-mgmt.artifact-registry-manager` using
   `schemas/project-artifact.schema.json`, including producing skill, location,
   version, status, timestamps and checksum when available.
3. Use `core.project-mgmt.project-state-manager` to record the run under
   `project/{project_id}/state/runs/` and update only the declared offering-owned
   state fields when their work products change. The `skill_run_record` must
   conform to `schemas/skill-run.schema.json`, retain input/output and artifact
   references, and record the actual status. Append a run for a no-change revisit
   without replacing existing artifacts.
4. Record token usage at the manifest's shared token-log location using the core
   project service's token-usage guidance, and include the estimate and log
   reference in the run record. Exclude credentials and token-cache contents.

Before writing, validate project identity, destination paths, artifact metadata
and versioning requirements. On persistence failure, stop the affected handoff,
classify it as `artifact_persistence`, retain safely written artifacts, and report
their references and the next recovery action. Record the failed run and redacted
diagnostics in the selected project when writable; if that write also fails,
report the intended path and failure without claiming completion. Never persist
credentials, tokens, private keys or sensitive payloads. This local persistence
step does not invoke child setup execution or authorize external operations.
