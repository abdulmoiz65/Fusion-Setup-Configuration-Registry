---
skill_id: "cx.sales"
name: "Sales"
description: "Coordinates CX Sales implementation guidance and routes work to functional-area skills. Use for Sales offering scope and routing, including Sales Lead qualification templates, current or configured Sales Lead profile-option values, Sales Lead standard lookups, and questions about the Sales Orchestration functional area or its Sales Motions, Sales Plays and Content, Data Capture Rules, and Sales Orchestration Pre-requisites tasks. Route Leads requests to the Leads functional-area skill and delegate Sales Orchestration requests to the Sales Orchestration functional-area skill."
layer: "pillar"
pillar: "CX"
offering: "Sales"
type: "orchestration"
execution_mode: "assisted"
owner_team: "CX Sales pillar team"
version: "0.3.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "cx_scope"
  - "sales_requirements"
outputs:
  - "sales_scope"
  - "functional_area_skill_plan"
  - "sales_work_products"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/current/"
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

# Sales

## Purpose

Coordinates CX Sales implementation guidance across functional areas, setup tasks, and standard implementation activities.

## When to Use

Use this offering-level skill after Sales is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `CX`
- Pillar slug: `cx`
- Offering code: `ORA_MIDSIZE_SALES`
- Offering slug: `sales`
- Offering folder: `pillars/cx/sales`
- Offering mapping source: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

This skill routes control to functional-area skills created by developers under this folder. Developers should create functional-area skills with `core.fusion-dev.pillar-skill-gen` using the catalog-backed path pattern:

```text
pillars/cx/sales/{functional-area-slug}/
```

Route any question or implementation request about Sales Orchestration, Sales
Motions, Sales Plays and Content, Data Capture Rules, or Sales Orchestration
Pre-requisites to [Sales Orchestration](sales-orchestration/SKILL.md). Let that
functional-area skill classify the request and route task-specific questions to
its nested skills; do not duplicate or bypass its task-routing rules here.

Route any question or implementation request about Sales Leads, Lead
qualification templates, Sales Lead profile options or their current/configured
values, or Sales Lead standard lookups to [Leads](leads/SKILL.md). Treat phrases
such as "list all Sales Lead profile options and their values", "current
value", "configured value", and an exact Sales Lead profile-option code as
task-routing signals, not as documentation-only questions. Let the Leads skill
select the nested setup-task skill and complete its environment workflow before
returning an environment-specific answer.

Route any question or implementation request about Sales Foundation, Activity
profile options, Activity standard lookups, Activity types or subtypes, Sales
note types, or Sales note type mappings to
[Sales Foundation](sales-foundation/SKILL.md). Let that functional-area skill
select the nested setup-task skill and apply its task-specific execution route;
do not duplicate or bypass its task-routing rules here.

When a requested functional area is not yet present under this offering, use the setup catalog below to identify the matching functional area and invoke `core.fusion-dev.pillar-skill-gen` to generate the child skill before adding functional-area-specific guidance.

## Inputs

- `implementation_objective`
- `project_context`
- `cx_scope`
- `sales_requirements`

## Outputs

- `sales_scope`
- `functional_area_skill_plan`
- `sales_work_products`
- `token_usage_record`

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_MIDSIZE_SALES`
Functional area count: `21`
Setup task count: `365`

- `ORA_SVC_COMPANY_PROFILE`: Company Profile
- `ORA_ASK_USERS_AND_SECURITY`: Users and Security
- `ORA_ZBS_SALES_FOUNDATION`: Sales Foundation
- `ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS`: Sales Catalog and Products
- `ORA_SVC_ACCOUNTS_AND_CONTACTS`: Accounts and Contacts
- `ORA_MKT_CONFIGURE_SALES_CAMPAIGNS`: Sales Campaigns
- `ORA_LDS_LEADS`: Leads
- `ORA_MOO_OPPORTUNITIES`: Opportunities
- `ORA_TRT_TERRITORIES`: Territories
- `ZBS_FORECAST_DEPLOYED`: Sales Forecasting
- `ZBS_QUOTAS_DEPLOYED`: Quotas
- `ORA_ZCA_SALES_BUSINESS_PLAN`: Business Plans
- `ORA_ZPM_MANAGE_PARTNERS`: Partner Relationship Management
- `ORA_OKC_SALES_CONTRACTS`: Sales Contracts
- `ORA_OSS_SUBSCRIPTIONS`: Subscriptions
- `ORA_CN_INCENTIVES`: Incentives
- `ORA_ZCA_SALES_ADAPTIVE_INTELLIGENCE`: Intelligence in Sales
- `ORA_ZCA_INTEGRATIONS`: Integrations
- `ORA_ASK_APPLICATION_EXTENSIONS`: Application Extensions
- `ORA_DATA_QUALITY_VERIFICATION_SERVICES`: Data Quality Verification Services
- `CUSTOM_SALES_ORCHESTRATION`: [Sales Orchestration](sales-orchestration/SKILL.md)

## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
