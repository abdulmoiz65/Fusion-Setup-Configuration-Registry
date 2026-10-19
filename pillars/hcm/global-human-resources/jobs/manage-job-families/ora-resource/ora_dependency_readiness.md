# Manage Job Families Dependency Readiness

## Purpose

Defines the conditional Job Family, association, limit, and delete-history
dependencies. They are evaluated only when applicable.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Job Family identity | Resolve the current target or confirm the proposed create identity is available |
| 2 | Job Subfamily | Resolve one enabled effective Job Subfamily when the association is supplied |
| 3 | Association state and limit | Read current associations and the configured limit when associations are modified |
| 4 | Job references | Prove that no Job references the exact target before either delete mode |
| 5 | Delete history | For effective-split delete, resolve the retained predecessor and final future split |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| job_family_identity | Existing Job Family or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Job Families resource | find_manage_job_families | Prevents an ambiguous target or duplicate create | Provide one exact Job Family selector | Resolved Job Family identity and current values |
| job_subfamily | Job Subfamily association | Conditional | Create or edit supplies a Job Subfamily | Lookup | Common Lookup type ORA_PER_WS_JOB_SUB_FAMILY | resolve_job_family_subfamily | Prevents an invalid, disabled, or ineffective association | Provide one exact code or meaning and effective date | Stored Job Subfamily code, meaning, and effective range |
| association_state | Current Job Subfamily associations | Conditional | An association is read, changed, or verified | Lookup | Direct Job Subfamily association collection | read_job_family_associations | Prevents reliance on an incomplete parent expansion | Provide one exact Job Family | Complete current association set |
| association_limit | Job Subfamily association limit | Conditional | Create or edit supplies associations | Lookup | Effective profile value | resolve_job_family_association_limit | Enforces a configured maximum without inventing one | No input is required | Numeric maximum or not_configured |
| job_references | Zero Job references | Mandatory | Any delete | Lookup | Jobs resource | find_job_references_for_job_family | Prevents deletion of an in-use Job Family | No input is required | Complete zero-reference evidence |
| delete_history | Bounded future effective split | Conditional | Effective-split delete | Lookup | Current Job Family finder | read_job_family_delete_history | Preserves the predecessor and blocks first, nonfinal, or nonfuture split deletion | Provide the selected EffectiveStartDate | Retained start, deleted end, and internal eligibility |

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
| JF.DEPENDENCIES | decision | 3 | resolve_dependency | ready->JF.DEFAULTS;not_required->JF.DEFAULTS;needs_input->JF.ERROR;unresolved->JF.ERROR | JF.READ | stop | After target and association lookups and before defaulting |
