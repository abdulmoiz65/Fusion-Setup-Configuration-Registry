# Error Handling

Classify failures without exposing credentials or replaying an uncertain setup
CSV submission. Preserve server-issued process identifiers for status-only
follow-up.

Official sources:

- [Setup Data Export and Import service](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oeswa/setupdataexportandimport-d19810e12.html)
- [Automate export and import of CSV file packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html)

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact offering-and-functional-area discovery returns no task | Ignore filtered result when ZCM_MANAGE_CUSTOMER_CENTER_ASSESSMENT_TEMPLATE and package metadata agree; do not require another confirmation |
| Package validation or task binding fails | Stop before approval and identify failed archive or metadata check |
| Fusion rejects approved import for missing privilege | Stop as authorization_or_privilege; do not ask user to certify privileges before preview |
| Authentication fails before submission | Refresh cache-managed token once only when selected workflow permits; otherwise stop |
| Mutating request times out, loses connection, or is uncertain | Preserve stage and known process identifier, then reconcile read-only; never replay automatically |
| Import or export process completes with errors | Retrieve supported process result or log and report affected object without resubmitting |
| Package, environment, task code, or SHA-256 changes after approval | Invalidate approval and rebuild immutable preview |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Operation, environment, archive, metadata, binding, or fingerprint is invalid | Correct exact input and rebuild preview |
| catalog_context_mismatch | Filtered context lookup misses while fixed task-code evidence exists | Continue with exact task code and package metadata |
| authorization_or_privilege | Authentication succeeds but task CSV access is denied | Obtain applicable access and submit only after fresh approval |
| auth_expired_or_invalid | Authentication remains invalid after one permitted refresh | Reauthenticate without exposing token material |
| transport_or_environment | Network, host, or response certainty fails | Reconcile through safe read; require fresh approval before retry |
| fusion_api_error | Fusion rejects process creation or result retrieval | Preserve stage, response summary, and ECID when available |
| process_timeout | Existing process remains nonterminal at polling deadline | Stop polling and provide status-only continuation path |
| process_failed | Fusion reports terminal errors | Retrieve result or log and correct reported setup-data issue |
| approval_blocker | Approval is absent, stale, or no longer matches preview | Present one fresh preview and obtain standalone approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import approval | Target environment, task name and code, ZIP path, SHA-256, package-validation result, and whole-task impact |
| Before export approval | Source environment, task name and code, requested scope, output location, and one-process impact |
| Process accepted | Task name and code, process identifier, operation, and current status |
| Timeout or terminal failure | Environment, operation, task code, process identifier, last status, failure class, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is missing or stale | Do not invoke mutating request |
| Exact task code or package binding is unresolved | Do not choose similarly named task or another context |
| Filtered live task search returns no row | Do not claim this task cannot be imported |
| Package members or bytes changed | Do not reuse prior hash, preview, or approval |
| Submission response is uncertain | Do not submit another import or export automatically |
| Sensitive values are present | Do not print or persist tokens, secrets, authorization headers, or full ZIP content |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.APPROVAL | decision | 3 | execution_gate | approved->AT.READY;declined->AT.ISSUES | AT.VALIDATE_PACKAGE | stop | Exact validated operation, environment, task code, and archive fingerprint or export scope are displayed |
| AT.READY | terminal | 4 | terminal | none | AT.APPROVAL | continue | Validation and approval are complete for handoff to repository-selected task CSV workflow |
| AT.ERROR | step | 5 | error_handler | handled->AT.ISSUES | none | continue | Package validation, approval, submission, polling, or persistence fails |
| AT.ISSUES | terminal | 6 | terminal | none | none | continue | Request has unresolved package, approval, execution, or persistence issues |
