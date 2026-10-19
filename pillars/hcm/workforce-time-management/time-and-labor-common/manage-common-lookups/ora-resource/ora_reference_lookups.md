# Common Applications Provider Lookup

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_application_lookup_foundation | A configuration proposal requires a Common Applications lookup and the consuming skill supplies lookupType | Each exact lookupType supplied by the consuming skill at runtime | Documented read-only workflow in `core.fusion-api.apps-common.lookups`; guidance under core/fusion-api/apps-common/lookups/references | Current state, product-recommended comparison evidence, validation result, unresolved provider gap | Pass each consuming-skill lookupType unchanged; provider verifies the product LookupType | Before state, recommended state, validation result, provider gap | If an applicable lookupType is missing, return a missing-input gap and stop before a proposal; do not derive an identifier from an FSM source reference |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The consuming skill did not supply an applicable lookupType | Do not invoke the provider; return a missing-input gap. |
| Provider evidence is returned | Pass the evidence to the design gate; the consuming skill does not perform provider CRUD. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.QUERY_APPLICATION_LOOKUPS | step | 1 | reference_lookup | evidence->MCL.COMPARE_PROVIDER_STATE;identifier_missing->MCL.PROVIDER_GAP;provider_gap->MCL.PROVIDER_GAP | none | stop | A Common lookup configuration proposal is requested |
