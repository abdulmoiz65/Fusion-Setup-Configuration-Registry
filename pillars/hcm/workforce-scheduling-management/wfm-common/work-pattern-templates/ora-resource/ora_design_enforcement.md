# Work Pattern Templates Design Enforcement

## Source Basis

- Work Pattern Templates Rest Describe, Confluence page 21510086973, version 3
- Work Pattern Templates Technical Design Document for FSCR, Confluence page 21509588886, version 9
- User-Facing Value Resolution Policy, attached text source, received 12 August 2026
- Work Pattern Page Screen Shots, developer-provided DOCX, received 13 August 2026
- Enterprise Shift timing behavior for Flexible days and Start and end times, developer-confirmed functional source, received 13 August 2026
- Enterprise Shift candidate-search and selection behavior, developer-confirmed functional source, received 13 August 2026
- New Shift UI screenshot showing break-duration validation, developer-provided, received 13 August 2026
- Failed Work Pattern Template load reporting an orphan Break child, developer-provided Fusion diagnostic, received 13 August 2026
- Work Pattern Shift unpaid-break total requirement, developer-confirmed functional source, received 13 August 2026
- Child-association evidence rule, developer-confirmed functional source, received 13 August 2026
- Successful Work Pattern Templates collection and exact-name REST request shapes, user-confirmed, received 14 August 2026
- Successful Work Pattern Templates create and update through Data Loader DAT, user-confirmed, received 14 August 2026
- Cumulative DayOfWorkPattern rule for multi-cycle templates, user-provided, received 17 August 2026
- Failed Work Pattern Template duplicate load reporting a non-whole-number WorkPatternShiftId, developer-provided Fusion diagnostic, received 14 August 2026
- ID-only Work Pattern Template deletion requirement, user-provided, received 17 August 2026
- Grouped business-facing Work Pattern Template approval preview requirement, user-provided, received 17 August 2026
- User-facing field-label, defaulting, and Template Name rules, user-provided, received 18 August 2026
- Successful Work Pattern Templates create DAT with parent, Shift, and Break loader correlations, user-provided, received 17 August 2026
- Generalized user-intent field-resolution rule, user-confirmed, received 17 August 2026
- Work Pattern Template reuse, Enterprise Shift selection, cycle-week coverage, and minute-precision rules, user-provided, received 18 August 2026
- Break-type eligibility by Shift Period Type, user-provided, received 18 August 2026
- Work Pattern Template Data Loader source-route and approval-fingerprint handling, user-provided, received 21 August 2026
- WFM-81615 Recommended Best Practices: unspecified break type default, Jira, reviewed 10 September 2026
- WFM-81615 Recommended Best Practices: complete shift-duration reconciliation, Jira, reviewed 10 September 2026
- WFM-81615 AC2: Work Pattern Template reuse, duplication, and unsuitable classification, Jira, reviewed 10 September 2026
- WFM-81615 AC7: incomplete or conflicting requirement clarification, Jira, reviewed 10 September 2026
- WFM-81615 Recommended Best Practices: Work Pattern Template naming, Jira, reviewed 10 September 2026
- Full task-rule review before generated-sample interpretation, user-provided, received 21 August 2026
- Flexible Shift Period Type selection boundary, user-provided, received 24 August 2026
- Shift Period Type disclosure in every user-facing review and approval preview, user-provided, received 24 August 2026
- Required terminal-summary format and verified-structured-fields-only generation, user-provided, received 25 August 2026
- Break Name defaulting from duration, Shift Period Type, and paid or unpaid status, developer-provided, received 18 September 2026
- Existing Work Pattern Template immutable-field rule, user-provided, received 1 October 2026

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Rule-set review gate | Before interpreting a generated sample, read this selected task's complete input validation, dependency readiness, reference lookup, defaulting, design enforcement, error handling, and compiled rule-registry guidance. Treat samples as schema evidence only; they do not override a task rule, documented default, dependency, lookup result, or error-handling requirement. |
| 2 | Scope gate | Keep the request within Work Pattern Templates template mode and exclude assignment-only work-pattern behavior |
| 3 | Aggregate gate | Validate the parent, local shifts, nested breaks, and applicable rules as one task-local aggregate |
| 4 | Lookup gate | Resolve every applicable lookup and require current active values before preview |
| 5 | Structural gate | Require cycle coverage, at least one working week, valid shifts and breaks, and unique assignment-rule pairs |
| 6 | Operation-safety gate | Do not infer undocumented concurrency, batch, delete-cascade, or component-private behavior |
| 7 | Classification gate | Classify every value intended for a user-facing response as business-facing or internal |
| 8 | Resolution gate | Resolve each internal value privately from the highest-priority reliable source available |
| 9 | Meaning gate | Evaluate conditions and recommendations using the verified business meaning |
| 10 | Presentation gate | Present only verified labels, business names, meanings, descriptions, user-facing field labels, and intentionally displayed business codes |
| 11 | Sanitization gate | Confirm that no unresolved value, internal identifier, implementation detail, or real identifier in a technical URL remains |
| 12 | Existing-template immutable-field gate | Before previewing an update, compare Shift Period Type, Cycles, and Unit of Measure with the verified current template. Block the update when any of those values would change. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A generated sample is available | Error |  | The sample is interpreted for a required field, default, identifier, activation setting, naming decision, dependency, lookup, behavior, or error response before all governing skill and task-rule files are read | First read the parent WFM Common SKILL.md, the selected Work Pattern Templates SKILL.md, complete input validation, dependency readiness, reference lookup, defaulting, design enforcement, error handling, compiled rule-registry, and required task-node execution guide. Use the sample only to confirm schema or field availability; resolve all business decisions from the governing rules and verified current state. Block preview and execution until this review is complete. | Yes |
| User-facing create intake is prepared | Error | resolve_work_shift_type | Work Pattern Code is requested or presented as required even though the create UI does not expose it | Collect only supported fields using their exact labels from the current Data Loader describe, REST metadata, or approved UI input source. Apply documented defaults without asking; do not request Work Pattern Code | Yes |
| A create artifact is prepared | Error |  | WorkPatternCode is sent as a user-created or name-derived value even though describe marks it system-generated and not updatable | Omit the code and let Fusion generate it | Yes |
| A new template aggregate is prepared through Data Loader | Error |  | The parent WorkPatternTemplateId correlation is missing, duplicated, treated as a persisted Fusion identifier, or is not reused in each new Shift row | Allocate one unique local parent correlation value, use it to associate the new template and its new Shifts, and keep it distinct from the Fusion-generated Work Pattern Code | Yes |
| A template create, update, or duplicate is prepared | Error |  | An explicit Template Name is supplied but not used; a supplied customer naming convention is not followed; or no explicit name or convention is supplied and a derivable recognizable WPT <Population or Purpose> <Shift behavior or Pattern> - <Cycle> result is not used | Preserve an explicit Template Name. Otherwise, follow the supplied customer naming convention. When neither is supplied, derive and use the naming-guideline result with useful available population or purpose, shift behavior, and cycle information. Ask for Template Name only when none of those sources is available. Do not ask for extra values or enforce a format when the guideline cannot be applied | Yes |
| A template create, update, or duplicate is prepared | Error |  | The Template Name contains an environment identifier such as DEV, TEST, UAT, or PROD | Remove the environment identifier before preview | Yes |
| An existing template is selected by name | Error | find_work_pattern_template_by_exact_name | The name does not resolve to exactly one case-sensitive match, or an internal identifier is requested from the user | Resolve the exact displayed name, retain the returned identifier privately, and use it for the selected-template detail read | Yes |
| An existing Work Pattern Template is updated | Error | find_work_pattern_template_by_id | One or more requested Shift Period Type, Cycles, or Unit of Measure values differs from the verified current template | Show only the requested immutable field labels: You can't change {requested immutable field labels} for an existing Work Pattern Template. Preserve the existing values and do not update the existing template's scheduling structure. | No |
| A Data Loader update artifact is prepared | Error | find_work_pattern_template_by_id | The source does not use the exact WorkPatternCode returned from the current template, or uses a code invented from TemplateName | Retrieve the current code explicitly and regenerate the immutable update artifact | Yes |
| A Data Loader deletion artifact is prepared | Error | find_work_pattern_template_by_id | The deletion row omits WorkPatternTemplateId or treats WorkPatternCode as a required deletion identity | Use WorkPatternTemplateId with RestAction=DELETE; do not require or send WorkPatternCode for deletion | Yes |
| A create, update, duplicate, or delete mutation is prepared | Error |  | The task is routed to a generic direct REST mutation operation or blocked because a spreadsheet runtime is unavailable | Use core Data Loader to prepare and validate a DAT source and immutable ZIP archive; direct REST mutation and spreadsheet generation are not required for this task | Yes |
| A validated Work Pattern Templates archive is ready for submission | Error |  | The generated ZIP is selected as the Data Loader source input instead of the validated DAT source | Submit the validated DAT source through core Data Loader. The loader must generate and validate the immutable ZIP internally before upload and initiation. | Yes |
| A DAT file or REST payload is prepared | Error |  | Any included, omitted, derived, or parent-association field is not verified against the current registered attributes or REST describe for the intended operation, including the source-backed new-template correlation layout | Correct only the field mapping or value at issue; do not infer it from UI nesting, an optional flag, a prior payload, or a generated sample | Yes |
| A Work Pattern Shift has unpaid Break rows | Error |  | UnpaidBreakDurationMinutes is absent or differs from the sum of the Shift's unpaid Break durations | Set the shift total to the summed unpaid Break duration before preview | Yes |
| A Break child is included | Error |  | The Break has no association to its intended Work Pattern Shift and would be submitted as an orphan child | Attach the Break to its intended Work Pattern Shift before preview; do not rely on template context alone | Yes |
| Any user-facing name, label, or descriptive field is prepared | Error |  | A value is decorated, differentiated, qualified, or transformed beyond the smallest business value directly supplied by the user or a documented default; or multiple materially different valid interpretations are silently selected | Preserve the supplied business value exactly when it is usable. Apply only documented defaults. Ask the user to choose when multiple valid interpretations materially change the configuration. Do not add dates, days, cycles, sequence numbers, qualifiers, or other traceability text unless explicitly requested or required by a documented default. | Yes |
| Any user-facing prompt, suggestion, validation message, preview, or result is prepared | Error |  | A requested or suggested field is not an exact field label from the current Data Loader describe, REST metadata, or approved UI input source; a documented default is requested from the user; or an unsupported alias is used as an input field | Use the exact supported field label. Apply documented defaults silently. When a required supported field has neither a value nor a valid default, ask only for that field label | Yes |
| A new Shift and child Breaks are prepared in one Data Loader artifact | Error |  | The new Shift correlation value is not a whole number or is not unique, or a new Break references a persisted or unrelated Shift identifier instead of its new parent correlation value | Allocate one unique whole-number Shift correlation value and use it consistently for that new Shift and its new Breaks | Yes |
| A Shift day is prepared in a Data Loader artifact | Error | resolve_days_of_week | DayOfWorkPattern is inferred, missing, or does not equal (cycle - 1) x 7 plus the verified Sunday-through-Saturday weekday index | Resolve the displayed cycle and day, then use the cumulative numeric value before preview | Yes |
| Any request enters the task | Error |  | The request uses assignment-only pages, person context, FTE, effective-date warnings, correct, end-date, history, export, background, or standalone batch behavior | Keep the request within the source-confirmed template create, view, update, duplicate, delete, shift/break, assignment-rule, or condition-rule paths | Yes |
| A template create, update, or duplicate is prepared | Error | resolve_work_shift_type | Shift Period Type, cycle coverage, at least one shift, or at least one working week is unresolved | Resolve Shift Period Type and correct the complete local aggregate before preview | Yes |
| A requirement is incomplete, incompatible, or conflicts with another requirement | Error |  | The request proceeds to preview, approval, creation, or duplication without disclosing an unresolved question, available verified business options, business impact, and recommended assumption | Stop and present those four business-facing clarification elements. Wait for the user or specialist to resolve the requirement; do not treat the recommended assumption as an approved default. | Yes |
| Flexible days or Flexible days and times is selected | Error | resolve_work_shift_type | The business requirement represents guaranteed scheduled work rather than availability | Use a non-flexible Shift Period Type for guaranteed scheduled work. Select Flexible days or Flexible days and times only when the requirement represents availability. | Yes |
| Final completion verification is enabled after Data Loader accepts an archive | Error | verify_final_template_load | Final success is reported before the load reaches a terminal successful status and the exact template read-back fully matches the approved configuration | Report final status, totals, and verified business details only after successful load and complete read-back verification. On failure, timeout, or mismatch, report the result and stop without retrying the submission | Yes |
| A template create, update, or duplicate is prepared | Error | resolve_repeat_cycle | The repeat unit or cycle count is unresolved or invalid | Resolve the repeat definition before preview | Yes |
| A possible existing template is considered | Error | find_work_pattern_template_by_id | The complete parent, cycle-week shifts, breaks, available Condition Builder association, and expected behavior were not compared to the request; a relevant template lacks a Suitable for reuse, Suitable for duplication, or Unsuitable classification with business rationale; a partial match is treated as reusable; or an existing template is modified in a way that changes behavior for other users | Compare every required business value and behavior, display the classification and rationale for each relevant template. Offer reuse only for a complete match. For any other result, create or duplicate as appropriate without changing the existing template's current behavior | Yes |
| A Workday Definition is selected | Error | resolve_work_day_definition | The selected definition does not fully match the requested configuration and behavior | Use an approved existing Workday Definition only when it is a complete match; otherwise leave the optional value unresolved or obtain a matching selection | Yes |
| Shift details are supplied for a flow that supports Enterprise Shifts, but no Enterprise Shift is selected | Error | find_enterprise_shift_candidates | Active Enterprise Shifts were not searched; exactly one complete match was not selected; multiple complete matches were not all presented for user selection; or local times are replaced by an Enterprise Shift when no complete match exists | Select exactly one complete match automatically. For multiple complete matches, present all and request a selection. For no complete match, preserve the supplied local times and continue without prompting for or creating an Enterprise Shift. Do not perform this lookup for a flow that does not support Enterprise Shifts | Yes |
| The user chooses to create a new Enterprise Shift from the candidate-selection prompt | Error |  | Work Pattern Templates continues before the separate Enterprise Shifts task creates and verifies the new active Shift | Hand off to Enterprise Shifts and resume this task only after the new active Shift is verified and selected | Yes |
| A selected library shift is used for a flow that supports Enterprise Shifts | Error | resolve_enterprise_shift | The shift is missing, ambiguous, inactive, does not fully match the requested configuration and behavior, or its configured timing cannot be verified | Use an approved existing Enterprise Shift only when it is a complete match; then use its verified Start Time, End Time, duration, and break values | Yes |
| A selected Enterprise Shift has a configured break duration | Error | resolve_enterprise_shift | No break rows are entered, or the combined entered break duration does not exactly match the Shift's configured break duration | Ask the user to add or adjust break details until the combined break duration exactly matches the Shift's break duration | Yes |
| A working shift is prepared for approval or creation | Error |  | Total Duration does not equal Work Duration plus paid-break duration plus unpaid-break duration, or a timed shift's elapsed Start Time to End Time differs from that total | Stop before approval or creation. Show the supplied Start Time, End Time, Work Duration, paid-break duration, unpaid-break duration, and Total Duration that conflict; ask the user to clarify or correct the business values, then revalidate. | Yes |
| Start and end times or Flexible days is used without an Enterprise Shift | Error |  | The applicable Start and End values are missing | Provide the applicable local time values, then revalidate the shift | Yes |
| Duration or Flexible days and times is used | Error |  | Duration is missing or nonpositive; Start, End, ShiftName, or an Enterprise Shift is requested or treated as required | Require only a positive Duration and the selected days. Do not request or require Start, End, ShiftName, or an Enterprise Shift | Yes |
| A cycle week has no shift details | Error |  | The week is silently treated as working or nonworking | Ask the user whether to mark the entire week nonworking. When shift details are supplied for a week, configure one or more shifts for that week | Yes |
| A working shift or Break is prepared | Error |  | User-provided minutes were rounded to an obsolete 15-minute increment or otherwise changed without a validation requirement | Preserve Start Time, End Time, work duration, and break values with one-minute precision; make only validation-required corrections | Yes |
| A Break is included for Duration or Flexible days and times | Error | resolve_break_type | Break Type is not Any time during shift or Start or End is requested | Use only Any time during shift. Require paid or unpaid status and duration; preserve a supplied Break Name or derive one from any available combination of duration, Shift Period Type, and paid or unpaid status without requesting missing naming components, and do not request Start or End | Yes |
| A Break is included for any other Shift Period Type | Error | resolve_break_type | The selected Break Type is not a verified available value, or its type-specific timing, duration, totals, range, or overlap rules fail | Permit every verified Break Type and correct the affected break before revalidating its parent shift | Yes |
| A Break is included without a Break Type | Error | resolve_break_type | Any time during shift was not applied, or the approval preview does not show it as Default | Apply the documented Break Type default before validation and display Break Type: Any time during shift — Default in the proposed configuration before approval | Yes |
| Assignment-rule mode is used | Error | resolve_assignment_rule_level_type | Selection Type is unresolved | Resolve the Selection Type before choosing its object | Yes |
| A non-enterprise assignment rule is used | Error | resolve_assignment_rule_object | The selected rule object is incomplete or duplicates an existing pair | Resolve the correct provider value and keep each pair unique | Yes |
| An enterprise assignment rule is used | Error | resolve_enterprise_for_rules | The enterprise is unresolved or duplicates an existing pair | Resolve the enterprise and keep each pair unique | Yes |
| Request attributes are prepared for import | Error |  | Audit, read-only, disallowed, wrong-type, over-length, over-precision, or unverified LOV values remain | Retain only attributes supported for the intended operation by current describe metadata | Yes |
| Upsert behavior is selected | Error |  | Upsert-Mode is omitted or natural-key matching is assumed without target-environment evidence | Require Upsert-Mode=true and treat matching semantics as an unresolved environment validation item | No |
| A custom action is considered for a batch | Error |  | findByAdvancedSearchQuery or deleteAllRules is included even though describe reports batchEnabled=false | Keep both custom actions outside ADF batch requests | Yes |
| Delete, deleteAllRules, or another destructive action is considered | Error |  | Dependency/cascade behavior and exact target approval are not confirmed | Stop until the exact destructive effect, target, rollback plan, and explicit approval are available | No |
| Update or delete relies on optimistic concurrency | Error |  | An ETag, If-Match, retry, or stale-response contract is inferred | Treat concurrency as unresolved and do not invent or automatically retry it | No |
| A component-private condition-builder call is required | Error |  | The publicWorkers base, HCM Rules delete URL, response schema, internal endpoint ID, or private query contract is inferred | Retain the unresolved contract and obtain source-backed details before treating it as executable | No |
| A user-facing approval preview is prepared | Error |  | The preview does not use the required field-by-field format; omits the verified Shift Period Type; identical Shift or Break business details are repeated one row per day; or DayOfWorkPattern is shown | Present Name, Status, Workday Definition, and verified Shift Period Type first. Then present one clearly labelled block for each week with Days, Shift, and Break fields. Show Repeats last. When a week has different shift or break details for different days, use separate day-group blocks within that week. Omit DayOfWorkPattern and internal values. | Yes |
| Any user-facing response | Error |  | A lookup value, enumeration, record key, REST key, internal object or attribute name, service alias, endpoint identifier, finder value, bind value, or other implementation-only value would be exposed | Resolve the value privately and present only its verified business label, name, meaning, or description | Yes |
| A user supplied an internal value | Error |  | Confirmation, explanation, or recommendation repeats the raw value | Accept the value only as private processing input, verify its business meaning, and use only that meaning in the response | Yes |
| Both an internal value and display label were supplied | Error |  | The pair was not verified as one selection, or a conflict message would disclose the internal value | Verify the pair; when inconsistent, report inconsistent selection information using business language only | Yes |
| An internal value cannot be resolved | Error |  | The response guesses a label, exposes the raw value, or recommends an action based on it | Mark the selection unresolved or incomplete and request the displayed label or relevant lookup information | No |
| A field or attribute is mentioned to the user | Error |  | An internal field name is used when a verified user-facing label exists | Use the verified label; otherwise describe the field by business purpose without exposing the internal name | Yes |
| A code is proposed for display | Error |  | The UI does not explicitly present it as a meaningful business field, or it is only a lookup, enumeration, database, or implementation identifier | Omit it unless UI evidence confirms an intentionally displayed business code under a user-facing label | Yes |
| A technical URL is shown | Error |  | The URL contains a real record or implementation identifier | Replace the value with a descriptive placeholder such as {RECORD_IDENTIFIER} | Yes |
| Final response construction | Error |  | A recommendation uses unresolved or implementation-only values, an internal code-to-label mapping is exposed, or the response requires implementation knowledge | Resolve first, reason second, and present only the business meaning | Yes |
| Final completion summary is prepared | Info | verify_final_template_load | The terminal summary is manually composed or does not use the documented field order | Generate the summary only from available verified structured completion fields and use Final Completion Summary Format in the documented order. Do not block, warn, add placeholders, or expose unverified values when a field is unavailable. | Yes |

