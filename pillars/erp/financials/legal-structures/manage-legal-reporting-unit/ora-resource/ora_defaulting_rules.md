# Manage Legal Reporting Unit Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| MainEstablishmentFlag | N | Standalone LRU CREATE when user omits the main choice | No; explicit Y requires complete history validation | verify_lru_main_history |
| GeographyCode | Resolved two-letter TerritoryCode | Every supported candidate | No | resolve_lru_country_geography |
| GeographyName and GeographyElement1 | GeographyValue from the selected primary COUNTRY addressGeographies row | Every supported candidate | No | resolve_lru_country_geography |
| GeographyType | COUNTRY | Every supported candidate | No | resolve_lru_country_geography |
| GeographyUse | MASTER_REF | Every supported candidate | No | resolve_lru_country_geography |
| GeographyElement2 through GeographyElement10 | Null | Every supported candidate | No | resolve_lru_country_geography |
| GeographyCodeTransient, GeographyNameTransient, GeographyTypeTransient, GeographyUseTransient | Exact corresponding GeographyCode, GeographyName, GeographyType, GeographyUse values from the same country receipt | Every supported candidate | No | resolve_lru_country_geography |
| Jurisdiction | Null when omitted or blank; otherwise exact explicitly resolved Name | Always | No; never default or infer | resolve_lru_jurisdiction |
| Registration child rows | Zero when jurisdiction is null; one complete new child when explicit jurisdiction, number, and address are resolved | New LRU CREATE | No | resolve_lru_jurisdiction |
| Registration child Name | Exact selected jurisdiction Name | Registration child applies | No | resolve_lru_jurisdiction |
| Registration child RegistrationNumber and FormattedAddress | Explicit user number and exact selected exported address natural key | Registration child applies | No | resolve_lru_registration_address |
| Registration child IdentifyingFlag | Y for the first registration of this new LRU, consistent with the observed first-registration behavior; not copied from the jurisdiction definition flag | Registration child applies to a new LRU | No |  |
| Registration child RegisteredName | Exact LRU Name | Registration child applies | No |  |
| Registration child SourceTable | XLE_ETB_PROFILES | Registration child applies | No |  |
| EffectiveFrom and EffectiveTo | Null | User omits dates | Yes |  |
| MainEffectiveFrom | No CSV default | Main flag is Y | No | verify_lru_main_history |
| EtbInformationContext | Country/localization-derived context or null | Deployed runtime context applies | No | resolve_lru_country_geography |
| PartyName, IssuingFormattedAddress, hidden authority/site values | Null | Supported child | No |  |
| Function child candidate rows | Zero | Supported child | No |  |
| Optional company, activity, dates, DFF and localization segments | Null | Not supplied and no active context requires them | Yes |  |

No GeographyId lookup output is required. GeographyIdentifierId and the jurisdiction's GeographyId are different identities and are receipt-only. Leave GeographyId, LocationId, SourceId, authority IDs, audit, ESS, object-version, and other physical/system values blank on new rows; preserve unchanged baseline rows. Keep the exported parent identifier and LRU-name relationship keys exactly as the current headers require. A null jurisdiction means no new registration child, even when the parent LE has a registration.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.APPLY_DEFAULTS | step | 40 | apply_default | applied->LRU.ENFORCE_DESIGN;blocked->LRU.HANDLE_ERROR | LRU.CHECK_DEPENDENCIES | stop | After dependencies are ready |
