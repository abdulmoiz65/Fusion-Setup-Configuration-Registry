# Manage Resource Lookups Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_lookup_accessibility | Every request after input validation | Exact lookup type | GET /fscmRestApi/resources/11.13.18.05/standardLookups/<exact supported lookup type>?expand=lookupCodes through core.fusion-api.apps-common | Configuration level, REST Access Secured, lookup code, translated meaning, tag, enabled status | Require one exact lookup type | Lookup accessibility and configuration facts | Stop and report the match is unresolved |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Task-specific read path is not documented by the supplied sources | Retain the lookup as TBD and block execution planning |
| Lookup REST access is Secure | Stop and request the required function security policy or an authorized role |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRL.RESOLVE_LOOKUP | step | 3 | reference_lookup | resolved->MRL.ENFORCE_CONFIGURATION;unresolved->MRL.RETURN_ISSUES | MRL.RESOLVE_ACCESS | stop | Every request |
