# Landed Cost Routes Design Enforcement

Source: User-supplied Landed Cost Routes rule.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | RouteId lookup route | Permit the documented read-only resolve_landed_cost_route_by_code lookup only when RouteId is required. |
| 2 | Data Loader route | Confirm that core.data-loader is the only selected executor for the Landed Cost Routes load. |
| 3 | Registered business object | Use the registered landedCostRoutes business object through core.data-loader. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Landed Cost Routes load is requested | Blocker | | The selected executor is not core.data-loader, or the registered business object is not landedCostRoutes | Route the load only through core.data-loader with the landedCostRoutes business object. The documented read-only RouteId lookup does not change the load executor. | Yes |
| A delete or other RouteId-dependent operation is requested | Blocker | resolve_landed_cost_route_by_code | RouteId is absent, or the lookup has zero or multiple exact RouteCode matches | Resolve one RouteId through the documented unique RouteCode lookup before Data Loader archive preparation. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_landed_cost_route_by_code | Before preview for a delete or other RouteId-dependent operation | RouteId from exactly one RouteCode match | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_ROUTES.ENFORCE_DATA_LOADER_ROUTE | step | 50 | design_enforcement | compliant->LANDED_COST_ROUTES.EXECUTION_GATE;noncompliant->RETURN_ISSUES | LANDED_COST_ROUTES.CHECK_EXECUTION_CONTRACT | stop | Before preview or a live Landed Cost Routes load. |
