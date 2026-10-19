# Manage Assignment Status Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Assignment Status.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, or edit | Block | Provide one supported operation | Every request |  |
| Existing status selector | Exact assignment status code or name | Block | Provide one exact selector | get or edit | find_manage_assignment_status |
| Create fields | UserStatus, AssignmentStatusCode, PaySystemStatus, PerSystemStatus, and StartDate | Block | Provide all five values | create |  |
| Edit changes | One exact status and at least one editable value | Block | Provide the target and intended editable changes | edit | find_manage_assignment_status |
| Country context | Exact country name or territory code | Block when required | Provide one country value | Country is supplied or required | resolve_assignment_status_country |
| Original status | Exact assignment-status code or name | Block when required | Provide one current compatible status | Original Assignment Status is supplied | resolve_original_assignment_status |
| FSM source package | Not a user input | Do not block when absent | Obtain a fresh same-task export automatically | create or edit | validate_assignment_status_fsm_package |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing assignment status does not resolve exactly once | Missing | Provide one exact code or name | find_manage_assignment_status |
| A payroll system status does not resolve to one compatible stored code | Invalid | Correct the payroll status | resolve_payroll_system_status |
| An HR system status does not resolve to one compatible stored code | Invalid | Correct the HR status | resolve_hr_system_status |
| A supplied default flag does not resolve to one compatible stored code | Invalid | Correct the flag | resolve_default_flag |
| A Country does not resolve to one exact territory code | Invalid | Correct the Country | resolve_assignment_status_country |
| Original Assignment Status does not resolve to one current compatible status | Invalid | Correct the original status | resolve_original_assignment_status |
| The fresh FSM marker, object CSV, keys, source scope, or reviewed ZIP differs | Invalid | Rebuild from a fresh same-task export; do not request a cached archive | validate_assignment_status_fsm_package |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Date format and range | Reject an invalid StartDate or a StartDate later than EndDate | A date is supplied |  |
| Immutable edit fields | Reject changes to AssignmentStatusCode, PaySystemStatus, or PerSystemStatus | edit |  |
| Lookup-backed value | Require one exact compatible stored code for each system status or supplied default flag | A lookup-backed value is supplied |  |
| Original status mapping | Map only a fresh resolved AssignmentStatusTypeId to OrigAssignStatusTypeId; reject display-only or stale IDs | Original Assignment Status is supplied | resolve_original_assignment_status |
| Supported fields | Reject fields absent from the current assignment-status contract | A value is supplied |  |
| FSM archive shape | Require exact-case ASM_SETUP_CSV_METADATA.xml and the scoped task-object CSV; reject conversion to an HCM Data Loader archive | create or edit | validate_assignment_status_fsm_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.VALIDATE | decision | 1 | validate_input | valid->AS.DEPENDENCY;missing->AS.ERROR;invalid->AS.ERROR;unsupported->AS.ERROR | none | stop | Every Manage Assignment Status request |
