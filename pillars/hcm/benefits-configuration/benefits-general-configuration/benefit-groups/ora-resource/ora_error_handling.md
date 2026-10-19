# Benefit Groups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, artifact, target context, or identity is missing or invalid | Classify as input_validation and stop before a side effect |
| The catalog task, HDL object, or CSV support flag does not match the request | Classify as catalog_or_metadata_mismatch and stop; do not substitute a route or object |
| The read-only LegalEmployer lookup returns 403 | Record unverified_forbidden for that row and field; do not throw a field-validation error or mark the value invalid. Continue independent checks; require authoritative verification before live load |
| The LegalEmployer lookup returns zero or multiple distinct exact matches | Record invalid or ambiguous for that field; do not choose a candidate or rewrite the supplied name |
| Authentication is rejected with a cache-managed 401 or 403 | Delegate one refresh attempt to the selected core service for read-only operations only |
| A data-changing upload, initiation, or delete has an uncertain outcome | Classify as approval_blocker, preserve the artifact and diagnostics, and do not retry automatically |
| A Fusion process fails or times out | Capture sanitized status evidence and external identifiers when available, then stop and provide the next-check path |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Inputs or artifact are invalid | Correct the exact missing or invalid value and rerun preflight |
| catalog_or_metadata_mismatch | Object, task, or catalog support is ambiguous or mismatched | Resolve the catalog or live-metadata gap; do not infer a replacement |
| authorization_or_privilege | Access remains denied after the permitted read-only refresh | Obtain the required environment role or privilege |
| unverified_forbidden | The LegalEmployer lookup returned 403 | Keep field validation nonfailing; verify the name authoritatively before live load |
| transport_or_environment | A read-only request fails transiently | Stop or use the selected core service's bounded read-only retry policy |
| fusion_api_error | Fusion returns a usable API error | Preserve redacted error evidence and follow the recommended corrective action |
| process_timeout | The selected process exceeds its bounded wait | Stop polling and report last status plus next-check guidance |
| process_failed | Fusion returns a terminal failed state | Retrieve available process status or log and correct the source before a new approved run |
| approval_blocker | The mutation lacks current approval or has an uncertain outcome | Do not retry or submit another mutation without explicit approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preflight failure | Failure class, failed stage, exact missing requirement, and safe corrective action |
| LegalEmployer validation | Affected row reference, valid, invalid, ambiguous, or unverified_forbidden status, and safe correction |
| Process timeout or failure | Target environment, operation, task code, request or process identifier when available, last status, elapsed wait, and next-check path |
| Any diagnostic | Sanitized artifact references and external identifiers only; never credentials, tokens, token-cache contents, private keys, full base64 payloads, or customer-sensitive values |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Catalog support is ambiguous or CSV is requested | Do not substitute CSV, REST, browser, or another loader route |
| Update or Delete identity is missing or ambiguous | Do not infer keys, choose a candidate, or submit a mutation |
| A live mutation fails, times out, or has an uncertain result | Do not retry upload, initiation, update, or delete automatically |
| Current approval is absent, stale, or bound to a different artifact or target | Do not perform the mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_GRP.GATE_EXECUTION | decision | 50 | execution_gate | approved->BEN_GRP.READY_FOR_APPROVAL;blocked->BEN_GRP.HANDLE_ISSUE | BEN_GRP.ENFORCE_DESIGN | stop | Confirm a data-changing action has a current approval bound to the validated artifact and target |
| BEN_GRP.HANDLE_ISSUE | step | 90 | error_handler | handled->BEN_GRP.RETURN_ISSUES | none | stop | A validation, readiness, design, or approval gate blocks progress |
| BEN_GRP.READY_FOR_APPROVAL | terminal | 100 | terminal | none | BEN_GRP.GATE_EXECUTION | stop | Every documented gate passed; the task is ready for the selected core.data-loader approval workflow |
| BEN_GRP.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was safely disclosed |
