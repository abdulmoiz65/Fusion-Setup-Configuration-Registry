# Absence Types Defaulting Rules

Defaults in this file come only from [Absence Type Create - Defaults](https://confluence.oraclecorp.com/confluence/display/FUSIONANC/Absence+Type+Create+-+Defaults), except the developer-provided pattern-selection policy: infer only a suggestion from the name/description and require requester confirmation before applying it. Do not use the REST API Details page as a default source.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AbsencePatternCode | GENERIC | Create only, after the requester explicitly selects Generic pattern or confirms the Generic pattern suggestion and the live LOV resolves exactly once | No; never default from the name or description alone, ambiguous intent, silence, or a rejected suggestion | resolve_absence_pattern |
| ActionOnBPMTransactionExpiry | ORA_ANC_REJECT | The user omits the field | No | resolve_bpm_expiry_action |
| ApprovalRoutingCode | ORA_ANC_PRIMARY_MANAGER | The user omits the field | No | resolve_approval_routing |
| AttachmentTypeCode | ORA_ANC_ALL_TYPES | The user omits the field | No | resolve_attachment_type |
| DisplaySequence | null | The user omits the field | No; leave it unset or null and do not synthesize a sequence |  |
| EffectiveStartDate | Current system date in YYYY-MM-DD format, retained as create intent | The user omits EffectiveStartDate for a create | No; on the current contract do not emit the physical parent column. Change this only after a fresh live behavior test proves that the physical column controls creation; header presence or validation acceptance alone is insufficient. |  |
| DurationCalculationBasis | ORA_ANC_PUB_SCHED | The user omits the field | No | resolve_duration_calculation_basis |
| DurationUOMCode | H | The user omits the field | No | resolve_duration_uom |
| EmployeeAllowUpdatesFlag | true | The user omits the field | No |  |
| EmployeeRestrictions | ORA_ANC_NO_RESTRCT | The user omits the field | No | resolve_edit_restrictions |
| EvaluationExtentionPeriod | 30 | The user omits the field | No |  |
| EvaluationPeriod | 90 | The user omits the field | No |  |
| LegislationCode | US | The user omits the field | No | resolve_absence_legislation |
| ManagerRestrictions | ORA_ANC_NO_RESTRCT | The user omits the field | No | resolve_edit_restrictions |
| MaximumDuration | 4160 | The user omits the field | No |  |
| MaximumDurationCode | E | The user omits the field | No | resolve_duration_alert_rules |
| MinimumDurationCode | N | The user omits the field | No | resolve_duration_alert_rules |
| Status | P | The user omits the field | No | resolve_absence_type_status |
| TimeCardAvailableCode | ORA_ANC_EDIT | The user omits the field | No | resolve_time_card_availability |
| AgreementCode | ORA_ANC_NONE | AbsencePatternCode is GENERIC and the user omits the field | No |  |
| AgreementCode | null | AbsencePatternCode is II or MAP | No; leave the field absent |  |
| PartialDayCode | A | AbsencePatternCode is GENERIC or II and the user omits the field | No | resolve_partial_day_rule |
| PartialDayCode | N | AbsencePatternCode is MAP and the user omits the field | No | resolve_partial_day_rule |
| LinkageRuleCode | N | AbsencePatternCode is II and the user omits the field | No | resolve_linkage_rule |
| LinkageRuleCode | null | AbsencePatternCode is GENERIC or MAP | No; leave the field absent |  |
| MapEventTypeCode | null | AbsencePatternCode is GENERIC or II | No; leave the field absent |  |
| LinkageUOMCode, LinkageReasonCode, EligibilityProfileId, LinkageStartRuleCode, LegGroupCode, EmployeeMeasures, ManagerMeasures, ActionId, ActionReasonId, AssignmentStatusTypeId | null | The user omits the attribute | No; leave it absent and do not query or synthesize an LOV value |  |

Language is intentionally absent from the table because Fusion derives it from the authenticated login context. EffectiveEndDate is intentionally absent because Fusion derives it server-side unless the user specifically supplies a value. EffectiveStartDate is not sourced from Fusion; when absent, retain the current system date as create intent at validation time in YYYY-MM-DD format. Map that date to the validated parent `effectiveOf=RangeStartDate=<YYYY-MM-DD>` create control and omit the physical parent `EffectiveStartDate` column.

## Create Hierarchy Correlation Mapping

For a new type, set resolved-intent `hierarchyKeyStrategy` to `native-user-keys`. Omit root and child surrogate IDs. Bind direct children with `LegislationCode` plus `Name`; use unique `AbsenceRegionCode` for regions and unique `AbsenceUsageCode` for usages, with each usage carrying its owning `AbsenceRegionCode`. Verify these LOCAL/PARENT user-key alternatives against fresh registered metadata. Fusion allocates the IDs, so no client-generated-ID collision check or global collision endpoint is required. Include exactly one new type per archive. Retain all region and usage persona lookup/display/default fields from the fresh pattern. Omit standard rule rows and verify Fusion-generated rules after load; explicit rule creation is not supported by this key strategy. Existing-record operations continue to use exact returned IDs. Never automatically replay a create.

## Date-Effective Operation Mapping

Treat Effective Start Date as a normalized business input. For every selected
DAT section, inspect its refreshed header and emit `EffectiveStartDate` and/or
the operation-derived `effectiveOf` only when that exact header **and Fusion
validation** prove the field writable. Never accept `effectiveOf` as a
free-form input. A create retains the current system date when its business
effective start date is omitted and shows that date in the final summary; do
not default a date, range, deletion scope, or destructive choice for a
non-create operation.

| Requested operation | RestAction | effectiveOf | Required input |
|---|---|---|---|
| Create | POST | RangeStartDate=<EffectiveStartDate> | Exact requested or defaulted create Effective Start Date; emit it through parent `effectiveOf`, not the physical date column |
| Update | PATCH | RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate> | Exact current identity and explicit Effective Start Date; Legislation and Pattern remain unchanged |
| Correction | PATCH | RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate> | Exact current identity and explicit Effective Start Date |
| End date | PATCH | RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate> | Exact current identity and explicit Effective End Date |
| Delete changes | DELETE | RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate> | Exact current identity, explicit Effective Start Date, and explicit DELETE_CHANGES scope |
| ZAP | DELETE | RangeMode=ZAP | Exact current identity, explicit destructive intent, and immutable Data Loader approval |

After every terminal non-create result, run
`reconcile_absence_type_non_create_result` against the exact immutable archive
and pre-submit baseline. An UPDATE at date D is complete only when the new
slice starts on D and a post-submit exact-ID read at `effectiveDate=<D-1>` (or
a documented history route returning both slices) proves the predecessor ends
on D-1. Every requested value must match, and all unrequested root values plus
the complete independently paged child hierarchy must remain semantically
unchanged except for documented effective-date and audit fields. A correction
must change the selected slice without inventing a new slice. End date, Delete
Changes, ZAP, and child mutations must satisfy their operation-specific
expected presence, absence, and retained-history rules. Preserve the official
Data Loader status; map every intended mutation row and identity carrier to an
exact readback outcome; and map every returned diagnostic to an intended row
or owning top-level object without requiring one diagnostic per DAT row. When
the result reports no diagnostics, retain an explicit zero-diagnostic receipt
and counts. Record per-row and batch results with `noRetry=true`. Missing,
extra, partial, ambiguous, or incompletely paged state blocks the next archive
and never authorizes replay.

Apply this mapping independently to the exact target section. The current
registered section inventory is `absenceTypes`, `absenceTypeDDFs`,
`absenceTypeDFFs`, `absenceTypeRegions`, `absenceTypeRegionUsages`,
`absenceUsageRules`, `certifications`, `events`, `plans`, and `reasons`.
For a parent type end date, Delete Changes, or ZAP, prepare only the exact
`absenceTypes` parent operation. Do not synthesize a child lifecycle row merely
to carry date context or mirror the parent. A parent Delete Changes does not
cascade to independently dated Display Features usage slices. If the approved
intent also rolls back those child changes, reconcile the parent first and
then prepare a separate metadata-root child archive with exact usage `DELETE`
rows and `RangeMode=DELETE_CHANGES;RangeStartDate=<child slice start>`. A child
operation must retain its returned child identity and its independently
supported operation mapping. Never assume a parent operation cascades into
child rows or convert an unsupported child operation into a different one.
Refresh the registered template and stop if the target section lacks the
required operation controls. Create defaults
apply only to create; update, correction, end date, Delete Changes, and ZAP
preserve unspecified existing values and never receive create defaults.

For an existing Display Features usage update, emit a root metadata-only
marker (`METADATA|absenceTypes|RestAction`) with no parent MERGE. Follow it
with one identity-only `absenceTypeRegions` PATCH carrier per target region.
The carrier uses the exact returned `AbsenceTypeRegionId`, the parent user keys
`LegislationCode` and `Name`, and
`RangeMode=CORRECTION;RangeStartDate=<returned region EffectiveStartDate>`;
omit `AbsenceTypeId`. The target `absenceTypeRegionUsages` PATCH retains the
exact returned usage and region IDs, contains only requested persona
usage rows, carries the complete Administrator, Manager, and Employee
`UsageCode` tuple from current readback after applying requested edits, and
uses the requested operation-derived `effectiveOf`,
such as `RangeMode=UPDATE;RangeStartDate=<requested date>` for an update.

Resolve the region from the selected pattern and UI section before using those
returned IDs: Generic Additional
fields use `SUPPLEMENTAL_DETAILS`; Illness or Injury uses `SCHEDULING` only for
`SCHED_II_START_DATE` and `SUPPLEMENTAL_DETAILS` for its remaining Additional
fields; Maternity or Adoption Additional fields use `SUPPLEMENTAL_DETAILS`.
Never substitute `ADDITIONAL_DETAILS` because a usage code happens to match.
Never use a parent
MERGE, `AbsenceTypeId` on the region carrier, an `id,date` composite,
`SourceRef*` as hierarchy linkage, or physical `EffectiveStartDate`, lookup,
display, meaning, or unchanged business-value columns in this update shape.

Do not combine an `absenceTypes` parent MERGE with Display Features region or
usage rows in the same archive on the current registered contract. Live
parent-user-key, parent-ID, region-CORRECTION, region-UPDATE, and inherited-date
one-ZIP probes all returned child `Not Found` and committed no state. When both
scopes are requested, use a parent-only archive, reconcile it, refresh the
hierarchy, and then use the proven metadata-root child archive.

For Display Features, default an omitted legislation to `US` solely for the
two pattern resolvers `resolve_display_feature_pattern_template` and
`resolve_single_persona_display_features`. The selected pattern remains
required. Apply the master pattern template first, then overlay every returned
single-persona row's shared code and lookup type on Employee, Manager, and
Administrator, and finally apply the user's shared selection. Do not use this
US catalog as a default for another legislation.

If the live single-persona action remains unavailable after its one permitted
token refresh, apply the guarded US fallback for `GENERIC`, `II`, or `MAP`
without a separate readiness waiver. The locked 3/5/4 catalog supplies each
action-equivalent `EmployeeDefaultCode=DO_NOT_DISPLAY` and exact
`EmployeeLookupType`. The fresh exact live master template proves row placement
but must not supply or override those fallback fields. Require each catalog
default code to exist in the fresh live catalog-named lookup, then mirror the
validated code and lookup type to all three personas before the user's edit.
Record `singlePersonaSource: us-catalog-fallback`, the resolver failure, exact
catalog row, template-placement evidence, and matching live lookup row. All
fallback guards and the normal immutable Data Loader approval still apply.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.APPLY_DEFAULTS | step | 40 | apply_default | applied_or_not_needed->AT.NORMALIZE_DATE_EFFECTIVE_OPERATION;unresolved->AT.HANDLE_ISSUE | AT.RESOLVE_REFERENCES | stop | After required dependencies and applicable LOV values resolve |
