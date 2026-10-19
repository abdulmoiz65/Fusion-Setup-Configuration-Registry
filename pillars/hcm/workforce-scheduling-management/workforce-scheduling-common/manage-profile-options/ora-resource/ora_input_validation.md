# Manage Profile Options Input Validation

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026
- Runtime provider identifier requirement, user-provided 19 August 2026

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Provider identifier | Exact profileOptionCode supplied by the consuming task | Block before the provider lookup or any recommendation | Require the consuming task to supply the exact profileOptionCode for the requested configuration change; do not infer it from an FSM source reference or a display label | A profile-option configuration change is proposed |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A consuming task supplies profileOptionCode | Continue when one exact nonblank runtime value is present | Pass the supplied value unchanged to the provider lookup | query_profile_option_provider_state |
| The consuming task does not supply profileOptionCode | Stop before provider lookup | Request the exact profileOptionCode from the consuming task |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.VALIDATE_PROVIDER_INPUT | step | 5 | validate_input | valid->MPO.QUERY_PROFILE_OPTION_PROVIDER;blocked->MPO.HANDLE_ISSUES | none | stop | Before a profile-option provider lookup or recommendation |
