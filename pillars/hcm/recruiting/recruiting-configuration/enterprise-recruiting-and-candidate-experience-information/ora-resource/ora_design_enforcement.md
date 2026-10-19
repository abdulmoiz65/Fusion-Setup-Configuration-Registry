# Design Enforcement

## Interview Intelligence Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve final parent state | Determine the final Interview Companion value before applying child-field requests; when disabled, include every mandatory child reset below, even if omitted from the request or the parent is already N. |
| 2 | Resolve final streaming state | Apply the Companion reset first; otherwise determine the final real-time streaming value. When streaming is disabled, clear Words per Agent Invocation even if omitted from the request or streaming is already N; this reset overrides a conflicting words request. |
| 3 | Apply supported changes | Change only StringValue for requested applicable settings and mandatory child resets in existing setting rows. |
| 4 | Preserve the package contract | Preserve setting codes, SettingValueId values, metadata, and unrelated rows. |
| 5 | Determine whether anything changes | Compare the complete final change set, including mandatory child resets, with the current mutation export before returning no_change. |

## Interview Intelligence Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Interview Companion is disabled in the final requested state | Mandatory | | Any child switch remains enabled or Words per Agent Invocation remains populated. | Set ORA_IRC_INTEVIEW_INSIGHTS_ENABLED, ORA_IRC_DRAFT_FEEDBACK_RESPONSE_ENABLED, and ORA_IRC_IS_REALTIME_STREAMING_ENABLED to N; clear ORA_IRC_IS_RTMS_MIN_TRANSCRIPT_WORDS to an empty StringValue. Apply all four resets even when omitted from the request or Companion is already N. These resets take precedence over conflicting child requests; disclose them in the same preview as the parent. | Yes |
| Interview Companion is enabled in the final requested state | Mandatory | | A requested applicable child value was not normalized and written to its existing StringValue cell. | Apply the validated child change. | Yes |
| Interview Companion is enabled and real-time streaming is disabled in the final requested state | Mandatory | | Words per Agent Invocation remains populated. | Clear ORA_IRC_IS_RTMS_MIN_TRANSCRIPT_WORDS to an empty StringValue, even when omitted from the request or streaming is already N. This mandatory reset takes precedence over a conflicting words request; disclose the old and new values in the same preview as the streaming setting. | Yes |
| Real-time streaming is enabled in the final requested state | Mandatory | | A supplied words value is not blank or an integer greater than or equal to 50. | Correct the value before package preparation. | Yes |
| Interview insights is requested | Blocker | | The implementation substitutes a corrected spelling for ORA_IRC_INTEVIEW_INSIGHTS_ENABLED. | Use the released misspelled setting code exactly. | Yes |
| Any supported Interview Intelligence setting is changed | Blocker | | Code, SettingValueId, CSV structure, metadata rows, or unrelated values change. | Rebuild from the current mutation export and modify only requested applicable StringValue cells and mandatory child resets. Leave interview loop scheduling unchanged unless explicitly requested. | Yes |
| A mandatory Interview Companion or real-time streaming child reset cannot be mapped to exactly one existing export row | Blocker | | A required child row is missing or duplicated. | Stop the complete change before ZIP creation; do not append, guess, or submit a partial parent or child reset. | No |

## Integration Enforcement

| Applies When | Severity | Blocking Condition | Required Result | Fix Allowed? |
|---|---|---|---|---|
| Microsoft Graph Integration modification is requested | Blocker | CSV cannot provision the secure Application Password or prove FSM validation. | Return `FSM_REQUIRED`; report the exported non-secret configuration and direct the user to configure, save, and validate the integration in FSM. | No |
| Google Workspace Integration modification is requested | Blocker | CSV cannot provision authorization or refresh tokens, activate the required privacy-policy content, or prove FSM validation. | Return `FSM_REQUIRED`; direct the user to activate the privacy-policy content and complete authorization and validation in FSM. | No |
| Zoom Integration modification is requested | Blocker | CSV string rows do not establish that the secure credential store is populated or that validation succeeded. | Return `FSM_REQUIRED`; direct the user to configure, save, and validate the integration in FSM. | No |
| Any integration section is reported | Mandatory | Output would expose credential-like values or claim runtime readiness from CSV. | Redact credential values and label every result as exported configuration only. | Yes |

Task-level `csv_export_import_supported_flag: Y` does not override these
section-specific blockers. Do not build a partial integration package, even
when the requested field appears non-secret.

