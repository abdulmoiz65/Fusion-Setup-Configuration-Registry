# Review and Submit Accounting Configuration Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required name, scope, environment, project, or intent is missing | Stop before external work and request only the missing value |
| Ledger lookup returns zero, many, or wrong category | Show exact input, environment, match count, and safe candidate labels; never select first/fuzzy result |
| Filtered export POST lacks immediate approval | Stop before creating the process and show the exact request body |
| Export times out | Stop with TaskCode, ProcessId, last state, elapsed time, and same-process next-check path; do not create another export |
| Export fails or completes with warnings | Retrieve ProcessLog when available; preserve status and require warning review before payload approval |
| Export ZIP, metadata, scope, or option validation fails | Report the exact member, header, row, field, and owning corrective task; do not build a payload |
| LOV GET has HTTP, auth, authorization, client, schema, timeout, or malformed-result failure | Report the actual class/status/correlation and remediation; never call it not found |
| COA or calendar cross-check fails | Show both sanitized evidence values and stop; never substitute StructureInstanceId or a first calendar row |
| Final execution approval is absent or stale | Stop before ESS POST and regenerate the exact preview if any material value changed |
| ESS POST returns HTTP 201 and id | Persist the checkpoint and poll that request ID only |
| ESS POST response is lost, timed out, or indeterminate | Do not replay; reconcile the original narrow window/checkpoint through read-only evidence |
| ESS polling times out | Stop with environment, job, requestId, last state/phase, and elapsed time; resume the same ID only |
| ESS reaches unsuccessful terminal state | Retrieve status, error type, ECID, child requests, and process log; preserve diagnostics and do not retry automatically |
| ESS succeeds | Require state SUCCEEDED and processPhase Complete, then separately preview/approve the verification export |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required input, mode, export member/header/value, or identity is malformed or missing | Correct only the affected input or owning ledger options |
| catalog_or_metadata_mismatch | Task code, export metadata, category, period, COA, calendar, or parameter contract disagrees | Refresh authoritative evidence; do not infer |
| auth_expired_or_invalid | Eligible cached token fails once | Refresh once, retry the same safe call once, then stop |
| authorization_or_privilege | Final 403 or missing export/ESS privilege | Obtain the required access; do not downgrade to not found |
| transport_or_environment | DNS, network, wrong environment, 429, timeout, or 5xx | Retry only bounded read-only GET/status calls; never replay POST automatically |
| fusion_api_error | Fusion returns 4xx/5xx or a product diagnostic | Preserve status, endpoint path, message summary, and ECID |
| process_timeout | Export or ESS request is nonterminal after the wait budget | Stop and provide same-ID next-check guidance |
| process_failed | Export or ESS reaches an unsuccessful terminal state | Retrieve ProcessLog/status and route correction without retry |
| artifact_persistence | Checkpoint, result, or diagnostics cannot be stored safely | Stop and repair the governed path without exposing sensitive data |
| approval_blocker | Exact export, ESS, retry, or verification-export approval is absent | Stop before the affected mutation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Filtered export | Environment; TaskCode; business object; attribute set/name/value; complete body; expected output; no-retry rule |
| Options readiness | Exact scoped ledger roles; retained-earnings presence; first period and identity checks; every blocker and owning task |
| LOV resolution | Endpoint path; source field; exact match rule/count; mapped values; export cross-check; response fingerprint/time |
| ESS approval | Environment; job definition; requested scope; related candidates; full payload; SHA-256 fingerprint; irreversible effect; one-submit rule |
| ESS result | requestId; job; state; processPhase; elapsed time; completion/error information; ECID and child/process-log references when available |
| Post-submit verification | Separate export approval; exact repeated criterion; terminal export receipt; same configuration scope; final verification result |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Exact primary or target secondary identity is unresolved | Do not broaden lookup, choose first result, use ALC as SL, or use a secondary ID as PRIMARY_LEDGER_ID |
| Mandatory Retained Earnings Account or another required option is absent | Do not build, approve, or submit the ESS request |
| Caller requests primary plus a selected child subset | Do not invent an array or submit one parent request per child |
| Caller proposes StructureInstanceId as COA ID | Do not accept it; require ChartOfAccountsId equal to StructureInstanceNumber |
| Export, ESS, or verification-export approval is missing/stale | Do not perform that POST |
| Original mutation result is uncertain | Do not retry or start an equivalent request until reconciled and freshly approved |
| Sensitive value appears | Do not print or persist credentials, Authorization headers, tokens, token caches, private keys, or reusable customer-specific examples |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLREV.ERROR_POLICY | step | 60 | error_handler | classified->GLREV.APPROVAL_GATE | GLREV.ENFORCE | stop | Preflight outcomes and mutation boundaries must be classified |
| GLREV.APPROVAL_GATE | decision | 70 | execution_gate | approved->GLREV.APPROVED_REQUEST;missing->GLREV.RETURN_ISSUES | GLREV.ERROR_POLICY | stop | Preview-only returns missing; execute requires unchanged exact approval |
| GLREV.APPROVED_REQUEST | terminal | 80 | terminal | none | GLREV.APPROVAL_GATE | continue | Validation is ready and exact approval is bound; the task runbook may invoke the core ESS submitter once |
| GLREV.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Input, dependency, lookup, design, approval, or prior-request issues remain |
