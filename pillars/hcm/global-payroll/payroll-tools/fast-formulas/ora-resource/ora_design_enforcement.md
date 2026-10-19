# Fast Formulas Design Enforcement

## Functional Knowledge Summary

Payroll Fast Formulas support payroll calculation and proration, rate
conversion, element-entry and user-table validation, payment-method
preferences, payroll and work relationship groups, flow scheduling, balance
exceptions, element skip rules, access to HR data, and inbound-data
transformation for HCM Data Loader. The chosen formula type controls the
available inputs, contexts, and required return values.

Formula code can use inputs, local and output variables, database items,
contexts, operators, literals, arrays, functions, working storage, and calls to
other formulas. Database items are read-only. Formula variables derive their
types from inputs, defaults, database-item metadata, contexts, or usage; an
inconsistent type is a compilation error.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Route enforcement | Use HCM Data Loader through core.data-loader for Fast Formula setup-data mutation. |
| 2 | Formula-type contract | Confirm the type-specific contexts, inputs, and outputs before accepting formula text. |
| 3 | Language correctness | Enforce statement order, read-only database items, initialized variables, compatible types, safe arithmetic, and terminating loops. |
| 4 | Dependency correctness | Confirm required database items, flexfield generation, contexts, called formulas, and effective dates. |
| 5 | Performance review | Prefer inputs over database items, defer database-item access, minimize CHANGE_CONTEXTS, exit loops promptly, and remove unnecessary logging. |
| 6 | HDL archive review | Enforce the supplied MERGE contract, key strategy, attribute rules, and separate ClobFiles formula source before preview. |
| 7 | Compilation gate | Compile every loaded or changed formula and stop on any compilation error before use. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any Fast Formula setup-data mutation is requested | Error | | A route other than core.data-loader with HCM Data Loader is proposed | Use business object FastFormula and the authorized HDL workflow | Yes |
| A formula type is selected | Error | | Its supported contexts, inputs, output variables, or return types are absent or unconfirmed | Reconcile the formula against the type-specific Oracle documentation and target metadata | Yes |
| A database item is used | Error | | The formula attempts to assign to it, required contexts aren't supported, or a required default is absent | Treat database items as read-only and correct context/default handling | Yes |
| A flexfield database item is used | Error | | The flexfield isn't deployed or its database items haven't been generated | Deploy the flexfield, run Generate Flexfield Database Items, and recompile dependent formulas | Yes |
| CHANGE_CONTEXTS is used | Warning | | Context blocks are unnecessary, repeatedly nested, or reset contexts already supplied by the caller | Change only required contexts and combine changes into one block where practical | Yes |
| Database items are used when equivalent formula inputs are available | Warning | | The design adds avoidable database access | Prefer INPUTS statements and delay database-item evaluation until needed | Yes |
| A WHILE loop is used | Error | | The loop has no reachable exit or continues after its goal is met | Add a terminating condition or EXIT and leave the loop promptly | Yes |
| Logging is included | Warning | | Logging is unconditional or retained without a diagnostic need | Use logging sparingly, conditionally enable it, and disable it when diagnosis ends | Yes |
| A formula calls another formula | Error | | The called formula is missing, recursive, type-incompatible, or exceeds the documented call hierarchy depth | Correct the called-formula contract before compile | Yes |
| HDL formula text is packaged | Error | | Formula text is embedded in FastFormula.dat, FormulaText isn't a filename, or the ClobFiles text file is missing | Put source in one referenced UTF-8 file under ClobFiles and pass its filename in FormulaText | Yes |
| An HDL operation is selected | Error | | The action isn't MERGE | Use MERGE for source-evidenced create or update; don't infer DELETE | Yes |
| An existing formula is updated | Error | | FormulaCode is changed, or FormulaId/GUID is treated as a new-record value | Preserve FormulaCode and use an exported supported existing-record identity | Yes |
| Formula creation or change completes | Error | | The formula hasn't compiled successfully | Compile it before it is used by payroll or another application feature | Yes |
| Persisted formula content is requested | Error | resolve_fast_formula_action_target | FormulaId or effectiveDate is guessed, supplied from stale local state, or doesn't resolve to exactly one primary-endpoint record | Resolve the persisted formula first, then call getFormulaContent with the required action content type | Yes |
| Formula compilation is requested | Error | resolve_fast_formula_action_target | The formula isn't confirmed persisted, formulaId or effectiveDate is unresolved, task-specific mutation approval is absent, or a prior compile submission has an uncertain outcome | Resolve the persisted target, bind approval to the exact submission, and invoke submitCompileJob once through an authorized executor | Yes |
| Compilation monitoring is active | Error | resolve_fast_formula_action_target | Another submitCompileJob call is proposed while Compiled is N or the prior job outcome is uncertain | Poll the primary endpoint every 5 seconds and reconcile the existing job instead of submitting again | Yes |
| Compiler status requires a message | Error | get_fast_formula_compile_message | Compiled is Y and CompileStatus is I or E but the existing compiler message wasn't retrieved and displayed | Call getFormulaCompileMsg once with the resolved target and show the returned result | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_fast_formula_action_target | Before retrieving persisted formula content, submitting compilation, or monitoring compilation | FormulaId, EffectiveStartDate as effectiveDate, Compiled, and CompileStatus from one exact effective record | ora_reference_lookups.md |
| get_fast_formula_compile_message | When Compiled is Y and CompileStatus is I or E | Existing compiler status, warnings, and errors returned in result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FF.ENFORCE_DESIGN | decision | 5 | design_enforcement | compliant->FF.EXECUTION_GATE;noncompliant->FF.HANDLE_ERROR | FF.APPLY_DEFAULTS | stop | Dependencies and defaults are ready and formula or HDL design is available for review |

