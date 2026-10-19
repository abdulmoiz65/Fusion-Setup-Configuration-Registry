# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| relatedItemType or cyclicRelationshipFlag is missing or invalid | Stop and request the precise missing or invalid value. |
| cyclicRelationshipFlag is not true or false | Stop before source preparation. Do not coerce Y, N, 1, 0, blank, or another non-Boolean value. |
| The collection lookup finds no exact record or more than one exact record | Stop before preview; do not choose a record. |
| Fusion rejects the read-only lookup | Stop, classify the response, and do not retry automatically. |
| Fusion reports that create is not enabled | Treat the prepared source as an invalid update action. Set RestAction to PATCH, revalidate the source, and obtain a new approval before resubmission. |
| A Data Loader PATCH returns Not Found for a relatedItemType meaning | Treat this as an invalid source identity mapping. Do not retry or resubmit the archive. Resolve the meaning through EGP_RELATIONSHIP_TYPES, rebuild the source row with its LookupCode, validate, and obtain fresh approval. |
| The PATCH row lacks, alters, or reuses the resolved LookupCode | Stop as an input-validation or lookup-contract failure. Repeat the EGP_RELATIONSHIP_TYPES meaning-to-code lookup, then rebuild the relatedItemType source value from its LookupCode. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Existing record identity is unresolved, missing, or ambiguous | Do not prepare an update, generate a hash key, substitute another record, or submit a write. |
| A requested update includes undocumented fields | Do not include those fields in the cyclic-relationship update. |
| RestAction is blank or create-oriented | Do not upload or initiate the source as an update. |
| The relatedItemType source value is a meaning instead of the resolved LookupCode | Do not submit the archive. Replace the source value using the exact EGP_RELATIONSHIP_TYPES lookup mapping and obtain a fresh approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIT.HANDLE_ISSUE | step | 50 | error_handler | disclosed->RETURN_ISSUES | none | stop | Prior node reports invalid input, an unresolved identity, or a lookup failure |
| RIT.DONE | terminal | 60 | terminal | none | RIT.ENFORCE_UPDATE | stop | Update request passed all documented authoring gates |
| RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Error disclosure complete |
