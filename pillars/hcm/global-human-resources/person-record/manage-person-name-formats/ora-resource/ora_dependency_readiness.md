# Manage Person Name Formats Dependency Readiness

## Purpose

Defines the conditional country, format, target, and component-token references
used by Manage Person Name Formats. Dependencies are resolved only when their
fields apply and are never created or derived from display text.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Name Format scope and identity | Resolve the country or legislation, format type, and current target together |
| 2 | Ordered component tokens | Resolve one proven stored token for every supplied component, whitespace separator, literal character, or separator label; resolve the preferred and fallback token independently for every replacement component |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| name_format_identity | Country-scoped Name Format target | Conditional | Read, edit, delete, or create identity check | Lookup | Name Formats resource and current Data Loader template | find_manage_person_name_formats | Prevents an ambiguous country, format scope, or current target and selects the least-coupled accepted source identity | Provide one exact country or legislation and format selector | Country, LegislationCode, FormatName, format type, scope, current components, and whether the live operation accepts a source-system identity or natural scope key before `NameFormatId` |
| component_tokens | Ordered Name Format component, separator, literal-character, and replacement-component tokens | Conditional | Create or edit supplies component or separator labels | Lookup | Current Name Format rows, component metadata, and `PER_NAME_SUB_FORMAT_COMPONENTS` | resolve_name_format_component_token | Prevents guessed abbreviations or unsupported mask tokens | Provide the ordered components and literal separators; use the proven literal mapping table. For each replacement component, provide the preferred then fallback core attributes. | Ordered stored tokens used to build FormatMask |

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
| PNF.DEPENDENCY | decision | 2 | resolve_dependency | ready->PNF.READ;not_required->PNF.READ;needs_input->PNF.ERROR;unresolved->PNF.ERROR | PNF.VALIDATE | stop | After input validation and before task-local reference lookups |
