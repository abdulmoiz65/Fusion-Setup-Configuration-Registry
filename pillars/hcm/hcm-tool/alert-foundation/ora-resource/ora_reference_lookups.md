# Alert Foundation Reference Lookups

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | inspect_event_alert_contract | Deep validation or explicit metadata inspection | Target environment and selected framework version: 9 for sequential; 4 for batch-create | /hcmRestApi/resources/11.13.18.05/eventAlerts/describe | Resource methods, item key, finders, actions, attributes, children | Require compatibility with the selected operation, nested children and provider version; batch also requires reviewed batch-route evidence | Compatible methods, AlertId key, finder and attribute contract | Stop with catalog_or_metadata_mismatch |
| CUSTOM_ALERTS | Alerts | resolve_template_mime_type | Deep validation with included Templates | LookupType ORA_HRC_ALERT_MIME_TYPE and literal MimeType, from the observed Template describe LOV mapping | /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_HRC_ALERT_MIME_TYPE | LookupCode, Meaning | Fetch all required pages and match exactly one requested LookupCode | MimeType: LookupCode; MimeTypeMeaning: Meaning | Stop and request a valid MIME code; do not downgrade to simple |
| CUSTOM_ALERTS | Alerts | resolve_template_language | Deep validation with included Templates | Literal DefaultLanguage and ActiveLanguageFinder, from the observed Template describe LOV mapping | /hcmRestApi/resources/11.13.18.05/languagesLOV?finder=ActiveLanguageFinder | LanguageCode, Description | Fetch all required pages and match exactly one requested LanguageCode | DefaultLanguage: LanguageCode; LanguageDescription: Description | Stop on no match, ambiguity or unavailable route; do not downgrade to simple |
| CUSTOM_ALERTS | Alerts | resolve_alert_type_code | AlertType must be validated | LookupType ORA_HRC_ALERT_TYPE and requested AlertType | /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_HRC_ALERT_TYPE | LookupCode, Meaning | Match exactly one returned LookupCode | AlertType: LookupCode; AlertTypeMeaning: Meaning | Stop and request a valid alert type code |
| CUSTOM_ALERTS | Alerts | resolve_alert_access_level | AlertAccessLevel must be validated | LookupType ORA_HRC_ALERT_ACCESS_LEVEL and requested AlertAccessLevel | /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_HRC_ALERT_ACCESS_LEVEL | LookupCode, Meaning | Match exactly one returned LookupCode | AlertAccessLevel: LookupCode; AlertAccessLevelMeaning: Meaning | Stop and request a valid alert access-level code |
| CUSTOM_ALERTS | Alerts | resolve_recipient_channel_type | A Template Recipient is requested | LookupType ORA_HRC_ALERT_CHANNEL_TYPE and requested ChannelType | /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_HRC_ALERT_CHANNEL_TYPE | LookupCode, Meaning | Match exactly one returned LookupCode | ChannelType: LookupCode; ChannelTypeMeaning: Meaning | Stop and request a valid recipient channel code |
| CUSTOM_ALERTS | Alerts | find_event_alert_by_code | Existing-item resolution or duplicate prevention is required | Exact AlertCode | /hcmRestApi/resources/11.13.18.05/eventAlerts?finder=findByAlertCode;AlertCode={AlertCode}&onlyData=true | AlertId, AlertCode, Name, AlertAccessLevel, EnabledFlag, TestModeFlag and response context | Match exactly one item for update, disable, delete, or copy; match zero items for create | AlertId: AlertId; CanonicalKey: response context key; CurrentAlertCode: AlertCode; CurrentName: Name; CurrentAccessLevel: AlertAccessLevel; CurrentEnabledFlag: EnabledFlag; CurrentTestModeFlag: TestModeFlag | Stop on ambiguity; create requires zero matches and existing-item operations require exactly one |
| CUSTOM_ALERTS | Alerts | read_event_alert_by_canonical_key | Exact current state or post-write verification is required | Server-returned canonical key or URI | /hcmRestApi/resources/11.13.18.05/eventAlerts/{canonicalKey} | AlertId, AlertCode, Name, Description, AlertType, AlertAccessLevel, EnabledFlag, TestModeFlag, LastUpdateDate | Match the exact canonical item URI and compare AlertId plus requested business fields | Verified AlertId, canonical key, alert state, and server-managed LastUpdateDate | Stop on not found, identity mismatch, or field mismatch |

## Lookup Execution Rules

The live resolver rows are available only for deep preflight, explicit read
requests or required existing-item identity/read-back checks. Simple CREATE
does not run describe, coded-value, language or existing-Alert duplicate checks.
Record ALERT.LOOKUP as skipped_simple and continue to local dependency/design
checks; do not claim any live value was verified. Deep uses every applicable
resolver, including MIME and language. Its describe runs first; follow complete
pagination and stop rather than substituting an undeclared endpoint on failure.

Live Template Recipient expression validation is deferred in provider version
`0.8.0`. The workflow must not call the eventAlerts `validateExpression`
action, and its absence must not block preview, approval, or execution. The
workbook reader continues to require a nonblank `ValueExpression` of at most
2,000 characters.

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| CUSTOM_ALERTS | Alerts | A lookup receives 401 or 403 | Allow the shared OAuth client to refresh once; if rejection remains, stop as authorization_or_privilege |
| CUSTOM_ALERTS | Alerts | A lookup has a transport failure | Retry only when the call is read-only and the failure is known recoverable |
| CUSTOM_ALERTS | Alerts | A lookup returns ambiguous identity | Stop before preview; never choose an arbitrary item |
| CUSTOM_ALERTS | Alerts | Describe is incompatible | Stop before any mutation and report the missing method, key, finder, action, or field |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | ALERT.LOOKUP | decision | 2 | reference_lookup | resolved->ALERT.DEPENDENCY;skipped_simple->ALERT.DEPENDENCY;unresolved->ALERT.RETURN_ISSUES | ALERT.VALIDATE | stop | Deep or explicit read/identity checks execute declared resolvers; simple CREATE records skipped_simple without an external call |
