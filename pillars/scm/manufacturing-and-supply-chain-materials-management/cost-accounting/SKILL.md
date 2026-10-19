---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
name: "Cost Accounting Implementation Guidance"
description: "Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "cost_accounting_scope"
  - "cost_accounting_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_CST_COST_ORGANIZATIONS"
  - "ORA_CST_COST_BOOKS"
  - "ORA_CST_COST_ORGANIZATION_RELATIONSHIPS"
  - "ORA_CST_COST_COMPONENT_MAPPINGS"
  - "ORA_CST_VALUATION_STRUCTURES"
  - "ORA_CST_COST_PROFILES"
  - "ORA_CST_DEFAULT_COST_PROFILES"
  - "ORA_CST_COST_ANALYSIS_GROUPS"
  - "ORA_CST_COST_ELEMENTS"
  - "ORA_CST_VALUATION_UNITS"
  - "ORA_CST_OVERHEAD_EXPENSE_POOLS"
  - "ORA_CST_ITEM_COST_PROFILES"
  - "ORA_MANAGE_COST_ACCOUNTING_PROFILE_OPTIONS"
  - "ORA_CST_COSTING_LOOKUPS"
  - "CST_MANAGE_COSTING_KEY_FLEXFIELDS"
  - "ORA_CST_OVERHEAD_COST_ELEMENT_GROUPS"
  - "CST_MANAGE_COSTING_DESCRIPTIVE_FLEXFIELDS"
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

# Cost Accounting Implementation Guidance

## Purpose

Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Cost Accounting functional area.

## When to Use

Use this functional-area skill after Manufacturing and Supply Chain Materials Management scope is confirmed and the project needs cost accounting setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Manufacturing and Supply Chain Materials Management` (`ORA_MANUFACTURING_AND_SUPPLY_C`)
- Functional area / Setup Object: `Cost Accounting` (`CST_DEFINE_COST_MANAGEMENT`)

## Setup Tasks

1. [Cost Organizations](cost-organizations/SKILL.md) (`ORA_CST_COST_ORGANIZATIONS`)
2. [Cost Books](cost-books/SKILL.md) (`ORA_CST_COST_BOOKS`)
3. [Cost Organization Relationships](cost-organization-relationships/SKILL.md) (`ORA_CST_COST_ORGANIZATION_RELATIONSHIPS`)
4. [Cost Component Mappings](cost-component-mappings/SKILL.md) (`ORA_CST_COST_COMPONENT_MAPPINGS`)
5. [Valuation Structures](valuation-structures/SKILL.md) (`ORA_CST_VALUATION_STRUCTURES`)
6. [Cost Profiles](cost-profiles/SKILL.md) (`ORA_CST_COST_PROFILES`)
7. [Default Cost Profiles](default-cost-profiles/SKILL.md) (`ORA_CST_DEFAULT_COST_PROFILES`)
8. [Cost Analysis Groups](cost-analysis-groups/SKILL.md) (`ORA_CST_COST_ANALYSIS_GROUPS`)
9. [Cost Elements](cost-elements/SKILL.md) (`ORA_CST_COST_ELEMENTS`)
10. [Valuation Units](valuation-units/SKILL.md) (`ORA_CST_VALUATION_UNITS`)
11. [Overhead Expense Pools](overhead-expense-pools/SKILL.md) (`ORA_CST_OVERHEAD_EXPENSE_POOLS`)
12. [Item Cost Profiles](item-cost-profiles/SKILL.md) (`ORA_CST_ITEM_COST_PROFILES`)
13. [Manage Cost Accounting Profile Options](manage-cost-accounting-profile-options/SKILL.md) (`ORA_MANAGE_COST_ACCOUNTING_PROFILE_OPTIONS`)
14. [Manage Costing Lookups](manage-costing-lookups/SKILL.md) (`ORA_CST_COSTING_LOOKUPS`)
15. [Manage Costing Key Flexfields](manage-costing-key-flexfields/SKILL.md) (`CST_MANAGE_COSTING_KEY_FLEXFIELDS`)
16. [Overhead Cost Element Groups](overhead-cost-element-groups/SKILL.md) (`ORA_CST_OVERHEAD_COST_ELEMENT_GROUPS`)
17. [Manage Costing Descriptive Flexfields](manage-costing-descriptive-flexfields/SKILL.md) (`CST_MANAGE_COSTING_DESCRIPTIVE_FLEXFIELDS`)

## Inputs

- `implementation_objective`
- `project_context`
- `cost_accounting_scope`
- `cost_accounting_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
