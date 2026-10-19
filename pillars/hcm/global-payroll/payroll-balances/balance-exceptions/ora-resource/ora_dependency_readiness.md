# Balance Exceptions dependency readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legislative data group and legislation context | Select and resolve the LDG before balances, dimensions, groups, formulas, or LOV codes |
| 2 | Source balance configuration | Set up the source balance and an applicable compatible dimension |
| 3 | Conditional formula or target balance | Create and validate the Formula, or validate the target balance and dimension, when the selected variance type needs it |
| 4 | FSM template evidence | Generate a task-level template/spec export and inspect its ZIP layout before preparing an import |
| 5 | Report setup | Create the Balance Exception Report after the exception; submit Run Balance Exception Report only through its separately approved payroll-flow workflow |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ldg_context | Legislative data group and legislation | Yes | Always | Satisfied with an ID; Lookup when only a name is provided; Blocked on zero or multiple matches | Workflow-approved read-only target-pod capture | resolve_ldg_by_exact_name | LDG controls available balances, dimensions, groups, formulas, and LOV values | Provide one LDG ID or an unambiguous LDG name | LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode |
| source_balance | Defined balance with compatible dimension | Conditional | A defined balance is the selected source | Lookup when exact BalanceName and DimensionName are supplied without an ID; blocked until comparison type, balance type, and dimension are resolved | Selected read-only target-pod LOV evidence | resolve_defined_balance_id | A defined balance selection sends DefinedBalanceId; the dimension LOV depends on BalanceTypeId | Provide exact balance and dimension names in the selected LDG and comparison type | DefinedBalanceId, BalanceName, DimensionName |
| source_balance_group | Balance group | Conditional | A balance group is the selected source | Lookup when exact BalanceGroupName is supplied without an ID; blocked until comparison type and group are resolved | Selected read-only target-pod LOV evidence | resolve_balance_group_id | A group selection sends BalanceGroupId instead of DefinedBalanceId | Provide the exact group name in the selected LDG and comparison type | BalanceGroupId, BalanceGroupName |
| comparison_type | Comparison type selection | Yes | Always | Lookup until a drawer-supported comparison code is confirmed | Selected read-only target-pod LOV evidence | resolve_comparison_type_code | Comparison type filters balances, groups, variance types, and operators | Provide a drawer-supported comparison label or code | ComparisonType |
| variance_type | Variance type selection | Yes | Always | Lookup after comparison type and optional group are selected | Selected read-only target-pod LOV evidence | resolve_variance_type_code | Available variance types change with comparison and group | Provide an available variance label or code | VarianceType |
| variance_formula | Balance Exception formula | Conditional | VarianceType is F | Lookup until the selected formula ID is confirmed; blocked on missing or ambiguous formula | Selected read-only target-pod LOV evidence | resolve_formula_id | Formula variance requires a Balance Exception formula | Provide exact formula name or ID | FormulaId, FormulaName |
| variance_target_balance | Target balance | Conditional | VarianceType is B | Blocked pending live verification of the configured-only target balance lookup | Configured UI provider; live response not captured | resolve_target_balance_type_id | Balance variance requires a target balance | Provide target balance name and source defined balance context | TargetBalanceTypeId, TargetBalanceName |
| variance_target_dimension | Target dimension | Conditional | VarianceType is B | Blocked pending live verification of the configured-only target dimension lookup | Configured UI provider; live response not captured | resolve_target_defined_balance_id | Balance variance requires a target defined balance | Provide target dimension name and target balance context | TargetDefinedBalanceId, TargetDimensionName |
| fsm_template | Current task-level FSM template and ZIP contract | Yes | Export or import is requested | Blocked until current task template/process evidence is captured | Public FSM task-template export after workflow selection | verify_balance_exception_fsm_template | CSV filenames, headers, action keys, required flags, and dependency order are not derivable from the supplied source | Generate a task-level template export for PAY_MANAGE_BALANCE_EXCEPTIONS and provide the redacted ZIP/process evidence | Template ZIP filename, hash, CSV headers, ProcessId, ProcessLog |
| report_configuration | Balance Exception Report membership | Conditional | Reporting is requested | Verify after exception setup; Blocked when report membership is missing | Workflow-approved read-only UI or FSM verification | verify_balance_exception_report_membership | The report consumes exceptions after they are created | Provide the report identity and confirm it contains the exception | Report name, BalExceptionId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required setup and exact identifier evidence are present | Lookup only when a documented resolver is invoked; create is not authorized here |
| Lookup | A permitted alternate identifier needs one exact read-only resolution | Yes for workflow-approved read-only lookup only |
| Verify | A supplied dependency needs compatibility or membership confirmation | Yes for workflow-approved read-only lookup only |
| Blocked | Dependency is absent, ambiguous, incompatible, or lacks the required target-pod/template evidence | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BE.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | satisfied->BE.RESOLVE_REFERENCES;blocked->BE.RETURN_ISSUES | BE.VALIDATE_INPUT | stop | Input validation passed |
