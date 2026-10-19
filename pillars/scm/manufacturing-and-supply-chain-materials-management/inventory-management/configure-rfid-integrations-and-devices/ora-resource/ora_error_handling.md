# RFID Integrations and Devices Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A Device Type value is unsupported, ambiguous, or conflicts with a supplied code or display value | Classify as input validation, identify the field and supplied values, and stop before Data Loader handoff. |
| Event Type or Process Type has no exact standard-lookup result, more than one result, or conflicting code and meaning | Classify as input validation, retain the resolver evidence, and stop before Data Loader handoff. |
| The per-run metadata preflight cannot confirm inventoryRFIDConfigurations, inventoryRFIDDevices, or the processes child component | Classify as catalog or metadata mismatch and stop. Do not fall back to direct REST execution. |
| Cached authentication receives 401 or 403 | Refresh once through core authentication. A second authentication failure stops. |
| A read-only lookup has a transport or Fusion API failure | Preserve sanitized diagnostics and stop; retry only when the owning client declares the read recoverable. |

## Retry and Disclosure Rules

| Situation | Required Behavior |
|---|---|
| A Data Loader load, import, or live mutation is proposed | Do not retry, upload, or initiate without the separate Data Loader preview and approval workflow. |
| Diagnostics are reported | Redact credentials, tokens, private keys, opaque URLs, internal IDs, and sensitive payload values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RFID.HANDLE_ERROR | step | 7 | error_handler | stopped->RFID.BLOCKED | none | stop | Any prior node returns invalid, unresolved, failed, ambiguous, or unavailable |
| RFID.COMPLETE_PARENT | terminal | 8 | terminal | none | RFID.RESOLVE_DEVICE_TYPE | continue | Integration or Device input is resolved and no processes child row is supplied |
| RFID.COMPLETE_PROCESS | terminal | 9 | terminal | none | RFID.RESOLVE_PROCESS_TYPE | continue | Integration, Device, and every supplied processes child row are resolved |
| RFID.BLOCKED | terminal | 10 | terminal | none | none | stop | Corrected input, metadata, access, or lookup evidence is required |
