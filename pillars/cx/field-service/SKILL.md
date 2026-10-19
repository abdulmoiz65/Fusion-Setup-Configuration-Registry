---
skill_id: "cx.field-service"
name: "Field Service"
description: "Coordinates CX implementation guidance for the Field Service offering."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "CX Field Service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "field_service_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/current/"
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

# Field Service

## Purpose

Coordinates implementation work for offering `Field Service` (`ORA_FIELD_SERVICE`) under the `CX` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_FIELD_SERVICE`
Functional area count: `4`
Setup task count: `32`

- `ORA_SVC_COMPANY_PROFILE`: Company Profile
- `ORA_ASK_USERS_AND_SECURITY`: Users and Security
- `ORA_FFS_FA_MOBILE_EXPERIENCE`: Mobile Experience
- `ORA_FFS_FA_SCHEDULING_AND_DISPATCH`: Scheduling and Dispatch
