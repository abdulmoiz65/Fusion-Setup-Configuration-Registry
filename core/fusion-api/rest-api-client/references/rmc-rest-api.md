# Risk and Security REST API Instructions

Use this instruction file for Oracle Risk and Security REST endpoints whose
path contains `/api/risk-cloud`, such as
`/api/risk-cloud/rc-tools-ms/dataintegration/v1/dataIntegratorConnectorDefinitions`.

## Script

Run from the repository root:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rmc_rest_client.py \
  '/api/risk-cloud/rc-tools-ms/dataintegration/v1/dataIntegratorConnectorDefinitions' \
  --method POST \
  --body '{}'
```

## OAuth Scope and Cache

The Risk and Security client uses the `rmc_scope` property from:

```text
core/auth/fusionEnv.properties
```

Its default token cache is:

```text
.fusionaim_rmc_token.json
```

Pass `--token-cache` only to override that default for the calling workflow.
The client retries once after a 401 or 403 by forcing OAuth login with
`rmc_scope`.

## Endpoint Rules

- Relative endpoints are joined to `restBaseUrl`.
- Absolute endpoints are accepted only when their HTTPS host and port match a
  `restBaseUrl` or `*_restBaseUrl` value in `core/auth/fusionEnv.properties`.
- Query parameters must be passed with repeated `--query key=value` options.
- Request bodies for mutating calls must be JSON through `--body` or
  `--body-file` and follow the calling skill's approval gate.
- Do not use this route for `/api/boss` endpoints.
