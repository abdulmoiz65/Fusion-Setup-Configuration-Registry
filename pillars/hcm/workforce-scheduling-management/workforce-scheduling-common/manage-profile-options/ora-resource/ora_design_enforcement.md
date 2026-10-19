# Manage Profile Options Design Enforcement

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Provider query | Invoke the Common Applications provider through the documented route before proposing a configuration change. |
| 2 | State comparison | Compare the provider-returned current state with its product-recommended state and retain evidence. |
| 3 | Change gate | Apply a provider-owned change only when the requested implementation outcome requires it and the user confirms the exact change. |
| 4 | Ownership gate | Keep setup-task ownership, query behavior, CRUD behavior, validation, and execution in the provider skill. |

## Provider Dependency Best Practices

| Provider Dependency | Business Scenario | When to Use It | Recommended Configuration | Rationale | Prerequisites | Invocation Order | Validation | Exceptions | Source |
|---|---|---|---|---|---|---|---|---|---|
| Application Profile Option Foundation Skill | A Workforce Scheduling requirement depends on a Common Applications profile option | Before proposing or changing a profile option | Use core.fusion-api.apps-common.profile-options through manage-profile-options; pass the exact profileOptionCode supplied by the consuming task when the provider exposes that route | Reuses ApplCore ownership and prevents Workforce Scheduling from duplicating provider CRUD or setup-task logic | Exact product profileOptionCode requires PM confirmation; preserve Manage Administrator Profile Values as the FSM source reference | Validate runtime input, query provider, compare current and recommended state, present evidence, obtain user confirmation, then let the provider apply any required change | Provider returns before/after state, validation results, and unresolved gaps | No change when state already meets the product recommendation; stop when the runtime identifier or provider evidence is unresolved | Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026 |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile-option configuration change is proposed | Error | query_profile_option_provider_state | The provider has not been invoked, current and recommended state have not been compared, or the consuming task did not supply an exact profileOptionCode | Invoke the provider first and show its evidence; request the exact identifier from the consuming task when missing | Yes |
| A provider-owned change is considered | Error | query_profile_option_provider_state | The consumer attempts to create, update, delete, or otherwise execute profile-option behavior itself | Keep execution and setup-task ownership in the provider; request user confirmation only for a provider-evidenced required change | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| query_profile_option_provider_state | Before proposing or applying a profile-option configuration change | Exact profileOptionCode supplied by the consuming task; provider current state, recommended state, validation result, and gap result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.ENFORCE_PROVIDER_OWNERSHIP | decision | 20 | design_enforcement | passed->MPO.READY;blocked->MPO.HANDLE_ISSUES | MPO.QUERY_PROFILE_OPTION_PROVIDER | stop | Before a profile-option recommendation or provider-owned change using the exact runtime identifier |
