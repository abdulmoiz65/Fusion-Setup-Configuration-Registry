# WorkDay Definitions Input Validation

## Source Basis

- Developer-provided Workday Definition Skeleton.
- Confluence page 22040252607, Work Day Definitions Technical Design Document for FSCR.
- Confluence page 22040252605, Work Day Definitions REST API Technical Design Document.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Definition identity | Name | Block | Provide a nonblank Name of no more than 80 characters | Create or update | |
| Calendar-day choice | ETSameAsCalendarFlag | Block | Select whether the workday starts at midnight | Create or update | |
| Non-midnight workday boundary | Day start time; IsOvertimeNextDayFlag | Block | Provide a clock time, such as 8:30 AM, and select Current day or Next day | ETSameAsCalendarFlag is false | |
| Midnight entry treatment | ShiftsSpanMidnightFlag | Block | Select whether entries cross midnight | ETSameAsCalendarFlag is true | |
| Midnight-crossing assignment | EarnedDayBreakRule | Block | Select Based on entry start, Based on entry end, or Split at midnight | ETSameAsCalendarFlag and ShiftsSpanMidnightFlag are true | |
| Overtime boundary choice | OTSameAsCalendarFlag | Block | Select whether the overtime day starts at midnight | ETSameAsCalendarFlag is true | |
| Non-midnight overtime boundary | Day start time; IsOvertimeNextDayFlag | Block | Provide a clock time, such as 8:30 AM, and select Current day or Next day | ETSameAsCalendarFlag is true and OTSameAsCalendarFlag is false | |
| Existing definition identity | Name or Description search text | Block | Search by Name or Description and select a returned definition | Update or delete | find_workday_definitions_by_text |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Update or delete target is identified by Name or Description | Search all result pages, use one exact Name match, or require requester selection from multiple matching or nearest options | Continue only after a definition is selected; then read that item to confirm IsProfileUsedFlag is false | find_workday_definitions_by_text |
| Update or delete is requested | Require one item read to confirm IsProfileUsedFlag is false | Continue only with the verified mutable item | verify_workday_definition_mutability |
| EarnedDayBreakRule is Based on entry start or Based on entry end | Accept an integer EarnedBreakThreshold from 0 through 240 minutes, or apply the documented default | Continue to defaulting | |
| EarnedDayBreakRule is Split at midnight | EarnedBreakThreshold is not applicable | Clear any supplied threshold before preview | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name is blank or exceeds 80 characters | Reject the request | Create or update | |
| Description exceeds 1000 characters | Reject the request | Description is supplied | |
| WorkDay Definitions search | Accept a Name or Description search text, read every page, and require requester selection unless exactly one Name equals the supplied Name | A requester searches or an update or delete target is not supplied by item key | find_workday_definitions_by_text |
| Day start time is absent or cannot be parsed as a clock time | Reject the request and ask for a clock time such as 8:30 AM | A non-midnight boundary applies | |
| Day start time is supplied | Derive the internal DayStartTime from the fixed date 1970-01-01, the supplied time, zero seconds and milliseconds, and UTC; do not display the resulting technical value | A non-midnight boundary applies | |
| Boolean attribute value in a data loader file | Accept only the lowercase literal true or false; reject all other spellings, capitalization, and formats | A data loader file is created for a WorkDay Definitions request | |
| EarnedDayBreakRule is supplied | Resolve only the documented UI static options: Based on entry start, Based on entry end, or Split at midnight | ETSameAsCalendarFlag and ShiftsSpanMidnightFlag are true | resolve_earned_day_break_rule |
| EarnedBreakThreshold is supplied | Accept only an integer from 0 through 240 minutes | EarnedDayBreakRule is ORA_HWM_START_DAY or ORA_HWM_STOP_DAY | |
| EarnedBreakThreshold is supplied for split-at-midnight | Clear the value; do not retain it for the configuration | EarnedDayBreakRule is ORA_HWM_SPLIT_START_TIME | |
| WorkDayDefinitionId is absent | Block the request until the selected item's ID is resolved and added internally to the DAT | Update or delete | verify_workday_definition_mutability |
| WorkDayDefinitionId is supplied | Reject it for create; for update or delete, accept only the ID resolved by the task's live lookup and add it internally to the DAT | Create, update, or delete | verify_workday_definition_mutability |
| Other read-only field is supplied | Reject IsProfileUsedFlag, DayBreakerRuleName, and EarnedDayBreakRuleName as create or update values | Create or update | |

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Generate the summary only from populated structured business values that passed validation, applicable lookup resolution, and defaulting or preservation | A Complete Summary is prepared | |
| User selections | Include every verified business value explicitly supplied by the user | Every Complete Summary | |
| Applied defaults | Include every default actually applied in a separate Defaults Applied section | Every Complete Summary | |
| Blank and metadata values | Omit blank, null, unused, metadata-only, read-only, and system-managed values, including the derived DayStartTime | Every Complete Summary | |
| Business-only display | Show business labels and verified business display values; translate IDs, codes, booleans, and internal statuses before rendering | Every Complete Summary | |
| Technical-value exclusion | Do not render identifiers, REST or payload vocabulary, paths, methods, columns, directives, resolver names, rule IDs, internal statuses, diagnostics, warnings, or technical notes | Every Complete Summary | |
| Populated child records | Add a child section only when it contains populated business values, using business labels only | A child record has values | |
| Summary readiness | Always generate the Complete Summary before handing off to the provider-owned approval process | A create, update, or delete request is ready for provider approval | |

## Complete Summary Output Format

```md
## Complete Summary
| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied
| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |
```

Do not render an empty Defaults Applied row or an empty child section. Keep technical values only in the internal validation and provider-execution context.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WDD.VALIDATE_INPUT | decision | 10 | validate_input | create_valid->WDD.RESOLVE_CREATE_EARNED_RULE;update_valid->WDD.SEARCH_UPDATE_DEFINITION;delete_valid->WDD.SEARCH_DELETE_DEFINITION;missing_or_invalid->WDD.HANDLE_INPUT_ISSUE | none | stop | A WorkDay Definitions create, update, or delete request is prepared |
| WDD.COMPLETE_CREATE_SUMMARY | step | 40 | evaluate_result | summary_ready->WDD.PROVIDER_APPROVAL_READY_CREATE;summary_blocked->WDD.HANDLE_SUMMARY_ISSUE | WDD.ENFORCE_CREATE_DESIGN | stop | A create request has passed task-local gates |
| WDD.COMPLETE_CHANGE_SUMMARY | step | 41 | evaluate_result | summary_ready->WDD.PROVIDER_APPROVAL_READY_CHANGE;summary_blocked->WDD.HANDLE_SUMMARY_ISSUE | WDD.ENFORCE_CHANGE_DESIGN | stop | An update request has passed task-local gates |
| WDD.COMPLETE_DELETE_SUMMARY | step | 42 | evaluate_result | summary_ready->WDD.PROVIDER_APPROVAL_READY_DELETE;summary_blocked->WDD.HANDLE_SUMMARY_ISSUE | WDD.ENFORCE_DELETE_DESIGN | stop | A delete request has passed task-local gates |
