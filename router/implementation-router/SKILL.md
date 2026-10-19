---
skill_id: "router.implementation-router"
name: "Implementation Router"
description: "Accepts an implementation objective and routes the work to the appropriate shared, core, and pillar skills."
layer: "router"
pillar: "Router"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central architecture or platform team"
version: "0.1.0"
inputs: 
  - "implementation_objective"
  - "project_context"
  - "available_skill_catalog"
outputs: 
  - "routed_workflow"
  - "initial_next_actions"
  - "routing_rationale"
  - "token_usage_record"
depends_on:
  - "router.project-objective-classifier"
  - "router.next-action-planner"
uses_core: []
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

# Implementation Router

## Purpose

Accepts an implementation objective and routes the work to the appropriate shared, core, and pillar skills.

## When to Use

Use this router skill at the start of an implementation workflow or whenever the current workflow state must be reclassified, resequenced, or routed to the next responsible skill.

## Inputs

- `implementation_objective`
- `project_context`
- `available_skill_catalog`

## Outputs

- `routed_workflow`
- `initial_next_actions`
- `routing_rationale`

## Implementation Notes

Keep routing decisions explainable. Persist the selected skill IDs, confidence, assumptions, and human review points so downstream skills can continue from the same context.

## Initial Run Book Gate

For a newly initialized project, inspect `state/project-state.json` before routing a Fusion mutation. Run Book creation is owned by `core.project-mgmt.project-workspace-initializer` and `core.runbook`; do not infer or change its creation state in the router. Do not route to Data Loader or another Fusion-submission workflow until `runbook_control.status` is `active`. `pending`, `failed`, and `unknown` are blocking states. Local artifact refresh does not reset existing Run Book state; only pending, unbound projects are eligible for initial Oracle creation.
