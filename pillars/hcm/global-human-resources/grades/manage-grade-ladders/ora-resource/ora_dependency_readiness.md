# Manage Grade Ladders Dependency Readiness

## Purpose

Defines the conditional Grade, Step, Legislative Data Group, lookup, and
currency references used by Manage Grade Ladders. Dependencies are resolved
only for applicable ladder or rate content and are never created implicitly.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Grade Ladder identity | Resolve the current target or confirm the proposed create identity is available |
| 2 | Grade Set, Grade, and Steps | Use the explicit or defaulted Grade Set; resolve active STEP Grades, ordered Steps, Step count, and ceiling Step |
| 3 | Legislative Data Group | Resolve one LDG when a rate row is supplied |
| 4 | Rate lookups and currency | Resolve supplied rate type, frequency, status, and currency in the LDG context |
| 5 | Effective-split deletion range | Resolve the retained start and inclusive deletion end before removing future splits |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| grade_ladder_identity | Existing Grade Ladder or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Grade Ladders resource | find_manage_grade_ladders | Prevents an ambiguous target or duplicate create | Provide one exact ladder selector | Resolved ladder identity and current values |
| grade | Grade | Conditional | A Grade is supplied | Lookup | Current Grade setup | resolve_grade_ladder_grade | Prevents an inactive, ineffective, wrong-type, or wrong-set Grade | Provide one exact Grade and effective date; Grade Set defaults to COMMON | GradeId, GradeCode, Name, SetId, SetName, and item link |
| grade_steps | Ordered Grade Steps | Conditional | A Grade is supplied | Lookup | Resolved Grade V2 item | resolve_grade_ladder_steps | Requires a nonempty ordered Step collection for every supplied Grade | Provide the intended Grade and effective date | Ordered GradeStepId values, GradeStepsCount, and GradeCeilingStepId |
| legislative_data_group | Legislative Data Group | Conditional | A rate row is supplied | Lookup | Current LDG setup | resolve_grade_ladder_ldg | Establishes the rate parent key, legislation, and default currency | Provide one exact LDG name or ID | LegislativeDataGroupName, LegislativeDataGroupId, LegislationCode, and DefaultCurrencyCode |
| rate_lookups | Rate type, frequency, and status | Conditional | The corresponding value is supplied or defaulted | Lookup | Current Common Lookup configuration | resolve_grade_ladder_lookup_codes | Stores enabled effective codes | Provide one exact code or meaning and effective date | LookupCode and Meaning |
| currency | Currency | Conditional | A rate row is supplied | Lookup | Current currency configuration | resolve_grade_ladder_currency | Confirms one currency compatible with the resolved LDG | Provide one currency code or accept the resolved LDG default | CurrencyCode and Name |
| grade_ladder_split_deletion_range | Effective-split deletion range | Conditional | delete-effective-split | Lookup | Grade Ladder history and current generated loader contract | resolve_grade_ladder_split_deletion_range | Prevents logical-record deletion or an unintended history range | Provide the effective start of the last row to retain and the inclusive end date of the last split to remove | Confirmed retained start, deletion end, and predecessor values |

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
| GLAD.DEPENDENCIES | decision | 2 | resolve_dependency | ready->GLAD.READ;not_required->GLAD.READ;needs_input->GLAD.ERROR;unresolved->GLAD.ERROR | GLAD.VALIDATE | stop | After input validation and before task-local reference lookups |
