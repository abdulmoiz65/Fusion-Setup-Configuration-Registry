# Manage Assignment Status Dependency Readiness

## Purpose

Defines the conditional status, country, and related-status references used by
Manage Assignment Status. Dependencies are evaluated only for applicable
fields and are never created or substituted by the task.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Assignment Status identity | Resolve the current target or confirm the proposed create identity is available |
| 2 | Payroll and HR system statuses | Resolve supplied or create-required system status values |
| 3 | Country context | Resolve a supplied country to one legislation code |
| 4 | Original Assignment Status | Resolve a supplied related status to its stored identifier |
| 5 | Default flag lookup | Resolve an explicitly supplied or defaulted flag through the declared lookup |
| 6 | FSM setup CSV package | Obtain and validate a fresh same-task export for create or edit |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| assignment_status_identity | Existing Assignment Status or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Assignment Status resource | find_manage_assignment_status | Prevents an ambiguous target or duplicate create | Provide one exact status selector | Resolved status identity and current values |
| payroll_status | Payroll system status | Conditional | Create or a supported payroll status is supplied | Lookup | Common Lookup type PAY_ASS_SYS_STATUS | resolve_payroll_system_status | Stores one enabled payroll-system status code | Provide one exact code or meaning | Stored payroll status code |
| hr_status | HR system status | Conditional | Create or a supported HR status is supplied | Lookup | Common Lookup type PER_ASS_SYS_STATUS | resolve_hr_system_status | Stores one enabled HR-system status code | Provide one exact code or meaning | Stored HR status code |
| country_context | Country or legislation | Conditional | A country is supplied | Lookup | Current country LOV | resolve_assignment_status_country | Produces the legislation code used by the task source | Provide one exact country name or code | LegislationCode |
| original_status | Original Assignment Status | Conditional | Original Assignment Status is supplied | Lookup | Assignment Status resource | resolve_original_assignment_status | Stores the referenced status identifier rather than its display value | Provide one exact status code or name | OrigAssignStatusTypeId |
| default_flag | Default status flag | Conditional | The flag is explicitly supplied or a documented default requires validation | Lookup | Common Lookup type YES_NO | resolve_default_flag | Prevents a hard-coded or invalid stored flag | Provide one exact code or meaning when overriding | Stored default flag |
| fsm_package | FSM setup CSV package | Conditional | Create or edit is requested | Verify | Fresh same-task export | validate_assignment_status_fsm_package | Preserves the FSM submitTaskCSVImport route and prevents substitution with an HCM Data Loader object | No user input; obtain the export automatically | ASM_SETUP_CSV_METADATA.xml and scoped CSV rows |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.DEPENDENCY | decision | 2 | resolve_dependency | ready->AS.READ;not_required->AS.READ;needs_input->AS.ERROR;unresolved->AS.ERROR | AS.VALIDATE | stop | After input validation and before task-local reference lookups |
