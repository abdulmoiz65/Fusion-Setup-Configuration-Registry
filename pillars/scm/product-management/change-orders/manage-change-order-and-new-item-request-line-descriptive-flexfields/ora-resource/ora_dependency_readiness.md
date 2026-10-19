# Change Line DFF Dependency Readiness

This resource owns the conditional change-type prerequisite. Use the named resolver in ora_reference_lookups.md; baseline acquisition and artifact validation follow the task's declared shared route.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Allowed change-type contexts | Retrieve allowed InternalName values for explicit allowed-value lists/checks and requested Context definitions or Context Sensitive Segment associations, including a selected existing Context when membership applies; disable-only targets and unrelated preserved Contexts are not membership prerequisites |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| change_type | Allowed change-type contexts | Conditional | Explicit allowed-value lists/checks, requested Context definitions, or requested Context Sensitive Segment associations; excludes enabled-state-only disable | Verify | Declared read-only Fusion lookup | resolve_change_type_internal_name | The requested-code membership check needs the complete set of allowed context values | Resolve the lookup before evaluating membership. A supplied value is not existence evidence. A standalone membership check does not establish DFF setup readiness. Disable-only, Global-only and selector-only requests retain applicable baseline/design checks without fabricating this dependency; selector impact is assessed separately | allowed_context_codes and context_lookup_complete |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLDFF.DEPENDENCIES | step | 30 | resolve_dependency | success->CLDFF.DEFAULTS;failure->CLDFF.RETURN_ISSUES | CLDFF.LOOKUPS | stop | Evaluate applicable dependency rows using resolved evidence |
