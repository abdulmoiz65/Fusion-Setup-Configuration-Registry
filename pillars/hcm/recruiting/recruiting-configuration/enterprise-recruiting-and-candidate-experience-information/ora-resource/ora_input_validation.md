# Input Validation

## Interview Intelligence Setting Mapping

| User Field | Setting Code | Accepted Input | CSV Value |
|---|---|---|---|
| Enable interview loop scheduling | ORA_IRC_IS_LOOP_INTERVIEW_AGENT_ENABLED | Boolean, Y, or N | Y or N |
| Interview Companion | ORA_IRC_IS_INTERVIEW_COMPANION_ENABLED | Boolean, Y, or N | Y or N |
| Enable interview insights using interview transcript | ORA_IRC_INTEVIEW_INSIGHTS_ENABLED | Boolean, Y, or N | Y or N |
| Enable draft feedback using interview transcript | ORA_IRC_DRAFT_FEEDBACK_RESPONSE_ENABLED | Boolean, Y, or N | Y or N |
| Enable real-time meeting streaming | ORA_IRC_IS_REALTIME_STREAMING_ENABLED | Boolean, Y, or N | Y or N |
| Words per Agent Invocation | ORA_IRC_IS_RTMS_MIN_TRANSCRIPT_WORDS | Blank or an integer greater than or equal to 50 | Blank or the supplied base-10 integer |

Use the released setting code `ORA_IRC_INTEVIEW_INSIGHTS_ENABLED` exactly,
including its spelling.

## Integration Reporting Mappings

These mappings support read-only reporting. They do not authorize CSV changes
for Microsoft Graph, Google Workspace, or Zoom.

### Microsoft Graph Integration

| UI or report field | Exported setting code | Reporting rule |
|---|---|---|
| Access Type | ORA_IRC_O365_GRAPH_API_ACCESS_TYPE | Display the exported value |
| Default User Identifier | ORA_IRC_O365_DEFAULT_ADMIN_USER_IDENTIFIER | Display the exported value |
| Calendar Name | ORA_IRC_O365_CALENDAR_NAME | Display the exported value |
| Application Authentication Type | ORA_IRC_O365_AUTHENTICATION_TYPE | Display the exported value |
| Meeting Room Access | ORA_IRC_O365_MEETING_ROOM_ACCESS_ENABLED | Display Y, N, or blank exactly as exported |
| Enable Teams | ORA_IRC_IS_ENABLE_TEAMS | Display Y, N, or blank exactly as exported |
| Use Default Endpoints | ORA_IRC_GRAPH_API_CUSTOM_ENDPOINTS_USE_DEFAULT | Display Y, N, or blank exactly as exported |
| Microsoft Entra ID Endpoint | ORA_IRC_GRAPH_API_CUSTOM_LOGIN_URL | Display the exported endpoint only |
| Microsoft Graph Endpoint | ORA_IRC_GRAPH_API_CUSTOM_GRAPH_URL | Display the exported endpoint only |

The inspected CSV contract has no dedicated rows for the Microsoft Graph
**Enable Calendar Integration** state, Application ID, Tenant ID, or
Application Password. Report those fields as unavailable from the CSV export
and do not infer their values from other rows.

### Google Workspace Integration

| UI or report field | Exported setting code | Reporting rule |
|---|---|---|
| Enable Calendar Integration | ORA_IRC_GOOGLE_CALENDAR_ENABLED | Display Y, N, or blank exactly as exported |
| Authentication Type | ORA_IRC_GOOGLE_CALENDAR_AUTHENTICATION_TYPE | Display the exported value |
| Calendar Name | ORA_IRC_GOOGLE_CALENDAR_NAME | Display the exported value |
| Enable Google Meet | ORA_IRC_IS_ENABLED_GOOGLE_MEET | Display Y, N, or blank exactly as exported |
| Use Default Endpoints | ORA_IRC_GOOGLE_CUSTOM_ENDPOINTS_USE_DEFAULT | Display Y, N, or blank exactly as exported |
| Google API Endpoint | ORA_IRC_GOOGLE_API_ENDPOINT | Display the exported endpoint only |
| Google Authorization Endpoint | ORA_IRC_GOOGLE_AUTH_ENDPOINT | Display the exported endpoint only |
| Google Token Endpoint | ORA_IRC_GOOGLE_TOKEN_ENDPOINT | Display the exported endpoint only |
| Last Granted Date | ORA_IRC_GOOGLE_LAST_GRANTED_DATE | Display the exported date or blank; it is not proof of a currently valid authorization |

The CSV does not contain the authorization or refresh token and cannot prove
that the required Google Workspace Integration privacy-policy content is
active.

### Zoom Integration

| UI or report field | Exported setting code | Reporting rule |
|---|---|---|
| Active | ORA_IRC_IS_ENABLE_ZOOM | Display Y, N, or blank exactly as exported |
| Client ID | ORA_IRC_ZOOM_CLIENT_ID | Report only `populated` or `not populated`; never display the exported value |
| Client Secret | ORA_IRC_ZOOM_CLIENT_SECRET | Report only `populated` or `not populated`; never display the exported value |

## Integration Reporting Validation

| Check | Required behavior |
|---|---|
| Missing exported row | Report the field as unavailable from the current export; do not append a row or infer a value |
| Duplicate exported row | Report a catalog or metadata mismatch and stop section reporting until a valid export is supplied |
| Secret-like row | Return only presence status and never return the StringValue |
| Enablement wording | Describe the value as an exported configuration value, not proof that the integration is enabled, authenticated, validated, or ready |
| Integration modification request | Return `FSM_REQUIRED`; do not modify CSV files, create a ZIP, or invoke Data Loader |

## Read Freshness Request Contract

| Request form | Export-source result | Required behavior |
|---|---|---|
| Ordinary `show`, `read`, or `list` request | Reuse allowed | Use `find_reusable_section_export`; report from the latest valid matching completed export when available |
| Request includes `current`, `live`, `fresh`, `refresh`, `re-export`, or `latest` | Refresh required | Do not reuse cached evidence; hand off to `shared.setup-export.task-level-export` |
| No valid matching completed export exists | Refresh required | Hand off to `shared.setup-export.task-level-export` before section reporting |
| Interview Intelligence modification request | Mutation export required | Use an export produced for the current mutation workflow; do not repeat the export when that workflow already produced one |

## Interview Intelligence Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Current mutation export | A successful export produced for the current mutation workflow for task ORA_IRC_MANAGE_ENTERPRISE_RECRUITING_AND_CANDIDATE_EXPERIENCE_INFORMATION containing ORA_IRC_SETTING.csv and ORA_IRC_SETTING_VALUE.csv | Stop | Run `shared.setup-export.task-level-export`, record its sanitized export evidence, and then prepare the change | Any Interview Intelligence change | |
| Setting request | At least one supported Interview Intelligence field and its requested value | Stop | Supply the field to change and its intended value | Any Interview Intelligence change | |
| Recruiting Booster lookup context | Exact target `restBaseUrl` and target-matching Fusion OAuth properties sufficient for `core.fusion-api.rest-api-client` to run the versioned Features item GET | Stop | Supply the target environment configuration; `II.CHECK_BOOSTER` performs the fresh lookup before package preparation | Any Interview Intelligence change | verify_recruiting_booster_enabled |
| REST API version | Optional literal `latest` or a four-part numeric version such as `11.13.18.05`; default `latest` | Stop on any value containing braces, slashes, whitespace, or another format | Resolve the value before constructing the Features item path; the core REST client does not substitute endpoint templates | Any Interview Intelligence change | verify_recruiting_booster_enabled |
| Calendar integration readiness | availableCalendarIntegrations containing MICROSOFT_GRAPH or GOOGLE_CALENDAR, supplied in caller-provided task context | Stop | Supply an accepted calendar integration | Enabling interview loop scheduling | |

## Interview Intelligence Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A fresh same-target Booster response returns HTTP 200, exact `FeatureCode=ORA_IRC_ADVANCED_RECRUITING`, and `EnabledFlag=Y` | Valid | Continue with the remaining validation for the requested Interview Intelligence change | verify_recruiting_booster_enabled |
| The Booster response is disabled, missing, mismatched, stale, unauthorized, malformed, or from another environment | Invalid | Stop before modifying or importing any Interview Intelligence setting | verify_recruiting_booster_enabled |
| Enabling interview loop scheduling and an accepted calendar integration is available | Valid | Continue package preparation | |
| Enabling interview loop scheduling and no accepted calendar integration is available | Invalid | Stop before applying the loop scheduling change | |
| Interview loop scheduling is unchanged or disabled | Valid | Continue without requiring calendar integration readiness | |

## Events Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Complete Events settings | ORA_IRC_EVENTS_APPLIED_METRICS_DAYS and ORA_IRC_EVENTS_HIRED_METRICS_DAYS | Stop | Supply both mandatory settings as whole numbers from 1 through 999 | An Events modification is requested | |

## Events Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A fresh same-target Advanced Recruiting response confirms ORA_IRC_ADVANCED_RECRUITING is enabled | Valid | Evaluate the complete Events request as one atomic validation unit | verify_events_advanced_recruiting_enabled |
| Advanced Recruiting is disabled, unavailable, unauthorized, unsupported, or indeterminate | Invalid | Stop before Events export, input validation, setup-data validation, or import | verify_events_advanced_recruiting_enabled |

