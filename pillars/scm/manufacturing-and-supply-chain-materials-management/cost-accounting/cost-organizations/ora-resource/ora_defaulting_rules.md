# Defaulting Rules

## Source

- Oracle Fusion Cloud SCM, [Create a Cost Organization](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-a-cost-organization.html)
- User-verified Data Loader Status constraint: the loader supports only `A` (Active) and `I` (Inactive).


## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Effective Start Date | Leave blank for the Fusion default | Effective Start Date is not provided | No | |
| Effective Start Date | Resolved EffectiveStartDate | CopyExistingOrgFlag is true | Yes, after approval when a user-supplied date differs | resolve_non_cost_organization_exact |
| Status | `A` | Create a cost organization and Status is not provided | Yes | |
| Status | No default | Update an existing Cost Organization and Status is not supplied | No | |

## Status Normalization

Before constructing the Data Loader payload, normalize a supplied Status value as follows:

| Supplied value | Data Loader value | Result |
|---|---|---|
| blank | `A` | Default to Active. |
| `Active` | `A` | Normalize to the supported active code. |
| `Inactive` | `I` | Normalize to the supported inactive code. |
| `A` | `A` | Preserve. |
| `I` | `I` | Preserve. |
| any other value | none | Stop with input validation; do not create the payload. |

Compare the supplied descriptive values case-insensitively after trimming surrounding whitespace. The Data Loader payload must contain only `A` or `I`.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCO.DEFAULT_EFFECTIVE_DATE | decision | 6 | apply_default | defaulted->CCO.DONE_DEFAULTED;supplied->CCO.DONE_SUPPLIED | CCO.DEPENDENCIES | stop | Create a cost organization |
| CCO.NORMALIZE_STATUS | decision | 2 | apply_default | normalized->CCO.RESOLVE_EXISTING_ORGANIZATION;invalid->CCO.HANDLE_ISSUE | CCO.VALIDATE | stop | Default or normalize Status before further workflow processing |
| CCO.UPDATE_NORMALIZE_STATUS | decision | 12 | apply_default | normalized->CCO.UPDATE_ALLOWED_FIELDS;invalid->CCO.HANDLE_ISSUE | CCO.VALIDATE | stop | Update an existing Cost Organization; normalize Status only when supplied and do not apply the create default |
