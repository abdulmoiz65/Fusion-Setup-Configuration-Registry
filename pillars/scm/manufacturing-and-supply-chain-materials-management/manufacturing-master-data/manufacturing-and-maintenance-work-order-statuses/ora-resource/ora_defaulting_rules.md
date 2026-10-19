# Defaulting Rules

Source: `workOrderStatuses_rest_rules_summary.txt` supplied by the developer.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| WoStatusId | Fusion sequence-generated identifier | Creating a status and no identifier is supplied | No |  |
| SeededFlag | N, making the REST-created status user-defined | Creating a status | No |  |
| Audit and concurrency fields | Fusion-managed audit and version values | Creating or updating a status | No |  |
| WoStatusCode, WoStatusName, WoStatusDescription, WoSystemStatusCode, InactiveDate | No default | The business field is omitted | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOSTATUS.APPLY_DEFAULTS | step | 2 | apply_default | applied->WOSTATUS.LOOKUPS | WOSTATUS.VALIDATE_INPUT | stop | A valid create or update request is being prepared. |
