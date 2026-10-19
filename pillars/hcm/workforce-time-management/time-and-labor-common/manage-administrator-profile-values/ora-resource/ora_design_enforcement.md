# Common Applications Provider Best Practices

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Accept runtime identifier | Require profileOptionCode from the consuming skill and pass it unchanged without separate PM confirmation. |
| 2 | Query provider | Invoke Application Profile Option Foundation Skill through core.fusion-api.apps-common.profile-options route manage-profile-options. |
| 3 | Compare evidence | Show provider before state beside the product-recommended state and validation result. |
| 4 | Gate proposal | Propose a provider-owned change only when the implementation outcome requires it and the user explicitly confirms it. |

## Provider Best-Practice Entries

| Dependency | Business Scenario | When to Use It | Recommended Configuration | Rationale | Prerequisites | Invocation Order | Validation | Exceptions | Source |
|---|---|---|---|---|---|---|---|---|---|
| Application Profile Option Foundation Skill, Common Applications / ApplCore | An administrator profile value may affect the requested Time and Labor outcome | Before proposing a profile-value configuration change | Invoke core.fusion-api.apps-common.profile-options route manage-profile-options with the profileOptionCode supplied by the consuming skill; pass it unchanged and use provider evidence only | Provider owns execution, CRUD behavior, and profile-option setup-task ownership | Exact runtime profileOptionCode from the consuming skill | 2 | Compare provider current state with product-recommended state; return before/after, validation result, and provider gap | If profileOptionCode is missing or evidence is incomplete, stop and return the gap; consuming skill performs no provider CRUD | User-provided implementation contract; FSM source Manage Administrator Profile Values |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile-value configuration proposal is requested | Error | query_profile_option_foundation | The consuming skill did not supply profileOptionCode, provider evidence is missing, or provider validation reports a gap | Pass the consuming-skill value unchanged, preserve provider ownership, and show current versus recommended state before a proposal | Yes, by supplying profileOptionCode or resolving the provider gap; never by cloning provider behavior |
| A provider-owned profile-value change is proposed | Error | query_profile_option_foundation | Requested change is not required by the implementation outcome or lacks explicit user confirmation | Return the comparison and seek confirmation for the exact provider target and change | Yes, after explicit user confirmation through the provider workflow |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| query_profile_option_foundation | Before a profile-value configuration proposal | Before state, recommended state, validation result, provider gap | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAPV.COMPARE_PROVIDER_STATE | decision | 2 | design_enforcement | ready_to_propose->MAPV.PROPOSAL_READY;provider_gap->MAPV.PROVIDER_GAP | MAPV.QUERY_PROFILE_OPTION | stop | Provider evidence is available |
