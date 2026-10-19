# Absence Types Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legislation | Resolve one territory code before resolving a legislative data group |
| 2 | Legislative Data Group | Resolve one LDG within the selected legislation and retain LegislativeDataGroupId as LegDataGroupId |
| 3 | Associated Absence Plan | When requested, require one exact active/effective plan resolved and verified by the Absence Plans task before mapping the plans child section |
| 4 | Type-plan association status | For every plans-child create or update, resolve the requested association status through the filtered ANC_SETUP_OBJ_STATUS LOV; do not use parent plan or type status |
| 5 | Associated Absence Reason | When requested, require one exact reason resolved by the Absence Reasons task; if absent, complete and verify that task's separately approved creation before type preparation |
| 6 | Event-processing association | When requested, resolve one active ANC event condition and one event response through ORA_ANC_EVT_ABS_ACTIONS before the events child is prepared |
| 7 | Pattern-specific event setup | For MAP only, resolve one event type from ANC_MAP_EVENT_TYPE before the create data is considered ready |
| 8 | Optional LOV controls | When supplied, resolve optional LOV/checkbox controls after their legislation, linkage-rule, restriction, action, and effective-date prerequisites are known |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| absence_legislation | Legislation | Yes | Every create request | Lookup | Supplied legislation or the documented US default | resolve_absence_legislation | The selected LDG and legislation must agree | Provide a territory code or name to override the default | LegislationCode: TerritoryCode |
| legislative_data_group | Legislative Data Group | Yes | Every create request | Lookup | Supplied LDG ID or exact LDG name within the resolved legislation | resolve_legislative_data_group | The create UI requires a legislative data group | Provide one LDG ID or exact name for the selected legislation | LegDataGroupId: LegislativeDataGroupId |
| associated_absence_plan | Associated Absence Plan | Conditional | A request names a plan to associate with the absence type | Verify | Verified Absence Plans handoff with ResolvedAbsencePlanId, plan name, legislation, LDG, active/effective dates, required template values, and successful load status when created; supplied association date or resolved type EffectiveStartDate | resolve_associated_absence_plan | The association must use one compatible active/effective plan and a supplied Priority; Fusion validates duplicate plan and priority conflicts during the Data Loader operation | Provide one exact plan name and priority; provide an association date only to override the resolved type effective start date | plans.AbsencePlanId: ResolvedAbsencePlanId; plans.AbsencePlanName: ResolvedAbsencePlanName; plans.Priority: RequestedPriority |
| type_plan_association_status | Type-Plan Association Status | Conditional | A plans child is created or updated | Lookup | Requested PlanStatusCode or PlanStatusMeaning; current plans child header | resolve_type_plan_association_status | The plans child requires its own eligible association status; it is not the parent plan or absence type status | Provide one association status code or meaning other than C or P | plans.PlanStatusCode: LookupCode; plans.PlanStatusMeaning: Meaning when present in the current header |
| associated_absence_reason | Associated Absence Reason | Conditional | A request names a reason to associate with the absence type | Verify | ResolvedAbsenceReasonId and ResolvedAbsenceReasonName returned by Absence Reasons; otherwise a reason name and explicit find-or-create intent | resolve_associated_absence_reason | The type association must not reference an unknown or duplicate reason | Provide one exact reason name, or let the Absence Reasons task create it after its own approval | reasons.AbsenceReasonId: ResolvedAbsenceReasonId; reasons.AbsenceReasonName: ResolvedAbsenceReasonName |
| absence_type_event | Absence Type Event | Conditional | A request attaches an event to an absence type | Lookup | Exact event condition name or ObjConditionCode; product code ANC | resolve_absence_type_event | The events child must use a current active Absence Management event condition, not a name-derived identifier | Provide one exact event condition | events.EventId: ObjConditionId |
| absence_type_event_response | Absence Type Event Response | Conditional | An absence type events child is created or updated | Lookup | Exact response code or meaning | resolve_absence_type_event_response | The event response must be from the Absence Type response LOV, not the Absence Plan accrual-response LOV | Provide one exact response | events.ProcessingTypeCode: LookupCode |
| map_event_type | MAP event type | Conditional | AbsencePatternCode is MAP | Lookup | Supplied event-type meaning, absence-type name, stated business intent, or MapEventTypeCode | resolve_map_event_type | MAP requires an event type selected from the current event-type LOV | The system recommends the uniquely intent-matched Meaning. Confirm it or ask to choose another available event type; do not request or display a code. | MapEventTypeCode: LookupCode internally; Meaning shown to the user |
| linkage_period_controls | Linkage period UOM and start rule | Conditional | LinkageRuleCode is D or ORA_ANC_CHAIN and either linkage-period control is supplied | Lookup | LinkageUOMCode and LinkageStartRuleCode | resolve_linkage_period_controls | The two controls are only meaningful for applicable linkage rules | Provide compatible linkage period UOM and start-rule values, or omit the linkage feature | LinkageUOMCode; LinkageStartRuleCode |
| legislative_grouping | Legislative grouping | Conditional | LegGroupCode is supplied | Lookup | LegGroupCode and resolved LegislationCode | resolve_legislative_grouping | Grouping values must be compatible with the selected legislation | Provide one grouping code or display value valid for the resolved legislation | LegGroupCode: LookupCode |
| edit_restriction_measures | Employee and manager edit measures | Conditional | EmployeeMeasures or ManagerMeasures is supplied | Lookup | Supplied measure and its matching restriction | resolve_edit_restriction_measure | A measure is valid only for a compatible restriction rule | Provide a compatible restriction and measure, or omit the measure | EmployeeMeasures; ManagerMeasures |
| eligibility_profile | Eligibility profile | Conditional | EligibilityProfileId or eligibility profile name is supplied | Lookup | Profile ID or exact Name | resolve_eligibility_profile | The stored attribute is an ID, not an inferred profile name | Provide one exact eligibility profile | EligibilityProfileId: EligyPrflId |
| hr_assignment_update | HR assignment update | Conditional | Any ActionId, ActionReasonId, or AssignmentStatusTypeId is supplied | Lookup | Action, action reason, assignment status, and EffectiveStartDate | resolve_hr_assignment_update_controls | Action reason is action-dependent and the action-update flow requires an assignment status | Provide an action and assignment status; add an action reason only after the action resolves | ActionId; AssignmentStatusTypeId; ActionReasonId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | One exact dependency identity and required output value are already present and validated | No lookup needed; continue validation |
| Lookup | A documented resolver can map supplied or defaulted business input to one authoritative value | Run the read-only lookup only |
| Blocked | A required identity is missing, ambiguous, or unresolved | No; stop and request the missing business value |
| Verify | A separately owned setup task has returned one exact identity or an accepted load still requires status verification | Read-only verification only; do not prepare the dependent type until success is confirmed |
| Authoring gap | A required lookup endpoint or output mapping is TBD | No; do not substitute an endpoint or infer a value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.RESOLVE_DEPENDENCIES | step | 20 | resolve_dependency | ready->AT.RESOLVE_REFERENCES;blocked->AT.HANDLE_ISSUE | AT.VALIDATE_INPUT | stop | After required input groups and pattern intent are classified |
