# Manage Resource Role Lookups Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_resource_role_lookup_accessibility | Every request after input validation | Exact resource-role lookup type `JTF_RS_ROLE_TYPE` | GET /fscmRestApi/resources/11.13.18.05/standardLookups/JTF_RS_ROLE_TYPE?expand=lookupCodes through core.fusion-api.apps-common | Lookup type and returned lookup codes | Require one exact lookup type; accept a supplied role type only when one returned LookupCode is an exact match | Lookup accessibility result and validated LookupCode values | Stop on HTTP 401 or 403, an absent lookup type, or an unresolved or duplicate exact LookupCode match |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The caller must validate a resource-role type | Use the documented standard-lookup GET through core.fusion-api.apps-common with REST-Framework-Version: 9; map only exact returned LookupCode matches. |
| Lookup REST access returns HTTP 401 or 403 | Stop and request the required function security policy or an authorized role. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRRL.RESOLVE_LOOKUP | step | 3 | reference_lookup | resolved->MRRL.ENFORCE_CONFIGURATION;unresolved->MRRL.RETURN_ISSUES | MRRL.RESOLVE_ACCESS | stop | Every request |
