---
skill_id: "core.fusion-api.rest-api-client"
name: "Rest API Client"
description: "Routes Oracle Fusion, CPQ, Knowledge Management, Risk and Security, and Fusion BOSS REST API calls to the correct OAuth-backed client instructions and scripts."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "automated"
owner_team: "Central platform team"
version: "0.6.1"
inputs: 
  - "fusion_environment_context"
  - "request_payload"
  - "execution_options"
outputs: 
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
depends_on:
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
applicability:
  industries: 
    - "All"
  countries: 
    - "All"
  fusion_releases: 
    - "Current Oracle Fusion Cloud release"
side_effects: 
  - "Connects to Fusion REST APIs when invoked."
  - "May refresh the OAuth token cache when the cached token is unavailable or rejected."
required_privileges: 
  - "Fusion privileges appropriate to the requested operation"
---

# Rest API Client

## Purpose

Route Oracle Fusion REST, CPQ, Knowledge Management, Risk and Security, and Fusion BOSS REST API work to the correct
OAuth-backed client script and instruction file without duplicating token-cache,
request, retry, and response handling logic in consuming skills.

## Routing

Use this skill whenever another router, shared, core, or pillar skill needs to
call a Fusion REST endpoint.

| Endpoint type | Route to | Script |
| --- | --- | --- |
| Standard Fusion REST, such as `/fscmRestApi`, `/hcmRestApi`, `/crmRestApi`, `/fscmUI/applcoreApi`, or absolute Fusion REST URLs | `references/fusion-rest-api.md` | `scripts/fusion_rest_client.py` |
| Fusion Common REST endpoints under `/api/fusion-common` | `references/fusion-common-rest-api.md` | `scripts/fusion_rest_client.py --service fusion-common` |
| Calling skill specifies Fusion Field Service / Field Service | `references/field-service-rest-api.md` | `scripts/fusion_rest_client.py --service field-service` |
| Calling skill specifies CX Unity / Customer Data Platform | `references/cx-unity-cdp-rest-api.md` | `scripts/fusion_rest_client.py --service cdp` |
| CPQ REST endpoint containing `/cpq` | `references/cpq-rest-api.md` | `scripts/fusion_cpq_rest_client.py` |
| Knowledge Management REST endpoint containing `/api/knowledge-management` | `references/km-rest-api.md` | `scripts/fusion_km_rest_client.py` |
| Risk and Security REST endpoint containing `/api/risk-cloud` | `references/rmc-rest-api.md` | `scripts/fusion_rmc_rest_client.py` |
| Fusion BOSS REST endpoints under `/api/boss` | `references/boss-rest-api.md` | `scripts/boss-rest_client.py` |

Before invoking a script, read the routed instruction file in this skill folder.

## Shared Configuration

All client scripts read the default Fusion environment properties file:

```text
core/auth/fusionEnv.properties
```

All client scripts import OAuth helpers from:

```text
core/auth/fusion-oauth-authentication/scripts/fusion_auth.py
```

Endpoints under `/fscmUI/applcoreApi`, including Flexfield deployment APIs,
are standard Fusion REST routes. Authenticate them with the default Fusion
`scope` and `restBaseUrl` properties; do not select a service-specific scope
or token cache for them.

If the cached token is missing, expired, or rejected by Fusion with HTTP 401 or
403, the selected script invokes `core.auth.fusion-oauth-authentication` to
obtain a fresh token, saves it to the requested cache, and retries the REST call
once.

## Inputs

- `fusion_environment_context`
- `request_payload`
- `execution_options`

Common script-level inputs:

- `endpoint`: Fusion REST resource path or absolute URL.
- `--method`: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`.
- `--query`: repeated query parameters as `key=value`.
- `--header`: repeated extra headers as `Name=value` or `Name: value`.
- `--body` or `--body-file`: JSON request body for write operations.
- `--output`: optional response output file.
- `--token-cache`: optional external private cache override; the default `auto`
  resolves to `~/.fusionaim/<profile-fingerprint>_token.json`; checkout paths fail.
- `--scim-only`: provisioning mode; requires the standard service and relative
  `/hcmRestApi/scim/Users` or `/hcmRestApi/scim/Roles` collection/resource paths.
  Password fields, alternate origins and write redirects are rejected.
- `--force-login`, `--auth-code`, `--redirect-url`, and browser flags passed to
  the shared OAuth flow when login is required.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

Script-level outputs:

- Pretty-printed JSON response to stdout by default, or raw response bytes when
  `--output` is supplied.
- HTTP status when writing to a file.
- Token-cache refresh status without printing access tokens.

## Implementation Notes

Never print access tokens, refresh tokens, client secrets, token-cache contents,
or Authorization headers.

Only send credentials or bearer tokens to the single HTTPS origin selected for
the active service in `core/auth/fusionEnv.properties`. Reject other absolute
endpoints before obtaining a token, and reject redirects to a different origin,
including other configured service origins. Fusion Common endpoints require
`--service fusion-common`, `fusion_common_scope`, and their separate token cache.

Consumers that must pin a token to one approved service origin, including FSM
Set Optin, use `scripts/trusted_http.py`. Supply `approved_origin` from the
trusted environment profile, independently of request URLs or overrides. This
transport validates HTTPS scheme, hostname, and effective port on the initial
request and every redirect. Only same-origin GET/HEAD redirects are followed;
write redirects fail without replay. It never obtains or refreshes tokens.
The multi-service REST CLI routes use `fusion_auth.py` to bind requests to the
selected service origin and OAuth scope.

For mutating methods such as `POST`, `PUT`, `PATCH`, and `DELETE`, consuming
skills must capture the request purpose, target environment, endpoint, and any
Fusion job or process identifiers returned by Fusion in their own audit output.
