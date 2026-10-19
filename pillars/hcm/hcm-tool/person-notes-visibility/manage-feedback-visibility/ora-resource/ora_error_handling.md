# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A list, exact-context read, or contains-context search fails | Preserve the failure class and sanitized request context; stop without treating failure as zero matches. |
| Exact-context resolution returns zero rows for read, edit, or delete | Return not found and request the exact ContextType code or context Meaning. |
| Exact-context resolution returns more than one row | Return ambiguity and stop before mutation preparation. |
| Data Loader metadata lacks the requested operation or required keys | Classify as catalog or metadata mismatch and stop without constructing a REST mutation. |
| A common lookup or profile option value cannot be resolved | Return the missing or ambiguous dependency and stop before preview. |
| Fusion returns a stored NotificationManagerTypeList for a context other than ORA_NO_CONTEXT | Preserve the raw value only as backend read evidence; do not resolve it, leave Manager Type blank in lists, hide the field in detail or edit views, and do not copy it into a create or edit artifact. |
| Create or edit requests No Default | Preserve the normalized business value exactly as No Default; do not replace it with blank, null, or #NULL. Stop before Data Loader preview when the registered adapter has no explicit supported No Default mapping. |
| Fusion returns the literal #NULL in DefaultNoteVisibilityCode | Classify the row as invalid stored data caused by an unsupported mapping; do not treat the value as No Default or reuse it in another load. Reconcile the exact row and prepare a separate approved recovery with a valid mapped default. |
| A Data Loader artifact or preview fails validation | Preserve row-level diagnostics and stop before upload or execution. |
| A live Data Loader mutation has an uncertain outcome | Do not retry; reconcile through a fresh read before considering another operation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required operation input, exact target, lookup value, profile option value, key field, or artifact is absent | Supply the exact missing value or artifact. |
| AMBIGUOUS | More than one exact target or dependency match remains | Provide a more precise business identity and rerun resolution. |
| UNSUPPORTED | The requested operation is absent from Data Loader metadata or asks for a direct Fusion REST mutation | Use a supported core.data-loader operation or stop. |
| AUTH_AUTHZ | A read or metadata lookup returns 401 or 403 | Correct access; refresh cached authentication once only for the read-only request. |
| TRANSPORT_ENVIRONMENT | Host, network, timeout, or environment validation fails | Correct the environment and rerun only the read-only preflight. |
| FAILED | Response shape, paging, artifact validation, execution, or verification fails | Preserve sanitized diagnostics and correct the failed stage. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read failure | Environment, operation, filter mode, failure class, and safe next action. |
| Pre-mutation preview | Environment, create or edit or delete operation, exact target ContextType and displayed context Meaning, key fields, material values, immutable artifact reference, and validation result. |
| Mutation result | Confirmed status, verified readback, external identifiers when safe, and any row-level errors. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A browser trace or guessed item URL appears usable for mutation | Do not send a direct POST, PATCH, PUT, DELETE, or action request to Fusion. |
| A partial-context search returns one convenient row | Do not treat it as the edit or delete target without an exact-context read. |
| A context other than ORA_NO_CONTEXT has a raw or requested manager type | Do not display it as an active Manager Type or include it in a create or edit artifact; leave list output blank and hide the field in detail or edit views. |
| No Default is requested for create or edit | Do not normalize it to blank, null, or #NULL, and do not send the literal label as a lookup code. Preserve No Default as the task value and stop unless the Data Loader adapter explicitly supports the mapping. |
| Approval was given for a different environment, operation, artifact, key, or material value | Do not execute; regenerate the preview and obtain new approval. |
| A mutation outcome is uncertain | Do not retry automatically or switch to a direct REST route. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FEEDBACK_VISIBILITY.LIST_DONE | terminal | 10 | terminal | none | FEEDBACK_VISIBILITY.RESOLVE_LIST_LOOKUPS | stop | A complete configuration list is returned with current context and default visibility meanings; Manager Type is populated only for ORA_NO_CONTEXT and blank for every other context |
| FEEDBACK_VISIBILITY.READ_DONE | terminal | 11 | terminal | none | FEEDBACK_VISIBILITY.FIND_EXACT_CONTEXT | stop | One exact-context configuration is returned with Manager Type visible only for ORA_NO_CONTEXT and otherwise blank or hidden |
| FEEDBACK_VISIBILITY.SEARCH_DONE | terminal | 12 | terminal | none | FEEDBACK_VISIBILITY.SEARCH_CONTEXT_TERM | stop | A complete contains-context search result is returned with Manager Type populated only for ORA_NO_CONTEXT and blank for every other context |
| FEEDBACK_VISIBILITY.DATALOADER_READY | terminal | 13 | terminal | none | FEEDBACK_VISIBILITY.ENFORCE_MUTATION_ROUTE | stop | The Data Loader route and immutable preview are ready for the separate execution workflow |
| FEEDBACK_VISIBILITY.INPUT_INVALID | terminal | 14 | terminal | none | none | stop | Required input or preview information is missing or invalid |
| FEEDBACK_VISIBILITY.NOT_FOUND | terminal | 15 | terminal | none | none | stop | No exact ContextType configuration matches a read, edit, or delete request |
| FEEDBACK_VISIBILITY.AMBIGUOUS | terminal | 16 | terminal | none | none | stop | Exact-context target resolution is ambiguous or create would duplicate an existing ContextType configuration |
| FEEDBACK_VISIBILITY.DEPENDENCY_MISSING | terminal | 17 | terminal | none | none | stop | A required common lookup or profile option value cannot be resolved |
| FEEDBACK_VISIBILITY.ROUTE_UNSUPPORTED | terminal | 18 | terminal | none | none | stop | The operation is unsupported by Data Loader metadata or requests a direct Fusion REST mutation |
| FEEDBACK_VISIBILITY.READ_FAILED | terminal | 19 | terminal | none | none | stop | A read-only configuration, lookup, profile option, or metadata request failed |
