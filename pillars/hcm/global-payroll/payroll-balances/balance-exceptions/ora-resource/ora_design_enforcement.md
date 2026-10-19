# Balance Exceptions design enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Exact resolution | Resolve supplied display names to one target-pod identifier or code before preparation |
| 2 | Compatibility validation | Validate balance/dimension, comparison, variance, and conditional references |
| 3 | FSM artifact validation | Validate the current task-level template ZIP and immutable import artifact/hash |
| 4 | Live import approval | Present the exact target pod, task code, ZIP hash, and operation for explicit approval immediately before submission |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error |  | Exactly one BalanceGroupId or DefinedBalanceId is not selected | Supply one source selection and a compatible dimension | Yes |
| VarianceType is formula | Error | resolve_formula_id | Formula does not meet the Balance Exception Formula Type return contract | Select or create a qualifying formula through its own approved workflow | No |
| VarianceType is balance | Error | resolve_target_defined_balance_id | Target balance or target dimension is missing, comparison type is not permitted, or the configured-only target LOV contract has not been verified live | Correct the target configuration and comparison choice, then verify the target LOV contract | Yes |
| Export or import is requested | Error | verify_balance_exception_fsm_template | Current template ZIP/layout, hash, environment identity, or catalog evidence is unavailable | Capture and validate the template/process evidence before preparing or submitting an artifact | No |
| Live FSM import is requested | Error | verify_balance_exception_fsm_template | Exact target, task code, immutable ZIP hash, and immediate explicit approval are not present | Present the bound import details and request approval | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_comparison_type_code | Always | Drawer-supported code and display value | ora_reference_lookups.md |
| resolve_defined_balance_id | A defined balance is selected by name | Exact defined balance ID and compatible dimension | ora_reference_lookups.md |
| resolve_balance_group_id | A balance group is selected by name | Exact group ID | ora_reference_lookups.md |
| resolve_variance_type_code | Always | Context-supported variance code and display value | ora_reference_lookups.md |
| resolve_variance_operator_code | Always | Comparison-supported operator code and display value | ora_reference_lookups.md |
| resolve_severity_level_code | Always | Severity code and display value | ora_reference_lookups.md |
| resolve_formula_id | VarianceType is F | Formula ID and name | ora_reference_lookups.md |
| resolve_target_defined_balance_id | VarianceType is B | Verified target balance and dimension contract and ID | ora_reference_lookups.md |
| verify_balance_exception_fsm_template | Export, import, or live import is requested | Environment identity, task capability, template ZIP/hash, headers, process status/log | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BE.ENFORCE_DESIGN | step | 50 | design_enforcement | passed->BE.EXECUTION_GATE;blocked->BE.RETURN_ISSUES | BE.APPLY_DEFAULTS | stop | Defaults have been evaluated |
