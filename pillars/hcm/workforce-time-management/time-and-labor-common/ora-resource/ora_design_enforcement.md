# Time and Labor Common Design Enforcement

## Purpose

Defines Time and Labor business rules and best practices for consuming Common
Applications / ApplCore foundation skills. This consuming skill queries and
compares provider state; provider skills retain execution, CRUD behavior,
request construction, retry policy, verification, and setup-task ownership.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify the dependency | Determine whether the requested Time and Labor outcome depends on a profile option, a Common Applications lookup, both, or neither |
| 2 | Accept the exact runtime identifier | Require the consuming skill to supply profileOptionCode or lookupType; preserve FSM labels only as source references and do not require separate PM confirmation |
| 3 | Query the provider | Invoke the declared provider route with the exact consuming-skill identifier unchanged before proposing a configuration change |
| 4 | Compare evidence | Compare the provider before state with the product-recommended state and show the evidence and validation result |
| 5 | Decide whether change is required | Propose no change when current state already meets the recommendation; otherwise connect the required change to the requested implementation outcome |
| 6 | Confirm the provider-owned change | Obtain explicit user confirmation for the exact target, identifier, operation, and proposed change |
| 7 | Return verified results | Let the provider execute and verify; return before state, after state, validation results, and unresolved gaps |

## Provider Best Practices

| Dependency | Business Scenario | When to Use | Recommended Configuration | Rationale | Prerequisites | Invocation Order | Validation | Exceptions | Source |
|---|---|---|---|---|---|---|---|---|---|
| Application Profile Option Foundation Skill; Common Applications / ApplCore | A Time and Labor implementation outcome depends on an application profile value | Before proposing any profile-option-dependent Time and Labor configuration | Query core.fusion-api.apps-common.profile-options through manage-profile-options with the profileOptionCode supplied by the consuming skill; pass it unchanged and retain provider CRUD and setup-task ownership | Uses the authoritative ApplCore state and prevents duplicate profile-option execution logic in Time and Labor | Requested implementation outcome; target environment; consuming-skill profileOptionCode; provider availability and access | 1 of the applicable Common Applications provider queries; run before comparison or proposal | Compare provider before state with product-recommended state; show evidence; validate that the runtime identifier and target match; after an approved provider change return verified after state | If no profile option affects the outcome, do not invoke; if profileOptionCode is missing or provider evidence is incomplete, return the gap and stop; if state is already recommended, make no change | User-provided implementation contract; FSM source Manage Profile Values |
| Application Lookup Foundation Skill; Common Applications / ApplCore | A Time and Labor implementation outcome depends on Common Applications lookup behavior | Before proposing any lookup-dependent Time and Labor configuration | Read the applicable guidance under core/fusion-api/apps-common/lookups/references, then query core.fusion-api.apps-common.lookups through manage-lookups with each lookupType supplied by the consuming skill; pass every value unchanged and retain provider CRUD and setup-task ownership | Uses the authoritative ApplCore lookup state and prevents Time and Labor from cloning lookup category selection or CRUD behavior | Requested implementation outcome; target environment; consuming-skill lookupType for each applicable lookup; provider skill availability and access | 2 when both provider classes apply; invoke once per supplied lookupType after profile-option evidence and before comparison or proposal | Compare each provider before state with product-recommended state; show identifier-bound evidence; validate the target and provider result; after an approved provider change return verified after state | If no lookup affects the outcome, do not invoke; if lookupType is missing, provider access is unavailable, or evidence is incomplete, return the gap and stop; if state is already recommended, make no change | User-provided implementation contract; provider references core/fusion-api/apps-common/lookups/references; FSM sources Common Lookups, HCM Extended Lookup Code, Manage Common Lookups, and Manage Extended Lookup Codes |

## Exact Identifier Contract

| Provider Skill | Route | Payload Field | Identifier Source | Identifier Status | Required Pass Behavior | Unresolved Gap Behavior |
|---|---|---|---|---|---|---|
| core.fusion-api.apps-common.profile-options | manage-profile-options | profileOptionCode | Consuming skill at runtime | Exact provider identifier supplied by the consumer | Pass the supplied profileOptionCode unchanged; do not derive it from the FSM label and do not request separate PM confirmation | If profileOptionCode is missing, do not invoke or propose a dependent change; return the missing-input gap |
| core.fusion-api.apps-common.lookups | manage-lookups | lookupType | Consuming skill at runtime | Each exact provider identifier supplied by the consumer | Read the applicable guidance under core/fusion-api/apps-common/lookups/references; invoke once per applicable lookupType and pass each supplied value unchanged without separate PM confirmation | If an applicable lookupType is missing, do not invoke or propose a dependent change; return the missing-input gap |

## Before and After Evidence Contract

| Result | Required Evidence |
|---|---|
| No change required | Exact provider, route, identifier, target environment, before state, product recommendation, comparison result, and validation result |
| Change proposed | No proposal until the no-change comparison fails and the change is necessary for the requested implementation outcome |
| Change confirmed | Exact target, provider-owned operation, identifier-bound proposed state, current preview, and explicit user confirmation |
| Change applied | Provider-returned before state, verified after state, validation result, external evidence reference when safe, and unresolved gaps |
| Provider or identifier gap | Missing provider skill, missing access, missing runtime identifier, ambiguous result, or incomplete evidence; no configuration proposal or mutation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile-option-dependent change is considered | Blocking |  | The consuming skill did not supply profileOptionCode, or core.fusion-api.apps-common.profile-options was not queried through manage-profile-options with that exact value before the proposal | Pass the consuming-skill value unchanged, query the provider, compare current and recommended state, and retain evidence | Provider query or consuming-skill input only |
| A lookup-dependent change is considered | Blocking |  | The consuming skill did not supply an applicable lookupType, core.fusion-api.apps-common.lookups was not queried through manage-lookups once per supplied value, or the applicable guidance under core/fusion-api/apps-common/lookups/references was not read | Read the provider guidance, pass each consuming-skill value unchanged, and query the declared provider; do not substitute another provider | Provider query or consuming-skill input only |
| Provider state already matches the product recommendation | Blocking |  | A configuration change is still proposed | Return no change required with comparison evidence | Remove the unnecessary proposal |
| Provider state differs from the product recommendation | Blocking |  | The proposed change is not required by the requested implementation outcome or lacks explicit user confirmation | Show the exact provider-owned change and obtain confirmation | User confirmation only |
| A provider mutation is ready | Blocking |  | The consuming skill constructs or submits provider CRUD, retries a mutation, or assumes setup-task ownership | Hand off to the provider skill and return its verified result | No; provider ownership is mandatory |

## Exceptions and Ownership

- The consuming skill may classify the business scenario, supply exact runtime
  identifiers, invoke provider queries, compare evidence, and decide whether a
  proposal is necessary.
- The consuming skill performs no provider CRUD and does not reproduce provider
  payload construction, category routing, retry behavior, or setup-task logic.
- An FSM source reference is context only and must not replace the exact
  profileOptionCode or lookupType supplied by the consuming skill.
- No provider-dependent change proceeds while a required runtime identifier,
  provider skill, current state, product recommendation, validation result, or
  change confirmation is unresolved.