## Candidate Authenticity Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Complete Candidate Authenticity settings | ORA_IRC_CAND_AUTH_ENDPOINT_URL, ORA_IRC_CAND_AUTH_ACCESS_TOKEN_URL, and ORA_IRC_CAND_AUTH_AGENT_SCOPE | Stop | Identify every missing or blank field and ask the user to supply a valid nonblank value for each one | A Candidate Authenticity Settings modification is requested | |

## Candidate Authenticity Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The configured Site-level value for ORA_IRC_CANDIDATE_AUTHENTICITY_AGENT_ENABLED is exactly Y | Valid | Validate the complete three-setting request as one atomic unit | verify_candidate_authenticity_profile_option_enabled |
| The configured Site-level value is N, blank, missing, unavailable, or unreadable | Invalid | Stop before input validation or import and tell the user that Candidate Authenticity must be enabled before its settings can be updated | verify_candidate_authenticity_profile_option_enabled |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Interview Intelligence Boolean setting value | Normalize true or Y to Y and false or N to N; reject every other value. | Any Interview Intelligence checkbox field is supplied. | |
| Words data type | Accept blank or a base-10 integer; reject decimals, negative numbers, signs without digits, and nonnumeric text. | Words per Agent Invocation is supplied. | |
| Words minimum | Accept 50 or greater with no maximum; reject an integer below 50. | A nonblank Words per Agent Invocation value is supplied. | |
| Interview Intelligence setting CSV headers | Require ORA_IRC_SETTING_VALUE.Code, StringValue, and SettingValueId in their exported order. | Validating the current mutation export or prepared package. | |
| Existing Interview Intelligence setting rows | Require exactly one existing row for every requested setting code and every mandatory child reset selected by design enforcement; reject a missing or duplicate code and do not append a row. | Preparing an Interview Intelligence setting change. | |
| Interview Intelligence metadata CSV | Require ORA_IRC_SETTING_VALUE.csv to remain byte-for-byte unchanged. | Preparing the import package. | |
| Interview Intelligence unrelated data | Require all rows outside requested applicable settings and mandatory child resets to remain unchanged; preserve codes, SettingValueId values, headers, quoting, and column order. | Preparing the import package. | |
| Interview Intelligence no-op evaluation | Defer the no-change decision to II.ENFORCE_DESIGN so the comparison includes its complete final change set. | After request normalization. | |
| Events mandatory values | Require nonblank values for both ORA_IRC_EVENTS_APPLIED_METRICS_DAYS and ORA_IRC_EVENTS_HIRED_METRICS_DAYS. | An Events modification is requested. | |
| Events whole-number syntax | Accept only base-10 digits representing a whole number; reject negative signs, decimal points, letters, symbols, and mixed text and numbers. | Either Events setting is supplied. | |
| Events range | Require each supplied Events value to resolve to a whole number from 1 through 999 inclusive; reject zero and values outside the range. | Either Events setting is supplied. | |
| Events atomic validation | Validate both mandatory Events settings together. If either value is missing or invalid, stop and ask for a valid whole number from 1 through 999; do not save, export, invoke downstream setup-data validation, or import either Events setting. | An Events modification is requested. | |
| Candidate Authenticity supported setting codes | Accept only ORA_IRC_CAND_AUTH_ENDPOINT_URL, ORA_IRC_CAND_AUTH_ACCESS_TOKEN_URL, and ORA_IRC_CAND_AUTH_AGENT_SCOPE. Reject the complete Candidate Authenticity request when another setting code or credential field is supplied. | A Candidate Authenticity Settings modification is requested. | |
| Candidate Authenticity mandatory values | Require all three supported fields and require each value to contain at least one non-whitespace character. Do not infer a value or apply URL-format validation that the source does not define. | A Candidate Authenticity Settings modification is requested after profile-option readiness succeeds. | |
| Candidate Authenticity atomic validation | Validate all three supported fields together. If any field is missing or blank, identify every invalid field, ask for a valid nonblank value, and do not create or import any Candidate Authenticity setting row. | A Candidate Authenticity Settings modification is requested after profile-option readiness succeeds. | |
| Candidate Authenticity credential input | Reject credential fields without reading, retaining, logging, previewing, or echoing their values. Direct credential maintenance only to the FSM setup UI. | A Candidate Authenticity Settings input contains a credential field. | |
| Candidate Experience Boolean value | Accept only Y or N. | Keep me signed in for external candidates, Candidate auto-confirmation, Verify last name and allow phone-number claim, Verify date of birth and allow email claim, Repeat blocks in request-information flows, Career-site search in requisition description, or Enable sitemap submission and job posting markup is supplied. | |
| Candidate Experience signed-in idle period | Accept only base-10 whole-number syntax from 0 through 90 inclusive. Reject blanks, signs, decimal points, characters, symbols, and mixed text and numbers. | Number of days to remain signed in is supplied. | |
| Candidate Experience validation population | Accept exactly Ex-Workers or All Candidates. | Apply validation to candidates is supplied. | |
| Candidate Experience Search Configuration URL | Accept blank or text containing no more than 1,000 characters. Do not impose a URL-format rule that the source does not define. | Search Configuration URL is supplied. | |
| Candidate Experience application-count tags | Require numeric input. Reject blank and nonnumeric input, but do not invent a whole-number rule, sign rule, decimal rule, minimum, or maximum that the source does not provide. | Be the First to Apply - Maximum Number of Applications or Trending - Minimum Number of Applications is supplied. | |
| Candidate Experience preview shape | Display exactly Field, Current Value, Proposed Value, and Change Status in that order. Include the per-field validation or exact-mapping result in Change Status. | Any Candidate Experience preview is displayed. | |
| Configure Active Candidate Filter Boolean meaning | Accept only the user-facing values Enabled or Disabled for Enable Candidate Activity and every event-specific activity setting. Convert Enabled to the internal enabled value and Disabled to the internal disabled value without displaying either internal value. Reject internal codes and every other input as user-facing values. | A Configure Active Candidate Filter Boolean field is supplied. | |
| Configure Active Candidate Filter timeframe meaning | Accept only one permitted user-facing meaning returned by the active Common Lookup. Keep the corresponding lookup code internal. | Activity Timeframe is supplied. | resolve_active_candidate_timeframe_meanings |
| Configure Active Candidate Filter independent changes | Accept one or multiple setting changes in the same request and validate every supplied field independently. A failure affects only that field when another field remains independently valid. | One or more Configure Active Candidate Filter settings are supplied. | |
| Configure Active Candidate Filter event-specific fields | Treat Applied for a Job, Attended an Event, Clicked an Email, Opened an Email, Registered for an Event, Responded to an Email, Responded to Request More Information, Responded to SMS, Responded to WhatsApp, Updated Job Alert Opt-In, Updated Marketing Opt-In, and Updated Talent Community Preferences as twelve separate fields. Reject an aggregated all-event-controls input. | Configure Active Candidate Filter settings are listed, validated, or previewed. | |
| Configure Active Candidate Filter preview shape | Display exactly Field, Current Value, Proposed Value, and Change Status in that order. Include every requested field separately and use only user-facing meanings and Enabled or Disabled values. | Any Configure Active Candidate Filter preview is displayed. | |
| Updates to Candidate Info Candidate Type | Accept exactly Contingent Worker, Ex-Contingent Worker, Ex-Employee, or Additional Person Types. Reject acronyms, aliases, and the term populations as Candidate Type input. | An Updates to Candidate Info change is supplied. | |
| Updates to Candidate Info field | Accept exactly Address, Email, Name, or Phone for each supplied Candidate Type. Resolve every Candidate Type and field pair independently. | An Updates to Candidate Info change is supplied. | |
| Updates to Candidate Info value | Accept only one active user-facing meaning returned for the documented Common Lookup, limited to None, Hiring App, Candidate Portal, and Hiring App and Candidate Portal. Keep the resolved lookup code internal. | An Updates to Candidate Info value is supplied. | resolve_candidate_info_update_allowed_values |
| Updates to Candidate Info multiple changes | Accept one or multiple Candidate Type and field pairs in one request. Preserve every successful validation result, but require every requested pair to pass before approval or import. | One or more Updates to Candidate Info changes are supplied. | |
| Updates to Candidate Info preview shape | Display exactly Candidate Type, Field, Current Value, Proposed Value, and Change Status in that order. Include every requested Candidate Type and field pair in one combined preview. | Any Updates to Candidate Info preview is displayed. | |
| Candidate Search Archiving value | Accept only the user-facing values Enabled or Disabled. Convert Enabled to the internal enabled value and Disabled to the internal disabled value without displaying either stored value. Reject Y, N, and every other value as user-facing input. | Candidate Search Archiving is supplied. | |
| Candidate Search Archiving preview shape | Display exactly Field, Current Value, Proposed Value, and Change Status in that order. Display current and proposed values only as Enabled or Disabled. | Any Candidate Search Archiving preview is displayed. | |
| Recruiting Management exact mapping | Require a fresh export of this exact task to contain exactly one child setting row and exactly one matching parent row for every retained Recruiting Management setting. Do not infer a setting code, parent row, default, persistence behavior, or import route. | A Recruiting Management field is read, previewed, or modified. | |
| Requisition number generation method | Accept only a lookup-verified exact code from ORA_IRC_REQ_GEN_METHOD: ORA_IRC_REQ_GEN_METHOD_AUTO or ORA_IRC_REQ_GEN_METHOD_MANUAL. Do not match by Meaning. | REQUISITION_NUMBER_GENERATION_METHOD is supplied. | verify_requisition_number_generation_method |
| Requisition number generation starting number | Require a numeric value greater than or equal to 0. Do not invent a whole-number requirement or upper bound. | REQUISITION_NUMBER_GENERATION_STARTING_NUMBER is supplied. | |
| Maximum unconfirmed submissions | Require a base-10 integer from 1 through 10 inclusive. | ORA_IRC_MAX_UNCONFIRMED_SUBS is supplied. | |
| Recruiting Management Boolean values | Accept only Y or N. | ORA_IRC_JA_WITHDRAW_REAPPLY, ORA_IRC_JA_PREFILL_LEG_INFO, or ORA_IRC_JA_PREFILL_QSTNR_INFO is supplied. | |
| Recruiting Management independent validation | Validate each supplied setting independently. Skip only an invalid setting and disclose its code, supplied value, and reason; for an invalid generation method also disclose both accepted codes. | One or more Recruiting Management settings are supplied. | |
| Recruiting Management preview shape | Display exactly Field, Current Value, Proposed Value, and Change Status in that order. | Any Recruiting Management preview is displayed. | |
| Recruiting Management archive parent relationship | For every retained ORA_IRC_SETTING.csv child update, require exactly one matching ORA_IRC_SETTING_VALUE.csv parent where parent Code equals child ORA_IRC_SETTING_VALUE.Code. Copy the complete matching parent row unchanged from the same fresh task export. | A Recruiting Management preview or import archive contains one or more retained setting updates. | |
| Recruiting Management archive columns | Require parent columns Code and Description, and child columns ORA_IRC_SETTING_VALUE.Code, StringValue, and SettingValueId. | A Recruiting Management preview or import archive contains one or more retained setting updates. | |
| Recruiting Management archive atomic validation | If a required parent is absent, empty, duplicated, or mismatched, block the entire preview and import, list every affected setting code, and do not treat Fusion row skipping as acceptable partial processing. | A Recruiting Management archive is validated. | |
| Campaign Email Metrics retention entity | Require ENTITY_NAME to identify irc_cmt_recipients. | Data Purging configuration is selected. | |
| Campaign Email Metrics retention days | Require ACTIVE_DAYS as an integer from 180 through 1000. | Data Purging configuration is selected. | |
| Fields without exported values | Display Field, Supported Values, Default or Seeded Values. | The request does not include exported values. | |
| Fields with exported values | Display Field, Current Value, Supported Values. | The request includes current values from a task export. | |
| Pre-import field preview | Display Field, Current Value, Proposed Value, Supported Values. | The request asks for a preview before import. | |
| Import/export display eligibility | Show only Supported or Conditionally supported fields; hide Not supported fields. | A section field list is requested. | |
| AI Features exact mapping | Require exactly one row in a fresh export of this task for every requested supported AI Features setting code. A missing or duplicate mapping stops only the affected field; do not infer a code or append a row. | A supported AI Features field is read, previewed, or modified. | verify_ai_features_setting_mappings |
| AI Features unsupported fields | Do not generate an import row for Enable job application highlights, Enable job application rating, ORA_IRC_AI_SIMILAR_CANDIDATE, ORA_IRC_AI_EXCLUDED_COUNTRIES_ENABLED, ORA_IRC_AI_JOBS2CANDIDATE_ENABLED, ORA_IRC_AI_JOBS2JOBS_ENABLED, or ORA_IRC_AI_TIME_TO_HIRE_ENABLED. | An AI Features request contains a field marked Not supported. | |
| AI Features importance decimal syntax | Require decimal syntax for Education importance, Skill importance, and Experience importance. | One or more importance values are in scope. | |
| AI Features importance total | Validate the final Education, Skill, and Experience importance values together and require their exact decimal total to equal 1. Use proposed values for supplied fields and exact fresh-export current values for the remaining members; block the complete importance group when all three final values cannot be established. | One or more importance values are read, previewed, or modified. | verify_ai_features_setting_mappings |
| AI Features maximum summaries | Require numeric syntax for ORA_IRC_AI_MAX_NUMBER_OF_SUMMARIES_PER_DAY. Do not invent a minimum, maximum, or whole-number requirement. | Maximum summaries per day is supplied. | |
| AI Features candidate suggestions toggle | Accept only Y or N for ORA_IRC_AI_MATCHING_ENABLED. | Enable candidate suggestions on requisitions is supplied. | |
| AI Features selected countries preservation | Require one exact nonblank ORA_IRC_AI_EXCLUDED_COUNTRIES value from the fresh export and preserve it without constructing, translating, or simplifying it. | Selected countries is read, previewed, or retained as a standalone value. | verify_ai_features_setting_mappings |
| Offer Boolean values | Accept only Y or N for Download Offer Letter with Resolved Tokens, Withdraw candidates from all other active job applications when they move to the HR phase, Remove candidates from candidate pools when they move to the HR phase, Allow candidates to accept or decline job offers after the offer's expiration date, Attach candidate resume, Enable versioning of job offer letters, and Enable Provisional Offer Letter. | An Offer Boolean setting is supplied. | |
| Offer day values | Require a whole number equal to or greater than 0. Allow blank only for the three End Dating Offer Assignments settings, where blank means no end date. Do not invent a maximum. | An Offer day setting is supplied. | |
| Offer collaborator selection mode | Accept exactly one mode: All collaborator types, one or more specific collaborator labels or codes, or None. | Requisition Collaborators Added to Offers is supplied. | |
| Offer specific collaborator types | Require the complete supplied selection to resolve before generating its CSV value. | One or more specific collaborator labels or codes are supplied. | resolve_offer_collaborator_types |
| Offer collaborator None representation | Require the stored CSV representation to be established before generating the setting row. | None is supplied. | resolve_offer_collaborator_none_representation |
| Move to HR potential-duplicate person types | Accept only ALL or ORA_RECRUITING. | Include as Potential Duplicates is supplied. | |
| Move to HR manual duplicate-check choice | Accept only None - no duplicate validation; Use person creation duplicate check setting for all candidates; or Use person creation duplicate check setting only for candidates with date of birth and national identifier. Do not generate a CSV row or invent a setting code for this input. | Duplicate Check in Move to HR is supplied. | |
| Agency Hiring Boolean values | Accept only Y or N for Hide Candidate Data, Allow Internal Candidate Search, and Enable Agent Actions. | An Agency Hiring Boolean setting is supplied. | |
| Agency Hiring Agent User Category | Require a nonblank Security Console User Category code that the user has manually verified in the target environment. Reject an unknown or unverified code. | Agent User Category is supplied. | |
| Agency Hiring Agent Role | Require a nonblank Security Console job-role code that the user has manually verified in the target environment. Reject an unknown or unverified code. | Agent Role is supplied. | |
| PDF delivery method | Map only to ORA_IRC_PRINT_PDF_DELIVERY_METHOD; accept FILE_ATTACHMENT or HYPERLINK. | Print to PDF is selected. | |
| Maximum file size | Map only to ORA_IRC_PRINT_PDF_MAX_FILE_SIZE; require integer syntax from 1 through 10. | Print to PDF is selected. | |
| Maximum selections | Map only to ORA_IRC_PRINT_PDF_MAX_SELECTIONS; require integer syntax from 1 through 100. | Print to PDF is selected. | |
| Document Types import selector | Accept one System Document Type or one GHR Document Type Name. If both are supplied, require both to resolve to the same GHR document. | A Document Types import is requested. | resolve_ghr_document_type_for_import |

