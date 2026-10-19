# Reporting Hierarchy Generation Error Handling

Source: [Oracle Reporting Hierarchy Generation](https://docs.oracle.com/en/cloud/saas/sales/fauss/reporting-hierarchy-generation.html).

## Error Situations

| Situation | What Should Happen |
|---|---|
| A mandatory parameter is missing or invalid | Stop and request the required Tree Structure Code, Tree Code, or Tree Version ID. |
| Tree Code discovery has no candidates, fails, or returns an incomplete response | Return a read-only diagnostic and an empty candidate list. Do not infer, select, persist, or submit a Tree Code or Tree Version ID. |
| Tree Version discovery has no candidates, fails, or returns an incomplete response | Return a read-only diagnostic and an empty candidate list. Do not infer, select, persist, or submit a Tree Version ID. |
| Discovery response is paginated | Retrieve every page before presenting candidates; do not silently truncate the candidate list. |
| The `fndTrees` lookup does not return the supplied Tree Structure Code and Tree Code as an exact pair | Stop before ESS submission and report that the Tree Code is not valid for the selected Tree Structure Code. |
| The `fndTrees` lookup fails or is incomplete | Stop before ESS submission and report the lookup outcome; do not assume the Tree Code is valid. |
| The `fndTreeVersions` lookup does not return exactly one TreeVersionId equal to the supplied version | Stop before ESS submission and report that the Tree Version ID is not valid for the selected Tree Structure Code and Tree Code. |
| The matched Tree Version is inactive | Report its Status, EffectiveStartDate, EffectiveEndDate, and INACTIVE classification. Classify as INACTIVE only when both EffectiveStartDate and EffectiveEndDate are before the current validation date. Request explicit confirmation to use it. Do not continue until confirmed; require the final approval to confirm all three submitted parameter values. |
| A current-request value is missing and only a prior-request or conversation value is available | Stop and request the value in the current execution request; do not default it. |
| A discovery candidate is available but absent from a later submit request | Stop and request a new complete submit triple. Do not reuse the discovery result. |
| A hierarchy or privilege prerequisite cannot be confirmed | Stop before scheduling and request the missing confirmation or authorized access. |
| The exact execution request is not explicitly approved | Stop before submitting; request approval for the ESS job and all three parameter values. |
| Another Reporting Hierarchy Generation instance is running | Do not submit a parallel instance; wait for the first instance to complete because subsequent instances remain blocked. |
| ESS submission fails or times out | Preserve the request ID and sanitized ESS diagnostics when available; do not automatically resubmit. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | A mandatory parameter is absent or invalid. | Correct the parameter selection. |
| transport/environment | A read-only discovery lookup fails, is incomplete, or cannot retrieve all pages. | Resolve the configured Fusion connection or response issue and rerun the discovery lookup; do not submit ESS. |
| approval_blocker | A parameter value is absent from the current execution request or exact execution approval, or required privilege, hierarchy readiness, or approval is not confirmed. | Obtain the missing current-request value and authorized confirmation; do not substitute a prior value. |
| auth/authz | Fusion rejects the submitting identity or the documented privilege is absent. | Obtain the required privilege; do not retry automatically. |
| process_failed | ESS returns a terminal unsuccessful status. | Preserve diagnostics and correct the reported cause before a newly approved submission. |
| process_timeout | ESS tracking reaches its configured wait timeout, or an existing self-incompatible process prevents submission. | Track the existing request or wait for it to complete; do not submit another instance. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Scheduling blocker | The failed prerequisite or parameter, the reason submission stopped, and the corrective action. |
| Active-instance blocker | That the process is self-incompatible and a subsequent instance remains blocked until the active instance completes. |
| ESS failure | The request ID when available, last returned ESS status, failure class, and recommended next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Another instance is active | Do not submit another Reporting Hierarchy Generation instance. |
| Proven ESS binding is unavailable | Do not use display labels as `requestParameters` names or submit the job. |
| ESS request fails or times out | Do not automatically submit a replacement request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RH.DONE_TREE_CODE_DISCOVERY | terminal | 9 | terminal | none | RH.TREE_CODE_DISCOVERY | stop | Read-only Tree Code discovery returned candidates; no Tree Version or ESS request is bound. |
| RH.DONE_TREE_VERSION_DISCOVERY | terminal | 10 | terminal | none | RH.TREE_VERSION_DISCOVERY | stop | Read-only Tree Version discovery returned candidates; no ESS request is bound. |
| RH.DONE | terminal | 8 | terminal | none | RH.DESIGN | stop | Submit parameters, Tree Code, Tree Version, dependency, explicit approval, and design gates have passed; the delegated ESS submission route is authorized. |
| RETURN_ISSUES | terminal | 11 | terminal | none | none | stop | Any validation, discovery, Tree Code, Tree Version, dependency, approval, privilege, active-instance, or ESS execution blocker occurs. |
