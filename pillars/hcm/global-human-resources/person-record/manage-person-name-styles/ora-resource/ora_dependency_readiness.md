# Manage Person Name Styles Dependency Readiness

## Purpose

Defines the conditional country, component, parent-row, and target references
used by Manage Person Name Styles. Dependencies are scoped to the requested
style and are never created or borrowed from another country context.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Country context | Resolve a supplied country or legislation before the Name Style read |
| 2 | Name Style identity | Resolve the current target or confirm the requested scope is available |
| 3 | Name component | Resolve each supplied component within the established country context |
| 4 | Parent source row | Confirm the parent style precedes requested child rows in the approved source |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| country_context | Country or legislation | Conditional | Read, create, or edit targets a country-specific style | Lookup | Current approved country or legislation reference | resolve_country_context | Establishes the country scope before resolving the style | Provide one exact country or legislation | CountryName, LegislationCode, and grouping context |
| name_style_identity | Existing Name Style or create-availability evidence | Conditional | Read, edit, or create identity check | Lookup | Name Styles resource | find_manage_person_name_styles | Prevents an ambiguous target or duplicate scope | Provide one exact style selector | Resolved style identity and current values |
| name_component | Enabled Name Style component | Conditional | A Name Component is supplied | Lookup | Common Lookup type PER_NAME_STYLE_ATTRIBUTES | resolve_name_style_component | Prevents display-label or unsupported-component values | Provide one exact component code or meaning | Stored component code |
| parent_before_child | Parent Name Style source row | Conditional | Child Name Style rows are requested | Verify | Reviewed task source | validate_parent_before_child | Keeps child rows attached to their requested parent style | Include the parent before its child rows | Ordered parent and child source rows |

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
| PNS.DEPENDENCY | decision | 2 | resolve_dependency | ready->PNS.READ;not_required->PNS.READ;needs_input->PNS.ERROR;unresolved->PNS.ERROR | PNS.VALIDATE | stop | After input validation and before task-local reference lookups |