## Recruiting Management

Never guess a Recruiting Management setting code or its FSM mapping. Include a
setting only when a fresh export of this exact task proves the exact setting
code and its parent/child CSV mapping. If that evidence is missing or
duplicated, skip only the affected field and disclose the evidence gap. Do not
infer a code, parent row, default, persistence behavior, or import route, and do
not describe an environment-exported value as a seeded or packaged default
without separate authoritative evidence.

| Field | Setting Code | Supported Values | Validation |
|---|---|---|---|
| Requisition Number Generation Method | REQUISITION_NUMBER_GENERATION_METHOD | ORA_IRC_REQ_GEN_METHOD_AUTO or ORA_IRC_REQ_GEN_METHOD_MANUAL | Require an exact accepted code verified through ORA_IRC_REQ_GEN_METHOD by verify_requisition_number_generation_method. Do not accept a Meaning as the stored value. |
| Requisition Number Generation Starting Number | REQUISITION_NUMBER_GENERATION_STARTING_NUMBER | Numeric value greater than or equal to 0 | Reject a nonnumeric or negative value. Do not invent a whole-number requirement or upper bound. |
| Maximum Number of Unconfirmed Submissions | ORA_IRC_MAX_UNCONFIRMED_SUBS | Integer from 1 through 10 | Require base-10 integer syntax and a value from 1 through 10 inclusive. |
| Allow Candidates to Withdraw and Reapply | ORA_IRC_JA_WITHDRAW_REAPPLY | Y or N | Accept only Y or N. |
| Prefill Legislative Information | ORA_IRC_JA_PREFILL_LEG_INFO | Y or N | Accept only Y or N. |
| Prefill Questionnaire Information | ORA_IRC_JA_PREFILL_QSTNR_INFO | Y or N | Accept only Y or N. |

