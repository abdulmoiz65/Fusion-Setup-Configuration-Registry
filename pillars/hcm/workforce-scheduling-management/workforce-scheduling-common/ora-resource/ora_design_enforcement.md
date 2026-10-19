# Workforce Scheduling Common Provider Design Enforcement

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 31 August 2026

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Receive identifier | Receive the exact product identifier from the consuming skill for the applicable provider route; retain FSM source references as traceability only. |
| 2 | Invoke provider | Query or invoke the named Common Applications provider before proposing a configuration change. |
| 3 | Compare state | Retain and compare the provider-returned current state with the provider's product-recommended state. |
| 4 | Confirm required change | Present before state, recommended state, validation result, and unresolved gap; obtain user confirmation immediately before a provider-owned change. |
| 5 | Preserve ownership | Keep setup-task ownership, validation, execution, and CRUD behavior in the provider skill. |

## Provider Dependency Best Practices

| Provider Dependency | Business Scenario | When to Use It | Recommended Configuration | Rationale | Prerequisites | Invocation Order | Validation | Exceptions | Source |
|---|---|---|---|---|---|---|---|---|---|
| Application Profile Option Foundation Skill | A Workforce Scheduling outcome depends on a Common Applications profile option. | Before proposing or changing a profile option. | Invoke core.fusion-api.apps-common.profile-options through manage-profile-options with the profileOptionCode supplied by the consuming skill, unchanged. Preserve Manage Administrator Profile Values as the FSM source reference. | The provider owns profile-option definition, state validation, setup-task behavior, and CRUD; the consumer must not recreate those capabilities. | The consuming skill supplies one exact product profileOptionCode. Manage Administrator Profile Values alone is not a runtime identifier. | Receive profileOptionCode from the consuming skill, invoke the provider, compare current and product-recommended state, present evidence, obtain user confirmation, then let the provider apply any required change. | Return before state, after state when changed, validation result, and unresolved provider gap. | Make no change when current state meets the recommendation. Stop when the consuming skill omits the identifier, state is ambiguous, or provider evidence is unavailable. | Workforce Scheduling Common Applications provider-dependency contract, user-provided 31 August 2026; consuming-skill identifier authority, user-provided 31 August 2026. |
| Application Lookup Foundation Skill | A Workforce Scheduling outcome depends on a Common Applications lookup. | Before proposing or changing a lookup. | Invoke core.fusion-api.apps-common.lookups.references through manage-lookups with the lookupType supplied by the consuming skill, unchanged. Preserve Manage Common Lookups and Manage Extended Lookup Codes as FSM source references; retain Common Lookups and HCM Extended Lookup Code as supplied lookup-source labels. | The provider owns lookup resolution, state validation, setup-task behavior, and CRUD; the consumer must not recreate those capabilities. | The consuming skill supplies one exact product lookupType. The supplied FSM source references and lookup-source labels are not runtime identifiers. | Receive lookupType from the consuming skill, invoke the provider, compare current and product-recommended state, present evidence, obtain user confirmation, then let the provider apply any required change. | Return before state, after state when changed, validation result, and unresolved provider gap. | Make no change when current state meets the recommendation. Stop when the consuming skill omits the identifier, state is ambiguous, or provider evidence is unavailable. | Workforce Scheduling Common Applications provider-dependency contract, user-provided 31 August 2026; consuming-skill identifier authority, user-provided 31 August 2026. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile-option change is proposed. | Error | query_profile_option_provider_state | The consuming skill did not supply one exact profileOptionCode, the provider has not been invoked, or current and recommended state have not been compared. | Stop, request profileOptionCode from the consuming skill, invoke the provider, and show its evidence before proposing a change. | Yes |
| A lookup change is proposed. | Error | query_lookup_provider_state | The consuming skill did not supply one exact lookupType, the provider has not been invoked, or current and recommended state have not been compared. | Stop, request lookupType from the consuming skill, invoke the provider, and show its evidence before proposing a change. | Yes |
| A provider-owned change is considered. | Error | Provider invocation evidence | The consuming skill attempts to implement provider execution, CRUD, validation, or setup-task behavior. | Keep the change in the provider skill and require current user confirmation for the exact provider-owned change. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| query_profile_option_provider_state | Before a profile-option recommendation or change. | profileOptionCode supplied by the consuming skill; provider current state; product-recommended state; validation result; unresolved provider gap. | ora_reference_lookups.md |
| query_lookup_provider_state | Before a lookup recommendation or change. | lookupType supplied by the consuming skill; provider current state; product-recommended state; validation result; unresolved provider gap. | ora_reference_lookups.md |
