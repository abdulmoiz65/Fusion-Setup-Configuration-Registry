# Absence Certification Defaulting Rules

These are captured Redwood request values, not asserted server-side defaults. After the user selects the certification type, select only its applicable create default candidates. Resolve every lookup-backed candidate through its documented target-environment LOV before committing it, preserve an explicit user value, and validate explicit lookup-backed values through the same resolver. Validate captured read-only Management and fixed flags against their current field contract; they do not introduce an undeclared LOV or new requester selection.

The [Redwood conditional rules](../references/redwood-workflow.md) determine
visibility before a captured profile is used. All Standard Defaults rows are
create-only candidates; never copy a create profile into maintenance. The
existing APPLY_DEFAULTS node must omit hidden groups, including nulls, and
return override_or_unknown for conflicting supplied choices requiring review.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveStartDate / RangeStartDate | Current system date in YYYY-MM-DD format | A create request omits both values | No; preserve a requester-supplied date | |
| ManagementTypeCode | UD | Documentation or entitlement/payment percentage captured scenario | No | |
| StatusCode | ACTIVE | Documentation or entitlement/payment percentage captured scenario | No | resolve_absence_certification_status |
| AbsenceRecordUpdateRuleCode | OTHER | Documentation or entitlement/payment percentage captured scenario | No | resolve_absence_record_update_rule |
| AutoCompleteFlag | N | Documentation or entitlement/payment percentage captured scenario | No | |
| AllowOnDemandFlag | N | Only the visible Managed by entitlement formula checkbox in Entitlement Create | No | |
| ConfirmOnDemandFlag | N | Only the visible Managed by entitlement formula checkbox in Entitlement Create | No | |
| CreateUpdateCode, DueDateUpdateCode, CompleteUpdateCode, ExpirationUpdateCode | NONE | Documentation or entitlement/payment percentage captured scenario, only each visible applicable create event group; omit Creation reevaluation, Due Date, and Expiration for Managed by entitlement formula | No | resolve_absence_certification_update_rule |
| CreateCalculationCode, DueDateCalculationCode, CompleteCalculationCode, ExpirationCalculationCode | NONE | Documentation or entitlement/payment percentage captured scenario, only each visible applicable create event group; omit Creation reevaluation, Due Date, and Expiration for Managed by entitlement formula | No | resolve_absence_certification_calculation_rule |
| CreateCalculationModeCode, DueDateCalculationModeCode, CompleteCalculationModeCode, ExpirationCalculationModeCode | NONE | Documentation or entitlement/payment percentage captured scenario, only each visible applicable create event group; omit Creation reevaluation, Due Date, and Expiration for Managed by entitlement formula | No | resolve_absence_certification_calculation_mode |
| CreateCalculationOverride, DueDateReferenceDateCode, DueDateUnits, DueDateUOMCode, DueDateCalculationOverride, ConfirmReasonValues, CompleteCalculationOverride, ExpirationReferenceDateRuleCode, ExpirationDuration, ExpirationUOMCode, ExpirationCalculationOverride, VoidReasonValues, EligibilityProfileId | null | Documentation or entitlement/payment percentage captured scenario, only each omitted visible applicable create field; exclude hidden managed-formula groups and fields required by Calculate date, Entry required, or Entitlement Update Rule Override | No | |
| DueDateRuleCode, ExpirationRuleCode | ORA_ANC_NO_DUE_DATE | Documentation or entitlement/payment percentage captured scenario, only visible applicable create date groups; omit both for Managed by entitlement formula | No | resolve_absence_certification_due_date_rule |
| ConfirmReasonRuleCode, VoidReasonRuleCode | ORA_ANC_NOT_APPLICABLE | Documentation or entitlement/payment percentage captured scenario, only omitted visible applicable create reason rules; preserve supplied Entry required and require its complete reason list | No | resolve_absence_certification_reason_rule |
| ClassificationCode | ORA_ANC_DOCUMENTATION | Documentation certification | No | resolve_absence_certification_classification |
| ClassificationCode | ORA_ANC_PAYMENT_PERCENT | Entitlement / payment percentage certification | No | resolve_absence_certification_classification |

## Date-Effective Operation Mapping

Treat `EffectiveStartDate` as a normalized business input. Never accept `effectiveOf` as free-form caller input. Refresh the registered `absenceCertifications` Data Loader template before using a mapping, and apply the derived value to every populated supported section that exposes `effectiveOf`. The template and final DAT METADATA may retain the physical `EffectiveStartDate` attribute, but its data-record value remains blank by default.

These mappings are candidates pending the [lifecycle preflight](../../references/absence-additional-lifecycle.md),
not support claims. The design node owns the target-application and adapter
capability and field gates before source preparation. Exact existing-row,
before/after, protection and reference-impact gates apply only when required
by the selected maintenance/destructive operation. Ordinary Create uses the
current declared create contract, required inputs, validated dependencies and
collision check; it does not require an existing new-record identity or a
deletion-impact resolver. Missing contracts leave
operation_capability_status=unverified and fail closed; a generic RangeMode,
ready registry, template column, waiver, or approval cannot establish support.

