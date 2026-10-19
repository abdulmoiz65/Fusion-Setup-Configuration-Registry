# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required hierarchy type or flattening method is missing | Ask once for all unresolved required values, showing all four hierarchy-type options and both flattening-method options, or accept an explicit request to use Oracle defaults. |
| Partner wording or a null hierarchy name is supplied | Map bare partner wording to Partner Hierarchy. Treat a null name as proposed all-hierarchy scope, disclose it in the consolidated confirmation, and do not create a separate scope question. |
| The selected type or method is outside the documented option set | Return input_validation and keep the request preview-only. |
| A Version value is supplied | Preserve and pass the exact value as argument3; do not ask the user for a separate internal identifier. |
| Payload construction cannot produce all four ordered STRING positions | Return catalog_or_metadata_mismatch; never hand-build or submit a partial payload. |
| 401 or 403 | Classify auth/authz, refresh a cache-managed token at most once when policy permits, and never reinterpret denial as missing metadata. |
| A submission outcome is uncertain | Reconcile read-only by correlation, exact job identity, UTC window, and complete parameter contract; never submit a replacement automatically. |
| A new run or rerun is requested and an older run exists | Treat the older run only as audit history. Start a fresh intake and do not report the older completion as the outcome of the new request. |
| Future polling times out | Preserve requestId, last state, environment, elapsed wait, and safe resume guidance. |
| Future process fails | Retrieve and persist safe status or process-log evidence and stop before retry. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required value is missing, malformed, unsupported, or ambiguous | Correct the business input and rebuild the preview. |
| catalog_or_metadata_mismatch | Task, LOV, hierarchy, version, or contract metadata has no exact match | Reconcile source evidence; do not guess. |
| auth_expired_or_invalid | A cache-managed session is rejected | Refresh once only under repository policy. |
| authorization_or_privilege | Access remains denied or the required role/duty is absent | Restore exact access; do not retry a side effect. |
| transport_or_environment | DNS, VPN, service, or target identity fails | Retry only bounded read-only checks. |
| fusion_api_error | Fusion rejects an approved request | Persist status, endpoint path, safe response summary, and ECID, then stop. |
| process_timeout | A request does not finish in the declared wait window | Preserve requestId and resume tracking only when asked. |
| process_failed | A request reaches a failed or completed-with-errors state | Preserve status/process log and require correction or approved retry. |
| artifact_persistence | Preview, checkpoint, result, or diagnostic cannot be saved | Preserve safe temporary diagnostics and report the intended path. |
| approval_blocker | Remaining contract details are incomplete, the consolidated approval is missing or stale, overwrite is unapproved, or retry is unsafe | Stop before side effects and report one safe next action. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Environment, hierarchy type, name/scope, version, flattening method, default provenance, warnings, and execution readiness. |
| Contract blocker | The verified application, jobDefinitionId, ordered STRING positions, supported mappings, payload fingerprint, and exact remaining blocker. |
| Submission | In one consolidated approval, show only the job name Party Hierarchy Generation, exact environment, business-facing hierarchy type, scope, version, flattening method, and applicable warnings. Keep application, job-definition path, task code, ESS arguments, transport values, payload fingerprint, correlation description, retry mechanics, and polling mechanics internal. |
| Failure or timeout | Failure class, redacted evidence, task code, requestId/ECID when available, last state, elapsed time, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Executable contract contains TBD or inferred values | Do not construct an ESS payload or call the submitter. |
| Browser, UI automation, another loader, or direct REST is proposed as a shortcut | Do not bypass the declared ESS enablement gate. |
| A Version value is available | Do not transform, replace, or separately reinterpret it before sending it as argument3. |
| A POST outcome is uncertain | Do not replay the POST without exact reconciliation and explicit approval. |
| Tokens, secrets, authorization headers, or sensitive hierarchy data are present | Do not print or persist them. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PHG.EXECUTION_GATE | decision | 5 | execution_gate | ready->PHG.READY;blocked->PHG.RETURN_ISSUES | PHG.DESIGN_GATE | stop | Confirm the complete source-backed contract, exact target, immutable preview, checkpoint plan, retry restrictions, and one consolidated approval bound to all of them. |
| PHG.READY | terminal | 6 | terminal | none | PHG.EXECUTION_GATE | continue | Request is validated and ready for its owning executor after the enablement gate is complete. |
| PHG.RETURN_ISSUES | terminal | 7 | terminal | none | none | continue | Validation, dependency, design, contract, approval, or execution readiness is blocked. |
