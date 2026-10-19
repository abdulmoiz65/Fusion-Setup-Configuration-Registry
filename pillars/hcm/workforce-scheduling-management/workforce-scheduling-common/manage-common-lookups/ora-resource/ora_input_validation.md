# Manage Common Lookups Input Validation

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026
- Runtime provider identifier requirement, user-provided 19 August 2026
- Exact runtime lookupType must be supplied by the consuming task, user-provided 25 August 2026

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Provider identifier | Exact lookupType supplied by the consuming task | Block before the provider lookup or any recommendation | Require the consuming task to supply the exact lookupType for the requested configuration change; do not infer it from an FSM source reference or a lookup-category label | A lookup configuration change is proposed |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A consuming task supplies lookupType | Continue when one exact nonblank runtime value is present | Pass the supplied lookupType unchanged to the provider lookup; do not replace, normalize, or infer it | query_lookup_provider_state |
| The consuming task does not supply lookupType | Stop before provider lookup | Request the exact lookupType from the consuming task |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.VALIDATE_PROVIDER_INPUT | step | 5 | validate_input | valid->MCL.QUERY_LOOKUP_PROVIDER;blocked->MCL.HANDLE_ISSUES | none | stop | Before a lookup provider lookup or recommendation |
