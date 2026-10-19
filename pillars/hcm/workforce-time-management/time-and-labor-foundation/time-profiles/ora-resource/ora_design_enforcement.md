# Time Profiles Design Enforcement

## Purpose

Defines mandatory Worker Time Profile design and lifecycle gates before a
preview or provider-owned configuration change. It does not perform lookups,
construct payloads, or execute CRUD operations.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm feature availability, operation, identity, and update impact | Before any profile search or configuration activity, verify that Enable Time Profile is effective as Enabled for the current user. When the effective value is unavailable, accept the same option's exact site-level value Y through the Time and Labor Common Manage Profile Options task. Require TIME_PROFILE scope; for existing-record operations search profiles with bounded contains or LIKE matching, select one candidate, and load fresh state through the documented item route. For update or correction, display effective-dated history and current group assignments before the Complete Summary; disclose but do not block on unavailable history. |
| 2 | Interpret the business requirement and validate guided-process scope | When a Time Profile may be needed, derive the intended population, required Layout Set, required Time Card Period, and applicable optional processing configuration from the plain-language Time and Labor requirement. Treat Get Started selections as step visibility state, not persisted fields. |
| 3 | Resolve references | Resolve required and selected optional values from their documented value-source services |
| 4 | Apply conditional behavior | For every selected feature, validate or clear its documented conditional values and require its documented prerequisites before preview |
| 5 | Enforce date-effective child identity, ISO dates, and effective context | For an existing profileProperties update or correction, include SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns; populate TimeProfileId with the same value as SetupProfileId; for an existing calendarEventPayrollElements update or correction, include SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate as mandatory DAT columns; serialize every populated EffectiveStartDate and EffectiveEndDate as YYYY-MM-DD and include effectiveOf as RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD} |
| 6 | Validate assignments | Run Assignment Validation independently; never place non-batch-enabled custom actions in ADF batch |
| 7 | Enforce lifecycle semantics | Keep create, update, correction, duplicate, and Delete Changes distinct |
| 8 | Route the mutation provider | Send every CRUD mutation to core.data-loader using dataloader_import_mode REST and businessObject timeProfiles |
| 9 | Allocate priority and generate Complete Summary | For create or duplicate, resolve the next Priority from the latest live Time Profile collection before generating the Complete Summary. Always show the exact allocated Priority in that business-only summary before any preview or approval; include populated child sections only and show applied defaults separately |
| 10 | Review Data Loader contract | Before creating a DAT, review the selected task guidance and fresh live timeProfiles Data Loader sample headers and attribute details; retain the exact supported fields, keys, and formats |
| 10a | Enforce existing-profile parent action and sparse DAT emission | When an existing-profile parent context row is required, require RestAction PATCH; require every emitted DAT field to have a verified value and every emitted section to contain a populated row |
| 11 | Gate execution | Transition from the completed metadata preflight to the core.data-loader provider-owned approval gate; continue only when no blocker remains and the provider-generated DAT/ZIP preview is satisfied |
| 12 | Complete asynchronous processing | After the approved provider submission is accepted, use the task-authorized provider status flow and require terminal success plus documented persisted-state verification before final success |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocking |  | Requested scope is not Worker Time Profile of type Time | Use the Time profile type, represented by ProductArea TIME_PROFILE | Input fix |
| Create, duplicate, or ProfileName update | Blocking |  | ProfileName does not identify a workforce population, policy, or time-entry purpose; or it contains DEV, TEST, UAT, or PROD as a standalone token, regardless of capitalization | Use a meaningful business-purpose name and remove the environment token; do not reject ordinary business words that merely contain the same letters | Input fix |
| A Time Profile may be needed | Blocking |  | The plain-language Time and Labor requirement has not been interpreted into intended population, required Layout Set, required Time Card Period, and applicable optional processing configuration | Derive the business requirements before dependency resolution; ask for clarification only for unresolved requirements and do not invent values | Input fix |
| Every request | Blocking | verify_time_profile_feature_enabled | Enable Time Profile is unavailable, inactive, disabled, or neither effective as Enabled for the current user nor verified as Y at the exact site level when the effective value is unavailable | Stop and show: “Time Profiles can’t continue because Enable Time Profile isn’t enabled for your user or at the site level. Ask your Time and Labor administrator to enable it, then start a new session. This task doesn’t change profile options.” | No |
| Create with no exact ProfileName match | Blocking | find_similar_time_profiles_for_reuse | One or more candidates match the complete derived requirement, including description, effective-date applicability, and configuration, and the user has not selected reuse or new creation | Show suitable and unsuitable candidates with business comparison reasons and ask whether to use an existing profile or create a new profile; do not proceed automatically | No |
| Create or duplicate | Blocking | resolve_next_time_profile_priority | Priority was supplied by the caller or inherited from a source profile, the current highest Priority was not fetched immediately before DAT preparation, or the prepared value is not exactly the current highest Priority plus 1 | Derive Priority from the latest Time Profile collection; use 1 only when no Time Profiles exist, and regenerate the DAT after any later priority lookup | Automatic correction allowed |
| Existing profile operation | Blocking | find_time_profile_by_exact_name | The exact ProfileName query returns zero or multiple results, or the loaded TimeProfileId does not match the one collection result | Provide the exact Profile Name or a verified TimeProfileId, then resolve it through the documented collection and item routes; do not use LIKE, contains matching, or Advanced Search | Input or lookup fix |
| Every create flow | Blocking |  | Get Started options are authored as payload fields or the guided steps are described as independent browser routes | Keep Get Started as questionnaire/navigation state inside manage-time-profile | Input fix |
| Create, duplicate, update, or correct | Blocking | resolve_time_card_period | Time Card Period is unresolved | Select one exact period before Consumer Set resolution | Lookup fix |
| Create, duplicate, update, or correct | Blocking | resolve_time_card_layout_set | Layout Set is unresolved | Select one exact Layout Set | Lookup fix |
| Consumer Set is supplied | Blocking | resolve_time_consumer_set | The value is stale or incompatible with the selected Time Card Period | Clear and reselect from the period-filtered values | Lookup fix |
| A reference-backed field is supplied | Blocking |  | A sample ID, display label, inactive provider, design-time provider, or unresolved value is used as the stored value | Resolve the current tenant value through its owning resolver and persist the documented key or code | Lookup fix |
| Any optional feature is selected | Blocking |  | One or more documented required or conditional feature prerequisites are absent, unresolved, unsupported for persistence, or represented only by a display or control value | Request and resolve every documented prerequisite through its owning provider; include the feature in the Complete Summary only when its supported persisted values are verified | Input or lookup fix |
| Any supported field has an explicit user selection | Blocking |  | A documented default replaces, conflicts with, or is presented instead of the verified explicit selection | Resolve and preserve the user's selected value; apply a default only when the user did not provide a value | Automatic correction allowed |
| A calendar-event row is included | Blocking | resolve_calendar_event_category | Calendar Event Category is missing, unresolved, or duplicated contrary to row-add behavior | Correct the affected category | Input or lookup fix |
| A calendar-event row is included | Blocking | resolve_payroll_time_type | Payroll Element is missing or unresolved, its composite Code still includes the leading LDG identifier in PayrollTimeTypeCode, LDGId is absent or differs from the resolved selection, or duration is outside 0 through 24 | Normalize only PayrollTimeTypeCode, retain the separately resolved LDGId, and correct the duration when needed | Input or lookup fix |
| A new calendar-event row is created | Blocking |  | AttributeCategory is absent or differs from the UI-evidenced standalone child-create value C_P_M | Include AttributeCategory C_P_M in the child DAT row | Provider fix |
| A calendar-event row includes Include Ineligible Pattern Days in current live Data Loader metadata | Blocking | resolve_yes_no_lookup | Include Ineligible Pattern Days is missing or unresolved | Select a valid Yes or No value; omit the field when current live metadata does not expose it | Input or lookup fix |
| More than ten Time Attribute rows are supplied | Blocking | resolve_time_attribute_field | The ordered rows cannot fit TimeAttributeId1 through TimeAttributeId10 | Reduce the selection to ten or fewer and preserve order | Input fix |
| Change Audit is disabled | Blocking |  | EnableChangeAudit or MandatoryCaReason remains populated | Clear both values | Automatic clearing allowed |
| Worker Attestation Allow Edits is not selected | Blocking |  | Day-limit values are authored as active settings | Omit or clear inapplicable day-limit values | Input fix |
| Geofencing is enabled | Blocking | resolve_geofence_validation_mode | Validation Mode is absent; or non-record-only mode lacks radius 50 through 1000 | Select a valid mode and supply a valid radius when required | Input or lookup fix |
| Web Clock is selected | Blocking |  | Mobile-only access, Web Clock edit access, or the Web Clock geofencing parent control is represented by an undeclared field or a raw display value | Use the documented Web Clock persisted representations; do not derive behavior from an attribute name | Input fix |
| Web Clock geofencing is enabled | Blocking | resolve_geofence_validation_mode | Validation Mode is absent; a required radius is outside 50 through 1000; or the working-from-home or office-location choices are populated when they are not applicable | Resolve the mode, supply a valid radius when required, and clear inapplicable location choices | Input or lookup fix |
| Time Collection Device and Web Clock edit access are both selected | Blocking |  | The two selections conflict even though they share one persisted setting | Require one consistent selection before preview | Input fix |
| Geofencing is disabled or record-only mode is selected | Blocking | resolve_geofence_validation_mode | Inapplicable geofencing fields remain populated | Apply the documented clearing rules | Automatic clearing allowed |
| A Group Assignment is added or changed | Blocking | validate_profile_assignments | Group is not selected from the resolver's available or closest choices, or server validation returns any duplicate, other-profile, or same-date-range message | Select an eligible group, then correct every assignment message before completion | Input or lookup fix |
| An edit is requested | Blocking | read_worker_time_profile | Target was not loaded through the verified collection and item read path or returned ID does not match the collection result | Resolve the exact profile name and reread the returned item | Lookup fix |
| Start Date differs from loaded Start Date | Blocking | read_worker_time_profile | The change is described or routed as CORRECTION | Use effective-dated UPDATE semantics | Routing fix |
| Start Date matches loaded Start Date or is blank during edit | Blocking | read_worker_time_profile | The change is described or routed as UPDATE | Reuse loaded date and use CORRECTION semantics | Routing fix |
| An existing profileProperties update or correction is prepared | Blocking | read_worker_time_profile | SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, EffectiveEndDate, or effectiveOf is absent from the DAT; either effective-date field is not YYYY-MM-DD; TimeProfileId differs from SetupProfileId; or effectiveOf is not RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD} | Rebuild the DAT from the freshly read child values and metadata; populate TimeProfileId with the same value as SetupProfileId and serialize both effective-date fields as YYYY-MM-DD | Provider fix |
| A new or duplicated Time Profile has a profileProperties row | Blocking | review_time_profiles_dataloader_metadata | TimeProfileId or SetupProfileId is absent, nonnumeric, or differs from the new parent local ID | Rebuild the child row with both fields populated by the same newly generated numeric parent local ID | Provider fix |
| A calendarEventPayrollElements row is created | Blocking | review_time_profiles_dataloader_metadata | TimeProfileId is absent, nonnumeric, or does not match the new parent local ID for a new or duplicated parent or the verified TimeProfileId for an existing parent | Rebuild the calendar-event child row with the applicable numeric parent TimeProfileId | Provider fix |
| A profileAssignments row is created | Blocking | review_time_profiles_dataloader_metadata | TimeProfileId is absent, nonnumeric, or does not match the new parent local ID for a new or duplicated parent or the verified TimeProfileId for an existing parent | Rebuild the profile-assignment child row with the applicable numeric parent TimeProfileId | Provider fix |
| An existing calendarEventPayrollElements update or correction is prepared | Blocking | read_worker_time_profile | SetupProfileExtraInformationId, EffectiveStartDate, or EffectiveEndDate is absent from the DAT, or either effective-date field is not YYYY-MM-DD | Rebuild the DAT from the freshly read child values and metadata; serialize both effective-date fields as YYYY-MM-DD | Provider fix |
| Duplicate | Blocking | read_worker_time_profile | Source identity, status, priority, setup identifiers, or effective dates are retained as identity for the new record | Remove source lifecycle identity and require a new name and start date | Input fix |
| Delete Changes | Blocking | read_time_profile_history | The action is represented as whole-profile delete, lacks an eligible history row and returned child links, or bypasses the Data Loader provider | Pass the verified delete intent and effective context to core.data-loader for its supported delete mapping | Routing fix |
| Parent item DELETE is considered | Blocking |  | Service capability is treated as active UI behavior or its cascade rules are invented | Treat it as inactive for this skill until an approved source defines whole-profile deletion | No |
| Assignment validation is invoked | Blocking |  | validateProfileAssignments is included in ADF batch | Invoke it independently because live describe reports batchEnabled=false | Routing fix |
| Any item or child operation | Blocking | read_worker_time_profile | A composite path key is invented from finder metadata | Follow returned opaque links | Lookup fix |
| Any write is proposed | Blocking |  | Read-only audit fields, derived display values, UI-only EnableChangeAuditFlag, or sample values are included | Keep only documented writable stored fields in the provider-owned preview | Input fix |
| Any CRUD mutation is proposed | Blocking |  | The consuming task invokes POST, PATCH, or DELETE directly on timeProfiles or constructs its own execution request | Route normalized verified fields to core.data-loader; the provider owns DAT creation, archive preparation, submission, and verification | Routing fix |
| Any Data Loader handoff is proposed | Blocking |  | dataloader_import_mode is not REST or businessObject is not exactly timeProfiles | Pass REST and timeProfiles unchanged to core.data-loader | Input fix |
| An existing profileProperties DAT is prepared | Blocking | read_worker_time_profile | The DAT does not carry SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, and EffectiveEndDate, TimeProfileId differs from SetupProfileId, or it omits date-effective effectiveOf context | Populate TimeProfileId with the same value as SetupProfileId, return the required values and effectiveOf context to core.data-loader, and require regenerated, revalidated archive bytes | Provider fix |
| An existing calendarEventPayrollElements DAT is prepared | Blocking | read_worker_time_profile | The DAT does not carry SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate, or either effective-date field is not YYYY-MM-DD | Return the required identifiers and YYYY-MM-DD effective-date values to core.data-loader and require regenerated, revalidated archive bytes | Provider fix |
| A new date-effective child DAT is prepared | Blocking | review_time_profiles_dataloader_metadata | effectiveOf contains RangeMode or is not RangeStartDate={YYYY-MM-DD} | Rebuild the create DAT with effectiveOf as RangeStartDate={YYYY-MM-DD}; do not add RangeMode | Provider fix |
| Any Time Profiles DAT is about to be created | Blocking | review_time_profiles_dataloader_metadata | The selected task SKILL.md and applicable ora_* rules were not reviewed, or fresh live timeProfiles Data Loader sample headers and attribute details were not reviewed to derive the applicable field set, key form, and value formats | Stop before DAT creation; complete the metadata preflight and use only its reviewed values and representations | Provider fix |
| A Time Profiles Data Loader source contains a Boolean attribute | Blocking | review_time_profiles_dataloader_metadata | A populated Boolean value is not the lowercase text literal `true` or `false`, or an unset Boolean is represented by a placeholder | Regenerate the source with lowercase `true` or `false` for each populated Boolean and omit unset Boolean attributes, then validate the regenerated archive | Provider fix |
| An existing-profile timeProfiles parent context row is prepared | Blocking | review_time_profiles_dataloader_metadata | RestAction is UPDATE or any value other than PATCH solely because the profile already exists or the lifecycle is described as an update | Rebuild the parent context row with RestAction PATCH; do not conflate lifecycle terminology with the Data Loader parent action | Provider fix |
| Any Time Profiles DAT is prepared | Blocking | review_time_profiles_dataloader_metadata | An emitted METADATA section has no populated MERGE row, or an emitted field is blank, null, unused, read-only, or a placeholder rather than a verified value | Remove the empty section and blank placeholder fields; retain only verified populated writable fields and sections with data rows, then regenerate and validate the archive | Provider fix |
| A Data Loader mutation is ready for preview | Blocking |  | The provider has not generated and validated the DAT file and immutable ZIP archive | Invoke core.data-loader to generate, validate, and preview the archive before submission | Provider fix |
| A validated request is ready for provider-owned approval | Blocking |  | Complete Summary is absent; contains a blank, metadata-only, technical, identifier, code, key, opaque link, request detail, diagnostic, or warning; omits a verified user selection or an actually applied default; uses a technical label where a verified business label is available; or paraphrases, renames, combines, or substitutes a configured field label or selected display value | Generate the exact business-only summary format below from verified Fusion business labels and selected display values, then transition to the provider-owned approval process without changing provider execution or approval ownership | Automatic summary generation allowed |
| Any mutation is proposed | Blocking |  | Exact target environment, operation, immutable Data Loader archive preview, or the core.data-loader approval gate is absent | Use the provider's approval workflow; do not add a second consuming-task approval for the same submission | No automatic fix |
| An approved asynchronous submission has been accepted | Blocking | monitor_approved_time_profile_load | Terminal success has not been returned, the result is failed, timed out, partial, uncertain, or unavailable, or persisted state has not passed verify_submitted_time_profile | Let core.data-loader own task-authorized monitoring; do not report final success or retry until terminal success and documented read-back verification pass | No automatic fix |

