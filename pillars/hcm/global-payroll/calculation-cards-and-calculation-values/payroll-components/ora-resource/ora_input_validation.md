# Payroll Components Input Validation

## Scope

This task accepts read-only discovery plus two native HCM Data Loader Create
shapes for the **Deduction Type** business object:

- Parent Payroll Component Create with discriminator `PayrollDeductionType`.
- Reference Child Create with discriminator `DeductionContextUsage`.

Correct, Update, Delete, and every unlisted lifecycle mutation are deferred
future work and return `PCOMP_HDL_ROUTE_FROZEN`. End Date, translation Create,
specific tax reporting unit assignments, and Calculation Card references are
`UNSUPPORTED` because the delivered native contract lacks the required action,
discriminator, or field. Both classes stop before DAT authoring.

## Input Kind and Continuation Contract

| Input Kind | Prompt Label | Behavior |
|---|---|---|
| fusion_lov | Select from Fusion | Run the declared scoped read-only resolver, show business labels, and require an explicit selection. |
| fixed_choice | Select one | Show the complete task-supported set. Do not run a Fusion LOV. |
| free_form | Enter a free-form value | Ask for a business-authored value and state its validation rule. |
| defaulted | No prompt unless override is supported | Apply only the declared default and bind it to task validation; core/data-loader owns any user-facing report. |
| derived_or_route_owned | No prompt | Resolve internally; never request or display a surrogate ID, source key, link, or transport value. |

The Source System Owner is a `fusion_lov` choice, not a derived value. Its
returned business meaning may be shown, with `LookupCode` only as a
disambiguator. The generated `SourceSystemId` and combined source-key identity
remain internal and are never added to the core approval report.

For a required Fusion choice with more than 20 eligible values, ask for a
business-name or business-code search term and show at most 20 sorted,
case-insensitive contains matches per page. Never require an unseen exact
value. After every accepted answer, invalidate affected dependent values,
resolve the next dependency, and end with the next actionable question.

## Supported Create Profiles

| Profile | Business Purpose | HDL Rows | Evidence Boundary |
|---|---|---|---|
| create_parent | Create a Payroll Component | One MERGE&#124;PayrollDeductionType; zero child rows | Direct native-HDL load and exact read-back proved |
| create_reference_t | Add a Wage Basis Rule reference | Zero parent rows; one MERGE&#124;DeductionContextUsage with UsageType=T | Native child discriminator, T value, complete field shape, load, and exact read-back directly proved |
| create_reference_c | Add a Calculation Factor reference | Zero parent rows; one MERGE&#124;DeductionContextUsage with UsageType=C | Same native child field shape; C is Fusion-valid and REST-proved, and remains an explicit QA coverage case |

The business journey selection derives T or C internally; neither usage code is
ordinary user input. The nonproduction evidence gate for C is owned by
`ora_design_enforcement.md`.

`create_reference` is the operation family name. After journey selection it is
specialized as `create_reference_t` or `create_reference_c`; receipts and
reconciliation use the specialized profile name.

## Native HDL Record Allowlists

The archive contains one member named `PayrollDeductionType.dat`. Validate the
selected operation against the exact ordered field set below. Do not add fields
merely because they appear in live metadata, product REST, historical evidence,
or the source-reference tail of the delivered template.

| Operation | Exact Ordered Fields |
|---|---|
| Parent Create | DeductionCode, DeductionName, LegislativeDataGroupName, DeductionGroupId, DisplaySequence, UseAllTaxUnits |
| Reference Child Create root METADATA header | DeductionCode, LegislativeDataGroupName; header only, with no parent data row |
| Reference Child Create | DeductionTypeId, LegislativeDataGroupId, ContextId, UsageType, Sequence, NavigationUse, SourceSystemOwner, SourceSystemId |

A child-only DAT starts with the exact root header
`METADATA|PayrollDeductionType|DeductionCode|LegislativeDataGroupName`, followed
by the child header and one child row; it contains no parent data row. A
parent-only DAT contains no child metadata or data row. Translation rows belong
to the separate `PayrollDeductionTypeTranslation` object and are prohibited in
these packets.

For parent identity, `DeductionCode + LegislativeDataGroupName` is the
business user key. `DeductionGroupCode` is the business-facing alternative for
the required Component Group foreign key; it is not an additional parent-key
segment. The proved Create packet resolves the selected group to the internal
`DeductionGroupId` and never requests that ID from the user.