## User-Facing Resolution Source Order

| Priority | Verified Source | Required Use |
|---|---|---|
| 1 | Display label supplied with the selected value | Use after confirming that it represents the selected value |
| 2 | Name, Meaning, DisplayName, Label, or Description attribute | Use the verified display attribute, not its internal key |
| 3 | Active list of values or selection provider | Resolve against the active selectable result |
| 4 | Configured value and display attributes | Use the configured display attribute after verifying the mapping |
| 5 | Verified lookup-service result | Resolve privately and retain only sanitized evidence for the response |
| 6 | Verified REST response display attribute | Use a documented display attribute from the selected record |
| 7 | Verified metadata definition | Use the documented user-facing label or meaning |
| 8 | Verified static value-to-label mapping | Use only a checked and current mapping |
| 9 | Checked-in application source | Use only when higher-priority sources are unavailable and the mapping is explicit |

Do not derive a label by removing prefixes, replacing underscores, changing
capitalization, expanding abbreviations, or comparing similar internal values.


## User-Facing Response Contract

| Response Section | Required Content |
|---|---|
| Selected option | Verified user-facing label only |
| Applicable information | Business-language details derived from verified meanings |
| Required information | User-facing field labels for missing mandatory values |
| Optional information | User-facing field labels for optional values |
| Unavailable or hidden information | Business-language explanation without implementation details |
| Validation | Business-language validation messages tied to the affected selection |
| Recommendation | Recommendation based only on resolved business meanings |
| Unresolved information | Explanation of what could not be resolved without exposing the raw value |
| Approval preview | Use the required field-by-field format in Approval Preview Format. Use business language only; omit internal day indexes and repeated day rows when configuration is identical. |

