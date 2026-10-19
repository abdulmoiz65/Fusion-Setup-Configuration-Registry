# Document Types Dependency Readiness

## Purpose

Defines the conditional parent and lookup-backed business references used by
Document Types. Dependencies are evaluated only when their operation or field
applies and are never created implicitly.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Document Type identity | Resolve the target for read, edit, delete, or child preference work, or confirm create availability |
| 2 | Delivery Preferences parent | Resolve one current parent before evaluating its preference child |
| 3 | Delivery Preferences country | Resolve a supplied country to one current CountryName and TerritoryCode pair |
| 4 | Delivery Preferences payroll statutory unit | Resolve a supplied PSU display name to one current OrganizationId |
| 5 | Delivery Preferences legal employer | For GENERAL hierarchy, resolve a supplied Legal Employer display name to one current OrganizationId |
| 6 | Hierarchy state | Resolve all current preferences and classify the applicable organization anchor and same-organization lower rows |
| 7 | Mutation route | Select Data Loader, no-op/update, or blocker before artifact construction |
| 8 | Child identity | For a Data Loader create, generate one deterministic collision-checked child source key without user input |
| 9 | Lookup-backed values | Confirm each supplied category or subcategory value is enabled and current |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| document_type_identity | Existing Document Type or create-availability evidence | Conditional | Read, edit, delete, Delivery Preferences request, or create duplicate check | Lookup | Document Types resource | find_document_types | Prevents an ambiguous parent, incorrect target, or duplicate create | Provide one exact Document Type selector | DocumentTypeId and current parent values |
| delivery_preferences_parent | Delivery Preferences parent | Conditional | Delivery Preferences are requested | Lookup | Resolved Document Type | find_document_types | A preference child must remain attached to one exact current parent | Provide one exact parent Document Type | DocumentTypeId and current delivery preference |
| delivery_preferences_country | Delivery Preferences country | Conditional | A Delivery Preferences mutation supplies a country | Lookup | HCM Countries LOV | find_country | Distinguishes the display value required by Country from the code required by LegislationCode | Provide one exact current country name or territory code | CountryName and TerritoryCode |
| delivery_preferences_psu | Delivery Preferences payroll statutory unit | Conditional | A PAYROLL Delivery Preferences mutation supplies a PSU | Lookup | Payroll Statutory Units LOV | find_payroll_statutory_unit | Prevents padded LOV display text from being treated as a numeric PsuId | Provide one exact PSU name, ignoring only surrounding whitespace | PsuId from OrganizationId and the canonical display name for evidence |
| delivery_preferences_legal_employer | Delivery Preferences legal employer | Conditional | A GENERAL Delivery Preferences mutation supplies a Legal Employer | Lookup | Legal Employers LOV | find_legal_employer | Resolves the hierarchy anchor and prevents a display name from being used as LempId | Provide one exact current Legal Employer name | LempId from OrganizationId and the canonical display name for evidence |
| delivery_preferences_hierarchy_state | Applicable organization anchor and same-organization lower rows | Conditional | A Department or Location Delivery Preference is requested or a prior attempt may have partially succeeded | Lookup | Complete bounded `documentDeliveryPreference` collection plus resolved organization | reconcile_delivery_preference_hierarchy | Determines whether Data Loader can safely author the required hierarchy | No technical user input; the skill resolves current state | Exact anchor count, lower-row count, current modes, and route classification |
| delivery_preferences_anchor_source_key | Unique child create identity | Conditional | A missing PSU or Legal Employer anchor is routed to Data Loader | Verify | Current child source-key namespace and deterministic project convention | reconcile_delivery_preference_hierarchy | Gives a genuinely new Data Loader child stable identity | Do not ask the user; generate a stable owner and unique ID scoped to document type, country, organization, and anchor level | SourceSystemOwner and SourceSystemId on the new Data Loader child only |
| lookup_backed_value | Category or category-scoped subcategory | Conditional | Create or edit supplies the corresponding reference | Verify | Existing enabled lookup configuration |  | Prevents an invalid or ineffective stored reference | Provide one exact enabled code or meaning | Confirmed stored lookup value |

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
| DOCT.DEPENDENCY | decision | 2 | resolve_dependency | ready->DOCT.READ;not_required->DOCT.READ;needs_input->DOCT.ERROR;unresolved->DOCT.ERROR | DOCT.VALIDATE | stop | After input validation and before task-local reference lookups |
