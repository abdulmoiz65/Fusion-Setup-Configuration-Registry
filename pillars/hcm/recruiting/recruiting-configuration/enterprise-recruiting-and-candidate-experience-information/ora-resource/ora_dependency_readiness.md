# Dependency Readiness

## Candidate Sourcing Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fresh current full-task export | Use the existing shared current-export workflow and require its successful fresh ORA_IRC_SETTING.csv result before any Candidate Sourcing read, preview, or modification. |
| 2 | Exact setting mappings and current values | Resolve every requested UI field to exactly one of the eight authoritative setting codes and retain only exact exported current values. |
| 3 | Conditional Talent Community attributes default | When a modification proposes Enable Talent Community = Y and omits the attributes field, add Job Category without overriding an explicit value. |
| 4 | Final Talent Community state | Before processing Talent Community attributes or Global Talent Community Pool visibility, require the final Talent Community state to be enabled, using the proposed value when supplied or the exact fresh-export current value otherwise. |
| 5 | Per-field validation | Validate each exact-mapped field against its Boolean, whole-number range, or exact Talent Community attributes contract. |
| 6 | CSV or FSM/ADF route classification | Allow Global Talent Community Pool Visible = N through CSV; route Y only to the documented Candidate Sourcing FSM/ADF UI save action. Separate both routes explicitly in a mixed request. |
| 7 | Existing guarded workflow | Continue CSV-eligible fields only through the existing combined-preview, approval, and import workflow. Do not silently import a subset of a mixed-route request. |

## Candidate Sourcing Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CAND-SRC-FRESH-EXPORT-MAPPINGS | Fresh current full-task Candidate Sourcing setting mappings | Yes | Before any Candidate Sourcing read, preview, or modification | Verify | Successful fresh ORA_IRC_SETTING.csv result from the existing shared current-export workflow | verify_candidate_sourcing_setting_mappings | Exact exported evidence prevents guessed setting rows, mappings, and current values | Obtain a fresh full-task export; a missing or duplicate mapping blocks only the affected field and any field that depends on unavailable Talent Community state | UI label, exact setting code, current value, row identity, mapping status, final-state evidence, and fresh-export provenance |
| CAND-SRC-TALENT-COMMUNITY-ENABLED | Final Talent Community enabled state | Conditional | Talent Community attributes or Global Talent Community Pool visibility is requested or conditionally defaulted | Verify | A valid proposed ORA_IRC_TC_OPTIN_ENABLED value in the same request, otherwise its exact current value from the fresh export | verify_candidate_sourcing_setting_mappings | The two dependent settings are applicable only while Talent Community is enabled | Set Enable Talent Community to Y in the same request or confirm its exact current exported value is Y; otherwise remove or correct the dependent field | Final Talent Community value and whether it came from the proposed request or fresh export |

## Candidate Search Archiving Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fresh current full-task export | Use the existing shared current-export workflow and require its successful fresh full-task result before any Candidate Search Archiving read, preview, or modification. |
| 2 | Exact setting mapping | Require exactly one exported mapping for ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED and stop only Candidate Search Archiving when the mapping is missing or duplicated. |
| 3 | User-facing validation | Accept only Enabled or Disabled and keep the corresponding stored Y or N value internal. |
| 4 | Combined preview | Display Candidate Search Archiving with the required four preview columns and user-facing values only. |
| 5 | Existing approval and import workflow | Continue only through the existing shared approval and import workflow without introducing an alternate execution route or fallback. |

## Candidate Search Archiving Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CSA-FRESH-EXPORT-MAPPING | Fresh current full-task Candidate Search Archiving mapping | Yes | Before any Candidate Search Archiving read, preview, or modification | Verify | Successful fresh full-task result from the existing shared current-export workflow | verify_candidate_search_archiving_setting_mapping | Exact exported evidence prevents a guessed or substituted setting identity | Obtain a fresh full-task export through the existing current-export workflow; a missing or duplicate mapping blocks only Candidate Search Archiving | Internal setting identity, current stored value, row identity, mapping status, and fresh-export provenance |

