# Manage Collective Agreements Dependency Readiness

## Purpose

Defines the conditional business references that must be available when a
Collective Agreement request uses them. Dependencies are evaluated only when
applicable and are never created or inferred by this task.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Agreement identity | Resolve the target for read, edit, or delete, or confirm that the proposed identity is available for create |
| 2 | Legislation and organization scope | Confirm each supplied country or legislation, Legal Employer, Union, and bargaining unit in that order |
| 3 | Lookup-backed values | Resolve each supplied status or configured lookup value to one compatible stored value |
| 4 | EFF context and value | Resolve current EFF metadata before resolving any lookup-backed segment value |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| agreement_identity | Existing agreement or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Collective Agreements resource | find_manage_collective_agreements | Prevents an ambiguous target or duplicate create | Provide one exact agreement identifier, code, or name | Resolved agreement identity and effective context |
| legislation_scope | Country or legislation | Conditional | A country or legislation is supplied or required by a selected reference | Verify | Current request and existing Fusion setup |  | Establishes the effective legislative scope for dependent references | Provide one exact country or legislation | Confirmed legislation scope |
| organization_scope | Legal Employer, Union, or bargaining unit | Conditional | The corresponding association is supplied | Verify | Existing effective organization setup |  | Prevents an unresolved or incompatible organization association | Provide one exact value for each requested association | Confirmed organization references |
| status_lookup | Agreement status or configured lookup value | Conditional | A status or configured lookup value is supplied | Lookup | Common lookup configuration | resolve_status_lookup | Stores the enabled effective code rather than a display value | Provide one exact code or meaning and effective date | Stored agreement-status code |
| eff_metadata | EFF context and segment contract | Conditional | An EFF context or segment is requested | Lookup | Current Collective Agreements describe | resolve_collective_agreement_eff_metadata | Prevents a value from being placed in an unsupported context or attribute | Provide the requested context and business segment | Context, segment, target attribute, and value-set contract |
| eff_value | EFF lookup-backed segment value | Conditional | Current segment metadata declares an LOV and a value is supplied | Lookup | Describe-declared EFF value set | resolve_collective_agreement_eff_value_set | Stores one compatible typed value for the resolved segment | Provide one exact display value | Metadata-declared stored code or ID |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Run the read-only resolver now; do not pause |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CA.DEPENDENCIES | decision | 2 | resolve_dependency | ready->CA.READ;not_required->CA.READ;needs_input->CA.ERROR;unresolved->CA.ERROR | CA.VALIDATE | stop | After input validation and before task-local reference lookups |

## Date-effective Split Dependency

For delete, split history is mandatory: resolve the complete ordered timeline through hcmDateEffectiveObjectChanges before source authoring or approval. Stop when history is incomplete, a selected start date is absent, the selection is the first/only split, an adjacent boundary is ambiguous, or the loader template does not accept the required retained predecessor key and `SET PURGE_FUTURE_CHANGES Y` directive.


## Corrected HDL Split-Deletion Contract (Supersedes Earlier Examples)

Use exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one retained-predecessor `MERGE` row, with DAT dates in `YYYY/MM/DD`. The retained predecessor start and final selected end bound the contiguous removal. Reject HDL DELETE, mixed instructions, ISO DAT dates, first/only split deletion, and any REST mutation.
