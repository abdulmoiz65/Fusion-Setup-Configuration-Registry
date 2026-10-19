# Configure Barcode Formats Error Handling

## Error Handling Rules

| Situation | What Happens |
|---|---|
| A selected FieldCode or FieldName, DataLengthType or DataLengthTypeName, or DataType or DataTypeName value has no exact match | Stop before Data Loader handoff and request a valid LookupCode or Meaning for the selected lookup type. |
| A selected FieldCode or FieldName, DataLengthType or DataLengthTypeName, or DataType or DataTypeName value is ambiguous | Stop before Data Loader handoff; do not select a candidate automatically. |
| Supplied code and meaning representations resolve to different rows | Stop before Data Loader handoff and request one authoritative representation or a matching pair. |
| The client-side DateFormat syntax is invalid | Stop before Data Loader handoff and request a pattern using only the supported tokens and separators. |
| A supplied Status or switch-backed field uses an unsupported representation | Stop before Data Loader handoff and request true, false, yes, no, y, or n; Status additionally accepts active or inactive. Do not coerce arbitrary text. |
| A required per-run BO metadata preflight fails or the registered BO is unavailable | Stop before Data Loader handoff; record the selected environment identifier, BO name, result, and sanitized diagnostic in the task validation artifact and skill-run record; do not fall back to direct REST write guidance. |
| Data Loader rejects prepared data | Preserve the Data Loader status, row identity, failure class, and sanitized message. Retain the resolved LookupCode and Meaning evidence for FieldCode, DataLengthType, or DataType; Data Loader and Fusion own backend validation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Client syntax validation | DateFormat contains an unsupported token or separator | Provide a blank DateFormat or a supported pattern. |
| Lookup no match | An exact LookupCode-or-Meaning lookup returns no item | Provide a valid LookupCode or Meaning for the selected lookup type. |
| Lookup ambiguity | An exact LookupCode-or-Meaning lookup returns multiple items | Provide a more precise value. |
| Conflicting lookup representations | Supplied code and meaning representations resolve to different rows | Provide one authoritative representation or a matching pair. |
| Switch/status normalization | A supplied Status or supported switch field is not an approved enabled or disabled representation | Provide an approved representation; for Status, active or inactive is also accepted. |
| BO visibility preflight | The selected environment does not expose inventoryBarcodeFormats or the read-only metadata check fails | Verify registration and selected-environment access, then run a new preflight before retrying. |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct the source data using the returned diagnostic. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup is missing or ambiguous | Do not fuzzy-match, guess, or select the first candidate. |
| Data Loader reports an uncertain failure | Do not resubmit until status and read-only verification clarify the outcome. |
| Metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BCF.DATA_LOADER_HANDOFF | decision | 70 | execution_gate | ready->BCF.DONE;blocked->BCF.HANDLE_ERROR;failure->BCF.HANDLE_ERROR | BCF.RESOLVE_DATA_TYPE | stop | Before handing validated data to core.data-loader for inventoryBarcodeFormats |
| BCF.HANDLE_ERROR | step | 80 | error_handler | handled->BCF.RETURN_ISSUES | none | stop | Any approved validation, defaulting, lookup, readiness, or Data Loader issue |
| BCF.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| BCF.DONE | terminal | 100 | terminal | none | BCF.DATA_LOADER_HANDOFF | stop | Local task rules passed; Data Loader owns final validation and execution |
