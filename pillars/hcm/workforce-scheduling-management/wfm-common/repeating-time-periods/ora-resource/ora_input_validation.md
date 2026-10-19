# Repeating Time Periods Input Validation

## Source Basis

- Repeating Time Period UI Skeleton, developer-provided text file, used only for UI fields, allowed choices, and conditional requirements.
- Repeating Time Period Skeleton, developer-provided text, used only for Period Usage-to-Period Type eligibility and combination behavior.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Basic period identity | Name; one or more Period Usage selections | Block the request | Provide a Name and select one or more Period Usage values: Time Card, Approval, Accrual Processing, Overtime, Balances, or Attendance Tracking | Create |  |
| Existing period identity | Current Name | Block the request | Provide the existing Repeating Time Period Name before supplying edits | Edit | verify_repeating_time_periods_fsm_export |
| Edit mutation | New Name and/or Description | Block the request | Provide at least one permitted edit; retain the exported PeriodCd and all fields other than Name and Description | Edit | verify_repeating_time_periods_fsm_export |
| Period definition | Period Type permitted by every selected Period Usage | Block the request | Select a Period Type from the values available for the selected Period Usage or usages | Create |  |
| Period Usage combination behavior | Intersection of permitted Period Type values, except when Overtime is selected with Time Card or Approval | Block the request | Use Monthly, Weekly for the exception; otherwise calculate the intersection and display it in canonical order Daily, Monthly, Semimonthly, Weekly | Create with more than one Period Usage |  |
| Daily multi-day definition | Period Length = More than one day; Number of Days; Sample Start Date | Block the request | Provide Number of Days and Sample Start Date | Create; Period Type is Daily and Period Length is More than one day |  |
| Daily one-day definition | Period Length = One day | Block the request | Select One day; do not collect additional period-definition fields | Create; Period Type is Daily and Period Length is One day |  |
| Monthly definition | Period Length = Calendar month; Sample Start Date | Block the request | Select Calendar month and provide Sample Start Date | Create; Period Type is Monthly |  |
| Semimonthly definition | Sample Start Date | Block the request | Provide Sample Start Date | Create; Period Type is Semimonthly |  |
| Weekly biweekly definition | Period Length = Biweekly; Sample Start Date | Block the request | Select Biweekly and provide Sample Start Date | Create; Period Type is Weekly and Period Length is Biweekly |  |
| Weekly extended definition | Period Length = More than two weeks; Number of Weeks greater than 2; Sample Start Date | Block the request | Provide Number of Weeks greater than 2 and Sample Start Date | Create; Period Type is Weekly and Period Length is More than two weeks |  |
| Weekly one-week definition | Period Length = One week; Sample Start Date | Block the request | Select One week and provide Sample Start Date | Create; Period Type is Weekly and Period Length is One week |  |
| Operation scope | Create or Edit; Delete is prohibited | Block the request | Select Create or Edit. Reject Delete because it is not a supported Repeating Time Periods operation. | Before preparing a task-specific change |  |
| Task-specific FSM contract | Field mappings; defaults; LOV behavior; every exported task-scoped CSV member; valid keys; relationships; and reconciliation selector | Keep the task incomplete | Support every task-scoped CSV member present in the fresh FSM export. | Before preparing any task-specific FSM change |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name is blank | Reject the request because Name is required | Create, or Edit when New Name is supplied |  |
| Derived create PeriodCd already exists in the fresh same-task export | Reject the request; duplicate PeriodCd values are not allowed | Create | verify_repeating_time_periods_fsm_export |
| Current Name is blank | Reject the request | Edit | verify_repeating_time_periods_fsm_export |
| Current Name matches zero or multiple rows in the fresh same-task export | Reject the edit request | Edit | verify_repeating_time_periods_fsm_export |
| Edit supplies neither New Name nor Description | Reject the request | Edit | verify_repeating_time_periods_fsm_export |
| Edit changes any parent or translation field other than Name or Description | Reject the request and restore the exported value | Edit | verify_repeating_time_periods_fsm_export |
| Edit changes PeriodCd or GroupingKey | Reject the request and retain the exact existing PeriodCd and GroupingKey | Edit | verify_repeating_time_periods_fsm_export |
| Period Usage is blank or outside the supported choices | Reject the request and require one or more of Time Card, Approval, Accrual Processing, Overtime, Balances, or Attendance Tracking | Create |  |
| Period Type is blank | Apply the documented Period Type default after Period Usage validation; reject only when no permitted Period Type outcome is available | Create |  |
| Period Type is not eligible for Time Card or Approval | Reject the request and require Monthly, Semimonthly, or Weekly | Create; Time Card or Approval is selected |  |
| Period Type is not eligible for Accrual Processing, Balances, or Attendance Tracking | Reject the request and require Daily, Monthly, Semimonthly, or Weekly | Create; Accrual Processing, Balances, or Attendance Tracking is selected |  |
| Period Type is not eligible for Overtime | Reject the request and require Daily or Weekly | Create; Overtime is selected |  |
| Time Card and Approval are selected | Populate Monthly, Semimonthly, Weekly | Create; only Time Card and Approval are selected |  |
| Time Card, Approval, and Accrual Processing are selected | Populate Monthly, Semimonthly, Weekly | Create; only Time Card, Approval, and Accrual Processing are selected |  |
| Time Card, Approval, Accrual Processing, and Overtime are selected | Populate Monthly, Weekly | Create; those four usages are selected |  |
| All Period Usage values are selected | Populate Monthly, Weekly | Create; Time Card, Approval, Accrual Processing, Overtime, Balances, and Attendance Tracking are selected |  |
| Accrual Processing and Overtime are selected | Populate Daily, Weekly | Create; only Accrual Processing and Overtime are selected |  |
| Approval, Accrual Processing, and Overtime are selected | Populate Monthly, Weekly | Create; only Approval, Accrual Processing, and Overtime are selected |  |
| Time Card and Overtime are selected | Populate Monthly, Weekly | Create; only Time Card and Overtime are selected |  |
| Overtime is selected with Time Card or Approval | Populate Monthly, Weekly, including when other Period Usage values are also selected | Create; any selected combination contains Overtime and at least one of Time Card or Approval |  |
| A non-exception Period Usage combination is selected | Populate the intersection of every selected usage's permitted Period Type values | Create; the combination does not contain Overtime with Time Card or Approval |  |
| A confirmed Period Usage combination is selected | Display its permitted Period Type values in this order: Daily, Monthly, Semimonthly, Weekly | Create; the combination has a documented UI outcome |  |
| Daily Period Length is invalid | Reject the request and require More than one day or One day | Create; Period Type is Daily |  |
| Daily multi-day fields are incomplete | Reject the request until Number of Days and Sample Start Date are provided | Create; Period Type is Daily and Period Length is More than one day |  |
| Additional daily fields are supplied | Do not require or populate Number of Days or Sample Start Date from this skeleton | Create; Period Type is Daily and Period Length is One day |  |
| Monthly Period Length differs from Calendar month | Reject the request | Create; Period Type is Monthly |  |
| Monthly Sample Start Date is missing | Reject the request | Create; Period Type is Monthly |  |
| Semimonthly Sample Start Date is missing | Reject the request | Create; Period Type is Semimonthly |  |
| Weekly Period Length is invalid | Reject the request and require Biweekly, More than two weeks, or One week | Create; Period Type is Weekly |  |
| Number of Weeks is missing or not greater than 2 | Reject the request | Create; Period Type is Weekly and Period Length is More than two weeks |  |
| Weekly Sample Start Date is missing | Reject the request | Create; Period Type is Weekly |  |
| Sample Start Date is supplied | Store it in the FSM CSV ReferenceDate field | Create FSM package |  |
| PeriodStartDate is supplied | Do not collect or retain it as a create input; populate the parent CSV PeriodStartDate field blank | Create FSM package for every Period Type |  |
| Start Day is supplied as independent input | Do not validate it as an independent user input; it is populated from Sample Start Date | Create; Period Type is Weekly |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| RTP.VALIDATE_INPUT | decision | 10 | validate_input | valid->RTP.APPLY_DEFAULTS;invalid->RTP.BLOCKED | none | stop | Validate a requested Repeating Time Periods configuration against the supplied UI skeleton |  |
