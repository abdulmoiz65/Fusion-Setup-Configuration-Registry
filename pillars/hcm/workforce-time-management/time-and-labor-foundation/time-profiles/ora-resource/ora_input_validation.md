# Time Profiles Input Validation

## Purpose

Defines source-backed input, conditional-field, and lifecycle validation for a
Worker Time Profile. It does not own lookup mechanics, defaults, design policy,
payload construction, DAT generation, or Data Loader execution.

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Use only populated business values that have completed input validation, applicable reference resolution, and defaulting or preservation | A Complete Summary is prepared |  |
| User selections | Include every verified business value explicitly supplied by the user | A supplied value remains populated after validation |  |
| Blank and metadata values | Omit blank, null, unused, read-only, and metadata-only values | Every Complete Summary |  |
| Business display value | Replace a stored identifier or code with its verified business display value or meaning; present a boolean as Selected or Not selected, Enabled or Disabled, or Yes or No | A verified business label is available |  |
| Summary display fidelity | For every configured field, display the exact verified Fusion business label and selected display value. Do not paraphrase, rename, combine, or substitute configured field labels or values. | A Complete Summary is prepared |  |
| Child records | Include a child section only when it contains populated verified business values; use business labels for the section and fields | A child record is populated |  |
| Summary readiness | Do not enter the provider-owned approval process until the Complete Summary is generated from verified structured values and every selected feature has its documented prerequisites resolved | A mutation is ready for provider approval |  |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create, save draft, submit, read, update, correct, duplicate, view history, or delete changes | Block | Provide one supported lifecycle operation | Every request |  |
| Plain-language requirement interpretation | Intended population, required Layout Set, required Time Card Period, and applicable optional processing configuration | Block configuration planning | Interpret the supplied Time and Labor requirement into these business requirements. Ask for clarification only for an interpretation that remains ambiguous or missing; do not invent a population, Layout Set, Time Card Period, or optional processing setting. | A Time Profile may be needed |  |
| Time Profiles availability | Enable Time Profile is effective as Enabled for the current user, or its exact site-level value is Y when the effective value is unavailable | Block | Verify ProfileOptionName ORA_HXT_ENABLE_TIME_PROFILE through the Time and Labor Common Manage Profile Options task. This task only checks the option; it does not change it. | Every request | verify_time_profile_feature_enabled |
| Data Loader mutation contract | dataloader_import_mode REST and businessObject timeProfiles | Block | Route the mutation through core.data-loader with both exact values | create, update, correct, duplicate, or delete changes |  |
| DAT pre-authoring evidence | Selected Time Profiles SKILL.md, every applicable ora_* rule, fresh current-state values, and fresh live timeProfiles Data Loader sample plus attribute-details workbook | Block | Review the task guidance and live Data Loader headers, keys, types, and formats before constructing any DAT row | Every Data Loader DAT creation | review_time_profiles_dataloader_metadata |
| Existing profile selector | ProfileName search text, verified TimeProfileId, or browse request | Block only when an operation requires one profile and multiple matches have no explicit selection | For update and every other existing-profile operation, search the documented collection through search_time_profiles. Compare the supplied name against every paginated Time Profile result using case-insensitive contains matching, regardless of capitalization; fetch the item when exactly one profile matches, and otherwise display all matches for selection. | read, update, correct, duplicate, view history, delete changes, or browse | search_time_profiles |
| Update impact review | Fresh current profile state and current group assignments | Informational; do not block an update when effective-dated history is unavailable | Display affected group assignments before the Complete Summary. | update or correct | read_worker_time_profile |
| Update history review | Effective-dated history when available | Informational; do not block an update when history is unavailable | Display effective-dated history before the Complete Summary. If history is unavailable, disclose that limitation and continue with the verified current state. | update or correct | read_time_profile_history |
| Create reuse decision | Complete derived requirement: name and description when supplied, effective date, and every applicable configuration value | Block approval and creation when a suitable candidate exists but the user has not chosen reuse or new creation | After an exact name search returns no match, read every Time-profile candidate at the applicable effective date. Compare derived name and description case-insensitively, and compare effective-date applicability and every applicable configuration value. Display suitable and unsuitable candidates with business reasons, then obtain the user's reuse-or-create decision. | create | find_similar_time_profiles_for_reuse |
| Create identity | ProfileName | Block | Provide a nonblank profile name | create or duplicate |  |
| Existing profileProperties identity, dates, and effective context | Freshly read SetupOptionValId, SetupProfileId, EffectiveStartDate, EffectiveEndDate, and effectiveOf | Block | Include SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, EffectiveEndDate, and effectiveOf as mandatory DAT columns; populate TimeProfileId with the same value as SetupProfileId, serialize both effective-date fields as YYYY-MM-DD, and serialize effectiveOf as RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD} | An existing profileProperties record is updated or corrected | read_worker_time_profile |
| Existing calendar-event update identity and dates | Freshly read SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate | Block | Include SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns, and serialize both effective-date fields as YYYY-MM-DD | An existing calendarEventPayrollElements record is updated or corrected | read_worker_time_profile |
| Existing-profile parent DAT action | Freshly reviewed parent-context mapping and PATCH action | Block | When a parent timeProfiles DAT context row is required for an existing profile, set RestAction to PATCH; never infer UPDATE merely because the profile already exists | Any DAT includes a timeProfiles parent context row for an existing profile | review_time_profiles_dataloader_metadata |
| DAT populated-field and section contract | Each emitted section has at least one data row, and every emitted field has a verified value | Block | Emit only fields with verified values and only sections with one or more populated rows; reject empty metadata-only sections and blank placeholder columns before validation or preview | Every Time Profiles DAT creation | review_time_profiles_dataloader_metadata |
| Time Card Period | Time Card Period search text or identifier | Block | Use the documented LOV search and select one returned period | create, duplicate, update, or correct | resolve_time_card_period |
| Layout Set | Layout Set search text or identifier | Block | Use the documented LOV search and select one returned layout | create, duplicate, update, or correct | resolve_time_card_layout_set |
| Selected feature completion | Every documented required or conditional value for each selected feature | Block | Resolve the feature's documented prerequisites through their owning resolvers; do not treat a display or control value as a complete selection | Any optional feature is selected |  |
| Consumer Set | Time Consumer Set compatible with the selected Time Card Period | Clear invalid value and block until corrected | Select a value returned for the selected period | Consumer Set is supplied | resolve_time_consumer_set |
| Calendar-event category | Calendar Event Category | Block the row | Resolve one exact category | A calendar-event row is included | resolve_calendar_event_category |
| Calendar-event payroll value | Payroll Element | Block the row | Resolve one exact composite payroll value, remove its leading LDG identifier from the selected Code only for PayrollTimeTypeCode, and map the LDG identifier separately to LDGId | A calendar-event row is included | resolve_payroll_time_type |
| Calendar-event row discriminator | AttributeCategory | Block the row | For a standalone Calendar Event Payroll child create, use the UI-evidenced AttributeCategory C_P_M; do not omit it or infer a different value | A new calendarEventPayrollElements row is created |  |
| Calendar-event eligibility selection | Include Ineligible Pattern Days | Block the row | Resolve one exact Yes or No lookup value | A calendar-event row is included and the current live Data Loader metadata exposes the field | resolve_yes_no_lookup |
| Calendar duration | Default Duration from 0 through 24 | Block the row | Supply a number in the inclusive range or omit it | Default Duration is supplied |  |
| Group assignment | Group Name and fixed AssignTo value GROUP; From Date is optional | Block the row | Resolve one group. Preserve a supplied YYYY-MM-DD From Date; when omitted, default it to the resolved Profile Start Date. To Date is optional | A group assignment is included | resolve_hcm_group |
| Permission window | Positive whole number | Block the field | Supply a positive integer or leave it blank | Any days-before or days-after permission value is supplied |  |
| Attestation edit window | Whole number or blank | Block the field | Supply a whole number or leave it blank | Allow Edits is selected for Worker Attestation |  |
| Geofencing mode | Validation Mode | Block | Select one documented mode | Enable Geofencing is selected | resolve_geofence_validation_mode |
| Geofencing radius | Radius in Meters from 50 through 1000 | Block | Supply an integer in the inclusive range | Geofencing is enabled and mode is not ORA_HXT_GF_VAL_MD_RECORD_ONLY |  |
| Web Clock access | Allow Edits to Times Generated from Web Clock and Allow Workers to Access Only on Mobile Devices | Accept selected or not selected | Record each supplied checkbox using its documented persisted representation; when both Time Collection Devices and Web Clock edit choices are supplied, require one consistent selection because they share one persisted setting | Web Clock is selected |  |
| Web Clock geofencing | Enable Geofencing, then Validation Mode and Radius in Meters when enabled | Block | Select geofencing, resolve one documented Validation Mode, and provide a radius from 50 through 1000 when required | Web Clock geofencing is selected | resolve_geofence_validation_mode |
| Web Clock location choices | Working from Home and Any Office Location | Accept selected or not selected | Record each supplied checkbox only when geofencing applies; clear both when it does not | Web Clock geofencing is enabled |  |
| Edit changes | At least one explicit supported field or child-row change | Block | State the intended change | update or correct |  |
| Duplicate identity | New ProfileName and Start Date | Block | Supply values for the new independent profile | duplicate |  |
| Delete Changes target | Verified history row, effective start date, parent link, and returned profileProperties child links | Block | Reopen History and select one eligible effective-dated change | delete changes | read_worker_time_profile |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing-profile name search has zero matches, multiple matches without a selection, or a loaded identity mismatch | Missing | Refine the name search, select one displayed matching profile, or provide a verified TimeProfileId, then load the selected item through read_worker_time_profile | find_time_profile_by_exact_name |
| A plain-language requirement does not yield an intended population, required Layout Set, required Time Card Period, or applicable optional processing configuration | Missing | Ask for clarification on only the unresolved business requirement; do not infer a value. |  |
| A create request has one or more suitable profiles and no reuse-or-create decision | Blocked | Show suitable and unsuitable candidates with their business comparison reasons, then ask whether to use an existing profile or create a new profile; do not proceed automatically. | find_similar_time_profiles_for_reuse |
| Enable Time Profile is not effective as Enabled for the current user and the exact site-level value is not verified as Y | Blocked | Stop before profile search, validation, preview, approval, or provider handoff. Ask the Time and Labor administrator to enable Enable Time Profile or verify its site-level value, then start a new session. | verify_time_profile_feature_enabled |
| Time Card Period is unresolved or ambiguous | Invalid | Select one current value | resolve_time_card_period |
| Layout Set is unresolved or ambiguous | Invalid | Select one current value | resolve_time_card_layout_set |
| Consumer Set is not returned for the selected Time Card Period | Invalid | Clear it and select a compatible Consumer Set | resolve_time_consumer_set |
| A selected feature has an unresolved documented prerequisite or lacks a supported persisted representation | Invalid | Request and resolve the missing feature selection; do not include the feature in the Complete Summary or proceed to approval |  |
| A referenced rule set, category, payroll value, device setup, attestation set, time attribute, or group is unresolved | Invalid | Review the resolver's available or closest choices and select one; do not reuse a sample identifier or infer the first result |  |
| Assignment validation returns any message | Invalid | Correct the duplicate, cross-profile, or overlapping-date assignment | validate_profile_assignments |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ProfileName length | Accept a nonblank string up to the describe-reported length of 255 | ProfileName is supplied |  |
| ProfileName business purpose | Require a meaningful business name that identifies the workforce population, policy, or time-entry purpose. Reject DEV, TEST, UAT, and PROD when used as standalone name tokens, case-insensitively; do not reject ordinary business words that merely contain those letters. | create, duplicate, or an update changes ProfileName | |
| Description length | Accept blank or a string up to the describe-reported precision of 1000 | Description is supplied |  |
| Effective-date fields | Require every populated EffectiveStartDate and EffectiveEndDate DAT value to be a valid YYYY-MM-DD date; reject slash-formatted, timestamp, or other non-ISO representations | Any Time Profiles DAT row includes either effective-date field | review_time_profiles_dataloader_metadata |
| Existing profileProperties DAT mapping | Include SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns; populate TimeProfileId with the same value as SetupProfileId, and serialize both effective-date fields as YYYY-MM-DD | An existing profileProperties record is updated or corrected | read_worker_time_profile |
| New profileProperties DAT mapping | Include TimeProfileId and SetupProfileId as mandatory DAT columns. Populate both with the same newly generated numeric parent local ID | A profileProperties row is created for a new or duplicated Time Profile | review_time_profiles_dataloader_metadata |
| New calendar-event DAT mapping | Include TimeProfileId as a mandatory DAT column. For a new or duplicated parent, populate it with the same newly generated numeric parent local ID; for an existing parent, populate it with the verified parent TimeProfileId | A calendarEventPayrollElements row is created | review_time_profiles_dataloader_metadata |
| New profile-assignment DAT mapping | Include TimeProfileId as a mandatory DAT column. For a new or duplicated parent, populate it with the same newly generated numeric parent local ID; for an existing parent, populate it with the verified parent TimeProfileId | A profileAssignments row is created | review_time_profiles_dataloader_metadata |
| Existing calendar-event DAT mapping | Include SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns and serialize both effective-date fields as YYYY-MM-DD | An existing calendarEventPayrollElements record is updated or corrected | read_worker_time_profile |
| Data Loader field and format contract | Before authoring a DAT, review the selected task guidance and fresh live Data Loader sample headers and attribute details; use only the applicable documented fields, composite or surrogate-key form, required dates, and effectiveOf representation returned by that review | Every Data Loader DAT creation; for a date-effective create use effectiveOf as RangeStartDate={YYYY-MM-DD}; for an update or PATCH of an existing date-effective object use RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD} | review_time_profiles_dataloader_metadata |
| Boolean source serialization | Serialize every populated Boolean attribute in the Data Loader source as the lowercase text literal `true` or `false`. Omit an unset Boolean attribute; do not substitute a default merely because it is omitted. Reject native JSON Boolean values and `True`, `False`, `TRUE`, `FALSE`, `Y`, `N`, or numeric equivalents. | Every Time Profiles Data Loader source | review_time_profiles_dataloader_metadata |
| Existing-profile parent action | When a parent timeProfiles context row is required for an existing profile, use RestAction PATCH; do not derive a parent UPDATE action from the lifecycle label or the fact that the profile exists | Every DAT with an existing-profile timeProfiles parent context row | review_time_profiles_dataloader_metadata |
| DAT sparse emission | Emit only verified populated writable fields in every METADATA and MERGE pair, and emit a section only when it has a populated MERGE row; reject blank-only columns and metadata-only sections | Every Time Profiles DAT creation | review_time_profiles_dataloader_metadata |
| Date-effective child context | Require effectiveOf for a date-effective child object. For create, serialize it as RangeStartDate={YYYY-MM-DD}; for update or PATCH, serialize it as RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD}. RangeMode is a component of effectiveOf, not a separate DAT column. Do not add effectiveOf to a non-date-effective object | A date-effective child DAT row is prepared | review_time_profiles_dataloader_metadata |
| Product area | Require TIME_PROFILE for this Worker Time Profile scope | create or duplicate |  |
| Status | Accept DRAFT for Save or Save and Close and SUBMIT for final Submit | A persistence outcome is selected |  |
| Priority for create or duplicate | Derive the value from a fresh Time Profile collection read immediately before DAT preparation: use the current highest Priority plus 1; use 1 only when no Time Profiles exist. Ignore a caller-supplied or source-profile priority for this lifecycle scope | create or duplicate | resolve_next_time_profile_priority |
| Priority reorder | Require a positive number | priority reorder |  |
| Calendar duration | Accept decimals from 0 through 24 inclusive | Default Duration is supplied |  |
| Permission action windows | Accept positive whole numbers only | A Worker, Line Manager, or Time and Labor Manager days-before or days-after value is supplied |  |
| Time Attribute slots | Preserve row order in TimeAttributeId1 through TimeAttributeId10; reject an eleventh persisted row | Time Collection Device attributes are included | resolve_time_attribute_field |
| Change Audit clearing | Clear EnableChangeAudit and MandatoryCaReason when Change Audit is disabled | Change Audit is disabled |  |
| Attestation conditional fields | Accept day limits only when Allow Edits is selected | Worker Attestation values are included |  |
| Geofencing clearing | Clear Validation Mode, Radius, Working from Home, and Any Office Location when geofencing is disabled | Enable Geofencing is not selected |  |
| Web Clock mobile access | Map Allow Workers to Access Only on Mobile Devices to DesktopGeofencingEnabledFlag; do not derive its stored value from the REST attribute name | Web Clock mobile access is supplied |  |
| Web Clock enablement | Map Enable Geofencing to WebClockGeofenceEnabledFlag and retain it as the parent control for the conditional geofencing fields | Web Clock geofencing is supplied |  |
| Shared Web Clock and device edit setting | Map Allow Edits to Times Generated from Web Clock and Allow Edits to Times Generated from Time Collection Device Events to AllowEditsToTimeEntriesFlag; reject conflicting selections because the current model exposes one persisted setting | Either or both selections are supplied |  |
| Record-only geofencing | Clear Radius and both location checkboxes | Validation Mode is ORA_HXT_GF_VAL_MD_RECORD_ONLY | resolve_geofence_validation_mode |
| Assignment dates | Preserve a supplied DateFrom or default an omitted DateFrom to the resolved Profile Start Date; require the resulting DateFrom and any supplied DateTo as ISO YYYY-MM-DD dates, reject slash-formatted or otherwise non-ISO values, and require DateTo not to precede DateFrom | A group assignment is included |  |
| Update versus correction | Use UPDATE when entered Start Date differs from the loaded Start Date; use CORRECTION when it matches or edit leaves it blank | update or correct | read_worker_time_profile |
| Composite payroll selection | For a calendar-event payroll selection, remove the leading LDG identifier and separator only from the value for PayrollTimeTypeCode, and populate LDGId separately from the verified composite selection. Retain the documented on-call mapping separately | An on-call or calendar payroll selection is included | resolve_payroll_time_type |
| Read-only attributes | Reject CreatedBy, CreationDate, LastUpdateDate, LastUpdateLogin, LastUpdatedBy, and derived display fields from authored writes | Any write input includes a read-only attribute |  |
| UI-only attribute | Do not persist EnableChangeAuditFlag under that name | Change Audit is included |  |
| Sample-only attributes | Do not treat Entered permission flags, sample IDs, codes, names, dates, or values as defaults | Source-pack example values are considered |  |
| Explicit selection precedence | Treat a supported value the user supplies in the context of a profile feature as an explicit selection; resolve a reference-backed business value through its documented resolver and retain the verified result | Any supported field is supplied |  |
| Child standalone requirements | Do not convert standalone child REST requirements into extra visible fields for nested parent create | A nested parent create is authored |  |
| Mutation provider | Accept only dataloader_import_mode REST and businessObject timeProfiles for task mutation handoff | create, update, correct, duplicate, or delete changes |  |