## Sources

- Developer-provided /scratch/share/FastFormulaAll.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormula.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormulasExport.xls, accessed 2026-08-17.
- Oracle Fusion Cloud HCM, Improve Formula Performance: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/improve-formula-performance.html
- Oracle Fusion Cloud HCM, Types of Variables: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/types-of-variables.html
- Oracle Fusion Cloud HCM, Naming Schemes for Variables: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/naming-schemes-for-variables.html
- Oracle Fusion Cloud HCM, Formula Operators: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-operators.html
- Oracle Fusion Cloud HCM, Literals: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/literals.html
- Oracle Fusion Cloud HCM, How Formulas Determine Variable Data Types: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/how-formulas-determine-variable-data-types.html
- Oracle Fusion Cloud HCM, Array Variables: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/array-variables.html
- Oracle Fusion Cloud HCM, Overview of Working Storage Area: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-working-storage-area.html
- Oracle Fusion Cloud HCM, Overview of Fast Formula Functions: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-fast-formula-functions.html
- Oracle Fusion Cloud HCM, Text Formula Functions: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/text-formula-functions.html
- Oracle Fusion Cloud HCM, Numeric Formula Functions: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/numeric-formula-functions.html
- Oracle Fusion Cloud HCM, Date Formula Functions: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/date-formula-functions.html
- Oracle Fusion Cloud HCM, Data Conversion Formula Functions: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/data-conversion-formula-functions.html
- Oracle Fusion Cloud HCM, Miscellaneous Formula Functions: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/miscellaneous-formula-functions.html
- Oracle Fusion Cloud HCM, Overview of Payroll Formulas: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-payroll-formulas.html
- Oracle Fusion Cloud HCM, Create Conversion Formulas for Proration: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/create-conversion-formulas-for-proration.html
- Oracle Fusion Cloud HCM, Configure Periodicity Conversion Rules: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/configure-periodicity-conversion-rules.html
- Oracle Fusion Cloud HCM, Element Input Validation Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/element-input-validation-formula-type.html
- Oracle Fusion Cloud HCM, User Table Validation Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/user-table-validation-formula-type.html
- Oracle Fusion Cloud HCM, Payroll User Interface Configuration Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/payroll-user-interface-configuration-formula-type.html
- Oracle Fusion Cloud HCM, Payroll Access to HR Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/payroll-access-to-hr-formula-type.html
- Oracle Fusion Cloud HCM, Payroll Relationship Group Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/payroll-relationship-group-formula-type.html
- Oracle Fusion Cloud HCM, Flow Schedule Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/flow-schedule-formula-type.html
- Oracle Fusion Cloud HCM, Balance Exception Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/balance-exception-formula-type.html
- Oracle Fusion Cloud HCM, Element Skip Formula Type: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/element-skip-formula-type.html
- Oracle Fusion Cloud HCM, Get the Rate Amount for an Assignment Base Rate: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/get-the-rate-amount-for-an-assignment-base-rate.html
- Oracle Fusion Cloud HCM, Overview of Payroll Calculation Information Formulas: https://docs.oracle.com/en/cloud/saas/human-resources/faigp/overview-of-payroll-calculation-information-formulas.html
- Oracle Fusion Cloud HCM, Overview of Using Fast Formulas for Payroll: https://docs.oracle.com/en/cloud/saas/human-resources/fapcd/overview-of-using-fast-formulas.html
- Oracle Fusion Cloud HCM, Define Elements, Balances, and Formulas: https://docs.oracle.com/en/cloud/saas/human-resources/faibf/define-elements-balances-and-formulas.html
- Developer-provided persisted formula-content and formula-compilation custom-action contracts, received 2026-08-18.
