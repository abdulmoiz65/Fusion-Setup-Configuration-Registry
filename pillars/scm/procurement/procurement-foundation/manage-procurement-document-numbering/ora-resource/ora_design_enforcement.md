# Design Enforcement

Apply these gates before Data Loader preview. They define the selection of the Data Loader operation; they do not authorize a direct REST write.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate determinant source | Confirm the Determinant Value was selected from LegalEntityName only for Purchase Order, otherwise from BusinessUnitName. |
| 2 | Derive identifier | Run derive_document_number_id_by_surrogate_user_key and require zero or one matching row. |
| 3 | Route operation | Route a row with no DocumentNumberId to POST; route a row with an existing DocumentNumberId to PATCH using that returned identifier. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Document Type is Purchase Order | Error | derive_document_number_id_by_surrogate_user_key | The Data Loader Determinant Value is not LegalEntityName, or the lookup does not resolve a unique result | Send LegalEntityName as Determinant Value and correct the identity inputs before preview | Yes |
| Document Type is not Purchase Order | Error | derive_document_number_id_by_surrogate_user_key | The Data Loader Determinant Value is not BusinessUnitName, or the lookup does not resolve a unique result | Send BusinessUnitName as Determinant Value and correct the identity inputs before preview | Yes |
| No existing row is identified | Error | derive_document_number_id_by_surrogate_user_key | A PATCH operation is selected without a returned DocumentNumberId | Use POST and omit DocumentNumberId | Yes |
| An existing row is identified | Error | derive_document_number_id_by_surrogate_user_key | A POST operation is selected despite a returned DocumentNumberId | Use PATCH with the derived DocumentNumberId | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| derive_document_number_id_by_surrogate_user_key | Every validated Data Loader row | DocumentNumberId and match result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PDN.ENFORCE_OPERATION_ROUTE | decision | 30 | design_enforcement | post->PDN.DONE_POST_ROUTE;patch->PDN.DONE_PATCH_ROUTE;blocked->RETURN_ISSUES | PDN.DERIVE_DOCUMENT_NUMBER_ID | stop | Every row after DocumentNumberId derivation |