For every Recruiting Management preview, display exactly:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|
| Each requested Recruiting Management field | Value from its exact fresh-export row | Independently validated supplied value | Exact mapping, lookup, and validation result for that field |

Validate each supplied field independently. An invalid value skips only the
affected setting and discloses the setting code, supplied value, and reason.
For an invalid Requisition Number Generation Method, also disclose
`ORA_IRC_REQ_GEN_METHOD_AUTO` and `ORA_IRC_REQ_GEN_METHOD_MANUAL`.

## Recruiting Management Archive Validation

When `ORA_IRC_SETTING.csv` contains retained setting updates, every child row
must have exactly one matching parent row in `ORA_IRC_SETTING_VALUE.csv` using:

`ORA_IRC_SETTING_VALUE.csv.Code = ORA_IRC_SETTING.csv.ORA_IRC_SETTING_VALUE.Code`

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent row | Require exactly one nonempty matching parent and copy its complete row unchanged from the same fresh task export. | A child setting update is retained. | |
| Parent columns | Require Code and Description. | ORA_IRC_SETTING_VALUE.csv is validated. | |
| Child columns | Require ORA_IRC_SETTING_VALUE.Code, StringValue, and SettingValueId. | ORA_IRC_SETTING.csv is validated. | |
| Archive completeness | If any required parent is absent, empty, duplicated, or mismatched, block the entire preview and import and list every affected setting code. Do not rely on Fusion to skip individual rows. | One or more retained Recruiting Management updates are present. | |

## Print to PDF Scalar Settings

| Field | Setting Code | Default or Seeded Value | Supported Values |
|---|---|---|---|
| PDF delivery method | ORA_IRC_PRINT_PDF_DELIVERY_METHOD | FILE_ATTACHMENT | FILE_ATTACHMENT or HYPERLINK |
| Maximum file size | ORA_IRC_PRINT_PDF_MAX_FILE_SIZE | 10 | Integer from 1 through 10 |
| Maximum selections | ORA_IRC_PRINT_PDF_MAX_SELECTIONS | 30 | Integer from 1 through 100 |

## Document Types

All Document Types rows use business object `ORA_IRC_DOCUMENT_TYPES`, XML file
`DOCUMENT_TYPE_MIG.xml`, XML row `DocumentTypeMigrationVORow`, and row identity
`SystemDocumentType`.

| Field | Runtime or CSV attribute | Import/export status | Validation and import rule |
|---|---|---|---|
| System Document Type | SystemDocumentType | Supported | This is the unique alternate key. Use only a value selected from the existing Document Type list; do not construct or infer it from a display label, duplicate an existing row, or change it for an existing imported row. |
| Document Type Name | GHR `DocumentType` | Output-only | Resolve it through the GHR Document Types skill by exact `SystemDocumentType`. Display it for a Document Types list or current-value response, but never use it as an import identity. |
| Active | ActiveFlag | Not supported as a user-controlled import value | Import always overwrites the value to `N`. Do not generate a row intended to activate a document type. Activate it through the page UI after import; activation creates or maps the related Recruiting document category. |
| Requires validation | VerificationRequiredFlag / ValidationRequiredFlag | Supported subject to fresh export-header confirmation | Accept `Y` or `N`; UI default is `N`. The runtime attribute is `VerificationRequiredFlag`, while setup CSV metadata currently labels the CSV attribute `ValidationRequiredFlag`. Use the exact header in the fresh target export. |
| CategoryId | CategoryId | Not user-supported | Import resets it to `0`; do not populate or preserve it. |
| CategoryName | CategoryName | Not user-supported as an authored value | Do not manually create or modify it. UI activation derives it from `SystemDocumentType`: use that value when 30 characters or fewer; otherwise truncate and append a unique suffix such as `_01`. |

For a Document Types import, resolve the supplied System Document Type or GHR
Document Type Name through the GHR Document Types skill. Require exactly one
GHR record and validate all of the following before artifact creation:

| Check | Required result |
|---|---|
| GHR identity | The supplied selector resolves to exactly one GHR document. If both selector forms are supplied, they resolve to that same record. |
| Active | The resolved GHR document is active. |
| Recruiting uniqueness | A fresh Enterprise Recruiting Document Types export has no row with the resolved `SystemDocumentType`. |

Use the exact resolved `SystemDocumentType` as the `SystemDocumentType` import
identity. Do not use the GHR Document Type Name in the import row.

Never guess a Document Type value, `SystemDocumentType`, or CSV header. If a
fresh export does not establish the exact `SystemDocumentType` and
verification-flag column structure, stop only the affected row and explain the
evidence gap.

For a Document Types list or current-value response, use the GHR Document
Types skill to resolve each exported `SystemDocumentType` to exactly one GHR
`DocumentType`. Display the result as:

| Document Type Name | System Document Type | Active | Requires validation |
|---|---|---|---|

Do not derive a name from the code. If the GHR lookup returns zero or multiple
matches, retain the system code, mark only that name as unresolved, and explain
the evidence gap.

For every Document Types preview, display:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|

For Active, always display:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|
| Active | `<current value>` | Inactive (forced by import) | Requires post-import UI activation |

For Document Types current-value output, include the exported `ActiveFlag`
value. Add a note that Active is returned for export only, is not considered
for import, and is forced to `N` for every imported row.

## AI Features

AI Features uses the existing generic settings structure for supported scalar
rows: CSV identity `ORA_IRC_SETTING_CODE` maps to XML `Code`, and CSV value
`ORA_IRC_STRING_VALUE` maps to XML `StringValue`. Never guess a setting code.
Require a fresh export of this exact task to prove every supported field's
exact mapping before generating a row.

### Job Application Overview

| Field | Setting Code | Import/export status | Seeded Default | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|---|
| Enable job application highlights | No direct setting code proven | Not supported | Not established | None | Do not generate a setting row or infer a code. |
| Enable job application rating | No direct setting code proven | Not supported | Not established | None | Do not generate a setting row or infer a code. |
| Education importance | ORA_IRC_AI_SNIPPET_EDUCATION_SCORE | Supported | 0.3 | Decimal | Require decimal syntax and validate the final Education, Skill, and Experience values together; their exact decimal total must equal 1. |
| Skill importance | ORA_IRC_AI_SNIPPET_SKILL_SCORE | Supported | 0.3 | Decimal | Require decimal syntax and validate the final Education, Skill, and Experience values together; their exact decimal total must equal 1. |
| Experience importance | ORA_IRC_AI_SNIPPET_EXPERIENCE_SCORE | Supported | 0.4 | Decimal | Require decimal syntax and validate the final Education, Skill, and Experience values together; their exact decimal total must equal 1. |
| Maximum summaries per day | ORA_IRC_AI_MAX_NUMBER_OF_SUMMARIES_PER_DAY | Supported | blank | Numeric | Require numeric syntax. Do not invent a minimum, maximum, or whole-number requirement. |

When any importance value is requested, use proposed values for supplied
members and exact current values from the fresh export for omitted members.
Validate the three final decimal values as one group and require their total to
equal exactly `1`. If an exact mapping or current value for any group member is
unavailable, block the complete importance group without affecting other
independently valid AI Features settings.

### Candidate Suggestions

| Field | Setting Code | Import/export status | Seeded Default | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|---|
| Enable candidate suggestions on requisitions | ORA_IRC_AI_MATCHING_ENABLED | Supported | N | Y or N | Require exactly Y or N. |
| Enable similar candidates | ORA_IRC_AI_SIMILAR_CANDIDATE | Not supported | Not established | None | The standard migration view excludes this code. Do not generate or import a row. |
| Hide suggestions in selected countries | ORA_IRC_AI_EXCLUDED_COUNTRIES_ENABLED | Not supported | Not established | None | The standard migration view excludes this code. Do not generate or import a row. |
| Selected countries | ORA_IRC_AI_EXCLUDED_COUNTRIES | Conditionally supported as a standalone value | blank | Exact nonblank fresh-export representation | Preserve the country-list value exactly as represented in a nonblank fresh export. Do not construct, translate, or simplify it. This does not make Hide suggestions in selected countries importable. |

### Job Suggestions

| Field | Setting Code | Import/export status | Seeded Default | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|---|
| Enable suggested jobs for external candidates | ORA_IRC_AI_JOBS2CANDIDATE_ENABLED | Not supported | Not established | None | The standard migration view excludes this code. Do not generate or import a row. |
| Enable similar jobs for external candidates | ORA_IRC_AI_JOBS2JOBS_ENABLED | Not supported | Not established | None | The standard migration view excludes this code. Do not generate or import a row. |

### Time to Hire

| Field | Setting Code | Import/export status | Seeded Default | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|---|
| Enable time to hire on requisitions | ORA_IRC_AI_TIME_TO_HIRE_ENABLED | Not supported | Not established | None | The standard migration view excludes this code. Do not generate or import a row. |

Validate each independently supported scalar field separately, except for the
three importance values, which form one validation group. A missing exact
fresh-export mapping stops only the affected independent field or the complete
importance group. Preserve every unsupported field as an explicit blocked
result and never generate its import row.

## Events Settings

Treat an Events modification as one atomic two-setting request. Both values are
mandatory even though the product defaults are documented below; a default is
informational and must not replace a missing modification input.

