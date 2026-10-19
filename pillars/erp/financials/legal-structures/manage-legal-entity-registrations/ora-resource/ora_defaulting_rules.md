# Manage Legal Entity Registrations Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SourceTable | XLE_ENTITY_PROFILES | Every supported entity registration row | No |  |
| IdentifyingFlag | Value from the exact jurisdiction receipt | Jurisdiction resolves | No | resolve_entity_registration_jurisdiction |
| Jurisdiction and RegInformation contexts | Values derived from the same jurisdiction and legislative-category receipt; otherwise null | Deployed target localization requires a context | No | resolve_entity_registration_jurisdiction |
| PartyName and IssuingFormattedAddress | Null | Every supported candidate | No |  |
| Hidden authority and authority-site identifiers | Null | Every supported candidate | No |  |
| Place, effective dates, DFF and localization segments | Null | Not supplied and no active context requires them | Yes |  |
| ORA_XLE_LEGAL_ENTITY_REGISTRATION_FUNCTION.csv candidate rows | Zero | Every supported candidate | No |  |

FormattedAddress is the exact active legal-address natural key. Leave LocationId, SourceId, JurisdictionId, authority IDs, audit fields, ESS fields, and object versions blank on CREATE. Never default RegistrationNumber; the supported deterministic CSV path requires explicit user input.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LER.APPLY_DEFAULTS | step | 40 | apply_default | applied->LER.ENFORCE_DESIGN;blocked->LER.HANDLE_ERROR | LER.CHECK_DEPENDENCIES | stop | After dependencies are ready |
