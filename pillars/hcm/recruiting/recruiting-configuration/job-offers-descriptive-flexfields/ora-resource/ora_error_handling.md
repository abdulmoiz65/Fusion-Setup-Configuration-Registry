# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Catalog identity differs from the exact task code or CSV support is not Y | Stop as CATALOG_MISMATCH; do not substitute a generic DFF task. |
| Export submission lacks a unique ProcessId or the local result is lost | Do not submit another export. Reconcile a matching Ready for download entry and validate its task metadata; return OUTCOME_UNCERTAIN only if that exact match cannot be established. |
| Export, context, segment, value-set, or package contract is missing or ambiguous | Stop before preview, import, deployment, or Fusion access. |
| An import instruction is absent, or the candidate fingerprint is stale | Stop as BLOCKED or STALE_PREVIEW; require a new import request or create a new candidate. |
| Import, deployment, or verification outcome is failed, partial, timed out, or uncertain | Preserve sanitized evidence, return PROCESS_FAILED or OUTCOME_UNCERTAIN, and do not retry automatically. |
| Deployment or TDS configuration is requested without a proven automated route | Return MANUAL_INTERVENTION_REQUIRED and route to the approved manual task workflow. |
| Access is missing or a 401/403 occurs | Stop as AUTH_REQUIRED and route to the security owner. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| CATALOG_MISMATCH | Exact catalog identity or capability differs | Correct the selected task or catalog association. |
| BLOCKED | Evidence, authority, or import instruction is incomplete | Supply the required export, authority, or import instruction. |
| STALE_PREVIEW | Target state or candidate ZIP changed | Export and validate again, then submit a new import request. |
| AUTH_REQUIRED | Task or setup-data access is unavailable | Obtain required FSM and task-specific access. |
| PROCESS_FAILED | A known process failure is returned | Correct the source and create a new preview; do not retry automatically. |
| OUTCOME_UNCERTAIN | Acceptance or completion cannot be reconciled | Reconcile through the approved task workflow before another mutation. |
| MANUAL_INTERVENTION_REQUIRED | Deployment or TDS operation has no supported automation | Perform the separately approved manual workflow. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Import preview | Target environment, task and DFF identity, operation, exact target, changed fields, source-export timestamp, and candidate SHA-256 |
| Import instruction | Original request explicitly directs import to the selected target; the same-run candidate SHA-256 is retained in the result |
| Failure | Business identity, result category, safe next action, and sanitized evidence only |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Package contract is not proven by a fresh export | Do not hand-build CSV members, headers, keys, or payloads. |
| Value-set authority is incomplete | Do not use an application lookup or label as a substitute. |
| Import is requested without an explicit original import instruction, or deployment lacks separate approval | Do not upload, import, deploy, or retry. |
| Transaction Design Studio change is requested | Do not attempt it through the DFF package. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IRC_OFFER_DFF.READINESS_GATE | decision | 70 | execution_gate | ready->IRC_OFFER_DFF.DONE_VALIDATED;blocked->IRC_OFFER_DFF.HANDLE_ISSUE | IRC_OFFER_DFF.ENFORCE_DESIGN | stop | Before handing a validated immutable package to core.data-loader |
| IRC_OFFER_DFF.HANDLE_ISSUE | step | 80 | error_handler | handled->IRC_OFFER_DFF.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, import-instruction, process, or authorization issue |
| IRC_OFFER_DFF.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| IRC_OFFER_DFF.DONE_VALIDATED | terminal | 100 | terminal | none | IRC_OFFER_DFF.READINESS_GATE | stop | The request is validated and ready for the explicitly requested next operation |
