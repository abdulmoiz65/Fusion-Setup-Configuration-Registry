# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Existing definition matches | Report existing object and do not create duplicate |
| Existing definition differs | Identify differences and ask update versus new |
| Technical default unresolved | Stop before package generation |
| Import error | Persist diagnostics; never use failure as normal default discovery |
| Data Loader authentication or UCM authorization failure | Refresh the cached token once when the Data Loader contract permits it; on a repeated 401 or 403, stop with auth or authz diagnostics and do not fall back to a direct FSM import endpoint. |
| Data Loader upload or initiation failure | Preserve the approved package fingerprint, environment, Data Loader stage, and returned identifiers; correct the failure and require fresh validation and approval before another submission. |
| ModuleId missing or blank before package generation | Apply 47110F64AC0B08E2E040449823C60DB6, regenerate and validate the package, show the final value, and require fresh live-import approval. This identifier is used in every environment. |
| ModuleId differs from the approved value before package generation | Stop; replace it with 47110F64AC0B08E2E040449823C60DB6, regenerate and validate the package, show the final value, and require fresh live-import approval. |
| Import completed with ModuleId required error | Persist ProcessId, ProcessLog, target environment, affected rows, and zero or partial success counts; do not submit a dependent structure import or retry the failed package |
| ValueSetIdentifier missing | Default it to SegmentName, validate its identifier format locally, and show it in readiness before import |
| ValueSetIdentifier invalid | Stop; correct from user-provided SegmentName or an explicit valid user identifier; require fresh approval before a retry |
| COA segment value-set candidate is unresolved | Stop before package generation; identify the affected SegmentCode and whether the missing fact is candidate code, format, or MaximumLength. |
| Vague COA-creation request | Stop before value-set creation or artifact generation; return the proposed baseline and request COA identity, confirmation or revision, segment lengths, and any additional user-designed segments. Do not request or create segment values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAVS.GATE | step | 7 | error_handler | pass->COAVS.READY_IMPORT | COAVS.BULK | stop | Object absent |
| COAVS.READY_IMPORT | terminal | 8 | terminal | none | COAVS.GATE | stop | Readiness record passes |
| COAVS.DONE_MATCH | terminal | 9 | terminal | none | COAVS.LOOKUP | stop | Existing definition matches |
