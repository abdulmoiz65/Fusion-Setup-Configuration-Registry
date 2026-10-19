# Generic Lookups

## Source

Use the [Generic Lookups REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-generic-lookups.html)
when a task must access a lookup through a generic lookup view. The
`ApplicationCode` finder determines the underlying lookup view, such as the
standard or common lookup view; provide that context before treating a generic
lookup result as authoritative.

## Endpoints

| Resource | Operation | Method | Endpoint |
| --- | --- | --- | --- |
| Generic lookup | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/genericLookups` |
| Generic lookup | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/genericLookups/{genericLookups_Id}` |
| Lookup code | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/genericLookups/{genericLookups_Id}/child/lookupCodes` |
| Lookup code | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/genericLookups/{genericLookups_Id}/child/lookupCodes/{LookupCode}` |

Use the returned `genericLookups_Id`; do not construct it from a lookup type
or display name.

## Usage

First inspect the service description and perform the documented
`ApplicationCode` finder query for the caller's lookup view. Then retrieve the
specific generic lookup and, if required, its codes through the shared client.

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/genericLookups/describe

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/genericLookups/<genericLookups_Id>'

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/genericLookups/<genericLookups_Id>/child/lookupCodes'
```

Do not use a generic lookup to bypass a failed Common or Standard lookup
authorization check. For a write, retrieve the current resource, verify the
underlying view selected by `ApplicationCode`, obtain explicit approval, and
send the documented JSON body with `POST` or `PATCH`. Do not retry a mutating
request automatically.
