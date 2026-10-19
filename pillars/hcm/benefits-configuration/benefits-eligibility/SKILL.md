---
skill_id: "hcm.benefits-configuration.benefits-eligibility"
name: "Benefits Eligibility"
description: "Routes Benefits Eligibility requests to the implemented Eligibility Profiles setup workflow."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Eligibility"
functional_area_code: "ORA_BENEFITS_ELIGIBILITY"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Benefits Configuration pillar team"
version: "0.2.1"
inputs: ["implementation_objective", "eligibility_profile_requirements"]
outputs: ["eligibility_profile_result"]
depends_on: []
uses_core: []
persists_project_state: false
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact accounting is available"
  required_fields: ["activity_start_time", "skill_id", "task", "trigger", "artifacts_written", "files_read", "estimated_input_tokens", "estimated_output_tokens", "estimated_total_tokens", "estimation_method", "notes"]
side_effects: []
required_privileges: []
required_setup_tasks:
  - "BEN_MANAGE_ELIGIBILITY_PROFILES"
---

# Benefits Eligibility

## Purpose

Route Benefits eligibility-profile creation and evaluation requests to the supported setup task.

## Routing

For requests to create or evaluate eligibility profiles, invoke
[Eligibility Profiles](eligibility-profiles/SKILL.md) explicitly. The task skill
owns requirement collection, preview and approval, import execution, and result
validation.

## Setup Tasks

1. [Eligibility Profiles](eligibility-profiles/SKILL.md) (`BEN_MANAGE_ELIGIBILITY_PROFILES`)
