---
skill_id: "scm.procurement.external-purchase-prices"
name: "External Purchase Prices Implementation Guidance"
description: "Provides SCM Procurement implementation guidance for the External Purchase Prices functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "External Purchase Prices"
functional_area_code: "ORA_EXTERNAL_PURCHASE_PRICES"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "external_purchase_prices_scope"
  - "external_purchase_prices_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/external-purchase-prices/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/external-purchase-prices/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/external-purchase-prices/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_REQBU_MAPPING"
  - "ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_PA_DEFAULTS"
  - "ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_SELECTION_CRITERIA"
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

# External Purchase Prices Implementation Guidance

## Purpose

Provides SCM Procurement implementation guidance for the External Purchase Prices functional area.

## When to Use

Use this functional-area skill after Procurement scope is confirmed and the project needs external purchase prices setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Procurement` (`PO_PROCUREMENT`)
- Functional area / Setup Object: `External Purchase Prices` (`ORA_EXTERNAL_PURCHASE_PRICES`)

## Setup Tasks

1. [Manage External Purchase Prices Requisitioning BU Mapping](manage-external-purchase-prices-requisitioning-bu-mapping/SKILL.md) (`ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_REQBU_MAPPING`)
2. [Manage External Purchase Prices Purchase Agreement Defaults](manage-external-purchase-prices-purchase-agreement-defaults/SKILL.md) (`ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_PA_DEFAULTS`)
3. [Manage External Purchase Prices Selection Criteria](manage-external-purchase-prices-selection-criteria/SKILL.md) (`ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_SELECTION_CRITERIA`)

## Inputs

- `implementation_objective`
- `project_context`
- `external_purchase_prices_scope`
- `external_purchase_prices_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
