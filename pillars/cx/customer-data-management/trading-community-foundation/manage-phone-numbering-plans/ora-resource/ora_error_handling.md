# Error Handling

Classify failures without exposing credentials or replaying an uncertain setup
CSV submission. Preserve the exact task identity and any server-issued process
identifier needed for status-only follow-up.

Official sources:

- [Setup Data Export and Import service](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oeswa/setupdataexportandimport-d19810e12.html)
- [Automate export and import of CSV file packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html)

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact offering-and-functional-area discovery returns no task | Ignore that filtered discovery result when HZ_MANAGE_TELEPHONE_NUMBERING_PLANS and the package metadata agree; do not require another user confirmation |
| Package validation or task binding fails | Stop before approval and identify the failed archive or metadata check |
| Fusion rejects the approved import for missing privilege | Stop as authorization_or_privilege and name the required business capability; do not ask the user to certify privileges before preview |
| Authentication fails before submission | Refresh a cache-managed token once only when the selected workflow permits it; otherwise stop |
| A mutating request times out, loses its connection, or returns an uncertain response | Preserve the stage and known process identifier, then reconcile read-only; never replay the request automatically |
| An import or export process completes with errors | Retrieve the supported process result or log and report the affected business object without resubmitting |
| The package, environment, task code, or SHA-256 changes after approval | Invalidate approval and rebuild the immutable preview |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Operation, environment, archive, metadata, task binding, or fingerprint is missing or invalid | Correct the exact input and rebuild the preview |
| catalog_context_mismatch | A filtered offering or functional-area lookup misses the task while fixed task-code evidence exists | Treat the lookup as non-blocking and continue using exact task code and package metadata; do not substitute another task |
| authorization_or_privilege | Authentication succeeds but required task CSV access is denied | Obtain Export Import Functional Setups User and applicable task-specific access |
| auth_expired_or_invalid | Authentication remains invalid after one permitted refresh | Reauthenticate without exposing token material |
| transport_or_environment | Network, DNS, VPN, host, or response certainty fails | Reconcile through a safe read; require fresh approval before any retry |
| fusion_api_error | Fusion rejects task CSV process creation or result retrieval | Preserve the stage, HTTP result, response summary, and ECID when available |
| process_timeout | The existing process remains nonterminal at the polling deadline | Stop polling and provide a status-only continuation path |
| process_failed | Fusion reports terminal errors | Retrieve the process result or log and correct the reported setup-data issue |
| approval_blocker | Approval is absent, stale, or no longer matches the immutable preview | Present one fresh preview and obtain a standalone affirmative response |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import approval | Target environment, task name and code, ZIP path, SHA-256, package-validation result, and whole-task impact |
| Before export approval | Source environment, task name and code, requested task scope, output location, and one-process impact |
| Process accepted | Task name and code, process identifier, operation, and current status |
| Timeout or terminal failure | Environment, operation, task code, process identifier, last status, failure class, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is missing or stale | Do not invoke a mutating request |
| Exact task code or package binding is unresolved | Do not choose a similarly named task or another offering context |
| A filtered live task search returns no row | Do not convert that one result into a claim that Manage Phone Numbering Plans cannot be imported |
| Package members or bytes changed | Do not reuse the prior hash, preview, or approval |
| A submission response is uncertain | Do not submit another import or export automatically |
| Sensitive values are present | Do not print or persist tokens, secrets, authorization headers, or full ZIP content |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PN.APPROVAL | decision | 3 | execution_gate | approved->PN.READY;declined->PN.ISSUES | PN.VALIDATE_PACKAGE | stop | The exact validated operation, environment, task code, and archive fingerprint or export scope have been displayed |
| PN.READY | terminal | 4 | terminal | none | PN.APPROVAL | continue | Validation and approval are complete for handoff to the repository-selected task CSV workflow |
| PN.ERROR | step | 5 | error_handler | handled->PN.ISSUES | none | continue | Package validation, approval, submission, polling, or persistence fails |
| PN.ISSUES | terminal | 6 | terminal | none | none | continue | The request has unresolved package, approval, execution, or persistence issues |
