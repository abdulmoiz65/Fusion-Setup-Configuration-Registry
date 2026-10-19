---
skill_id: "shared.baseline-assessment.topology-manager.environment-info"
name: "Topology Manager Environment Information API"
description: "Plans and executes read-only Topology Manager environment-information and version-detail retrieval."
layer: "shared"
pillar: "Common"
type: "assessment"
execution_mode: "assisted"
owner_team: "Topology Manager and shared enablement teams"
version: "0.3.1"
inputs:
  - "target_environment"
  - "requested_fields"
  - "execution_options"
outputs:
  - "validated_environment_information_request_plan"
  - "environment_information_summary"
  - "environment_version_details"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
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
persists_project_state: false
workspace_outputs: []
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Target environment release supporting the Topology Manager API"
side_effects:
  - "Read operations retrieve target-environment information."
  - "FDOS OAuth may refresh its local gitignored token cache."
required_privileges:
  - "Authenticated access to Topology Manager environment information and BOSS previous-release data"
---

# Topology Manager Environment Information API

## Purpose

Retrieve read-only environment information, current and last-shipped release
version details, and a derived upgrade status for one target environment. Load
the environment-information reference before forming a request.

## Help Intent

Treat requests for help, usage, capabilities, or example requests as
informational. Do not resolve an API operation or resource class. Do not
authenticate. Do not display a request preview. Do not call any API. Explain
that this skill retrieves read-only environment name, type, size, release,
break-glass, and upgrade-status information.

## Resource Reference

Load `references/evironment_info.md` before forming the Topology Manager or
BOSS request.

## Authentication

Use the shared FDOS OAuth authentication flow through
`core.auth.fusion-oauth-authentication` and execute both Topology Manager and
BOSS requests with `core.fusion-api.rest-api-client`. The shared flow owns
login, token-cache reuse, and refresh. For the Environment Information API,
select the Fusion Common service route; the REST client obtains and caches a
token using `fusion_common_scope`. This skill must not ask for a Fusion
password, construct Basic authentication, or accept a manually supplied token.

Preflight a non-empty `fusion_common_scope` in the selected properties. For a
separately requested login, run:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py --service fusion-common
```

It writes the external `~/.fusionaim/<profile-fingerprint>_token.json`, which the Fusion Common REST
route reuses. Report a missing scope or OAuth scope/grant rejection as a
configuration or auth/authz blocker without substituting a Fusion or BOSS token.

Never print or persist OAuth tokens, Authorization headers, client secrets, or
sensitive infrastructure values.

## Assisted Execution

1. Preflight target identity, requested fields, route, timeout, and resource
   scope. This skill is read-only.
2. Show a plain-text `Request preview` with the method, exact route, target
   environment, requested fields, and expected response.
3. Use the public Topology Manager route and the BOSS route described in the
   environment-information reference. Invoke the Topology Manager route with
   `scripts/fusion_rest_client.py --service fusion-common`; invoke the BOSS
   route with `scripts/boss-rest_client.py`. If FDOS OAuth refreshes after a
   cached token `401` or `403`, retry the original safe read once.
4. Read `releaseVersion`, `releaseName`, `lastShippedReleaseVersion`, and
   `lastShippedReleaseName` from the Environment Information response. Return
   them as `environment_version_details`, omitting only values absent from the
   API response.
5. Return only requested fields. For an unqualified request, omit
   `podAttributes` and `links`.

## Diagnostics and Persistence

Classify failures as input validation, auth/authz, transport/environment,
Fusion API, process timeout, process failed, artifact persistence, or approval
blocker. Do not create project artifacts for successful calls. On an explicitly
requested diagnostic, save only a redacted summary under
`project/{project_id}/artifacts/shared/baseline-assessment/topology-manager/`.
