# Event Action Input Validation

Source: developer-provided EventAction-HDL.md, sections Primary Goal, HDL Attribute Metadata Output, Standard Instructions, and Field-Level Validations. Rules describe the supplied HDL examples; target-release metadata remains authoritative.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Action identity | EventActionCode or a target-supported alternative key | Block file preparation | Obtain the intended action code or supported key; target key precedence is TBD | Create or maintain an action | |
| Action definition | EventActionName, EventActionTypeCode, EffectiveStartDate | Block file preparation | Obtain values and compare the type with the five published codes | Create an action | |
| Submission | ActionSubmission | Block file preparation | Specify SYNC or MESS for the selected action type | Create an action | |
| Legislative context | LegislativeDataGroupName or LegislativeDataGroupId | Block until applicability is decided | Confirm whether the selected action requires an LDG; the HCM Rates example leaves it blank while the late-hire example supplies one | LDG-specific action | find_ldg_by_exact_name |
| Time-card lookback | LookbackTimeDefinitionCode | Block file preparation | Supply one documented month-start code | EventActionTypeCode is ORA_HWM_ACTION_TYPE_TC_RESUBMIT | |
| HCM Rates processing | FLEX:PAY_EVENT_ACTIONS_DDF, ProcessingType, InformationCategory | Block file preparation | Use the ORA_HCM_RATES_RECALC context and a target-supported processing value; InformationCategory target availability is TBD | EventActionTypeCode is ORA_HCM_RATES_RECALC | |
| Worker group criterion | HCMGroupCode, HCMGroupId, or target-supported SourceCode | Block criterion row | Supply one group identifier and settle SourceCode versus HCMGroupCode from target Attributes metadata | EventActionCriteria is requested | find_hcm_group_by_name_or_id |
| Event Group association | EventGroupCode or EventGroupId | Block association row | Supply one action-type Event Group; confirm EventGroupAction component availability | Association is requested | find_event_group_by_exact_code |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| LDG-specific action lacks a uniquely confirmed LDG | Blocked | Resolve exactly one target LDG before generating the DAT row | find_ldg_by_exact_name |
| Criteria requests a group without a uniquely confirmed group code or ID | Blocked | Resolve the HCM group and confirm accepted Criteria column in target metadata | find_hcm_group_by_name_or_id |
| Association references an unconfirmed group or withdrawn component | Blocked | Resolve the group and confirm target component availability | find_event_group_by_exact_code |
| Target release has not confirmed ProcessMode, AutoApprove, or InformationCategory where used | Blocked | Export current EventAction attributes and reconcile the chosen HDL pattern | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| EventActionTypeCode | Accept ORA_CREATE_RUN_REL_ACTIONS, ORA_ANC_ACTION_TYPE_RESUBMIT, ORA_HWM_ACTION_TYPE_TC_RESUBMIT, ORA_HCM_RATES_RECALC, or ORA_HRX_MX_SDI_UPDATE; any later code requires current target evidence | Type supplied | |
| ActionSubmission | Accept SYNC or MESS; require SYNC for the published time-card pattern; MESS is recommended rather than mandatory for HCM Rates | Create or maintain an action | |
| Effective dates | Parse YYYY/MM/DD and reject an end date earlier than the start date as a local consistency check | Dates supplied | |
| Time-card lookback | Accept 3_MONTHS_AGO_MONTH_START_DATE, 6_MONTHS_AGO_MONTH_START_DATE, or 12_MONTHS_AGO_MONTH_START_DATE | Time-card resubmission | |
| Time-card ProcessMode and AutoApprove | Public example uses AUTO or MANUAL and Y or N; block use until target confirms attributes remain loadable | Fields supplied | |
| HCM Rates processing | Public Full example uses ORA_FULL in ORA_HCM_RATES_RECALC DDF context; Fast and Periodic HDL codes are TBD | HCM Rates action | |
| Late-hire DDF switches | Public samples use Y or N for CreateFlow, HireDateLater, RunPayRelationshipGroup, AdditionalAssignments; confirm intended combination | Late-hire action | |
| Action and child identity | Child EventActionCode must equal the configured parent's code; EventActionTypeCode is not the action's identity | Criteria, translation, or association row | |
| Unresolved sample values | Reject literal angle-bracket placeholders and copied environment-specific IDs, LDGs, or group codes without target confirmation | DAT built from a sample | |
| Field lengths and universal mandatory flags | TBD: supplied headers do not establish data types, length limits, or all required attributes | Any load preparation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EA.VALIDATE_INPUT | step | 10 | validate_input | valid->EA.CHECK_DEPENDENCIES;invalid->EA.RETURN_ISSUES | none | stop | Any Event Action HDL request; evaluate Required Groups, Dependency-Aware Validation, and Field Validation |
