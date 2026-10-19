# Configure Legislations for Human Resources Errors and Outcomes

This file owns failure classification, safe disclosure, and recovery.
Search result and exact-identity lookup semantics belong to ora_reference_lookups.md.
Every failing step records its stage and reason before transitioning to CLHR.ERROR.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Filter shape or value is invalid | Return INPUT_VALIDATION; identify the filter and accepted contract without making a request |
| Enclosing manifest or registry identifies Payroll instead of Human Resources | Return TASK_IDENTITY_MISMATCH; stop before authentication or Search |
| The execution guide, task plan, or reachable source anchors fail validation | Return AUTHORING_CONTRACT_ERROR before lookup or artifact preparation; correct the owning rule source and recompile |
| Applicable project or Run Book context is missing | Return WORKFLOW_NOT_READY with the concrete prerequisite and owning project/Run Book workflow; do not substitute an external execution route |
| Configured environment identity or restBaseUrl is missing, invalid, or inconsistent | Return ENVIRONMENT_NOT_READY with the concrete environment configuration issue; the skill owns the lookup path, so do not request a path or resource version |
| Operation is outside Search, Create, Delete, and Verify Delete | Return UNSUPPORTED; do not perform a write or substitute FSM |
| Proxy-bypass preflight fails | Return TRANSPORT_ENVIRONMENT; disclose only hostname and sanitized verification booleans; do not issue the request |
| Authentication or read access fails | Return AUTH_AUTHZ; the governed client may perform its one declared cached-token recovery; do not add another task-level retry or read the token cache |
| TLS or certificate failure occurs | Return TRANSPORT_ENVIRONMENT and stop; do not disable verification or install trust material; any login recovery remains governed by the explicit session policy |
| HTTP 400 rejects the query or a filter attribute | Return QUERY_CONTRACT_ERROR with the sanitized service message; do not remove filters or change query semantics to obtain rows |
| HTTP 404 is returned | Return ENDPOINT_NOT_FOUND for the declared standard resource and stop; this is not evidence that a legislation does not exist and does not authorize a browser-route fallback |
| Another HTTP failure occurs, including 429 or 5xx | Return FUSION_API; retain sanitized status and safe next action; no task-level automatic retry is declared |
| Response is malformed, violates the filter, or has unsupported field values | Return RESPONSE_CONTRACT_ERROR or SEARCH_INCONCLUSIVE; do not coerce the response into a valid result |
| Pagination is incomplete, repeats, or fails to advance | Return SEARCH_INCOMPLETE with complete=false and the last offset; disclose partial results as partial |
| Combined empty results contradict diagnostic results | Return SEARCH_INCONCLUSIVE; report the contradictory filter combination without asserting absence |
| The caller's timeout or cancellation limit is reached | Return PROCESS_TIMEOUT with complete=false, elapsed time, and last offset; a new search restarts at offset 0 to avoid treating stale pages as one snapshot |
| No transition fits a node's result | Return AUTHORING_CONTRACT_ERROR; never invent a success path |
| Delete target is missing | Return MISSING_TARGET and ask for the legislation name; reuse any identifier already supplied |
| Delete lookup has no exact target | Return TARGET_NOT_FOUND without a DAT or upload; this is not proof of a previous deletion |
| Delete lookup needs selection or supplied name/code conflict | Return TARGET_SELECTION_REQUIRED or TARGET_CONFLICT with business-facing candidates; require one consistent exact identity |
| DAT filename, columns, values, directive, or record count violate the contract | Return DELETE_DAT_INVALID and the concrete correction; a suffixed inner DAT filename must be corrected even if the outer ZIP name is valid |
| Live loader schema or business-object registration differs from the contract | Return CATALOG_MISMATCH through Data Loader; do not submit, switch to FSM, or replace the custom action with HTTP DELETE |
| Task Hook lacks an immutable artifact/preflight or detects changed bytes | Return MISSING_ARTIFACT_CONTEXT or ARTIFACT_MISMATCH to Data Loader; require fresh source validation before approval |
| File persistence or unsafe/occupied destination fails | Return ARTIFACT_PERSISTENCE; preserve existing artifacts and request a safe distinct destination instead of overwriting another deletion |
| Load is unapproved or approval no longer matches its context | Let Data Loader report its approval blocker; do not add a task-specific approval prompt or bypass its envelope |
| Upload/initiation fails, times out, or has an uncertain result | Retain the loader's sanitized stage and any returned identifiers for reconciliation; do not automatically upload or initiate again |
| Status reports processing or failed objects | Return the loader's actual status/errors; do not run absence verification or declare deletion complete |
| Verify Delete lacks its original target/environment or visibility context | Return MISSING_VERIFICATION_CONTEXT or VERIFICATION_INCONCLUSIVE; do not reconstruct identity from a filename or infer absence |
| Verification still finds the exact code | Return DELETE_NOT_CONFIRMED and the record found; a successful load does not override observed presence or authorize another delete |
| Create target omitted or uncertain | Return AVAILABLE_LEGISLATIONS with complete current names/codes and ask for one; do not run dependent LOVs |
| Create target is already installed | Return ALREADY_EXISTS with matched legislation; explain that changes require Edit, without switching operation automatically |
| Create target absent from both complete relevant collections | Return LEGISLATION_UNAVAILABLE with available choices; describe it as invalid or unavailable for Create in this context, not as globally invalid |
| Required date or TRU choice missing | Return MISSING_CREATE_INPUTS; ask only unanswered fields together and include current TRU Meanings |
| Explicit currency/rule/person/relationship choice invalid or ambiguous | Return INVALID_CREATE_OPTION with current relevant labels/codes; preserve supplied input for correction and do not default it |
| Generic LOV required key missing/duplicated, sole default cardinality wrong, or ProcessInRun unsupported | Return CREATE_LOOKUP_CONTRACT_ERROR; stop preparation rather than guessing positions, values or a replacement route |
| Default person alias unresolved or conflicting | Return DEFAULT_PERSON_TYPE_UNRESOLVED for the displayed default row; do not request a source attachment or invent its code |
| Legislation Rules inputs prepared | Return CREATE_DATA_PREPARED and CREATE_BO_CONTRACT_PENDING with the business summary; no actual DAT, upload or completed creation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | MISSING_CREATE_INPUTS, INVALID_CREATE_OPTION, LEGISLATION_UNAVAILABLE, INPUT_VALIDATION, MISSING_TARGET, TARGET_NOT_FOUND, TARGET_SELECTION_REQUIRED, TARGET_CONFLICT, DELETE_DAT_INVALID, or MISSING_VERIFICATION_CONTEXT | Correct only the missing or conflicting input; no load follows an unresolved target |
| Catalog mismatch | CREATE_LOOKUP_CONTRACT_ERROR, DEFAULT_PERSON_TYPE_UNRESOLVED, TASK_IDENTITY_MISMATCH, CATALOG_MISMATCH, or AUTHORING_CONTRACT_ERROR | Correct the owning metadata or resource contract and recompile before execution |
| Input validation | WORKFLOW_NOT_READY | Establish the required project context or satisfy the router's Run Book prerequisite before the relevant stage |
| Auth/authz | AUTH_AUTHZ | Restore governed authentication or resource access |
| Transport/environment | ENVIRONMENT_NOT_READY, TRANSPORT_ENVIRONMENT, or ENDPOINT_NOT_FOUND | Confirm the current environment, endpoint, and connectivity |
| Fusion API | QUERY_CONTRACT_ERROR, FUSION_API, RESPONSE_CONTRACT_ERROR, SEARCH_INCOMPLETE, or SEARCH_INCONCLUSIVE | Inspect sanitized evidence and fix the source or service contract before an explicit rerun |
| Process timeout | PROCESS_TIMEOUT | Report partial progress; rerun only when the caller requests or authorizes it |
| Input validation / unsupported operation | UNSUPPORTED | Use a separately authored operation workflow |
| Artifact persistence | ARTIFACT_PERSISTENCE, MISSING_ARTIFACT_CONTEXT, or ARTIFACT_MISMATCH | Resolve destination/integrity issues through the owning artifact or loader workflow |
| Approval blocker | Data Loader's approval-required or invalid-approval result | Follow only its exact-artifact approval lifecycle |
| Process failed | Loader import/load failure or DELETE_NOT_CONFIRMED | Review the returned diagnostics or present record before considering a separately approved correction |
| Transport/environment | VERIFICATION_INCONCLUSIVE | Restore the same confirmed environment/access context before another explicit verification |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Failed operation | Task name, operation, failure class, current stage, sanitized target/filter summary, HTTP status when available, complete=false for incomplete reads, verified partial count, and one safe next action |
| Pagination interruption | Last offset, elapsed time when available, and an explicit incomplete-result warning |
| Task identity blocker | Expected Human Resources identity and the mismatched manifest path; never disguise the generated Payroll task code as a valid Human Resources registry |
| Source inconsistency | A combined-filter zero contradicts its complete diagnostic queries; report the current-run inconsistency without asserting absence |
| Protected material | Never show or persist Authentication headers, cookies, token cache contents, session identifiers, opaque links, or complete raw responses |
| Validated deletion draft | DELETE_READY returns selected legCode/name/environment, complete lookup evidence, validated contract values, and execution_intent to the owning workflow; that workflow prepares the DAT and applies the handoff gates in ora_design_enforcement.md; the terminal itself grants no upload approval |
| Prepared deletion | Link to the DAT and selected legislation; for prepare_only return the file without upload, and for load continue only through the declared Data Loader handoff; state prepared, with no implication of upload or deletion |
| Accepted initiation | Return Data Loader's prescribed report unchanged; initiation is not completed deletion and does not trigger automatic polling |
| Explicit successful verification | State that the original code is absent in the confirmed environment/access context after the successful load and completed lookup; user confirmation from the UI is separate evidence and must not be presented as an automated REST verification |
| Durable task artifact or run | The owning project workflow records sanitized selection, validation, artifact references, and side effects under the task's project artifact location and state/runs; apply the project's token-usage log policy and never include authentication/configuration material |
| Timeout or uncertain load | Environment, operation, task, request/process identifier when available, last known status, elapsed wait, and safe status-check path; no replay |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| An HTTP or pagination failure occurred | Do not translate failure into NO_MATCHES |
| Evidence is partial or contradictory | Do not assert absence, global nonexistence, or Search completion |
| A governed client cannot execute the route | Do not replay captured cookies, use an ad hoc HTTP client, or switch to browser or FSM |
| A filter is rejected by the service | Do not fetch all records and silently filter them locally |
| A new mutation or retry is requested | Do not invent a write contract, reuse former Payroll creation defaults, or reuse another deletion's approval |
| A status says success but no complete absence query ran | Do not claim automated confirmation that the legislation was removed |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLHR.ERROR | step | 900 | error_handler | reported->RETURN_ISSUES | none | stop | A preceding node failed or rejected the request; classify and disclose its recorded reason |
| CLHR.COMPLETE | terminal | 1000 | terminal | none | CLHR.SEARCH | continue | Search completed consistently; preserve MATCHES, MULTIPLE_MATCHES, or NO_MATCHES without any mutation |
| CLHR.DELETE_READY | terminal | 1001 | terminal | none | CLHR.ENFORCE_DELETE_DESIGN | continue | Delete rules passed; return selected code and contract values for preparation, or validated final-artifact evidence to Task Hook; this is neither upload approval nor a completed deletion |
| CLHR.DELETE_CONFIRMED | terminal | 1002 | terminal | none | CLHR.VERIFY_DELETED | continue | Successful load followed by complete consistent lookup with absent outcome; return DELETE_CONFIRMED in the confirmed environment/access context |
| CLHR.DELETE_PRESENT | terminal | 1003 | terminal | none | CLHR.VERIFY_DELETED | continue | Verification returned present; report DELETE_NOT_CONFIRMED and do not submit another deletion |
| RETURN_ISSUES | terminal | 1099 | terminal | none | none | continue | CLHR.ERROR reported the blocker; no claim of completed Search, upload, or deletion |
| CLHR.CREATE_SELECTION_REQUIRED | terminal | 1051 | terminal | none | CLHR.RESOLVE_CREATE_LEGISLATION | continue | Available choices returned; await one legislation and restart eligibility; no dependent lookup or mutation |
| CLHR.CREATE_UNAVAILABLE | terminal | 1052 | terminal | none | CLHR.CLASSIFY_UNAVAILABLE | continue | Explain ALREADY_EXISTS or LEGISLATION_UNAVAILABLE from complete evidence; no implicit Edit or Create |
| CLHR.CREATE_INPUT_REQUIRED | terminal | 1064 | terminal | none | CLHR.VALIDATE_CREATE_RULE_INPUTS | continue | Ask only missing required business values with relevant choices; retain shared selection and resume Create validation with current evidence |
| CLHR.CREATE_DATA_PREPARED | terminal | 1065 | terminal | none | CLHR.ENFORCE_CREATE_DESIGN | continue | Validated Legislation Rules data and logical action parameters prepared; disclose defaults and CREATE_BO_CONTRACT_PENDING; no DAT or Fusion write |
| CLHR.CREATE_OPTIONS_RETURNED | terminal | 1056 | terminal | none | CLHR.CREATE_OPTION_REQUEST | continue | Display requested live options and ask the intended selection; no omission default applied for that choice, no claim that preparation is complete |
