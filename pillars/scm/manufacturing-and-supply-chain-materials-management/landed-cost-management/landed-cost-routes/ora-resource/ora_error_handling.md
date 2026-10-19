# Landed Cost Routes Error Handling

Source: Oracle, [Manage Routes](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/faims/manage-routes.html) (25D), and the task's `core.data-loader` import route.

## Error Situations

| Situation | What Should Happen |
|---|---|
| The published landedCostRoutes Data Loader create contract is unavailable or no longer validates | Stop before preview or submission. Regenerate and validate the Data Loader sample; do not substitute an annotation-derived display name or a direct REST route. |
| A route load is requested through anything other than core.data-loader | Stop before preview or submission. Route the request through core.data-loader using the registered landedCostRoutes business object. |
| A RouteId-dependent operation has no unique RouteCode lookup result | Stop before preview or submission. Do not guess RouteId or issue a direct REST write; correct the RouteCode or resolve the data ambiguity, then restart validation. |
| Input validation or dependency readiness fails | Return the missing input or contract requirement and do not prepare a live request. |
| A live Data Loader request fails or has an indeterminate outcome | Preserve sanitized diagnostics and stop before retrying or issuing another create request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Supplied route data does not conform to the registered Data Loader contract | Correct the data and validate again. |
| Contract blocker | The published landedCostRoutes create contract cannot be validated | Regenerate the registered landedCostRoutes sample through core.data-loader and correct the confirmed discrepancy. |
| Process failed | Fusion rejects a submitted request | Preserve the returned diagnostic and correct the confirmed issue before a new approved attempt. |
| Lookup mismatch | The documented RouteCode lookup returns zero or multiple exact matches | Stop before Data Loader preparation and correct the route identity. |
| Process timeout | Submission status is indeterminate | Stop and reconcile the route through an approved read path before any retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before a live import | Exact target environment, registered business object, validated route data, intended create or update operation, and the approval requirement. |
| Before a RouteId-dependent import | RouteCode, uniquely resolved RouteId, target environment, intended operation, and the approval requirement. |
| After a failed or indeterminate import | Environment, operation, known status, sanitized diagnostic, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Published Data Loader create contract is unavailable | Do not construct a direct REST path, substitute an annotation-derived display name, or submit an unvalidated artifact. |
| RouteId cannot be resolved uniquely | Do not guess a RouteId, submit a delete archive without RouteId, or issue a direct REST write. |
| The selected load route is not core.data-loader | Do not load Landed Cost Routes through a direct REST request, database update, or another executor. |
| Approval is absent or no longer matches the preview | Do not create or update a route. |
| A create outcome is indeterminate | Do not retry the create automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_ROUTES.EXECUTION_GATE | step | 60 | execution_gate | preview-ready-and-approved->RETURN_SUCCESS;contract-missing-or-approval-absent->RETURN_ISSUES | LANDED_COST_ROUTES.ENFORCE_DATA_LOADER_ROUTE | stop | The Data Loader contract and route input have passed validation, and a live import is requested. |
| RETURN_SUCCESS | terminal | 70 | terminal | none | LANDED_COST_ROUTES.EXECUTION_GATE | continue | The validated route request is ready for its separate explicit import approval. |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | continue | An input, contract, dependency, preview, approval, or execution gate failed. |
