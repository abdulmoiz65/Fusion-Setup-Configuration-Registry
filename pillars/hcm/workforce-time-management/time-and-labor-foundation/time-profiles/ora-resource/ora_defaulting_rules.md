# Time Profiles Defaulting Rules

## Purpose

Defines only source-verified create defaults, lifecycle values, clearing, and
preservation behavior for a Worker Time Profile. Sample payload values and
inactive commented defaults are never defaults.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ProductArea | TIME_PROFILE | Every Worker Time Profile create or duplicate | No |  |
| profileProperties.Type | TIME_PROFILE | Every Worker Time Profile create or duplicate | No |  |
| Start Date / effectiveOf | Current date in the target Fusion environment, represented for a date-effective create as RangeStartDate={current YYYY-MM-DD date} | Create does not supply Start Date; duplicate must still receive a valid new date through normal create validation. Do not add RangeMode for a create | No |  |
| Status | DRAFT | Save or Save and Close is selected | No |  |
| Status | SUBMIT | Submit is selected | No |  |
| Priority | The current highest Time Profile Priority plus 1; use 1 only when no Time Profiles exist | Every create or duplicate, after a fresh live Time Profile collection read and before the Complete Summary is generated | Yes; do not retain a caller-supplied or duplicated source priority | resolve_next_time_profile_priority |
| Worker create and edit permissions | Selected for Create and Edit Saved, Submitted, Rejected, and Approved | New profile uses the checked-in create-default object and the user has not changed the controls | No |  |
| Worker delete permissions | Selected for Saved; not selected for Submitted, Rejected, and Approved | New profile uses the checked-in create-default object and the user has not changed the controls | No |  |
| Line Manager create, edit, and delete permissions | Selected for Create and for Saved, Submitted, Rejected, and Approved edit/delete statuses | New profile uses the checked-in create-default object and the user has not changed the controls | No |  |
| Time and Labor Manager create, edit, and delete permissions | Selected for Create and for Saved, Submitted, Rejected, and Approved edit/delete statuses | New profile uses the checked-in create-default object and the user has not changed the controls | No |  |
| Permission days before and after | Blank | A new profile is initialized and the user did not provide either value | No |  |
| AssignTo | GROUP | A Group Assignment row is included | No |  |
| profileAssignments.DateFrom | Profile Start Date | A Group Assignment row is included and no From Date is supplied; use the new profile's resolved Start Date or the freshly read existing profile Start Date | No |  |

## Default Precedence

| Situation | Required Behavior | Outcome |
|---|---|---|
| The user explicitly supplies a supported value, including a business value expressed in the context of the selected profile feature | Treat it as the selected value; resolve it through the field's documented resolver when applicable and preserve the verified result | Do not apply or retain a conflicting default |
| The user does not supply a value and one documented default applies | Apply that default only after validation and dependency resolution | Record it as an applied default |
| The user does not supply a value and no documented default applies | Leave the value unset or preserve the freshly read existing value for an update or correction | Do not invent a value |
| A user supplies a business display value for a reference-backed field | Resolve the value through its owning documented resolver; the resolved value remains an explicit user selection | Do not classify the resolved result as a default |
| A caller supplies Priority for a create or duplicate | Ignore it and apply the latest allocated Priority from resolve_next_time_profile_priority | Do not preserve a caller-supplied or source-profile Priority for a new profile |
| A sample, example, blank, null, unresolved, or inapplicable value is encountered | Do not treat it as a user selection or a default | Stop for resolution or omit/clear it according to the applicable rule |

## Complete Summary Default Presentation

| Check | Required Behavior |
|---|---|
| Applied defaults | Include every default that was actually applied in the Defaults Applied section, using its business label and verified business display value |
| Priority allocation | Resolve and show the exact allocated Priority in the Complete Summary before presenting any approval or preview |
| User value precedence | Do not list a default when a verified user-provided value was retained instead |
| Unused defaults | Omit a documented default when its condition did not apply |
| Cleared values | Omit values that were cleared because they are blank, inapplicable, or unused |
| Display wording | Present a defaulted boolean as Selected or Not selected, Enabled or Disabled, or Yes or No rather than its stored representation |

