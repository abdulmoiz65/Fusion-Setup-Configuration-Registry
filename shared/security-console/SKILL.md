---
skill_id: "shared.security-console"
name: "Security Console Legacy Redirect"
description: "Compatibility entry point that redirects legacy shared Security Console requests to the Common-pillar Security Console skill."
layer: "shared"
pillar: "Common"
type: "orchestration"
execution_mode: "assisted"
owner_team: "FSCR Security team"
version: "1.0.0"
inputs:
  - "implementation_objective"
  - "project_id"
  - "target_environment"
  - "requested_operation"
outputs:
  - "redirected_skill_id"
  - "security-console-skill-routing-plan"
depends_on:
  - "common.security-console"
uses_core: []
persists_project_state: false
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

# Security Console Legacy Redirect

This is a compatibility entry point only. Immediately route every invocation
to `common.security-console` at
`pillars/common/security-console/SKILL.md`; do not perform any Security Console
workflow from this shared path.

When a pillar, agent, or user selects this legacy path, tell them: **“This
shared Security Console path is deprecated. Please use
`common.security-console` from `pillars/common/security-console/SKILL.md`.”**
Do not treat the legacy path as an executable route.
