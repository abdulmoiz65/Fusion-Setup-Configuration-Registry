# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Events Advanced Recruiting API version | latest | api_version is omitted before an Events read or modification readiness check | No | |
| AI Features Education importance - ORA_IRC_AI_SNIPPET_EDUCATION_SCORE | 0.3 | Reporting the seeded default after exact fresh-export mapping, or the user explicitly requests this value as part of a valid importance group | No | verify_ai_features_setting_mappings |
| AI Features Skill importance - ORA_IRC_AI_SNIPPET_SKILL_SCORE | 0.3 | Reporting the seeded default after exact fresh-export mapping, or the user explicitly requests this value as part of a valid importance group | No | verify_ai_features_setting_mappings |
| AI Features Experience importance - ORA_IRC_AI_SNIPPET_EXPERIENCE_SCORE | 0.4 | Reporting the seeded default after exact fresh-export mapping, or the user explicitly requests this value as part of a valid importance group | No | verify_ai_features_setting_mappings |
| AI Features Maximum summaries per day - ORA_IRC_AI_MAX_NUMBER_OF_SUMMARIES_PER_DAY | blank | Reporting the seeded default after exact fresh-export mapping | No | verify_ai_features_setting_mappings |
| AI Features Enable candidate suggestions on requisitions - ORA_IRC_AI_MATCHING_ENABLED | N | Reporting the seeded default after exact fresh-export mapping, or the user explicitly requests this value | No | verify_ai_features_setting_mappings |
| AI Features Selected countries - ORA_IRC_AI_EXCLUDED_COUNTRIES | blank | Reporting the seeded default after exact fresh-export mapping; a retained standalone value still requires an exact nonblank fresh-export representation | No | verify_ai_features_setting_mappings |
| Campaign Email Maximum Retry Count - ORA_IRC_CMT_MSG_RETRY_LIMIT | 3 | Reporting the Campaigns seeded default after the exact setting mapping is resolved, or the user explicitly requests the seeded value | No | |
| Recent-campaign exclusion duration - ORA_IRC_CAMP_AUD_EMAIL_LIMIT_UNIT_CODE | ORA_LAST_WEEK; display 1 week | Reporting the Campaigns seeded default after exact setting mapping and active Common Lookup resolution, or the user explicitly requests the seeded value | No | resolve_campaign_email_cap_unit |
| Enable Candidate Activity - ORA_IRC_CAND_ACT_MASTER_ENABLED | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Activity Timeframe - ORA_IRC_CAND_ACT_TIMEFRAME | LAST_THREE_MONTHS; display only its active lookup meaning | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_active_candidate_timeframe_meanings |
| Applied for a Job - ORA_IRC_CAND_ACT_APPLIED_JOB | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Attended an Event - ORA_IRC_CAND_ACT_ATTENDED_EVENT | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Clicked an Email - ORA_IRC_CAND_ACT_CLICK_EMAIL | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Opened an Email - ORA_IRC_CAND_ACT_OPEN_EMAIL | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Registered for an Event - ORA_IRC_CAND_ACT_REGISTER_EVENT | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Responded to an Email - ORA_IRC_CAND_ACT_RESPONSE_EMAIL | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Responded to Request More Information - ORA_IRC_CAND_ACT_RESPONSE_RMI | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Responded to SMS - ORA_IRC_CAND_ACT_RESPONSE_SMS | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Responded to WhatsApp - ORA_IRC_CAND_ACT_RESPONSE_WHATSAPP | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Updated Job Alert Opt-In - ORA_IRC_CAND_ACT_UPDATE_JOB_ALERT_OPT_IN | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Updated Marketing Opt-In - ORA_IRC_CAND_ACT_UPDATE_MARK_OPT_IN | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Updated Talent Community Preferences - ORA_IRC_CAND_ACT_UPDATE_TC | Y; display Enabled | Reporting the Configure Active Candidate Filter seeded default after exact fresh-export mapping | No | |
| Contingent Worker - Address - ORA_IRC_CWK_EXT_ADDRESS_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Contingent Worker - Email - ORA_IRC_CWK_EXT_EMAIL_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Contingent Worker - Name - ORA_IRC_CWK_EXT_NAME_UPDATES_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Contingent Worker - Phone - ORA_IRC_CWK_EXT_PHONE_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Contingent Worker - Address - ORA_IRC_EX_CWK_ADDRESS_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Contingent Worker - Email - ORA_IRC_EX_CWK_EMAIL_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Contingent Worker - Name - ORA_IRC_EX_CWK_NAME_UPDATES_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Contingent Worker - Phone - ORA_IRC_EX_CWK_PHONE_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Employee - Address - ORA_IRC_EX_EMP_ADDRESS_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Employee - Email - ORA_IRC_EX_EMP_EMAIL_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Employee - Name - ORA_IRC_EX_EMP_NAME_UPDATES_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Ex-Employee - Phone - ORA_IRC_EX_EMP_PHONE_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Additional Person Types - Address - ORA_IRC_ADDITIONAL_PER_TYPES_ADDRESS_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Additional Person Types - Email - ORA_IRC_ADDITIONAL_PER_TYPES_EMAIL_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Additional Person Types - Name - ORA_IRC_ADDITIONAL_PER_TYPES_NAME_UPDATES_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Additional Person Types - Phone - ORA_IRC_ADDITIONAL_PER_TYPES_PHONE_UPDATE_BLOCK | ORA_IRC_BLOCK_NONE; display None | Reporting the Updates to Candidate Info seeded default after exact fresh-export mapping and active Common Lookup resolution | No | resolve_candidate_info_update_allowed_values |
| Candidate Search Archiving - ORA_IRC_CANDIDATE_SEARCH_ARCHIVING_ENABLED | N; display Disabled | Reporting the Candidate Search Archiving seeded default after exact fresh-export mapping | No | |
| Fields displayed to external candidates when they join a talent community - ORA_IRC_TC_ACTIVE_ATTRIBUTES | Job Category | A Candidate Sourcing modification proposes Enable Talent Community = Y, omits this field from the same request, and its exact fresh-export setting row has been resolved | No | |
| Keep me signed in for external candidates - ORA_IRC_KEEP_CANDIDATE_SIGNED_IN_ENABLED | N | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Number of days to remain signed in - ORA_IRC_KEEP_CANDIDATE_SIGNED_IN_IDLE_PERIOD_DAYS | 30 | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Candidate auto-confirmation - ORA_IRC_AUTO_CONFIRM_CANDIDATE_ENABLED | N | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Verify last name and allow phone-number claim - ORA_IRC_LAST_NAME_CHECK_AND_CLAIM_PHONE_NUMBER_ENABLED | N | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Verify date of birth and allow email claim - ORA_IRC_DATE_OF_BIRTH_CHECK_AND_CLAIM_EMAIL_ENABLED | N | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Apply validation to candidates - ORA_IRC_DOB_VALIDATION_ATTRIBUTES | All Candidates | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Repeat blocks in request-information flows - ORA_IRC_JA_CAND_ALLOW_RESUBMIT_ENABLED | N | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Career-site search in requisition description - ORA_IRC_CX_SEARCH_KEYWORD_IN_REQ_DESC | Y | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Enable sitemap submission and job posting markup - ORA_IRC_CX_GOOG_JOB_SEARCH_ENABLED | Y | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Search Configuration URL - ORA_IRC_CX_SEO_JOB_SEARCH_CONFIG_URL | https://www.googleapis.com/webmasters/v3/sites/{SEARCHCONSOLE_SITEURL}/sitemaps/{SITEMAP_URL} | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Be the First to Apply - Maximum Number of Applications - ORA_IRC_CX_NUMBER_APPLICATIONS_BE_FIRST_TO_APPLY_TAG | 5 | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |
| Trending - Minimum Number of Applications - ORA_IRC_CX_NUMBER_APPLICATIONS_TRENDING_TAG | 50 | Reporting the Candidate Experience seeded default, or the user explicitly requests this seeded value after exact fresh-export mapping | No | |

