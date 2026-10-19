# Fusion REST API Instructions

Use this instruction file for standard Oracle Fusion REST endpoints such as:

- `/fscmRestApi/...`
- `/hcmRestApi/...`
- `/crmRestApi/...`
- `/fscmUI/applcoreApi/...`, including Flexfield metadata deployment
- Other non-BOSS Fusion REST endpoints hosted by `restBaseUrl`

When the calling skill specifies Field Service or CX Unity / Customer Data
Platform, use the service-specific instruction files: `field-service-rest-api.md`
and `cx-unity-cdp-rest-api.md`.

Do not use this script for `/api/boss` endpoints. Route those calls to
`references/boss-rest-api.md`.

## Script

Run from the repository root:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/setupTasks \
  --query onlyData=true \
  --query limit=1
```

## OAuth Scope and Cache

The script uses the standard `scope` property from:

```text
core/auth/fusionEnv.properties
```

Default token cache:

```text
.fusionaim_token.json
```

Pass `--token-cache` only when a consuming skill needs a different cache path.
`/fscmUI/applcoreApi` is a standard Fusion route, so it must use this default
Fusion scope rather than `fusion_common_scope`, `fs_scope`, `cdp_scope`, or
`boss_scope`.

## Endpoint Rules

- Relative endpoints are joined to `restBaseUrl`.
- Absolute endpoints are accepted only when their HTTPS host and port match a
  `restBaseUrl` or `*_restBaseUrl` value in `core/auth/fusionEnv.properties`.
- Query parameters must be passed with repeated `--query key=value` options.
- Request bodies for mutating calls must be JSON through `--body` or
  `--body-file`.
- The client retries once after a 401 or 403 by forcing OAuth login.

## Examples

Read one setup task:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/setupTasks \
  --query onlyData=true \
  --query limit=1
```

Write response bytes to a file:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/setupTasks \
  --query onlyData=true \
  --output /private/tmp/setupTasks.json
```
