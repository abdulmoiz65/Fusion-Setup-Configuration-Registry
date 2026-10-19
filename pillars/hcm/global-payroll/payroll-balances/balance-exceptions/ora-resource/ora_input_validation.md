# Balance Exceptions input validation

Use this guidance only for Balance Exceptions (PAY_MANAGE_BALANCE_EXCEPTIONS). It validates an intended task-level FSM operation; it does not authorize internal Payroll Generic REST routes.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Legislative data group context | LegislativeDataGroupId or LegislativeDataGroupName | Stop with a field-specific missing LDG error | Supply an LDG ID, or provide a name for exact target-pod resolution | Always | resolve_ldg_by_exact_name |
| Balance to evaluate | Exactly one of BalanceGroupId, DefinedBalanceId, exact BalanceName plus DimensionName, or exact BalanceGroupName | Stop with a field-specific balance-selection error | Select one source; named sources require read-only target-pod resolution before FSM preparation | Always |  |
| Core exception definition | BalExceptionName, ComparisonType, VarianceType, VarianceOperator, SeverityLevel | Stop with the missing field names | Supply values valid for the selected LDG and comparison context | Always |  |
| Amount or percent variance | VarianceValue | Stop with a variance-value error | Supply a numeric value | VarianceType is A or P |  |
| Formula variance | FormulaId or exact FormulaName | Stop with a formula error | Resolve the Balance Exception formula before artifact preparation | VarianceType is F | resolve_formula_id |
| Target-balance variance | TargetBalanceTypeId and TargetDefinedBalanceId, or exact target balance and dimension names | Stop with a target-balance error | Verify the configured-only target LOVs in the active workflow before resolving names | VarianceType is B |  |
| FSM movement artifact | Source or target task-level template ZIP, intended operation, immutable ZIP hash | Stop before preview or import | Generate and inspect the task-level template export, then prepare and hash the import artifact | Export or import is requested | verify_balance_exception_fsm_template |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Both BalanceGroupId and DefinedBalanceId are supplied | Invalid | Reject the request; retain only the intended source selection |  |
| Neither ID is supplied, but exact BalanceName and DimensionName are supplied | Lookup | Resolve the balance type, then its defined balance ID in the selected LDG and comparison context | resolve_defined_balance_id |
| Neither ID is supplied, but exact BalanceGroupName is supplied | Lookup | Resolve the group ID in the selected LDG and comparison context | resolve_balance_group_id |
| Neither ID nor a complete named source selection is supplied | Invalid | Request exactly one balance-selection alternative |  |
| A defined balance is supplied | Verify | Confirm its dimension is available for the selected balance type and comparison type | resolve_defined_balance_id |
| A balance variance is supplied | Verify | Confirm the comparison choice and target references through the configured-only target LOVs after live contract verification | resolve_target_defined_balance_id |
| A comparison type label is supplied | Lookup | Resolve it from the drawer-specific options, not the broad initial lookup | resolve_comparison_type_code |
| A variance type label or code is supplied | Lookup | Resolve it after comparison type and optional group selection | resolve_variance_type_code |
| A variance operator label or code is supplied | Lookup | Resolve it for the selected comparison type | resolve_variance_operator_code |
| A severity label or code is supplied | Lookup | Resolve it from the severity lookup | resolve_severity_level_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Balance Exception Name is nonblank | Reject blank value; the supplied implementation evidence indicates an 80-character UI limit, but the FSM/public contract is unconfirmed | Always |  |
| Comparison Value is present | Require it for MAN; use fixed comparison values only after target-pod evidence confirms them | Comparison type requires a value |  |
| Formula return contract | Reject a formula that has input variables or lacks REFERENCE_VALUE and REFERENCE_INFO | Formula variance |  |
| Identifier preservation | Retain BalExceptionId and every selected LOV ID or code with its display value; use Unresolved (ID/Code: value) when display resolution is unavailable | Reading or displaying a record |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BE.VALIDATE_INPUT | step | 10 | validate_input | valid->BE.CHECK_DEPENDENCIES;invalid->BE.RETURN_ISSUES | none | stop | A Balance Exceptions request is received |