| Field | Setting Code | Mandatory | Default or Seeded Value | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|---|
| Applied Metrics Days | ORA_IRC_EVENTS_APPLIED_METRICS_DAYS | Yes | 30 | Whole number from 1 through 999 | Require a nonblank whole number in range and generate its setting row only when both Events settings pass validation. |
| Hired Metrics Days | ORA_IRC_EVENTS_HIRED_METRICS_DAYS | Yes | 90 | Whole number from 1 through 999 | Require a nonblank whole number in range and generate its setting row only when both Events settings pass validation. |

Reject blank values, zero, negative values, decimals, characters, and mixed
text and numbers. If either Events setting is missing or invalid, stop the
complete Events request and ask for a valid whole number from 1 through 999.
Do not save, export, invoke downstream setup-data validation, or import a
partial or invalid Events request.

## Candidate Authenticity Settings

Treat every Candidate Authenticity modification as one atomic three-setting
request. The profile-option readiness check must succeed before these values
are validated or imported.

| Field | Setting Code | Mandatory | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|
| Endpoint URL | ORA_IRC_CAND_AUTH_ENDPOINT_URL | Yes | Nonblank text | Require at least one non-whitespace character and generate its setting row only when all three fields pass validation. |
| Access Token URL | ORA_IRC_CAND_AUTH_ACCESS_TOKEN_URL | Yes | Nonblank text | Require at least one non-whitespace character and generate its setting row only when all three fields pass validation. |
| Scope | ORA_IRC_CAND_AUTH_AGENT_SCOPE | Yes | Nonblank text | Require at least one non-whitespace character and generate its setting row only when all three fields pass validation. |

No credential setting code or credential value is supported by this CSV
contract. Do not accept a credential field, silently drop it into a partial
package, or expose its supplied value. Credential maintenance is available
only through the FSM setup UI.

## Candidate Experience

| Field | Setting Code | Supported Values | Validation and CSV Rule |
|---|---|---|---|
| Keep me signed in for external candidates | ORA_IRC_KEEP_CANDIDATE_SIGNED_IN_ENABLED | Y or N | Require exactly Y or N and use the row only after its exact setting code is verified in the fresh export. |
| Number of days to remain signed in | ORA_IRC_KEEP_CANDIDATE_SIGNED_IN_IDLE_PERIOD_DAYS | Whole number from 0 through 90 | Require base-10 whole-number syntax and an inclusive value from 0 through 90. |
| Candidate auto-confirmation | ORA_IRC_AUTO_CONFIRM_CANDIDATE_ENABLED | Y or N | Require exactly Y or N. |
| Verify last name and allow phone-number claim | ORA_IRC_LAST_NAME_CHECK_AND_CLAIM_PHONE_NUMBER_ENABLED | Y or N | Require exactly Y or N. |
| Verify date of birth and allow email claim | ORA_IRC_DATE_OF_BIRTH_CHECK_AND_CLAIM_EMAIL_ENABLED | Y or N | Require exactly Y or N. |
| Apply validation to candidates | ORA_IRC_DOB_VALIDATION_ATTRIBUTES | Ex-Workers or All Candidates | Require one of the two documented values exactly. |
| Repeat blocks in request-information flows | ORA_IRC_JA_CAND_ALLOW_RESUBMIT_ENABLED | Y or N | Require exactly Y or N. |
| Career-site search in requisition description | ORA_IRC_CX_SEARCH_KEYWORD_IN_REQ_DESC | Y or N | Require exactly Y or N. |
| Enable sitemap submission and job posting markup | ORA_IRC_CX_GOOG_JOB_SEARCH_ENABLED | Y or N | Require exactly Y or N. |
| Search Configuration URL | ORA_IRC_CX_SEO_JOB_SEARCH_CONFIG_URL | Blank or text up to 1,000 characters | Accept blank or text within the length limit; do not add an undocumented URL-format requirement. |
| Be the First to Apply - Maximum Number of Applications | ORA_IRC_CX_NUMBER_APPLICATIONS_BE_FIRST_TO_APPLY_TAG | Numeric input | Require a nonblank numeric value; do not invent an integer-only rule or range. |
| Trending - Minimum Number of Applications | ORA_IRC_CX_NUMBER_APPLICATIONS_TRENDING_TAG | Numeric input | Require a nonblank numeric value; do not invent an integer-only rule or range. |

For each supplied field, use only the documented setting code after
`verify_candidate_experience_setting_mappings` finds exactly one corresponding
row in the fresh target export. A missing or duplicate mapping stops only that
field and must not cause a guessed or substituted CSV row.

### Candidate Experience FSM Package Contract

For a Candidate Experience modification, begin with the exact successful fresh
task-export ZIP used for the field mappings. The final import package retains
that full export; it is not a one-CSV or otherwise scoped archive.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Candidate Experience source package | Require the current-workflow fresh task-export ZIP that produced the exact field mappings. | Preparing a Candidate Experience import package. | |
| Candidate Experience member inventory | Retain every meaningful source member. For every metadata object marked `MigrateFlag=Y`, include exactly one case-sensitive `<BusinessObjectShortName>.csv` member, ordered by its `NodeSequence`. Do not omit, rename, replace, or add a data CSV. | Preparing a Candidate Experience import package. | |
| Candidate Experience metadata | Preserve ASM_SETUP_CSV_METADATA.xml byte-for-byte. Do not edit, regenerate, rename, replace, or scope its object list. | Preparing a Candidate Experience import package. | |
| Candidate Experience allowed row changes | In ORA_IRC_SETTING.csv, change only StringValue cells for requested, exact-mapped, validated Candidate Experience setting rows. Preserve ORA_IRC_SETTING_VALUE.Code, SettingValueId, headers, column order, every unrequested row, and serialization outside an approved changed StringValue cell. | Preparing a Candidate Experience import package. | |
| Candidate Experience unchanged members | Preserve every CSV member other than ORA_IRC_SETTING.csv byte-for-byte, including ORA_IRC_SETTING_VALUE.csv. | Preparing a Candidate Experience import package. | |
| Candidate Experience package comparison | Before preview or import, compare the final archive with the fresh source package: require the full member inventory and required NodeSequence order, byte-identical metadata and non-target CSVs, and only approved StringValue differences in ORA_IRC_SETTING.csv. | Candidate Experience package construction is complete. | |
| Candidate Experience package mismatch | Stop before preview or import and rebuild from the same fresh full export. | The final archive fails any Candidate Experience package-contract check. | |

For every Candidate Experience preview, display exactly:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|

## Configure Active Candidate Filter

| Field | Setting Code | Seeded Default | User-Facing Values | Validation and Internal Mapping |
|---|---|---|---|---|
| Enable Candidate Activity | ORA_IRC_CAND_ACT_MASTER_ENABLED | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Activity Timeframe | ORA_IRC_CAND_ACT_TIMEFRAME | LAST_THREE_MONTHS | Active meanings from Common Lookup ORA_IRC_CAND_ACT_TIMEFRAME | Resolve the current internal value, permitted user-facing meanings, and any proposed meaning through resolve_active_candidate_timeframe_meanings. Display meanings only. |
| Applied for a Job | ORA_IRC_CAND_ACT_APPLIED_JOB | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Attended an Event | ORA_IRC_CAND_ACT_ATTENDED_EVENT | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Clicked an Email | ORA_IRC_CAND_ACT_CLICK_EMAIL | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Opened an Email | ORA_IRC_CAND_ACT_OPEN_EMAIL | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Registered for an Event | ORA_IRC_CAND_ACT_REGISTER_EVENT | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Responded to an Email | ORA_IRC_CAND_ACT_RESPONSE_EMAIL | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Responded to Request More Information | ORA_IRC_CAND_ACT_RESPONSE_RMI | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Responded to SMS | ORA_IRC_CAND_ACT_RESPONSE_SMS | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Responded to WhatsApp | ORA_IRC_CAND_ACT_RESPONSE_WHATSAPP | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Updated Job Alert Opt-In | ORA_IRC_CAND_ACT_UPDATE_JOB_ALERT_OPT_IN | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Updated Marketing Opt-In | ORA_IRC_CAND_ACT_UPDATE_MARK_OPT_IN | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |
| Updated Talent Community Preferences | ORA_IRC_CAND_ACT_UPDATE_TC | Y | Enabled or Disabled | Accept Enabled or Disabled and retain the corresponding internal value only for the guarded shared workflow. |

Before listing current values, previewing changes, or preparing a modification,
require `verify_active_candidate_filter_setting_mappings` to find exactly one
row for each requested field's documented setting code in the fresh current
full-task export. A missing or duplicate mapping stops only the affected field;
do not guess, substitute, append, or select a duplicate setting row.

Support one or multiple setting changes in one request. Every event-specific
activity setting must remain a separate item in lists, validation results, and
the combined preview. Do not create or display a combined all-event-controls
field.

Keep internal Boolean values, setting codes, row identifiers, export file
names, and lookup codes out of all user-facing Configure Active Candidate
Filter output. Display Enabled for an internal enabled value, Disabled for an
internal disabled value, and only active Common Lookup meanings for Activity
Timeframe.

For every Configure Active Candidate Filter preview, display exactly:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|

## Updates to Candidate Info

