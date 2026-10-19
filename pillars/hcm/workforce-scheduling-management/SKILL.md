---
skill_id: "hcm.workforce-scheduling-management"
name: "Workforce Scheduling Management"
description: "Coordinates HCM implementation guidance for the Workforce Scheduling Management offering."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Scheduling Management"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Workforce Scheduling Management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "workforce_scheduling_management_requirements"
outputs:
  - "offering_scope"
  - "functional_area_skill_plan"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
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
  - "scope"
  - "skill_path"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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
side_effects: []
required_privileges: []
---

# Workforce Scheduling Management

## Purpose

Coordinates HCM Workforce Scheduling Management implementation guidance across functional areas, setup tasks, and standard implementation activities.

## When to Use

Use this offering-level skill after Workforce Scheduling Management is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `HCM`
- Pillar slug: `hcm`
- Offering code: `ORA_WORKFORCE_SCHEDULING_MANAGEMENT`
- Offering slug: `workforce-scheduling-management`
- Offering folder: `pillars/hcm/workforce-scheduling-management`
- Offering mapping source: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

This skill routes control to functional-area skills created by developers under this folder. Developers should create functional-area skills with `core.fusion-dev.pillar-skill-gen` using the catalog-backed path pattern:

```text
pillars/hcm/workforce-scheduling-management/{functional-area-slug}/
```

When a requested functional area is not yet present under this offering, use the setup catalog below to identify the matching functional area and invoke `core.fusion-dev.pillar-skill-gen` to generate the child skill before adding functional-area-specific guidance.

## Inputs

- `implementation_objective`
- `project_context`
- `hcm_scope`
- `workforce_scheduling_management_requirements`

## Outputs

- `workforce_scheduling_management_scope`
- `functional_area_skill_plan`
- `workforce_scheduling_management_work_products`
- `token_usage_record`

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_WORKFORCE_SCHEDULING_MANAGEMENT`
Functional area count: `10`
Setup task count: `28`

- `ORA_WORKFORCE_SCHEDULING_COMMON`: Workforce Scheduling Common
- `ORA_WORKFORCE_SCHEDULING_ENTERPRISE`: Workforce Scheduling Enterprise
- `ORA_WORKFORCE_SCHEDULING_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`: Workforce Scheduling Legal and Legislative Organizations
- `ORA_WORKFORCE_SCHEDULING_HCM_TOOL`: Workforce Scheduling HCM Tool
- `ORA_WORKFORCE_SCHEDULING_PERSON_RECORD`: Workforce Scheduling Person Record
- `ORA_WORKFORCE_SCHEDULING_EMPLOYMENT_ACTIONS_FRAMEWORK`: Workforce Scheduling Employment Actions Framework
- `ORA_WFM_COMMON`: WFM Common
- `ORA_WORKFORCE_SCHEDULING_ABSENCE`: Workforce Scheduling Absence
- `ORA_WORKFORCE_SCHEDULING_TIME_AND_LABOR`: Workforce Scheduling Time and Labor
- `ORA_SCHEDULING`: Scheduling

## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
