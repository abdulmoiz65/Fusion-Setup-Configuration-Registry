---
skill_id: "hcm.benefits-configuration.benefits-program-and-plan-hierarchy"
name: "Benefits Program and Plan Hierarchy"
description: "Routes supported Benefits plan creation requests to the plan-only workflow under the catalog's Benefit Programs task. Benefits program creation is not implemented."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Program and Plan Hierarchy"
functional_area_code: "ORA_BENEFITS_PROGRAM_AND_PLAN_HIERARCHY"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Benefits Configuration pillar team"
version: "0.3.1"
inputs: ["implementation_objective", "benefit_plan_requirements"]
outputs: ["benefit_plan_import_result"]
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
  - "BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS"
---

# Benefits Program and Plan Hierarchy

## Purpose

Route supported Benefits plan creation requests to the Benefit Programs setup task.

## Routing

For requests to create a supported benefits plan, invoke
[Benefit Programs](benefit-programs/SKILL.md) explicitly. The task skill owns
template selection, preview and approval, import execution, and result
validation.

The task name follows the Fusion catalog. Program creation is unsupported;
do not interpret a request to create a Benefits program as a request to import
a plan package.

## Setup Tasks

1. [Benefit Programs](benefit-programs/SKILL.md) (`BEN_MANAGE_BENEFIT_PROGRAMS_DETAILS`)
