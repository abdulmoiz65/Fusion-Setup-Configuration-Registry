# Manage Actions Dependency Readiness

## Purpose

Defines the conditional business references used by Manage Actions.
Dependencies apply only to the requested Action or association and are never
created, inferred, or copied from another Action.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Action identity | Resolve the current target or confirm that the proposed Action Code is available |
| 2 | Country | Resolve a supplied country before country-scoped references |
| 3 | Lookup-backed values | Resolve each supplied Action Type, Action Reason, assignment status, or configured lookup value |
| 4 | Role | Resolve one active role when an action-reason role mapping is requested |
| 5 | Action-reason role mapping | Confirm the exact Action, Action Reason, active Role, and supported association shape together |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| action_identity | Existing Action or create-availability evidence | Conditional | Read, copy, edit, delete, association work, or create duplicate check | Lookup | Actions resource | find_manage_actions | Prevents an ambiguous target or duplicate Action Code | Provide one exact Action Code, name, or current identifier | Resolved Action identity, effective context, and current associations |
| country | Country | Conditional | A country is supplied or required by the requested association | Lookup | Current country configuration | resolve_action_country | Establishes the country scope for dependent values | Provide one exact country code or name | Validated country code |
| configured_lookup | Action Type, Action Reason, assignment status, or configured lookup value | Conditional | The corresponding value is supplied | Lookup | Current Common Lookup configuration | resolve_action_common_lookup | Prevents invalid, disabled, or ineffective stored values | Provide one exact code or meaning and effective date | Registered-object-compatible stored value |
| role | Action-reason role | Conditional | An action-reason role mapping is supplied | Lookup | Current authorized role configuration | resolve_action_role | Keeps the mapping attached to one active exact role | Provide one exact role name | Active RoleCode and RoleName |
| action_reason_role_mapping | Action-reason role mapping | Conditional | An action-reason role mapping is requested | Verify | Resolved Action, Action Reason, Role, and current association evidence |  | Prevents an association with an unresolved parent or unsupported mapping shape | Supply one exact Action, Action Reason, and active Role | Confirmed parents and supported association values |

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
| ACT.DEPENDENCIES | decision | 2 | resolve_dependency | ready->ACT.READ;not_required->ACT.READ;needs_input->ACT.ERROR;unresolved->ACT.ERROR | ACT.VALIDATE | stop | After input validation and before task-local reference lookups |