| Candidate Type | Field | Setting Code | Seeded Default | User-Facing Values | Validation and Internal Mapping |
|---|---|---|---|---|---|
| Contingent Worker | Address | ORA_IRC_CWK_EXT_ADDRESS_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Contingent Worker | Email | ORA_IRC_CWK_EXT_EMAIL_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Contingent Worker | Name | ORA_IRC_CWK_EXT_NAME_UPDATES_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Contingent Worker | Phone | ORA_IRC_CWK_EXT_PHONE_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Contingent Worker | Address | ORA_IRC_EX_CWK_ADDRESS_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Contingent Worker | Email | ORA_IRC_EX_CWK_EMAIL_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Contingent Worker | Name | ORA_IRC_EX_CWK_NAME_UPDATES_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Contingent Worker | Phone | ORA_IRC_EX_CWK_PHONE_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Employee | Address | ORA_IRC_EX_EMP_ADDRESS_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Employee | Email | ORA_IRC_EX_EMP_EMAIL_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Employee | Name | ORA_IRC_EX_EMP_NAME_UPDATES_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Ex-Employee | Phone | ORA_IRC_EX_EMP_PHONE_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Additional Person Types | Address | ORA_IRC_ADDITIONAL_PER_TYPES_ADDRESS_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Additional Person Types | Email | ORA_IRC_ADDITIONAL_PER_TYPES_EMAIL_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Additional Person Types | Name | ORA_IRC_ADDITIONAL_PER_TYPES_NAME_UPDATES_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |
| Additional Person Types | Phone | ORA_IRC_ADDITIONAL_PER_TYPES_PHONE_UPDATE_BLOCK | None (ORA_IRC_BLOCK_NONE) | None, Hiring App, Candidate Portal, or Hiring App and Candidate Portal | Require one active Common Lookup meaning and keep its code internal. |

Before reading current values, previewing changes, or preparing a modification,
require `verify_candidate_info_update_setting_mappings` to find exactly one row
for every requested Candidate Type and field pair in the fresh current
full-task export. A missing or duplicate mapping stops only that pair; do not
guess, substitute, append, or select a duplicate setting row.

Use only the exact Candidate Type names Contingent Worker, Ex-Contingent
Worker, Ex-Employee, and Additional Person Types. Do not replace them with
acronyms, aliases, or the term populations.

Support multiple Candidate Types and fields in one request. Preserve every
successfully validated change and show every requested pair in one combined
preview. If any requested pair remains invalid or unresolved, do not approve
or import a subset; correct the complete request and rebuild the preview.

Keep lookup codes internal. Display only the active Common Lookup meanings
None, Hiring App, Candidate Portal, and Hiring App and Candidate Portal.

For every Updates to Candidate Info preview, display exactly:

| Candidate Type | Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|---|

## Candidate Search Archiving

| Field | Setting Code | Seeded Default | Stored Values | User-Facing Values | Validation and Internal Mapping |
|---|---|---|---|---|---|
| Candidate Search Archiving | ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED | N | Y or N | Enabled or Disabled | Accept only Enabled or Disabled as user input. Retain the corresponding Y or N value internally for the existing guarded workflow. |

Before reading the current value, previewing a change, or preparing a
modification, require `verify_candidate_search_archiving_setting_mapping` to
find exactly one row for `ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED` in the
fresh current full-task export. A missing or duplicate mapping stops only this
field; do not guess, substitute, append, or select a duplicate setting row.

Keep stored values internal. Display Enabled for the stored enabled value and
Disabled for the stored disabled value.

For every Candidate Search Archiving preview, display exactly:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|

## Candidate Sourcing

Candidate Sourcing uses `ORA_IRC_SETTING.csv`. Accept only the following eight
field-to-code mappings. Use each UI label as the primary display value and
retain the setting code only for traceability.

| Field | Setting Code | Allowed Values | Validation and CSV Rule |
|---|---|---|---|
| Enable rule-based pools for all pool users | ORA_IRC_RULE_BASED_POOL_ENABLED | Y or N | Require exactly Y or N. |
| Enable job notifications for candidate pools | ORA_IRC_PROMOTE_JOBS_TO_CAND_POOL_MEMBERS_ENABLED | Y or N | Require exactly Y or N. |
| Send Notifications Every {n} Days (Candidate-pool email frequency) | ORA_IRC_CAND_POOL_EMAIL_FREQUENCY | Whole number from 0 through 30 | Require a nonblank base-10 whole number in the inclusive range 0 through 30. |
| Enable Talent Community | ORA_IRC_TC_OPTIN_ENABLED | Y or N | Require exactly Y or N. Use the proposed value, when supplied, to determine the final Talent Community state. |
| Fields displayed to external candidates when they join a talent community | ORA_IRC_TC_ACTIVE_ATTRIBUTES | Job Category; Job Function; or Job Function,Job Category | Require one documented value exactly. When Enable Talent Community is proposed as Y and this field is omitted from the same modification, apply the documented Job Category default. |
| Global Talent Community Pool Visible | ORA_IRC_TC_GLOBAL_POOL_VISIBLE | Y or N | Require exactly Y or N. N is CSV-importable. Y must not be imported and requires the documented Candidate Sourcing FSM/ADF UI save action to enable or create the pool. |
| Enable Job Alerts | ORA_IRC_JOB_ALERTS_ENABLED | Y or N | Require exactly Y or N. |
| Send Job Alert Every {n} Days | ORA_IRC_TC_EMAIL_FREQUENCY | Whole number from 0 through 30 | Require a nonblank base-10 whole number in the inclusive range 0 through 30. |

Before reading current values, previewing changes, or preparing a modification,
require `verify_candidate_sourcing_setting_mappings` to find exactly one
`ORA_IRC_SETTING.csv` row for every requested field's documented setting code
in the fresh current full-task export. When Enable Talent Community = Y is
proposed and the attributes field is omitted, require the resolver to find the
exact attributes row before defaulting it. A missing or duplicate mapping
stops only the affected field. Do not infer, substitute, append, or select a
row, and do not infer a current value.

Reject every setting code outside the eight-code allowlist. Reject blank,
negative, decimal, character, or mixed-text frequency values and every value
outside 0 through 30. Reject Talent Community attributes that differ from the
three exact documented values.

Talent Community attributes and Global Talent Community Pool visibility are
dependent on Talent Community being enabled in the final state. Determine the
final state from a proposed Enable Talent Community value when supplied;
otherwise use only its exact current value from the fresh export. Do not infer
the final state when that mapping or value is unavailable.

Support one or multiple Candidate Sourcing fields in one request and preserve
each field's result in the combined preview. Use the UI label in the `Field`
column and keep the setting code as secondary traceability rather than the
primary display value. A mixed request containing Global Talent Community Pool
Visible = Y must separate the required FSM/ADF UI action from CSV-eligible
rows; do not silently import only the CSV subset.

## Campaigns

Campaigns uses `ORA_IRC_SETTING.csv`. Accept only the following seven
field-to-code mappings. Use the Campaign Settings display order and UI purpose
as the primary user-facing representation. Retain setting and lookup codes only
for traceability and CSV construction.

| Display Order | Group | Field | Setting Code | Default or Seeded Value | Supported Values | Validation and CSV Rule |
|---|---|---|---|---|---|---|
| 1 | Campaign Numbering | Campaign Number Generation Method | ORA_IRC_CAMP_NUM_AUTO_GEN_FLAG | TBD | ORA_IRC_CAMP_GEN_METHOD_AUTO or ORA_IRC_CAMP_GEN_METHOD_MANUAL | Require one documented value exactly. |
| 2 | Campaign Numbering | Campaign Number Starting Value | ORA_IRC_CAMP_NUM_INIT_VALUE | TBD | Digits only | Require a nonblank sequence of base-10 digits. Reject signs, decimals, whitespace-only values, characters, symbols, and mixed text and numbers. |
| 3 | Email Designer and Campaign Delivery | Enable rich text editor in email designer | ORA_IRC_CAMP_EMAIL_DESIGNER_LEGACY_EDITOR | TBD | Y or N | Require exactly Y or N. |
| 4 | Email Designer and Campaign Delivery | Campaign Email Maximum Retry Count | ORA_IRC_CMT_MSG_RETRY_LIMIT | 3 | Numeric value greater than or equal to 0 | Require nonblank numeric syntax and a value greater than or equal to 0. Do not invent an upper bound or a whole-number restriction that the source does not document. |
| 5 | Campaign Audience Exclusions | Exclude candidates who were included in a recent campaign | ORA_IRC_CAMP_AUD_EMAIL_LIMIT_ENABLED_FLAG | TBD | Y or N | Require exactly Y or N. |
| 6 | Campaign Audience Exclusions | Recent-campaign exclusion duration | ORA_IRC_CAMP_AUD_EMAIL_LIMIT_UNIT_CODE | 1 week | 1 week, 2 weeks, or 1 month | Resolve the supplied UI value through Common Lookup ORA_IRC_CAMP_EMAIL_CAP_UNITS and store only the corresponding LookupCode in StringValue. |
| 7 | Campaign Audience Exclusions | Do not send emails to candidates flagged as do not rehire | ORA_IRC_CAMP_AUD_REHIRE_ELIG_ENABLED_FLAG | TBD | Y or N | Require exactly Y or N. |

