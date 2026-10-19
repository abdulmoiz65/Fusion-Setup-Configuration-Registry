# Recruiting Messaging Configuration Input Validation

Accept only the documented country-permission and messaging-setting fields below. Keep implementation identifiers internal unless technical diagnostics are requested. Validation prepares a proposal only; it does not apply a change.

## Supported Country-Permission Fields

| Business Value | Implementation Field | Accepted Input | Normalized Result | If Missing or Invalid |
|---|---|---|---|---|
| Country | PhoneCountryCode | Exact country name, exact two-character territory code, or exact digits-only phone-country code | Resolve or validate through resolve_phone_country_code and return a digits-only phone-country code | Ask only for a missing country, no exact active match, an ambiguous name or territory code, or a numeric code absent from the active country list; never infer a value |
| Messaging channel | ChannelTypeCode | SMS, WhatsApp, or WA | SMS becomes ORA_SMS; WhatsApp and WA become ORA_WHATSAPP | Reject every other channel; treat supported channel enablement for a country as a country-permission request, not provider or general channel activation |
| Country and channel message limit | ThrottleLimit | Optional positive whole number greater than zero, using digits only | Preserve the supplied digits; when omitted, leave the field absent | Reject zero, signs, decimals, and non-digits; do not interpret omission as zero, unlimited, deletion, a default, or inheritance |
| Unique country and channel permission | PhoneCountryCode plus ChannelTypeCode | One row for each normalized country-code and channel pair | Retain one unique pair | Reject a duplicate pair; do not silently deduplicate |

## Supported Messaging Settings

