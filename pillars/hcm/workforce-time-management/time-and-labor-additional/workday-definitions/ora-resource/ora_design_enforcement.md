# WorkDay Definitions Design Enforcement

## Source Basis

- Developer-provided Workday Definition Skeleton.
- Confluence pages 22040252607 and 22040252605.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce profile-use protection | Block update or delete if the current item reports IsProfileUsedFlag true. |
| 2 | Enforce conditional boundary design | Include only fields applicable to the selected calendar-day, midnight-crossing, and overtime branches. |
| 3 | Enforce writable-attribute boundary | Do not prepare read-only fields or WorkDayDefinitionId as create or update values. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Update or delete | Error | verify_workday_definition_mutability | IsProfileUsedFlag is true or cannot be verified | Select a different unused definition or stop the requested change | No |
| Entries cross midnight and assignment is Split at midnight | Error | | EarnedBreakThreshold remains populated | Clear the threshold because it is applicable only to start- or end-based assignment | Yes |
| Create | Error | | A request includes WorkDayDefinitionId | Remove the system-managed identifier from the proposed values | Yes |
| Update or delete | Error | verify_workday_definition_mutability | The internally resolved WorkDayDefinitionId is absent from the DAT | Add the exact verified ID to the DAT; do not request or display it to the user | Yes |
| Create or update | Error | | A request includes IsProfileUsedFlag, DayBreakerRuleName, or EarnedDayBreakRuleName as editable values | Remove read-only or system-managed fields from the proposed values | Yes |
| Create or update | Error | | A conditional boundary field is omitted or included outside its selected branch | Complete applicable fields and omit inapplicable ones before preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_workday_definition_mutability | Update or delete | WorkDayDefinitionId; Name; IsProfileUsedFlag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WDD.ENFORCE_CREATE_DESIGN | decision | 30 | design_enforcement | compliant->WDD.COMPLETE_CREATE_SUMMARY;blocked->WDD.HANDLE_DESIGN_ISSUE | WDD.CHECK_CREATE_DEPENDENCIES | stop | A WorkDay Definitions create request has valid inputs and dependencies |
| WDD.ENFORCE_CHANGE_DESIGN | decision | 31 | design_enforcement | compliant->WDD.COMPLETE_CHANGE_SUMMARY;blocked->WDD.HANDLE_DESIGN_ISSUE | WDD.CHECK_CHANGE_DEPENDENCIES | stop | A WorkDay Definitions update request has valid inputs, mutability verification, and dependencies |
| WDD.ENFORCE_DELETE_DESIGN | decision | 32 | design_enforcement | compliant->WDD.COMPLETE_DELETE_SUMMARY;blocked->WDD.HANDLE_DESIGN_ISSUE | WDD.VERIFY_DELETE_MUTABILITY | stop | A WorkDay Definitions delete request has passed mutability verification |
