---
skill_id: "core.auth.fusion-oauth-authentication"
name: "Fusion OAuth Authentication"
description: "Provides the fusion oauth authentication core capability for Oracle Fusion Cloud implementation workflows."
layer: "core"
pillar: "Core"
type: "validation"
execution_mode: "assisted"
owner_team: "Central platform team"
version: "0.3.0"
inputs: 
  - "fusion_environment_context"
  - "request_payload"
  - "execution_options"
outputs: 
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
uses_core: []
applicability:
  industries: 
    - "All"
  countries: 
    - "All"
  fusion_releases: 
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "On first use, prompts for the Fusion URL, environment name and OAuth client ID, follows credential-free Fusion HTTPS login redirects, and creates the private OAuth trust policy."
  - "Opens the configured OAuth authorization page and exchanges an authorization code."
  - "Writes the selected local token cache or macOS Keychain entry; Linux confidential login reads a cloud-managed mount or a private local secret file."
required_privileges: 
  - "Fusion privileges appropriate to the requested operation"
---

# Fusion OAuth Authentication

Use this core skill whenever a project workflow needs Oracle Fusion Cloud OAuth
authentication or when the user asks for Fusion login, authentication, access
token retrieval, token-cache refresh, OAuth login, or equivalent Oracle Fusion
Cloud authentication.

## Purpose

For getting-started questions, IAM client application prerequisites, or help
understanding `core/auth/fusionEnv.properties` values, use
[FSCR Onboarding](../../getting-started/onboarding/SKILL.md) for advisory guidance.
Return here when the active workflow selects authentication execution.

Provide the shared OAuth2 authorization-code workflow for Oracle Fusion Cloud
implementation skills. Other router, shared, and pillar skills should use this
core capability instead of duplicating login, token refresh, token cache, or
Fusion REST authentication logic.

## Trigger Phrases

Use this skill when a user or downstream skill says:

- `fusion login`
- `authenticate`
- `get access token`
- `refresh token`
- `OAuth login`
- `Fusion OAuth`
- `Fusion authentication`

## Project Scripts

Run from the repository root. Use the scripts bundled with this skill:

- `core/auth/fusion-oauth-authentication/scripts/fusion_login.py`
- `core/auth/fusion-oauth-authentication/scripts/fusion_auth.py`

All login and REST CLI defaults use the shared external profile cache:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py --token-cache auto
```

Select a service explicitly to authenticate its configured scope and save its
separate reusable cache:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py --service fusion-common
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py --service boss
```

| Service | Base URL property | Scope property | Default service file cache |
| --- | --- | --- | --- |
| `standard` | `restBaseUrl` | `scope` | Managed profile cache |
| `boss` | `restBaseUrl` | `boss_scope` | Managed profile cache |
| `fusion-common` | `restBaseUrl` | `fusion_common_scope` | Managed profile cache |
| `field-service` | `fs_restBaseUrl` | `fs_scope` | Managed profile cache |
| `cdp` | `cdp_restBaseUrl` | `cdp_scope` | Managed profile cache |

Each profile uses `~/.fusionaim/<profile-fingerprint>_token.json`; the fingerprint
binds the approved issuer/endpoints, client, target and scope. `auto` means this
managed location, never a literal file named `auto`. Custom paths inside the
checkout are rejected. External custom paths need a user-owned mode-0700 parent;
cache reads/writes reject symlinks, hardlinks and unsafe permissions. Writes use
a mode-0600 temporary file and atomic replacement.

Login and REST clients share the service configuration in `fusion_auth.py`.
`--token-cache` overrides the selected default. Missing or blank service scopes
block authentication; never substitute `scope` or `boss_scope` for
`fusion_common_scope`. Use the exact scope registered with the configured OAuth
application, without deriving a scope from the environment label. Local scope
selection does not grant privileges at the identity provider or Fusion API.

The default Fusion environment properties file is:

```text
core/auth/fusionEnv.properties
```

This file provides:

- `environment`
- `restBaseUrl`
- `fs_restBaseUrl`
- `fs_scope`
- `fusion_common_scope`
- `cdp_restBaseUrl`
- `cdp_scope`
- `clientId`
- `scope`
- `boss_scope`
- `redirectUrl`

The additional service properties are read when the login CLI or a consuming
REST client selects the corresponding service. Standard login uses
`restBaseUrl` and `scope`.

OAuth `authorizeUrl` and `tokenUrl` are derived from the selected environment's
`issuer`, `authorize_path`, and `token_path` in `~/.fusionaim/oauth-trust.json`.
Do not add these URLs to the properties file. Matching legacy URL settings remain
compatible; conflicting values are rejected before authentication.