## Updates to Candidate Info Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fresh current full-task export | Use the existing shared current-export workflow and require its successful fresh full-task result before any Updates to Candidate Info read, preview, or modification. |
| 2 | Exact Candidate Type and field mappings | Require exactly one exported setting mapping for every requested Candidate Type and field pair and stop only a pair whose mapping is missing or duplicated. |
| 3 | Active user-facing meanings | Resolve every retained current and proposed value through the active Common Lookup and keep lookup codes internal. |
| 4 | Independent validation | Validate exact Candidate Type names, fields, and permitted active meanings independently while preserving all successful validation results. |
| 5 | Combined preview | Include every requested pair and its validation or mapping status in one five-column preview. |
| 6 | Atomic approval and import | Continue through the existing approval and import workflow only when every requested pair passes. Never import only the successful subset. |

## Updates to Candidate Info Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| UCI-FRESH-EXPORT-MAPPINGS | Fresh current full-task Candidate Type and field mappings | Yes | Before any Updates to Candidate Info read, preview, or modification | Verify | Successful fresh full-task result from the existing shared current-export workflow | verify_candidate_info_update_setting_mappings | Exact exported evidence prevents guessed or cross-Candidate-Type setting identities | Obtain a fresh full-task export through the existing current-export workflow; a missing or duplicate mapping blocks only the affected pair | Internal Candidate Type and field mapping, setting identity, current lookup code, row identity, mapping status, and fresh-export provenance |
| UCI-ACTIVE-ALLOWED-VALUES | Active Common Lookup ORA_IRC_CAND_TYPE_BLOCK_UPDATE | Yes | An Updates to Candidate Info pair is requested, displayed, previewed, or modified | Lookup | Target Common Lookups | resolve_candidate_info_update_allowed_values | Current values, permitted user-facing values, and proposed values must resolve to active meanings while lookup codes remain internal | Use one active meaning: None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal; correct every unresolved or ambiguous pair before approval or import | Candidate Type, field, current meaning, proposed meaning, permitted active meanings, and internal resolved code for the guarded workflow |

## Configure Active Candidate Filter Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fresh current full-task export | Use the existing shared current-export workflow and require its successful fresh full-task result before any Configure Active Candidate Filter read, preview, or modification. |
| 2 | Exact setting mappings | Require exactly one exported setting mapping for every requested field and stop only a field whose documented mapping is missing or duplicated. |
| 3 | Active Activity Timeframe meanings | When Activity Timeframe is in scope, resolve its current value, permitted values, and proposed value through the active Common Lookup and retain lookup codes internally. |
| 4 | Per-field input validation | Validate one or multiple requested settings independently and retain every event-specific activity field as a separate item. |
| 5 | Combined user-facing preview | Build one combined preview containing every requested field with user-facing values only. |
| 6 | Existing approval and import workflow | Hand the unchanged combined preview to the existing approval and import workflow; do not introduce an alternate execution route or fallback. |

## Configure Active Candidate Filter Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ACF-FRESH-EXPORT-MAPPINGS | Fresh current full-task setting mappings | Yes | Before any Configure Active Candidate Filter read, preview, or modification | Verify | Successful fresh full-task result from the existing shared current-export workflow | verify_active_candidate_filter_setting_mappings | Exact exported evidence prevents guessed setting identities and preserves the shared workflow baseline | Obtain a fresh full-task export through the existing current-export workflow; a missing or duplicate mapping blocks only the affected field | Internal setting identity, current internal value, row identity, mapping status, and fresh-export provenance |
| ACF-ACTIVE-TIMEFRAME-MEANINGS | Active Common Lookup ORA_IRC_CAND_ACT_TIMEFRAME | Conditional | Activity Timeframe is requested, displayed, previewed, or modified | Lookup | Target Common Lookups | resolve_active_candidate_timeframe_meanings | The current value, permitted user-facing values, and proposed value must use active meanings while lookup codes remain internal | Select one active user-facing Activity Timeframe meaning; correct an unresolved or ambiguous value before including that field | Current meaning, proposed meaning, permitted active meanings, and internal resolved code for the guarded workflow |

