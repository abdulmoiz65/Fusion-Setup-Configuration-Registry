# Manage Divisions Dependency Readiness

## Purpose

Defines the identity dependency for Manage Divisions.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Division identity | Resolve the target or confirm create availability |
| 2 | Delete history | Resolve the retained start and inclusive deletion end against complete Division history for delete-effective-split |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| division_identity | Existing Division or create-availability evidence | Conditional | Read, edit, inactivate, delete-effective-split, or create duplicate check | Lookup | Divisions resource | find_manage_divisions | Prevents ambiguity and duplicates | Provide one exact selector | Division identity and current values |
| division_delete_history | Complete Division history | Conditional | delete-effective-split | Lookup | hcmDateEffectiveObjectHistory | resolve_division_delete_history | Prevents deletion of a logical Division or unintended history range | Provide the effective start of the last row to retain and the inclusive end date of the last split to remove | Confirmed retained start and deletion end |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact evidence exists | No |
| Lookup | The declared resolver can resolve the dependency | Read-only lookup only |
| Not Applicable | The condition is false | No |
| Needs Input | A selector is missing | No |
| Unresolved | Resolution is absent or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DIV.DEPENDENCIES | decision | 6 | resolve_dependency | ready->DIV.DEFAULTS;not_required->DIV.DEFAULTS;needs_input->DIV.ERROR;unresolved->DIV.ERROR | DIV.VALUESET | stop | After applicable reference lookups |
