# Selection Criteria Reference Lookups

## Source Boundary

This resource owns only read-only lookup mechanics for reviewing selection criteria. It uses the documented Oracle Procurement GET endpoints and does not authorize POST, PATCH, DELETE, or any other mutation.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_selection_criteria_by_identity | A current selection criterion is requested for review | Validated positive decimal SelectionId, exact RequisitioningBUName, or both | For SelectionId: GET /fscmRestApi/resources/11.13.18.05/externalPurchasePricesSelectionCriteria/{SelectionId}. For BU name without SelectionId: GET /fscmRestApi/resources/11.13.18.05/externalPurchasePricesSelectionCriteria with fields=SelectionId,RequisitioningBUName,RequisitioningBUId,RequisitioningBUGroupId,SourceContractType,SourceContractTypeCode,PartyType,PartyTypeCode,LowestPriceFlag,LastUpdateDate, onlyData=true, limit=500, and offset={offset}; add q=RequisitioningBUName='<exact name>' only when the name has no apostrophe, semicolon, or backslash. | SelectionId, RequisitioningBUName, RequisitioningBUId, RequisitioningBUGroupId, SourceContractType, SourceContractTypeCode, PartyType, PartyTypeCode, LowestPriceFlag, LastUpdateDate; for a collection, count and hasMore | Use core.fusion-api.rest-api-client with GET. For SelectionId, require the returned SelectionId to equal the validated ID and, when a BU name is also supplied, require the returned RequisitioningBUName to equal it exactly. For a BU-name-only read containing an apostrophe, semicolon, or backslash, omit q and inspect every paginated result; otherwise pass the quoted q literal through the core client's query encoder exactly once. Follow every page until hasMore=false and require exactly one record whose RequisitioningBUName exactly equals the unmodified supplied name. Never fuzzy-match or select the first result. | Current selection-criterion identity, scope indicators, source-type preference, party-type preference, lowest-price preference, and last-update timestamp | Zero exact matches after a complete collection read: report no caller-visible match without inferring BU access or global absence. Conflicting ID and BU name, multiple exact matches, incomplete pagination, malformed collection data, authentication or authorization failure, transport failure, or Fusion API failure: stop and report a sanitized diagnostic. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Neither SelectionId nor RequisitioningBUName is supplied | Stop before the GET and request at least one exact identity. |
| Both identities are supplied | Read by SelectionId, then require the returned RequisitioningBUName to exactly equal the supplied name; stop on a mismatch. |
| SelectionId is not a positive decimal integer | Stop before constructing an item path; request a valid SelectionId. |
| RequisitioningBUName contains an apostrophe, semicolon, or backslash | Omit the q filter, page through the visible collection, and compare the original complete name exactly. Do not escape or rewrite the name in a guessed query syntax. |
| The lookup returns one exact criterion | Return only the documented criterion fields and continue to the task-local review gates. |
| A complete collection lookup returns no exact criterion | Report that no matching criterion was visible to the caller; do not infer BU access, global absence, an all-BU criterion, or a replacement to create. |
| The lookup returns multiple exact matches or pagination is incomplete | Stop and report an ambiguous or incomplete read; do not select a record. |
| The REST read fails | Stop and return a sanitized authentication, authorization, transport, or Fusion API diagnostic. Do not substitute another workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPSEL.RESOLVE_CRITERIA | decision | 20 | reference_lookup | resolved->EPPSEL.CHECK_DEPENDENCIES;not_found->EPPSEL.RETURN_NOT_FOUND;blocked->EPPSEL.HANDLE_ERROR | EPPSEL.VALIDATE_INPUT | stop | A current criterion is requested by SelectionId or exact RequisitioningBUName |

## Oracle Sources

- [Oracle Procurement 26D: REST endpoints](https://docs.oracle.com/en/cloud/saas/procurement/26d/fapra/rest-endpoints.html) — selection-criteria collection and item GET paths.
- [Oracle Procurement REST API: Get all selection criteria](https://docs.oracle.com/en/cloud/saas/procurement/25d/fapra/op-externalpurchasepricesselectioncriteria-get.html) — query and response fields, including `count` and `hasMore`. Verify these field details against the target environment's release metadata before a live read.
