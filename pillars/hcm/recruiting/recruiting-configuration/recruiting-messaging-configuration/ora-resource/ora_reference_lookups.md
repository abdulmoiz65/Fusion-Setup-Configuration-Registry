# Recruiting Messaging Configuration Reference Lookups

The country resolver is read-only and runs automatically only for a country-permission request. The native-value verifier reads approved local task artifacts only. Neither resolver authorizes a configuration change.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_messaging_setting_value | A checkbox or outbound-vanity category setting requires a native stored value | Exact setting code and stored value from successful current release-matched task data and template exports | Require an exact setting-code match and preserve the exported native representation without translation; the artifact identity must satisfy the current-evidence gate | Artifact-verified native proposed value and its immutable source-artifact identity | Stop only the affected setting and request the exact current task-export evidence; never guess a token, code, label, delimiter, ordering, All representation, or omission behavior |

## Artifact-Gated Local Values

| Affected Configuration | Status | Missing Evidence | Owner | Blocker | Next Action |
|---|---|---|---|---|---|
| ORA_IRC_INBOUND_EMAIL_NOTIFY_RECRUITER_OR_POOL_OWNER | TBD — artifact verification required | Exact selected and unselected strings emitted by the current release-matched task export for this setting code | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation for this setting only | Export selected and unselected states and record the exact stored strings with the complete artifact identity |
| ORA_IRC_INBOUND_SMS_NOTIFY_RECRUITER | TBD — artifact verification required | Exact selected and unselected strings emitted by the current release-matched task export for this setting code | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation for this setting only | Export selected and unselected states and record the exact stored strings with the complete artifact identity |
| ORA_IRC_INBOUND_SMS_NOTIFY_SENDER | TBD — artifact verification required | Exact selected and unselected strings emitted by the current release-matched task export for this setting code | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation for this setting only | Export selected and unselected states and record the exact stored strings with the complete artifact identity |
| ORA_IRC_INBOUND_SMS_NOTIFY_HM | TBD — artifact verification required | Exact selected and unselected strings emitted by the current release-matched task export for this setting code | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation for this setting only | Export selected and unselected states and record the exact stored strings with the complete artifact identity |
| ORA_IRC_INBOUND_EMAIL_NOTIFY_HM | TBD — artifact verification required | Exact selected and unselected strings emitted by the current release-matched task export for this setting code | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation for this setting only | Export selected and unselected states and record the exact stored strings with the complete artifact identity |
| ORA_IRC_INBOUND_EMAIL_ATTACHMENT | TBD — artifact verification required | Exact selected and unselected strings emitted by the current release-matched task export for this setting code | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation for this setting only | Export selected and unselected states and record the exact stored strings with the complete artifact identity |
| ORA_IRC_OUTBOUND_VANITY_EMAIL_CATEGORIES | TBD — artifact verification required | Exact category codes, delimiter, ordering, persisted representation of All, and omission behavior from current exports with none, one, and all categories selected | Resource Authoring Engineering Owner | Mutation of this setting only | Capture the three export states and record the native values with the complete artifact identity |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_phone_country_code | An exact country name, exact two-character territory code, or exact digits-only phone-country code is supplied for an SMS or WhatsApp country permission | Target environment active HCM Countries List of Values | /hcmRestApi/resources/{version}/hcmCountriesLov | AlternateTerritoryCode, CountryName, CurrencyCode, Description, NlsTerritory, ObsoleteFlag, PhoneCountryCode, PhoneCountryCodeId, TerritoryCode | Retrieve candidates with finder findByWord;DataSecurityPrivilege=false, onlyData=true, a bounded limit, and the listed fields. Escape user-supplied query literals. For a name or territory code, trim and compare case-insensitively against CountryName or the exact two-character TerritoryCode, require ObsoleteFlag=false, and require exactly one exact match. For digits-only numeric input, require at least one active row with that exact PhoneCountryCode. A finder or wildcard candidate is never final resolution. Do not infer partial matches; accept an additional alias only from a separately approved alias table. | Digits-only PhoneCountryCode without a plus sign or decimal; also fill the resolved display country for a unique name or territory-code match | For zero or multiple exact active name or territory-code matches, request a more exact supported input. For numeric input with no active row, request an exact active digits-only code. Do not infer a value or request lookup evidence. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Country input is present | The owning workflow invokes resolve_phone_country_code automatically through its approved read-only binding; the customer supplies no binding, receipt, release, timestamp, or numeric code when a name or territory code resolves uniquely |
| Candidate rows are returned | Apply the exact active-match rule locally; do not accept the first finder or wildcard result |
| Country name or territory code resolves once | Return the digits-only phone-country code and resolved display country |
| Numeric phone-country code is supplied | Validate that at least one active row has that exact code and return the same digits-only code |
| Country input has no acceptable result or an ambiguous named result | Stop only that country permission and request a more exact supported input; preserve unrelated valid settings |
| The approved binding is missing, unauthorized, unavailable, returns an incompatible shape, or cannot establish a complete candidate set | Classify a system-side lookup readiness failure, stop only the affected permission, record a sanitized diagnostic, and have the owning workflow restore or verify the approved read-only contract; do not ask the customer to change an otherwise valid country input |
| Live lookup succeeds | Record the target environment identity, release or build, lookup timestamp, supplied input, active match count, and resolved code; do not persist or expose raw payloads |
| Native-value artifact is absent, stale, unsuccessful, or incompatible | Keep the business intent but block only the affected native setting value until exact current evidence is supplied |
| Any resolver is used | Perform no write, retry no mutation, and disclose no secret, credential, authentication header, raw payload, or unrelated customer value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| IRCMSG.LOOKUP.COUNTRY | decision | 12 | reference_lookup | resolved->IRCMSG.DEFAULT.ADMIN_ALERT_EMAIL;not_required->IRCMSG.DEFAULT.ADMIN_ALERT_EMAIL;no_match->IRCMSG.ERROR.INPUT;ambiguous->IRCMSG.ERROR.INPUT;unavailable->IRCMSG.ERROR.INPUT | IRCMSG.VALIDATE.REQUEST | stop | A country permission requires resolution or validation; otherwise return not_required without calling Fusion | all |
