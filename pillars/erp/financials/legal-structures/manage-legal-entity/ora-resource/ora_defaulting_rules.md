# Manage Legal Entity Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TransactingEntityFlag | Y | User omits the optional flag | Yes when target UI supports the choice |  |
| PsuFlag | N | User omits payroll statutory-unit selection | Yes only with supported HCM validation |  |
| LegalEmployerFlag | N | User omits legal-employer selection | Yes only with supported HCM validation |  |
| EffectiveFrom and EffectiveTo | Null | User omits dates | Yes |  |
| ParentPsuLeIdentifier | Null | No parent PSU applies | Yes only through exact resolver | resolve_entity_parent_psu |
| AttributeCategory and LeInformationContext | Resolved country or deployed localization context; otherwise null | Runtime metadata requires the country-derived context | No | resolve_entity_country_geography |
| Main LRU Name | Exact legal-entity Name | Explicit UI-equivalent aggregate CREATE | No |  |
| MainEstablishmentFlag | Y | Explicit same-name main-LRU child in entity aggregate | No |  |
| TerritoryCode | Resolved territoriesLOV TerritoryCode | Root column when present | No | resolve_entity_country_geography |
| TerritoryShortName | Resolved territoriesLOV TerritoryShortName | Root column when present | No | resolve_entity_country_geography |
| GeographyCode | Resolved TerritoryCode, consistent with the LE country LOV's code relationship | Existing root/main-LRU columns | No | resolve_entity_country_geography |
| GeographyName | Selected primary country addressGeographies GeographyValue | Existing geography-name column | No | resolve_entity_country_geography |
| GeographyType | Selected country result's GeographyType, validated as COUNTRY | Existing geography-type column | No | resolve_entity_country_geography |
| GeographyUse | MASTER_REF, from the endpoint's fixed geography-use restriction, not a returned field | Existing geography-use column | No | resolve_entity_country_geography |
| GeographyElement1 | GeographyName as the agreed country-level derivation | Existing main-LRU column | No | resolve_entity_country_geography |
| GeographyElement2 through GeographyElement10 | Null for this country-only flow | Existing main-LRU columns | No | resolve_entity_country_geography |
| GeographyCodeTransient | Same as GeographyCode | Existing main-LRU transient column | No | resolve_entity_country_geography |
| GeographyNameTransient | Same as GeographyName | Existing main-LRU transient column | No | resolve_entity_country_geography |
| GeographyTypeTransient | Same as GeographyType | Existing main-LRU transient column | No | resolve_entity_country_geography |
| GeographyUseTransient | Same as GeographyUse | Existing main-LRU transient column | No | resolve_entity_country_geography |
| Entity registration RegisteredName | Exact legal-entity Name | Explicit identifying entity child | No |  |
| Entity registration SourceTable | XLE_ENTITY_PROFILES | Explicit identifying entity child | No |  |
| Main-LRU registration RegisteredName | Exact main-LRU Name | Explicit identifying main-LRU child | No |  |
| Main-LRU registration SourceTable | XLE_ETB_PROFILES | Explicit identifying main-LRU child | No |  |
| Both registration Name values | Exact selected jurisdiction Name; never the user's search fragment or LE/LRU name | XLE_REGISTRATION.csv and ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION.csv | No | resolve_entity_identifying_jurisdiction |
| Both registration IdentifyingFlag values | Y in the existing CSV encoding, from the resolved jurisdiction's true identifying flag | Both explicit identifying children | No | resolve_entity_identifying_jurisdiction |
| PartyName, IssuingFormattedAddress, hidden authority/site values | Null | Every supported registration child | No |  |
| Both function child files | Zero candidate rows | Every supported aggregate | No |  |
| Optional place, dates, DFF and localization segments | Null | Not supplied and no active context requires them | Yes |  |

Apply mappings only to columns already present in each target CSV; do not add headers. Keep normal and transient values consistent. TerritoryShortName remains the territory display name and is not a substitute for GeographyName.

GeographyElement1 = GeographyName is the agreed country-level derivation supported by the existing US export evidence. It is not returned by addressGeographies and is not claimed as a universally proven database invariant. Preserve that limitation in preview evidence.

LegalAddress and both child FormattedAddress values come from the same exact legal-address natural-key receipt. Leave LocationId, SourceId, GeographyId, GeographyIdentifierId, JurisdictionId, authority IDs, audit fields, ESS fields, object versions, and other physical or service-generated values blank on CREATE; do not add absent ID columns. Retain lookup IDs only as source-specific evidence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.APPLY_DEFAULTS | step | 40 | apply_default | applied->LE.ENFORCE_DESIGN;blocked->LE.HANDLE_ERROR | LE.CHECK_DEPENDENCIES | stop | After dependencies are ready |