## Candidate Experience Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current-workflow fresh task export | Obtain a successful fresh target export before any Candidate Experience preview or CSV generation; do not reuse cached export evidence. |
| 2 | Exact setting mappings | Resolve every supplied Candidate Experience field to exactly one fresh-export row using only its documented setting code. |
| 3 | Per-field validation | Validate each exactly mapped field against its documented scalar contract and stop only fields that fail. |
| 4 | Preview and CSV handoff | Use the required four-column preview and continue only with independently valid, exactly mapped fields. |

## Candidate Experience Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CAND-EXP-FRESH-EXPORT-MAPPINGS | Fresh Candidate Experience setting mappings | Yes | Before every Candidate Experience preview or CSV modification | Resolve | Successful fresh target-environment task export produced for the current Candidate Experience workflow | verify_candidate_experience_setting_mappings | Candidate Experience setting codes must never be guessed, substituted, appended, or selected from duplicate rows | Obtain a fresh export when needed; correct only fields whose exact documented setting-code mapping is missing or duplicated | Per-field setting code, current value, exported row identity, and exact-mapping status |

## Candidate Authenticity Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Candidate Authenticity Site-level profile option | Read ORA_IRC_CANDIDATE_AUTHENTICITY_AGENT_ENABLED through core.fusion-api.apps-common.profile-options and continue only when its configured Site-level value is exactly Y. |
| 2 | Complete Candidate Authenticity input | After readiness succeeds, require nonblank values for Endpoint URL, Access Token URL, and Scope and validate all three fields atomically. |
| 3 | Credential boundary | Reject credential fields and prevent their values from entering CSV input, import artifacts, previews, logs, diagnostics, or runtime output. |
| 4 | CSV workflow handoff | Continue only when readiness, atomic input validation, and the credential boundary all succeed. |

## Candidate Authenticity Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CAND-AUTH-PROFILE-OPTION | ORA_IRC_CANDIDATE_AUTHENTICITY_AGENT_ENABLED configured Site-level profile option | Yes | Before validating or importing a Candidate Authenticity Settings modification | Verify | Current configured target Site-level profile option value returned by core.fusion-api.apps-common.profile-options | verify_candidate_authenticity_profile_option_enabled | Candidate Authenticity settings may be validated or imported only when the prerequisite value is exactly Y | If the value is N, blank, missing, unavailable, or unreadable, enable Candidate Authenticity before updating its settings | CandidateAuthenticityProfileOptionCode, CandidateAuthenticityProfileOptionLevel, and CandidateAuthenticityProfileOptionValue |

## Events Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Events API version | Use the explicitly supplied api_version or default it to latest when omitted. |
| 2 | Advanced Recruiting readiness | Resolve fresh same-target Advanced Recruiting status through verify_events_advanced_recruiting_enabled before any Events export, input validation, downstream setup-data validation, or import. |
| 3 | Complete Events input | Require both Events setting values and validate the pair atomically as whole numbers from 1 through 999. |
| 4 | CSV workflow handoff | Continue only when Advanced Recruiting is enabled and both Events values are valid. |

## Events Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| EVENTS-ADVANCED-RECRUITING | Advanced Recruiting | Yes | Before any Events export, input validation, downstream setup-data validation, or import | Verify | Fresh same-target Fusion Features response | verify_events_advanced_recruiting_enabled | Events processing may proceed only when Advanced Recruiting is enabled | Supply a supported api_version when required, or allow latest by default; stop when Advanced Recruiting is disabled, unavailable, unauthorized, unsupported, or indeterminate | ResolvedEventsApiVersion, AdvancedRecruitingFeatureCode, and AdvancedRecruitingEnabledFlag |

## Interview Intelligence Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Section read export source | Reuse the latest valid matching completed export for an ordinary read, or require a fresh task export when freshness is requested or reuse cannot be proven. |
| 2 | Current mutation export | For an Interview Intelligence change, use an export produced for the current mutation workflow as the package baseline. |
| 3 | Recruiting Booster readiness | Resolve `{version}` to the caller-supplied supported REST API version or `latest`, run the exact same-target Features REST item GET, and require `ORA_IRC_ADVANCED_RECRUITING` to return `EnabledFlag=Y` before changing any Interview Intelligence setting. |
| 4 | Calendar integration readiness | When enabling loop scheduling, confirm Microsoft Graph or Google Calendar is available. |
| 5 | Data Loader handoff | Validate the exact changed package before routing it to core.data-loader. |

