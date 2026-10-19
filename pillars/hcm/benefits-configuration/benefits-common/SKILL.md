---
skill_id: "hcm.benefits-configuration.benefits-common"
name: "Benefits Common"
description: "Placeholder for Benefits Common guidance within Benefits Configuration; implementation is not yet available."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Common"
functional_area_code: "ORA_BENEFITS_COMMON"
type: "advisory"
execution_mode: "advisory"
owner_team: "HCM Benefits Configuration pillar team"
version: "0.1.1"
inputs: ["implementation_objective"]
outputs: ["implementation_gap"]
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
---

# Benefits Common

## Status

Placeholder only. This page reserves the catalog-backed Benefits Common
functional area (`ORA_BENEFITS_COMMON`) within Benefits Configuration; it does
not provide a supported setup or execution workflow.

## Handling Requests

Explain that Benefits Common implementation guidance is not yet available.
Record the requested capability as an implementation gap and refer it to the
HCM Benefits Configuration pillar team. Do not infer task codes, business-object
mappings, API endpoints, or load instructions from this placeholder.

No database access, uploads, imports, or Fusion configuration changes are
performed by this placeholder.
