# Reference Lookups

Use only read-only Apps Common profile-option reads to verify the target state needed for a profile-value change plan. Do not use these lookups to write a value or select an import adapter.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_profile_option_definition | A changed FND_APP_PROFILE_VALUE row is proposed for import, or view/update requests identify a profile code | Exact ProfileOptionName and requested level | /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName} and the matching level-specific child resource documented by core.fusion-api.apps-common | ProfileOptionName, level enabled/updatable flags, configured level key, ProfileOptionValue | Match exactly one profile definition and one configured record at the requested level | Current value, enabled flag, updatable flag, level key | Stop before preview when the definition or requested level is missing, ambiguous, disabled, or non-updatable |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The request is import and no profile-value row changes | Do not run a profile definition lookup solely to inspect unrelated values |
| The request changes one or more profile-value rows | Read each exact changed ProfileOptionName before building the immutable preview |
| A read returns a privilege or transport failure | Stop before preview; classify the failure and do not substitute a browser or guessed value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CTCP.READ_PROFILE_OPTION | step | 2 | reference_lookup | resolved->CTCP.DEPENDENCY_READINESS;unresolved->CTCP.ERROR | CTCP.VALIDATE_CONTEXT | stop | Before preview whenever changed profile-value rows require target-state verification |
