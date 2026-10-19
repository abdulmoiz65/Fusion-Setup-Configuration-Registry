# Input Validation

## Schema-Derived Field Rules

| Section | Validate | Rule |
|---|---|---|
| `individualCompensationPlans` | Parent plan row | Require the live template section. Resolve `Status`, `DefaultVisibility`, `PaymentStartDate`, and `RestrictPlanAccess` through their declared lookups. Resolve `AllowStartDateOverride` and `AllowEndDateOverride` from enabled `YES_NO`: default each to `N` (`No`) when omitted; otherwise require an enabled exact code. Fill each required paired meaning and validate supplied meanings. Resolve `PaymentEndDate` from enabled `CMP_END_DATE`: default to `ONGOING_OR_USER_CHOOSE_DATE` when omitted; otherwise require an enabled exact code. Fill `PaymentEndDateMeaning` and validate a supplied meaning. Validate `Plan`, all resolved values, and `RestAction` against the operation-specific contract. |
| `Option` | Option row | Require an existing parent-plan lineage in the prepared source. `DocumentType`, `GrantType`, `NonMonetaryUOMMeaning`, `RequiresAttachmentMeaning`, and `PlanAttributeId` are optional: omit them when absent and validate each only when supplied. Validate `Option` and `RestAction` against the operation-specific contract. |
| `AttributeElement` | Element row | Require option lineage and an `ElementName`. Resolve it through the declared read-only describe-first resolver, require an exact effective element identity and agreement with any supplied LDG, country, classification, or processing type, then fill `LegislativeDataGroupName`, a nonblank `LegislationCode` as Country, `ClassificationName` from `PrimaryClassificationName`, and `ProcessingTypeCode` from `ProcessingType`. Resolve `ProcessingTypeMeaning` from enabled common lookup `PROCESSING_TYPE` using that code. Validate `RestAction` against the selected operation. |
| `OptionEligibility` and `PlanEligibility` | Eligibility rows | Optional. Omit both sections when no eligibility profile is provided. For every supplied row, require its respective parent lineage and validate `EligibilityProfileId`, `Name`, and `RestAction` from the live contract; do not equate a profile name to its ID without live metadata that declares the mapping. |
| `PlanAccess` and `PlanPeriod` | Access and period rows | Require plan-to-access and access-to-period lineage. Validate `Action`/access-level fields and `PeriodStartDate`/`PeriodEndDate` against their live types. |

## General Rules

1. Permit only sections returned by the live `individualCompensationPlans`
   template and child-object metadata.
2. Validate every supplied `RestAction`; do not add a default action.
3. Treat mandatory status as operation guidance. Do not reject a source merely
   because it omits an attribute that the live metadata marks mandatory for a
   different operation.
4. Reject an unknown field, duplicate field target, malformed parent-child
   lineage, or a supplied value that violates the current type, length,
   precision, reference, or lookup contract.
5. Do not create missing plans, elements, eligibility profiles, document types,
   actions, periods, or access levels during validation.
6. Do not create an empty eligibility child row to represent an omitted
   eligibility profile. The absence of `OptionEligibility` and
   `PlanEligibility` rows is valid.
7. Do not add an empty Option value or invent a default for an omitted
   `DocumentType`, `GrantType`, `NonMonetaryUOMMeaning`,
   `RequiresAttachmentMeaning`, or `PlanAttributeId`.
8. Populate the mandatory paired meanings for defaulted date-override and
   payment-end-date values only from their declared lookup results.

## Task Nodes

| Rule ID | Action Type | Transitions | Prerequisites | Applies When |
|---|---|---|---|---|
| ICP.VALIDATE_INPUT | validate_input | valid -> ICP.CHECK_DEPENDENCIES; invalid -> ICP.HANDLE_ISSUE | ICP.READ_SCHEMA | After the registered object and current schema resolve. |
