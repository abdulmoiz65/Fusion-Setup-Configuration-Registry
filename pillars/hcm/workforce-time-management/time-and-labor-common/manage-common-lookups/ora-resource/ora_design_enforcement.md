# Common Applications Provider Best Practices

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Accept runtime identifier | Require each applicable lookupType from the consuming skill and pass it unchanged without separate PM confirmation. |
| 2 | Query provider | Read the applicable guidance under core/fusion-api/apps-common/lookups/references, then use the documented read-only workflow in `core.fusion-api.apps-common.lookups`. |
| 3 | Compare evidence | Show provider before state beside the product-recommended state and validation result. |
| 4 | Gate proposal | Propose a provider-owned change only when the implementation outcome requires it and the user explicitly confirms it. |

## Provider Best-Practice Entries

| Dependency | Business Scenario | When to Use It | Recommended Configuration | Rationale | Prerequisites | Invocation Order | Validation | Exceptions | Source |
|---|---|---|---|---|---|---|---|---|---|
| Application Lookup Foundation Skill, Common Applications / ApplCore | A Common Applications lookup may affect the requested Time and Labor outcome | Before proposing a lookup-dependent configuration change | Read core/fusion-api/apps-common/lookups/references, then use `core.fusion-api.apps-common.lookups` with each exact lookupType supplied by the consuming skill; pass every value unchanged and use provider evidence only | Provider owns execution, CRUD behavior, and lookup setup-task ownership | Each applicable exact runtime lookupType from the consuming skill | 2 | Compare provider current state with product-recommended state; return before/after, validation result, and provider gap | If an applicable lookupType is missing or evidence is incomplete, stop and return the gap; consuming skill performs no provider CRUD | User-provided implementation contract; FSM sources Common Lookups, HCM Extended Lookup Code, Manage Common Lookups, Manage Extended Lookup Codes |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A lookup-dependent configuration proposal is requested | Error | query_application_lookup_foundation | The consuming skill did not supply an applicable lookupType, provider evidence is missing, or provider validation reports a gap | Pass each consuming-skill value unchanged, preserve provider ownership, and show current versus recommended state before a proposal | Yes, by supplying lookupType or resolving the provider gap; never by cloning provider behavior |
| A provider-owned lookup change is proposed | Error | query_application_lookup_foundation | Requested change is not required by the implementation outcome or lacks explicit user confirmation | Return the comparison and seek confirmation for the exact provider target and change | Yes, after explicit user confirmation through the provider workflow |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| query_application_lookup_foundation | Before a lookup-dependent configuration proposal | Before state, recommended state, validation result, provider gap | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.COMPARE_PROVIDER_STATE | decision | 2 | design_enforcement | ready_to_propose->MCL.PROPOSAL_READY;provider_gap->MCL.PROVIDER_GAP | MCL.QUERY_APPLICATION_LOOKUPS | stop | Provider evidence is available |
