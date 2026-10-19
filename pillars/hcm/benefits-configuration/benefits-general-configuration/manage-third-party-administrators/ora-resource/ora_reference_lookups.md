# Manage Third-Party Administrators Reference Resolution

| Resolver | Required result | Failure behavior |
|---|---|---|
| `core.data-loader` Organization metadata | Compatible `Organization` and `OrgUnitClassification` sections, keys, allowed values, and required fields | Stop on unavailable, ambiguous, or incompatible metadata. |
| Organization classifications LOV | `GET /hcmRestApi/resources/latest/organizationClassificationsLOV?q=ClassificationCode='BEN TPA'` with `REST-Framework-Version: 9` returns exactly one nonblank `ClassificationName` | Stop on a failed, zero, multiple, or blank-name result; do not hard-code. |
| Locations LOV | `GET /hcmRestApi/resources/latest/locationsLov`, effective on `EffectiveStartDate`, with `REST-Framework-Version: 9`, returns one exact `LocationName`/`SetName` match | Map `LocationCode` and `SetCode`; stop on missing mapped fields or non-unique results. |

Use the returned classification name in both DAT rows and keep every
`ClassificationCode` field blank. If both explicit location codes are supplied,
skip the location resolver and use the values as-is. All reads are through the
declared core REST client; do not use a direct REST write.
