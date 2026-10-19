# Fusion Common REST API Instructions

Use this instruction file for Fusion Common REST endpoints under:

```text
/api/fusion-common
```

## Service Configuration

Use `scripts/fusion_rest_client.py --service fusion-common`. The client uses
`restBaseUrl` and `fusion_common_scope` from:

```text
core/auth/fusionEnv.properties
```

Keep the Fusion Common token in `.fusionaim_fusion_common_token.json` by
default. This separate cache prevents a Fusion Common token from being reused
for standard Fusion, BOSS, Field Service, or CDP endpoints.

To obtain or refresh this token separately, use:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py --service fusion-common
```

The login CLI and REST client use the same configured scope and default cache.
An empty or missing `fusion_common_scope` fails before login; an identity-provider
scope rejection requires correction of the registered scope or client grants,
not a fallback to another token.

## Endpoint Rules

- Use `--service fusion-common` for every `/api/fusion-common` endpoint.
- Relative endpoints are joined to `restBaseUrl`; absolute HTTPS endpoints are
  sent as supplied while authentication still uses `fusion_common_scope`.
- Do not use the standard `scope` or `boss_scope` for this route.
- The client rejects Fusion Common endpoints without `--service fusion-common`
  and rejects other API paths when that service is selected, before login.
- The client retries one safe read after an HTTP 401 or 403 by refreshing only
  the Fusion Common token.

## Example

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  --service fusion-common \
  /api/fusion-common/topologymanager/v1/environmentInfo
```
