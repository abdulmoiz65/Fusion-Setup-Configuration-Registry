# Knowledge Management REST API Instructions

Use this instruction file for Oracle Knowledge Management REST endpoints whose
path contains `/api/knowledge-management`, such as
`/api/knowledge-management/v2/contentIntelligence`.

## Script

Run from the repository root:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_km_rest_client.py \
  '/api/knowledge-management/v2/contentIntelligence' \
  --method POST \
  --body '{
    "userInput": "{\\"additionalFilters\\":[{\\"fieldName\\":\\"contentTypeAttributes.ORA_CX_SALES_CONTRACT.BUSINESS_UNIT\\",\\"value\\":\\"Vision Operations\\",\\"operator\\":\\"co\\"}],\\"question\\":\\"<SearchQuestion>\\",\\"extractFiltersFromQuestion\\":true}",
    "connectorDetails": {
      "connectorId": "ORA_CX_SALES_CONTRACT"
    },
    "filters": [
      {
        "fieldName": "contentState",
        "value": "PUBLISHED",
        "operator": "eq"
      },
      {
        "fieldName": "contentType.referenceKey",
        "value": "ORA_CX_SALES_CONTRACT",
        "operator": "eq"
      }
    ]
  }'
```

## OAuth Scope and Cache

The Knowledge Management client uses the `km_scope` property from:

```text
core/auth/fusionEnv.properties
```

Its default token cache is:

```text
.fusionaim_km_token.json
```

Pass `--token-cache` only to override that default for the calling workflow.
The client retries once after a 401 or 403 by forcing OAuth login with
`km_scope`.

## Endpoint Rules

- Relative endpoints are joined to `restBaseUrl`.
- Absolute endpoints are accepted only when their HTTPS host and port match a
  `restBaseUrl` or `*_restBaseUrl` value in `core/auth/fusionEnv.properties`.
- Query parameters must be passed with repeated `--query key=value` options.
- Request bodies for mutating calls must be JSON through `--body` or
  `--body-file` and follow the calling skill's approval gate.
- Do not use this route for `/api/boss` endpoints.
