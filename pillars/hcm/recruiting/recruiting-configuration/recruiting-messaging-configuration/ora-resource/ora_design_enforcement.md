# Recruiting Messaging Configuration Design Enforcement

These rules gate a review-ready proposal. They preserve the requested business intent, block only affected paths when evidence is missing, and never apply a configuration change.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 10 | Confirm current task evidence | Require successful release-matched data and template exports and the complete immutable evidence tuple before treating a proposal as current |
| 20 | Confirm supported scope | Retain only documented country-permission fields and messaging setting codes; preserve every unlisted configuration area unchanged |
| 30 | Enforce business relationships | Evaluate country/channel uniqueness, optional-limit behavior, message-limit relationships, attachment enablement, and native-value evidence without silently changing values |
| 40 | Enforce package safety | Preserve the exported ZIP structure and every CSV member, apply the verified component effect, and keep unproved native fields or removal behavior artifact-gated |
| 50 | Prepare exact review | Produce a redacted proposal showing the target environment, intended business effect, unchanged scope, and every replacement effect; no live change has occurred |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A country permission is proposed | Error | resolve_phone_country_code | Country resolution is not acceptable, the channel is not SMS or WhatsApp, or the normalized PhoneCountryCode plus ChannelTypeCode pair is duplicated | Resolve or validate the country through the active list, use the verified channel code, and retain one row per pair | Normalize only from the documented exact lookup result and channel mapping; never infer or silently deduplicate |
| ThrottleLimit is supplied | Error |  | The value is not a positive digits-only whole number greater than zero | Request a positive whole number; no upper limit is imposed | No silent value change |
| ThrottleLimit is omitted | Error |  | The proposal interprets omission as zero, unlimited, deletion, a default, or inheritance | Leave the field absent for a new permission and omit it for an unrelated update so the current value is preserved | Yes; remove only the invented value or deletion meaning |
| Either RECRUITING_WIDE_OUTBOUND_SMS_SOFT_LIMIT or RECRUITING_WIDE_OUTBOUND_SMS_HARD_LIMIT changes | Error |  | The resulting SMS warning threshold is not lower than the resulting SMS system-wide maximum, or either peer value needed for comparison is unavailable | Compare proposed values with the unchanged current peer value and require a positive whole-number warning threshold lower than the maximum | No silent value change; obtain the missing current peer value when needed |
| Either CANDIDATE_OUTBOUND_SMS_HARD_LIMIT or RECRUITING_WIDE_OUTBOUND_SMS_HARD_LIMIT changes | Error |  | The resulting SMS per-candidate maximum exceeds the resulting SMS system-wide maximum, or either peer value needed for comparison is unavailable | Compare proposed values with the unchanged current peer value and require the per-candidate maximum not to exceed the system-wide maximum | No silent value change; obtain the missing current peer value when needed |
| Either RECRUITING_WIDE_OUTBOUND_WHATSAPP_SOFT_LIMIT or RECRUITING_WIDE_OUTBOUND_WHATSAPP_HARD_LIMIT changes | Error |  | The resulting WhatsApp warning threshold is not lower than the resulting WhatsApp system-wide maximum, or either peer value needed for comparison is unavailable | Compare proposed values with the unchanged current peer value and require a positive whole-number warning threshold lower than the maximum | No silent value change; obtain the missing current peer value when needed |
| Either CANDIDATE_OUTBOUND_WHATSAPP_HARD_LIMIT or RECRUITING_WIDE_OUTBOUND_WHATSAPP_HARD_LIMIT changes | Error |  | The resulting WhatsApp per-candidate maximum exceeds the resulting WhatsApp system-wide maximum, or either peer value needed for comparison is unavailable | Compare proposed values with the unchanged current peer value and require the per-candidate maximum not to exceed the system-wide maximum | No silent value change; obtain the missing current peer value when needed |
| A notification checkbox or inbound-email-attachment checkbox is requested | Error | verify_messaging_setting_value | A current release-matched export has not proved the exact native selected or unselected string for that exact setting code | Preserve selected or unselected business intent and obtain both current exported states for that setting | Never infer Y/N, true/false, or another token |
| ORA_IRC_OUTBOUND_VANITY_EMAIL_CATEGORIES is requested | Error | verify_messaging_setting_value | Current exports have not proved codes, delimiter, ordering, the representation of All, and omission behavior for none, one, and all selections | Obtain all three current export states before generating a native value | Never reuse marketing codes, store display labels, or infer All or the functional default as a native value |
| ORA_IRC_INBOUND_EMAIL_ATTACHMENT is requested | Error |  | Two-way email is confirmed disabled, or its enablement state is unknown | When disabled, use the approved email setup process first. When unknown, have the implementation owner verify the current state; block only this setting pending that evidence. | Do not invent a dependency, lookup, connection action, or enablement value |
| A review-ready proposal is prepared | Error |  | The exact task data/template evidence is incomplete, unsuccessful, stale, or incompatible with the destination release | Capture the complete immutable evidence tuple from successful current artifacts and recapture it after a release or template-column change | No |
| A package is prepared | Error |  | The exported ZIP structure or any CSV member is removed, reconstructed without evidence, or treated as deletion merely because records are omitted | Preserve the ZIP and every exported CSV. A header-only CSV may represent intentional omission of that member's records. | No automatic reconstruction or deletion |
| General setup-data behavior applies and no component-specific replacement rule overrides it | Error |  | New, changed, unchanged, target-only, or omitted records would be handled contrary to the verified behavior | Create new records, update changed matches, retain unchanged matches and target-only records, and never treat omission as deletion. Deletion or obsoletion requires a separately verified native operation and separate exact approval; this resource does not define that operation. | No |
| A component-specific Recruiting import effect applies | Error |  | The preview does not show the verified add, replace, or update effect, or relies on an unproved SMS-country removal effect | Apply the component behavior below and block only an effect that depends on unproved SMS allowed-country removal or replacement | No |

