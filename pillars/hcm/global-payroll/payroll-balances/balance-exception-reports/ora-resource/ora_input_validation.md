# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Report identity | BalExcepReportName | Stop with a field-specific missing-value result | Supply a nonblank report name | Create, update, export, or import preparation | |
| Legislative context | LegislativeDataGroupId, or an LDG display name | Stop with a field-specific missing-value result | Supply an ID or resolve an exact display-name match | All report-definition work | resolve_ldg_by_exact_name |
| Included exceptions | One or more UI display names | Stop before treating the report as runnable or preparing import data | Evaluate each exact name for FSM against the selected LDG and legislation context; do not require the user to supply an ID | New or changed report definition | evaluate_balance_exception_for_fsm |
| Optional definition restrictions | ConsolidationSetId and/or PayrollId only when a restriction is intended | Do not require either restriction; when omitted in an FSM CSV, encode identifier columns as `#null` | Supply an ID or resolve an exact name only when a restriction is intended | Create, update, export, or import preparation | |
| FSM import artifact | Task-specific template/export ZIP, immutable import ZIP, and SHA-256 hash | Block import preparation or submission | Obtain a current template export for PAY_MANAGE_BALANCE_EXCEPTION_REPORTS and inspect its schema | FSM import | verify_report_task_template_export |
| FSM child relationship | `PAY_EXCEPTION_REPORT_SUFFIX.ViewInstanceName` and `GroupingKey` | Stop before import when the child uses a parent view instance or parent grouping key | Use `BalanceExceptionReportEntryMigration`; form `GroupingKey` as `BaseBalExceptionName,LegislativeDataGroupName,BalExcepReportName` | FSM import with one or more included exceptions | verify_report_task_template_export |
| Optional FSM foreign keys | `PAY_EXCEPTION_REPORT_GROUP.ConsolidationSetId` and `PayrollId` | Do not require either foreign key. Stop only when an unrestricted report leaves its omitted identifier as an empty CSV field | Keep display-name columns blank and encode each omitted identifier as `#null`, matching a current task data export | FSM import with no Payroll or Consolidation Group restriction | verify_report_task_template_export |
| Included-exception identity | An exact UI-supplied `BaseBalExceptionName` | Stop before import if the workflow cannot evaluate a usable FSM binding in the report LDG and legislation context | Evaluate the name as LDG-owned or compatible seeded/shared, and retain the evaluator's FSM child binding while using the canonical name-based child CSV row | FSM import with one or more included exceptions | evaluate_balance_exception_for_fsm |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An LDG name is supplied | Exactly one match is required | Retain LegislativeDataGroupId and LegislationCode;otherwise stop | resolve_ldg_by_exact_name |
| A Payroll or Consolidation Group restriction is supplied | The reference must resolve in the selected LDG | Stop on no match, many matches, or incompatible context | |
| A Balance Exception is supplied | Every entry must evaluate to an LDG-owned or compatible seeded/shared FSM binding, and duplicates are rejected | Stop on no match, many matches, incompatible legislation, or duplicate selection | evaluate_balance_exception_for_fsm |
| FSM import is requested | Current task template and target-pod evidence must be available | Stop until the task-specific template/export evidence is captured | verify_report_task_template_export |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exception Report Name is nonblank | Reject a blank value. Length, uniqueness, character set, and FSM mandatory status are not documented. | Create or update | |
| Category is a valid lookup code | Store the code rather than the display meaning;stop if the authoritative code cannot be confirmed. | Category is supplied | resolve_report_category |
| Child relationship is preserved | Keep each included exception associated with its parent report and BalExceptionId;do not merge entries across reports. | Import or maintenance preparation | |
| FSM child view and key are exact | Require `BalanceExceptionReportEntryMigration` for the child. Its grouping key begins with the included exception name, followed by LDG and report name; do not reuse the parent `BalanceExceptionReportMigration` view or `BalExcepReportName,LDG` key. | FSM import preparation | |
| Optional unrestricted foreign keys use the FSM null sentinel | Payroll and Consolidation Group remain optional. When neither restriction is requested, leave `PayrollName` and `ConsolidationSetName` empty, but set `PayrollId` and `ConsolidationSetId` to `#null`. Empty identifier fields can be treated as unresolved foreign keys. | FSM import preparation | |
| Included exception evaluates for the FSM report context | Evaluate the user-provided UI name as LDG-owned or compatible seeded/shared before preparation. Do not reject a seeded exception solely because an LDG-owned FSM export omits it, or use an existing report as its lookup source. The canonical CSV row retains `BaseBalExceptionName`; apply the evaluator's `BalExceptionId` binding only when the target importer requires it. | FSM import preparation | evaluate_balance_exception_for_fsm |
| Read-only display values are not identifiers | Do not substitute names, audit values, comparison values, or variance values for IDs or codes. | Read, export, import, or maintenance preparation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEXR.VALIDATE-REQUEST | step | 1 | validate_input | valid->BEXR.CHECK-DEPENDENCIES;invalid->RETURN-ISSUES | none | stop | A Balance Exception Reports request is received |
