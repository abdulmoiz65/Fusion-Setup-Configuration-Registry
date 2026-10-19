# Receiving Parameters Reference Lookups

## Live Lookups

| Resolver | Runs When | Lookup Source Values | Service Path or URL | Query or Match Rule | Fields to Request | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_receiving_parameter_standard_lookup | A supported field is supplied as a display `Meaning` rather than its backend code | Field-specific display value and its lookup type from the table below | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | Read-only GET filtered by the mapped `LookupType`; compare returned `Meaning` using trim plus case-insensitive exact matching. Require exactly one matching row. Never fuzzy-match or select the first result. | `LookupType`, `LookupCode`, `Meaning`, `Description`, and active/enabled status when returned | Store returned `LookupCode` in the mapped backend field; retain only sanitized lookup evidence. | Stop Data Loader handoff for zero or multiple exact matches, an inactive/disabled result where returned, a lookup read failure, or a conflicting supplied display value and code. |
| resolve_receiving_parameter_job_set | A Job Set is supplied as either its display name or its Job Set name | Supplied Job Set display name and/or Job Set name | `/fscmRestApi/resources/11.13.18.05/shippingDocumentJobSetsLOV?finder=findByProductCode;bindProductCode=RCV&onlyData=true` | Read-only GET scoped to product code `RCV`; compare the supplied value with returned `JobSetDisplayName` and `JobSetName`, using trim plus case-insensitive exact matching. Deduplicate a row matching both fields and require exactly one distinct matching row. Never fuzzy-match or select the first result. | `JobSetDisplayName`, `JobSetName`, `JobSetPackageName` | Store the matching row's canonical `JobSetName` in the backend field; retain `JobSetDisplayName` and `JobSetPackageName` only as sanitized lookup evidence. | Stop Data Loader handoff for zero or multiple distinct exact matches, a lookup read failure, or supplied display and Job Set names that resolve to different rows. |

## Supported Field Mappings

| Backend Field | Lookup Type | Display Attribute | Value Attribute |
|---|---|---|---|
| `ReceiptDaysExceedActionCode` | `RCV_RECEIVING_OPTION` | `Meaning` | `LookupCode` |
| `OverReceiptActionCode` | `RCV_RECEIVING_OPTION` | `Meaning` | `LookupCode` |
| `ShipToExceptionActionCode` | `RCV_RECEIVING_OPTION` | `Meaning` | `LookupCode` |
| `ASNControlActionCode` | `RCV_RECEIVING_OPTION` | `Meaning` | `LookupCode` |
| `ReceiptRoutingId` | `RCV_ROUTING_HEADERS` | `Meaning` | `LookupCode` |
| `RMAReceiptRoutingId` | `RCV_ROUTING_HEADERS` | `Meaning` | `LookupCode` |
| `ReceiptNumberGenerationCode` | `RCV_USER_DEF_RCPT_NUM_CODE` | `Meaning` | `LookupCode` |
| `ReceiptNumberTypeCode` | `RCV_MANUAL_RECEIPT_NUM_TYPE` | `Meaning` | `LookupCode` |
| `RMAValidateLotsCode` | `RCV_ENFORCE_RMA_LOT_NUM` | `Meaning` | `LookupCode` |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RCV_PARAMS.RESOLVE_STANDARD_LOOKUPS | step | 30 | reference_lookup | resolved->RCV_PARAMS.RESOLVE_JOB_SET;not-applicable->RCV_PARAMS.RESOLVE_JOB_SET;blocked->RCV_PARAMS.RETURN_ISSUES;failure->RCV_PARAMS.RETURN_ISSUES | RCV_PARAMS.CHECK_READINESS | stop | One or more supported standard lookup fields are supplied as display values. |
| RCV_PARAMS.RESOLVE_JOB_SET | step | 35 | reference_lookup | resolved->RCV_PARAMS.DATALOADER_HANDOFF;not-applicable->RCV_PARAMS.DATALOADER_HANDOFF;blocked->RCV_PARAMS.RETURN_ISSUES;failure->RCV_PARAMS.RETURN_ISSUES | RCV_PARAMS.RESOLVE_STANDARD_LOOKUPS | stop | A Job Set display name or Job Set name is supplied. |
