# WorkDay Definitions Error Handling

## Source Basis

- Developer-provided Workday Definition Skeleton.
- Confluence pages 22040252607 and 22040252605.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required or conditionally required field is absent or invalid | Identify the affected field and stop before preview. |
| Day start time is absent or invalid | Request a clock time in a clear format, such as 8:30 AM; do not ask the user for an internal timestamp. |
| A WorkDay Definitions search returns multiple matching or nearest options | Present all business-facing options and request a selection; do not select the first row. |
| A WorkDay Definitions search has no acceptable selection | Ask whether the requester wants to create a new definition; do not infer an existing target. |
| An update or delete target cannot be read | Stop and request a valid selection or existing opaque item key; do not infer identity from Name alone. |
| IsProfileUsedFlag is true | Stop; the definition cannot be updated or deleted. |
| An update or delete DAT is missing its internally resolved WorkDayDefinitionId | Stop before preview; repeat the selected-item lookup and add the verified ID internally. |
| A request includes another read-only or system-managed field | Remove the field and restart validation. |
| Fusion rejects a later mutation, times out, or has an uncertain result | Preserve sanitized diagnostics, reconcile the current definition with a read-only GET, and stop before retry. |
| Optimistic-locking behavior is required | Treat the ETag and If-Match contract as runtime-verified only; stop rather than assuming a retry strategy. |
| A Complete Summary cannot be formed only from verified structured business values | Return to validation, lookup resolution, or defaulting; do not hand off to provider approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required field, enum, time, length, or threshold check fails | Correct the identified value and restart validation. |
| Dependency blocker | Existing definition selection, identity, or profile-use state cannot be verified | Select a definition from the presented options, provide a valid item key, or confirm creation of a new definition. |
| Design blocker | The selected boundary branches conflict with supplied fields or threshold behavior | Correct the conditional configuration before preview. |
| Fusion API | A later service call rejects the request | Preserve the sanitized response and stop; do not change the request route. |
| Process timeout | A later call does not reach a known result | Reconcile with a read-only GET before considering another operation. |
| Summary blocker | A summary value is unverified, technical-only, or cannot be translated to a business display value | Correct or resolve the value before generating the summary. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or design failure | Affected business field, safe failure category, and one corrective action. |
| Profile-use blocker | Definition Name when safely available, that it is in use, and that update or delete is blocked. |
| Lookup failure | Requested operation, the matching or nearest business options when available, whether the item identity was resolved, and one safe next action. |
| Uncertain later mutation | Operation, sanitized status or error, and the required read-only reconciliation step. |
| Complete Summary blocker | Missing or unverified business value, affected business setting, and one safe corrective action; do not disclose technical values. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| IsProfileUsedFlag is true | Do not update or delete the definition. |
| Item identity is unresolved | Do not select a first search result, construct an item path from Name, or perform a write. |
| A mutation is rejected, times out, or is uncertain | Do not automatically retry. |
| Delete is requested | Do not execute without the separate selected-task execution route and fresh explicit approval. |
| A Complete Summary is rendered | Do not expose IDs, codes, keys, internal identifiers, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw booleans, diagnostics, warnings, or technical notes. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WDD.HANDLE_INPUT_ISSUE | step | 80 | error_handler | handled->WDD.RETURN_ISSUES | none | stop | Required or field validation fails |
| WDD.HANDLE_LOOKUP_ISSUE | step | 81 | error_handler | handled->WDD.RETURN_ISSUES | none | stop | Existing definition selection, identity, or mutability cannot be resolved |
| WDD.HANDLE_MUTABILITY_BLOCKER | step | 82 | error_handler | handled->WDD.RETURN_ISSUES | none | stop | IsProfileUsedFlag is true |
| WDD.HANDLE_DESIGN_ISSUE | step | 83 | error_handler | handled->WDD.RETURN_ISSUES | none | stop | A design enforcement rule blocks preview |
| WDD.HANDLE_SUMMARY_ISSUE | step | 84 | error_handler | handled->WDD.RETURN_ISSUES | none | stop | A Complete Summary cannot be formed solely from verified business values |
| WDD.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | A blocking issue has been disclosed with one safe next action |
| WDD.PROVIDER_APPROVAL_READY_CREATE | terminal | 95 | terminal | none | WDD.COMPLETE_CREATE_SUMMARY | stop | A business-only Complete Summary is ready for the unchanged provider-owned approval process for create |
| WDD.PROVIDER_APPROVAL_READY_CHANGE | terminal | 96 | terminal | none | WDD.COMPLETE_CHANGE_SUMMARY | stop | A business-only Complete Summary is ready for the unchanged provider-owned approval process for update |
| WDD.PROVIDER_APPROVAL_READY_DELETE | terminal | 97 | terminal | none | WDD.COMPLETE_DELETE_SUMMARY | stop | A business-only Complete Summary is ready for the unchanged provider-owned approval process for delete; separate execution route and fresh approval remain required |