## Candidate Authenticity Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Candidate Authenticity CSV input or import artifact is proposed | Blocker | | The package contains a setting other than ORA_IRC_CAND_AUTH_ENDPOINT_URL, ORA_IRC_CAND_AUTH_ACCESS_TOKEN_URL, and ORA_IRC_CAND_AUTH_AGENT_SCOPE. | Reject the complete request and rebuild it only from the three supported mandatory setting rows. Do not silently remove an unsupported field and continue with a partial package. | No |
| Candidate Authenticity Client ID or Client Secret is supplied | Blocker | | A credential field or its value would be accepted, retained, logged, previewed, diagnosed, emitted, or written to an import artifact. | Reject the credential input without echoing its value, return only a generic protected-credential refusal, and direct credential maintenance to the FSM setup UI. | No |
| Candidate Authenticity output is produced | Blocker | | A preview, log, diagnostic, report, or other runtime output contains a Client ID or Client Secret value. | Omit the credential field and value entirely. Report only that protected credentials must be maintained through the FSM setup UI. | No |

## Configure Active Candidate Filter Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve exact field identity | Retain every requested setting as an independent field after exact fresh-export mapping. |
| 2 | Resolve user-facing values | Convert internal Boolean values to Enabled or Disabled and resolve Activity Timeframe through its active Common Lookup meaning. |
| 3 | Build one combined preview | Include every requested field separately using the required four-column preview. |
| 4 | Preserve the shared workflow | Continue only through the existing combined-preview, approval, and import workflow without introducing another execution route or fallback. |

## Configure Active Candidate Filter Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Configure Active Candidate Filter field is processed | Blocker | verify_active_candidate_filter_setting_mappings | The field does not have exactly one fresh current full-task export mapping for its documented setting code. | Stop only the affected field and explain the evidence gap; do not guess, substitute, append, or select a duplicate row. | No |
| A Configure Active Candidate Filter Boolean value is displayed | Blocker | | The output contains an internal Boolean value instead of Enabled or Disabled. | Rebuild the output using Enabled for the internal enabled value and Disabled for the internal disabled value. | Yes |
| Activity Timeframe is displayed or previewed | Blocker | resolve_active_candidate_timeframe_meanings | The current value, proposed value, or permitted values contain a lookup code or were not resolved to active Common Lookup meanings. | Resolve through the active Common Lookup and display meanings only. | Yes |
| Configure Active Candidate Filter output is produced | Blocker | | The output contains a setting code, row or setting identifier, export filename, lookup code, or other internal value. | Remove the internal value and show only field labels, user-facing meanings, Enabled or Disabled values, and change status. | Yes |
| Event-specific activity settings are listed, validated, or previewed | Blocker | | Two or more event settings are aggregated into an all-event-controls item or any of the twelve documented fields is summarized rather than listed separately. | Rebuild the result with each event-specific activity setting as a separate field. | Yes |
| Multiple Configure Active Candidate Filter changes are requested | Blocker | | The combined preview omits a requested field or uses columns other than Field, Current Value, Proposed Value, and Change Status. | Rebuild one combined preview containing every requested field separately in the required column order. | Yes |
| A Configure Active Candidate Filter workflow is prepared | Blocker | | A direct REST, browser, FSM-save, CSV-import, loader, Fusion-update, or other fallback is proposed outside the existing shared workflow. | Stop the fallback and continue only through the existing current-export, Common Lookup, validation, combined-preview, approval, and import workflow. | No |

## Updates to Candidate Info Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve exact pair identity | Retain every requested Candidate Type and field as an independent pair after exact fresh-export mapping. |
| 2 | Resolve user-facing values | Resolve the current and proposed values through the active Common Lookup and keep lookup codes internal. |
| 3 | Validate every requested pair | Validate the exact Candidate Type, field, mapping, and active user-facing value independently; retain both successful and blocked results for the combined preview. |
| 4 | Build one combined preview | Include every requested pair using the required five-column preview and exact Candidate Type names. |
| 5 | Preserve atomic shared execution | Continue to approval and import only when every requested pair is valid; never import only the successfully validated subset. |

