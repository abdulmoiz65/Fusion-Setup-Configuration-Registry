---
skill_id: "router.next-action-planner"
name: "Next Action Planner"
description: "Determines the next recommended skill or human action based on workflow state, dependencies, and readiness."
layer: "router"
pillar: "Router"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central architecture or platform team"
version: "0.1.0"
inputs: 
  - "objective_classification"
  - "workflow_state"
  - "dependency_graph"
  - "validation_results"
outputs: 
  - "next_action_plan"
  - "recommended_skill_ids"
  - "human_review_points"
  - "token_usage_record"
depends_on:
  - "router.project-objective-classifier"
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

# Next Action Planner

## Purpose

Determines the next recommended skill or human action based on workflow state, dependencies, and readiness.

## When to Use

Use this router skill at the start of an implementation workflow or whenever the current workflow state must be reclassified, resequenced, or routed to the next responsible skill.

## Inputs

- `objective_classification`
- `workflow_state`
- `dependency_graph`
- `validation_results`

## Outputs

- `next_action_plan`
- `recommended_skill_ids`
- `human_review_points`

## Implementation Notes

Keep routing decisions explainable. Persist the selected skill IDs, confidence, assumptions, and human review points so downstream skills can continue from the same context.
