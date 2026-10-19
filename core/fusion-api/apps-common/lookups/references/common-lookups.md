# Common Lookups

## Source

Use the [Common Lookups REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-common-lookups.html)
for common lookup types, codes, and translations. Common lookups support legacy
or attribute-bearing lookup definitions and backward compatibility.

## Endpoints

| Resource | Operation | Method | Endpoint |
| --- | --- | --- | --- |
| Common lookup type | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/commonLookups` |
| Common lookup type | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/commonLookups/{LookupType}` |
| Lookup code | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/commonLookups/{LookupType}/child/lookupCodes` |
| Lookup code | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/commonLookups/{LookupType}/child/lookupCodes/{LookupCode}` |
| Lookup-code translations | List | `GET` | `/fscmRestApi/resources/11.13.18.05/commonLookups/{LookupType}/child/lookupCodes/{LookupCode}/child/translations` |
| Lookup-code translation | Get | `GET` | `/fscmRestApi/resources/11.13.18.05/commonLookups/{LookupType}/child/lookupCodes/{LookupCode}/child/translations/{Language}` |

## Usage

Use the shared standard REST client. Retrieve the common lookup before changing
it and use the documented `LookupType` and `LookupCode` resource keys.

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/commonLookups/<LookupType>' \
  --query expand=lookupCodes

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/commonLookups/<LookupType>/child/lookupCodes/<LookupCode>' \
  --method PATCH \
  --body-file /private/tmp/common-lookup-code-update.json
```

`POST` create requests support `application/json` and
`application/vnd.oracle.adf.resourceitem+json`. Use `Upsert-Mode=true` only
when the caller has explicitly chosen the documented upsert behavior. Obtain
explicit approval before any create, update, or delete, and do not retry a
mutating request automatically.
