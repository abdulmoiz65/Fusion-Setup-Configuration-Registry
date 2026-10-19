# AutoInvoice Grouping Rule Error Handling

Sources: SRC-CODE-AMIMPL, SRC-CODE-PRIMARY-EO, SRC-CODE-CLASS-EO, SRC-CODE-GROUPBY-EO. Run Book and Data Loader own package submission, preview, approval and verification.

## Error Situations

| Situation | What Should Happen |
|---|---|
| LineOrderingRuleName has no exact match | Report the affected root row and supplied name; correct the reference before another preview. |
| FromColumnName has no exact match | Report the affected child row and supplied name; confirm the target-pod characteristic before another preview. |
| Duplicate class within a grouping rule | Report AR_SU_DEFGR_DUPCLASS and the affected class; stop. |
| Duplicate group-by column within a class | Report AR_SU_DEFGR_DUPCOL and the affected characteristic; stop. |
| A non-key update field contract or resolver behavior remains unverified | Classify evidence_unresolved; apply known validations and offer exact-field application-validation acceptance for eligible uncertainty. Do not claim Fusion rejects it. Preserve hard identity/key/audit/package/known-value controls and normal import approval. |
| DFF or consolidated-billing create inputs remain unverified | Preserve the existing conditional create checks; do not invent values or deployed configuration. |
| Import outcome uncertain | Preserve process diagnostics and reconcile through read-only export before considering another submission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Candidate preview | Bind exact task, environment, three CSV members plus metadata, field changes and unresolved applicable behavior in the validation context required by the selected Core Data Loader workflow. Display its required user-facing preview and follow that workflow's integrity and approval-artifact handling. |
| Import failure | Process identifier, sanitized log, affected rows and verified persisted state when available. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing candidate-specific approval | Do not submit an import or change Fusion data. |
| Changed candidate after preview | Do not reuse the prior approval; regenerate preview and request fresh approval. |
| Uncertain prior submission | Do not automatically retry; reconcile first. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIGR.GATE | step | 4 | execution_gate | pass->AIGR.DONE;blocked->AIGR.ISSUES | AIGR.ENFORCE | stop | Candidate handoff |
| AIGR.DONE | terminal | 5 | terminal | none | AIGR.GATE | stop | Static checks and preview readiness pass |
| AIGR.ISSUES | terminal | 6 | terminal | none | none | stop | A blocking condition is found |
