# Receiving Parameters Dependency Readiness

## Readiness Rules

| Dependency | Status | Evidence | Handling |
|---|---|---|---|
| Registered Data Loader business object | Ready | `receivingOrganizationParameters` resolved from configured-environment Data Loader metadata. | Route import preparation through `core.data-loader`. |
| Organization and Default Delivery Cart | BO-owned | User confirmed these resolvers are handled by the registered business object. | Do not add task-local lookup or normalization rules. |
| Job Set | Conditional | Redwood Receiving Setup displays `JobSetDisplayName` while its selected value is `JobSetName`, using the RCV-scoped Job Set LOV. | Run `resolve_receiving_parameter_job_set` when either a display name or Job Set name is supplied. |
| Standard lookup-backed values | Conditional | Redwood Receiving Setup maps display `Meaning` values to `LookupCode`. | Run `resolve_receiving_parameter_standard_lookup` only when a supported field is supplied as a display value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RCV_PARAMS.CHECK_READINESS | step | 20 | resolve_dependency | ready->RCV_PARAMS.RESOLVE_STANDARD_LOOKUPS;blocked->RCV_PARAMS.RETURN_ISSUES | RCV_PARAMS.NORMALIZE_INPUT | stop | A Receiving Parameters request has passed local normalization scope checks. |
