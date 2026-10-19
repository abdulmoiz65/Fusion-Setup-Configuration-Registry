---
skill_id: "cx.subscriptions"
name: "Subscriptions"
description: "Coordinates CX implementation guidance for the Subscriptions offering."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
offering_code: "CUSTOM_SUBSCRIPTIONS"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "CX Subscriptions pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "subscriptions_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/current/"
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

# Subscriptions

## Purpose

Coordinates implementation work for offering `Subscriptions` (`CUSTOM_SUBSCRIPTIONS`) under the `CX` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

Route `Manage Price Adjustment Variables`, `Track Price Adjustment Variables`, `Advanced Pricing Term Variables`, `Flexible Pricing Term Option`, and `Formula Driven Flexible Pricing Term Adjustments` to **Billing Setup > Manage Price Adjustment Variables** (`CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES`).

Route requests whose primary object is a **Subscription Profile** or
**Subscription Profiles** to **Foundation Setup > Manage Subscription Profiles**
(`CUSTOM_MANAGE_SUBSCRIPTION_PROFILES`). This includes profile queries,
lookups, lists, reviews, creation, updates, and import requests. Do not route
these requests to **Usage Rating Setup > Manage Balance Profiles**; Balance
Profiles are a separate object.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `CUSTOM_SUBSCRIPTIONS`
Functional area count: `8`
Setup task count: `37`

- `CUSTOM_FOUNDATION_SETUP`: Foundation Setup
- `CUSTOM_BILLING_SETUP`: Billing Setup
- `CUSTOM_USAGE_RATING_SETUP`: Usage Rating Setup
- `CUSTOM_RENEWAL_SETUP`: Renewal Setup
- `CUSTOM_COVERAGE_SETUP`: Coverage Setup
- `CUSTOM_INTEGRATION_SETUP`: Integration Setup
- `ORA_SVC_COMPANY_PROFILE`: Company Profile
- `ORA_ASK_USERS_AND_SECURITY`: Users and Security
