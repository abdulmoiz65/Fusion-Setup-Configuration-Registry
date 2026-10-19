# Recruiting Messaging Configuration Error Handling

Use business language in normal responses. Internal codes, native import details, package structure, fingerprints, and lookup mechanics appear only in requested technical diagnostics. Every failure stops safely before a configuration change.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required business information is missing | Ask only for the missing business value and do not expose an implementation field name |
| A requested field or action is unsupported | Explain that the field cannot be included, omit it, and direct the requester to the approved setup process; do not create a mapping, action, lookup, test, or activation |
| A country input is missing | Ask for an exact country name, exact two-character territory code, or exact digits-only phone-country code |
| A country name or territory code has no exact active match or is ambiguous | Explain that the country could not be resolved uniquely and request a more exact supported input; do not ask for an internal lookup receipt |
| A numeric phone-country code has no active match | Ask for an exact active digits-only phone-country code; do not add a plus sign or infer another country |
| The approved country lookup is missing, unauthorized, unavailable, incompatible, or incomplete | Treat this as a system-side lookup readiness failure, stop only the affected permission, preserve the supplied country input, and have the owning workflow restore or verify the approved read-only contract; do not ask the customer for another country merely because the system lookup failed |
| A supplied value fails a verified rule | Name the affected business setting, state the business rule, and request a corrected value without silently changing it |
| A message-limit relationship cannot be evaluated | Identify both related business settings and request the missing current peer value or a corrected proposed value |
| A native setting value is artifact-gated | Explain that only the affected setting cannot be prepared safely until the implementation owner supplies current task-export evidence; preserve unrelated valid settings |
| Two-way-email status blocks attachment processing | If disabled, direct the requester to the approved email setup process; if unknown, ask the implementation owner to verify current enablement and block only attachment processing |
| Current task-artifact identity is incomplete, unsuccessful, stale, or incompatible | Stop before describing the proposal as current and request successful release-matched data and template artifacts with the complete evidence tuple |
| Package structure or component effect cannot be proved | Stop the affected proposal, preserve every exported member, and obtain exact release evidence; omission never authorizes deletion |
| A secret or protected value is supplied | Stop; do not retain, repeat, persist, or place it in a proposal, diagnostic, or authoring file; use the approved secure configuration process |
| The proposal is stale, unexpected, materially changed, or unapproved | Stop, rebuild the redacted proposal, and obtain fresh exact approval before returning it to the owning workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing information | A required business setting, country, channel, or requested value is absent | Request only the missing business value |
| Unsupported input | A provider, connection, activation, test, credential, blocked-phone upload, Text Assistant, or unlisted field/action is requested | Omit the affected field and use the approved setup process |
| Invalid input | A supplied value fails the documented shape, range, list, uniqueness, enablement, or field relationship | Request a corrected business value and preserve the original intent |
| Artifact evidence gap | An exact native encoding, package mapping, or current artifact identity is unproved | Stop only the affected path and obtain the named task-export evidence |
| Country match failure | The approved active-country lookup completes but has no acceptable exact result or has an ambiguous name or territory-code result | Ask for a more exact supported country input; do not infer a code |
| Lookup readiness failure | The approved binding is missing, unauthorized, unavailable, incompatible, or cannot establish a complete candidate set | Stop only the affected permission, retain the valid supplied input, record a sanitized system diagnostic, and restore or verify the read-only contract through the owning workflow |
| Package-semantics blocker | The requested effect depends on unproved member placement, replacement, merge, or deletion behavior | Compare current release-matched artifacts and do not construct or delete the affected path |
| Security | A secret, credential, authentication material, protected value, or raw sensitive payload is supplied | Stop and use the approved secure configuration process |
| Review or approval blocker | The proposal is stale, unexpected, changed, or lacks exact approval | Rebuild, review, and obtain fresh approval for the exact target and proposal |

## Customer Response Rules

