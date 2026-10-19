---
skill_id: "erp.public-sector-business-licenses"
name: "Public Sector Business Licenses"
description: "Coordinates ERP Public Sector Business Licenses implementation guidance and routes work to developer-created functional-area skills."
layer: "pillar"
pillar: "ERP"
offering: "Public Sector Business Licenses"
type: "orchestration"
execution_mode: "assisted"
owner_team: "ERP Public Sector Business Licenses pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "erp_scope"
  - "public_sector_business_licenses_requirements"
outputs:
  - "public_sector_business_licenses_scope"
  - "functional_area_skill_plan"
  - "public_sector_business_licenses_work_products"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.artifact-version-manager"
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
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/erp/public-sector-business-licenses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/erp/public-sector-business-licenses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/public-sector-business-licenses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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

# Public Sector Business Licenses

## Purpose

Coordinates ERP Public Sector Business Licenses implementation guidance across functional areas, setup tasks, and standard implementation activities.

## When to Use

Use this offering-level skill after Public Sector Business Licenses is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `ERP`
- Pillar slug: `erp`
- Offering code: `ORA_PSCR_OFR_BUSINESS_LICENSES`
- Offering slug: `public-sector-business-licenses`
- Offering folder: `pillars/erp/public-sector-business-licenses`
- Offering mapping source: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

This skill routes control to functional-area skills created by developers under this folder. Developers should create functional-area skills with `core.fusion-dev.pillar-skill-gen` using the catalog-backed path pattern:

```text
pillars/erp/public-sector-business-licenses/{functional-area-slug}/
```

When a requested functional area is not yet present under this offering, use the setup catalog below to identify the matching functional area and invoke `core.fusion-dev.pillar-skill-gen` to generate the child skill before adding functional-area-specific guidance.

## Inputs

- `implementation_objective`
- `project_context`
- `erp_scope`
- `public_sector_business_licenses_requirements`

## Outputs

- `public_sector_business_licenses_scope`
- `functional_area_skill_plan`
- `public_sector_business_licenses_work_products`
- `token_usage_record`

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_PSCR_OFR_BUSINESS_LICENSES`
Functional area count: `15`
Setup task count: `206`

- `ORA_PSC_FA_INITIAL_SET_UP`: Initial Set Up
- `ORA_PSC_FA_AGENCY_PROFILE`: Agency Profile
- `ORA_PSC_FA_FEES_PAYMENTS`: Fees and Payments
- `ORA_PSC_FA_BL_INSPECTION`: Business License Inspections
- `ORA_PSC_FA_REFERENCE_ENTITIES`: Reference Entities
- `ORA_PSC_FA_BUS_LICENSE_TYPES`: Business License Types
- `ORA_PSC_FA_ACCOUNTING`: Accounting
- `ORA_PSC_FA_AGENCY_STAFF`: Agency Staff
- `ORA_PSC_FA_PUBLIC_USERS`: Public Users
- `ORA_PSC_FA_ANALYTICS`: Analytics and Reporting
- `ORA_PSC_FA_HELP`: Help Management
- `ORA_PSC_FA_GIS`: GIS
- `ORA_PSC_FA_SYSADMIN`: System Administration
- `ORA_PSC_FA_BRANDING`: Branding
- `ORA_ASK_APPLICATION_EXTENSIONS`: Application Extensions

## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
