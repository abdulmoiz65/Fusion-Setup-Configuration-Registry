# Design Enforcement

1. Use `individualCompensationPlans` only as the Data Loader business object
   for this task.
2. Use current template and component metadata as the field authority; do not
   infer an alternate FSM layout or REST resource.
3. Allow only the parent and child sections declared in the live template.
4. Resolve the parent plan's `Status` from enabled `CMP_PLAN_STATUS`, using
   its one enabled `Active` meaning only when no value is supplied.
5. Resolve the parent plan's `DefaultVisibility` from enabled
   `ORA_CMP_IC_PLANINFO_VISIBILITY`, using its one enabled `People see after
   clicking show plan info` meaning only when no value is supplied.
6. Resolve the parent plan's `PaymentStartDate` from enabled `CMP_START_DATE`,
   using `APPRVL_DT_OR_USER_CHOOSE_DATE` only when no value is supplied.
7. Resolve the parent plan's `RestrictPlanAccess` from enabled standard lookup
   `YES_NO`, using `N` (`No`) only when no value is supplied.
8. Resolve `AllowStartDateOverride` and `AllowEndDateOverride` from enabled
   `YES_NO`, defaulting each to `N` (`No`), and fill their paired meanings.
   Resolve `PaymentEndDate` from enabled `CMP_END_DATE`, defaulting to
   `ONGOING_OR_USER_CHOOSE_DATE`, and fill `PaymentEndDateMeaning`.
9. Resolve the Element-derived LDG, `ClassificationName`, and
   `ProcessingTypeCode` only for supplied `AttributeElement` rows. Resolve
   `ProcessingTypeMeaning` through the enabled `PROCESSING_TYPE` common lookup
   using that exact code.
10. Treat `DocumentType`, `GrantType`, `NonMonetaryUOMMeaning`,
   `RequiresAttachmentMeaning`, and `PlanAttributeId` as optional Option
   values. Do not require or fabricate them when absent; validate them only
   when supplied.
11. Treat eligibility profiles as optional. Do not require
   `OptionEligibility` or `PlanEligibility` sections when no eligibility
   profile is supplied; validate the template-defined linkage and fields of
   every supplied eligibility row.
12. Route eligible data only to the separate approved `core.data-loader`
   workflow. Never create, update, delete, upload, or import through a lookup
   resolver.

## Task Nodes

| Rule ID | Action Type | Transitions | Prerequisites | Applies When |
|---|---|---|---|---|
| ICP.ENFORCE_SCHEMA_GATE | design_enforcement | eligible -> ICP.DONE_VALIDATED; blocked -> ICP.HANDLE_ISSUE | ICP.CHECK_DEPENDENCIES | After field and dependency validation. |