## Shared Export and Interview Intelligence Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SECTION-EXPORT-SOURCE | Reusable section export | Yes | Any supported section read | Resolve | Append-only `skill_run_record` files produced by this task | find_reusable_section_export | Ordinary reads can use verified local evidence without causing an unnecessary export, but explicit freshness and ambiguous evidence require refresh | Reuse the latest valid matching completed export or obtain a fresh export through `shared.setup-export.task-level-export` | Source export path, CSV path, ProcessId, completion timestamp, SHA-256, target environment, task code, optional release, and source mode |
| II-CURRENT-EXPORT | Current mutation export | Yes | Any Interview Intelligence change | Resolve | Successful `shared.setup-export.task-level-export` result recorded by this task for the current mutation workflow | | Environment-specific SettingValueId values and unrelated settings must be preserved | Obtain and record a fresh target-environment export before preparing the change; reuse it within the same workflow | Current ORA_IRC_SETTING.csv, unchanged ORA_IRC_SETTING_VALUE.csv, and export evidence fields |
| II-BOOSTER-READINESS | Recruiting Booster | Yes | Any Interview Intelligence change | Verify | Fresh same-target response from `GET /fscmRestApi/resources/{version}/features/ORA_IRC_ADVANCED_RECRUITING`, with `{version}` resolved before execution | verify_recruiting_booster_enabled | The Interview Intelligence section is available only when `ORA_IRC_ADVANCED_RECRUITING` is enabled | Run the resolved item GET through `core.fusion-api.rest-api-client`; default to `latest` when no explicit REST API version is supplied, and never send literal braces; a missing, disabled, mismatched, unauthorized, or cross-environment response blocks every Interview Intelligence change | ResolvedRestApiVersion, RecruitingBoosterFeatureCode, and RecruitingBoosterEnabledFlag |
| II-CALENDAR-READINESS | Calendar integration | Yes | Enabling interview loop scheduling | Satisfied | Caller-provided task context | | Loop scheduling additionally requires MICROSOFT_GRAPH or GOOGLE_CALENDAR in availableCalendarIntegrations | Supply at least one accepted calendar integration | Accepted calendar integration |
| II-DATALOADER | FSM CSV import route | Yes | A validated nonempty Interview Intelligence change is ready for import | Route | core.data-loader | | The task catalog supports FSM CSV export and import; core.data-loader owns preview approval and submission | Hand off the validated immutable ZIP to core.data-loader | Target environment, task code, ZIP path, and SHA-256 |

## Integration FSM Prerequisites

These dependencies are advisory outputs for the manual FSM route. They are not
satisfiable or verifiable from the task CSV alone.

| Section | FSM prerequisites | CSV limitation |
|---|---|---|
| Microsoft Graph Integration | Application and tenant identity, secure application password, Save, and successful integration validation | Exported O365 and endpoint rows do not populate the secure credential store or prove validation |
| Google Workspace Integration | Active Google Workspace Integration Privacy Policy content, completed authorization, Save, and successful integration validation | The export does not contain authorization or refresh tokens and cannot prove privacy-content readiness |
| Zoom Integration | Client credentials stored through FSM, Save, and successful integration validation | Client ID and secret CSV rows do not prove secure credential-store provisioning or validation |