| Requested operation | RestAction | effectiveOf | Required input |
|---|---|---|---|
| Create | POST | RangeStartDate=<EffectiveStartDate> | Explicit EffectiveStartDate or RangeStartDate, or the current-system-date default when both are omitted; allow the physical attribute in METADATA but leave its data-record value blank by default |
| Update | PATCH | RangeMode=UPDATE;RangeStartDate=<OperationDate> | Exact current identity, explicit operation date separate from stored Effective Start Date, verified lifecycle capability/allowed-field/impact gates, and current-template confirmation; immutable fields remain blank |
| Correction | PATCH | RangeMode=CORRECTION;RangeStartDate=<StoredSelectedStartDate> | Exact selected row and its returned stored Start Date, current visible mutable fields, and current-template confirmation; no new date intake |
| End date | PATCH | RangeMode=END_DATE;RangeEndDate=<ChosenEndDate> | Exact current identity, supplied End Date or disclosed Redwood current-date candidate, confirmation of the final chosen date in core preview, and current-template confirmation |
| Delete Record | DELETE | RangeMode=DELETE_CHANGES;RangeStartDate=<SelectedStoredStartDate> | Exact configuration bound to the non-first History row; complete contiguous History, full before state, User-defined protection and physical-row adapter contract. One identity-only parent; preserve previous row and extend its end to the selected row end. No replacement date |
| ZAP | DELETE | RangeMode=ZAP | Exact current identity, explicit destructive intent, date-free current-contract confirmation and applicable protection/impact for source readiness; core obtains immutable approval after preview and before execution |

## Values That Must Not Be Defaulted

| Field or Value | Why It Must Not Be Defaulted | Required Action |
|---|---|---|
| Maintenance date | The UI distinguishes an Update date, stored Correct context, and chosen End Date | Require the explicit Update date. Correct reuses the selected stored Start Date; do not ask for a replacement. Preserve an End Date or disclose the current-date UI candidate and bind it to the final core preview. Whole-object ZAP accepts no range date; Delete Record uses the selected stored row start after configuration/History checks |
| EffectiveEndDate for create | The captured create omitted it from the effective context and does not prove a portable client default | Do not request or synthesize it; reject a supplied create end date because the reviewed Create form does not expose this input |
| effectiveOf | It is a derived Data Loader control, not a free-form business input | Derive it from the validated operation and its applicable date only after lifecycle capability gates pass; ZAP derives its date-free control. It never authorizes changing a stored immutable field |
| Physical EffectiveStartDate data-record value | The business date is represented through derived effectiveOf by default; template-header presence does not populate the value | Always leave it blank for Update. For other operations, leave it blank unless current task-, operation-, and section-specific evidence explicitly proves dual-population support |
| Name, ClassificationCode, LegislationCode, and TriggerCode in Update | The Update input contract rejects these immutable values, including unchanged values copied from a create template | Leave their data-record values blank; retain saved values and target Name outside the loader record as lookup context, with only the resolved identity and mutable changes prepared |
| Dual-population support | The registered template exposing both attributes does not prove Fusion accepts both populated simultaneously | Update always rejects a nonblank physical EffectiveStartDate. For other applicable operations, require equal normalized dates and explicit current operation-specific evidence before permitting both; a mismatch always blocks |
| TriggerCode | A new required Trigger is a requester-confirmed choice, not a default; saved maintenance context is retained | For Create, resolve Classification and the applicable live list and validate the supplied value. Suggest an omitted Create choice only when intent is clear, otherwise present options, and require explicit confirmation or selection. For View or unrelated maintenance, resolve the saved display meaning without collecting a new selection; Update never populates TriggerCode |
| DFF __FLEX_Context, including US | Flexfield contexts and active segments are deployment-specific, and legislation alone does not prove that DFF data is required | Omit the DFF section when no DFF values are requested. When DFF values are supplied, resolve the current context and allowed segments through refresh_absence_certifications_describe and resolve_absence_certification_dff_context. |
| A coded value absent from the selected certification-type profile | No source-backed candidate exists for the field in that profile | Leave it absent unless the requester supplies a value that its documented resolver validates. |
| Hidden managed-formula groups | Passage of Due Date, Expiration, and Creation entitlement reevaluation are absent from that confirmed Trigger branch | Omit the complete hidden groups, including null/default candidates; do not interpret a generic captured profile as visibility evidence |
| Calculated Reference Date, Duration, or Duration UOM | Calculate date is an explicit complete input group, not an inferred arithmetic default | Leave the group unresolved until its corresponding input validation passes; never fill missing members with null or copy another date group's choices |
| Required Confirmation Reasons or Voiding Reasons | Entry required has a conditional minimum-selection contract in ora_input_validation.md | Block empty or partial selections before defaulting; never substitute null, copy the other reason list, or silently choose a reason |
| Revised Payment Percentage | A visible entitlement reevaluation with Entitlement Update Rule Override requires an explicit input validated by the current registered constraints | Never infer a percentage or invent a range; leave the choice unresolved until the owning input validation passes |

## Optional LOV Defaults

The captured null defaults for EligibilityProfileId, DueDateReferenceDateCode, ExpirationReferenceDateRuleCode, DueDateUOMCode, ExpirationUOMCode, ConfirmReasonValues, and VoidReasonValues apply only when omitted and otherwise applicable. Resolve supplied nonempty values through the additional resolvers in ora_reference_lookups.md before defaulting; never overwrite them with null. Do not query an LOV for an omitted value or an explicit clear. Empty reason selections serialize to null; omitted selections remain omitted unless an applicable captured create default requires null.

Entry required is an exception to empty-list serialization: an empty selection
is an input blocker, not an eligible null default. Hidden groups are omitted
entirely. Conflicting supplied choices remain unresolved for clarification;
never clear or replace them silently to make the default profile pass.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ANC_CERT.APPLY_DEFAULTS | step | 50 | apply_default | defaults_applied->ANC_CERT.ENFORCE_DESIGN;override_or_unknown->ANC_CERT.STOP_EXECUTION | ANC_CERT.VALIDATE_LOOKUPS | stop | Commit only applicable omitted create defaults whose coded candidates were resolved by ANC_CERT.VALIDATE_LOOKUPS; preserve explicit values and omit inapplicable, hidden, or unprofiled fields; never fill incomplete calculated-date, required-reason, or entitlement-Override choices from generic defaults |
