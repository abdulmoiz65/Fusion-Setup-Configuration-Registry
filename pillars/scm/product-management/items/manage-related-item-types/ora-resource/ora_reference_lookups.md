# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_relationship_type_code_by_meaning | Before preparing an update for a related item type | relatedItemType meaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='EGP_RELATIONSHIP_TYPES'&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Trim outer whitespace and require exactly one case-insensitive exact Meaning match for lookup type EGP_RELATIONSHIP_TYPES. | relatedItemType Data Loader source value: LookupCode; normalized relatedItemType meaning | Zero or multiple Meaning matches block preview; do not fuzzy-match or select the first result. |
| find_related_item_type_by_exact_name | Before preparing an update for an existing related item type | relatedItemType meaning | /fscmRestApi/resources/11.13.18.05/relatedItemTypes?q=relatedItemType={relatedItemType} | relatedItemType, cyclicRelationshipFlag | Require exactly one returned record whose relatedItemType exactly equals the supplied meaning. | current cyclicRelationshipFlag and exact relatedItemType meaning | No exact record or more than one exact record blocks preview. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Collection lookup returns 401 or 403 | Stop as an authentication or privilege failure. |
| Collection lookup returns an incompatible response | Stop as a Fusion API contract failure; do not retry automatically. |
| Exact match is missing or ambiguous | Stop before preview and request a resolvable related item type. |

## Source

Oracle public REST documentation: https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-relateditemtypes-get.html and https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-relateditemtypes-relateditemtypesuniqid-patch.html

## PATCH Identity Handoff

| Handoff Fact | Required Behavior |
|---|---|
| Lookup input | Use the supplied relatedItemType meaning to resolve one lookup row in EGP_RELATIONSHIP_TYPES. |
| Data Loader source identity | Replace relatedItemType with the exact resolver-returned LookupCode for the PATCH row. |
| PATCH action | Set RestAction to PATCH. |
| Changed value | Send only cyclicRelationshipFlag with its normalized Boolean value. |
| Data Loader archive | The PATCH row uses the exact resolved LookupCode as the relatedItemType value; do not retain the supplied meaning in that field. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIT.RESOLVE_LOOKUP_CODE | decision | 20 | reference_lookup | resolved->RIT.FIND_EXISTING;not_found->RIT.HANDLE_ISSUE;ambiguous->RIT.HANDLE_ISSUE;lookup_failed->RIT.HANDLE_ISSUE | RIT.VALIDATE_INPUT | stop | Before preparing a Data Loader PATCH source for a related item type meaning |
| RIT.FIND_EXISTING | decision | 30 | reference_lookup | found->RIT.ENFORCE_UPDATE;not_found->RIT.HANDLE_ISSUE;ambiguous->RIT.HANDLE_ISSUE;lookup_failed->RIT.HANDLE_ISSUE | RIT.RESOLVE_LOOKUP_CODE | stop | Before preparing an update for an existing related item type |
