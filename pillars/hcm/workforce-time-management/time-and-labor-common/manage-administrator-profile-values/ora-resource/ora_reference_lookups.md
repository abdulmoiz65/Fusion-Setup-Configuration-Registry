# Common Applications Provider Lookup

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_profile_option_foundation | A configuration proposal requires an administrator profile value and the consuming skill supplies profileOptionCode | Exact profileOptionCode supplied by the consuming skill at runtime | core.fusion-api.apps-common.profile-options route manage-profile-options | Current state, product-recommended comparison evidence, validation result, unresolved provider gap | Pass the consuming-skill profileOptionCode unchanged; provider verifies the product ProfileOptionName | Before state, recommended state, validation result, provider gap | If profileOptionCode is missing, return a missing-input gap and stop before a proposal; do not derive an identifier from the FSM source reference |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The consuming skill did not supply profileOptionCode | Do not invoke the provider; return a missing-input gap. |
| Provider evidence is returned | Pass the evidence to the design gate; the consuming skill does not perform provider CRUD. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAPV.QUERY_PROFILE_OPTION | step | 1 | reference_lookup | evidence->MAPV.COMPARE_PROVIDER_STATE;identifier_missing->MAPV.PROVIDER_GAP;provider_gap->MAPV.PROVIDER_GAP | none | stop | An administrator profile-value configuration proposal is requested |
