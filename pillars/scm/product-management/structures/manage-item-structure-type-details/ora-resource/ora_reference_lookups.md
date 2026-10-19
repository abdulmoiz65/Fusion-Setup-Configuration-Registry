# Reference Lookups

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_rd_range_indicator_lookup_value | A Reference Designator Range Indicator value is supplied or a range is requested | Lookup Type ORA_EGP_COMP_REF_DES_RANGE_IND; requested indicator lookup code or meaning | GET /fscmRestApi/resources/11.13.18.05/standardLookups/ORA_EGP_COMP_REF_DES_RANGE_IND/child/lookupCodes?limit=500 | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Match the lookup type exactly. Match the requested code or meaning to exactly one enabled, effective lookup value. None is the default | Validated Reference Designator Range Indicator lookup code and meaning | Stop before validation and request another value when the supplied value is outside ORA_EGP_COMP_REF_DES_RANGE_IND, inactive, ineffective, or ambiguously matched |

## Valid Target-Environment Values

The following enabled values were retrieved from the configured environment. Query the documented endpoint at validation time because lookup status can change.

| Lookup Code | Meaning | Enabled | Start Date | End Date |
|---|---|---|---|---|
| ORA_DASH | - | Y | 1959-01-01 | |
| ORA_BANG | ! | Y | 1959-01-01 | |
| ORA_AT | @ | Y | 1959-01-01 | |
| ORA_HASH | # | Y | 1959-01-01 | |
| ORA_DOLLAR | $ | Y | 1959-01-01 | |
| ORA_PERCENTAGE | % | Y | 1959-01-01 | |
| ORA_CARET | ^ | Y | 1959-01-01 | |
| ORA_AMPERSAND | & | Y | 1959-01-01 | |
| ORA_ASTERISK | * | Y | 1959-01-01 | |
| ORA_PLUS | + | Y | 1959-01-01 | |
| ORA_COLON | : | Y | 1959-01-01 | |
| ORA_SEMICOLON | ; | Y | 1959-01-01 | |
| ORA_NONE | None | Y | 1959-01-01 | |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The requested indicator is None | Accept only the enabled, effective None value from lookup type ORA_EGP_COMP_REF_DES_RANGE_IND and retain side-panel reference-designator maintenance behavior |
| Hyphen is selected | Resolve display value - to lookup code ORA_DASH and validate it is enabled and effective |
| A special character other than hyphen is selected | Validate it is an enabled, effective value from lookup type ORA_EGP_COMP_REF_DES_RANGE_IND |
| Import, REST, or SOAP enters reference designators using a range | Do not expect range expansion or collapse from the client; provide individual values or handle the range in a supported user interface |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| STRUCTURE_DETAILS.RESOLVE_RD_RANGE_INDICATOR | decision | 20 | reference_lookup | resolved->STRUCTURE_DETAILS.ENFORCE_DESIGN;not-required->STRUCTURE_DETAILS.ENFORCE_DESIGN;invalid->STRUCTURE_DETAILS.INVALID_REQUEST | STRUCTURE_DETAILS.VALIDATE_REQUEST | stop | A Reference Designator Range Indicator value or reference-designator range is requested |