## Required Complete Summary Format

The customer-facing summary must use the following headings and table columns.
It must contain no warnings, diagnostics, technical notes, or technical labels.

```md
## Complete Summary

| Business Setting | Selected Value |
|---|---|
| {business label} | {verified business display value} |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| {business label} | {verified default display value} |
```

Add a named child-record section with the same Business Setting and Selected
Value columns only when that child has populated verified business values. Do
not render an empty child section.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_time_profile_feature_enabled | Every request before Time Profiles activity | Verified Enable Time Profile availability for the current user or the exact site-level fallback when the effective value is unavailable | ora_reference_lookups.md |
| resolve_next_time_profile_priority | Create or duplicate before the Complete Summary, Data Loader preview, or approval | Latest highest Priority and derived next Priority | ora_reference_lookups.md |
| search_time_profiles | A user asks to browse or search Time Profiles | Paginated business results and explicit selection when one profile is required | ora_reference_lookups.md |
| find_similar_time_profiles_for_reuse | A create request has no exact ProfileName match | Full-match candidate profiles and explicit reuse-or-create decision | ora_reference_lookups.md |
| read_worker_time_profile | Existing profile operations | Fresh parent and child state, effective context, and opaque links | ora_reference_lookups.md |
| find_time_profile_by_exact_name | Existing profile operations and final verification | Verified profile identity and item link | ora_reference_lookups.md |
| resolve_time_card_period | Create, duplicate, update, or correct | TimecardPeriodId and optional OvertimePeriodId | ora_reference_lookups.md |
| resolve_time_card_layout_set | Create, duplicate, update, or correct | LayoutSetId | ora_reference_lookups.md |
| resolve_time_consumer_set | Consumer Set is supplied | TimeConsumerSetId compatible with selected period | ora_reference_lookups.md |
| resolve_calendar_event_category | Calendar rows are included | CalendarEventCategoryCode | ora_reference_lookups.md |
| resolve_payroll_time_type | Payroll selection is supplied | PayrollTimeTypeCode and LDGId for calendar-event; documented on-call fields for on-call | ora_reference_lookups.md |
| resolve_yes_no_lookup | Calendar rows are included | IncludeIneligiblePatternDays code | ora_reference_lookups.md |
| resolve_time_attribute_field | Time Attributes are supplied | Ordered identifiers for up to ten fields | ora_reference_lookups.md |
| resolve_geofence_validation_mode | Geofencing is enabled | Mode code and applicability result | ora_reference_lookups.md |
| validate_profile_assignments | Assignments are added or changed | Server validation outcome | ora_reference_lookups.md |
| read_time_profile_history | View History or Delete Changes | Selected eligible history row | ora_reference_lookups.md |
| monitor_approved_time_profile_load | Approved asynchronous submission is accepted | Terminal provider request result and sanitized diagnostics | ora_reference_lookups.md |
| verify_submitted_time_profile | Provider reports terminal success | Persisted Time Profiles state for supported approved values and applied defaults | ora_reference_lookups.md |
| review_time_profiles_dataloader_metadata | Before any Time Profiles DAT creation | Reviewed DAT headers, required keys, writable fields, SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, EffectiveEndDate, date fields, and effectiveOf representation | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the provider handoff gate |
| not_required | No design rule applies to the requested read-only scope | Continue without changing configuration |
| blocked | An applicable blocker, unresolved required contract, or missing approval evidence remains | Stop and require the declared correction |