## Approval Preview Format

Present the final preview in this order. Do not use a wide summary table as the primary preview.

```text
Name: {Template Name}
Status: {Active or Inactive}
Workday Definition: {Verified Workday Definition}
Shift Period Type: {Verified Shift Period Type}

Week 1
Days: {Working days or day group}
Shift: {Start time–end time; work time when applicable}
Break: {Verified break name; duration, paid or unpaid status, and timing}

Week 2
Days: {Working days or day group}
Shift: {Start time–end time; work time when applicable}
Break: {Verified break name; duration, paid or unpaid status, and timing}

Week N
Days: {Working days or day group}
Shift: {Start time–end time; work time when applicable}
Break: {Verified break name; duration, paid or unpaid status, and timing}

Repeats: {Repeat cycle}
```

For different day groups within one week, retain the Week heading and repeat
only the Days, Shift, and Break fields for each distinct configuration.

## Final Verification

| Check | Required Result |
|---|---|
| Internal-value resolution | Every internal value is resolved before response construction |
| Business terminology | Every recommendation uses understandable business terminology |
| Identifier sanitization | No internal code, identifier, item key, service alias, or endpoint identifier appears |
| Field-label translation | No internal attribute name appears when a verified user-facing label exists |
| Business-facing code evidence | A code is shown only when the UI intentionally displays it as a business field |
| Unresolved-value safety | No unresolved value is guessed or exposed |
| Recommendation evidence | No recommendation depends on an unresolved value |
| Technical placeholders | Descriptive placeholders replace real record identifiers in technical examples |
| Understandability | The response is understandable without implementation knowledge |
| Final completion summary | Generated only from available verified structured completion fields and follows Final Completion Summary Format when fields are available |

