---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-orchestration"
name: "Supply Chain Orchestration Implementation Guidance"
description: "Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Supply Chain Orchestration functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Orchestration"
functional_area_code: "ORA_DOS_SUPPLY_CHAIN_ORCH"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "supply_chain_orchestration_scope"
  - "supply_chain_orchestration_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.common.manual-tasks"
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-orchestration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-orchestration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-orchestration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_DOS_MANAGE_SUPPLY_ORCHESTRATION_LOOKUPS"
  - "ORA_DOS_MANAGE_SUPPLY_ORDER_DEFAULTING_AND_ENRICHMENT_RULES"
  - "ORA_DOS_MANAGE_SUPPLY_EXECUTION_DOCUMENT_CREATION_RULES"
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

# Supply Chain Orchestration Implementation Guidance

## Purpose

Provides SCM Manufacturing and Supply Chain Materials Management implementation guidance for the Supply Chain Orchestration functional area.

## When to Use

Use this functional-area skill after Manufacturing and Supply Chain Materials Management scope is confirmed and the project needs supply chain orchestration setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Manufacturing and Supply Chain Materials Management` (`ORA_MANUFACTURING_AND_SUPPLY_C`)
- Functional area / Setup Object: `Supply Chain Orchestration` (`ORA_DOS_SUPPLY_CHAIN_ORCH`)

## Setup Tasks

1. [Manage Supply Orchestration Lookups](manage-supply-orchestration-lookups.md) (`ORA_DOS_MANAGE_SUPPLY_ORCHESTRATION_LOOKUPS`)
2. [Manage Supply Order Defaulting and Enrichment Rules](manage-supply-order-defaulting-and-enrichment-rules.md) (`ORA_DOS_MANAGE_SUPPLY_ORDER_DEFAULTING_AND_ENRICHMENT_RULES`)
3. [Manage Supply Execution Document Creation Rules](manage-supply-execution-document-creation-rules.md) (`ORA_DOS_MANAGE_SUPPLY_EXECUTION_DOCUMENT_CREATION_RULES`)

## Inputs

- `implementation_objective`
- `project_context`
- `supply_chain_orchestration_scope`
- `supply_chain_orchestration_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the flat setup-task file linked above for the approved lookup types, System versus User Extensible category restrictions, and routing to `core.fusion-api.apps-common`. The core workflow resolves each lookup's view; do not assume one view for the full task scope. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For Manage Supply Order Defaulting and Enrichment Rules and Manage Supply Execution Document Creation Rules, use the respective flat task file and `shared.common.manual-tasks`. These two tasks provide manual-only guidance; generated import-mode metadata does not authorize API, import, automated configuration, or browser execution. Keep task-specific steps and validation guidance in those files, and stop at their documented missing-detail checks.
