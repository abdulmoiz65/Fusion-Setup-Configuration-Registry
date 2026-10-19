# Manage Legal Reporting Unit Registrations Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Two-level parent scope | LegalEntityIdentifier or exact entity name; LegalReportingUnitName | Block before preview | Resolve one exact effective entity and one exact effective LRU owned by it | Always | verify_lru_registration_parents |
| Registration identity | JurisdictionName, RegisteredName, RegistrationNumber, FormattedAddress | Block before preview | Resolve one active LRU-geography-compatible jurisdiction and one exact active internal legal address | Always | resolve_lru_registration_jurisdiction |
| Supported child scope | No authority or function input | Block candidate as unsupported | Remove authority/site fields, function display/code values, and every function candidate row | Always |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Parent inputs are present | Continue only with one exact effective entity and one exact effective LRU whose LegalEntityId matches | Retain both natural keys and include exact unchanged parent rows required by hierarchy | verify_lru_registration_parents |
| Jurisdiction free text is supplied | Continue only with one exact active/effective row compatible with LRU geography | Derive IdentifyingFlag, legislative context, and LRU registration type code; keep any separately evidenced localized UI label distinct | resolve_lru_registration_jurisdiction |
| Address free text is supplied | Continue only with one exact active internal address compatible with jurisdiction country | Write FormattedAddress and keep LocationId blank | resolve_lru_registration_address_exact |
| Candidate identity is complete | CREATE only when complete target scope has no same-LRU match or same jurisdiction/number collision across sibling LRUs under the entity | Reuse, decide update-versus-new, or block conflict | find_lru_registration_conflict |
| Function text or code is supplied | Enabled lookup may identify ICINV, ITC, DAS2, or SITC, but candidate remains unsupported | Remove the function and preserve zero child rows | resolve_lru_enabled_function_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Required values | Reject blank parent entity, parent LRU, jurisdiction, registered name, registration number, or formatted address | Always |  |
| Parent ownership | Reject an LRU belonging to another entity or an ambiguous global-name match | Always | verify_lru_registration_parents |
| Lengths and dates | Reject RegisteredName over 240, RegistrationNumber over 30, inverted dates, or dates outside parent LRU range | Applicable values supplied | verify_lru_registration_parents |
| Identifying state | Derive from jurisdiction; reject user override and block a second identifying row for the same LRU context | Always | find_lru_registration_conflict |
| Issuing authority | Reject any authority input; require PartyName, IssuingFormattedAddress, and hidden authority/site identifiers null | Always |  |
| Registration functions | Reject any function input or FunctionCode and require ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION_FUNCTION.csv zero candidate rows | Always | resolve_lru_enabled_function_code |
| System ownership | Keep LocationId, SourceId, JurisdictionId, parent physical IDs, authority IDs, audit, ESS, and object-version values blank on CREATE | Always |  |
| DFF and localization | Keep base values null unless a supplied or active runtime context requires exact segment validation | Context or segment supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUR.VALIDATE_INPUT | step | 10 | validate_input | valid->LRUR.RESOLVE_REFERENCES;invalid->LRUR.HANDLE_ERROR | none | stop | Before any lookup or package preview |
