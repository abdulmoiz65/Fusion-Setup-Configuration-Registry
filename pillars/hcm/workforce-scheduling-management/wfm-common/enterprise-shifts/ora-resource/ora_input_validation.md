# Enterprise Shifts Input Validation

## Source Basis

- Enterprise Shifts Rest Describe, Confluence page 21451526148, version 3
- Enterprise Shifts Test Technical Design Document for FSCIR, Confluence page 21452837175, version 4
- Same-target Enterprise Shifts REST describe, collection read, and successful create response captured 10 August 2026
- Enterprise Shifts naming, category recommendation, time, reuse, and approval policy, developer-provided, received 18 August 2026
- Enterprise Shift name, field-value precedence, and default-origin display rules, user-provided, received 19 August 2026
- Boolean-field serialization policy, user-provided, received 10 September 2026
- Explicit Enterprise Shift Name policy, user-provided, received 24 September 2026

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity and schedule | Shift Name, or complete unambiguous naming information available from supplied values, current conversation, selected configuration, and configured defaults; WorkDurationMinutes | Block before preview only when name construction fails and Shift Name is absent, or Work Duration is absent or invalid | Attempt naming-guideline construction first. Preserve a supplied Shift Name. When construction fails, ask for Shift Name directly; do not request missing naming inputs. Resolve all other required values using the documented field-value precedence | Creating a shift | find_enterprise_shift_by_exact_name |
| Update identity | ShiftId or the exact item URL returned by Fusion | Block before preview | Resolve one existing shift and retain its returned identity | Updating a shift | find_enterprise_shift_by_id |
| Work duration | WorkDurationMinutes, or workHours and workMinutes that recombine to a positive integer minute value | Block before preview | Supply a nonzero duration that passes the active target validators | Creating or changing duration |  |
| Shift category | ShiftCategory lookup code, when supplied | Block the category-bearing candidate | Resolve one exact enabled LookupCode through Workforce Scheduling – Common – Manage Common Lookups for LookupType ORA_HTS_ENT_SHIFTS_CATEGORY; when omitted, provide a category-name recommendation from the shift time and description without defaulting a code | ShiftCategory is optional | resolve_shift_category_code |
| Time serialization | Target-supported HH:mm:ss+00:00 JSON string for StartTime and any EndTime | Block before preview | Round a supplied HH:MM:SS time to the nearest minute, then serialize it as a zero-padded 24-hour value with zero seconds and the target REST +00:00 lexical suffix | A time value will be sent |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| ShiftName is supplied or derived for create | Continue only after exact-name candidate discovery is complete | Reuse an exact existing shift or retain an explicit create-candidacy receipt | find_enterprise_shift_by_exact_name |
| ShiftId is supplied for update | Continue only with exactly one current shift | Use the returned item identity and compare requested values with the current record | find_enterprise_shift_by_id |
| ShiftCategory is supplied | Continue only with exactly one enabled code from ORA_HTS_ENT_SHIFTS_CATEGORY | Pass LookupCode, not Meaning | resolve_shift_category_code |
| ShiftCategory is omitted | Continue without a category code and present a category-name recommendation based on the shift time and description | Do not infer, default, or submit a category code without a supplied category selection |  |
| Time values are supplied | Continue only when each value matches HH:mm:ss+00:00 after nearest-minute rounding and preserves the rounded shift wall-clock time | Record the same-target evidence and reject values that would require an unconfirmed clock-time conversion |  |
| A mutation is requested | Continue only when the separate writable runbook, exact preview, and current approval are present | Hand off validated facts without constructing a write in this resource layer |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ShiftName | Attempt construction from all valid explicit, current-conversation, selected-configuration, and configured-default inputs. Accept an explicit nonblank Shift Name instead of a constructed name; reject a name longer than 240 characters. When construction fails and no explicit Shift Name is supplied, ask for Shift Name directly without requesting missing naming inputs | Creating or renaming |  |
| Shift name guidance | Apply naming guidance only when deriving a Shift Name. When the naming inputs are complete, derive a recognizable name using the supplied wording, start time, end time, and unpaid-break duration; include Population or Purpose when supplied, retain both in their supplied order when both are supplied, and include Shift Type only when it is not a regular working shift. Preserve an explicit user-provided Shift Name without applying this guidance. An explicit customer configuration naming convention takes precedence for derived names. Do not ask for Shift Name when construction succeeds. | Creating or renaming without an explicit Shift Name |  |
| Field-value precedence | Use an explicit user value first; then a still-applicable current-conversation or selected-configuration value; then an applicable configured default. Ask only for a required field that remains unresolved after those steps, and ask for all such missing required fields together | Any create or update input is validated |  |
| Optional or unsupported input | Do not request an optional field. Do not infer or submit an unsupported value for a missing required field | Any create or update input is validated |  |
| Environment identifiers in derived name | Do not derive a business configuration name containing DEV, TEST, UAT, or PROD. Preserve an explicit user-provided Shift Name without applying this check. | Creating or renaming without an explicit Shift Name |  |
| ShiftCode and ShiftCategory lengths | Reject supplied values longer than 30 characters | Either value is supplied |  |
| Required work duration | Reject missing, zero, negative, noninteger, or internally inconsistent work duration | Creating or changing duration |  |
| UI duration parts | Require workHours from 0 through 24 and workMinutes from 0 through 59 under the currently active relaxed UI branch; do not use the conflicting overlay maximum of 60 as authority | UI-shaped duration input is supplied |  |
| Break duration | Reject negative or noninteger BreakDurationMinutes. Accept zero only when the business requirement explicitly confirms that no unpaid break applies. | BreakDurationMinutes is supplied |  |
| Duration arithmetic | Reconcile all supplied time values before preview: End Time minus Start Time, using the declared same-day or next-day end day, must equal Work Duration plus Unpaid Break Duration. For an overnight shift, calculate elapsed time across midnight and explicitly validate the next-day end time. Reject a mismatch and identify the conflicting business values. | Start Time, End Time, Work Duration, and Unpaid Break Duration are supplied |  |
| Overnight end-day declaration | Require the request to identify whether the end time is on the same day or the next day | An end time is supplied; mandatory for overnight shifts |  |
| Active flag | Accept a JSON boolean only | ActiveFlag is supplied |  |
| Boolean field serialization | Send every Boolean field in Data Loader source as lowercase true or false. Do not send titlecase, uppercase, numeric, or synonym values. | A Boolean-valued field is emitted to Data Loader source |  |
| Offset and day values | Require integers; EndPlusDays is 0 or 1; require StartTime, EndTime, offsets, and next-day state to agree | Offset or end-day input is supplied |  |
| REST time lexical format | Require a zero-padded 24-hour value matching HH:mm:ss+00:00 after nearest-minute rounding; send zero seconds and do not change the rounded wall-clock minute | StartTime or EndTime is supplied |  |
| Time representation | Reject simultaneous time and offset representations until controlled target evidence proves their combined contract | Time and offset forms are both supplied |  |
| Read-only fields | Reject CreatedBy, CreationDate, LastUpdateDate, and LastUpdatedBy from create or update input | Any audit field is supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ES.VALIDATE_INPUT | step | 10 | validate_input | valid->ES.APPLY_DEFAULTS;invalid->ES.HANDLE_ERROR | none | stop | Before defaulting, lookup, design check, or mutation handoff |