Do not print access tokens, client secrets, or `.fusionaim_token.json` contents.

## Inputs

- `fusion_environment_context`
- `request_payload`
- `execution_options`

Script-level inputs:

- `--service`: `standard` (default), `boss`, `fusion-common`, `field-service`, or
  `cdp`; selects the configured scope, base URL, and default cache

- `--properties`: optional override path for the Fusion environment properties file;
  defaults to `core/auth/fusionEnv.properties`
- `--auth-code`: optional OAuth2 authorization code
- `--code-verifier`: required with `--auth-code` when `pkce=true`
- `--redirect-url`: optional redirect URI override
- `--callback-timeout`: seconds to wait for a loopback callback
- `--token-cache`: path to the file token cache
- `--no-open-browser`: print the authorization URL without opening a browser

## Independent OAuth Trust Enrollment

Login requires a trust policy enrolled separately from caller-selectable properties.
The user supplies the Fusion URL, environment name and OAuth client ID; the supplied
Fusion origin's HTTPS login redirects establish the IdP origin for enrollment.
Do not derive the trust source from an arbitrary properties file's OAuth URLs.
The fixed trust source is `~/.fusionaim/oauth-trust.json` (mode 0600 in a mode-0700
directory); properties and environment variables cannot select another policy.
When the file is missing, use this exact welcome prompt in both interactive CLI
and agent-assisted login:

> FSCR needs to enroll the trusted Fusion Environment
> Please enter the Fusion URL and a name for the environment. Also provide the Oauth Client ID so that an approved environments trust file can be created

Collect **Fusion URL**, **environment name**, and **Oauth Client ID** together.
Do not ask for the issuer or append a client-secret request to this welcome prompt.
The name and client ID must match the selected configuration for login to continue.

After validating the inputs, the declared discovery step performs unauthenticated
GET requests from the supplied Fusion HTTPS origin's root. It follows at most eight
same-origin redirects within 30 seconds and derives the issuer from the redirect to
`/oauth2/v1/authorize` on the identity origin, without requesting that off-origin URL.
It sends no bearer token, Basic header, client secret or cookies, does not submit
forms or execute scripts, and never stores redirect query parameters. HTTP downgrade,
credential URLs, ambiguous destinations, loops and failed discovery stop enrollment.
For environment validation, the same read-only discovery helper may inspect the
already selected Fusion environment; validation alone must not create/replace trust.

The resulting policy pins the Fusion origin, issuer, client ID and exact OAuth paths;
subsequent login derives both OAuth endpoints from it. No OpenID
discovery document is used. Standard endpoint paths are documented by
[Oracle](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oaext/configure-oauth.html).
The directory is mode 0700 and the policy mode 0600. Blank, cancelled, invalid or
mismatched inputs do not create a policy, and existing invalid files are not replaced.

For agent-run login without interactive stdin, show the welcome prompt, collect the
three values, run the command below using those answers, then resume the requested
login and scope. Unattended callers receive setup guidance instead of waiting for input.

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_auth_setup.py trust \
  --fusion-url https://APPROVED_FUSION_HOST --environment ENVIRONMENT_NAME \
  --client-id APPROVED_CLIENT_ID
```

The pinned paths are `/oauth2/v1/authorize` and `/oauth2/v1/token`. Environments with
other login mechanisms or approved endpoint paths can use explicit `--issuer`
instead of `--fusion-url`, together with `--authorize-path` and `--token-path`.
Existing enrollment changes require `--replace`. This local enrollment does not
authorize live Fusion operations or bypass their routed workflow prerequisites.

## PKCE Public-Client Option

PKCE/public-client mode is the default (`pkce=true`). `clientId` remains required;
plaintext `clientSecret` properties are never used for authentication. The login
script creates a one-time S256 verifier and challenge for interactive browser
logins; it never stores or prints the verifier. When supplying `--auth-code`,
also supply its matching `--code-verifier`.

An existing confidential application may explicitly set `pkce=false`. On
macOS and Windows, after independent trust enrollment, store its secret through
the hidden prompt:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_auth_setup.py store-client-secret \
  --properties core/auth/fusionEnv.properties
```

Remove real `clientSecret` values from the properties file after successful
storage; never put secrets in command arguments. The helper validates pins before
prompting or accessing private credential storage, and the exchange revalidates
before forming Basic. For a legacy properties secret on macOS or Windows, add
`--migrate-properties-secret` to move it into private storage after pin
validation, verify storage, and clear only that property value.