| Situation | Customer-Facing Wording Rule | Internal Behavior |
|---|---|---|
| Supported country permission | State that SMS or WhatsApp permission for the named country will be prepared and that no change has been applied | Resolve the country automatically and normalize the channel; never describe this as provider or general channel activation |
| Administrator alert email omitted | State that the proposed administrator alert email is admin_alerts@invalidemail.com and that no change has been applied | Apply the default only to MESSAGE_LIMIT_ADMIN_ALERT_EMAIL_ID and only when omitted |
| All marketing categories omitted | State that the proposal includes all supported marketing email categories and that no change has been applied | Apply only the exact complete ordered list to ORA_IRC_ALL_EMAIL_MARKETING_CATEGORIES |
| Unsupported setting | State that the named business setting cannot be included and identify the approved setup process as the next action | Omit the field and never disclose or invent a technical mapping |
| Invalid message limit | State that the named setting must be a positive whole number and must satisfy its relationship to the related business setting | Return the applicable input or relationship failure without exposing setting codes |
| Artifact-gated setting | State that the setting cannot be prepared safely until the implementation owner confirms its current format | Identify the exact missing artifact evidence in technical diagnostics only |
| Proposal ready for review | Present the proposed business changes and ask for review; state that no changes have been applied | Bind approval to the exact redacted proposal and target environment |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation result | Supported business setting names, sanitized proposed values, and each missing, unsupported, or invalid business value |
| Design result | Each relationship, evidence, enablement, scope, and package rule that passed or blocked, plus one safe correction |
| Artifact gate | The affected configuration path, exact missing evidence, owner, blocking scope, and next action; do not expose hashes or raw artifact content |
| Review gate | Exact target environment, intended business effect, sanitized proposed changes, unchanged scope, full component-specific replacement effects, and confirmation that no live change has occurred |
| Failure | Failure category, affected business setting, redacted evidence, and one safe next action |

## Review and Approval Gate

| Requirement | Required Result | If Not Satisfied |
|---|---|---|
| Supported scope | Every included field and value is documented and every unsupported request is disclosed | Stop the affected request and rebuild the proposal |
| Current artifacts | The exact successful data and template artifacts have the complete immutable evidence tuple and are compatible with the destination | Stop; obtain current release-matched artifacts |
| Package verification | The preserved ZIP and every CSV member are accounted for, and each add, replace, or update effect is shown without invented names or mappings | Stop; compare the exact export and do not reconstruct or delete |
| Sanitized preview | The exact target, requested business changes, unchanged scope, and replacement effects are visible without secrets or raw sensitive values | Stop and rebuild a redacted preview |
| Exact approval | The requesting owner approves that exact target and exact proposal | Stop; a material change invalidates approval and requires fresh review |
| Required reviewers | Oracle Recruiting Functional Product Owner and Fusion Setup Migration and Resource Authoring Engineering Owner review the proposal; Recruiting Security Owner reviews only when authorization or secure configuration is involved | Stop until the applicable reviewers complete the exact review |
| Execution boundary | The result returns only to the owning setup-task workflow | Do not import, activate, test, call a write action, or claim that a change occurred |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unsupported field or action | Do not infer a mapping, endpoint, service, default, test, activation, provider configuration, credential field, or import behavior |
| Artifact-gated native value | Do not substitute a guessed token, UI label, category code, delimiter, ordering, All representation, package member, or field mapping |
| Positive-whole-number contract | Do not allow decimals, signs, zero, or an unsupported upper bound; do not interpret blank as zero, unlimited, deletion, or a default |
| Product or UI value | Do not emit 20 MB, 180 days, or no vanity-category selections as an import fallback |
| Deletion or obsoletion request | Do not infer a delete token, row omission, merge rule, replacement rule, package member, or native operation; require a separately verified native operation and separate exact approval |
| Secret or protected data | Do not request, retain, display, persist, or place it in a proposal or generated resource |
| Unapproved or changed proposal | Do not return it for execution and do not reuse stale approval |
| Execution uncertainty | Do not retry a write, invent a success check, or claim success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| IRCMSG.GATE.REVIEW | decision | 30 | execution_gate | approved->RETURN_SUCCESS;blocked->IRCMSG.ERROR.REVIEW | IRCMSG.ENFORCE.DESIGN | stop | A complete redacted proposal is ready for exact review and approval | all |
| IRCMSG.ERROR.UNSUPPORTED | step | 40 | error_handler | handled->RETURN_ISSUES | none | stop | A requested field or action is unsupported | all |
| IRCMSG.ERROR.INPUT | step | 50 | error_handler | handled->RETURN_ISSUES | none | stop | Validation, lookup, artifact readiness, or design enforcement is blocked | all |
| IRCMSG.ERROR.REVIEW | step | 60 | error_handler | handled->RETURN_ISSUES | none | stop | The proposal is stale, unexpected, changed, unapproved, or violates a package rule | all |
| RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A documented issue was disclosed with one safe next action | all |
| RETURN_SUCCESS | terminal | 80 | terminal | none | IRCMSG.GATE.REVIEW | stop | Resource checks and exact review completed; this does not mean a Fusion change was applied | all |
