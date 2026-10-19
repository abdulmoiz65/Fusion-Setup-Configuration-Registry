---
skill_id: "erp.risk-and-security.add-other-data-sources"
name: "Add Other Data Sources Implementation Guidance"
description: "Provides ERP Risk and Security implementation guidance for the Add Other Data Sources functional area."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Add Other Data Sources"
functional_area_code: "ORA_GTG_ADD_OTHER_DATA_SOURCES"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP risk and security pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "add_other_data_sources_scope"
  - "add_other_data_sources_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/add-other-data-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/add-other-data-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/add-other-data-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_GTG_ADD_EPM_DATA_SOURCES"
  - "ORA_GTG_ADD_OTHER_DATA_SOURCES"
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

# Add Other Data Sources Implementation Guidance

## Purpose

Provides ERP Risk and Security implementation guidance for the Add Other Data Sources functional area.

## When to Use

Use this functional-area skill after Risk and Security scope is confirmed and the project needs add other data sources setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Risk and Security` (`ORA_RISK_AND_CONTROLS`)
- Functional area / Setup Object: `Add Other Data Sources` (`ORA_GTG_ADD_OTHER_DATA_SOURCES`)

## Setup Tasks

1. [Add EPM Data sources](add-epm-data-sources/SKILL.md) (`ORA_GTG_ADD_EPM_DATA_SOURCES`)
2. [Add Other Data sources](add-other-data-sources/SKILL.md) (`ORA_GTG_ADD_OTHER_DATA_SOURCES`)

## Business Object Mapping

| Setup task | Data Loader import mode | Business object | Verification status |
| --- | --- | --- | --- |
| `Add EPM Data sources` (`ORA_GTG_ADD_EPM_DATA_SOURCES`) | `REST` | `Data Sources` | Developer-supplied; verify that it is registered in the target Fusion environment before generating a sample or preparing data. |
| `Add Other Data sources` (`ORA_GTG_ADD_OTHER_DATA_SOURCES`) | `REST` | `Risk Cloud connector-definition REST endpoint` | Developer-supplied; verify the endpoint and payload contract before preparing or posting data. |

The catalog does not mark this task as CSV export/import supported. Use the
declared Risk Cloud REST POST workflow for this task and keep its payload and
approval artifacts separate from Data Loader workflows. The BOSS OAuth scope
is separate from Data Loader's standard OAuth scope.

## Inputs

- `implementation_objective`
- `project_context`
- `add_other_data_sources_scope`
- `add_other_data_sources_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
