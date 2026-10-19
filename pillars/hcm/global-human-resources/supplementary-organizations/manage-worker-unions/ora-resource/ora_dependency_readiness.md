# Manage Worker Unions Dependency Readiness

## Purpose

Defines the conditional country, classification, EFF, bargaining-unit, code,
and target references used by Manage Worker Unions. Dependencies are resolved
only when applicable. A missing bargaining unit is created only with user
agreement through Manage Common Lookups.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Worker Union identity | Resolve the target or confirm that the proposed Union name is available |
| 2 | Country | Resolve one country before country-scoped organization information |
| 3 | Organization component contract | Confirm the Organization, OrgUnitClassification, and conditional OrgInformation hierarchy for a mutation |
| 4 | Classification parent | Resolve the effective Worker Union classification when Additional Information is requested |
| 5 | EFF context and segment | Resolve current context and segment metadata before any lookup-backed value |
| 6 | Bargaining unit and information code | Resolve a supplied bargaining unit; if agreed, create a missing value through Manage Common Lookups and re-resolve it; confirm a supplied Additional Information code is unique |
| 7 | Delete history | Resolve the retained start and inclusive deletion end against complete Worker Union history for delete-effective-split |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| worker_union_identity | Existing Worker Union or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Worker Unions resource | find_manage_worker_unions | Prevents an ambiguous target or duplicate create | Provide one exact OrganizationId or Union name and legislation context when needed | OrganizationId, effective context, current values, and create-availability evidence |
| country | Country | Conditional | Create or country change supplies a country | Lookup | Current country LOV | resolve_worker_union_country | Establishes one exact legislation context | Provide one exact country code or name | LegislationCode and display name |
| organization_components | Organization component contract | Conditional | Create or edit is requested | Verify | Current registered Organization business-object metadata | resolve_worker_union_components | Prevents guessed fields, missing parents, or an unsupported component hierarchy | Provide only requested business values; do not supply technical parent identifiers | Organization, OrgUnitClassification, and conditional OrgInformation mappings |
| classification_parent | Worker Union classification parent | Conditional | OrgInformation is supplied | Lookup | Current Organization classification metadata | resolve_worker_union_classification | Attaches Additional Information to the `ORA_PER_UNION` classification | Do not supply or guess a classification identifier | OrgUnitClassificationId, category `ORA_PER_UNION`, and effective values |
| eff_context | Additional Information context and segment | Conditional | Additional Information is supplied or its details are requested | Lookup | Current Worker Union EFF metadata | resolve_worker_union_eff_context | Prevents a value from being placed in the wrong context or attribute | Provide one exact context or business segment | Context, segment, type, cardinality, target attribute, and value-set contract |
| bargaining_unit | Associated bargaining unit | Conditional | An Associated Bargaining Units value is supplied | Lookup | Resolved segment value set; conditionally Manage Common Lookups | resolve_worker_union_bargaining_unit | Stores one existing value compatible with the resolved context segment | Provide one exact code or name; if absent, agree before creating it | Metadata-declared typed stored value |
| information_code | Additional Information code uniqueness | Conditional | An Additional Information code is supplied or copied | Lookup | Current Worker Union and resolved context data | validate_worker_union_information_code | Prevents reuse of a code already assigned to another Worker Union | Provide one proposed code | Validated unique code |
| worker_union_delete_history | Complete Worker Union history | Conditional | delete-effective-split | Lookup | hcmDateEffectiveObjectHistory | resolve_worker_union_delete_history | Prevents logical-record deletion or unintended future-split removal | Provide retained EffectiveStartDate and inclusive deletion EffectiveEndDate | Confirmed retained start and deletion end |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Conditional Create | The supplied bargaining unit is absent and the user agrees to create it | Manage Common Lookups only; re-resolve before continuing |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UNION.DEPENDENCIES | decision | 6 | resolve_dependency | ready->UNION.DEFAULTS;not_required->UNION.DEFAULTS;needs_input->UNION.ERROR;unresolved->UNION.ERROR | UNION.VALUESET | stop | After all applicable reference lookups |
