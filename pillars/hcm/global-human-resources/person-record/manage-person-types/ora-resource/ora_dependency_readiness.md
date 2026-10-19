# Manage Person Types Dependency Readiness

## Purpose

Defines the conditional System/User Person Type business key and Active lookup
used by Manage Person Types. Dependencies are evaluated only for the requested
operation or supplied field and are never created implicitly.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | System Person Type | Resolve one enabled System Person Type |
| 2 | Person Type target | When required, resolve the exact System/User Person Type pair |
| 3 | Active value | Resolve an explicitly supplied Active value to one enabled stored code |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| system_person_type | Enabled System Person Type | Conditional | Read, create identity check, edit, or delete | Lookup | System Person Type lookup | resolve_system_person_type | Supports system-type scope resolution | Provide the System Person Type | Enabled SystemPersonType code |
| person_type_target | Exact System/User Person Type pair | Conditional | Read, create identity check, edit, or delete | Lookup | Person Types resource | find_manage_person_types | Prevents an incorrect exact target | Provide the System Person Type and, for an exact target, User Person Type | Current person-type values and current-run identity |
| active_value | Active lookup value | Conditional | Active is explicitly supplied | Lookup | Common Lookup type YES_NO | resolve_person_type_active | Stores one enabled code rather than an unverified display value | Provide one exact code or meaning | LookupCode mapped to ActiveFlag |

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
| PT.DEPENDENCY | decision | 2 | resolve_dependency | ready->PT.READ;not_required->PT.READ;needs_input->PT.ERROR;unresolved->PT.ERROR | PT.VALIDATE | stop | After input validation and before task-local reference lookups |
