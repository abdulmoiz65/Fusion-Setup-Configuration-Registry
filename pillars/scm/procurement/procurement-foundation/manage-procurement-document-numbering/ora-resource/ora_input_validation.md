# Input Validation

Use this guidance with the Procurement Document Numbering REST/Data Loader contract documented by Oracle for release 26c and the implementation guidance supplied for this task.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Document-numbering identity | Document Type, Determinant Type, and Determinant Value | Stop the affected row | Provide all three values; use LegalEntityName as the Determinant Value for Purchase Order and BusinessUnitName for every other Document Type | Every Data Loader row | |
| Numbering definition | CurrentMaximumUniqueIdentifier, Prefix, Suffix, and MinimumDigits as applicable to the requested numbering scheme | Stop the affected row | Provide the intended next number and any applicable format values before preview | Every Data Loader row | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Determinant Value source follows Document Type | For Document Type Purchase Order, send LegalEntityName as the Data Loader Determinant Value. For every other Document Type, send BusinessUnitName as the Data Loader Determinant Value. Do not substitute the other name field. | Every Data Loader row | |
| DocumentNumberId is not supplied as an invented value | Derive DocumentNumberId through the documented surrogate user key derivation query before choosing the Data Loader operation. | Every Data Loader row | derive_document_number_id_by_surrogate_user_key |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PDN.VALIDATE_INPUT | step | 10 | validate_input | valid->PDN.DERIVE_DOCUMENT_NUMBER_ID;invalid->RETURN_ISSUES | none | stop | Every requested Data Loader row |
