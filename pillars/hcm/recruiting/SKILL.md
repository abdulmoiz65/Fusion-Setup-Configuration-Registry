---
skill_id: "hcm.recruiting"
name: "Recruiting"
description: "Coordinates HCM Recruiting implementation guidance and routes work to developer-created functional-area skills."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_scope"
  - "recruiting_requirements"
outputs:
  - "recruiting_scope"
  - "functional_area_skill_plan"
  - "recruiting_work_products"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
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
  - "scope"
  - "skill_path"
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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

# Recruiting

## Purpose

Coordinates HCM Recruiting implementation guidance across functional areas, setup tasks, and standard implementation activities.

## When to Use

Use this offering-level skill after Recruiting is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `HCM`
- Pillar slug: `hcm`
- Offering code: `ORA_RECRUITING`
- Offering slug: `recruiting`
- Offering folder: `pillars/hcm/recruiting`
- Offering mapping source: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

This skill routes control to functional-area skills created by developers under this folder. Developers should create functional-area skills with `core.fusion-dev.pillar-skill-gen` using the catalog-backed path pattern:

```text
pillars/hcm/recruiting/{functional-area-slug}/
```

When a requested functional area is not yet present under this offering, use the setup catalog below to identify the matching functional area and invoke `core.fusion-dev.pillar-skill-gen` to generate the child skill before adding functional-area-specific guidance.

## Inputs

- `implementation_objective`
- `project_context`
- `hcm_scope`
- `recruiting_requirements`

## Outputs

- `recruiting_scope`
- `functional_area_skill_plan`
- `recruiting_work_products`
- `token_usage_record`

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_RECRUITING`
Functional area count: `12`
Setup task count: `59`

- `ORA_RECRUITING_ADDRESS_VALIDATION`: Recruiting Address Validation
- `ORA_RECRUITING_COMMON`: [Recruiting Common](recruiting-common/SKILL.md)
- `ORA_RECRUITING_LOCATIONS`: Recruiting Locations
- `ORA_RECRUITING_JOBS`: Recruiting Jobs
- `ORA_RECRUITING_HCM_TREES`: Recruiting HCM Trees
- `ORA_RECRUITING_PAYROLL_TOOLS`: Recruiting Payroll Tools
- `ORA_RECRUITING_BENEFITS_ELIGIBILITY`: Recruiting Benefits Eligibility
- `ORA_RECRUITING_HCM_TOOL`: Recruiting HCM Tool
- `ORA_RECRUITING_FOUNDATION_DATA`: Recruiting Foundation
- `ORA_CANDIDATE_EXPERIENCE_CONFIGURATION`: Candidate Experience Configuration
- `ORA_RECRUITING_CONFIGURATION`: Recruiting Configuration
- `ORA_RECRUITING_CONTENT`: Recruiting Content

## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
