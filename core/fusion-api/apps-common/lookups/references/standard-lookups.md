# Standard Lookups

## Source

Oracle documents the standard lookup resources in [Standard Lookups REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html).
Use them for standard lookup types and their lookup codes, including translated
meanings. These are Application Common Features REST endpoints, invoked through
the shared standard Fusion REST client.

## Endpoints

| Resource | Operation | Method | Endpoint |
| --- | --- | --- | --- |
| Standard lookup type | List | `GET` | `/fscmRestApi/resources/11.13.18.05/standardLookups` |
| Standard lookup type | Create | `POST` | `/fscmRestApi/resources/11.13.18.05/standardLookups` |
| Standard lookup type | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}` |
| Lookup code | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes` |
| Lookup code | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}` |
| Lookup-code translations | List | `GET` | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}/child/translations` |
| Lookup-code translation | Get | `GET` | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}/child/translations/{Language}` |

`LookupType` and `LookupCode` are documented resource keys. If Fusion returns a
different item URI, use that URI.

## Usage

Read a lookup type and its codes:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/standardLookups/<LookupType>' \
  --query expand=lookupCodes
```

Read codes directly when a full parent expansion is not needed:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/standardLookups/<LookupType>/child/lookupCodes'
```

For a create or update, put the exact supported JSON body in a temporary file
and invoke the same shared client with `--method POST|PATCH` and `--body-file`.
Oracle documents `application/json` and
`application/vnd.oracle.adf.resourceitem+json` as supported types for standard
lookup create/update requests. Set `Upsert-Mode=true` only when the caller has
explicitly requested the documented upsert behavior.

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/standardLookups/<LookupType>/child/lookupCodes/<LookupCode>' \
  --method PATCH \
  --body-file /private/tmp/standard-lookup-code-update.json
```

Read the existing resource and obtain explicit approval before any create,
update, or delete. Do not retry a mutating request automatically.
