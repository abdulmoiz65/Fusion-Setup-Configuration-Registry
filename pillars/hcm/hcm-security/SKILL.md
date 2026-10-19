---
skill_id: "hcm.hcm-security"
name: "HCM Security"
description: "Coordinates HCM implementation guidance for the HCM Security offering."
layer: "pillar"
pillar: "HCM"
offering: "HCM Security"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM HCM Security pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_security_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/current/"
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

# HCM Security

## Purpose

Coordinates implementation work for offering `HCM Security` (`ORA_HCM_SECURITY`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_HCM_SECURITY`
Functional area count: `4`
Setup task count: `20`

- `ORA_HCM_SECURITY_PROFILE`: HCM Security Profile
- `ORA_CONFIGURE_PUBLIC_WORKERS_FOR_ORACLE_SEARCH`: Configure Public Workers for Oracle Search
- `ORA_HCM_DATA_ROLE`: HCM Data Role
- `ORA_HCM_SECURITY_COMMON`: HCM Security Common
