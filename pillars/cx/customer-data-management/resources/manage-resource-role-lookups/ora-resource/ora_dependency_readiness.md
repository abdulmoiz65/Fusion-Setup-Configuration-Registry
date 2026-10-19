# Manage Resource Role Lookups Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Lookup REST accessibility | Determine whether the requested resource-role lookup is accessible to the caller before resolving or changing values |
| 2 | Lookup configuration level | Determine editability before planning a lookup-type or lookup-code change |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MRRL.ACCESS | Resource-role lookup REST accessibility | Yes | Every request | Lookup | GET /fscmRestApi/resources/11.13.18.05/standardLookups/JTF_RS_ROLE_TYPE?expand=lookupCodes through core.fusion-api.apps-common | resolve_resource_role_lookup_accessibility | The role type must be visible and exactly match a returned LookupCode before it can be used | Obtain the required function security policy or an authorized role when the read returns HTTP 401 or 403 | Lookup accessibility result and validated LookupCode values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The documented standard-lookup GET resolves accessibility and exact role-type code matches | Yes |
| Blocked | The lookup is secured, inaccessible, absent, or a required exact LookupCode is unresolved | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRRL.RESOLVE_ACCESS | step | 2 | resolve_dependency | ready->MRRL.RESOLVE_LOOKUP;blocked->MRRL.RETURN_ISSUES | MRRL.VALIDATE_INPUT | stop | Every request |
