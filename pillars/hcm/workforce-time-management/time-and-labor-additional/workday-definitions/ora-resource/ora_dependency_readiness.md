# WorkDay Definitions Dependency Readiness

## Source Basis

- Developer-provided Workday Definition Skeleton.
- Confluence pages 22040252607 and 22040252605.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing-definition selection | For update or delete, search by Name or Description when an item key is not supplied, read every page, and require requester selection for multiple or nearest options. |
| 2 | Existing-definition mutability | For update or delete, retrieve the selected definition and verify that IsProfileUsedFlag is false. |
| 3 | Boundary applicability | Determine the calendar-day and midnight-crossing branches before validating their conditional fields. |
| 4 | Threshold applicability | Retain the grouping threshold only for start- or end-based earned-day assignment. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_definition_selection | Existing WorkDay Definition is selected | Yes | Update or delete | Lookup | Name or Description search result | find_workday_definitions_by_text | A selected definition is required before its profile-use state can be verified | Search by Name or Description; select from multiple or nearest options, or confirm a new definition is needed | WorkDayDefinitionId retained internally; Name; Description |
| existing_definition_mutability | Existing WorkDay Definition is mutable | Yes | Update or delete | Verify | Selected WorkDayDefinitionId and item GET response | verify_workday_definition_mutability | The UI disables edit and delete when the definition is used by a profile; the supplied skeleton prohibits update or delete in that state | Select an existing definition by Name or Description, or provide its item key | Name; WorkDayDefinitionId; IsProfileUsedFlag |
| workday_boundary_branch | Workday boundary branch | Yes | Create or update | Satisfied | Validated ETSameAsCalendarFlag, supplied day start time, internally derived DayStartTime, and conditional boundary values | | Determines the fields that are applicable to the selected configuration | Select whether the workday starts at midnight; for a non-midnight boundary, provide only the day start clock time | ETSameAsCalendarFlag; Day start time; IsOvertimeNextDayFlag |
| earned_day_assignment | Earned-day assignment | Conditional | Entries cross midnight | Satisfied | Validated ShiftsSpanMidnightFlag, EarnedDayBreakRule, and EarnedBreakThreshold | | Prevents a threshold from being retained when split-at-midnight applies | Select the assignment rule and provide a threshold only for start or end assignment | EarnedDayBreakRule; EarnedBreakThreshold |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Conditional fields are valid for the selected branch | No |
| Lookup | A search identifies or requires selection of an existing WorkDay Definition | Read-only lookup only |
| Verify | An update or delete must confirm that the existing definition is not profile-used | Read-only lookup only |
| Needs Input | A required conditional value is absent | No |
| Unresolved | Item identity or mutability cannot be verified | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WDD.CHECK_CREATE_DEPENDENCIES | step | 22 | resolve_dependency | ready->WDD.ENFORCE_CREATE_DESIGN;needs_input->WDD.HANDLE_INPUT_ISSUE;unresolved->WDD.HANDLE_LOOKUP_ISSUE | WDD.APPLY_CREATE_DEFAULTS | stop | A valid create request has completed defaulting |
| WDD.CHECK_CHANGE_DEPENDENCIES | step | 23 | resolve_dependency | ready->WDD.ENFORCE_CHANGE_DESIGN;needs_input->WDD.HANDLE_INPUT_ISSUE;unresolved->WDD.HANDLE_LOOKUP_ISSUE | WDD.APPLY_CHANGE_DEFAULTS | stop | A valid update request has completed defaulting |
