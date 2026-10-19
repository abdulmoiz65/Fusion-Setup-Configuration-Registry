# Field Service REST API Instructions

Use this instruction file when a calling skill specifies Fusion Field Service or
Field Service. The endpoint path itself must be passed unchanged; do not add an
`/fs` prefix.

## Service Configuration

For the specified Field Service route, the REST client must use
`fs_restBaseUrl` from:

```text
core/auth/fusionEnv.properties
```

Obtain the access token with `fs_scope` from the same properties file. Keep the
Field Service token in `.fusionaim_fs_token.json` by default so it is not mixed
with tokens for the standard Fusion service.

## Endpoint Rules

- Use `scripts/fusion_rest_client.py --service field-service`.
- Do not alter the endpoint path or add an `/fs` prefix.
- Do not use `restBaseUrl` or the standard `scope` for this route.
- Relative endpoints are joined to `fs_restBaseUrl`; absolute URLs are sent as
  supplied, while authentication uses `fs_scope`.

## Example

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  --service field-service \
  /<field-service-resource-path>
```