Resolve only the prerequisites required by the supplied Offer, Move to HR, or
Agency Hiring settings. These checks are read-only. They must not create or
update a profile-option value, lookup value, Security Console User Category,
or Security Console role as a side effect. The Move to HR dependency and
Agency Hiring Security Console verification are manual gates.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Applicable Offer profile options | Read each required Site-level profile option through the common Profile Option Values skill and require its current value to be Y. |
| 2 | Specific Offer collaborator types | Resolve every supplied label or code through the common Lookups skill against ORA_IRC_COLLABORATOR_RESP_TYPE and require one enabled current LookupCode for each selection. |
| 3 | None representation | When None is requested, use only the stored CSV representation established by the fresh target export or task metadata. |
| 4 | Move to HR duplicate-check configuration | When Duplicate Check in Move to HR is supplied, require manual completion in Fusion and require the Enterprise HCM Information: Person Creation Duplicate Check setup. Do not route this setting to the common Profile Option Values skill. |
| 5 | Agency Hiring Security Console verification | Before previewing Agent User Category or Agent Role, require manual confirmation that the supplied code exists in the target Security Console. The current skill has no approved read-only lookup route. |
| 6 | Dependency decision | Reject the complete affected setting or collaborator selection when any required dependency is missing, disabled, ambiguous, unresolved, unverified, or awaiting manual completion. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| IRC.OFFER.AUTO_PROCESS_PROFILE | ORA_IRC_AUTO_PROCESS_INTERNAL_OFFERS Site-level profile option | Conditional | ORA_IRC_INTERNAL_OFFER_AUTO_PROCESS_DAYS is supplied. | Verify | Current target Site-level profile option value | resolve_offer_profile_option_prerequisites | The Days Before Proposed Start Date setting is available only when this feature gate is Y. | Enable ORA_IRC_AUTO_PROCESS_INTERNAL_OFFERS through the common Profile Option Values skill before updating the dependent Offer setting. | Profile option code, current Site-level value, affected setting code, and affected UI field |
| IRC.OFFER.TERMINATE_ASSIGNMENT_PROFILE | ORA_IRC_OFFERS_TERMINATE_ASG_ENABLED Site-level profile option | Conditional | ORA_IRC_OFFER_PROCESSED_ASG_END_DATE_DAYS, ORA_IRC_OFFER_TERMINAL_ASG_END_DATE_DAYS, or ORA_IRC_OFFER_ABANDONED_DAYS is supplied. | Verify | Current target Site-level profile option value | resolve_offer_profile_option_prerequisites | End Dating Offer Assignments requires this prerequisite to be Y. | Enable ORA_IRC_OFFERS_TERMINATE_ASG_ENABLED through the common Profile Option Values skill before updating any dependent end-dating setting. | Profile option code, current Site-level value, affected setting code, and affected UI field |
| IRC.OFFER.TERMINATE_ABANDONED_PROFILE | ORA_IRC_TERM_ABANDONED_OFFERS_ENABLED Site-level profile option | Conditional | ORA_IRC_OFFER_PROCESSED_ASG_END_DATE_DAYS, ORA_IRC_OFFER_TERMINAL_ASG_END_DATE_DAYS, or ORA_IRC_OFFER_ABANDONED_DAYS is supplied. | Verify | Current target Site-level profile option value | resolve_offer_profile_option_prerequisites | The complete end-dating workflow requires this prerequisite and ORA_IRC_OFFERS_TERMINATE_ASG_ENABLED to be Y. | Enable ORA_IRC_TERM_ABANDONED_OFFERS_ENABLED through the common Profile Option Values skill before updating any dependent end-dating setting. | Profile option code, current Site-level value, affected setting code, and affected UI field |
| IRC.OFFER.COLLABORATOR_TYPES | Enabled current ORA_IRC_COLLABORATOR_RESP_TYPE lookup codes | Conditional | One or more specific collaborator labels or codes are supplied for ORA_IRC_OFFER_COLLABORATORS_TO_COPY. | Lookup | Target Common Lookups | resolve_offer_collaborator_types | The stored StringValue must contain verified collaborator-type codes, not inferred UI labels. | Correct every unknown, disabled, or ambiguous selection; the complete collaborator selection is rejected until all items resolve. | One LookupCode per supplied selection, retained in requested order |
| IRC.OFFER.COLLABORATOR_NONE | Stored CSV representation for None | Conditional | None is supplied for ORA_IRC_OFFER_COLLABORATORS_TO_COPY. | Verify | Fresh target ORA_IRC_SETTING.csv and ORA_IRC_SETTING_VALUE.csv export or task metadata | resolve_offer_collaborator_none_representation | The source explicitly prohibits guessing whether None is blank or another stored value. | Obtain a fresh export or task metadata that establishes how the selection is cleared; otherwise use the manual Fusion action. | Exact stored CSV representation for clearing all collaborator types |
| IRC.MOVE_TO_HR.PERSON_CREATION_DUPCHECK | Enterprise HCM Information: Person Creation Duplicate Check | Conditional | Duplicate Check in Move to HR is supplied. | Blocked | Manual target-environment configuration and confirmation | | Duplicate Check in Move to HR is not represented in ORA_IRC_SETTING.csv and depends on the Enterprise HCM Information setting. | Configure Person Creation Duplicate Check in Enterprise HCM Information, then complete Duplicate Check in Move to HR manually in Fusion. Do not use the common Profile Option Values skill. | Selected UI value, confirmation of the Enterprise HCM Information dependency, and confirmation of manual completion |
| IRC.AGENCY_HIRING.USER_CATEGORY | Target Security Console User Category | Conditional | ORA_IRC_AGENCY_USER_CATEGORY_CODE is supplied. | Blocked | Manual target Security Console verification and user-provided verified code | | The setting is FSM-importable, but the current skill has no approved read-only Security Console route for verifying the code. | Verify the code in the target Security Console and provide the verified code before preview. Do not invent a value or create a User Category. | Verified target User Category code and manual verification confirmation |
| IRC.AGENCY_HIRING.AGENT_ROLE | Target Security Console job role | Conditional | ORA_IRC_AGENT_CUSTOM_ROLE_CODE is supplied. | Blocked | Manual target Security Console verification and user-provided verified code | | The setting is FSM-importable, but the current skill has no approved read-only Security Console route for verifying the code. | Verify the code in the target Security Console and provide the verified code before preview. Do not invent a value or create a role. | Verified target job-role code and manual verification confirmation |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Candidate Experience ready | Every remaining supplied field has exactly one fresh-export setting mapping and passes its scalar validation. | Continue to the required Candidate Experience preview and guarded CSV workflow. |
| Candidate Experience partially ready | Some supplied fields are blocked by mapping or validation evidence while other fields independently pass. | Continue only with the independently valid fields and disclose every blocked field in the preview. |
| Candidate Experience fresh export required | No successful target export exists for the current Candidate Experience workflow. | Delegate a fresh export to shared.setup-export.task-level-export, then rerun exact mapping before preview or CSV generation. |
| Candidate Experience blocked | No supplied field has both one exact fresh-export mapping and a valid value. | No; stop without generating Candidate Experience CSV rows. |
| Configure Active Candidate Filter ready | Every requested field has one exact fresh-export mapping, Activity Timeframe has resolved active meanings when applicable, all retained values pass per-field validation, and the user-facing combined preview passes display enforcement. | Continue through the existing approval and import workflow. |
| Configure Active Candidate Filter partially ready | Some fields are blocked by mapping, lookup, or input evidence while other fields independently pass. | Continue only with independently valid fields, list every event-specific activity field separately, and disclose each blocked field in the combined preview. |
| Configure Active Candidate Filter fresh export required | No successful fresh current full-task export exists for this workflow. | Use the existing shared current-export workflow and rerun exact mapping; do not use another export or update route. |
| Configure Active Candidate Filter blocked | No requested field remains independently valid, or the combined preview/display policy cannot be satisfied. | Stop without invoking approval or import and without using REST, browser, FSM-save, CSV-import, loader, or Fusion-update fallbacks. |
| Updates to Candidate Info ready | Every requested Candidate Type and field pair has one exact fresh-export mapping, resolves through one active permitted meaning, passes validation, and appears in the combined preview. | Continue through the existing approval and import workflow for the complete request. |
| Updates to Candidate Info validation incomplete | One or more requested pairs are blocked while other pairs validate successfully. | Preserve all results in the combined preview, but stop before approval or import until every requested pair is corrected. Do not perform a partial import. |
| Updates to Candidate Info fresh export required | No successful fresh current full-task export exists for this workflow. | Use the existing shared current-export workflow and rerun exact mapping; do not use another export or update route. |
| Updates to Candidate Info blocked | No requested pair remains valid, or the required exact-name, lookup-meaning, preview, or atomic-import contract cannot be satisfied. | Stop without approval or import and without REST, browser, FSM-save, CSV-import, loader, or Fusion-update fallbacks. |
| Candidate Search Archiving ready | The field has one exact fresh-export mapping, its proposed value is Enabled or Disabled, and the required user-facing preview passes display enforcement. | Continue through the existing approval and import workflow. |
| Candidate Search Archiving fresh export required | No successful fresh current full-task export exists for this workflow. | Use the existing shared current-export workflow and rerun exact mapping; do not use another export or update route. |
| Candidate Search Archiving blocked | The mapping is missing or duplicated, the input or preview is invalid, or the shared workflow cannot be preserved. | Stop only Candidate Search Archiving without approval or import and without REST, browser, FSM-save, CSV-import, loader, Fusion-update, or other fallbacks. |
| Candidate Sourcing CSV ready | Every retained CSV-eligible field has one exact fresh-export mapping, a valid value, satisfied Talent Community dependency when applicable, and a compliant UI-label-first preview. | Continue through the existing approval and import workflow. |
| Candidate Sourcing partially ready | Some fields are blocked by mapping, current-value, dependency, or input evidence while other independent fields validate successfully. | Preserve every field result in the combined preview; continue only after the user reviews the blocked fields and the exact CSV scope. |
| Candidate Sourcing FSM/ADF UI action required | Global Talent Community Pool Visible = Y is the only requested action and Talent Community is enabled in the final state. | Do not create or import a CSV row. Require the documented Candidate Sourcing FSM/ADF UI save action to enable or create the pool. |
| Candidate Sourcing mixed action required | Global Talent Community Pool Visible = Y is requested with one or more CSV-eligible changes. | Show the CSV and FSM/ADF routes separately and obtain an explicit decision for the split workflow; do not silently import only the CSV subset. |
| Candidate Sourcing fresh export required | No successful fresh current full-task ORA_IRC_SETTING.csv export exists for this workflow. | Use the existing shared current-export workflow and rerun exact mapping; do not infer rows, mappings, or current values. |
| Candidate Sourcing blocked | No requested field remains valid, a Talent Community dependent field lacks an enabled final state, or the required route separation cannot be satisfied. | Stop without generating an invalid or unsupported Candidate Sourcing import row. |
| Candidate Authenticity ready | The configured Site-level value of ORA_IRC_CANDIDATE_AUTHENTICITY_AGENT_ENABLED is exactly Y and the complete three-field request passes validation and the credential boundary. | Continue to the guarded Candidate Authenticity CSV workflow. |
| Candidate Authenticity blocked | The Site-level prerequisite is N, blank, missing, unavailable, or unreadable; a mandatory setting is missing or blank; or a credential field is supplied. | No; stop the complete Candidate Authenticity request before validation or import as applicable, and do not create a partial package. |
| Events ready | A fresh same-target Advanced Recruiting lookup confirms the feature is enabled and the complete Events input is valid. | Continue to the applicable Events read or CSV workflow. |
| Events blocked | Advanced Recruiting is disabled, unavailable, unauthorized, unsupported, or indeterminate, or either Events value is missing or invalid. | No; stop the complete Events request without saving, exporting, invoking downstream setup-data validation, or importing either setting. |
| Reusable | A matching completed export passes all cache-validity and provenance checks. | Local read-only lookup only. |
| Refresh required | Freshness was requested, no matching export exists, or validity/provenance cannot be proven. | Delegate export creation to `shared.setup-export.task-level-export`. |
| Route | A validated immutable Interview Intelligence package is ready for the shared import workflow. | No. |
| Satisfied | Every applicable profile option is Y, each applicable collaborator selection or None representation is resolved, any supplied Move to HR manual-only setting is confirmed complete with its Enterprise HCM Information dependency, and every supplied Agency Hiring Security Console code is manually verified. | Continue to the design and CSV-support gate. |
| Not Applicable | No supplied Offer setting requires a profile-option, collaborator-type, or None-representation check, the Move to HR manual-only setting is not supplied, and no Agency Hiring Security Console reference code is supplied. | Continue without an Offer lookup, Move to HR manual dependency, or Agency Hiring manual verification. |
| Blocked | A required profile option is not Y, a collaborator selection is unknown, disabled, or ambiguous, the None representation is not established, the Move to HR manual-only setting or its Enterprise HCM Information dependency is unconfirmed, or an Agency Hiring Security Console code is unknown or unverified. | Use only the documented read-only resolution or manual Fusion action; do not create or update prerequisite or Security Console master data as a side effect. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| II.CHECK_DEPENDENCIES | decision | 4 | resolve_dependency | ready->II.ENFORCE_DESIGN;blocked->II.BLOCKED | II.CHECK_BOOSTER | stop | The Recruiting Booster lookup is enabled and remaining Interview Intelligence dependencies must be evaluated. |
| SECTION.RESOLVE_EXPORT_SOURCE | decision | 15 | resolve_dependency | reusable->SECTION.REPORT_CONFIGURATION;refresh_required->SECTION.FRESH_EXPORT_REQUIRED;invalid->TASK.BLOCKED | TASK.ROUTE_SECTION | stop | A supported section read must resolve reusable evidence or request a fresh task export. |
| IRC.CHECK_OFFER_DEPENDENCIES | decision | 87 | resolve_dependency | satisfied->IRC.CHECK_MOVE_TO_HR_DEPENDENCIES;not_applicable->IRC.CHECK_MOVE_TO_HR_DEPENDENCIES;blocked->IRC.RETURN_ISSUES | IRC.RESOLVE_OFFER_COLLABORATOR_TYPES | stop | Offer is selected; otherwise return not_applicable. |
| IRC.CHECK_MOVE_TO_HR_DEPENDENCIES | decision | 88 | resolve_dependency | satisfied->IRC.CHECK_AGENCY_HIRING_DEPENDENCIES;not_applicable->IRC.CHECK_AGENCY_HIRING_DEPENDENCIES;blocked->IRC.RETURN_ISSUES | IRC.CHECK_OFFER_DEPENDENCIES | stop | Duplicate Check in Move to HR is supplied; otherwise return not_applicable. |
| IRC.CHECK_AGENCY_HIRING_DEPENDENCIES | decision | 89 | resolve_dependency | satisfied->IRC.ENFORCE_CONFIGURATION_MIGRATION;not_applicable->IRC.ENFORCE_CONFIGURATION_MIGRATION;blocked->IRC.RETURN_ISSUES | IRC.CHECK_MOVE_TO_HR_DEPENDENCIES | stop | Agent User Category or Agent Role is supplied for Agency Hiring; otherwise return not_applicable. |
| ACF.CHECK_DEPENDENCIES | decision | 43 | resolve_dependency | ready->ACF.VALIDATE_INPUT;partial->ACF.VALIDATE_INPUT;blocked->ACF.BLOCKED | ACF.RESOLVE_TIMEFRAME_MEANINGS | stop | Confirm exact fresh-export mappings and active Activity Timeframe meaning resolution when applicable before validating Configure Active Candidate Filter input. |
| UCI.CHECK_DEPENDENCIES | decision | 51 | resolve_dependency | ready->UCI.VALIDATE_INPUT;partial->UCI.VALIDATE_INPUT;blocked->UCI.BLOCKED | UCI.RESOLVE_ALLOWED_VALUES | stop | Confirm exact pair mappings and active user-facing value resolution before validating the complete Updates to Candidate Info request. |
| CSA.CHECK_DEPENDENCY | decision | 58 | resolve_dependency | ready->CSA.VALIDATE_INPUT;blocked->CSA.BLOCKED | CSA.RESOLVE_FRESH_EXPORT_MAPPING | stop | Confirm that Candidate Search Archiving has exactly one fresh-export mapping before validating its user-facing value. |
| CAND_SRC.CHECK_DEPENDENCIES | decision | 66 | resolve_dependency | ready->CAND_SRC.VALIDATE_INPUT;partial->CAND_SRC.VALIDATE_INPUT;blocked->CAND_SRC.BLOCKED | CAND_SRC.APPLY_ACTIVE_ATTRIBUTES_DEFAULT | stop | Confirm exact Candidate Sourcing mappings and require an enabled final Talent Community state for attributes and Global Talent Community Pool visibility before input validation. |
