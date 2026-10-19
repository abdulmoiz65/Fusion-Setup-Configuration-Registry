---
skill_id: "shared.extensibility.extensibility-strategy-advisor"
name: "Extensibility Strategy Advisor"
description: "Provides cross-pillar extensibility strategy advisor guidance for Oracle Fusion Cloud implementations."
layer: "shared"
pillar: "Common"
type: "advisory"
execution_mode: "advisory"
owner_team: "Shared enablement team with pillar review"
version: "0.1.0"
inputs: 
  - "implementation_objective"
  - "project_context"
  - "pillar_scope"
  - "offering_scope"
  - "functional_area_scope"
outputs: 
  - "recommendations"
  - "work_products"
  - "review_points"
  - "token_usage_record"
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

# Extensibility Strategy Advisor

## Purpose

Provides cross-pillar extensibility strategy advisor guidance for Oracle Fusion Cloud implementations.

## When to Use

Use this shared skill when the implementation activity applies across multiple pillars or should be standardized before being specialized by ERP, HCM, SCM, CX, or common setup areas.

## Inputs

- `implementation_objective`
- `project_context`
- `pillar_scope`
- `offering_scope`
- `functional_area_scope`

## Outputs

- `recommendations`
- `work_products`
- `review_points`

## Implementation Notes

Keep outputs reusable by pillar skills. Where the guidance depends on a specific offering, country, or release, capture that condition in the work product rather than hardcoding it in the generic shared method.
