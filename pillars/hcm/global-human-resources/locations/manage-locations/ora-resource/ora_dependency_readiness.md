# Manage Locations Dependency Readiness

## Purpose

Defines the conditional Location target, reference-data set, and country-specific
MAIN-address contract used by Manage Locations. Dependencies are evaluated only for the
requested operation and missing setup is never created implicitly.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Location identity | Resolve the target or confirm that the proposed create identities are available |
| 2 | Reference-data set | Resolve one exact set for create or a supplied edit change |
| 3 | MAIN address contract | Resolve the country's SUPP_TAX_AND_RPTNG_ADDR layout and require its mandatory MAIN-address fields on create |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| location_identity | Existing Location or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Locations resource | find_manage_locations | Prevents an ambiguous target or duplicate create | Provide exact identity values or a bounded search fragment | Resolved Location identity or create-availability evidence |
| reference_data_set | Reference-data set | Conditional | Create or edit supplies reference-data scope | Lookup | Current reference-data set LOV | resolve_location_reference_set | Keeps the Location in one existing reference-data set | Provide one exact SetCode or SetId | SetCode and SetId |
| action_reason | Action reason | Conditional | Create or date-effective edit explicitly supplies an action reason | Lookup | Current describe-declared actionReasonsLOV | resolve_location_action_reason | Ensures a user-supplied reason is valid for the operation and requested date | Provide the exact user-supplied operation-appropriate reason; never source it from a prior or create row | ActionReasonCode and ActionReasonId |
| main_address | Country-specific MAIN address contract | Conditional | Create, MAIN-address edit, or a complete read requests address details | Lookup | Current country, SUPP_TAX_AND_RPTNG_ADDR layout, Locations describe, and address child | resolve_location_address_contract | Requires one complete MAIN address using the country layout | Provide Country for create or a country change, plus only missing labelled values | Loader mapping for mutation; current MAIN-address values for read |
| location_delete_history | Complete Location history and bounded delete range | Yes | Date-effective delete | Lookup | Every LocationHistoryDef page | resolve_location_delete_history | Protects the first history row and derives the only permitted retained/deleted range | Provide one exact non-first EffectiveStartDate | LocationId, predecessor EffectiveStartDate, selected EffectiveEndDate, FirstSplitFlag eligibility, and before/after evidence |

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
| LOC.DEPENDENCIES | decision | 5 | resolve_dependency | ready->LOC.DEFAULTS;not_required->LOC.DEFAULTS;needs_input->LOC.ERROR;unresolved->LOC.ERROR | LOC.ADDRESS | stop | After Location, set, and address lookups and before defaulting |