Before reading current values, previewing changes, or preparing a Campaigns
modification, require `verify_campaign_setting_mappings` to find exactly one
`ORA_IRC_SETTING.csv` row for every requested field's documented setting code.
A read may reuse valid matching export evidence through the shared export-cache
workflow. A preview or modification requires a fresh current full-task export.
Do not infer, substitute, append, or select a duplicate setting row or current
value.

Resolve Recent-campaign exclusion duration through
`resolve_campaign_email_cap_unit`. Show only the active lookup Meaning to the
user and keep the LookupCode internal. The documented mappings are 1 week to
ORA_LAST_WEEK, 2 weeks to ORA_LAST_2_WEEKS, and 1 month to ORA_LAST_MONTH.
Require the delegated Common Lookup result to confirm the selected value is
enabled and current before using its code.

Support one or multiple Campaigns fields in one request. Validate the complete
request before preview, approval, or import; do not create or import a partial
Campaigns package. Use the task's standard preview columns: Field, Current
Value, Proposed Value, and Supported Values.

## Offer

Offer configuration is scoped to
ORA_IRC_MANAGE_ENTERPRISE_RECRUITING_AND_CANDIDATE_EXPERIENCE_INFORMATION and
uses ORA_IRC_SETTING.csv and ORA_IRC_SETTING_VALUE.csv. Support only these
twelve setting codes. Before generating a CSV row, require the exact setting
code to be represented by the task's approved fresh FSM export/import files;
otherwise apply the documented manual-action rule.

| Display Order | Field | Setting Code | Supported Values | Applicability Condition | Validation and CSV Rule | Error |
|---|---|---|---|---|---|---|
| 1 | Download Offer Letter with Resolved Tokens | ORA_IRC_RESOLVED_OFFER_LETTER_ENABLED | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 2 | Withdraw candidates from all other active job applications when they move to the HR phase | ORA_IRC_WITHDRAW_OTHER_JA_ON_ACCEPT_OFFER | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 3 | Remove candidates from candidate pools when they move to the HR phase | ORA_IRC_CAND_FROM_CANDPOOL_REMOVAL_ON_ACPT_OFFER | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 4 | Allow candidates to accept or decline job offers after the offer's expiration date | ORA_IRC_ALLOW_CAND_ACCEPT_DECLINE_EXPIRED_OFFER | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 5 | Attach candidate resume | ORA_IRC_ATTACH_CANDIDATE_RESUME | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 6 | Enable versioning of job offer letters | ORA_IRC_OFFER_LETTER_VERSIONING_ENABLED | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 7 | Enable Provisional Offer Letter | ORA_IRC_ENABLE_PROVISIONAL_OFFER_LETTER | Y or N | The field is supplied. | Generate one setting row using the supplied Y or N value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 8 | Automatically Process Internal Offers to Assignments — Days Before Proposed Start Date | ORA_IRC_INTERNAL_OFFER_AUTO_PROCESS_DAYS | 0 or a positive whole number of days | ORA_IRC_AUTO_PROCESS_INTERNAL_OFFERS is Y. | Require a non-negative whole number. A value of 0 processes on the proposed start date. | INVALID_DAY_VALUE — Enter a whole number equal to or greater than 0. PROFILE_OPTION_PREREQUISITE_NOT_MET — Enable the required Profile Option before updating this setting. |
| 9 | End Dating Offer Assignments — After Reaching the Final Successful State (HR - Processed) | ORA_IRC_OFFER_PROCESSED_ASG_END_DATE_DAYS | 0 or a positive whole number of days; blank means no end date | ORA_IRC_OFFERS_TERMINATE_ASG_ENABLED and ORA_IRC_TERM_ABANDONED_OFFERS_ENABLED are Y. | Require a non-negative whole number or blank. | INVALID_DAY_VALUE — Enter a whole number equal to or greater than 0, or leave blank for no end date. PROFILE_OPTION_PREREQUISITE_NOT_MET — Enable the required Profile Option before updating this setting. |
| 10 | End Dating Offer Assignments — After Reaching Any Final Unsuccessful State | ORA_IRC_OFFER_TERMINAL_ASG_END_DATE_DAYS | 0 or a positive whole number of days; blank means no end date | ORA_IRC_OFFERS_TERMINATE_ASG_ENABLED and ORA_IRC_TERM_ABANDONED_OFFERS_ENABLED are Y. | Require a non-negative whole number or blank. | INVALID_DAY_VALUE — Enter a whole number equal to or greater than 0, or leave blank for no end date. PROFILE_OPTION_PREREQUISITE_NOT_MET — Enable the required Profile Option before updating this setting. |
| 11 | End Dating Offer Assignments — For Abandoned Offers After | ORA_IRC_OFFER_ABANDONED_DAYS | 0 or a positive whole number of days; blank means no end date | ORA_IRC_OFFERS_TERMINATE_ASG_ENABLED and ORA_IRC_TERM_ABANDONED_OFFERS_ENABLED are Y. | Require a non-negative whole number or blank. | INVALID_DAY_VALUE — Enter a whole number equal to or greater than 0, or leave blank for no end date. PROFILE_OPTION_PREREQUISITE_NOT_MET — Enable the required Profile Option before updating this setting. |
| 12 | Requisition Collaborators Added to Offers | ORA_IRC_OFFER_COLLABORATORS_TO_COPY | ALL; one or more specific collaborator labels or codes; or None | The field is supplied. | Map All collaborator types directly to ALL. For specific selections, use the complete ordered StringValue returned by resolve_offer_collaborator_types and reject the complete selection on resolver failure. For None, use only the value returned by resolve_offer_collaborator_none_representation. | INVALID_COLLABORATOR_SELECTION — Select an enabled collaborator type available in this environment. |

## Move to HR

Move to HR duplicate-check configuration is scoped to
ORA_IRC_MANAGE_ENTERPRISE_RECRUITING_AND_CANDIDATE_EXPERIENCE_INFORMATION.
The CSV-backed setting uses ORA_IRC_SETTING.csv and ORA_IRC_SETTING_VALUE.csv.
Support only the documented setting code; do not invent a code or import value
for the manual-only field.

| Display Order | Field | Setting Code or Import Status | Supported Values | Validation and CSV Rule | Error |
|---|---|---|---|---|---|
| 1 | Include as Potential Duplicates | ORA_IRC_OFFER_DUPCHECK_PERSON_TYPES | All person types = ALL; Only person types supported in Recruiting = ORA_RECRUITING | Accept only ALL or ORA_RECRUITING. Generate one setting row using the accepted value; reject any other value. | INVALID_PERSON_TYPE_VALUE — Select All person types or Only person types supported in Recruiting. |
| 2 | Duplicate Check in Move to HR | Not exported in ORA_IRC_SETTING.csv | None - no duplicate validation; Use person creation duplicate check setting for all candidates; Use person creation duplicate check setting only for candidates with date of birth and national identifier | Do not generate a CSV row or invent a setting code. Complete the selection manually in Fusion. The setting depends on Enterprise HCM Information: Person Creation Duplicate Check and is not a Profile Option. | MANUAL_INTERVENTION_REQUIRED — This setting isn't available in the FSM import file. Complete it manually in Fusion. |

## Agency Hiring

Agency Hiring configuration is scoped to
ORA_IRC_MANAGE_ENTERPRISE_RECRUITING_AND_CANDIDATE_EXPERIENCE_INFORMATION and
uses ORA_IRC_SETTING.csv and ORA_IRC_SETTING_VALUE.csv. Support only these five
setting codes. Security Console reference codes remain FSM-importable only
after the documented manual target-environment verification.

