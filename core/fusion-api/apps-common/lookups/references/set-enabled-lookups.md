# Set-Enabled Lookups

## Source

Use the [Set-Enabled Lookups REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-set-enabled-lookups.html)
when lookup codes must be associated with a reference data set. This category
supports reference-data sharing; the set-enabled code resource includes the
set identity with the lookup code.

## Endpoints

| Resource | Operation | Method | Endpoint |
| --- | --- | --- | --- |
| Set-enabled lookup type | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/setEnabledLookups` |
| Set-enabled lookup type | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/setEnabledLookups/{LookupType}` |
| Lookup code | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/setEnabledLookups/{LookupType}/child/lookupCodes` |
| Lookup code | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/setEnabledLookups/{LookupType}/child/lookupCodes/{setEnabledLookups_lookupCodes_Id}` |

The returned child resource identifier, not a guessed `LookupCode`, identifies
a set-enabled lookup-code item. The resource exposes set information such as
`SetId` and read-only `SetCode`.

## Usage

Retrieve the lookup type and its codes before a change. Use the shared standard
REST client and the exact returned child item link for an update or delete.

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/setEnabledLookups/<LookupType>' \
  --query expand=lookupCodes

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/setEnabledLookups/<LookupType>/child/lookupCodes/<setEnabledLookups_lookupCodes_Id>' \
  --method PATCH \
  --body-file /private/tmp/set-enabled-lookup-code-update.json
```

Confirm the target reference-data set and the current lookup code before a
write. Obtain explicit approval before any create, update, or delete, and do
not retry a mutating request automatically.
