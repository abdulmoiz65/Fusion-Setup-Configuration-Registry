# Benefit Reporting Groups Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request context | Requested operation, target environment, task identity, and record tree | Stop preflight for missing operation or target | Supply the missing context through the active project workflow | Every request | |
| HDL contract | Current selected-environment metadata for benefitReportingGroups and every supplied child section | Block derivation, artifact construction, and load | Obtain metadata through core.data-loader and confirm each section's keys, date-effectivity, effectiveOf availability, and supported operation | Every request that derives row controls or prepares an artifact | |
| Mutation controls | Validated immutable artifact and active Run Book | Block live submission | Follow core.data-loader preflight and approval workflow | Live mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Any optional reference field is absent | No lookup is required for that field; absence alone is not a validation error | Preserve the omitted field and continue | |
| Any optional reference field is supplied | Validate that field in its own child row against its named resolver | Record valid, invalid, ambiguous, or unverified_forbidden per row and field | |
| A supplied field's LOV returns 403 | Mark only that field unverified_forbidden; do not throw a field-validation error | Continue remaining independent checks; retain access issue for load readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent and child shape | Require an object for each reporting group and an array of objects for each supplied child collection; preserve row order and parent association | Each supplied record or collection | |
| Nested child shape | regulatoryPurposes must be an array of objects under its own regulatoryBodies row | regulatoryPurposes supplied | |
| Supplied reference scalar | Require a nonblank string; a supplied empty or null value is invalid rather than omitted | Any of the nine named reference fields supplied | |
| Date-effective child row | Require a valid EffectiveStartDate; default an omitted EffectiveEndDate to 4712/12/31 for create, update, and correction | A date-effective child row is supplied | |
| Derived effectiveOf date format | Parse each required row date using its documented source format; require every RangeStartDate or RangeEndDate in effectiveOf to be a valid YYYY-MM-DD date; reject invalid or ambiguous source dates | A date-effective child row is supplied | |
| Unsupported effectiveOf | Omit effectiveOf entirely when the current section metadata does not expose it; reject a supplied or generated effectiveOf on that section and stop if date-effectivity or field availability is ambiguous | Every included parent or child section | |
| Program or plan association | Require exactly one of ProgramName or PlanName in each reportingGroupForProgramsOrPlans row; reject a row containing both or neither | reportingGroupForProgramsOrPlans supplied | |
| CompensationObjectType | When supplied, require PLN for a PlanName row or PGM for a ProgramName row; reject a conflicting value | reportingGroupForProgramsOrPlans supplied | |
| Usage | Require an exact permitted lookup value; no match or multiple exact matches is invalid or ambiguous | benefitReportingGroups.Usage supplied | resolve_reporting_group_usage |
| RegulatoryBodyName | Require one exact Name match | regulatoryBodies.RegulatoryBodyName supplied | resolve_regulatory_body_name |
| RegulatoryPurpose | Require an exact permitted lookup value | regulatoryBodies.regulatoryPurposes.RegulatoryPurpose supplied | resolve_regulatory_purpose |
| RegulationName | Require one exact Name match | regulations.RegulationName supplied | resolve_regulation_name |
| RegulatoryPlanType | Require an exact permitted lookup value | regulations.RegulatoryPlanType supplied | resolve_regulatory_plan_type |
| ProgramName | Require one exact Name match | reportingGroupForProgramsOrPlans.ProgramName supplied | resolve_reporting_group_program |
| PlanName | Require one exact Name match | reportingGroupForProgramsOrPlans.PlanName supplied | resolve_reporting_group_plan |
| LanguageName | Require one exact Description match | translations.LanguageName supplied | resolve_translation_language |
| SourceLanguageName | Require one exact Description match | translations.SourceLanguageName supplied | resolve_source_language |
| Unsupported or malformed fields | Reject only when current selected-environment metadata establishes that the field or value is unsupported; do not silently discard child rows | Any supplied record | |

Do not coerce, trim, case-fold, or replace supplied reference values. An empty supplied value is provided and must be checked. Validate all rows, including repeated children. For a date-effective child, use that exact row's EffectiveStartDate for every date-effective validation and lookup; do not inherit a date from its parent or a sibling and do not fall back to the current date. An End date operation requires a supplied EffectiveEndDate. Report field path and row index for each result. Do not claim the unspecified parent identity, mandatory fields, keys, or HDL operation defaults are known until current metadata confirms them.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_RPTG.VALIDATE_INPUT | decision | 10 | validate_input | valid->BEN_RPTG.APPLY_DEFAULTS;invalid->BEN_RPTG.HANDLE_ISSUE | none | stop | Validate request context, supplied parent and child shape, and each included section's date-effectivity and effectiveOf availability before derivation |
| BEN_RPTG.EVALUATE | decision | 110 | evaluate_result | recorded->BEN_RPTG.RETURN_RESULT;invalid->BEN_RPTG.HANDLE_ISSUE | BEN_RPTG.ENFORCE_DESIGN | stop | Aggregate every supplied field result; retain unverified_forbidden without throwing |
