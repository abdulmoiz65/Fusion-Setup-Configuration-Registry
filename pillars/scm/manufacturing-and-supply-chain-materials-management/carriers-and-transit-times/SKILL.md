---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.carriers-and-transit-times"
name: "Carriers and Transit Times Implementation Guidance"
description: "Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Carriers and Transit Times functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Carriers and Transit Times"
functional_area_code: "ORA_RCS_CARRIERS_TRANSIT_TIMES"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "carriers_and_transit_times_scope"
  - "carriers_and_transit_times_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/carriers-and-transit-times/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/carriers-and-transit-times/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/carriers-and-transit-times/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "WSH_MANAGE_CARRIERS"
  - "WSH_MANAGE_TRANSIT_TIMES"
  - "ORA_RCS_MANAGE_SHIPPING_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_RCS_MANAGE_TRANSIT_TIMES_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_RCS_MANAGE_CARRIERS_VALUE_SETS"
  - "ORA_RCS_MANAGE_TRANSIT_TIMES_VALUE_SETS"
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

# Carriers and Transit Times Implementation Guidance

## Purpose

Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Carriers and Transit Times functional area.

## When to Use

Use this functional-area skill after Manufacturing and Supply Chain Materials Management scope is confirmed and the project needs carriers and transit times setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Manufacturing and Supply Chain Materials Management` (`ORA_MANUFACTURING_AND_SUPPLY_C`)
- Functional area / Setup Object: `Carriers and Transit Times` (`ORA_RCS_CARRIERS_TRANSIT_TIMES`)

## Setup Tasks

1. [Manage Carriers](manage-carriers/SKILL.md) (`WSH_MANAGE_CARRIERS`)
2. [Manage Transit Times](manage-transit-times/SKILL.md) (`WSH_MANAGE_TRANSIT_TIMES`)
3. [Manage Carriers Descriptive Flexfields](manage-carriers-descriptive-flexfields.md) (`ORA_RCS_MANAGE_SHIPPING_DESCRIPTIVE_FLEXFIELDS`)
4. [Manage Transit Times Descriptive Flexfields](manage-transit-times-descriptive-flexfields.md) (`ORA_RCS_MANAGE_TRANSIT_TIMES_DESCRIPTIVE_FLEXFIELDS`)
5. [Manage Carriers Value Sets](manage-carriers-value-sets.md) (`ORA_RCS_MANAGE_CARRIERS_VALUE_SETS`)
6. [Manage Transit Times Value Sets](manage-transit-times-value-sets.md) (`ORA_RCS_MANAGE_TRANSIT_TIMES_VALUE_SETS`)

## Inputs

- `implementation_objective`
- `project_context`
- `carriers_and_transit_times_scope`
- `carriers_and_transit_times_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