## Final Completion Summary Format

Present the verified terminal summary in this order. Do not use a free-form or manually assembled substitute.

```text
Name: {Verified Template Name}
Status: {Verified Active or Inactive status}
Workday Definition: {Verified Workday Definition}
Shift Period Type: {Verified Shift Period Type}

Week 1
Days: {Verified working days or day groups}
Shift: {Verified start time–end time; work time when applicable}
Break: {Verified break name; duration, paid or unpaid status, and timing}

Week 2
Days: {Verified working days or day groups}
Shift: {Verified start time–end time; work time when applicable}
Break: {Verified break name; duration, paid or unpaid status, and timing}

Repeats: {Verified repeat cycle}
```

When one week contains distinct verified day groups, retain the Week heading and
repeat only Days, Shift, and Break for each group. If a field is absent
from the verified structured result, omit it without a warning, placeholder, or
unverified substitute.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_work_shift_type | Create, update, or duplicate | WorkShiftType and verified Shift Period Type meaning | ora_reference_lookups.md |
| find_work_pattern_template_by_exact_name | An existing template is selected by name | Internal selection key retained privately, verified Template Name, and current WorkPatternCode | ora_reference_lookups.md |
| find_work_pattern_template_by_id | A Data Loader update artifact is prepared | Current template identity and exact system-generated WorkPatternCode | ora_reference_lookups.md |
| resolve_repeat_cycle | Create, update, or duplicate | RepeatCycle and verified Unit of Measure meaning | ora_reference_lookups.md |
| resolve_work_day_definition | A Workday Definition is selected | WorkDayDefinitionId, verified Workday Definition name, earned-day timing values, and complete-match result | ora_reference_lookups.md |
| resolve_days_of_week | A Shift day is prepared | Verified displayed day and DayOfWorkPattern numeric value | ora_reference_lookups.md |
| find_enterprise_shift_candidates | Shift details are supplied without an Enterprise Shift selection in a flow that supports Enterprise Shifts | Ranked active Shift suggestions, complete-match indication, and pending user selection | ora_reference_lookups.md |
| verify_final_template_load | Wait for final completion is enabled after Data Loader accepts an archive | Terminal load status, totals, diagnostics when present, and complete exact-template verification result | ora_reference_lookups.md |
| resolve_enterprise_shift | A library shift is selected in a flow that supports Enterprise Shifts | ShiftId, verified Shift name, active status, times, durations, and complete-match result | ora_reference_lookups.md |
| resolve_break_type | A break is included | BreakTypeOption and verified Break Type meaning | ora_reference_lookups.md |
| resolve_assignment_rule_level_type | Assignment-rule mode is used | LevelTypeCode and verified Selection Type meaning | ora_reference_lookups.md |
| resolve_assignment_rule_object | A non-enterprise assignment rule is used | LevelObjectId and verified display meaning | ora_reference_lookups.md |
| resolve_enterprise_for_rules | Enterprise assignment rule is used | Enterprise identifier and verified name | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WPT.ENFORCE_TEMPLATE_DESIGN | decision | 50 | design_enforcement | passed->WPT.ENFORCE_USER_FACING_VALUES;blocked->WPT.HANDLE_ERROR | WPT.APPLY_DEFAULTS | stop | Before interpreting a generated sample for a business decision or treating any task result as preview-ready |
| WPT.ENFORCE_USER_FACING_VALUES | decision | 60 | design_enforcement | passed->WPT.WAIT_FOR_FINAL_COMPLETION;blocked->WPT.HANDLE_ERROR | WPT.ENFORCE_TEMPLATE_DESIGN | stop | Before automatic final-completion monitoring and any final user-facing setup response |
