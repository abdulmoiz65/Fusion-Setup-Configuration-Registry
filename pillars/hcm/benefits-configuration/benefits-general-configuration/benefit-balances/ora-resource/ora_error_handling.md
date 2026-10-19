# Benefit Balances Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, object, artifact, identity, prerequisite, or target context is missing or invalid | Classify as input_validation and stop before side effects. |
| The catalog task, HDL object, CSV flag, DAT schema, or selected action does not match the request | Classify as catalog_or_metadata_mismatch and stop; do not substitute a route, field, or action. |
| A date-effective DAT row is rejected because effectiveOf is absent or invalid | Classify as input_validation; do not replay the artifact, derive effectiveOf from the exact row operation and explicit required input, rebuild the immutable preview, and obtain a new approval before submission. |
| A conditional read-only LOV returns 403 | Record unverified_forbidden for only that supplied field; do not throw a field-validation error or mark the value invalid. Continue other independent checks. Resolve access or obtain another workflow-approved authoritative check before live load. |
| A conditional read-only LOV returns zero or multiple distinct exact matches | Record invalid or ambiguous for that field; do not select a candidate or rewrite the supplied value. |
| Authentication is rejected with a cache-managed 401 or 403 during a read-only status operation | Permit the selected core service to refresh once; stop if access remains denied. |
| A data-changing upload, initiation, update, or delete has an uncertain result | Classify as approval_blocker, preserve redacted diagnostics, reconcile through a selected read-only status route, and do not retry automatically. |
| A Fusion load process fails or times out | Capture sanitized status evidence and external identifiers when available, retrieve the available process log, and stop with next-check guidance. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Inputs, record prerequisites, or DAT artifact are invalid | Correct the exact missing or invalid value and rerun preflight. |
| catalog_or_metadata_mismatch | Object, task, schema, action, or catalog support is ambiguous or mismatched | Resolve the current metadata gap; do not infer a replacement. |
| authorization_or_privilege | Access remains denied after the one permitted read-only refresh | Obtain the required environment role or privilege. |
| unverified_forbidden | A conditional lookup returned 403 | Keep the field-validation result nonfailing, but require authoritative verification before live load. |
| transport_or_environment | A read-only request fails transiently | Stop or use the selected core service's bounded read-only retry policy. |
| fusion_api_error | Fusion returns a usable error | Preserve redacted evidence and follow the corrective action. |
| process_timeout | The process exceeds its bounded wait | Stop polling; report last status and the next-check path. |
| process_failed | Fusion returns a terminal failed state | Retrieve available process status or log, correct the source, and seek approval for a new run. |
| approval_blocker | Approval is missing, stale, or the outcome is uncertain | Do not retry or submit another mutation without explicit approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preflight failure | Failure class, failed stage, exact missing requirement, affected record reference where safe, and corrective action. |
| Reference validation | Each supplied field's row reference, status, and safe correction; distinguish invalid, ambiguous, and unverified_forbidden. |
| Process timeout or failure | Target environment, operation, task code, benefitBalances object, request or process identifier when available, last status, elapsed wait, and next-check path. |
| Any diagnostic | Sanitized artifact references and external identifiers only; never credentials, tokens, token-cache contents, private keys, full payload values, or customer-sensitive data. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Catalog, business object, current schema, or action support is ambiguous | Do not substitute CSV, REST, browser, or another loader route. |
| Identity or prerequisite is missing or ambiguous | Do not infer keys, select a candidate, or submit a mutation. |
| A mutation fails, times out, or has an uncertain outcome | Do not automatically retry an upload, initiation, update, or delete. |
| Current approval is absent, stale, or bound to another artifact or target | Do not perform the mutation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_BAL.GATE_EXECUTION | decision | 40 | execution_gate | approved->BEN_BAL.READY_FOR_EXECUTION;blocked->BEN_BAL.HANDLE_ISSUE | BEN_BAL.ENFORCE_DESIGN | stop | Confirm current approval is bound to the validated artifact, target, and operation |
| BEN_BAL.HANDLE_ISSUE | step | 90 | error_handler | handled->BEN_BAL.RETURN_ISSUES | none | stop | A validation, readiness, design, approval, or load failure blocks progress |
| BEN_BAL.READY_FOR_EXECUTION | terminal | 100 | terminal | none | BEN_BAL.GATE_EXECUTION | stop | Every documented gate passed; ready for the selected core.data-loader workflow |
| BEN_BAL.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was safely disclosed |
