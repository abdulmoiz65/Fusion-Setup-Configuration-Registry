# WorkDay Definitions Reference Lookups

## Source Basis

- Confluence page 22040252605, live REST describe evidence dated 2026-09-22.
- Confluence page 22040252607, UI static-option, edit, and delete eligibility behavior.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_earned_day_break_rule | Entries cross midnight and an earned-day assignment is selected | Verified WorkDay Definitions UI static options: ORA_HWM_START_DAY, ORA_HWM_STOP_DAY, ORA_HWM_SPLIT_START_TIME | Map exactly one selected constant: ORA_HWM_START_DAY to Based on entry start; ORA_HWM_STOP_DAY to Based on entry end; ORA_HWM_SPLIT_START_TIME to Split at midnight | EarnedDayBreakRule and verified business display label | Stop when the supplied value is not one of the three static options; do not call Common Lookups or REST |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_workday_definitions_by_text | A requester searches for a WorkDay Definition, or an update or delete request needs a target selected by Name or Description | Name or Description search text; initial offset 0 | GET /hcmRestApi/resources/11.13.18.05/workDayDefinitions?fields=WorkDayDefinitionId,Name,Description,EarnedDayStartTime,EarnedDayBreakRuleName,EarnedDayBreakRule,IsEarnedNextDayFlag,EarnedBreakThreshold,DayStartTime,DayBreakerRuleName,DayBreakerRule,IsOvertimeNextDayFlag,IsProfileUsedFlag&orderBy=Name:asc&q=(Name like '%<search text>%' or Description like '%<search text>%')&limit=25&offset=<offset>. Start at offset 0 and increase offset by the returned-row count while hasMore is true. If no search result exists after every search page, repeat the request without q from offset 0 through every page to find and present the nearest Name or Description options | WorkDayDefinitionId; Name; Description; EarnedDayStartTime; EarnedDayBreakRuleName; EarnedDayBreakRule; IsEarnedNextDayFlag; EarnedBreakThreshold; DayStartTime; DayBreakerRuleName; DayBreakerRule; IsOvertimeNextDayFlag; IsProfileUsedFlag | Read every page. When exactly one returned Name equals the supplied Name, select it. When more than one result matches the supplied Name or Description, present all matching business options and require requester selection. When no search result exists, read all pages and present nearest Name or Description options, then require selection or confirmation to create a new definition | Selected WorkDayDefinitionId retained internally; selected Name and Description; business-facing matching or nearest options | Do not choose the first row. When multiple matching or nearest options exist, show all options and ask the requester to select one. When no acceptable option is selected, ask whether the requester wants to create a new definition. Stop when pagination cannot be completed or the response omits the requested fields |
| verify_workday_definition_mutability | Update or delete is requested | WorkDayDefinitionId | GET /hcmRestApi/resources/11.13.18.05/workDayDefinitions/{WorkDayDefinitionId}?fields=WorkDayDefinitionId,Name,IsProfileUsedFlag | WorkDayDefinitionId; Name; IsProfileUsedFlag | Require exactly one item response with the requested opaque item key and IsProfileUsedFlag false | WorkDayDefinitionId; Name; IsProfileUsedFlag | Stop when the item is absent, cannot be read, has a different identity, or IsProfileUsedFlag is true |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A WorkDay Definitions search is requested | Use limit 25 and offset 0, order by Name ascending, and read every page before classifying zero, one, or multiple results. |
| A search returns one exact Name match | Use that result as the selected target and retain its item key only for the following item verification. |
| A search returns multiple matching results | Present every matching business option and wait for requester selection; do not select the first row. |
| A search has no result after every page | Read every WorkDay Definitions page, present nearest Name or Description options, and ask the requester to select one or confirm creation of a new definition. |
| Update or delete is requested | Run verify_workday_definition_mutability before preview; do not rely on a stale table row or a name-only match. |
| The response reports IsProfileUsedFlag true | Block update and delete. |
| The item GET fails or returns an unexpected identity | Stop and request a valid existing definition item key; do not attempt a write. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WDD.SEARCH_UPDATE_DEFINITION | decision | 13 | reference_lookup | selected->WDD.VERIFY_MUTABILITY;selection_required->WDD.HANDLE_LOOKUP_ISSUE;unresolved->WDD.HANDLE_LOOKUP_ISSUE | WDD.VALIDATE_INPUT | stop | An update request needs a WorkDay Definition selected by Name or Description |
| WDD.SEARCH_DELETE_DEFINITION | decision | 14 | reference_lookup | selected->WDD.VERIFY_DELETE_MUTABILITY;selection_required->WDD.HANDLE_LOOKUP_ISSUE;unresolved->WDD.HANDLE_LOOKUP_ISSUE | WDD.VALIDATE_INPUT | stop | A delete request needs a WorkDay Definition selected by Name or Description |
| WDD.VERIFY_MUTABILITY | decision | 15 | reference_lookup | mutable->WDD.RESOLVE_CHANGE_EARNED_RULE;profile_used->WDD.HANDLE_MUTABILITY_BLOCKER;unresolved->WDD.HANDLE_LOOKUP_ISSUE | WDD.SEARCH_UPDATE_DEFINITION | stop | Update is requested |
| WDD.VERIFY_DELETE_MUTABILITY | decision | 16 | reference_lookup | mutable->WDD.ENFORCE_DELETE_DESIGN;profile_used->WDD.HANDLE_MUTABILITY_BLOCKER;unresolved->WDD.HANDLE_LOOKUP_ISSUE | WDD.SEARCH_DELETE_DEFINITION | stop | Delete is requested |
| WDD.RESOLVE_CREATE_EARNED_RULE | decision | 17 | evaluate_result | resolved->WDD.APPLY_CREATE_DEFAULTS;not_applicable->WDD.APPLY_CREATE_DEFAULTS;invalid->WDD.HANDLE_INPUT_ISSUE | WDD.VALIDATE_INPUT | stop | A create request uses the midnight-crossing assignment branch |
| WDD.RESOLVE_CHANGE_EARNED_RULE | decision | 18 | evaluate_result | resolved->WDD.APPLY_CHANGE_DEFAULTS;not_applicable->WDD.APPLY_CHANGE_DEFAULTS;invalid->WDD.HANDLE_INPUT_ISSUE | WDD.VERIFY_MUTABILITY | stop | An update request uses the midnight-crossing assignment branch |