On Linux, `store-client-secret` can enroll an explicitly supplied secret in
`~/.fusionaim/oauth-client-secrets/<account>.json`. This is a hidden, user-owned
mode-0600 file under mode-0700 directories, bound to the approved environment,
issuer, and client. It is plaintext at rest, so use it only when that local
storage is acceptable for the VM. The helper prompts without echo and verifies
the stored value. `--migrate-properties-secret` also works on Linux after trust
validation and clears the properties value after successful storage.

For a VM with a cloud secret manager, prefer its mounted secret instead. When
either `FSCR_OAUTH_CLIENT_SECRET_FILE` or `FSCR_OAUTH_CLIENT_SECRET_ACCOUNT` is
set, FSCR requires the complete cloud mount configuration and does not fall
back to the local file.

On a headless Linux VM, use the VM's cloud secret manager to mount the approved
client secret as a private, single-line UTF-8 file outside the checkout. The
runner supplies only its absolute path and the account binding through
`FSCR_OAUTH_CLIENT_SECRET_FILE` and `FSCR_OAUTH_CLIENT_SECRET_ACCOUNT`.
FSCR reads the secret at exchange time; it does not copy it into its own store.
The file must be a regular single-link file owned by root or the runner, with
no group or other permissions (for example mode 0400 or 0600). Symlinks are
rejected. The cloud secret manager and VM identity are configured outside FSCR.
Do not place the secret value in an environment variable, properties file,
command argument, repository file, log, or project artifact.

After enrolling trust, get the non-secret account binding for the selected
configuration and configure the VM's mount and environment:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_auth_setup.py \
  client-secret-account --properties core/auth/fusionEnv.properties
# Set FSCR_OAUTH_CLIENT_SECRET_ACCOUNT to that output.
# Set FSCR_OAUTH_CLIENT_SECRET_FILE to the absolute mounted-file path.
python3 core/auth/fusion-oauth-authentication/scripts/fusion_auth_setup.py \
  check-client-secret --properties core/auth/fusionEnv.properties
```

A Linux runner using the cloud mount replaces `store-client-secret` with this preflight. Keep
`pkce=false` and the existing login/token-cache flow. A different environment,
issuer, or client ID produces a different account binding and fails closed
until the runner's secret configuration is updated.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

Script-level outputs:

- A refreshed access token cache stored in the requested cache path, macOS Keychain,
  or the default per-profile file cache.
- Console status indicating login completion and cache location, without exposing
  token values.

## Callback Behavior

If `redirectUrl` is a loopback URL such as:

```text
http://127.0.0.1:8765/oauth/callback
```

the login script starts a temporary local listener before opening the browser
and auto-captures the authorization code.

If `redirectUrl` is not loopback, the script cannot capture the code
automatically. Ask the user to paste only the redirected `code=` query parameter,
then feed it to the waiting login process.

## Use by Other Skills

Other project skills should reference this skill for login and token refresh.
Their REST scripts may import `fusion_auth.py` from this skill's `scripts/`
folder and accept:

- `--token-cache auto`
- `--auth-code`
- `--redirect-url`
- `--force-login`
- `--access-token`

If a REST script reports that the cached token was rejected, refresh
authentication using this skill, then retry the original operation.

## Security Rules

1. Never print access tokens, refresh tokens, client secrets, or full token-cache
   contents.
2. Use the managed cache outside the checkout; never store a token under `project/`
   or pass a historical repository-local cache name.
3. Keep file token caches user-readable and user-writable only.
4. Treat `core/auth/fusionEnv.properties` as
   environment-specific configuration and avoid copying its values into generated
   artifacts.

## Error Handling

Preflight the selected environment, enrolled trust policy, client ID, redirect
URI, PKCE mode, and private cache path before login. For `pkce=false`, validate
the secret account binding and private storage before the token exchange.
Missing or mismatched configuration is an input-validation or authorization
failure; stop without trying another environment or secret source.

Treat an unavailable identity provider or cloud-mounted secret as a transport
or environment failure. A rejected authorization code or token response is an
OAuth service failure. Report the stage, selected environment, failure class,
and a safe next action. Never print or persist authorization codes, access
tokens, client secrets, token-cache contents, or secret-bearing responses.
Do not retry a token exchange automatically after an ambiguous failure; start
a fresh authorization flow when needed.

## Implementation Notes

This file defines the repository contract for the OAuth capability. The bundled
scripts provide the current implementation. Implementations must record request
parameters, environment identity, side effects, and any authentication diagnostic
information needed for auditability without exposing secrets.

## Final Response

For login-only requests, report whether login completed and where the cache was
saved:

```text
Fusion login complete. The refreshed token was saved in ~/.fusionaim/<profile-fingerprint>_token.json.
```
