# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Related item type update request | relatedItemType, RestAction=PATCH, cyclicRelationshipFlag | Block | Provide the exact related item type, PATCH action, and a cyclic relationship value that can normalize to Boolean true or false. | Before a related item type update | find_related_item_type_by_exact_name |
| Relationship type lookup-code handoff | relatedItemType mapped from the exact `LookupCode` result for lookup type EGP_RELATIONSHIP_TYPES | Block | Run the meaning-to-code resolver and replace the supplied meaning with its returned LookupCode in the relatedItemType Data Loader source field. | Before a PATCH preview or execution | resolve_relationship_type_code_by_meaning |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| cyclicRelationshipFlag normalizes to Boolean true or false | Normalize the case-insensitive literals true and false to Boolean true and false before source preparation. Reject blank, Y, N, 1, 0, and any other value. | A cyclic relationship setting is supplied |  |
| relatedItemType is supplied as an exact relationship-type value | Stop and request the exact type value. | A related item type update is requested |  |
| RestAction is exactly PATCH | Stop before preview. Blank or create actions are not valid for Related Item Types modifications. | A related item type update is requested |  |
| relatedItemType is populated from the resolved LookupCode | Stop if a prepared Data Loader row uses the supplied meaning instead of the exact resolver-returned LookupCode. The meaning is lookup input only. | A PATCH is prepared | resolve_relationship_type_code_by_meaning |
| LookupCode is preserved exactly | Stop if the resolved code is missing, altered, reused for a different lookup type, or included as an additional source field. | A PATCH is prepared | resolve_relationship_type_code_by_meaning |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIT.VALIDATE_INPUT | decision | 10 | validate_input | valid->RIT.RESOLVE_LOOKUP_CODE;invalid->RIT.HANDLE_ISSUE | none | stop | Before a related item type update |