| Business Setting | Setting Code | Accepted Business Input | Normalized Business Value | If Invalid or Unresolved |
|---|---|---|---|---|
| SMS system-wide daily maximum | RECRUITING_WIDE_OUTBOUND_SMS_HARD_LIMIT | Positive whole number greater than zero, using digits only; no additional upper bound is authorized | Supplied number | Reject zero, signs, decimals, and non-digits; the related warning-threshold relationship is enforced before review |
| SMS warning threshold | RECRUITING_WIDE_OUTBOUND_SMS_SOFT_LIMIT | Positive whole number greater than zero, using digits only; no additional upper bound is authorized | Supplied number | Reject zero, signs, decimals, and non-digits; the relationship to the SMS system-wide maximum is enforced before review |
| SMS per-candidate daily maximum | CANDIDATE_OUTBOUND_SMS_HARD_LIMIT | Positive whole number greater than zero, using digits only; no additional upper bound is authorized | Supplied number | Reject zero, signs, decimals, and non-digits; the relationship to the SMS system-wide maximum is enforced before review |
| WhatsApp system-wide daily maximum | RECRUITING_WIDE_OUTBOUND_WHATSAPP_HARD_LIMIT | Positive whole number greater than zero, using digits only; no additional upper bound is authorized | Supplied number | Reject zero, signs, decimals, and non-digits; the related warning-threshold relationship is enforced before review |
| WhatsApp warning threshold | RECRUITING_WIDE_OUTBOUND_WHATSAPP_SOFT_LIMIT | Positive whole number greater than zero, using digits only; no additional upper bound is authorized | Supplied number | Reject zero, signs, decimals, and non-digits; the relationship to the WhatsApp system-wide maximum is enforced before review |
| WhatsApp per-candidate daily maximum | CANDIDATE_OUTBOUND_WHATSAPP_HARD_LIMIT | Positive whole number greater than zero, using digits only; no additional upper bound is authorized | Supplied number | Reject zero, signs, decimals, and non-digits; the relationship to the WhatsApp system-wide maximum is enforced before review |
| Administrator alert email for message limits | MESSAGE_LIMIT_ADMIN_ALERT_EMAIL_ID | A syntactically valid email address, or omission | Preserve a supplied valid address; omission is handled by the documented default | Request a corrected address when supplied input is invalid; do not replace a supplied valid value |
| Notify recruiter or pool owner about inbound email | ORA_IRC_INBOUND_EMAIL_NOTIFY_RECRUITER_OR_POOL_OWNER | enable, disable, yes, no, on, or off | enable, yes, and on become selected; disable, no, and off become unselected | Reject other business input; do not emit a native token until artifact verification succeeds |
| Notify recruiter for active job requisitions | ORA_IRC_INBOUND_SMS_NOTIFY_RECRUITER | enable, disable, yes, no, on, or off | enable, yes, and on become selected; disable, no, and off become unselected | Reject other business input; do not emit a native token until artifact verification succeeds |
| Notify the latest sender in a conversation | ORA_IRC_INBOUND_SMS_NOTIFY_SENDER | enable, disable, yes, no, on, or off | enable, yes, and on become selected; disable, no, and off become unselected | Reject other business input; do not emit a native token until artifact verification succeeds |
| Notify hiring managers for active job requisitions | ORA_IRC_INBOUND_SMS_NOTIFY_HM | enable, disable, yes, no, on, or off | enable, yes, and on become selected; disable, no, and off become unselected | Reject other business input; do not emit a native token until artifact verification succeeds |
| Relay email notification to the hiring manager when one exists | ORA_IRC_INBOUND_EMAIL_NOTIFY_HM | enable, disable, yes, no, on, or off | enable, yes, and on become selected; disable, no, and off become unselected | Reject other business input; do not emit a native token until artifact verification succeeds |
| All marketing email categories | ORA_IRC_ALL_EMAIL_MARKETING_CATEGORIES | Omission, All, or the exact ordered nine-code list | ORA_PROSPECT_EMAIL_TEMPLATE,ORA_POOL_EMAIL_TEMPLATE,ORA_PROFILE_EMAIL_TEMPLATE,ORA_EVENT_POOL_NOTIFICATION,ORA_SEND_EVENTINVITE_EXT,ORA_IRC_CAND_POOL,ORA_SEND_INVITE,ORA_IRC_OUTREACH_MESSAGE,BULK_ADHOC_MESSAGE_FROM_LIST_VIEWS | Reject any changed, missing, added, substituted, or reordered code; All uses this field only and does not also set the selected-category field |
| Selected marketing email category | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | Exactly one supported complete label or exactly one supported stored code from the marketing-category mapping | Exactly one mapped stored code | Reject blank, multiple values, partial or fuzzy labels, and values outside the mapping; never store a display label |
| Outbound vanity email categories | ORA_IRC_OUTBOUND_VANITY_EMAIL_CATEGORIES | Optional business selection of zero, one, or multiple notification categories | Selected categories use the no-reply address; unselected categories can use the vanity address when Capture Message is enabled | Do not generate or change the native value until current exports with none, one, and all selections prove the codes and list encoding |
| Process inbound email attachments | ORA_IRC_INBOUND_EMAIL_ATTACHMENT | enable, disable, yes, no, on, or off | enable, yes, and on become selected; disable, no, and off become unselected | Reject other business input; processing also requires the documented two-way-email design condition and artifact-verified native token |
| Maximum size for email messages sent and received | ORA_IRC_EMAIL_MAX_SIZE | Positive whole number of megabytes, using digits only | Supplied number of megabytes for the complete sent or received email, including its body and attachments | Reject zero, signs, decimals, and non-digits; no additional upper bound is authorized |
| Number of days of messages to display | ORA_IRC_INBOX_CONVERSATION_DURATION | Positive whole number of days from 1 through 365, using digits only | Supplied number of days | Reject zero, signs, decimals, non-digits, and values greater than 365 |

## Marketing Category Mapping

Match a complete label case-insensitively after trimming surrounding whitespace. Do not use partial or fuzzy matching.

