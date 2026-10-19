---
skill_id: "hcm.talent-review-setup"
name: "Talent Review Setup"
description: "Coordinates HCM implementation guidance for the Talent Review Setup offering."
layer: "pillar"
pillar: "HCM"
offering: "Talent Review Setup"
offering_code: "ORA_TALENT_REVIEW_SETUP"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Talent Review Setup pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "talent_review_setup_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/talent-review-setup/current/"
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

# Talent Review Setup

## Purpose

Coordinates implementation work for offering `Talent Review Setup` (`ORA_TALENT_REVIEW_SETUP`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_TALENT_REVIEW_SETUP`
Functional area count: `6`
Setup task count: `23`

- `ORA_TALENT_REVIEW_COMMON`: Talent Review Common
- `ORA_TALENT_REVIEW_HCM_TOOL`: Talent Review HCM Tool
- `ORA_TALENT_REVIEW_DEPARTMENTS`: Talent Review Departments
- `ORA_TALENT_REVIEW_JOBS`: Talent Review Jobs
- `ORA_TALENT_REVIEW_POTENTIAL_ASSESSMENT`: Talent Review Potential Assessment
- `ORA_TALENT_REVIEW_TALENT_REVIEW_TEMPLATE`: Talent Review Talent Review Template
