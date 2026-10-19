---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows"
name: "Supply Chain Financial Flows Implementation Guidance"
description: "Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Supply Chain Financial Flows functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Financial Flows"
functional_area_code: "ORA_FOS_SUPPLY_CHAIN_FIN_FLOW"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "supply_chain_financial_flows_scope"
  - "supply_chain_financial_flows_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_FOS_DEFINE_TRADE_AND_ACCOUNTING_RULES_NEW"
  - "ORA_FOS_DEFINE_TRANSFER_PRICING_RULES_NEW"
  - "ORA_PROFIT_CENTER_PARTY_RELATIONSHIPS_NEW"
  - "ORA_FOS_MANAGE_SYSTEM_OPTIONS_NEW"
  - "ORA_FOS_MANAGE_TRADE_QUALIFIER_NEW"
  - "ORA_FOS_MANAGE_SUPPLY_CHAIN_FINANCIAL_TRADE_AGREEMENTS_NEW"
  - "ORA_FOS_MANAGE_LOOKUPS"
  - "ORA_FOS_MANAGE_DFF"
  - "ORA_FOS_MANAGE_DROP_SHIP_AGREEMENTS"
  - "ORA_FOS_REGISTER_PRICING_STUB"
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

# Supply Chain Financial Flows Implementation Guidance

## Purpose

Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Supply Chain Financial Flows functional area.

## When to Use

Use this functional-area skill after Manufacturing and Supply Chain Materials Management scope is confirmed and the project needs supply chain financial flows setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Manufacturing and Supply Chain Materials Management` (`ORA_MANUFACTURING_AND_SUPPLY_C`)
- Functional area / Setup Object: `Supply Chain Financial Flows` (`ORA_FOS_SUPPLY_CHAIN_FIN_FLOW`)

## Setup Tasks

1. [Documentation and Accounting Rules](documentation-and-accounting-rules/SKILL.md) (`ORA_FOS_DEFINE_TRADE_AND_ACCOUNTING_RULES_NEW`)
2. [Transfer Pricing Rules](transfer-pricing-rules/SKILL.md) (`ORA_FOS_DEFINE_TRANSFER_PRICING_RULES_NEW`)
3. [Profit Center Party Relationships](profit-center-party-relationships/SKILL.md) (`ORA_PROFIT_CENTER_PARTY_RELATIONSHIPS_NEW`)
4. [Financial Orchestration System Options](financial-orchestration-system-options/SKILL.md) (`ORA_FOS_MANAGE_SYSTEM_OPTIONS_NEW`)
5. [Financial Qualifiers](financial-qualifiers/SKILL.md) (`ORA_FOS_MANAGE_TRADE_QUALIFIER_NEW`)
6. [Financial Orchestration Lookups](manage-supply-chain-financial-orchestration-lookups/SKILL.md) (`ORA_FOS_MANAGE_LOOKUPS`)
7. [Financial Orchestration Descriptive Flexfields](manage-supply-chain-financial-orchestration-descriptive-flexfields/SKILL.md) (`ORA_FOS_MANAGE_DFF`)
8. [Manage Drop Ship Financial Flows](manage-drop-ship-financial-flows/SKILL.md) (`ORA_FOS_MANAGE_DROP_SHIP_AGREEMENTS`)
9. [Register Financial Orchestration Third-Party Transfer Pricing Service](register-financial-orchestration-third-party-transfer-pricing-service/SKILL.md) (`ORA_FOS_REGISTER_PRICING_STUB`)
10. [Financial Orchestration Flows](financial-orchestration-flows/SKILL.md) (`ORA_FOS_MANAGE_SUPPLY_CHAIN_FINANCIAL_TRADE_AGREEMENTS_NEW`)

## Inputs

- `implementation_objective`
- `project_context`
- `supply_chain_financial_flows_scope`
- `supply_chain_financial_flows_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
