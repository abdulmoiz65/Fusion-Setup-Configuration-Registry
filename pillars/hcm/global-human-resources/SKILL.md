---
skill_id: "hcm.global-human-resources"
name: "Global Human Resources"
description: "Coordinates HCM implementation guidance for the Global Human Resources offering."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Global Human Resources pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "global_human_resources_requirements"
  - "requirement_documents"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/current/"
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

# Global Human Resources

## Purpose

Coordinates implementation work for offering `Global Human Resources` (`ORA_GLOBAL_HUMAN_RESOURCES`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_GLOBAL_HUMAN_RESOURCES`
Functional area count: `16`
Setup task count: `39`

- `ORA_GLOBAL_HUMAN_RESOURCES_COMMON`: Global Human Resources Common
- `ORA_ENTERPRISE`: Enterprise
- `ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`: Legal and Legislative Organizations
- `ORA_DOCUMENT_TYPES`: Document Types
- `ORA_EMPLOYMENT_ACTIONS_FRAMEWORK`: Employment Actions Framework
- `ORA_LOCATIONS`: Locations
- `ORA_PERSON_RECORD`: Person Record
- `ORA_COLLECTIVE_AGREEMENTS`: Collective Agreements
- `ORA_SUPPLEMENTARY_ORGANIZATIONS`: Supplementary Organizations
- `ORA_DEPARTMENTS`: Departments
- `ORA_GRADES`: Grades
- `ORA_JOBS`: Jobs
- `ORA_POSITIONS`: Positions
- `ORA_HCM_TREES`: HCM Trees
- `ORA_SENIORITY_DATES`: Seniority Dates
## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
- `CUSTOM_HCM_RESPONSIBILITIES`: HCM Responsibilities