| Customer Input | Normalized Setting | Normalized Value | Internal Handling |
|---|---|---|---|
| All | ORA_IRC_ALL_EMAIL_MARKETING_CATEGORIES | ORA_PROSPECT_EMAIL_TEMPLATE,ORA_POOL_EMAIL_TEMPLATE,ORA_PROFILE_EMAIL_TEMPLATE,ORA_EVENT_POOL_NOTIFICATION,ORA_SEND_EVENTINVITE_EXT,ORA_IRC_CAND_POOL,ORA_SEND_INVITE,ORA_IRC_OUTREACH_MESSAGE,BULK_ADHOC_MESSAGE_FROM_LIST_VIEWS | Use the complete ordered list and do not also set ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES |
| Outreach Messages - Start Outreach Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_IRC_OUTREACH_MESSAGE | Use exactly this one code |
| User-Defined Content - Send Message Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | BULK_ADHOC_MESSAGE_FROM_LIST_VIEWS | Use exactly this one code |
| Prospect Candidate Notification - Send Message Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_PROSPECT_EMAIL_TEMPLATE | Use exactly this one code |
| Candidate Profile Notification - Send Message Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_PROFILE_EMAIL_TEMPLATE | Use exactly this one code |
| Candidate Pool Member Notification - Send Message Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_POOL_EMAIL_TEMPLATE | Use exactly this one code |
| Send Event Invite Notification - Add to Event Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_SEND_EVENTINVITE_EXT | Use exactly this one code |
| Candidate Pool Job Notification - Promote Requisition to Pool Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_IRC_CAND_POOL | Use exactly this one code |
| Send Invite Notification - Add to Requisition and Send Invite Actions | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_SEND_INVITE | Use exactly this one code |
| Event Pool Member Notification - Send Message Action | ORA_IRC_SELECTED_EMAIL_MARKETING_CATEGORIES | ORA_EVENT_POOL_NOTIFICATION | Use exactly this one code |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supported requested change | At least one country-permission field group or supported messaging setting listed above | Ask which supported business setting should change | The requester supplies the business setting and intended value | Every request |  |
| Country permission identity | Country plus SMS, WhatsApp, or WA; ThrottleLimit is optional | Ask only for a missing country or channel | Resolve or validate the country automatically and normalize the supported channel | A country permission is requested | resolve_phone_country_code |
| Messaging setting value | One supported setting and a value satisfying its business contract, unless an executable default applies | Apply only an authorized default; otherwise ask for a value required by the requested change | Validate against Supported Messaging Settings; artifact-gated native encodings use the local verifier | A messaging setting change is requested | verify_messaging_setting_value |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A country name, territory code, or numeric phone-country code is supplied | Continue only after the active-country contract returns an acceptable result | Resolve a name or territory code automatically; validate numeric input against the same active list | resolve_phone_country_code |
| A checkbox or outbound-vanity category setting is requested | Business intent may validate, but the affected native value remains blocked until its exact current representation is proved | Obtain the required release-matched task exports; preserve independently valid settings | verify_messaging_setting_value |
| All requested business inputs pass and any affected artifact gates are satisfied | Satisfied | Continue to defaults and design enforcement |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Reject unlisted fields | Omit the field and give the supported-scope guidance; never invent a mapping or behavior | A requested field is absent from the supported tables |  |
| Resolve country input | Require the documented active exact-match behavior and digits-only result | A country permission is requested | resolve_phone_country_code |
| Require a supported channel | Normalize SMS, WhatsApp, or WA and reject every other value | A country permission is requested |  |
| Validate documented input shapes | Apply only the email, checkbox, positive-whole-number, list, and day-range contracts above | A supported value is supplied |  |
| Normalize marketing labels | Map only All or one complete supported label; never store the display label | A marketing-category label is supplied |  |
| Preserve product behavior on omission | Omit maximum email size and inbox duration when not requested; do not synthesize product/UI values | Either setting is omitted |  |

## Explicitly Unsupported Input

| Requested Category | Customer Guidance | Internal Action |
|---|---|---|
| Provider name, description, selection, account, sender ID, URL, method, authentication, headers, body mapping, provider message length, status, activation, or test | This provider setting cannot be included in the proposed change. Use the approved provider setup process. | Do not map, retain, test, activate, or include the field |
| Credential, token, password, client secret, certificate, credential reference, or other secret | This information must be handled through the approved secure configuration process. | Stop; do not request, copy, repeat, persist, or include the value |
| Email provider, connection, IMAP, OAuth, mailbox, vanity-address setup, no-reply-address setup, endpoint, or connection test | This email connection setting cannot be included in the proposed change. Use the approved email setup process. | Do not infer or create an integration |
| Blocked-phone upload, Text Assistant, provider or general channel activation, or another unlisted task field | This setting cannot be included in the proposed change. Use the approved manual setup process or ask an administrator. | Stop the affected field and do not infer a mapping |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| IRCMSG.VALIDATE.REQUEST | decision | 10 | validate_input | valid->IRCMSG.LOOKUP.COUNTRY;unsupported->IRCMSG.ERROR.UNSUPPORTED;invalid->IRCMSG.ERROR.INPUT;blocked->IRCMSG.ERROR.INPUT | none | stop | Every Recruiting Messaging Configuration request | all |
