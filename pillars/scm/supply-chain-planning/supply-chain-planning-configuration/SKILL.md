---
skill_id: "scm.supply-chain-planning.supply-chain-planning-configuration"
name: "Supply Chain Planning Configuration Implementation Guidance"
description: "Provides SCM Supply Chain Planning implementation guidance for the Supply Chain Planning Configuration functional area."
layer: "pillar"
pillar: "SCM"
offering: "Supply Chain Planning"
functional_area: "Supply Chain Planning Configuration"
functional_area_code: "ORA_MSC_VC_PLANNING_CONFIGURAT"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM supply chain planning pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "supply_chain_planning_configuration_scope"
  - "supply_chain_planning_configuration_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/supply-chain-planning/supply-chain-planning-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/supply-chain-planning/supply-chain-planning-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/supply-chain-planning/supply-chain-planning-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "MSC_MANAGE_PLANNING_SOURCE_SYSTEMS"
  - "ORA_MSC_CONFIGURE_PLANNING_ANALYTICS"
  - "ORA_MSC_LOAD_PLANNING_DATA_FROM_FLAT_FILES"
  - "CUSTOM_MSC_MANAGE_PLANNING_MEASURES"
  - "CUSTOM_PLANNING_VISUALIZATIONS"
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

# Supply Chain Planning Configuration Implementation Guidance

## Purpose

Provides SCM Supply Chain Planning implementation guidance for the Supply Chain Planning Configuration functional area.

## When to Use

Use this functional-area skill after Supply Chain Planning scope is confirmed and the project needs supply chain planning configuration setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Supply Chain Planning` (`ORA_MSC_VALUE_CHAIN_PLANNING`)
- Functional area / Setup Object: `Supply Chain Planning Configuration` (`ORA_MSC_VC_PLANNING_CONFIGURAT`)

## Setup Tasks

1. [Manage Planning Source Systems](manage-planning-source-systems/SKILL.md) (`MSC_MANAGE_PLANNING_SOURCE_SYSTEMS`)
2. [Configure Planning Analytics](configure-planning-analytics/SKILL.md) (`ORA_MSC_CONFIGURE_PLANNING_ANALYTICS`)
3. [Load Planning Data from Files](load-planning-data-from-files/SKILL.md) (`ORA_MSC_LOAD_PLANNING_DATA_FROM_FLAT_FILES`)
4. [Manage Planning Measures](manage-planning-measures/SKILL.md) (`CUSTOM_MSC_MANAGE_PLANNING_MEASURES`)
5. [Manage Planning Visualizations](manage-planning-visualizations.md) (`CUSTOM_PLANNING_VISUALIZATIONS`)

## Inputs

- `implementation_objective`
- `project_context`
- `supply_chain_planning_configuration_scope`
- `supply_chain_planning_configuration_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
