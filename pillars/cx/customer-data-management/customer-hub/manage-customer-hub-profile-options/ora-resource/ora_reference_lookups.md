# Reference Lookups

Use only read-only Apps Common profile-option reads to verify Customer Hub option membership, SITE eligibility, configured state, and validation metadata. These lookups do not write a value or select an import adapter.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_customer_hub_profile_definition | A view, update, documented-default request, or changed FND_APP_PROFILE_VALUE row identifies a profile code | Exact ProfileOptionName and SITE level | GET /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}, then GET its child/siteProfileOptionValues/SITE through core.fusion-api.apps-common | ProfileOptionName, SqlValidation, SiteLevelEnabled, SiteLevelUpdatable, ProfileOptionValue, level key | Match exactly one supported Customer Hub profile definition and at most one configured SITE record | Current SITE value, SITE enabled/updatable flags, SITE key, and validation metadata | Stop when the definition is missing, ambiguous, non-site, disabled, non-updatable for a change, or inconsistent with the enclosing inventory |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| View or update names one supported code | Read that exact definition and SITE record; never search by display-name approximation |
| A changed FSM profile-value row is proposed | Read each exact changed ProfileOptionName before building the immutable preview |
| The profile has no configured SITE row | Report the definition and missing configured value; creation still requires an exact approved preview |
| SqlValidation or current definition exposes allowed values | Preserve those values as authoritative runtime evidence; do not copy or evaluate undocumented SQL locally |
| A read returns a privilege, transport, or metadata failure | Stop before preview and do not substitute a browser, guessed value, or another profile level |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHP.READ_PROFILE_OPTION | step | 2 | reference_lookup | resolved->CHP.DEPENDENCY_READINESS;unresolved->CHP.ERROR | CHP.VALIDATE_CONTEXT | stop | Before preview whenever a profile definition or configured SITE value must be verified |
