---
skill_id: "shared.best-practices.security-role-guidance"
name: "Security Role Guidance"
description: "Provides cross-pillar security role guidance guidance for Oracle Fusion Cloud implementations."
layer: "shared"
pillar: "Common"
type: "advisory"
execution_mode: "advisory"
owner_team: "Shared enablement team with pillar review"
version: "0.1.1"
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
  - "security_role_guidance_report"
  - "artifact_index_entry"
  - "token_usage_record"
uses_core: []
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
  - "reports"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/shared/best-practices/security-role-guidance/current/security-role-guidance.md"
    versioning_policy: "major-new-version-minor-confirm-update"
applicability:
  industries: 
    - "All"
  countries: 
    - "All"
  fusion_releases: 
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Writes security role guidance to the active project workspace."
  - "Registers the guidance report in the project artifact index when a project workspace is active."
required_privileges: []
---

# Security Role Guidance

## Purpose

Provides cross-pillar security role guidance guidance for Oracle Fusion Cloud implementations.

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
- `security_role_guidance_report`
- `artifact_index_entry`

## Project Workspace Persistence

Every invocation must save the generated guidance into the active project
workspace when `project_context` includes a project ID or project workspace
root.

Default report location:

```text
project/{project_id}/artifacts/shared/best-practices/security-role-guidance/current/security-role-guidance.md
```

The saved report must include:

- Project ID, project name, phase, pillar scope, offering scope, and functional
  area scope when available.
- The generated recommendations, work products, and review points.
- Any assumptions caused by missing project objective, scope, country, industry,
  or environment information.

After writing the report, register it in:

```text
project/{project_id}/artifacts/artifact-index.json
```

Use artifact type `report`, skill ID
`shared.best-practices.security-role-guidance`, and the repository project
artifact versioning policy. Record a skill-run audit entry under:

```text
project/{project_id}/state/runs/
```

## Implementation Notes

Keep outputs reusable by pillar skills. Where the guidance depends on a specific
offering, country, or release, capture that condition in the work product rather
than hardcoding it in the generic shared method.

Do not store credentials, access tokens, client secrets, private keys, or copied
environment secret values in the security role guidance report, artifact index,
or skill-run record.
