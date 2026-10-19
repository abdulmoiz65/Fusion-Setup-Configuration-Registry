---
skill_id: "shared.implementation-planning.fsm-set-optin.fsm-set-optin"
name: "FSM Set Optin"
description: "Shared implementation engine for setting Oracle Fusion FSM Redwood opt-in status for offerings, functional areas, and features using FSCR OAuth, BOSS lookups, Fusion Common PATCH, and ADF refresh APIs."
layer: "shared"
pillar: "Common"
type: "planning"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.1"
inputs:
  - "fusion_environment_context"
  - "set_optin_scope"
  - "target_identifier"
  - "action"
  - "execution_options"
outputs:
  - "set_optin_result"
  - "standard_report"
  - "diagnostics"
  - "token_usage_record"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.fsm-rest-client"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/shared/implementation-planning/fsm-set-optin/{target_type}/{target}/"
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
  - "Uses BOSS and Fusion REST read APIs to resolve setup targets and choices."
  - "May PATCH Fusion Common feature selections when not run with --dry-run."
  - "Refreshes setup feature selections after successful writes."
  - "Writes sanitized reports and process output to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to read BOSS setup feature metadata, update Fusion Common feature selections, and refresh setup feature selections"
---

# FSM Set Optin

Use this shared engine for low-level Oracle Fusion FSM Redwood opt-in changes.
Prefer the entity-specific user-facing skills for normal work:

- `shared.implementation-planning.fsm-set-optin.fsm-set-optin-offerings`
- `shared.implementation-planning.fsm-set-optin.fsm-set-optin-functional-areas`
- `shared.implementation-planning.fsm-set-optin.fsm-set-optin-features`

## Required Reference

Read `references/optin-api.md` before changing endpoints, payload fields,
authentication scopes, or safety behavior.

## Engine Boundary

This engine owns:

1. Reading Fusion environment configuration from
   `core/auth/fusionEnv.properties`.
2. Obtaining standard Fusion REST, BOSS, and Fusion Common OAuth tokens through
   `core.auth.fusion-oauth-authentication`.
3. Resolving names to short names/codes with the setup export-style
   `/features` lookup, then hydrating through BOSS.
4. Discovering `featureSelectedChoices`.
5. Applying disable safety checks.
6. Building and optionally executing Fusion Common PATCH payloads.
7. Calling `setupProcesses/action/refreshFeatureSelections`.
8. Writing sanitized process output, a standard report, and token usage records.

Entity skills own target-specific input rules and defaults. They must call this
engine instead of duplicating lookup, choice selection, PATCH, refresh, report,
or token logging behavior.

## Project Assumptions

- Run scripts from the repository root.
- Use FSCR OAuth token caches:
  - `.fusionaim_token.json` for standard Fusion REST.
  - `.fusionaim_boss_token.json` for BOSS.
  - `.fusionaim_fusion_common_token.json` for Fusion Common feature writes.
- Use `--project-id` for explicit workspace selection when provided. Otherwise
  use `FDOS_PROJECT_ID`, then the only initialized `project/{project_id}`
  workspace, with the Fusion `environment` value as a compatibility fallback.
- Store outputs under:

```text
project/{project_id}/artifacts/shared/implementation-planning/fsm-set-optin/<target-type>/<target>/
```

- Do not print access tokens, refresh tokens, client secrets, token cache
  contents, Authorization headers, cookies, passwords, or raw long responses.
- Network access to Fusion REST normally requires command approval/escalation.

## Raw Script

Use the raw engine only when the caller already knows the target type:

```bash
python3 shared/implementation-planning/fsm-set-optin/fsm-set-optin/scripts/fsm_set_optin.py \
  --target-type offering \
  --target PER_CORE \
  --action opt-in \
  --token-cache auto \
  --boss-token-cache auto \
  --fusion-common-token-cache auto
```

Use `--dry-run` to resolve and build the request plan without PATCH or refresh.

## Destination security

The approved service origin is the HTTPS origin of `restBaseUrl` in the trusted
environment profile. `--base-url` may select a host, UI URL, or REST root only
on that same origin; it cannot select another environment or configured service.
Validate before token acquisition, including dry runs and explicit-token runs.
Neither `--force` nor token refresh may bypass destination validation.

All Standard Fusion, BOSS, and Fusion Common requests use the strict core
`trusted_http.py` transport. It checks every destination and redirect hop;
cross-origin destinations and all automatic write redirects are rejected.
Validate BOSS pagination links after resolving them against the final response
URL. Destination failures are non-retryable input/transport validation failures,
not authentication failures. Never retry a PATCH/refresh after such a failure;
an earlier approved-origin write may already have succeeded.

Read [destination-security.md](references/destination-security.md) when changing
URL handling, invoking the Python engine directly, or retesting H13 / CS3.

## Final Response

For completed set opt-in runs, include:

- Environment host.
- Target type, target name, and resolved short name.
- Action and selected choices.
- PATCH status and refresh status.
- Refresh offering IDs.
- Standard report path and sanitized process output path.
- Any warnings or follow-up needed.
