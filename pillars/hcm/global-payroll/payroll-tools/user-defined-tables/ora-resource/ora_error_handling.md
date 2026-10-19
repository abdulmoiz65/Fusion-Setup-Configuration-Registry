# User-Defined Tables HDL Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required table, column, row, cell-value, or effective-date field is missing | Stop before preview; identify the exact missing field and request a corrected HDL source. |
| Matched and range row attributes are mixed | Stop before preview; require one consistent row model and a corrected source. |
| A supplied validation formula violates the documented User Table Validation contract | Stop before preview; correct the formula input or required return result. |
| Flex-context identifiers disagree or flex attributes are supplied for a no-flex load | Stop before preview; correct the variant selection, context code, or context-qualified segment columns. |
| An operation other than source-confirmed MERGE is requested | Stop before preview; report that the operation is outside this reviewed resource contract until support is confirmed and authored. |
| The requested route is not core.data-loader with HDL | Stop before any Fusion interaction; return an approval blocker and restart through the required Data Loader route. |
| Core Data Loader validation, preview, approval, upload, or initiation fails or is uncertain | Preserve safe diagnostics, stop, and do not retry an upload or initiation automatically. |
| Loading produces a failed or timed-out process | Preserve the process status and log when available; report the last status and safe next-check path without resubmitting. |
| A required table name, range-or-match value, unit of measure, range bound, or exact match value is missing | Stop before preview; identify the missing field and the table or row record that requires it. |
| A range table does not use Number as its unit of measure | Stop before preview; require UserKeyUnits N for the range table. |
| A supplied flex field is not defined for the selected context | Stop before preview; identify the field and context and require a valid context segment. |
| An update or correct action changes an immutable table-level attribute | Stop before preview; preserve the current name, legislative data group, range-or-match value, unit of measure, and context. Permit only the row-title change. |
| An action targets a predefined user-defined table | Stop before preview; report that predefined user-defined tables do not permit actions. |
| UserTableCode is absent but UserTableName or Name is supplied | Do not stop, pause, prompt, or perform a Fusion lookup; copy the supplied name exactly into UserTableCode and continue DAT preparation. |
| A separately supplied UserTableCode differs from UserTableName or Name | Do not use the mismatched value; normalize UserTableCode to the supplied name exactly and continue without requesting confirmation. |
| UserTableName and Name are both absent when UserTableCode must be prepared | Stop before DAT generation and identify the missing name; do not fabricate a name or code. |
| SourceSystemOwner or SourceSystemId is present in prepared DAT content | Remove the fields from the DAT header and records, or clear their values when omission is not possible; re-run the final integrity check before handoff. |
| Final DAT integrity verification fails | Stop before preview or upload; report each code-to-name mismatch and each populated source-system field. |
| A describe response is unavailable or incomplete | Stop REST metadata mapping; identify the resource and each missing attribute, data type, requiredness rule, validation, accepted value, format, length, reference or LOV dependency, or finder contract. Do not infer missing metadata. |
| A required finder input is missing | Stop the read-only lookup and identify the missing LegislativeDataGroupId, UserTableName search text, UserTableId, context, or metadata-derived finder expression. |
| A row-flex attribute has lov metadata but its lovResourcePath filter is absent or cannot produce one finder expression | Stop value resolution; identify the flex field and context and do not invent a finder expression. |
| A REST lookup returns zero or multiple exact matches | Stop mapping; report the resource, finder, supplied identity, and match count without selecting a value automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required HDL field, row model, date, flex-context contract, operation, or formula contract is invalid | Correct the source and revalidate. |
| approval_blocker | The Data Loader route, immutable preview, or exact approval is missing or stale | Prepare the required Data Loader preview and obtain approval before the load. |
| process_failed | The Data Loader process ends with errors | Preserve available process diagnostics and correct the source before a separately approved retry. |
| process_timeout | The Data Loader process remains nonterminal after its wait window | Retain the process identity and check its status; do not resubmit. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| HDL preview | Task code, business object, target environment, source identity, intended matched or range model, and immutable approval artifact details. |
| Data Loader failure | Failure class, business stage, safe status summary, and one safe next action. |
| Timeout | Task code, process identity, last status, elapsed wait, and next-check guidance. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Direct Fusion API or manual UI route is proposed for setup-data loading | Do not create a substitute payload or load data through that route. |
| Preview or approval is missing, changed, or stale | Do not upload or initiate the HDL archive. |
| Upload or initiation result is uncertain | Do not repeat the operation automatically. |
| Process failure or timeout | Do not treat it as success or submit a replacement load without reconciliation and new approval. |
| Predefined resolves to Y | Do not prepare, upload, initiate, or otherwise perform any action for that user-defined table. |
| UserTableCode is not identical to its corresponding supplied name | Do not hand off, package, preview, or upload the DAT file until UserTableCode is normalized to the exact name. |
| SourceSystemOwner or SourceSystemId is populated | Do not hand off, package, preview, or upload the DAT file until both fields are omitted or unpopulated. |
| Describe metadata required for mapping is unresolved | Do not claim that the REST attribute inventory, validation contract, or finder inventory is complete. |
| Flex LOV finder cannot be derived from that attribute's describe metadata | Do not call the flex value-set endpoint with an invented, copied, or guessed finder expression. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UDT.EXECUTION_GATE | decision | 6 | execution_gate | ready->UDT.READY;blocked->UDT.RETURN_ISSUES | UDT.RESOLVE_REFERENCES | stop | Confirm the validated source will use core.data-loader and has the required preview and approval before a Fusion load. |
| UDT.READY | terminal | 7 | terminal | none | UDT.EXECUTION_GATE | continue | The HDL UserDefinedTable source is ready for its owning Core Data Loader workflow. |
| UDT.RETURN_ISSUES | terminal | 8 | terminal | none | none | continue | Input, dependency, design, routing, approval, or processing readiness is blocked. |

## Sources

- Developer-provided Resolve code from name and Strict Instructions for UserTableCode and source-system fields in the current request.
- Developer-provided primary REST endpoints, describe endpoints, finder variants, response mappings, contextual-flex describe flow, and flex value-set LOV contract in the current request.
