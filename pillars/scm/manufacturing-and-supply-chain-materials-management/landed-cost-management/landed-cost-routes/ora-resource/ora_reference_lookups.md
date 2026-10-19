# Landed Cost Routes Reference Lookups

Source: User-supplied RouteId lookup contract for Landed Cost Routes.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_landed_cost_route_by_code | A Landed Cost Routes operation requires RouteId, including a delete request, after RouteCode passes input validation and before Data Loader archive preparation | User-provided RouteCode | /fscmRestApi/resources/11.13.18.05/landedCostRoutes?q=RouteCode='<RouteCode>' | RouteId; RouteCode | Require exactly one returned record whose RouteCode exactly equals the user-provided RouteCode | RouteId from the unique returned record | No match: stop and report that the route code was not found. Many matches: stop and report the RouteCode lookup is ambiguous; do not select a record. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The operation does not require RouteId | Do not call the lookup; continue to the Data Loader execution-contract check. |
| The operation requires RouteId and the RouteCode lookup returns exactly one record | Use the returned RouteId only to populate the Data Loader request; keep core.data-loader as the only Fusion load executor. |
| The lookup has no exact match or more than one match | Stop before preview, preserve sanitized lookup evidence, and request a corrected RouteCode or resolve the data issue. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_ROUTES.RESOLVE_ROUTE_ID | decision | 30 | reference_lookup | resolved->LANDED_COST_ROUTES.CHECK_EXECUTION_CONTRACT;not-required->LANDED_COST_ROUTES.CHECK_EXECUTION_CONTRACT;unresolved->RETURN_ISSUES | LANDED_COST_ROUTES.DEFAULT_INACTIVE_FLAG | stop | A Landed Cost Routes operation requires RouteId, including a delete request. |
