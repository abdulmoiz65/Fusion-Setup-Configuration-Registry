# Manage Legal Reporting Unit Registrations Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SourceTable | XLE_ETB_PROFILES | Every supported LRU registration row | No |  |
| Entity and LRU parent carriers | Exact resolved LegalEntityIdentifier and LegalReportingUnitName | Every supported row | No | verify_lru_registration_parents |
| IdentifyingFlag | Value from the exact jurisdiction receipt | Jurisdiction resolves | No | resolve_lru_registration_jurisdiction |
| Jurisdiction and RegInformation contexts | Values from the same jurisdiction and legislative-category receipt; otherwise null | Deployed target localization requires context | No | resolve_lru_registration_jurisdiction |
| PartyName and IssuingFormattedAddress | Null | Every supported candidate | No |  |
| Hidden authority and authority-site identifiers | Null | Every supported candidate | No |  |
| Place, effective dates, DFF and localization segments | Null | Not supplied and no active context requires them | Yes |  |
| ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION_FUNCTION.csv candidate rows | Zero | Every supported candidate | No |  |

FormattedAddress is the exact active legal-address natural key. Leave LocationId, SourceId, parent physical IDs, JurisdictionId, authority IDs, audit fields, ESS fields, and object versions blank on CREATE. RegistrationNumber is explicit user input and receives no surrogate default.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUR.APPLY_DEFAULTS | step | 40 | apply_default | applied->LRUR.ENFORCE_DESIGN;blocked->LRUR.HANDLE_ERROR | LRUR.CHECK_DEPENDENCIES | stop | After dependencies are ready |
