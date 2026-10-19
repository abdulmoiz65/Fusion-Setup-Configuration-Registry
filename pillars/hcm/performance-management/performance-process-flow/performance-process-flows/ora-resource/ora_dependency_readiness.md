# Performance Process Flows Dependency Readiness

Apply this task guidance using current target metadata and the declared execution route.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | REST resource identity | For an update, resolve the existing ProcessFlowId through the read-only REST resource. |
| 2 | Effective-date and in-use state | Validate requested dates and enforce documented guarded changes for an in-use flow. |
| 3 | Parent flags | Validate criteria, evaluation, approval, sharing, meeting, final-feedback, and participant-feedback parent-child combinations. |
| 4 | Feature applicability | Validate Redwood support before CalendarInviteFlag and compensation-calibration applicability before AllowShareLockForCalib. |
| 5 | Task-role definitions | Preserve task input order, resolve each TaskCode to manager and worker task names, and include the resulting task-role rows in the CSV archive. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PERFORMANCE_PROCESS_FLOWS.EXISTING_FLOW | Existing process flow | Yes | Update | Lookup | ProcessFlowId | get_performance_process_flow_by_id | InUseFlag is server-managed and controls documented update restrictions. | Resolve the resource before evaluating the update. | ProcessFlowId, InUseFlag, DateFrom, DateTo, Status |
| PERFORMANCE_PROCESS_FLOWS.TEMPLATE_DATE_COVERAGE | Template effective period | Conditional | A flow is used or created in template context | Verify | Template context supplied to the selected workflow | | A process flow must cover the associated template period; inline REST creation cannot start after the template start. | Compare the two effective periods before the write. | Template DateFrom, Template DateTo |
| PERFORMANCE_PROCESS_FLOWS.REDWOOD_FEATURE_APPLICABILITY | Redwood performance-documents applicability | Conditional | CalendarInviteFlag is true | Lookup | ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED profile value | resolve_redwood_performance_documents_feature | Calendar invitations require the effective Redwood performance-documents feature. | Enable CalendarInviteFlag only after the profile value resolves to Y. | ProfileOptionValue = Y |
| PERFORMANCE_PROCESS_FLOWS.COMPENSATION_CALIBRATION_FEATURE_APPLICABILITY | Compensation-calibration applicability | Conditional | AllowShareLockForCalib is true | Lookup | ORA_HRA_COMP_CALIBRATION_STATUS_ENABLED profile value | resolve_compensation_calibration_feature | Share-and-lock for calibration requires the effective compensation-calibration feature. | Enable AllowShareLockForCalib only after the profile value resolves to Y. | ProfileOptionValue = Y |
| PERFORMANCE_PROCESS_FLOWS.TASK_ROLE_DEFINITIONS | Process task-role CSV data | Conditional | Task-role rows are needed | Lookup | Ordered user task names | resolve_process_task_definition_by_task_name | Task codes and names must come from the process-task-definition catalog, while task order determines the CSV sequence. | Keep input order; set SequenceNumber to each task's one-based input position. Map the returned TaskName to both MgrTaskName and WkrTaskName unless TaskCode is MGREVAL; for MGREVAL, populate MgrTaskName only. | TaskCode, SequenceNumber, MgrTaskName, WkrTaskName |
| PERFORMANCE_PROCESS_FLOWS.HIDE_DOCUMENT_SEQUENCE | Hidden-document task ordering | Conditional | HidePdFrWkrBfrShareFlag is Y | Verify | Resolved employee-evaluation and manager-share-performance-document task-role rows | | Hiding the performance document from the worker before sharing requires the manager-share-performance-document task to occur first. | Require the employee-evaluation task SequenceNumber to be greater than the manager-share-performance-document task SequenceNumber; otherwise stop before approval or import. | Employee-evaluation SequenceNumber, Manager-share-performance-document SequenceNumber |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | An update requires current REST state. | Yes; read-only through get_performance_process_flow_by_id. |
| Verify | A documented cross-field, effective-date, or child-service dependency must be checked. | No |
| Blocked | A required dependency is missing, violates a documented constraint, or has a TBD contract. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_PROCESS_FLOWS.DEPENDENCIES | decision | 30 | resolve_dependency | ready->PERFORMANCE_PROCESS_FLOWS.REFERENCE_LOOKUPS;missing->PERFORMANCE_PROCESS_FLOWS.STOP_DEPENDENCY | PERFORMANCE_PROCESS_FLOWS.APPLY_DEFAULTS | stop | A valid request has applicable update, feature, template, or child-task dependencies. |