| Display Order | Field | Setting Code | Supported Values | Validation and CSV Rule | Error |
|---|---|---|---|---|---|
| 1 | Hide Candidate Data | ORA_IRC_AGENCY_HIDE_CANDIDATE_DATA | Y or N | Accept only Y or N. Generate one setting row using the supplied value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 2 | Allow Internal Candidate Search | ORA_IRC_AGENCY_ENABLE_CAND_INTERNAL_SEARCH | Y or N | Accept only Y or N. Generate one setting row using the supplied value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 3 | Enable Agent Actions | ORA_IRC_AGENT_ACTIONS_ENABLE | Y or N | Accept only Y or N. Generate one setting row using the supplied value. | INVALID_BOOLEAN_VALUE — Enter Y or N for this setting. |
| 4 | Agent User Category | ORA_IRC_AGENCY_USER_CATEGORY_CODE | An existing target Security Console User Category code, such as DEFAULT | Require manual target Security Console verification before preview. Reject an unknown or unverified code. Do not invent a code or create Security Console master data as a side effect. | MANUAL_INTERVENTION_REQUIRED — Verify Agent User Category in target Security Console before importing. |
| 5 | Agent Role | ORA_IRC_AGENT_CUSTOM_ROLE_CODE | An existing target Security Console job-role code, such as ORA_IRC_RECRUITING_AGENT_JOB | Require manual target Security Console verification before preview. Reject an unknown or unverified code. Do not invent a code or create Security Console master data as a side effect. | MANUAL_INTERVENTION_REQUIRED — Verify Agent Role in target Security Console before importing. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TASK.ROUTE_SECTION | decision | 1 | evaluate_result | interview_intelligence_read->SECTION.RESOLVE_EXPORT_SOURCE;interview_intelligence_write->II.VALIDATE_INPUT;microsoft_graph_read->SECTION.RESOLVE_EXPORT_SOURCE;microsoft_graph_write->INTEGRATION.FSM_REQUIRED;google_workspace_read->SECTION.RESOLVE_EXPORT_SOURCE;google_workspace_write->INTEGRATION.FSM_REQUIRED;zoom_read->SECTION.RESOLVE_EXPORT_SOURCE;zoom_write->INTEGRATION.FSM_REQUIRED;events_read->EVENTS.DEFAULT_API_VERSION;events_write->EVENTS.DEFAULT_API_VERSION;candidate_authenticity_read->SECTION.RESOLVE_EXPORT_SOURCE;candidate_authenticity_write->CAND_AUTH.CHECK_PROFILE_OPTION;candidate_experience_read->SECTION.RESOLVE_EXPORT_SOURCE;candidate_experience_write->CAND_EXP.RESOLVE_FRESH_EXPORT_MAPPINGS;active_candidate_filter_read->ACF.RESOLVE_FRESH_EXPORT_MAPPINGS;active_candidate_filter_write->ACF.RESOLVE_FRESH_EXPORT_MAPPINGS;updates_to_candidate_info_read->UCI.RESOLVE_FRESH_EXPORT_MAPPINGS;updates_to_candidate_info_write->UCI.RESOLVE_FRESH_EXPORT_MAPPINGS;candidate_search_archiving_read->CSA.RESOLVE_FRESH_EXPORT_MAPPING;candidate_search_archiving_write->CSA.RESOLVE_FRESH_EXPORT_MAPPING;candidate_sourcing_read->CAND_SRC.RESOLVE_FRESH_EXPORT_MAPPINGS;candidate_sourcing_write->CAND_SRC.RESOLVE_FRESH_EXPORT_MAPPINGS;campaigns_read->CAMP.RESOLVE_SETTING_MAPPINGS;campaigns_write->CAMP.RESOLVE_SETTING_MAPPINGS;recruiting_management_read->IRC.VALIDATE_DATA_PURGING;recruiting_management_write->IRC.VALIDATE_DATA_PURGING;data_purging_read->IRC.VALIDATE_DATA_PURGING;data_purging_write->IRC.VALIDATE_DATA_PURGING;print_to_pdf_read->SECTION.RESOLVE_EXPORT_SOURCE;print_to_pdf_write->IRC.VALIDATE_DATA_PURGING;document_types_read->SECTION.RESOLVE_EXPORT_SOURCE;document_types_write->IRC.VALIDATE_DATA_PURGING;ai_features_read->AI_FEATURES.RESOLVE_FRESH_EXPORT_MAPPINGS;ai_features_write->AI_FEATURES.RESOLVE_FRESH_EXPORT_MAPPINGS;offer_read->SECTION.RESOLVE_EXPORT_SOURCE;offer_write->IRC.VALIDATE_DATA_PURGING;move_to_hr_read->SECTION.RESOLVE_EXPORT_SOURCE;move_to_hr_write->IRC.VALIDATE_DATA_PURGING;agency_hiring_read->SECTION.RESOLVE_EXPORT_SOURCE;agency_hiring_write->IRC.VALIDATE_DATA_PURGING;unsupported->TASK.BLOCKED | none | stop | A supported section read or modification request is received. |
| II.VALIDATE_INPUT | decision | 2 | validate_input | valid->II.CHECK_BOOSTER;invalid->II.BLOCKED | TASK.ROUTE_SECTION | stop | An Interview Intelligence setting change is requested. |
| EVENTS.ROUTE_OPERATION | decision | 12 | evaluate_result | events_read->SECTION.RESOLVE_EXPORT_SOURCE;events_write->EVENTS.VALIDATE_INPUT;unsupported->EVENTS.BLOCKED | EVENTS.CHECK_ADVANCED_RECRUITING | stop | Advanced Recruiting is enabled and the Events request must be routed to read or modification handling. |
| EVENTS.VALIDATE_INPUT | decision | 13 | validate_input | valid->EVENTS.READY_FOR_CSV_WORKFLOW;invalid->EVENTS.BLOCKED | EVENTS.ROUTE_OPERATION | stop | Validate both mandatory Events settings atomically after Advanced Recruiting readiness succeeds. |
| CAND_AUTH.VALIDATE_INPUT | decision | 17 | validate_input | valid->CAND_AUTH.ENFORCE_CREDENTIAL_BOUNDARY;invalid->CAND_AUTH.BLOCKED;prohibited_field->CAND_AUTH.BLOCKED | CAND_AUTH.CHECK_PROFILE_OPTION | stop | Validate the three mandatory Candidate Authenticity settings atomically only after the configured Site-level profile option is exactly Y. |
| CAND_EXP.VALIDATE_INPUT | decision | 27 | validate_input | valid->CAND_EXP.READY_FOR_CSV_WORKFLOW;partial->CAND_EXP.READY_FOR_CSV_WORKFLOW;invalid_all->CAND_EXP.BLOCKED;package_mismatch->CAND_EXP.BLOCKED | CAND_EXP.RESOLVE_FRESH_EXPORT_MAPPINGS | stop | Validate each exact-mapped Candidate Experience field independently, then validate the final full-export FSM package before it is ready; retain per-field failures in the required preview. |
| IRC.VALIDATE_DATA_PURGING | decision | 30 | validate_input | valid->IRC.VALIDATE_RECRUITING_MANAGEMENT_SETTINGS;not_applicable->IRC.VALIDATE_RECRUITING_MANAGEMENT_SETTINGS;invalid->IRC.RETURN_ISSUES | TASK.ROUTE_SECTION | stop | A configuration section, including Recruiting Management, Offer, Move to HR, or Agency Hiring, is selected. |
| IRC.VALIDATE_RECRUITING_MANAGEMENT_SETTINGS | decision | 82 | validate_input | valid->IRC.LOOKUP_REQUISITION_NUMBER_GENERATION_METHOD;partial->IRC.LOOKUP_REQUISITION_NUMBER_GENERATION_METHOD;invalid_all->IRC.RETURN_ISSUES;not_applicable->IRC.RESOLVE_OFFER_PROFILE_OPTIONS | IRC.VALIDATE_DATA_PURGING | stop | Validate every supplied Recruiting Management setting independently after exact fresh-export mapping; otherwise continue the existing configuration path. |
| IRC.VALIDATE_RECRUITING_MANAGEMENT_ARCHIVE | decision | 91 | validate_input | valid->IRC.DONE;not_applicable->IRC.DONE;invalid->IRC.RETURN_ISSUES | IRC.ENFORCE_CONFIGURATION_MIGRATION | stop | Before any Recruiting Management preview or import, validate the retained child rows, matching unchanged parent rows, required columns, and complete archive relationship; otherwise return not_applicable. |
| AI_FEATURES.VALIDATE_INPUT | decision | 95 | validate_input | valid->AI_FEATURES.ENFORCE_MIGRATION;partial->AI_FEATURES.ENFORCE_MIGRATION;invalid_all->AI_FEATURES.BLOCKED | AI_FEATURES.RESOLVE_FRESH_EXPORT_MAPPINGS | stop | Validate supported AI Features scalar inputs, validate the three importance values as one exact-sum group, preserve eligible Selected countries evidence, and retain unsupported fields as explicit blocked results. |
| ACF.VALIDATE_INPUT | decision | 44 | validate_input | valid->ACF.ENFORCE_DISPLAY_AND_WORKFLOW;partial->ACF.ENFORCE_DISPLAY_AND_WORKFLOW;invalid_all->ACF.BLOCKED | ACF.CHECK_DEPENDENCIES | stop | Validate every supplied Configure Active Candidate Filter field independently, retain multiple valid changes, and keep every event-specific activity field separate. |
| UCI.VALIDATE_INPUT | decision | 52 | validate_input | valid_all->UCI.ENFORCE_PREVIEW_AND_WORKFLOW;partial->UCI.ENFORCE_PREVIEW_AND_WORKFLOW;invalid_all->UCI.BLOCKED | UCI.CHECK_DEPENDENCIES | stop | Validate every requested Updates to Candidate Info Candidate Type and field pair independently and retain all results for one combined preview. |
| CSA.VALIDATE_INPUT | decision | 59 | validate_input | valid->CSA.ENFORCE_DISPLAY_AND_WORKFLOW;invalid->CSA.BLOCKED | CSA.CHECK_DEPENDENCY | stop | Accept only Enabled or Disabled for Candidate Search Archiving and retain the corresponding stored value internally. |
| CAND_SRC.VALIDATE_INPUT | decision | 67 | validate_input | valid->CAND_SRC.ENFORCE_WORKFLOW;partial->CAND_SRC.ENFORCE_WORKFLOW;invalid_all->CAND_SRC.BLOCKED | CAND_SRC.CHECK_DEPENDENCIES | stop | Validate each exact-mapped Candidate Sourcing field against the eight-code allowlist, Boolean, frequency, and Talent Community attribute contracts. |
| CAMP.VALIDATE_INPUT | decision | 76 | validate_input | valid->CAMP.ENFORCE_WORKFLOW;invalid->CAMP.BLOCKED | CAMP.RESOLVE_DURATION_UNIT | stop | Validate every requested Campaigns field against the seven-code allowlist and its documented enum, digits-only, Boolean, numeric-minimum, or lookup-backed value contract as one complete request. |
