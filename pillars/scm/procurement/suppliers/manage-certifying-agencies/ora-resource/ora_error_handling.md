# Manage Certifying Agencies Functional Error Handling

## Execution Gate

| Situation | What Must Be Shown | What Must Not Happen | Next Action |
|---|---|---|---|
| Create, update, or supported business-classification association maintenance is requested | Route the approved setup-data change through core.data-loader. | Do not perform a direct mutation from this task guidance. | Resolve the mandatory-field contract, validate the requested business-classification codes, and obtain approval for the exact Data Loader request. |
| A business-classification association removal is requested | `businessClassifications` DELETE is unsupported by this task's Data Loader contract. | Do not submit a child DELETE row, issue a direct REST delete, or interpret a Fusion error as a missing privilege that can make the operation supported. | Stop without generating an executable Data Loader artifact; route the request to a separately approved functional process. |
| A configuration error occurs | Return the affected agency action and sanitized validation or execution failure. | Do not retry, alter the request, or use an undocumented fallback. | Resolve the documented failure, then revalidate and obtain new approval if needed. |
| A child PATCH key is absent or does not identify a current association | Return the child-row lookup blocker. | Do not use a generated sample value, a standard-lookup value, or an inferred ID as BusinessClassificationId. | Resolve the existing association through the documented read-only child lookup, then rebuild and validate the Data Loader artifact. |
| BusinessClassificationCode foreign-key derivation fails with ORA-00942 | Disclose the loader request ID and sanitized backend derivation failure, separately from any REST lookup failure. | Do not remove lookup validation, change APEX SQL, or automatically resubmit a live load. | Prepare a code-only child using the validated lookup output and the live contract; obtain Core approval for the new exact artifact. This is a loader-input workaround, not proof that the backend resolver is fixed. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Must Be Shown |
|---|---|---|---|---|---|---|---|---|
| POZ.CA.CONFIGURATION_GATE | step | 50 | execution_gate | approved->POZ.CA.RETURN_RESULT;blocked->POZ.CA.RETURN_RESULT | POZ.CA.RESOLVE_EXISTING_BUSINESS_CLASSIFICATION | stop | Before a Core Data Loader create, update, or supported association add or change operation | Verify the exact approved preview, current agency state, validated BusinessClassificationCode, absence of the BusinessClassification column in executable child rows, and compatibility with the live contract. The execution route is core.data-loader and remains subject to the task workflow and approval gate. |
| POZ.CA.RETURN_RESULT | terminal | 60 | terminal | none | none | stop | Validation, lookup, approval, or execution-gate processing completes | Return either the approved Data Loader request context or the applicable validation, lookup, or approval blocker. |
