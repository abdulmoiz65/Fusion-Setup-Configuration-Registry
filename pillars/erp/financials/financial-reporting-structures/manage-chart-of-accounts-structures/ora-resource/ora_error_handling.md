# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Existing definition matches | Report existing object and do not create duplicate |
| Existing definition differs | Identify differences and ask update versus new |
| Technical default unresolved | Stop before package generation |
| Explicit column/sequence mismatch | Preserve the supplied values, classify as warning, list the affected segment rows in import readiness, and ask for confirmation before package generation |
| SegmentIdentifier missing | Derive it from SegmentCode using the documented lowercase and special-character capitalization rule, then validate the result before package generation. |
| SegmentIdentifier cannot be derived | Stop before package generation when SegmentCode is blank or a special character isn't immediately followed by a letter. Request a corrected SegmentCode or an explicitly supplied identifier that satisfies the documented rule. |
| Essbase-incompatible segment name | Stop before package generation, identify the segment and offending whitespace or character rule, and require a corrected name followed by fresh validation. |
| Segment name matches a value | Stop before package generation, report the segment name and conflicting same-COA value using case-insensitive comparison, and require one of them to be changed. |
| FND-3043 segment identifier required | Persist ProcessId, request ID, ProcessLog, affected structure and segment, row and object counts, and post-failure lookup result. Invalidate the package approval and require corrected identifiers, validation, and fresh approval before retry. |
| Import error | Persist diagnostics; never use failure as normal default discovery |
| Data Loader authentication or UCM authorization failure | Refresh the cached token once when the Data Loader contract permits it; on a repeated 401 or 403, stop with auth or authz diagnostics and do not fall back to a direct FSM import endpoint. |
| Data Loader upload or initiation failure | Preserve the approved package fingerprint, environment, Data Loader stage, and returned identifiers; correct the failure and require fresh validation and approval before another submission. |
| Referenced value set unresolved | Stop before structure package generation; report every affected SegmentCode, candidate or supplied ValueSetCode, lookup result, and required compatible MaximumLength. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COASTR.GATE | step | 7 | error_handler | pass->COASTR.READY_IMPORT | COASTR.BULK | stop | Object absent |
| COASTR.READY_IMPORT | terminal | 8 | terminal | none | COASTR.GATE | stop | Readiness record passes |
| COASTR.DONE_MATCH | terminal | 9 | terminal | none | COASTR.LOOKUP | stop | Existing definition matches |
