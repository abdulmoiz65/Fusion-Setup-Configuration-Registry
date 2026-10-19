# Manage Assignment Status Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_assignment_status | Read is requested, or an exact target is needed before create or edit | Assignment status code or display name | /hcmRestApi/resources/{version}/assignmentStatuses | AssignmentStatusCode, UserStatus, current values, and item identity when available | Query a supplied code with q=AssignmentStatusCode='value' and a supplied display name with q=UserStatus='value', replacing value with the escaped caller value. Require one exact row for details or edit. | Resolved assignment-status identity and current values | Stop on zero or multiple exact matches. |
| resolve_payroll_system_status | A payroll system status is supplied | Exact code or meaning | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type PAY_ASS_SYS_STATUS | Enabled lookup code, meaning, and effective range | Require one compatible result | Stored payroll status code | Stop and request a more precise value |
| resolve_hr_system_status | An HR system status is supplied | Exact code or meaning | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type PER_ASS_SYS_STATUS | Enabled lookup code, meaning, and effective range | Require one compatible result | Stored HR status code | Stop and request a more precise value |
| resolve_default_flag | The default flag is blank on create or explicitly supplied | Exact code or meaning | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type YES_NO | Enabled lookup code and meaning | Require one compatible result; use the meaning No only for a blank create value | Stored default flag | Stop and request a more precise value |
| resolve_assignment_status_country | Country is supplied | Exact country name or territory code | /hcmRestApi/resources/{version}/hcmCountriesLov | CountryName and TerritoryCode | Follow bounded pages and require one exact name or code match | TerritoryCode to LegislationCode | Stop on zero or multiple exact matches |
| resolve_original_assignment_status | Original Assignment Status is supplied | Exact assignment-status code or name | /hcmRestApi/resources/{version}/assignmentStatuses | AssignmentStatusTypeId, AssignmentStatusCode, UserStatus, effective state, and legislation | Require one current exact compatible status; never reuse an ID from an earlier run | AssignmentStatusTypeId to OrigAssignStatusTypeId | Stop on zero or multiple compatible matches |
| validate_assignment_status_fsm_package | Create or edit is requested | Task code and resolved business values | Fresh export from shared.setup-export.task-level-export | ASM_SETUP_CSV_METADATA.xml marker, exported object CSV, scoped parent keys and rows, and ZIP bytes | Obtain the same-task export, populate only the requested row, and validate the exact-case marker, CSV name, keys, and scope. Preserve the ZIP bytes after preview. | Validated FSM archive for core.data-loader; Fusion operation submitTaskCSVImport | Stop only when the fresh export cannot be obtained or validated. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.READ | decision | 3 | reference_lookup | resolved->AS.DEFAULTS;not_found->AS.ERROR;ambiguous->AS.ERROR;failed->AS.ERROR | AS.DEPENDENCY | stop | Read is requested, or exact target and reference resolution is required before create or edit |
