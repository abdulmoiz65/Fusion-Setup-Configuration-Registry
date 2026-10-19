# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Existing definition matches | Report existing object and do not create duplicate |
| Existing definition differs | Identify differences and ask update versus new |
| Technical default unresolved | Stop before package generation |
| StructureInstanceIdentifier missing | Derive it from StructureInstanceCode using the documented first-letter capitalization and special-character normalization rule, then validate the result before package generation. |
| StructureInstanceIdentifier cannot be derived | Stop before package generation when StructureInstanceCode is blank or a special character isn't immediately followed by a letter. Request a corrected code or an explicitly supplied identifier that satisfies the documented rule. |
| Generated member-ID collision | Stop cube-ready approval, report the segment sequence and conflicting value, and require the value to be corrected before revalidation. |
| FND-3042 structure instance identifier required | Persist ProcessId, request ID, ProcessLog, affected instance, row and object counts, and post-failure lookup result. Invalidate the package approval and require a corrected identifier, validation, and fresh approval before retry. |
| Import error | Persist diagnostics; never use failure as normal default discovery |
| Data Loader authentication or UCM authorization failure | Refresh the cached token once when the Data Loader contract permits it; on a repeated 401 or 403, stop with auth or authz diagnostics and do not fall back to a direct FSM import endpoint. |
| Data Loader upload or initiation failure | Preserve the approved package fingerprint, environment, Data Loader stage, and returned identifiers; correct the failure and require fresh validation and approval before another submission. |
| Structure or referenced value set unresolved | Stop before instance package generation; report the missing structure identity or each affected SegmentCode and ValueSetCode with its lookup result. |
| Vague COA-creation request | Stop before structure-instance creation or artifact generation; return the proposed baseline and request COA identity, confirmation or revision, segment lengths, and any additional user-designed segments. Do not request or create segment values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAINS.GATE | step | 7 | error_handler | pass->COAINS.READY_IMPORT | COAINS.BULK | stop | Object absent |
| COAINS.READY_IMPORT | terminal | 8 | terminal | none | COAINS.GATE | stop | Readiness record passes |
| COAINS.DONE_MATCH | terminal | 9 | terminal | none | COAINS.LOOKUP | stop | Existing definition matches |
