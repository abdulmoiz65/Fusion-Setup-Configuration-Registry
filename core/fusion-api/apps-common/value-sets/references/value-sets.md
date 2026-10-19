# Value Sets

## Source

Oracle documents the value-set collection in [Value Sets REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-value-sets.html).
A value set defines valid values for business-object attributes. The root
resource is documented for viewing; valid values have their own child resource.

## Endpoints

| Resource | Operation | Method | Endpoint |
| --- | --- | --- | --- |
| Value sets | List | `GET` | `/fscmRestApi/resources/11.13.18.05/valueSets` |
| Value set | Get | `GET` | `/fscmRestApi/resources/11.13.18.05/valueSets/{valueSets_Id}` |
| Table validation metadata | List | `GET` | `/fscmRestApi/resources/11.13.18.05/valueSets/{valueSets_Id}/child/validationTable` |
| Table validation metadata | Get | `GET` | `/fscmRestApi/resources/11.13.18.05/valueSets/{valueSets_Id}/child/validationTable/{valueSets_validationTable_Id}` |
| Value-set values | List, create | `GET`, `POST` | `/fscmRestApi/resources/11.13.18.05/valueSets/{valueSets_Id}/child/values` |
| Value-set value | Get, update, delete | `GET`, `PATCH`, `DELETE` | `/fscmRestApi/resources/11.13.18.05/valueSets/{valueSets_Id}/child/values/{valueSets_values_Id}` |

The child value operations are documented in [Values REST
Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-value-sets-values.html).
Use response identifiers as returned; do not derive an identifier from a value
name or value set code.

## Usage

List value sets, retrieve one value set, and retrieve its valid values through
the shared client:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/valueSets

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/valueSets/<valueSets_Id>'

python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/valueSets/<valueSets_Id>/child/values'
```

To change a valid value, first retrieve it and then use its returned identifier
with the documented request body:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  '/fscmRestApi/resources/11.13.18.05/valueSets/<valueSets_Id>/child/values/<valueSets_values_Id>' \
  --method PATCH \
  --body-file /private/tmp/value-set-value-update.json
```

The current scope exposes no create/update/delete operation for the root value
set in the linked Value Sets REST endpoint page. Treat any request to create or
alter a value-set definition as unsupported by this skill until a current Oracle
source identifies a supported endpoint. Obtain explicit approval before writes
to child values and do not retry them automatically.