## Updates to Candidate Info Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An Updates to Candidate Info pair is processed | Blocker | verify_candidate_info_update_setting_mappings | The Candidate Type and field pair does not have exactly one fresh current full-task export mapping for its documented setting code. | Stop only the affected pair and explain the evidence gap; do not guess, substitute, append, or select a duplicate row. | No |
| A Candidate Type is displayed, validated, or previewed | Blocker | | The name is not exactly Contingent Worker, Ex-Contingent Worker, Ex-Employee, or Additional Person Types, or the output uses an acronym or calls Candidate Types populations. | Rebuild the result with the exact documented Candidate Type name. | Yes |
| An Updates to Candidate Info value is displayed or previewed | Blocker | resolve_candidate_info_update_allowed_values | The current value, proposed value, or permitted values contain a lookup code or were not resolved to one of the four active documented Common Lookup meanings. | Resolve through the active Common Lookup and display only None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal. | Yes |
| Multiple Updates to Candidate Info changes are requested | Blocker | | The combined preview omits a requested pair or uses columns other than Candidate Type, Field, Current Value, Proposed Value, and Change Status. | Rebuild one combined preview containing every requested pair in the required column order. | Yes |
| Any requested Updates to Candidate Info pair is blocked | Blocker | | Approval or import would include only the successfully validated subset, or any package would be imported before all requested pairs pass. | Preserve every result in the combined preview, stop approval and import, and request corrections for the blocked pairs. | No |
| An Updates to Candidate Info workflow is prepared | Blocker | | A direct REST, browser, FSM-save, CSV-import, loader, Fusion-update, or other fallback is proposed outside the existing shared workflow. | Stop the fallback and continue only through the existing current-export, Common Lookup, validation, combined-preview, approval, and import workflow. | No |

## Candidate Sourcing Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve exact setting identity | Resolve each requested UI label to exactly one of the eight authoritative setting codes in a fresh current full-task ORA_IRC_SETTING.csv export. |
| 2 | Apply the conditional default | Add Job Category only when Enable Talent Community is proposed as Y and the attributes field is omitted from the same modification. |
| 3 | Enforce the Talent Community dependency | Require Talent Community to be enabled in the final state before attributes or Global Talent Community Pool visibility can proceed. |
| 4 | Validate retained fields | Enforce the exact Boolean, whole-number range, and Talent Community attributes contracts without inferring missing values. |
| 5 | Classify the execution route | Send CSV-eligible rows to the existing guarded workflow, Global Talent Community Pool Visible = Y to the documented FSM/ADF UI save action, and mixed requests to an explicit split-route decision. |
| 6 | Build the combined preview | Use UI labels as the primary field display, retain codes only for traceability, and show every requested field and its route or blocked status. |

## Candidate Sourcing Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Candidate Sourcing field is read, previewed, or modified | Blocker | verify_candidate_sourcing_setting_mappings | The field lacks exactly one fresh ORA_IRC_SETTING.csv row for its authoritative setting code, or its current value is inferred. | Stop only the affected field, explain the evidence gap, and use no guessed, substituted, appended, or duplicate row. | No |
| Candidate Sourcing output is produced | Blocker | | A setting code replaces the documented UI label as the primary display value. | Rebuild the output with the exact UI label in the Field column and retain the code only as traceability evidence. | Yes |
| Talent Community attributes or Global Talent Community Pool visibility is processed | Blocker | verify_candidate_sourcing_setting_mappings | Talent Community is disabled in the final state, or the final state cannot be established from a valid proposed value or exact fresh-export current value. | Enable Talent Community in the same request or remove the dependent field; never infer the final state. | No |
| Global Talent Community Pool Visible = N is proposed | Error | | The value is rejected solely because it disables visibility or is routed to the manual enablement action. | Keep N as a valid CSV-importable value after normal mapping, dependency, validation, preview, and approval checks. | Yes |
| Global Talent Community Pool Visible = Y is proposed | Blocker | | A CSV row, partial CSV package, or completed-update claim is prepared for Y. | Do not import Y. Require the documented Candidate Sourcing FSM/ADF UI save action to enable or create the Global Talent Community Pool. | No |
| A Candidate Sourcing request mixes Global Talent Community Pool Visible = Y with CSV-eligible changes | Blocker | | The manual-only field is silently removed and the remaining CSV subset proceeds, or all fields are put into one CSV package. | Show the UI-only and CSV routes separately and require an explicit decision before either route proceeds. | No |
| A Candidate Sourcing combined preview is produced | Blocker | | A requested field is omitted, the UI label is not primary, or the execution route and blocked status are unclear. | Rebuild one combined preview containing every requested field and clearly distinguish CSV-ready, FSM/ADF UI required, and blocked items. | Yes |

