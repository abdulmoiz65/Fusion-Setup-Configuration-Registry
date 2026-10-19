# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Parent or child required group is incomplete | Stop and identify the missing parent or child fields. |
| A child record has neither BalanceId nor BalanceCode with LegislativeDataGroupName | Stop and require one documented parent-key option. |
| A source-system identifier is absent from a direct ID-based record | Continue; SourceSystemOwner and SourceSystemId are optional. |
| A reference lookup has no match or many matches | Stop and report the supplied field and value; do not select a match automatically. |
| Target metadata or lookup contract is TBD | Stop before HDL preparation; obtain the View Business Objects export or approved documented contract. |
| A design gate fails | Stop preview and identify the exact LDG, category, dimension, feed, linkage, or file-splitting condition to correct. |
| HDL import fails | Preserve the import diagnostics, correct only rejected records, and do not retry a live import without idempotency or explicit approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required inputs are absent or a child has no documented parent key | Correct the field set and rerun validation. |
| Catalog mismatch | A target-LDG category, dimension, context, element, input value, or classification is invalid | Correct the LDG-scoped value or select a valid target value. |
| Metadata blocker | Required target business-object metadata is unavailable or incomplete | Export and verify target metadata before preparing HDL. |
| Lookup or transport or authorization or Fusion API | A read-only lookup cannot establish exactly one value | Stop before retry and resolve the sanitized diagnostic. |
| Design blocker | A balance, feed, linkage, or seeded/custom file design rule is violated | Correct the design and rerun the applicable gates. |
| Approval blocker | Import is requested without approval bound to the exact artifact and environment | Obtain immediate explicit approval. |
| Process failed | An HDL import reports rejected records or process failure | Preserve diagnostics and correct rejected records before a separately approved retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup or metadata failure | Target environment, resolver purpose, failure class, sanitized message, and safe next action. |
| Design blocker | Affected balance component, LDG, blocking condition, and correction required. |
| Import approval | Exact target environment, intended import operation, and immutable HDL artifact reference. |
| HDL process failure | Environment, operation, process identifier when available, last status, diagnostics reference, and next safe action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Metadata or lookup contract is missing | Do not invent field requirements, endpoints, or lookup results. |
| Lookup has no unique result | Do not select a reference value automatically. |
| Direct BalanceId or BalanceCode with LDG is available | Do not require SourceSystemOwner or SourceSystemId. |
| Live import has not been explicitly approved | Do not upload or submit the HDL file. |
| HDL import outcome is uncertain or failed | Do not retry automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BAL.GATE_HDL_IMPORT | decision | 50 | execution_gate | ready_for_approved_import->BAL.DONE_READY;approval_or_readiness_missing->BAL.HANDLE_APPROVAL_BLOCKER | BAL.ENFORCE_DESIGN | stop | A validated HDL artifact is prepared for import |
| BAL.HANDLE_INPUT_ERROR | step | 60 | error_handler | handled->BAL.RETURN_ISSUES | BAL.VALIDATE_INPUT | stop | Input validation is invalid |
| BAL.HANDLE_LOOKUP_ERROR | step | 70 | error_handler | handled->BAL.RETURN_ISSUES | BAL.LOOKUP_EXISTING | stop | The existing-balance lookup fails |
| BAL.HANDLE_DEPENDENCY_ERROR | step | 80 | error_handler | handled->BAL.RETURN_ISSUES | BAL.RESOLVE_DEPENDENCIES | stop | A required dependency is blocked |
| BAL.HANDLE_DESIGN_BLOCKER | step | 90 | error_handler | handled->BAL.RETURN_ISSUES | BAL.ENFORCE_DESIGN | stop | A design rule blocks the request |
| BAL.HANDLE_APPROVAL_BLOCKER | step | 100 | error_handler | handled->BAL.RETURN_ISSUES | BAL.GATE_HDL_IMPORT | stop | HDL readiness or explicit approval is absent |
| BAL.DONE_READY | terminal | 110 | terminal | none | BAL.GATE_HDL_IMPORT | stop | The resource validation is complete and the separate approved data-loader workflow may proceed |
| BAL.RETURN_ISSUES | terminal | 120 | terminal | none | none | stop | A validation, lookup, dependency, design, or approval issue is handled |
