---
skill_id: "erp.risk-and-security.activate-algorithms"
name: "Activate Algorithms Implementation Guidance"
description: "Provides ERP Risk and Security implementation guidance for the Activate Algorithms functional area."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Activate Algorithms"
functional_area_code: "ORA_GTG_ACTIVATE_ALGORITHMS"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP risk and security pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "activate_algorithms_scope"
  - "activate_algorithms_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "erp.risk-and-security.activate-algorithms.activate-audit-policies"
  - "erp.risk-and-security.activate-algorithms.activate-algorithms"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/activate-algorithms/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/activate-algorithms/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/activate-algorithms/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_GTG_ACTIVATE_AUDIT_POLICIES"
  - "ORA_GTG_ACTIVATE_ALGORITHMS"
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

# Activate Algorithms Implementation Guidance

## Purpose

Provides ERP Risk and Security implementation guidance for the Activate Algorithms functional area.

## When to Use

Use this functional-area skill after Risk and Security scope is confirmed and the project needs activate algorithms setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Risk and Security` (`ORA_RISK_AND_CONTROLS`)
- Functional area / Setup Object: `Activate Algorithms` (`ORA_GTG_ACTIVATE_ALGORITHMS`)

## Setup Tasks

1. [Activate Audit Policies](activate-audit-policies/SKILL.md) (`ORA_GTG_ACTIVATE_AUDIT_POLICIES`)
2. [Activate Algorithms](activate-algorithms/SKILL.md) (`ORA_GTG_ACTIVATE_ALGORITHMS`)

Strongly recommend completing and verifying **Activate Audit Policies** in the
same environment before beginning **Activate Algorithms**. A planned backend
validation is expected to reject an algorithm activation when its audit
policies are disabled. This is currently a sequencing recommendation, not a
claim that the backend check already exists.

## Execution Routing

This parent skill provides functional-area guidance. For an **Activate
Algorithms** implementation run, first route to **Activate Audit Policies**,
then invoke its declared child
[Activate Algorithms](activate-algorithms/SKILL.md). Its executable planner is
`activate-algorithms/scripts/execute.py` relative to that child skill, not
`scripts/execute.py` relative to this parent.

When the consultant explicitly defers **Activate Audit Policies** and selects
**Activate Algorithms** as the next task, route directly to that child after
recording the deferral. This does not make audit coverage ready or bypass the
algorithm child's own readiness, approval, or publication gates.

When the durable workflow re-invokes either child, it may provide that child’s
[Phase Evidence Handoff](../references/phase-evidence-handoff.md) for valid
same-environment read-only evidence. The verified Audit Policies result is
reused only for its immediate approval path; it does not authorize publication.
Do not begin algorithm publication while Audit Policies is awaiting an
approval or verification. An explicit Audit Policies deferral is not an
awaiting state; it permits only the requested task switch.

## Inputs

- `implementation_objective`
- `project_context`
- `activate_algorithms_scope`
- `activate_algorithms_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