## Clearing and Preservation Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| EnableChangeAudit and MandatoryCaReason | Change Audit is disabled | Clear both persisted values | cleared |
| GeofenceValidationMode, GeofenceRadius, GeofenceWorkFromHomeEnabledFlag, and GeofenceAllowedToWorkFromAnyLocationFlag | Geofencing is disabled | Clear all four values | cleared |
| WebClockGeofenceEnabledFlag, GeofenceValidationMode, GeofenceRadius, GeofenceWorkFromHomeEnabledFlag, and GeofenceAllowedToWorkFromAnyLocationFlag | Web Clock geofencing is disabled | Clear the parent control and all conditional geofencing values | cleared |
| GeofenceRadius and both geofencing location flags | Validation Mode is ORA_HXT_GF_VAL_MD_RECORD_ONLY | Clear the three inapplicable values | cleared |
| TimeAttributeId1 through TimeAttributeId10 | Fewer than ten ordered Time Attribute rows are supplied | Map rows sequentially and set unused slots to null | applied |
| MandatoryCaReason | Change Audit is enabled and the checkbox is supplied | Transform the boolean selection to Y or N | applied |
| Existing omitted edit value | Update or correction omits a field and no documented clearing rule applies | Preserve the freshly read current value | preserved |
| Existing profileProperties IDs and effective dates | An existing profileProperties record is updated or corrected | Include SetupOptionValId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns; retain the verified IDs, populate TimeProfileId with the same value as SetupProfileId, and serialize both effective-date values as YYYY-MM-DD | preserved |
| Existing calendar-event ID and effective dates | An existing calendarEventPayrollElements record is updated or corrected | Include SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns; serialize both effective-date values as YYYY-MM-DD | preserved |
| Date-effective effectiveOf | A date-effective child DAT row is prepared | For create, use RangeStartDate={YYYY-MM-DD}. For update or PATCH, use RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD}. RangeMode is a component of this value, not a separate DAT field | not_required |
| profileAssignments effective context | A profile assignment row is included | Do not add effectiveOf because profileAssignments does not declare that attribute | not_required |
| Sample identifiers, values, names, dates, codes, and Entered flags | Any source-pack example is considered for reuse | Apply no default | not_required |
| Geofencing validation mode and radius 100 | Commented-out source defaults are considered | Apply no default because the declarations are inactive | not_required |
| Layout Set, Consumer Set, Overtime Period, rule sets, device setup, audit mode, attestation, geofencing mode, and groups | No verified default is documented | Apply no default | not_required |

## Defaulting Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| applied | Exactly one documented default or clearing rule applies | Continue to design enforcement |
| preserved | A valid explicit or freshly read current value is retained | Continue to design enforcement |
| not_required | No documented default applies | Continue without changing the value |
| blocked | A required resolver failed or conflicting rules apply | Stop without applying a value |

## Source Basis

- 01-functional-specification.md
- 03-authoring-guardrails.md
- 04-example-create-payload.json as shape evidence only
- 05-crud-lifecycle-behavior.md
- Developer-provided authoring directive: remove advanced-search from Time Profiles
- Developer-provided authoring directive: retain verified IDs and serialize every populated EffectiveStartDate and EffectiveEndDate as YYYY-MM-DD; reject every other representation before validation or preview
- Developer-provided authoring directive: show every actually applied default in a separate business-only Defaults Applied section
- Developer-provided authoring directive: apply documented defaults only when the user is silent; preserve each valid explicit user choice after applicable resolution
- Developer-provided authoring directive: default an omitted Group Assignment From Date to the resolved Profile Start Date and serialize the applied date as YYYY-MM-DD
- User-approved Time Profiles priority allocation rule: before every create or duplicate, retrieve the latest Time Profile collection and use the next value after its highest Priority; do not use a caller-supplied or duplicated source priority

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TP.DEFAULTS | decision | 22 | apply_default | applied->TP.DESIGN;preserved->TP.DESIGN;not_required->TP.DESIGN;blocked->TP.ERROR | TP.DEPENDENCIES | stop | After validation and all applicable resolvers complete |
