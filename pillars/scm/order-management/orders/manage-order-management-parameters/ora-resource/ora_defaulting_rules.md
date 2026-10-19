# Manage Order Management Parameters Defaulting Rules

## Oracle Guidance Source

Default values and conditional behavior in this file are sourced from Oracle's [Manage Order Management Parameters — 26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/manage-order-management-parameters.html#Order-Management-Parameters) guide.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Days to Retry Recovery for Business Events | 5 days | No approved replacement value is supplied | No | |
| Number of Processes for Order Import | 4 | No approved replacement value is supplied | No | |
| Filter Ship-To Addresses by Ship-to Usage | No | No approved replacement value is supplied | No | |
| Relationship for Ship-To Customer | Party Relationships | Customer Relationship Type is Related Customers and no value is supplied | No | |
| Return Control to Users After Requests to Save Sales Orders | No | No approved replacement value is supplied | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORDER_MANAGEMENT_PARAMETERS.APPLY_DOCUMENTED_DEFAULTS | step | 70 | apply_default | defaults-reviewed->ORDER_MANAGEMENT_PARAMETERS.ENFORCE_DOCUMENTED_CONSTRAINTS | ORDER_MANAGEMENT_PARAMETERS.RESOLVE_PARAMETER_VALUES | stop | A documented default is retained or an approved replacement is proposed. |
