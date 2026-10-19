---
skill_id: "erp.financials.financial-reporting-structures"
name: "Financial Reporting Structures Implementation Guidance"
description: "Provides ERP Financials implementation guidance for the Financial Reporting Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Financial Reporting Structures"
functional_area_code: "ORA_ASK_FIN_REPORTING_STRUCT"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "financial_reporting_structures_scope"
  - "financial_reporting_structures_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "GL_MANAGE_ACCOUNTING_CALENDARS"
  - "GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SETS"
  - "GL_MANAGE_CHARTS_OF_ACCOUNTS"
  - "GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES"
  - "GL_MANAGE_CHART_OF_ACCOUNTS_MAPPING"
  - "GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SET_VALUES"
  - "GL_MANAGE_ACCOUNT_COMBINATIONS"
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

# Financial Reporting Structures Implementation Guidance

## Purpose

Provides ERP Financials implementation guidance for the Financial Reporting Structures functional area.

## When to Use

Use this functional-area skill after Financials scope is confirmed and the project needs financial reporting structures setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Financials` (`XLE_FINANCIALS_JUR`)
- Functional area / Setup Object: `Financial Reporting Structures` (`ORA_ASK_FIN_REPORTING_STRUCT`)

## Required Setup Tasks

For an approved chart-of-accounts structure, sequence the following tasks:

1. [Manage Chart of Accounts Value Sets](manage-chart-of-accounts-value-sets/SKILL.md) (`GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SETS`)
2. [Manage Chart of Accounts Structures](manage-chart-of-accounts-structures/SKILL.md) (`GL_MANAGE_CHARTS_OF_ACCOUNTS`)
3. [Manage Chart of Accounts Structure Instances](manage-chart-of-accounts-structure-instances/SKILL.md) (`GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES`)

## Conditional Setup Tasks

Use the following tasks only when their stated scope is explicitly requested.
They are not baseline prerequisites for creating a chart-of-accounts structure.

When both `GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES` and
`GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SET_VALUES` are selected in an end-to-end
plan, schedule Value Set Values after Structure Instances. This preserves the
established structure-instance context used to prove whether a value set is
assigned to the Natural Account segment. A standalone Value Set Values request
is permitted for isolated task testing or targeted maintenance after its target
value set is resolved.

1. [Manage Accounting Calendars](manage-accounting-calendars/SKILL.md) (`GL_MANAGE_ACCOUNTING_CALENDARS`) — ledger-calendar design.
2. [Manage Chart of Accounts Value Set Values](manage-chart-of-accounts-value-set-values/SKILL.md) (`GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SET_VALUES`) — explicit segment-value creation or update through the approved FBDI Data Loader route. Do not route a COA-creation request here merely because the structure references value sets.
3. [Manage Chart of Accounts Mappings](manage-chart-of-accounts-mappings/SKILL.md) (`GL_MANAGE_CHART_OF_ACCOUNTS_MAPPING`) — mapping between approved distinct source and target charts, such as a balance-level secondary ledger or cross-ledger transfer.

## Accounting Calendar Guidance

Use the Manage Accounting Calendars task skill to design, validate, export, or import accounting calendar setup. It supports standard calendar patterns and adjustment-period guidance where supported by Fusion setup CSV import.

## Setup Tasks

1. [Manage Accounting Calendars](manage-accounting-calendars/SKILL.md) (`GL_MANAGE_ACCOUNTING_CALENDARS`)
2. [Manage Chart of Accounts Value Sets](manage-chart-of-accounts-value-sets/SKILL.md) (`GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SETS`)
3. [Manage Chart of Accounts Structures](manage-chart-of-accounts-structures/SKILL.md) (`GL_MANAGE_CHARTS_OF_ACCOUNTS`)
4. [Manage Chart of Accounts Structure Instances](manage-chart-of-accounts-structure-instances/SKILL.md) (`GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES`)
5. [Manage Chart of Accounts Mappings](manage-chart-of-accounts-mappings/SKILL.md) (`GL_MANAGE_CHART_OF_ACCOUNTS_MAPPING`)
6. [Manage Chart of Accounts Value Set Values](manage-chart-of-accounts-value-set-values/SKILL.md) (`GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SET_VALUES`)
7. [Manage Account Combinations](manage-account-combinations/SKILL.md) (`GL_MANAGE_ACCOUNT_COMBINATIONS`)

## Inputs

- `implementation_objective`
- `project_context`
- `financial_reporting_structures_scope`
- `financial_reporting_structures_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

For a vague request such as "create a chart of accounts", propose only the Fusion baseline segments — Company, Cost Center, Account, and Intercompany — and require the user to confirm or revise that set, identify the COA, and provide any additional segments. Do not infer additional segments, segment values, hierarchies, mappings, or a ledger calendar. Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
