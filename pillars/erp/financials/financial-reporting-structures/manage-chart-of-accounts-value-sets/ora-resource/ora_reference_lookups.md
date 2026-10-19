# Reference Lookups

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_value_set | Before any FSM export, package, or create for every requested COA segment | Explicit ValueSetCode; otherwise SegmentCode_VS candidate | GET /fscmRestApi/resources/11.13.18.05/valueSets?q=ValueSetCode='{ValueSetCode}' | ValueSetId, ValueSetCode, ValidationType, ValueDataType, ValueSubtype, MaximumLength, UppercaseOnlyFlag, ZeroFillFlag, SecurityEnabledFlag | Exactly one matching ValueSetCode with compatible format and MaximumLength | Existing definition, ValueSetId, and verified ValueSetCode | If compatible, reuse it and skip the package row; on no result continue automatically to creation readiness; on a differing or ambiguous result stop |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAVS.LOOKUP | decision | 4 | reference_lookup | absent->COAVS.DEFAULT;match->COAVS.DONE_MATCH | COAVS.READY | stop | Always |
