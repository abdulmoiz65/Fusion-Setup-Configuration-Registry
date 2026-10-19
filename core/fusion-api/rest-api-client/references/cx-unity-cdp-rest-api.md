# CX Unity / Customer Data Platform REST API Instructions

Use this instruction file when a calling skill specifies CX Unity or Customer
Data Platform. The endpoint path itself must be passed unchanged; do not add a
`/cdp` prefix.

## Service Configuration

For the specified CX Unity / Customer Data Platform route, the REST client must
use `cdp_restBaseUrl` from:

```text
core/auth/fusionEnv.properties
```

Obtain the access token with `cdp_scope` from the same properties file. Keep the
CDP token in `.fusionaim_cdp_token.json` by default so it is not mixed with
tokens for the standard Fusion service.

## Endpoint Rules

- Use `scripts/fusion_rest_client.py --service cdp`.
- Do not alter the endpoint path or add a `/cdp` prefix.
- Do not use `restBaseUrl` or the standard `scope` for this route.
- Relative endpoints are joined to `cdp_restBaseUrl`; absolute URLs are sent as
  supplied, while authentication uses `cdp_scope`.

## Example

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  --service cdp \
  /<cdp-resource-path>
```
