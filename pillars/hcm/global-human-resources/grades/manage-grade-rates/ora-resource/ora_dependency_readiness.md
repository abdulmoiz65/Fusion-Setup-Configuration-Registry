# Manage Grade Rates Dependency Readiness

## Purpose

Defines the conditional Legislative Data Group, lookup, currency, Grade, and
target references used by Manage Grade Rates. Dependencies apply only to the
requested rate content and are never created by this task.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Grade Rate identity | Resolve the current target or confirm the proposed create identity is available |
| 2 | Legislative Data Group | Resolve one effective LDG and retain its name, ID, legislation, and default currency when available |
| 3 | Rate lookups | Resolve enabled effective rate type, frequency, and populated active status values |
| 4 | Currency | Validate the supplied currency, or the LDG default when create omits currency |
| 5 | Grades | Resolve each Grade referenced by a rate-value row |
| 6 | Effective-split deletion range | Resolve the retained start and inclusive deletion end before removing a future split |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| grade_rate_identity | Existing Grade Rate or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Grade Rates resource | find_manage_grade_rates | Prevents an ambiguous target or duplicate create | Provide one exact Grade Rate selector | Resolved rate identity and current values |
| legislative_data_group | Legislative Data Group | Yes | Create; edit preserves the current LDG | Lookup | Current LDG setup | resolve_grade_rate_ldg | Establishes the legislation and supplies the create-only currency default; the LDG is not changed in place | Provide one exact LDG for create | Name -> LegislativeDataGroup, LegislativeDataGroupId, LegislationCode, and DefaultCurrencyCode when available |
| rate_lookups | Rate type, frequency, and active status | Conditional | Create or the corresponding field changes | Lookup | Current Common Lookup configuration | resolve_grade_rate_lookup_codes | Stores enabled effective codes and requires ActiveStatus to be populated | Provide one exact code or meaning and effective date | LookupCode and Meaning |
| currency | Currency | Conditional | Create, or edit supplies CurrencyCode | Lookup | Current currency configuration | resolve_grade_rate_currency | Requires one enabled effective currency without forcing equality to the LDG default | Supply a currency or accept the LDG default on create | CurrencyCode and Name |
| grade | Grade | Conditional | A rate-value row is supplied | Lookup | Current Grade setup | resolve_grade_rate_grade | Keeps each child row attached to one active effective Grade without exposing its internal identifier | Provide one exact Grade name or code and provide SetCode only when multiple Grade Sets match; RateObjectId is not user input | GradeCode and SetCode for the GradeRateValue user key; GradeId retained internally and used as RateObjectId only when Core Data Loader selects the internal-ID alternative |
| grade_rate_split_deletion_range | Effective-split deletion range | Conditional | delete-effective-split is requested | Lookup | Grade Rates resource | resolve_grade_rate_split_deletion_range | Prevents deletion of a logical Grade Rate or unintended history range | Provide the effective start of the last row to retain and the inclusive end date of the last split to remove | Confirmed retained start, deletion end, predecessor values, and future GradeRateValue rows for reconciliation |

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
| GRAT.DEPENDENCIES | decision | 2 | resolve_dependency | ready->GRAT.READ;not_required->GRAT.READ;needs_input->GRAT.ERROR;unresolved->GRAT.ERROR | GRAT.VALIDATE | stop | After input validation and before task-local reference lookups |