## Source Basis

- README.md scope and evidence labels
- 01-functional-specification.md
- 03-authoring-guardrails.md
- 05-crud-lifecycle-behavior.md
- 06-rest-describe-evidence.md
- 07-ui-field-rest-service-matrix.md
- Developer-provided authoring directive: Time Profile identity lookup uses GET {BASE}/timeProfiles?q=ProfileName='{exact Profile Name}'; do not use LIKE, contains matching, or Advanced Search
- Developer-provided authoring directive: use core.data-loader with businessObject timeProfiles for CRUD mutations
- Developer-provided authoring directive: serialize every populated EffectiveStartDate and EffectiveEndDate as YYYY-MM-DD; reject every other representation before validation or preview
- Developer-provided authoring directive: every new calendarEventPayrollElements and profileAssignments child row includes TimeProfileId; use the same newly generated numeric parent local ID for a new or duplicated parent, or the verified parent TimeProfileId for an existing parent
- Developer-provided authoring directive: require a business-only Complete Summary before the provider-owned approval process
- Developer-provided authoring directive: defaults apply only when the user is silent; verified explicit user selections take precedence across all supported fields
- Developer-provided authoring directive: all Time Profiles LOV and selector searches use bounded contains or LIKE matching, present eligible choices, and offer bounded closest choices when the contains search returns none
- Developer-provided authoring directive: before creating every Time Profiles DAT, review the selected task guidance and fresh live Data Loader metadata/sample headers and attribute details; use the reviewed field set, key form, and value formats without inference
- Developer-provided authoring directive: when an existing-profile DAT requires a timeProfiles parent context row, set RestAction to PATCH; never infer UPDATE from the profile's existence or lifecycle label
- Developer-provided authoring directive: emit only DAT fields with verified values and only sections with a populated MERGE row; reject blank placeholder columns and metadata-only sections before validation or preview
- Developer-provided authoring directive: for calendar-event payroll rows, strip any leading LDG identifier from a composite selected payroll Code only when populating PayrollTimeTypeCode, and retain that LDG identifier in the separate LDGId attribute

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TP.DESIGN | decision | 23 | design_enforcement | passed->TP.DATALOADER_METADATA;not_required->TP.DATALOADER_METADATA;blocked->TP.ERROR | TP.DEFAULTS | stop | After validation, reference resolution, all selected-feature prerequisite checks, defaults, and Complete Summary generation complete |