## Campaigns Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve exact setting identity | Resolve every requested Campaigns field to exactly one of the seven documented setting codes using permitted ORA_IRC_SETTING.csv export evidence. |
| 2 | Resolve duration meanings | When Recent-campaign exclusion duration is in scope, resolve the current and proposed values through active Common Lookup ORA_IRC_CAMP_EMAIL_CAP_UNITS and keep LookupCode internal. |
| 3 | Validate the complete request | Enforce the documented generation-method enum, digits-only starting value, Boolean values, nonnegative numeric retry count, and active duration meaning. |
| 4 | Build the Campaigns preview | Use the task's standard Field, Current Value, Proposed Value, and Supported Values columns and preserve the documented Campaign Settings display order. |
| 5 | Preserve the shared workflow | Continue only through the existing export, validation, preview, approval, import, and verification workflow. Do not import a partial Campaigns package. |

## Campaigns Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Campaigns field is read, previewed, or modified | Blocker | verify_campaign_setting_mappings | The field lacks exactly one permitted-export row for its documented setting code, its current value is inferred, or a modification does not use a fresh current full-task export. | Obtain the required export and resolve every requested field exactly; do not infer, substitute, append, or select a duplicate row. | No |
| Recent-campaign exclusion duration is displayed, previewed, or modified | Blocker | resolve_campaign_email_cap_unit | The value is not one enabled current Meaning from ORA_IRC_CAMP_EMAIL_CAP_UNITS, an undocumented lookup result is accepted, or a LookupCode is shown as the user-facing value. | Resolve exactly 1 week, 2 weeks, or 1 month through the Common Lookup provider, display the Meaning, and keep the verified code internal. | Yes |
| A Campaigns setting value is processed | Blocker | | The value violates its documented enum, digits-only, Boolean, numeric-minimum, or lookup-backed contract. | Stop the complete Campaigns request and request valid values for every affected field. | Yes |
| Multiple Campaigns changes are requested | Blocker | | Preview, approval, or import omits an invalid requested field or proceeds with only a validated subset. | Preserve every requested field in one result and continue only after the complete Campaigns request passes. | No |
| A Campaigns preview is produced | Blocker | | The preview omits a requested field, changes the documented display order, or uses columns other than Field, Current Value, Proposed Value, and Supported Values. | Rebuild one ordered preview using the task's standard Campaigns columns. | Yes |
| A Campaigns workflow is prepared | Blocker | | A direct REST, browser, FSM-save, ad hoc CSV import, loader, or Fusion-update fallback is proposed outside the existing shared workflow. | Stop the fallback and return to the existing export, validation, preview, approval, import, and verification workflow. | No |

## Candidate Search Archiving Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve exact setting identity | Require one exact fresh-export mapping for ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED. |
| 2 | Enforce user-facing values | Accept and display only Enabled or Disabled while retaining the corresponding stored value internally. |
| 3 | Build the required preview | Show Candidate Search Archiving with Field, Current Value, Proposed Value, and Change Status in that order. |
| 4 | Preserve the shared workflow | Continue only through the existing combined-preview, approval, and import workflow without another execution route or fallback. |

## Candidate Search Archiving Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Candidate Search Archiving is processed | Blocker | verify_candidate_search_archiving_setting_mapping | The fresh current full-task export does not contain exactly one row for ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED. | Stop only Candidate Search Archiving and explain the missing or duplicate mapping evidence; do not guess, substitute, append, or select a row. | No |
| Candidate Search Archiving is displayed or previewed | Blocker | | The current value, proposed value, or permitted values expose Y, N, or another stored code instead of Enabled or Disabled. | Rebuild the output using Enabled or Disabled only. | Yes |
| A Candidate Search Archiving preview is produced | Blocker | | The preview omits the field or uses columns other than Field, Current Value, Proposed Value, and Change Status. | Rebuild the preview in the required column order with user-facing values only. | Yes |
| A Candidate Search Archiving workflow is prepared | Blocker | | A direct REST, browser, FSM-save, CSV-import, loader, Fusion-update, or other fallback is proposed outside the existing shared workflow. | Stop the fallback and continue only through the existing current-export, validation, combined-preview, approval, and import workflow. | No |

