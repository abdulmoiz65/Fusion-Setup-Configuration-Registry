# Manage Departments Dependency Readiness

## Purpose

Defines the conditional business references used by Manage Departments.
Dependencies are evaluated only for the requested operation or supplied field
and are never created or inferred by this task.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Department identity | Resolve the target or confirm that the proposed create identity is available |
| 2 | Delete history | Resolve the retained start and inclusive deletion end against complete Department history for delete-effective-split |
| 3 | Reference-data set | Resolve the supplied Department Set before dependent attributes |
| 4 | Location | Resolve a supplied Location effective on the Department date |
| 5 | Action Reason | Resolve a supplied Action Reason to one stored pair |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| department_identity | Existing Department or create-availability evidence | Conditional | Read, edit, inactivate, delete-effective-split, or create duplicate check | Lookup | Departments resource | find_manage_departments | Prevents an ambiguous target or duplicate create | Provide one exact Department selector | Resolved Department identity and current values |
| department_delete_history | Complete Department history | Conditional | delete-effective-split | Lookup | hcmDateEffectiveObjectHistory | resolve_department_delete_history | Prevents deletion of a logical Department or unintended history range | Provide the effective start of the last row to retain and the inclusive end date of the last split to remove | Confirmed retained start and deletion end |
| department_set | Department Set | Conditional | Create supplies a Department Set | Verify | shared.validation.reference-data-validator | resolve_department_set | Preserves one exact SetId, SetCode, and SetName tuple | Provide one exact set candidate | SetId, SetCode, and SetName |
| location | Location | Conditional | Create or edit supplies a Location | Verify | locationsLov effective on the Department date | resolve_department_location | Prevents an inactive, ineffective, or ambiguous Location reference | Provide one exact Location code or name | LocationId and LocationCode |
| action_reason | Action Reason | Conditional | Create or edit supplies an Action Reason | Verify | Current describe-declared actionReasonsLOV | resolve_department_action_reason | Preserves one exact stored Action Reason pair | Provide one exact code or meaning | ActionReasonCode and ActionReasonId |

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
| DEPT.DEPENDENCIES | decision | 4 | resolve_dependency | ready->DEPT.DEFAULTS;not_required->DEPT.DEFAULTS;needs_input->DEPT.ERROR;unresolved->DEPT.ERROR | DEPT.HISTORY | stop | After target and delete-history resolution and before defaulting |
