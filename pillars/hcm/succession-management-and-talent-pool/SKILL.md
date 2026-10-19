---
skill_id: "hcm.succession-management-and-talent-pool"
name: "Succession Management and Talent Pool"
description: "Coordinates HCM implementation guidance for the Succession Management and Talent Pool offering."
layer: "pillar"
pillar: "HCM"
offering: "Succession Management and Talent Pool"
offering_code: "ORA_SUCCESSION_MANAGEMENT"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Succession Management and Talent Pool pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "succession_management_and_talent_pool_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/succession-management-and-talent-pool/current/"
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

# Succession Management and Talent Pool

## Purpose

Coordinates implementation work for offering `Succession Management and Talent Pool` (`ORA_SUCCESSION_MANAGEMENT`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_SUCCESSION_MANAGEMENT`
Functional area count: `6`
Setup task count: `23`

- `ORA_SUCCESSION_MANAGEMENT_COMMON`: Succession Management and Talent Pool Common
- `ORA_SUCCESSION_MANAGEMENT_HCM_TOOL`: Succession Management and Talent Pool HCM Tool
- `ORA_SUCCESSION_MANAGEMENT_BUSINESS_UNIT`: Succession Management and Talent Pool Business Unit
- `ORA_SUCCESSION_MANAGEMENT_DEPARTMENTS`: Succession Management and Talent Pool Departments
- `ORA_SUCCESSION_MANAGEMENT_JOBS`: Succession Management and Talent Pool Jobs
- `ORA_SUCCESSION_MANAGEMENT_POSITIONS`: Succession Management and Talent Pool Positions
