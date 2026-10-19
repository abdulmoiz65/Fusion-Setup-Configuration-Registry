# Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_print_orientation | PrintOrientationCode is supplied by meaning or code | Meaning, LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_WSH_DOC_ORIENTATION'&fields=Meaning,LookupCode&onlyData=true | Meaning, LookupCode | Trimmed case-insensitive exact match; supplied meaning and code must resolve to one row | PrintOrientationCode=LookupCode | Stop |
| resolve_print_side | PrintSideCode is supplied by meaning or code | Meaning, LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_WSH_DOC_PRINT_SIDE_TYPE'&fields=Meaning,LookupCode&onlyData=true | Meaning, LookupCode | Trimmed case-insensitive exact match; supplied meaning and code must resolve to one row | PrintSideCode=LookupCode | Stop |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SDOP.LOOKUP_ORIENTATION | step | 2 | reference_lookup | side_supplied->SDOP.LOOKUP_SIDE;no_print_side->SDOP.DONE | SDOP.VALIDATE_INPUT | stop | Print orientation is supplied |
| SDOP.LOOKUP_SIDE | step | 3 | reference_lookup | resolved->SDOP.DONE | SDOP.VALIDATE_INPUT | stop | Print side is supplied |
