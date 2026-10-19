# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legislative Data Group | Select and resolve the LDG before creating or changing a report. |
| 2 | Balance Exceptions | Evaluate one or more Balance Exceptions for the selected LDG and legislation context; compatible seeded/shared exceptions do not need an LDG-owned setup row. |
| 3 | Optional restrictions | Create and validate Payroll and Consolidation Group first when either is used to restrict the definition. |
| 4 | FSM schema and relationships | Export the current task-specific template or a known-good data export and inspect its ZIP/CSV schema, child view instance, and parent/child grouping-key syntax before preparing an import. |
| 5 | Target readiness | Verify task availability, reference values, privileges, and redacted target-pod evidence before a live import. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| BEXR-LDG | Legislative Data Group | Yes | All report-definition work | Lookup | User-supplied ID or display name | resolve_ldg_by_exact_name | The report and included exceptions must share LDG and legislation context. | Provide one LDG ID or a display name that resolves to exactly one LDG. | LegislativeDataGroupId;LegislationCode |
| BEXR-EXCEPTION | Balance Exception | Yes | New or changed report definition | Lookup | User-supplied display name | evaluate_balance_exception_for_fsm | A runnable report groups LDG-owned or compatible seeded/shared Balance Exceptions. | Provide one or more distinct exact UI names; the workflow evaluates and binds IDs internally if required. | BaseBalExceptionName;BalExceptionId;resolution provenance |
| BEXR-CONSOLIDATION | Consolidation Group | Conditional | Definition is restricted by consolidation group | Lookup | User-supplied ID or display name | resolve_consolidation_group_by_ldg | The optional restriction must be compatible with the selected LDG. | Provide an ID or exact name;omit only when no definition-level restriction is intended. | ConsolidationSetId;ConsolidationSetName |
| BEXR-PAYROLL | Payroll | Conditional | Definition is restricted by payroll, or the report will be run | Lookup | User-supplied ID or display name | resolve_payroll_by_ldg | Payroll is optional at definition but required when running the Balance Exception Report. | Provide an ID or exact name and validate run-time consistency. | PayrollId;PayrollName |
| BEXR-CATEGORY | Report Category | Conditional | Category is supplied | Lookup | User-supplied category code or display value | resolve_report_category | The definition stores a category code, not the display meaning. | Supply a confirmed code or resolve an exact category meaning. | Category;CategoryMeaning |
| BEXR-FSM-TEMPLATE | Report-task FSM template | Yes | FSM import is requested | Verify | Task-specific template or known-good data export and target-pod evidence | verify_report_task_template_export | The task-specific ZIP establishes CSV names, headers, keys, action values, and child-row syntax. For `PAY_EXCEPTION_REPORT_SUFFIX`, the child view is `BalanceExceptionReportEntryMigration` and the key is `BaseBalExceptionName,LDG,ReportName`. | Obtain and inspect the current PAY_MANAGE_BALANCE_EXCEPTION_REPORTS export;do not reuse the Balance Exceptions task template or parent-row values in a child row. | Template ZIP hash;CSV schema;child view/key evidence;process status;ProcessLog |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A supplied identifier/code has current authoritative evidence. | No |
| Lookup | A display value needs exactly one authoritative match. | Yes, read-only lookup only |
| Verify | FSM schema, task capability, privilege, or target-pod evidence must be confirmed. | Yes, read-only verification only |
| Blocked | Evidence is missing, ambiguous, incompatible, or unresolved. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEXR.CHECK-DEPENDENCIES | step | 2 | resolve_dependency | ready->BEXR.RESOLVE-LDG;blocked->RETURN-ISSUES | BEXR.VALIDATE-REQUEST | stop | Request inputs passed structural validation |
