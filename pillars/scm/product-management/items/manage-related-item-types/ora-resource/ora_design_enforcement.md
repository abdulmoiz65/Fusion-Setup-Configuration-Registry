# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate and normalize requested values | Confirm the relationship type is supplied and normalize cyclicRelationshipFlag to Boolean true or false. |
| 2 | Resolve relationship type code | Use lookup type EGP_RELATIONSHIP_TYPES to map the supplied meaning to one exact LookupCode. |
| 3 | Bind code to the Data Loader row | Replace the supplied meaning with the resolved LookupCode in relatedItemType and set RestAction to PATCH. |
| 4 | Restrict the change | Prepare a PATCH row that changes only cyclicRelationshipFlag for the resolved record. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Updating a related item type cyclic relationship setting | Blocking | find_related_item_type_by_exact_name | The supplied related item type does not resolve to exactly one record. | Resolve the exact existing record before preview. | Yes |
| Updating a related item type cyclic relationship setting | Blocking | find_related_item_type_by_exact_name | The update contains a field other than cyclicRelationshipFlag or its input cannot normalize to Boolean true or false. | Limit the update to cyclicRelationshipFlag. Supply true or false; source preparation must use the normalized Boolean value. | Yes |
| Updating an existing related item type through Data Loader REST |  Blocking |  | RestAction is blank or is not PATCH. relatedItemTypes does not support a create action for this modification. | Set RestAction to PATCH and prepare a new immutable preview. | Yes |
| Updating an existing related item type through Data Loader REST | Blocking | resolve_relationship_type_code_by_meaning | The Data Loader relatedItemType field is not the exact resolved LookupCode, or RestAction is not PATCH. | Rebuild the source row with relatedItemType mapped to the exact lookup code and RestAction set to PATCH. | Yes |
| Executing the Related Item Types PATCH | Blocking | resolve_relationship_type_code_by_meaning | The row includes the supplied meaning, an altered LookupCode, an additional identity field, or a field other than cyclicRelationshipFlag. | Rebuild the row from the exact lookup-code result and send only the normalized Boolean cyclicRelationshipFlag change. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_relationship_type_code_by_meaning | Before any update preview | relatedItemType source identity from LookupCode, lookup type EGP_RELATIONSHIP_TYPES, and exact supplied meaning | ora_reference_lookups.md |
| find_related_item_type_by_exact_name | Before any update preview | current cyclicRelationshipFlag and exact relatedItemType meaning | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIT.ENFORCE_UPDATE | decision | 40 | design_enforcement | allowed->RIT.DONE;blocked->RIT.HANDLE_ISSUE | RIT.FIND_EXISTING | stop | Existing related item type identity and lookup code are resolved |
