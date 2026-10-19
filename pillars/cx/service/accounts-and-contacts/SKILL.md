---
skill_id: "cx.service.accounts-and-contacts"
name: "Accounts and Contacts Implementation Guidance"
description: "Provides CX Service implementation guidance for the Accounts and Contacts functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Accounts and Contacts"
functional_area_code: "ORA_SVC_ACCOUNTS_AND_CONTACTS"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "accounts_and_contacts_scope"
  - "accounts_and_contacts_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/accounts-and-contacts/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/accounts-and-contacts/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/accounts-and-contacts/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_SVC_MANAGE_ACCT_IND_CLASS"
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

# Accounts and Contacts Implementation Guidance

## Purpose

Provides the CX Service overlay for the Accounts and Contacts functional area.

## When to Use

Use this functional-area skill after Service scope is confirmed. Reuse the CX Sales baseline for shared Accounts and Contacts use cases; retain local guidance only for documented Service-specific differences.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Service` (`ORA_SVC`)
- Functional area / Setup Object: `Accounts and Contacts` (`ORA_SVC_ACCOUNTS_AND_CONTACTS`)

## Setup Tasks

1. [Manage Account Industry Classification Profile Values](manage-account-industry-classification-profile-values/SKILL.md) (`ORA_SVC_MANAGE_ACCT_IND_CLASS`)

## Inputs

- `implementation_objective`
- `project_context`
- `accounts_and_contacts_scope`
- `accounts_and_contacts_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the [CX Sales Accounts and Contacts baseline](../../sales/accounts-and-contacts/SKILL.md) and its task-local `ora-resource/` guidance for the reused use cases. This folder deliberately retains only the CX Service-specific profile-value task and its resources; do not copy Sales task skills or resources here unless a documented Service-specific override is required. Track token usage for any generated project artifact or skill-run record using the manifest policy.
