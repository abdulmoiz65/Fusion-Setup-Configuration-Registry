# Reference Lookups

The lookup below is read-only. Oracle documents the Procurement Document Numbering collection at /fscmRestApi/resources/11.13.18.05/procurementDocumentNumberings and identifies DocumentNumberId as the item identifier.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| derive_document_number_id_by_surrogate_user_key | After row validation and before operation routing | Document Type, Determinant Type, and Data Loader Determinant Value | GET /fscmRestApi/resources/11.13.18.05/procurementDocumentNumberings using the configured surrogate user key derivation query | DocumentNumberId, DocumentType, DeterminantType, BusinessUnitName, LegalEntityName | Match exactly one row using the surrogate user key derivation query. The Data Loader Determinant Value is LegalEntityName for Purchase Order; otherwise it is BusinessUnitName. | DocumentNumberId: DocumentNumberId; ExistingRow: match result | No match: leave DocumentNumberId absent and route the row to POST. Many matches: stop the row and resolve the ambiguous surrogate user key. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exactly one existing row is found | Retain the returned DocumentNumberId and make it available to the operation-routing design gate. |
| No existing row is found | Treat the row as new; do not manufacture DocumentNumberId. |
| The query returns more than one row | Block the row; correct the identity values or the configured surrogate user key derivation query before preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PDN.DERIVE_DOCUMENT_NUMBER_ID | decision | 20 | reference_lookup | found->PDN.ENFORCE_OPERATION_ROUTE;not_found->PDN.ENFORCE_OPERATION_ROUTE;ambiguous->RETURN_ISSUES | PDN.VALIDATE_INPUT | stop | Every validated Data Loader row |
