# Manage Legal Entity Registrations Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parent scope | LegalEntityIdentifier or exact legal-entity name | Block before preview | Resolve one exact effective legal entity and retain its identifier as the child natural key | Always | verify_registration_parent_entity |
| Registration identity | JurisdictionName, RegisteredName, RegistrationNumber, FormattedAddress | Block before preview | Resolve one active geography-compatible jurisdiction and one exact active internal legal address; user supplies name and number | Always | resolve_entity_registration_jurisdiction |
| Supported child scope | No authority input and no function input | Block candidate as unsupported | Remove PartyName, IssuingFormattedAddress, hidden authority/site values, function display/code values, and every function candidate row | Always |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Parent is supplied | Continue only with one exact effective entity and exact parent identifier | Include the exact unchanged current parent row when the package hierarchy requires it | verify_registration_parent_entity |
| Jurisdiction free text is supplied | Continue only with one exact active/effective compatible jurisdiction | Derive IdentifyingFlag, legislative context, and registration type code from the same receipt; keep any separately evidenced localized UI label distinct | resolve_entity_registration_jurisdiction |
| Address free text is supplied | Continue only with one exact active internal address compatible with the jurisdiction country | Write FormattedAddress natural key and keep LocationId blank | resolve_entity_registration_address |
| Candidate identity is complete | CREATE only when the complete target export shows no exact or conflicting parent/jurisdiction/number registration | Reuse, make an explicit update decision, or block ambiguity | find_entity_registration_conflict |
| Function text or code is supplied | The enabled code lookup may identify ICINV, ITC, DAS2, or SITC, but the candidate remains unsupported | Remove the function; do not create a child row | resolve_enabled_registration_function_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Required values | Reject blank-after-trim parent, jurisdiction, registered name, registration number, or formatted address | Always |  |
| Lengths | Reject RegisteredName over 240 or RegistrationNumber over 30; never truncate or rely on a generated SYS surrogate | Values supplied |  |
| Dates | Reject EffectiveFrom after EffectiveTo or a registration range outside the parent effective range | Dates supplied | verify_registration_parent_entity |
| Identifying state | Derive from jurisdiction; reject independent override and block a second identifying row for the same legal context | Always | find_entity_registration_conflict |
| Issuing authority | Reject any authority input; require PartyName, IssuingFormattedAddress, and hidden authority/site identifiers null | Always |  |
| Registration functions | Reject any function input or FunctionCode and require ORA_XLE_LEGAL_ENTITY_REGISTRATION_FUNCTION.csv to contain zero candidate rows | Always | resolve_enabled_registration_function_code |
| System ownership | Keep LocationId, SourceId, JurisdictionId, authority IDs, audit, ESS, and object-version values blank on CREATE | Always |  |
| DFF and localization | Keep base DFF/localization values null unless a supplied or active runtime context requires exact segment validation | Context or segment supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LER.VALIDATE_INPUT | step | 10 | validate_input | valid->LER.RESOLVE_REFERENCES;invalid->LER.HANDLE_ERROR | none | stop | Before any lookup or package preview |
