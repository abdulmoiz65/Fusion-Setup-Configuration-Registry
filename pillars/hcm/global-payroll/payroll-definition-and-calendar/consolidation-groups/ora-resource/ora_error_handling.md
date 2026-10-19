# Consolidation Groups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Operation is missing | Stop and request Search, Read One, Create, Update, Monitor Load, Delete, FSM Import, or FSM Export. |
| LDG input is missing, unresolved, ambiguous, inaccessible, invalid, or doesn't match the exact returned LDG Name | Stop with the specific missing, not-found, ambiguous, unauthorized, or invalid-key classification. |
| Create duplicate preflight finds an exact Code or Name in the resolved LDG | Stop before preview, upload, submission, or create; return a duplicate error containing the existing ConsolidationSetId, Name, Code, LDG, and audit fields. |
| Create duplicate preflight has incomplete paging, ambiguous rows, authentication failure, or REST transport failure | Stop before preview, upload, submission, or create; preserve the sanitized failed stage and require complete read-only resolution. |
| Target View Business Objects metadata is required but absent | Stop and request the relevant Payroll Consolidation Group export; do not invent actions, requiredness, or key support. |
| Explicit integration-key columns are supplied for Create | Reject the columns and rebuild the documented create record without SourceSystemOwner, SourceSystemId, or fabricated integration keys. |
| HDL metadata and data rows have different fields or delimiter counts | Reject the file shape before compression and report the mismatched row and field position. |
| Name or Code is blank or exceeds 60 characters | Report the affected field and maximum length before packaging. |
| Update changes Code or uses an unconfirmed key or attribute set | Reject the update and require a View Business Objects-confirmed key, unchanged Code, and target-metadata-confirmed fields. |
| Comments text is placed directly in the data row or its file is missing | Require a filename in Comments and a matching UTF-8 file under ClobFiles. |
| Group search paging is incomplete | Report count, limit, offset, and hasMore; do not claim completeness. |
| A read-one endpoint is requested | State that none is confirmed; use the LDG-scoped collection and exact client-side ID match only in the supplied current App UI read scope. |
| Finder encoding is invalid | Rebuild the decoded finder and URL-encode it once. |
| Upload or submission succeeds but status is not terminal | Report the current request ID and statuses; do not claim the record is loaded. |
| Import or load fails | Retrieve the data-set, PayrollConsolidationGroup, and message results; report sanitized confirmed failures; stop before correction or resubmission. |
| A loader outcome is uncertain | Do not replay upload or submission; reconcile through read-only status and group verification. |
| Delete is requested without a target-metadata-confirmed action and keys | Stop; do not prepare or execute delete. |
| Internal payrollGeneric mutation or public CRUD is requested | Refuse the mutation route and direct supported Create or Update preparation to HCM Data Loader. |
| FSM contract is missing | Stop and request the task-specific action, schema, keys, scope, status, and error contract. |
| Backend failure text is unavailable | Use the local classification and mark the exact Oracle error shape unconfirmed. |
| A display reference cannot be resolved | Preserve the original identifier and mark the name unresolved. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required operation, LDG reference, update key, request ID, metadata, preview, or approval is absent | Request the exact missing fact or artifact. |
| INVALID | A field, length, delimiter, key hint, CLOB shape, finder, mapping, or operation shape violates the contract | Correct it and validate again. |
| NOT_FOUND | An accessible LDG, group, loader data set, business-object result, or reference has no match | Provide a valid identity or verify the prerequisite through the documented workflow. |
| DUPLICATE | An exact proposed ConsolidationSetCode or ConsolidationSetName already exists in the resolved LDG | Return the existing ID, Name, Code, LDG, and audit fields; do not prepare or submit Create. |
| AMBIGUOUS | More than one accessible record matches or status evidence cannot identify one target | Require a unique ID or exact selection. |
| UNAUTHORIZED | Authentication, functional privilege, HDL access, REST aggregate privilege, or LDG data security denies access | Correct access; do not infer nonexistence. |
| UNSUPPORTED | Delete, FSM, public CRUD, internal mutation, dedicated read-one, child resource, expansion, reverse relationship, or invented attribute is requested without evidence | Supply a supported contract or use the documented HDL and read-only scopes. |
| BLOCKED | Target metadata, dependency, safe key representation, preview, approval, terminal status, or verification is incomplete | Resolve the blocker first. |
| FAILED | A documented lookup, import, load, or status operation fails | Preserve sanitized evidence and stop before retry. |
| UNCERTAIN | A loader mutation may have completed but is not verified | Reconcile through read-only loader status and group search before another mutation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Mechanism boundary | State whether the request uses HCM Data Loader preparation, a public read-only LOV or status resource, an internal current App UI read contract, unsupported FSM, or unsupported mutation. |
| HDL preview | Show environment, business object, file and archive structure, operation, integration-key strategy, LDG key representation, Name, Code, optional Comments filename, expected business effect, and unresolved metadata risks. |
| Loader execution handoff | State that this resource authorizes preparation only; upload and submission require a separately authorized executor and approval tied to the unchanged preview. |
| Loader monitoring | Show RequestId, current or terminal data-set status, PayrollConsolidationGroup status and counts, relevant sanitized messages, and whether success criteria are met. |
| Failure | Show the failed stage, local classification, affected file or record when known, sanitized confirmed Oracle evidence, and one safe correction or next-check path. |
| Sensitive evidence | Redact credentials, tokens, cookies, tenant values, audit identities, trace values, routing data, and protected runtime material. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Resource authoring or HDL preparation | Do not invoke Fusion, upload a file, submit a load, or treat these rules as write authorization. |
| Internal payrollGeneric mutation is available | Do not use Create, Update, or Delete siblings as a fallback for HCM Data Loader. |
| Delete or FSM contract is unconfirmed | Do not construct or execute an invented action, schema, payload, key set, or status flow. |
| LDG key representation is unresolved | Do not put a Fusion ID under LegislativeDataGroupName, pass an unresolved name, alter the exact returned Name, or select one of several matches automatically. |
| Create duplicate preflight is incomplete, fails, or finds an exact match | Do not prepare, upload, submit, or create a Consolidation Group or Consolidation Set. |
| Unchanged preview and approval are absent | Do not hand off or submit a live HDL mutation. |
| Upload, submission, or status outcome is uncertain | Do not retry automatically or report success. |
| A loader phase fails | Do not resubmit the same failed archive automatically; correction requires a new archive and a new approved load. |
| Backend contract is unconfirmed | Do not fabricate Oracle errors, uniqueness rules, concurrency headers, optional attributes, or response schemas. |
| Sensitive evidence exists | Do not disclose or persist credentials, tokens, cookies, tenant data, private runtime identifiers, or protected audit details. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.EXECUTE_OR_RETURN | decision | 6 | execution_gate | search_ready->CG.DONE_SEARCH;read_ready->CG.DONE_READ;hdl_ready->CG.DONE_MUTATION_PREPARATION;monitor_ready->CG.DONE_MONITORING;reference_ready->CG.DONE_REFERENCE_RESOLUTION;guidance_ready->CG.DONE_GUIDANCE;blocked->CG.HANDLE_ERROR | CG.ENFORCE_DESIGN | stop | Validation, dependency, lookup, defaulting, and design checks completed |
| CG.HANDLE_ERROR | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | continue | A prior node reports invalid, blocked, unsupported, unauthorized, ambiguous, not-found, failed, or uncertain |
| CG.DONE_SEARCH | terminal | 8 | terminal | none | CG.EXECUTE_OR_RETURN | continue | A current App UI search result is ready for return; no mutation occurred |
| CG.DONE_READ | terminal | 9 | terminal | none | CG.EXECUTE_OR_RETURN | continue | One current App UI group result is ready for return; no mutation occurred |
| CG.DONE_MUTATION_PREPARATION | terminal | 10 | terminal | none | CG.EXECUTE_OR_RETURN | continue | HDL archive and loader handoff preparation are ready for a separately authorized executor; no write is authorized by this terminal |
| CG.DONE_REFERENCE_RESOLUTION | terminal | 11 | terminal | none | CG.EXECUTE_OR_RETURN | continue | Reference choices are ready for return; no mutation occurred |
| CG.DONE_GUIDANCE | terminal | 12 | terminal | none | CG.EXECUTE_OR_RETURN | continue | Conceptual or design guidance is ready for return; no mutation occurred |
| CG.DONE_MONITORING | terminal | 13 | terminal | none | CG.EXECUTE_OR_RETURN | continue | Loader status, business-object result, and messages are ready for return; no mutation occurred |
| RETURN_ISSUES | terminal | 14 | terminal | none | CG.HANDLE_ERROR | continue | Blocking or failure details are safely classified and disclosed |

## Sources

- Developer-provided ConsolidationGroups.md, updated and reviewed 2026-08-13.
- Oracle Fusion Cloud HCM, How Data Is Loaded Using HCM Data Loader: https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/how-data-is-loaded-using-hcm-data-loader.html
- Oracle HCM REST API, HCM Data Loader Data Sets: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-hcm-data-loader-data-sets.html
- Oracle Fusion Cloud HCM, Payroll Manager Security Reference: https://docs.oracle.com/en/cloud/saas/human-resources/oawpm/Payroll_Manager_job_roles.html
