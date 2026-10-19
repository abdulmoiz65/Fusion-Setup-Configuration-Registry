# Manage Common Lookups Provider Lookup

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026
- Exact runtime lookupType must be supplied by the consuming task, user-provided 25 August 2026

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_lookup_provider_state | A Workforce Scheduling implementation proposes a lookup resolution after the consuming task supplies lookupType. | Provider product/team Common Applications / ApplCore; provider route core.fusion-api.apps-common.lookups; route manage-lookups; exact lookupType supplied by the consuming task at runtime; FSM source references Common Lookups, HCM Extended Lookup Code, Manage Common Lookups, and Manage Extended Lookup Codes. | Invoke the provider skill through manage-lookups with lookupType only; the provider owns lookup resolution and all read and CRUD behavior. | Current state, product-recommended state, validation evidence, and returned LookupCode values for lookupType. | Require one exact nonblank runtime lookupType supplied by the consuming task and pass it unchanged. Do not send LookupCode as a provider input; the provider resolves and returns eligible LookupCode values. | Before state, recommended state, validation result, returned LookupCode values, and provider gap. | Stop and request the exact lookupType from the consuming task when it is missing, or report the provider gap; do not construct a provider request or clone provider CRUD behavior. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A configuration change is proposed | Invoke the named provider before presenting a recommendation and retain its before-state and validation evidence. |
| The provider exposes an API route | Pass lookupType exactly as supplied by the consuming task. Do not pass LookupCode; retain only provider-returned eligible LookupCode values as evidence. |
| The provider identifies no required difference | Do not apply a change. |
| The provider identifies a required difference | Present the provider evidence and obtain user confirmation immediately before the provider-owned change. |
| The consuming task does not provide the exact product identifier | Preserve the four FSM source references, record the missing runtime input, and stop. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.QUERY_LOOKUP_PROVIDER | step | 10 | reference_lookup | resolved->MCL.ENFORCE_PROVIDER_OWNERSHIP;blocked->MCL.HANDLE_ISSUES;failure->MCL.HANDLE_ISSUES | MCL.VALIDATE_PROVIDER_INPUT | stop | Before proposing a lookup configuration change with the exact runtime identifier supplied by the consuming task |
