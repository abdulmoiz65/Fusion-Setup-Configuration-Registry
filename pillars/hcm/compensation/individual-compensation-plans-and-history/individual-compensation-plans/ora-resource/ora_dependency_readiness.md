# Dependency Readiness

| Dependency | Applies When | Requirement | Outcome if Missing or Ambiguous |
|---|---|---|---|
| Registered object and current template | Every request | Exact registered `individualCompensationPlans` object, readable template, child metadata, and attributes. | Block before preview or import. |
| Plan status | Parent plan row | An enabled `CMP_PLAN_STATUS` lookup code. Use the one enabled code with meaning `Active` when `Status` is omitted; otherwise validate the supplied exact code. | Block for an unavailable/ambiguous Active default or invalid supplied code. |
| Default visibility | Parent plan row | An enabled `ORA_CMP_IC_PLANINFO_VISIBILITY` lookup code. Use the one enabled code with meaning `People see after clicking show plan info` when `DefaultVisibility` is omitted; otherwise validate the supplied exact code and any supplied meaning. | Block for an unavailable/ambiguous default, invalid code, or mismatched meaning. |
| Payment start date | Parent plan row | An enabled `CMP_START_DATE` lookup code. Use `APPRVL_DT_OR_USER_CHOOSE_DATE` when omitted; otherwise validate the supplied exact code. | Block for an unavailable/disabled default or invalid supplied code. |
| Plan access restriction | Parent plan row | An enabled `YES_NO` standard-lookup code. Use `N` (`No`) when `RestrictPlanAccess` is omitted; otherwise validate the supplied exact code. | Block for an unavailable/disabled default or invalid supplied code. |
| Parent-plan date settings | Parent plan row | Resolve `AllowStartDateOverride` and `AllowEndDateOverride` from enabled `YES_NO`, defaulting each to `N` (`No`), and fill their paired meanings. Resolve `PaymentEndDate` from enabled `CMP_END_DATE`, defaulting to `ONGOING_OR_USER_CHOOSE_DATE`, and fill `PaymentEndDateMeaning`. | Block for unavailable/disabled defaults, invalid codes, or mismatched meanings. |
| Optional Option values | `Option` row | `DocumentType`, `GrantType`, `NonMonetaryUOMMeaning`, `RequiresAttachmentMeaning`, and `PlanAttributeId` are optional. Validate each against its current schema contract only if supplied. | Do not block when omitted; block only a supplied value that violates its contract. |
| Eligibility profiles | `OptionEligibility` or `PlanEligibility` row supplied | Optional for plan creation. When supplied, each row must use its template-defined parent lineage and valid profile fields. | Do not block when no eligibility rows are supplied; block only a malformed supplied row. |
| Parent-child lineage | Any child row | Every Option, AttributeElement, eligibility, access, or period row links to a supplied valid parent in the template-defined hierarchy. | Block before preview or import. |
| Payroll element endpoint contract | AttributeElement row | Read payrollElementDefinitionsLOV describe metadata and require its declared single-value finder-expression contract before querying. | Block as a query-contract failure; do not use generic `q`, inferred query parameters, or separately serialized finder arguments. |
| Payroll element | AttributeElement row | One active effective exact payroll element for the supplied element name. Fill LDG and country from the returned LDG and nonblank LegislationCode, `ClassificationName` from `PrimaryClassificationName`, and `ProcessingTypeCode` from `ProcessingType`; any supplied values must agree. Unrelated returned rows are a query-contract failure. | Block for no/many exact matches, a mismatched returned identity, or a missing country value; do not infer country from LDG text. |
| Processing type meaning | Validated `AttributeElement` row | One enabled `PROCESSING_TYPE` lookup code matching the element's resolved `ProcessingType`. Fill `ProcessingTypeMeaning` from its exact lookup meaning. | Block for no/many, disabled, or mismatched lookup results. |
| Schema-declared references and lookups | A supplied field has a current reference or lookup contract | Resolve with the declared current metadata route; no guessed fallback. | Block as an unresolved dependency. |

## Task Nodes

| Rule ID | Action Type | Transitions | Prerequisites | Applies When |
|---|---|---|---|---|
| ICP.CHECK_DEPENDENCIES | resolve_dependency | ready -> ICP.ENFORCE_SCHEMA_GATE; blocked -> ICP.HANDLE_ISSUE | ICP.VALIDATE_INPUT | After supplied values pass field validation. |
