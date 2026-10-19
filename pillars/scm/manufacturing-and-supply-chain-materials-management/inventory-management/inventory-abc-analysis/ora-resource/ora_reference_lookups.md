# Inventory ABC Analysis Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood ABC Analysis service catalog | Confirms the standardLookupsLOV resource and Fusion REST version 11.13.18.05 |
| Redwood classification sets page and lookup action chains | Confirms Meaning as the display attribute, LookupCode as the value attribute, and the two LookupType contexts |
| User-approved resolver contracts | Limits the task to these two read-only resolvers |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| item_scope_lookup | abcClassifications includes an item-scope code, friendly value, or both | ContentScopeCode and friendly item-scope Meaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupType,Meaning,LookupCode&onlyData=true&q=LookupType='INV_ABC_ITEM_SCOPE' | LookupType, Meaning, LookupCode | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; all supplied representations must resolve to one row | ContentScopeCode: LookupCode | Stop on no match, ambiguity, or representations resolving to different rows |
| compile_type_lookup | abcClassifications includes a compile-type code, friendly value, or both | CompileTypeCode and friendly compile-type Meaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupType,Meaning,LookupCode&onlyData=true&q=LookupType='INV_ABC_COMPILE_TYPE' | LookupType, Meaning, LookupCode | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; all supplied representations must resolve to one row | CompileTypeCode: LookupCode | Stop on no match, ambiguity, or representations resolving to different rows |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Any code or friendly value is supplied | Run only the resolver documented for that field; do not trust a supplied canonical code without validating it |
| Lookup returns one exact matched row | Fill the documented canonical code and retain the returned system values in the result |
| Code and friendly value are both supplied | Accept them only when both match the same returned row |
| Lookup returns no or multiple exact matches | Stop and request a valid, unambiguous value; never fuzzy-match or select the first result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABC.RESOLVE_ITEM_SCOPE | step | 40 | reference_lookup | resolved->ABC.RESOLVE_COMPILE_TYPE;skipped->ABC.RESOLVE_COMPILE_TYPE;blocked->ABC.HANDLE_ERROR | ABC.CHECK_READINESS | stop | An item-scope code or friendly value is supplied for abcClassifications |
| ABC.RESOLVE_COMPILE_TYPE | step | 50 | reference_lookup | resolved->ABC.DATA_LOADER_HANDOFF;skipped->ABC.DATA_LOADER_HANDOFF;blocked->ABC.HANDLE_ERROR | ABC.RESOLVE_ITEM_SCOPE | stop | A compile-type code or friendly value is supplied for abcClassifications |
