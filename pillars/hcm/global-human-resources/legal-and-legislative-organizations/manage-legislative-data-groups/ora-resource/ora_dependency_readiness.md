# Manage Legislative Data Groups Dependency Readiness

## Purpose

Defines the conditional Legislative Data Group target and country-localization
reference used by this task. The task resolves existing values only and never
creates or infers related legislative setup.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legislative Data Group identity | Resolve the current target or confirm that the proposed name is available; retain the returned LegislativeDataGroupId only for a delete |
| 2 | Country localization | Resolve one country and retain its supported territory, legislation, and default currency values |
| 3 | Related setup | Verify one exact existing legislation or Legislative Data Group when a related business value requires it |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| legislative_data_group_identity | Existing LDG or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Legislative Data Groups resource | find_manage_legislative_data_groups | Prevents an ambiguous target or duplicate name | Provide one exact LDG name or current identifier | Create-availability evidence or resolved LDG values; for delete, the returned LegislativeDataGroupId only |
| country_localization | Country, legislation, and default currency | Conditional | Create or edit changes Country or Currency | Lookup | Current country-localization configuration | resolve_country_localization | Keeps territory, legislation, and currency values from one compatible country result | Provide one exact country | Territory, LegislationCode, and default Currency |
| related_setup | Related legislation or Legislative Data Group | Conditional | A related business value is supplied or required | Verify | Current task input and existing legislative setup |  | Prevents an unresolved or ambiguous related value | Provide one exact related business value | Confirmed legislation or Legislative Data Group value |

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
| LDG.DEPENDENCIES | decision | 4 | resolve_dependency | ready->LDG.DEFAULTS;not_required->LDG.DEFAULTS;needs_input->LDG.ERROR;unresolved->LDG.ERROR | LDG.COUNTRY | stop | After target and country-localization lookups and before defaulting |
