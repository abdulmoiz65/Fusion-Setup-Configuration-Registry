# Manage Assignment Status Design Enforcement

## Purpose

Defines the mandatory Assignment Status design gates evaluated before preview
or routing. It does not perform lookups, apply defaults, or create missing
setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact business record |
| 2 | Validate create or edit fields | Confirm required create fields, editable fields, and valid date range |
| 3 | Validate dependencies | Resolve payroll, HR, and default-flag lookup values |
| 4 | Validate FSM source | Obtain and validate the fresh same-task FSM archive and scoped object CSV |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_manage_assignment_status | Identity is absent, unresolved, or ambiguous | Supply one exact business identifier | Input fix |
| CREATE_PAYROLL | Create | Blocking | resolve_payroll_system_status | Payroll status is absent, unsupported, or unresolved | Supply one exact supported payroll status | Lookup fix |
| CREATE_HR | Create | Blocking | resolve_hr_system_status | HR status is absent, unsupported, or unresolved | Supply one exact supported HR status | Lookup fix |
| EDIT | Edit | Blocking | find_manage_assignment_status | AssignmentStatusCode, PaySystemStatus, or PerSystemStatus changes | Preserve immutable edit fields and submit a supported change | Input fix |
| DEFAULT | A default flag is supplied | Blocking | resolve_default_flag | Default flag is unresolved or ambiguous | Resolve one exact compatible stored value | Lookup fix |
| FSM_PACKAGE | Create or edit | Blocking | validate_assignment_status_fsm_package | A fresh same-task export cannot be obtained or its marker, CSV, keys, or scope is invalid | Obtain and validate a fresh same-task export automatically | Source rebuild |
| ROUTE | Create, edit, or delete is requested | Blocking |  | The request bypasses the reviewed FSM ZIP and Core Data Loader, or requests delete | Use the approved Core Data Loader FSM create or edit route; delete is unsupported | No |

| STATUS_CONFIGURATION | Create or edit | Warning |  | Existing status, HR or payroll status, defaulting, or downstream impact is not reviewed | Reuse a suitable status and confirm configuration and impact | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_assignment_status | Exact read or edit target | Current assignment-status identity and values | ora_reference_lookups.md |
| resolve_payroll_system_status | Create supplies payroll status | Stored payroll status code | ora_reference_lookups.md |
| resolve_hr_system_status | Create supplies HR status | Stored HR status code | ora_reference_lookups.md |
| resolve_default_flag | Default flag is supplied | Stored Yes/No code | ora_reference_lookups.md |
| validate_assignment_status_fsm_package | Create or edit | Fresh export, exact marker, scoped object CSV, keys, source scope, and reviewed ZIP identity | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.ENFORCE | decision | 5 | design_enforcement | passed->AS.ROUTE;not_required->AS.ROUTE;blocked->AS.ERROR | AS.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