## AI Features Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve supported mappings | Use a fresh current full-task export to resolve only the six supported or conditionally supported AI Features setting codes. |
| 2 | Validate scalar inputs | Validate decimal importance values as one exact-sum group, numeric Maximum summaries per day, Y or N candidate suggestions, and the exact preserved Selected countries representation. |
| 3 | Enforce migration exclusions | Prevent every Not supported field and migration-view-excluded code from generating an import row. |
| 4 | Enforce generic setting structure | For eligible scalar rows, use ORA_IRC_SETTING_CODE/XML Code as identity and ORA_IRC_STRING_VALUE/XML StringValue as value. |

## AI Features Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An AI Features scalar row is proposed | Error | verify_ai_features_setting_mappings | Its code is not ORA_IRC_AI_SNIPPET_EDUCATION_SCORE, ORA_IRC_AI_SNIPPET_SKILL_SCORE, ORA_IRC_AI_SNIPPET_EXPERIENCE_SCORE, ORA_IRC_AI_MAX_NUMBER_OF_SUMMARIES_PER_DAY, ORA_IRC_AI_MATCHING_ENABLED, or conditionally ORA_IRC_AI_EXCLUDED_COUNTRIES, or its exact fresh-export mapping is unavailable. | Generate only an exact-mapped supported row; do not guess, substitute, or append a setting code. | No |
| Enable job application highlights or Enable job application rating is requested | Error | | A setting row or inferred code is proposed. | Report the field as Not supported and omit it from the import artifact because no direct setting code is proven. | Yes |
| ORA_IRC_AI_SIMILAR_CANDIDATE, ORA_IRC_AI_EXCLUDED_COUNTRIES_ENABLED, ORA_IRC_AI_JOBS2CANDIDATE_ENABLED, ORA_IRC_AI_JOBS2JOBS_ENABLED, or ORA_IRC_AI_TIME_TO_HIRE_ENABLED is requested in AI Features | Error | | An import row is proposed for a code excluded by the standard migration view. | Report the field as Not supported and do not generate or import its row. | Yes |
| ORA_IRC_AI_EXCLUDED_COUNTRIES is retained as a standalone value | Error | verify_ai_features_setting_mappings | The fresh-export value is blank, missing, duplicated, constructed, translated, or simplified. | Preserve only the exact nonblank fresh-export representation. Do not infer or manually author the country list. | No |
| ORA_IRC_AI_EXCLUDED_COUNTRIES is retained | Warning | verify_ai_features_setting_mappings | | State that retaining the standalone country-list value does not make Hide suggestions in selected countries importable because ORA_IRC_AI_EXCLUDED_COUNTRIES_ENABLED remains unsupported. | No |
| A supported AI Features scalar row is generated | Error | | Identity or value uses anything other than ORA_IRC_SETTING_CODE/XML Code and ORA_IRC_STRING_VALUE/XML StringValue. | Rebuild the row with the existing generic settings import/export structure. | Yes |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify selected section | Determine whether the requested configuration is an IRC setting, an excluded scope, a data-retention configuration, or an integration. |
| 2 | Resolve references and prerequisites | Verify Requisition Number Generation Method against ORA_IRC_REQ_GEN_METHOD, Offer profile-option prerequisites, and Offer collaborator types only when their dependent fields are supplied. Require the documented manual Move to HR dependency and Agency Hiring Security Console verification when those fields are supplied. |
| 3 | Apply migration limits | Prevent a CSV workflow from being treated as a complete configuration where the source identifies excluded, unsupported, REST-only, or secure target-environment state. |
| 4 | Require FSM completion where documented | Complete and validate the configuration in FSM where the source requires direct target-environment entry or save behavior. |
| 5 | Validate Recruiting Management archive | Before preview or import, require every retained ORA_IRC_SETTING.csv child update to have exactly one unchanged matching parent row from the same fresh export. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Recruiting Management is selected | Error | | RECRUITING_ORG_TREE_CODE is included while its Manage Org Tree dependency is unavailable. | Exclude RECRUITING_ORG_TREE_CODE until the Manage Org Tree dependency is available. Do not infer or substitute another setting. | Yes |
| Recruiting Management is selected | Error | | IRC_TREAT_CWK_AS_EXTERNAL is included in a classic import or export. | Exclude IRC_TREAT_CWK_AS_EXTERNAL because classic import/export does not handle it. | Yes |
| Activity Center is requested | Error | | The setting is proposed in this task. | Exclude Activity Center because it belongs to another setup task. | Yes |
| Candidate Sourcing, Interview Intelligence, or Campaigns is selected | Warning | | | Use the supported FSM CSV route where that route is documented for the selected setting. Do not invent CSV support for another setting. | Yes |
| Data Purging is selected | Error | | A CSV migration is proposed for this setting. | Do not treat Data Purging as CSV-supported; validate the documented ENTITY_NAME and ACTIVE_DAYS constraints before choosing a supported route. | Yes |
| Campaign Email Metrics retention is selected | Error | | ENTITY_NAME does not identify irc_cmt_recipients. | Require ENTITY_NAME=irc_cmt_recipients before proceeding through a supported non-CSV route. | Yes |
| Campaign Email Metrics retention is selected | Error | | ACTIVE_DAYS is not an integer from 180 through 1000 inclusive. | Require an integer from 180 through 1000. | Yes |
| Microsoft Graph Integration is selected | Blocker | | Any CSV modification is proposed, including a partial non-secret update. | Return `FSM_REQUIRED`; enter, validate, and save the integration directly in the target environment through FSM, and do not include or retain application credentials in artifacts. | No |
| Google Workspace Integration is selected | Blocker | | Any CSV modification is proposed, including a partial non-secret update. | Return `FSM_REQUIRED`; activate the required privacy-policy content and complete authorization, save, and validation in FSM because CSV does not provision credential-store, authorization-token, or refresh-token state. | No |
| Zoom Integration is selected | Blocker | | Any CSV modification is proposed, including a partial non-secret update. | Return `FSM_REQUIRED`; use FSM Save and integration validation, and do not include or retain client credentials in artifacts. | No |
| A section field list is displayed | Error | | The response mixes columns from different display states or includes a Not supported field. | Use exactly the table shape for the requested display state and hide fields marked Not supported. | Yes |
| A Print to PDF field is proposed | Error | | The fresh export does not contain the exact documented Print to PDF setting code. | Stop only the affected field and explain the evidence gap; never guess the setting code. | No |
| A Document Types row is proposed | Error | | `SystemDocumentType` is inferred, changed for an existing row, or duplicated. | Use only the exact exported or existing-list identity; stop the affected row when it cannot be established. | No |
| A Document Types name is displayed | Error | get_ghr_document_type_name | The GHR lookup returns zero or multiple exact matches for the exported `SystemDocumentType`, or a display name is used as the import identity. | Retain `SystemDocumentType` as the identity. Do not infer a name; mark only the affected displayed name unresolved and explain the evidence gap. | No |
| A Document Types import is proposed | Error | resolve_ghr_document_type_for_import | The supplied system type or GHR document type name does not resolve to one active GHR document, or the resolved system type already appears in the fresh Recruiting export. | Stop only the affected document type. Use the exact resolved `SystemDocumentType` only after all eligibility checks pass. | No |
| A Document Types Requires validation value is proposed | Error | | The fresh export does not confirm the exact verification-flag header. | Stop only the affected row; use the exact target-export header rather than guessing between `VerificationRequiredFlag` and `ValidationRequiredFlag`. | No |
| A Document Types Active value is proposed | Error | | The artifact attempts to activate a document type. | Do not generate an activation import value. The import forces inactive; activate through the page UI after import. | No |
| A Document Types system-managed attribute is proposed | Error | | `CategoryId` or `CategoryName` is authored, preserved, or manually modified. | Omit the attribute; the import resets CategoryId and UI activation derives CategoryName. | No |
| A field explicitly marked Not supported is proposed | Error | | An import row is proposed for the field. | Do not generate or import the row. | No |
| An Offer setting row is proposed | Error | | The setting code differs from the exact field-to-code mapping in ora_input_validation.md. | Use only one of the twelve documented Offer setting codes and its mapped value rule; do not infer or substitute another code. | No |
| An Offer setting is absent from the task's approved fresh FSM export/import files or requires a REST/API operation | Error | | A CSV import is proposed for the setting. | Do not attempt the CSV import. Tell the user the value must be changed manually in Fusion, identify the setting and the Enterprise Recruiting and Candidate Experience Information > Offer navigation, and do not report it as updated until the manual action is confirmed. | No |
| All collaborator types is proposed | Error | | ORA_IRC_OFFER_COLLABORATORS_TO_COPY is not mapped directly to ALL. | Store ALL exactly; do not run a collaborator lookup or infer another value. | Yes |
| Specific collaborator types are proposed | Error | resolve_offer_collaborator_types | The resolver does not return one complete ordered StringValue for the supplied selection, or a partial result is retained after resolver failure. | Reject the complete selection unless the resolver succeeds, then use its returned StringValue without substitution. | No |
| None is proposed for collaborator types | Error | resolve_offer_collaborator_none_representation | A fresh export or task metadata does not establish the exact stored CSV representation. | Do not guess a blank or stored value. Use the manual Fusion action when the representation cannot be established. | No |
| Include as Potential Duplicates is proposed | Error | | The setting code is not ORA_IRC_OFFER_DUPCHECK_PERSON_TYPES or the value is not ALL or ORA_RECRUITING. | Use only ORA_IRC_OFFER_DUPCHECK_PERSON_TYPES. Map All person types to ALL and Only person types supported in Recruiting to ORA_RECRUITING. | Yes |
| Duplicate Check in Move to HR is proposed | Error | | A CSV setting code or import row is proposed, or the setting is routed to the common Profile Option Values skill. | Do not invent a setting code or import value. Complete the setting manually in Fusion and apply the Enterprise HCM Information: Person Creation Duplicate Check dependency. | No |
| An Agency Hiring Boolean setting is proposed | Error | | The value is anything other than Y or N. | Require Y or N before preview or CSV generation. | Yes |
| An Agency Hiring setting row is proposed | Error | | The setting code differs from the exact field-to-code mapping in ora_input_validation.md or is not one of the five documented Agency Hiring codes. | Use only the documented Agency Hiring setting code for that field; do not infer or substitute another code. | No |
| Agent User Category or Agent Role is proposed | Error | | The supplied code is unknown or has not been manually verified in the target Security Console. | Stop before preview with MANUAL_INTERVENTION_REQUIRED. Require the verified target code; do not invent a value or create Security Console master data. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_ai_features_setting_mappings | Any supported or conditionally supported AI Features field is read, previewed, or modified | Exact fresh-export mapping, current StringValue, row identity, importance-group completeness, and exact nonblank standalone country-list representation when applicable | ora_reference_lookups.md |
| verify_requisition_number_generation_method | REQUISITION_NUMBER_GENERATION_METHOD remains after exact fresh-export mapping and input validation | Exactly one accepted LookupCode and its Meaning from ORA_IRC_REQ_GEN_METHOD | ora_reference_lookups.md |
| get_ghr_document_type_name | A Document Types list or current-value response is requested | Exact `DocumentType` name for one exported `SystemDocumentType` | ora_reference_lookups.md |
| resolve_ghr_document_type_for_import | A Document Types import is requested | Exact GHR identity, active status, creation eligibility, and fresh Recruiting duplicate evidence | ora_reference_lookups.md |
| resolve_offer_collaborator_types | One or more specific collaborator labels or codes are supplied for ORA_IRC_OFFER_COLLABORATORS_TO_COPY | One enabled current LookupCode for every selection, preserved in requested order | ora_reference_lookups.md |
| resolve_offer_collaborator_none_representation | None is supplied for ORA_IRC_OFFER_COLLABORATORS_TO_COPY | Exact stored CSV representation for clearing all collaborator types | ora_reference_lookups.md |
| verify_active_candidate_filter_setting_mappings | Any Configure Active Candidate Filter field is read, previewed, or modified | Exact fresh current full-task export mapping and current internal value for every requested field | ora_reference_lookups.md |
| resolve_active_candidate_timeframe_meanings | Activity Timeframe is requested, displayed, previewed, or modified | Current meaning, proposed meaning, permitted active meanings, and an internal resolved code that is never displayed | ora_reference_lookups.md |
| verify_candidate_info_update_setting_mappings | Any Updates to Candidate Info Candidate Type and field pair is read, previewed, or modified | Exact fresh current full-task export mapping and current internal value for every requested pair | ora_reference_lookups.md |
| resolve_candidate_info_update_allowed_values | Any Updates to Candidate Info value is requested, displayed, previewed, or modified | Current meaning, proposed meaning, permitted active meanings, and an internal resolved code that is never displayed | ora_reference_lookups.md |
| verify_candidate_search_archiving_setting_mapping | Candidate Search Archiving is read, previewed, or modified | Exact fresh current full-task export mapping and current stored value for ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED | ora_reference_lookups.md |
| verify_candidate_sourcing_setting_mappings | Candidate Sourcing is read, previewed, or modified, or its final Talent Community state must be established | Exact authoritative mapping, exported current value, row identity, and final Talent Community state evidence for every applicable field | ora_reference_lookups.md |
| verify_campaign_setting_mappings | Campaigns is read, previewed, or modified | Exact mapping, current value, exported row identity, operation type, and permitted export provenance for every requested Campaigns field | ora_reference_lookups.md |
| resolve_campaign_email_cap_unit | Recent-campaign exclusion duration is displayed, previewed, or modified | Current and proposed active user-facing Meaning, permitted active Meanings, and internal verified LookupCode | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| II.ENFORCE_DESIGN | decision | 5 | design_enforcement | ready->II.DATALOADER_HANDOFF_GATE;no_change->II.NO_CHANGE;blocked->II.BLOCKED | II.CHECK_DEPENDENCIES | stop | Validated Interview Intelligence inputs and applicable readiness checks are complete; apply mandatory Companion and streaming child resets before comparing the complete final change set with the export. |
| CAND_AUTH.ENFORCE_CREDENTIAL_BOUNDARY | decision | 18 | design_enforcement | compliant->CAND_AUTH.READY_FOR_CSV_WORKFLOW;blocked->CAND_AUTH.BLOCKED | CAND_AUTH.VALIDATE_INPUT | stop | Enforce the three-setting CSV allowlist and prevent Candidate Authenticity credentials from entering artifacts, previews, logs, diagnostics, or runtime output. |
| IRC.ENFORCE_CONFIGURATION_MIGRATION | decision | 90 | design_enforcement | compliant->IRC.VALIDATE_RECRUITING_MANAGEMENT_ARCHIVE;blocked->IRC.RETURN_ISSUES | none | stop | A configuration section reaches migration enforcement from either the Recruiting Management lookup path or the existing configuration dependency path. |
| ACF.ENFORCE_DISPLAY_AND_WORKFLOW | decision | 45 | design_enforcement | compliant->ACF.READY_FOR_SHARED_WORKFLOW;blocked->ACF.BLOCKED | ACF.VALIDATE_INPUT | stop | Enforce separate event fields, user-facing values only, the required combined preview, and exclusive use of the existing approval and import workflow. |
| UCI.ENFORCE_PREVIEW_AND_WORKFLOW | decision | 53 | design_enforcement | all_valid->UCI.READY_FOR_SHARED_WORKFLOW;blocked->UCI.BLOCKED | UCI.VALIDATE_INPUT | stop | Enforce exact Candidate Type names, user-facing lookup meanings only, one combined preview for every requested pair, atomic import, and exclusive use of the existing shared workflow. |
| CSA.ENFORCE_DISPLAY_AND_WORKFLOW | decision | 60 | design_enforcement | compliant->CSA.READY_FOR_SHARED_WORKFLOW;blocked->CSA.BLOCKED | CSA.VALIDATE_INPUT | stop | Enforce user-facing Enabled or Disabled values, the required Candidate Search Archiving preview, and exclusive use of the existing approval and import workflow. |
| CAND_SRC.ENFORCE_WORKFLOW | decision | 68 | design_enforcement | csv_ready->CAND_SRC.READY_FOR_SHARED_WORKFLOW;fsm_ui_required->CAND_SRC.FSM_UI_REQUIRED;mixed_action_required->CAND_SRC.MIXED_ACTION_REQUIRED;blocked->CAND_SRC.BLOCKED | CAND_SRC.VALIDATE_INPUT | stop | Enforce UI-label-first output, Talent Community dependency, CSV support for Global Talent Community Pool Visible = N, the manual FSM/ADF UI route for Y, and explicit separation of mixed requests. |
| CAMP.ENFORCE_WORKFLOW | decision | 77 | design_enforcement | compliant->CAMP.READY_FOR_SHARED_WORKFLOW;blocked->CAMP.BLOCKED | CAMP.VALIDATE_INPUT | stop | Enforce exact Campaigns mappings, active duration meanings, documented display order, complete-request preview, and exclusive use of the existing guarded workflow. |
| AI_FEATURES.ENFORCE_MIGRATION | decision | 96 | design_enforcement | compliant->AI_FEATURES.READY_FOR_SHARED_WORKFLOW;blocked->AI_FEATURES.BLOCKED | AI_FEATURES.VALIDATE_INPUT | stop | Enforce the six-code AI Features allowlist, migration-view exclusions, exact standalone country preservation, and generic setting identity/value structure before shared workflow handoff. |
