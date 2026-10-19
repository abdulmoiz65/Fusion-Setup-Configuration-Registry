# Manage Resource Lookups Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Lookup REST accessibility | Determine whether the requested lookup is accessible to the caller before resolving or changing values |
| 2 | Lookup configuration level | Determine editability before planning a lookup-type or lookup-code change |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MRL.ACCESS | Lookup REST accessibility | Yes | Every request | Lookup | GET /fscmRestApi/resources/11.13.18.05/standardLookups/<exact supported lookup type>?expand=lookupCodes through core.fusion-api.apps-common | resolve_lookup_accessibility | REST visibility can be secured and is Secure by default | Obtain the required security access | REST Access Secured setting and accessibility result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The documented lookup contract resolves accessibility | Yes |
| Blocked | The lookup is secured, inaccessible, or its task-specific REST contract is TBD | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRL.RESOLVE_ACCESS | step | 2 | resolve_dependency | ready->MRL.RESOLVE_LOOKUP;blocked->MRL.RETURN_ISSUES | MRL.VALIDATE_INPUT | stop | Every request |
