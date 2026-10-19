# Manage Action Reasons Dependency Readiness

## Purpose

Defines the conditional business references used by Manage Action Reasons.
Dependencies apply only to the requested reason or association and are never
created, inferred, or copied from another action reason.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Action Reason identity | Resolve the current target or confirm that the proposed Reason Code is available |
| 2 | Country and configured references | Resolve each supplied country and configured lookup value exactly |
| 3 | Role | Resolve a supplied role to one current stored value |
| 4 | Parent Action | Resolve one current Action only when an action-reason association is requested |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| action_reason_identity | Existing Action Reason or create-availability evidence | Conditional | Read, edit, delete, association work, or create duplicate check | Lookup | Action Reasons resource | find_manage_action_reasons | Prevents an ambiguous target or duplicate Reason Code | Provide one exact Reason Code or current identifier | Resolved Action Reason identity and current values |
| country | Country | Conditional | A country-specific value is supplied | Lookup | Current country configuration | resolve_action_reason_country | Establishes the stored country or legislation value | Provide one exact country code or name | Stored country or legislation value |
| configured_lookup | Configured lookup value | Conditional | A lookup-backed Action Reason field is supplied | Lookup | Current Common Lookup configuration | resolve_action_reason_common_lookup | Prevents an invalid, disabled, or ineffective stored code | Provide one exact code or meaning | Stored lookup code |
| role | Role | Conditional | A role value or role association is supplied | Lookup | Current role configuration | resolve_action_reason_role | Prevents an unresolved role association | Provide one exact role code or name | Stored role value |
| parent_action | Parent Action | Conditional | An action-reason usage association is requested | Lookup | Current Actions resource | resolve_action_reason_action | Keeps the association attached to one exact existing Action | Provide one exact Action code or name | Resolved Action identity |

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
| AR.DEPENDENCIES | decision | 2 | resolve_dependency | ready->AR.READ;not_required->AR.READ;needs_input->AR.ERROR;unresolved->AR.ERROR | AR.VALIDATE | stop | After input validation and before task-local reference lookups |
