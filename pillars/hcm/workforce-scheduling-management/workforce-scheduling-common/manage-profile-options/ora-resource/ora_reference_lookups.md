# Manage Profile Options Provider Lookup

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_profile_option_provider_state | A Workforce Scheduling implementation proposes a profile-option configuration change after the consuming task supplies profileOptionCode | Provider product/team Common Applications / ApplCore; provider route core.fusion-api.apps-common.profile-options; route manage-profile-options; exact profileOptionCode supplied by the consuming task at runtime; FSM source reference Manage Administrator Profile Values | Invoke the provider skill through manage-profile-options before proposing a change; the provider owns all read and CRUD behavior | Current state, product-recommended state, and provider validation evidence for profileOptionCode | Require the exact runtime profileOptionCode supplied by the consuming task. Do not infer it from the FSM source reference or a display label. | Before state, recommended state, validation result, and provider gap | Stop and request the exact profileOptionCode from the consuming task when it is missing, or report the provider gap; do not construct a provider request or clone provider CRUD behavior. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A configuration change is proposed | Invoke the named provider before presenting a recommendation and retain its before-state and validation evidence. |
| The provider exposes an API route | Pass profileOptionCode exactly as supplied by the consuming task. |
| The provider identifies no required difference | Do not apply a change. |
| The provider identifies a required difference | Present the provider evidence and obtain user confirmation immediately before the provider-owned change. |
| The consuming task does not provide the exact product identifier | Preserve Manage Administrator Profile Values as an FSM source reference, record the missing runtime input, and stop. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.QUERY_PROFILE_OPTION_PROVIDER | step | 10 | reference_lookup | resolved->MPO.ENFORCE_PROVIDER_OWNERSHIP;blocked->MPO.HANDLE_ISSUES;failure->MPO.HANDLE_ISSUES | MPO.VALIDATE_PROVIDER_INPUT | stop | Before proposing a profile-option configuration change with the exact runtime identifier supplied by the consuming task |