Although the delivered child metadata marks `SourceSystemOwner` and
`SourceSystemId` optional, retained live loader evidence rejected the current
ID-based child packet without a supported unique key. The current UI context
lookup does not expose `ContextCode`, which is needed for the complete business
user key. Therefore the proved child profile requires an active Fusion-selected
source owner plus a fresh operation-derived source ID. Never invent or hardcode
a tenant owner.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation and environment | operation, environmentAlias | Return NEEDS_INPUT | Select read-only discovery or one supported Create profile, plus one configured environment alias | Every request | |
| Legislative scope | LegislativeDataGroupName | Return NEEDS_INPUT | Select an exact LDG business name; retain its ID and legislation internally | Parent or child Create, or scoped component/reference read | find_legislative_data_group |
| Parent business values | DeductionCode, DeductionName, DisplaySequence | Return NEEDS_INPUT | Collect validated free-form business values | Parent Create | |
| Component Group | ComponentGroupName | Return NEEDS_INPUT | Select an exact Component Group in the resolved legislation | Parent Create | find_component_group |
| Existing Payroll Component | DeductionCode or component name | Return NEEDS_INPUT | Select one exact existing component in the LDG | Read-only component/reference review or Reference Child Create | find_payroll_component |
| Reference journey | ReferenceJourney | Return NEEDS_INPUT | Select Wage Basis Rule Reference or Calculation Factor Reference | Reference Child Create | map_reference_journey |
| Reference context | DisplayContextName | Return NEEDS_INPUT | Select one exact current context label | Reference Child Create | find_reference_context |
| Source System Owner | SourceOwnerName or SourceSystemOwner | Return NEEDS_INPUT | Select one active current HRC_SOURCE_SYSTEM_OWNER row by business meaning or code | Reference Child Create | resolve_active_source_owner |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Deduction Code is nonblank and at most 240 characters | Continue; otherwise INPUT_VALIDATION | Parent Create | |
| Component Name is nonblank and at most 240 characters | Continue; otherwise INPUT_VALIDATION | Parent Create | |
| Any authored text contains pipe, CR, LF, or NUL | Block because the value cannot be represented safely in the current deterministic pipe-delimited DAT contract; do not call the tenant value invalid | Parent or child Create | |
| Display Sequence is an integer greater than or equal to zero | Continue; otherwise INPUT_VALIDATION | Parent Create | |
| UseAllTaxUnits is omitted or the lowercase string true | Apply or retain true; an explicit false or specific-unit request is UNSUPPORTED | Parent Create | |
| Reference Sequence is a positive integer | Continue; default to 1 only when omitted | Reference Child Create | |
| Display in Overview is Yes or No | Derive lowercase true or false; default to No when omitted | Reference Child Create | |
| Reference journey is Wage Basis Rule Reference | Derive UsageType=T | Reference Child Create | map_reference_journey |
| Reference journey is Calculation Factor Reference | Derive UsageType=C | Reference Child Create | map_reference_journey |
| A Fusion ID is supplied instead of a required business label | Return INPUT_VALIDATION for the raw ID; if the business label is still missing, return NEEDS_INPUT and run its declared resolver | Every request | |
| End Date, another date-effective field, a calculation-card component reference, or a translation Create field is supplied | Return UNSUPPORTED before DAT authoring because the native Create shape lacks that capability | Every Create | |
| Effective-Of, child ID, object version, or an undeclared source-reference field is supplied as authored Create input | Return INPUT_VALIDATION; remove the transport-only or server-owned field and continue only with business inputs | Every Create | |
| Source System Owner resolves to one active effective lookup row | Use its LookupCode internally as SourceSystemOwner; otherwise return NOT_FOUND, AMBIGUOUS, or INPUT_VALIDATION | Reference Child Create | resolve_active_source_owner |
| SourceSystemId is supplied as authored input | Return INPUT_VALIDATION; the route allocates a fresh collision-resistant value internally | Reference Child Create | |
| A field is outside the selected operation allowlist and no more specific capability rule applies | Return INPUT_VALIDATION and identify the unexpected field; never silently strip it | Every Create | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Parent Create duplicate discovery finds zero exact Deduction Code plus LDG matches after complete pagination | READY | Continue to metadata and archive validation | find_payroll_component |
| Parent Create duplicate discovery finds one or more exact matches | CONFLICT | Stop and ask for a different business code or switch to a read request | find_payroll_component |
| Reference Child Create finds exactly one parent and zero exact parent plus LDG plus context plus journey matches | READY | Resolve or revalidate the required Source System Owner before source-ID allocation and archive validation | find_reference_children |
| Reference Child Create finds one or more exact parent plus LDG plus context plus journey matches | CONFLICT | Stop before DAT authoring and show only business-facing match details | find_reference_children |
| A lookup is incomplete or has conflicting returned key aliases | CATALOG_MISMATCH | Refresh the declared resolver; never guess or request an ID | |
| A required lookup has multiple exact eligible matches | AMBIGUOUS | Show business-facing distinctions and require explicit selection | |
| A selected lookup row or immutable validation fact changed | STALE_PLAN | Invalidate the plan and rerun validation through the declared route | |
| Calculation Card Reference or specific tax reporting units are requested | UNSUPPORTED | Explain the missing native-HDL field or discriminator and record the feature as future work | |
| Correct, Update, Delete, or another unlisted lifecycle mutation is requested | PCOMP_HDL_ROUTE_FROZEN | Stop before lookup for mutation inputs, archive authoring, Task Hook validation, or core approval | |
| End Date or translation Create is requested | UNSUPPORTED | Explain the missing date behavior or Create action and stop before DAT authoring | |

## Operation Isolation

- Start every Create with a new operation ID and empty operation-local business
  state.
- Re-resolve all IDs, links, defaults, duplicate evidence, and source-owner
  metadata for the selected environment.
- Parent and child creates use different archives, hashes, approvals, and
  loader requests. A newly created parent must reconcile before a child plan
  can use its internally resolved identity.
- Add no task-local upload, initiation, retry, or monitoring behavior. Hand the
  immutable plan to `core/data-loader` and follow its current governed
  lifecycle; never replay an uncertain write.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCOMP.VALIDATE_INPUT | decision | 1 | validate_input | valid->PCOMP.RESOLVE_DEPENDENCIES;invalid->PCOMP.HANDLE_ERROR | none | stop | Always |
