---
skill_id: "shared.implementation-planning.fsm-set-optin.fsm-set-optin-functional-areas"
name: "FSM Set Optin Functional Areas"
description: "Sets Oracle Fusion FSM Redwood opt-in status for a functional area, resolving FunctionalAreaCode and parent offering context when needed and delegating execution to the shared FSM Set Optin engine."
layer: "shared"
pillar: "Common"
type: "planning"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "functional_area_identifier"
  - "offering_identifier"
  - "action"
  - "execution_options"
outputs:
  - "set_optin_result"
  - "standard_report"
  - "diagnostics"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.fsm-set-optin.fsm-set-optin"
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
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
persists_project_state: true
state_updates:
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/shared/implementation-planning/fsm-set-optin/functional-area/<functional-area-name>/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to a Fusion environment when approved."
  - "May PATCH Fusion Common feature selections when not run with --dry-run."
  - "Refreshes setup feature selections after successful writes."
required_privileges:
  - "Fusion privileges appropriate to update functional-area opt-in selections and refresh setup feature selections"
---

# FSM Set Optin Functional Areas

## Purpose

Sets FSM Redwood opt-in status for one functional area. This wrapper validates
functional-area inputs and optional parent offering context, then delegates
lookup, choice selection, PATCH, refresh, report rendering, and token logging to
`shared.implementation-planning.fsm-set-optin.fsm-set-optin`.

## REST Flow

1. Authenticate with `core.auth.fusion-oauth-authentication` when token refresh
   is needed.
2. Resolve `FunctionalAreaCode` and parent offering context when supplied or
   required by shared hierarchy.
3. Discover valid choices through BOSS.
4. Apply disable safety checks for locked children and shared auto-enabled
   parent offerings.
5. PATCH Fusion Common unless `--dry-run` is supplied.
6. Refresh setup feature selections and write reports.

## Project Scripts

Run from the repository root:

```bash
python3 shared/implementation-planning/fsm-set-optin/fsm-set-optin-functional-areas/scripts/set_optin_functional_area.py \
  --functional-area-name "Resources" \
  --offering-name "Financials" \
  --action opt-in \
  --token-cache auto \
  --boss-token-cache auto \
  --fusion-common-token-cache auto
```

The script derives the FSCR project workspace from the `environment` value in
`core/auth/fusionEnv.properties`; pass `--project-id` when the project
workspace cannot be resolved from `FDOS_PROJECT_ID`, the existing initialized
workspace, or the Fusion `environment` fallback.

Use `--dry-run` to resolve and build the request plan without writing.

## Implementation Notes

Keep the Python entrypoint aligned with setup-export and setup-compare drivers:
local repository bootstrap, `fusion_auth` through the shared engine, `utc_now`,
`parse_args`, `resolve_scope_feature_code`, `resolve_project_id`,
`run_set_optin`, and `main`. Keep `--project-id` pass-through aligned with the
shared `fsm-set-optin` engine.
