# Manage Common Lookups Design Enforcement

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026
- Exact runtime lookupType must be supplied by the consuming task, user-provided 25 August 2026

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
| Application Lookup Foundation Skill | A Workforce Scheduling requirement depends on a Common Applications lookup | Before proposing or changing a lookup | Use core.fusion-api.apps-common.lookups through manage-lookups; pass lookupType exactly as supplied by the consuming task at runtime when the provider exposes that route | Reuses ApplCore ownership and prevents Workforce Scheduling from duplicating provider CRUD or setup-task logic | One exact nonblank runtime lookupType from the consuming task; preserve Common Lookups, HCM Extended Lookup Code, Manage Common Lookups, and Manage Extended Lookup Codes as FSM source references | Validate the supplied runtime value, query provider, compare current and recommended state, present evidence, obtain user confirmation, then let the provider apply any required change | Provider returns before/after state, validation results, and unresolved gaps | No change when state already meets the product recommendation; stop when the runtime identifier or provider evidence is unresolved | Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026; exact runtime lookupType requirement, user-provided 25 August 2026 |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A lookup configuration change is proposed | Error | query_lookup_provider_state | The provider has not been invoked, current and recommended state have not been compared, or the consuming task did not supply an exact lookupType | Invoke the provider first and show its evidence; request the exact identifier from the consuming task when missing | Yes |
| A provider-owned change is considered | Error | query_lookup_provider_state | The consumer attempts to create, update, delete, or otherwise execute lookup behavior itself | Keep execution and setup-task ownership in the provider; request user confirmation only for a provider-evidenced required change | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| query_lookup_provider_state | Before proposing or applying a lookup configuration change | Exact lookupType supplied by the consuming task; provider current state, recommended state, validation result, and gap result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.ENFORCE_PROVIDER_OWNERSHIP | decision | 20 | design_enforcement | passed->MCL.READY;blocked->MCL.HANDLE_ISSUES | MCL.QUERY_LOOKUP_PROVIDER | stop | Before a lookup recommendation or provider-owned change using the exact runtime identifier |
