---
skill_id: "hcm.hcm-security.configure-public-workers-for-oracle-search"
name: "Configure Public Workers for Oracle Search Implementation Guidance"
description: "Provides HCM HCM Security implementation guidance for the Configure Public Workers for Oracle Search functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Security"
functional_area: "Configure Public Workers for Oracle Search"
functional_area_code: "ORA_CONFIGURE_PUBLIC_WORKERS_FOR_ORACLE_SEARCH"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm security pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "configure_public_workers_for_oracle_search_scope"
  - "configure_public_workers_for_oracle_search_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/configure-public-workers-for-oracle-search/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/configure-public-workers-for-oracle-search/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/configure-public-workers-for-oracle-search/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_PER_CONFIGURE_PUBLIC_WORKER_ACCESS"
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

# Configure Public Workers for Oracle Search Implementation Guidance

## Purpose

Provides HCM HCM Security implementation guidance for the Configure Public Workers for Oracle Search functional area.

## When to Use

Use this functional-area skill after HCM Security scope is confirmed and the project needs configure public workers for oracle search setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Security` (`ORA_HCM_SECURITY`)
- Functional area / Setup Object: `Configure Public Workers for Oracle Search` (`ORA_CONFIGURE_PUBLIC_WORKERS_FOR_ORACLE_SEARCH`)

## Setup Tasks

1. [Configure Public Worker Access](configure-public-worker-access/SKILL.md) (`ORA_PER_CONFIGURE_PUBLIC_WORKER_ACCESS`)

## Inputs

- `implementation_objective`
- `project_context`
- `configure_public_workers_for_oracle_search_scope`
- `configure_public_workers_for_oracle_search_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
