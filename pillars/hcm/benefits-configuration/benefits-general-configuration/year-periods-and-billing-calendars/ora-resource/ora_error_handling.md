# Benefit Year Periods Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required task context, source, target, or metadata validation is missing or invalid | Classify as input_validation and stop before a side effect |
| The task, business object, or CSV support flag conflicts with the request | Classify as catalog_or_metadata_mismatch and stop; do not substitute an object or route |
| The read-only PeriodTypeMeaning lookup returns 403 | Record unverified_forbidden for that row and field; do not throw a field-validation error or mark the meaning invalid. Continue independent checks; require authoritative verification before live load |
| The PeriodTypeMeaning lookup returns zero or multiple distinct exact matches | Record invalid or ambiguous for that field; do not select a candidate or rewrite the supplied meaning |
| Authentication or privileges prevent the selected core workflow | Classify as authorization_or_privilege after the permitted authentication handling and stop |
| A data-changing upload or initiation has an uncertain result | Classify as approval_blocker, retain sanitized diagnostics, and do not retry automatically |
| A Data Loader process fails or exceeds its wait window | Classify as process_failed or process_timeout, preserve available status evidence, and stop |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | The task context or HDL source is missing, malformed, changed, or unvalidated | Correct the named issue and rerun preflight |
| catalog_or_metadata_mismatch | The object, task, metadata, or route is ambiguous or unsupported | Resolve the mismatch without guessing a replacement |
| authorization_or_privilege | Access remains denied after permitted authentication handling | Obtain the required environment access or privilege |
| unverified_forbidden | The PeriodTypeMeaning lookup returned 403 | Keep field validation nonfailing; verify the meaning authoritatively before live load |
| transport_or_environment | A read-only operation has a transient environment failure | Use only the selected core workflow's bounded read-only retry policy |
| fusion_api_error | Fusion returns an actionable API error | Preserve redacted evidence and correct the source or environment condition |
| process_timeout | The load remains nonterminal after its bounded wait | Stop polling; report last status and next-check guidance |
| process_failed | The load has a terminal failure | Retrieve available process status or logs and correct the source before a new approved run |
| approval_blocker | Approval is absent, stale, mismatched, or the prior mutation is uncertain | Do not upload, initiate, or retry without a new approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preflight failure | Failure class, failed stage, exact missing requirement, and safe corrective action |
| PeriodTypeMeaning validation | Affected row reference, valid, invalid, ambiguous, or unverified_forbidden status, and safe correction |
| Process timeout or failure | Target environment, operation, task code, process or request identifier when available, last status, elapsed wait, and next-check path |
| Any diagnostic | Sanitized artifact references and external identifiers only; never credentials, tokens, token-cache contents, private keys, full base64 payloads, or customer-sensitive values |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The business object, task, metadata, or CSV support is ambiguous | Do not infer a substitute object, route, key, or HDL attribute |
| Approval is absent, stale, or bound to another artifact or environment | Do not upload or initiate the load |
| A live mutation fails, times out, or has an uncertain result | Do not automatically retry, rebuild, or submit a replacement load |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_YR.GATE_EXECUTION | decision | 40 | execution_gate | approved->BEN_YR.READY_FOR_LOAD;blocked->BEN_YR.HANDLE_ISSUE | BEN_YR.ENFORCE_DESIGN | stop | Confirm approval is current and bound to the exact validated artifact and target |
| BEN_YR.HANDLE_ISSUE | step | 90 | error_handler | handled->BEN_YR.RETURN_ISSUES | none | stop | A validation, dependency, design, or approval gate blocks progress |
| BEN_YR.READY_FOR_LOAD | terminal | 100 | terminal | none | BEN_YR.GATE_EXECUTION | stop | Every task-local gate passed; core.data-loader owns any approved load |
| BEN_YR.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was safely classified and disclosed |
