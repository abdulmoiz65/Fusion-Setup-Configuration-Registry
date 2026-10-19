# Application Endpoint API Reference

Source: supplied Topology Manager OpenAPI v3.0.1 contract.

| Operation | Method and path | Inputs | Contract behavior |
| --- | --- | --- | --- |
| List application endpoints | `GET /endpoints` | Optional `limit`, `offset`, `totalResults`, `q` | Defaults: `limit=500`, `offset=0`, `totalResults=false`, `q=""`. |
| Get application endpoint | `GET /endpoints/{endpointKey}` | `endpointKey` | Returns an `Endpoint`. |
| Create application endpoint | `POST /endpoints` | `endpointKey`, `endpoint`; optional `hostName`, `port`, `protocol`, `defaultUrl`, `canonicalEndpoint`, `additionalProperties` | Exact-preview approval; success is `201 Created`. |
| Update application endpoint | `PATCH /endpoints/{endpointKey}` | Path `endpointKey`; valid `Endpoint` payload | Exact-preview approval; success is `201 Created`. |
| Delete application endpoint | `DELETE /endpoints/{endpointKey}` | `endpointKey` | Exact-preview approval; success is `204 No Content`. |
| Get enterprise application domain | `GET /enterpriseApplications/{endpointKey}?fields=domainName` | `endpointKey` | Safe PATCH preflight: non-empty `domainName` means provisioned; empty or null `domainName` means not provisioned. |

The supported inbound `Endpoint` fields are `endpointKey`, `endpoint`,
`hostName`, `port`, `protocol`, `defaultUrl`, `canonicalEndpoint`, and
`additionalProperties`. `endpointKey` and `endpoint` are required for create or
update. Response JSON renders `hostName` as response field `host` and may also
include `links`.

## Provisioned Application Update Preflight

Before an endpoint PATCH preview, retrieve the enterprise application with
`GET /enterpriseApplications/{endpointKey}?fields=domainName`.

- A non-empty `domainName` identifies a provisioned application and requires
  the provisioned-app overwrite warning plus explicit approval.
- An empty or null `domainName` identifies a non-provisioned application and
  uses the standard PATCH preview and approval guidance.
- Any failed or unexpected preflight response must fail closed; do not render
  or execute the PATCH.

## Application Endpoint Resolution

- `app`, `application`, `endpoint`, and app-short-name variants identify
  `endpointKey`. Conflicting values require one concise clarification and no
  API call.
- `host` and `hostname` map to request field `hostName`. The response field
  `host` is outbound-only.
- An explicit `endpoint` label or a plain `url` maps to `endpoint`. Different
  supplied values fail closed.
- `default url`, `default_url`, and `defaultUrl` map to `defaultUrl`.
- Correct `protcol` to `protocol` only when the endpoint request has one clear
  interpretation.
- Numeric ports are serialized as strings. When host and port lack a protocol,
  send inferred `protocol: "https"` and mark it in the preview.
- Without an endpoint or URL, require `hostName` and `port`, construct
  `{protocol}://{hostName}:{port}`, and mark the constructed value as inferred.
  Complete host and port take precedence over `defaultUrl`. When host or port
  is missing, use `defaultUrl` as the endpoint only when supplied; otherwise
  ask for endpoint, URL, host and port, or default URL.

## Endpoint Create Preflight

Before `POST /endpoints`, issue `GET /endpoints/{endpointKey}` for the
normalized create target.

- A `404 Not Found` means the key is available; show the create preview and
  require explicit approval.
- A `200 OK` is an `overwrite-conflict`; stop and do not send POST or switch to
  PATCH.
- A separately requested PATCH requires a new explicit approval.
- Any other outcome fails closed; do not send POST.

For an unqualified list, request `limit=500` and `offset=0`. Continue pages
while `hasMore=true`, advancing the offset by `500`. If the user provides
`limit` or `offset`, do not infer another page range.

## Response Presentation

For one application endpoint lookup, return only the `endpoint` value unless
the user asks for additional fields. Do not add `endpointKey`, `host`, `port`,
`protocol`, `defaultUrl`, `links`, or other properties by default.

For endpoint lists, return only requested fields for each item. When no fields
are requested, return `endpointKey` and `endpoint` side by side. State the
total returned and final offset after an unqualified paginated list.

Do not automatically retry a mutation. Redact credentials and sensitive payload
values in diagnostics.
