---
skill_id: "hcm.hcm-tool"
name: "HCM Tool"
description: "Coordinates HCM HCM Tool implementation guidance and routes work to developer-created functional-area skills."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM HCM Tool pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_scope"
  - "hcm_tool_requirements"
outputs:
  - "hcm_tool_scope"
  - "functional_area_skill_plan"
  - "hcm_tool_work_products"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/current/"
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

# HCM Tool

## Purpose

Coordinates HCM HCM Tool implementation guidance across functional areas, setup tasks, and standard implementation activities.

## When to Use

Use this offering-level skill after HCM Tool is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `HCM`
- Pillar slug: `hcm`
- Offering code: `CUSTOM_HCM_TOOL`
- Offering slug: `hcm-tool`
- Offering folder: `pillars/hcm/hcm-tool`
- Offering mapping source: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

This skill routes control to functional-area skills created by developers under this folder. Developers should create functional-area skills with `core.fusion-dev.pillar-skill-gen` using the catalog-backed path pattern:

```text
pillars/hcm/hcm-tool/{functional-area-slug}/
```

When a requested functional area is not yet present under this offering, use the setup catalog below to identify the matching functional area and invoke `core.fusion-dev.pillar-skill-gen` to generate the child skill before adding functional-area-specific guidance.

## Inputs

- `implementation_objective`
- `project_context`
- `hcm_scope`
- `hcm_tool_requirements`

## Outputs

- `hcm_tool_scope`
- `functional_area_skill_plan`
- `hcm_tool_work_products`
- `token_usage_record`

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `CUSTOM_HCM_TOOL`
Functional area count: `14`
Setup task count: `40`

- `CUSTOM_QUESTIONNAIRE`: Questionnaire
- `CUSTOM_APPROVAL_RULES`: Approval Rules
- `CUSTOM_APPROVAL_TASK`: Approval Task
- `CUSTOM_APPROVAL_OPTIONS`: Approval Options
- `CUSTOM_PERSON_NOTES`: Person Notes Visibility
- `CUSTOM_PROFILE_RATING_MODEL`: Profile Rating Model Configuration
- `CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY`: Profile Management Content Library Configuration
- `CUSTOM_PROFILE_TYPES_AND_CONTENT_SECTION`: Profile Types and Content Section Configuration
- `CUSTOM_TALENT_PROFILE_NOTIFICATIONS_AND_ALERTS`: Talent Profile Notifications and Alerts Configuration
- `CUSTOM_ALERT_FOUNDATION`: Alert Foundation
- `CUSTOM_PULSE_SURVEY_FOUNDATION`: Pulse Survey Foundation
- `CUSTOM_TOUCHPOINTS_AGGREGATE_DATA_PROCESS`: Touchpoints Aggregate Data Process
- `CUSTOM_HCM_FILTERED_LISTS_FOUNDATION`: HCM Filtered Lists Foundation
- `CUSTOM_PROFILE_MANAGEMENT_DATA_LOAD_MIGRATION_AND_MAINTENANCE`: Profile Management Data Load, Migration, and Maintenance

## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
