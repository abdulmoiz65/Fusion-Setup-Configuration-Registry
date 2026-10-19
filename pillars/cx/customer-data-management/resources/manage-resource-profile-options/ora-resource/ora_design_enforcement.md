# Manage Resource Profile Options Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Verify the selected level | Require the resolved profile level to be enabled and updatable |
| 2 | Verify the lookup contract | Require one exact standard lookup type extracted from SqlValidation |
| 3 | Verify the requested code | Require the resolved code to be enabled and effective on the validation date |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every changed profile value | Blocker | resolve_profile_option_level | The selected level is not enabled, not updatable, or the scope does not match the live value | Select an enabled updatable level and exact scope | No |
| Every changed profile value | Blocker | resolve_profile_option_lookup_code | SqlValidation does not resolve to exactly one supported lookup type | Use a profile option with a resolvable standard-lookup validation contract | No |
| Every changed profile value | Blocker | resolve_profile_option_lookup_code | The requested code is missing, disabled, not yet active, or end-dated | Select an enabled effective code from the resolved lookup | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_profile_option_definition | Every changed profile value | SqlValidation | ora_reference_lookups.md |
| resolve_profile_option_level | Every changed profile value | Enabled flag, updatable flag, current value, and scope key | ora_reference_lookups.md |
| resolve_profile_option_lookup_code | Every changed profile value | Matched code, enabled flag, start date, and end date | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.ENFORCE_VALUE | decision | 6 | design_enforcement | compliant->RPO.RETURN_SUCCESS;blocked->RPO.RETURN_ISSUES | RPO.RESOLVE_CODE | stop | Every changed profile value |
