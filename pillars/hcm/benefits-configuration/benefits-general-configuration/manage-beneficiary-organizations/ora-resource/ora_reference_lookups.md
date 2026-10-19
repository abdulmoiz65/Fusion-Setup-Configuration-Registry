# Manage Beneficiary Organizations Reference Resolution

Use only read-only operations selected by the active workflow and the declared
core services. Do not construct a direct REST write or use a different business
object as a fallback.

| Resolver | Runs when | Required result | Failure behavior |
|---|---|---|---|
| `core.data-loader` Organization metadata | Before authoring or validating an HDL source | Current `Organization` and `OrgUnitClassification` sections, keys, required fields, allowed values, and classification-code support | Stop for missing, ambiguous, or incompatible metadata. |
| Declared shared REST client | Create duplicate check or update/inactivate identity resolution, when selected by the workflow | Zero exact existing matches for create; exactly one eligible target for update/inactivate | Stop for zero or multiple target matches; never choose the first result. |
| Organization classifications LOV | Before every create or update source is authored | `GET /hcmRestApi/resources/latest/organizationClassificationsLOV?q=ClassificationCode='HR_BEN'` with `REST-Framework-Version: 9` returns exactly one nonblank `ClassificationName` | Stop if the read fails, returns zero or multiple rows, or omits `ClassificationName`; do not hard-code a name. |
| Locations LOV | Create or update has Task Location Name and Location Set Name but no explicit complete code pair | `GET /hcmRestApi/resources/latest/locationsLov`, effective on `EffectiveStartDate`, with `REST-Framework-Version: 9` returns exactly one row whose `LocationName` and `SetName` exactly equal the supplied values | Map response `LocationCode` to DAT `LocationCode` and `SetCode` to DAT `LocationSetCode`; stop on zero or multiple exact matches, missing mapped fields, or a failed effective-date read. |

Use the returned `ClassificationName` in the `Organization` and
`OrgUnitClassification` DAT rows. Do not populate `ClassificationCode` in DAT
for create or update.

For the location LOV, send the beneficiary organization start date through the
endpoint's live effective-date parameter and filter by the two supplied names.
Comparison is exact: no trimming, case-folding, partial matching, or fallback
selection. When both explicit `LocationCode` and `LocationSetCode` are supplied,
skip this resolver and use those values as-is.

Every request to `organizationClassificationsLOV` or `locationsLov` must include
the exact header `REST-Framework-Version: 9`.

Retain identifiers internally for source construction and matching. Do not expose
surrogate IDs, credentials, or unnecessary source values in guidance or reports.
