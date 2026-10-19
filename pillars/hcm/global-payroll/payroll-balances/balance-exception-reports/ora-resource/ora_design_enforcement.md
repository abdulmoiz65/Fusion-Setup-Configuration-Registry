# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm report composition | Require one or more distinct LDG-owned or compatible seeded/shared Balance Exceptions in the selected LDG and legislation context before considering the report runnable. |
| 2 | Confirm restriction compatibility | Validate any Payroll or Consolidation Group restriction against the selected LDG. |
| 3 | Confirm FSM schema and child relationship | For import, use only current task-specific export evidence;do not infer the CSV contract, reuse the adjacent task template, or copy parent view/key values into the included-exception child. |
| 4 | Confirm live-operation approval | Immediately before an FSM import, bind approval to the exact target pod, task code, immutable ZIP/hash, and operation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A report is prepared as runnable | Error | evaluate_balance_exception_for_fsm | No included exception, duplicate exception, or exception lacking an LDG-owned or compatible seeded/shared FSM binding | Add distinct valid Balance Exceptions before running the report | Yes |
| A definition restriction is supplied | Error | resolve_payroll_by_ldg | Consolidation Group or Payroll is unresolved or incompatible with the selected LDG | Correct or remove the optional restriction | Yes |
| FSM import is prepared | Error | verify_report_task_template_export | Current task-specific template/export ZIP, schema, or target-pod evidence is unavailable | Obtain a current template export and capture redacted evidence | Yes |
| FSM import contains included exceptions | Error | verify_report_task_template_export | A `PAY_EXCEPTION_REPORT_SUFFIX` row does not use `BalanceExceptionReportEntryMigration`, or its grouping key is not `BaseBalExceptionName,LDG,ReportName` | Correct the child view instance and grouping key from current task export evidence | Yes |
| FSM import has no definition restriction | Error | verify_report_task_template_export | `ConsolidationSetId` or `PayrollId` is an empty CSV field rather than `#null` | Preserve blank display names and encode omitted identifier values as `#null` from the current task export pattern | Yes |
| FSM import contains included exceptions | Error | evaluate_balance_exception_for_fsm | The user-supplied exception name has no usable FSM binding after seeded/shared applicability evaluation | Evaluate the UI name against selected LDG and legislation applicability; do not use an existing-report export or require the user to supply an ID | Yes |
| FSM import is submitted | Error | verify_report_task_template_export | Exact approval is not bound to target pod, task code, immutable ZIP/hash, and operation | Obtain explicit approval immediately before submission | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| evaluate_balance_exception_for_fsm | A report is prepared as runnable | BaseBalExceptionName;BalExceptionId;LDG;legislation context;seed/shared provenance;duplicate status | ora_reference_lookups.md |
| resolve_consolidation_group_by_ldg | A Consolidation Group restriction is supplied | ConsolidationSetId;selected LDG | ora_reference_lookups.md |
| resolve_payroll_by_ldg | A Payroll restriction is supplied or the report will be run | PayrollId;selected LDG;effective payroll context | ora_reference_lookups.md |
| verify_report_task_template_export | FSM import is prepared or submitted | Task-specific ZIP/hash;CSV schema;target-pod evidence;approval evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEXR.ENFORCE-FSM-DESIGN | step | 10 | design_enforcement | passed->BEXR.EXECUTION-GATE;blocked->RETURN-ISSUES | BEXR.APPLY-BASE-NAME-DEFAULT | stop | A validated report definition or FSM import is prepared |
