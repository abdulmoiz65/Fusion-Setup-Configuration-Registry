# Landed Cost Routes Input Validation

Source: Oracle, [Manage Routes](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25d/faims/manage-routes.html) (25D); user-provided functional-input requirement; and user confirmation that the published top business-object name is landedCostRoutes.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Route identity | Business route code or identifier | Stop before Data Loader preparation | Ask the business user for the route code or identifier | A route create is requested | |
| Route details | Business route name and description | Stop before Data Loader preparation | Ask the business user to name and describe the route | A route create is requested | |
| Route availability | Active or inactive status stated in business terms, or no status so that Active is derived | Stop before Data Loader preparation | Ask for Active or Inactive when the default Active status is not intended | A route create is requested | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Functional input format | Accept business-user prose, a form, or a spreadsheet row. Do not require JSON or implementation attribute names from the business user. For a create, map confirmed values to RestAction POST, RouteCode, RouteName, RouteDescription, and InactiveFlag through core.data-loader. | Before preparing a Data Loader request | |
| Route code | Require a business route identifier and map it to RouteCode. Validate duplicate and create behavior through core.data-loader against the published landedCostRoutes object. | Before preparing a Data Loader request | |
| Route availability | Accept Active or Inactive in business terms. When the business user does not state a status, derive Active. Internally, Active maps to InactiveFlag false and N; Inactive maps to InactiveFlag true and Y. | Before Data Loader preparation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_ROUTES.VALIDATE_INPUT | step | 10 | validate_input | validated->LANDED_COST_ROUTES.DEFAULT_INACTIVE_FLAG;invalid->RETURN_ISSUES | none | stop | Before preparing a Landed Cost Routes Data Loader request from functional business input. |