The Campaigns seeded defaults are reporting metadata. Do not silently replace
an omitted or blank proposed value with a seeded default. Use a seeded value in
a modification only when the user explicitly requests it, the exact setting
mapping exists in the permitted export, and the value passes validation. For
Recent-campaign exclusion duration, resolve the active Common Lookup Meaning
and keep ORA_LAST_WEEK internal as the CSV StringValue.

AI Features seeded defaults are reporting metadata and must not silently
replace omitted modification inputs. The three importance defaults form the
documented `0.3 + 0.3 + 0.4 = 1` group, but each requested importance change
must still be validated with the other two exact final values. A blank Selected
countries default is not an importable standalone value; retain that setting
only when a fresh export supplies an exact nonblank representation.

The Events setting defaults `30` for
`ORA_IRC_EVENTS_APPLIED_METRICS_DAYS` and `90` for
`ORA_IRC_EVENTS_HIRED_METRICS_DAYS` are product defaults for reporting. They do
not satisfy the mandatory input contract for an Events modification and must
not be applied to replace a blank or missing requested value.

Candidate Experience seeded defaults are reporting metadata. Do not silently
replace an omitted proposed value with a seeded default. Use a seeded value for
a modification only when the user explicitly requests it, the value passes the
documented field validation, and the exact setting mapping exists in the fresh
target export.

Configure Active Candidate Filter seeded defaults are reporting metadata and
must not silently replace an omitted proposed value. In user-facing output,
render every enabled Boolean default as Enabled and resolve the Activity
Timeframe default to its active Common Lookup meaning. Keep the internal
Boolean values and timeframe lookup code out of the preview and report.

Updates to Candidate Info seeded defaults are reporting metadata. Do not use
the default to replace an omitted proposed value. Resolve the internal seeded
value through the active Common Lookup and display only None. Keep its lookup
code internal and preserve each Candidate Type and field default as a separate
item.

The Candidate Search Archiving seeded default is reporting metadata. Do not
use it to replace an omitted proposed value. Display the default as Disabled
and keep the stored N value internal.

The Candidate Sourcing Talent Community attributes default is an operational
conditional default, not reporting metadata. Apply `Job Category` only when a
modification proposes `ORA_IRC_TC_OPTIN_ENABLED=Y`, omits
`ORA_IRC_TC_ACTIVE_ATTRIBUTES` from that same request, and the mapping resolver
has found exactly one fresh-export attributes row. Do not override an explicit
attributes value, apply the default to a read, or apply it when the final
Talent Community state or exact target row cannot be established.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVENTS.DEFAULT_API_VERSION | step | 10 | apply_default | applied->EVENTS.CHECK_ADVANCED_RECRUITING;not_required->EVENTS.CHECK_ADVANCED_RECRUITING | TASK.ROUTE_SECTION | stop | For an Events read or modification, use latest only when api_version is omitted and preserve an explicitly supplied version for the readiness lookup. |
| CAND_SRC.APPLY_ACTIVE_ATTRIBUTES_DEFAULT | decision | 65 | apply_default | applied->CAND_SRC.CHECK_DEPENDENCIES;not_required->CAND_SRC.CHECK_DEPENDENCIES | CAND_SRC.RESOLVE_FRESH_EXPORT_MAPPINGS | stop | Apply Job Category only when Enable Talent Community is proposed as Y, the attributes field is omitted from the same Candidate Sourcing modification, and its exact fresh-export target row is resolved. |
