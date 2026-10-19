# CPQ REST API Instructions

Use this instruction file for Oracle CPQ REST endpoints whose path contains
`/cpq`, such as `/cpq/rest/v19/pricingSetup/models`.

## Script

Run from the repository root:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_cpq_rest_client.py \
  /cpq/rest/v19/pricingSetup/models \
  --method GET \
  --query '<key>=<value>' \
  --token-cache auto
```

## OAuth Scope and Cache

The CPQ client uses the `cpq_scope` property from:

```text
core/auth/fusionEnv.properties
```

Its default token cache is:

```text
.fusionaim_cpq_token.json
```

Pass `--token-cache` only to override that default for the calling workflow.
The client retries once after a 401 or 403 by forcing OAuth login with
`cpq_scope`.

## Endpoint Rules

- Relative endpoints are joined to `restBaseUrl`.
- Absolute endpoints are accepted only when their HTTPS host and port match a
  `restBaseUrl` or `*_restBaseUrl` value in `core/auth/fusionEnv.properties`.
- Query parameters must be passed with repeated `--query key=value` options.
- Request bodies for mutating calls must be JSON through `--body` or
  `--body-file` and follow the calling skill's approval gate.
- Do not use this route for `/api/boss` endpoints.