## Component-Specific Package Behavior

| Configuration Component | Verified Import Effect | Authoring Boundary | Required Review |
|---|---|---|---|
| WhatsApp provider records | Add | Provider configuration, testing, activation, status, accounts, URLs, methods, authentication, headers, and bodies are unsupported; preserve exported provider content without authoring it | Confirm no provider change is introduced by the proposal |
| WhatsApp country permissions | Replace | Author only supported country-permission semantics; native member and field placement require the current task artifacts | Show the complete replacement effect before approval |
| WhatsApp daily limits | Replace | Author only the supported WhatsApp hard, soft, and per-candidate settings | Show the complete replacement effect before approval |
| SMS provider records | Add | Provider configuration, testing, activation, status, accounts, URLs, methods, authentication, headers, and bodies are unsupported; preserve exported provider content without authoring it | Confirm no provider change is introduced by the proposal |
| SMS daily limits | Replace | Author only the supported SMS hard, soft, and per-candidate settings | Show the complete replacement effect before approval |
| SMS allowed-country permissions | Update | Country-permission authoring is supported, but merge versus replacement and deletion behavior are not verified when removals matter | Obtain release-specific evidence and compare source with target before any removal-sensitive proposal |

## Artifact Verification Gates

| Affected Configuration Path | Verified Semantic Contract | TBD Native or Release Evidence | Owner | Blocker | Next Action |
|---|---|---|---|---|---|
| Notification and attachment checkbox settings | Customer intent normalizes to selected or unselected for each documented setting code | Exact selected and unselected native strings for every affected code from successful current release-matched task exports | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Native-value generation only for each affected checkbox | Capture both exported states for every requested code and bind them to the complete artifact identity |
| ORA_IRC_OUTBOUND_VANITY_EMAIL_CATEGORIES | Optional multi-select; no selections is the functional default; selected categories use no-reply and unselected categories can use vanity when Capture Message is enabled | Native category codes, delimiter, ordering, All representation, and omission behavior from none, one, and all current export states | Resource Authoring Engineering Owner | Mutation of this setting only | Capture all three export states and preserve the exact native representation |
| Country-permission ThrottleLimit placement | Omission leaves the optional field absent and never implies a value or deletion; supplied input is a positive whole number | Exact release-matched package member, native field placement, and representation | Oracle Recruiting Functional Product Owner and Resource Authoring Engineering Owner | Construction of the affected native package path | Verify placement in the current task data and template exports without inventing a member or column name |
| Every supported configuration package path | Supported business fields, setting codes, relationships, and component effects are defined | Source environment alias, release/build, resolved task code, data-export process ID and filename, template-export process ID and filename, successful UTC timestamps, SHA-256 values, compatible destination releases, and exact package member/header mappings | Resource Authoring Engineering Owner | Treating a proposal or native package as current | Record the tuple from exact successful artifacts; do not use a vague current-release label or guess any member name or field mapping |
| SMS allowed-country removal or replacement | Allowed countries are updated and omission is not deletion | Release-specific proof of merge, replacement, and deletion behavior when the requested effect depends on removal | Resource Authoring Engineering Owner | Only a removal-sensitive SMS country-permission effect | Export and compare source and target behavior before permitting that effect |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_phone_country_code | A country name, territory code, or numeric phone-country code must be resolved or validated | Active country name, two-character territory code, digits-only phone-country code, active flag, release or build, and lookup timestamp | ora_reference_lookups.md |
| verify_messaging_setting_value | A checkbox or outbound-vanity category setting requires a native stored value | Exact native value emitted for the exact setting code and the complete successful artifact identity | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| IRCMSG.ENFORCE.DESIGN | decision | 20 | design_enforcement | passed->IRCMSG.GATE.REVIEW;blocked->IRCMSG.ERROR.INPUT | IRCMSG.DEFAULT.ALL_EMAIL_MARKETING_CATEGORIES | stop | Validated supported input exists and both executable defaults have been evaluated | all |