## Source Basis

- 01-functional-specification.md
- 02-ui-rest-field-mapping.md
- 03-authoring-guardrails.md
- 05-crud-lifecycle-behavior.md
- 06-rest-describe-evidence.md
- 07-ui-field-rest-service-matrix.md
- Developer-provided authoring directive: update identity lookup retrieves every Time-profile page and compares ProfileName with the supplied text using case-insensitive contains matching; show every match and require selection when more than one profile matches
- Developer-provided authoring directive: use core.data-loader with businessObject timeProfiles for CRUD mutations
- Developer-provided authoring directive: serialize every populated EffectiveStartDate and EffectiveEndDate as YYYY-MM-DD; reject every other representation before validation or preview
- Developer-provided authoring directive: every new calendarEventPayrollElements and profileAssignments child row includes TimeProfileId; use the same newly generated numeric parent local ID for a new or duplicated parent, or the verified parent TimeProfileId for an existing parent
- Developer-provided authoring directive: require a business-only Complete Summary after validation, lookup resolution, and defaulting, before provider-owned approval
- Developer-provided authoring directive: treat contextual supported user input as an explicit choice, resolve it when applicable, and do not replace it with a default
- Developer-provided authoring directive: serialize group assignment DateFrom and DateTo as ISO YYYY-MM-DD in the Data Loader source; reject non-ISO date strings before the provider preview
- Developer-provided authoring directive: when Group Assignment From Date is omitted, default it to the resolved Profile Start Date before validation and serialize it as YYYY-MM-DD
- Developer-provided authoring directive: before creating every Time Profiles DAT, review the selected task guidance and fresh live Data Loader metadata/sample headers and attribute details; use the reviewed field set, key form, and value formats without inference
- Developer-provided authoring directive: when an existing-profile DAT requires a timeProfiles parent context row, set RestAction to PATCH; never infer UPDATE from the profile's existence or lifecycle label
- Developer-provided authoring directive: emit only DAT fields with verified values and only sections with a populated MERGE row; reject blank placeholder columns and metadata-only sections before validation or preview
- Developer-provided authoring directive: for calendar-event payroll rows, strip any leading LDG identifier from a composite selected payroll Code only when populating PayrollTimeTypeCode, and retain that LDG identifier in the separate LDGId attribute
- Developer-provided authoring directive: for date-effective creates, use effectiveOf as RangeStartDate={YYYY-MM-DD}; for updates or PATCH operations, use effectiveOf as RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD}. RangeMode is part of effectiveOf, and SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, and EffectiveEndDate are mandatory for existing profileProperties updates; populate TimeProfileId with the same value as SetupProfileId
- Developer-provided authoring directive: SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate are mandatory DAT columns for calendarEventPayrollElements updates or corrections

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TP.INPUT | decision | 1 | validate_input | valid->TP.FEATURE_AVAILABILITY;missing->TP.ERROR;invalid->TP.ERROR;unsupported->TP.ERROR | none | stop | Every Time Profiles request; when a Time Profile may be needed, derive the intended population, required Layout Set, required Time Card Period, and applicable optional processing configuration from the plain-language requirement before continuing |
