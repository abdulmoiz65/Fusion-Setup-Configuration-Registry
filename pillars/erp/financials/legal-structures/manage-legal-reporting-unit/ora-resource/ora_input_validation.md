# Manage Legal Reporting Unit Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parent and identity | LegalEntityIdentifier or exact entity name; LegalReportingUnitName; country name or two-letter code | Block before preview | Resolve one effective parent and one active country geography receipt | Always | resolve_lru_country_geography |
| Optional jurisdiction | Explicit jurisdiction name or search text | Treat omitted or blank jurisdiction as null; do not look it up or default it | Resolve supplied jurisdiction without an identifying-only restriction | Only when jurisdiction is supplied | resolve_lru_jurisdiction |
| Conditional registration child | RegistrationNumber and legal-address selection | Ask for missing number/address only when jurisdiction is supplied | Resolve the exact jurisdiction name and one address from the scoped export | Explicit jurisdiction is supplied | resolve_lru_registration_address |
| Main designation | MainEstablishmentFlag and complete sibling/main-history evidence when Y | Block Y until overlap can be disproved | Verify every sibling LRU and historical main period under the parent | MainEstablishmentFlag is Y | verify_lru_main_history |
| Supported child scope | No authority or function input | Block candidate as unsupported | Remove supplied authority/function values and add zero function rows; preserve existing unrelated rows | Authority or function input is supplied |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Parent input is present | Continue only with one exact effective legal entity | Use its identifier as the child natural key and include unchanged parent row when hierarchy requires it | verify_lru_parent_entity |
| Country input is present | Continue only with one enabled territory and one unambiguous effective primary COUNTRY result from addressGeographies | Build persistent and transient country carriers; GeographyId is not a required lookup output | resolve_lru_country_geography |
| Jurisdiction is omitted or blank and no registration details are supplied | Continue with null jurisdiction and no new registration child | Skip jurisdiction and registration-address resolution even if the UI would default a jurisdiction |  |
| Jurisdiction is explicitly supplied | Continue only after one effective candidate is selected and its import name is unambiguous | Accept identifying or non-identifying jurisdictions; do not validate jurisdiction-to-LRU-geography association in this scope | resolve_lru_jurisdiction |
| Registration number or address is supplied without jurisdiction | Input is incomplete | Ask the user to supply the intended jurisdiction or explicitly remove the registration details; do not infer or silently discard them |  |
| Registration child applies | Continue only with an explicit number and one exact exported address passing the documented eligibility checks | Author the complete child or none; keep LocationId blank | resolve_lru_registration_address |
| Main flag is Y | Continue only when complete target history proves no overlapping main interval | Retain validated main-effective dates | verify_lru_main_history |
| Function text or code is supplied | The enabled lookup may identify ICINV, ITC, DAS2, or SITC, but the candidate remains unsupported | Remove the supplied function and add zero function rows; preserve existing unrelated rows | resolve_lru_enabled_function_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Required inputs | Reject blank parent, LRU name, or country; reject name over 240 | Always |  |
| Country-only geography | Require GeographyCode as country code; GeographyName and GeographyElement1 as country name; GeographyType COUNTRY; GeographyUse MASTER_REF; elements2-10 null; matching transients; GeographyId receipt-only | Always | resolve_lru_country_geography |
| Non-country geography | Return Unsupported Scope for STATE, COUNTY, CITY, POSTAL_CODE, or another non-country type. Do not convert it to its containing country or blank its code to bypass this gate; blank-code import with a complete hierarchy remains unvalidated | Any non-country input |  |
| Main designation | Accept only Y or N; default N. When Y, reject incomplete history, invalid dates, or overlap | Main selection | verify_lru_main_history |
| Conditional child completeness | Require selected jurisdiction, explicit RegistrationNumber of at most 30 characters, and one exported FormattedAddress; emit exactly one complete new registration for the new LRU | Explicit jurisdiction is supplied | resolve_lru_jurisdiction |
| Effective dates | Reject malformed or inverted supplied intervals; use the workflow as-of date consistently for reference eligibility, with null boundaries open | Dates are supplied or reference eligibility is checked |  |
| Authority and functions | Require PartyName, IssuingFormattedAddress, hidden authority/site values null and ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION_FUNCTION.csv zero candidate rows | Child applies | resolve_lru_enabled_function_code |
| System ownership | Keep GeographyId, LocationId, SourceId, authority IDs, audit, ESS, and object-version values blank on CREATE | Always |  |
| DFF and localization | Keep base values null unless a supplied or active runtime context requires exact segment validation | Context or segment supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.VALIDATE_INPUT | step | 10 | validate_input | valid->LRU.RESOLVE_REFERENCES;invalid->LRU.HANDLE_ERROR | none | stop | Before any lookup or package preview |
