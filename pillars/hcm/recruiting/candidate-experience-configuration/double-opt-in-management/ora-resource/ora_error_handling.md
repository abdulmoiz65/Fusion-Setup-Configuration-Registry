# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Duplicate country codes | Show error key IRC_CSP_CONTEXT_UNIQUEVALUES, do not commit, and remove or change the duplicate country. Resolved message text is unresolved; see Open Undocumented Items. |
| Required country blank | Stop before commit and complete the selection. If hcmCountriesLov `findByWord` could not resolve the supplied country, request its exact TerritoryCode instead of guessing. Exact required-field message is unresolved; see Open Undocumented Items. |
| Missing task access | Stop and route to the security owner. |
| No supported customer API or test action | Do not infer an internal endpoint or test action. Supported external read or validation API is unresolved; see Open Undocumented Items. |
| Derived-ID anchor, collision, or stale export | Stop before preflight. Do not submit or retry the archive; obtain the required fresh export and rebuild only when the derived-ID checks pass. |
| Derived-ID overflow or nonnumeric source ID | Stop package preparation. A SettingValueId must be a positive decimal integer with no more than 18 digits. |
| Unresolved SettingValueId | Stop package preparation and request the exact SettingValueId. User-facing error text must not reveal internal seed IDs, derived IDs, or allocation formulas. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INVALID | A country selection is blank, unrecognized, or duplicates another selected TerritoryCode | Correct the country selection before retrying Save and Close |
| AUTHORIZATION | The user cannot open the FSM task | Stop and route to the security owner |
| PRODUCT_CAPABILITY_GAP | No supported customer API or dedicated test action is documented | Do not use an internal-only endpoint; obtain the documented manual or public validation contract |
| INPUT_VALIDATION | The derived-ID anchor is missing or ambiguous, a candidate collides, or a value is nonnumeric or exceeds 18 digits | Correct the input/export condition and rebuild the archive; do not substitute an arbitrary ID |
| STALE_BASELINE | The second export changes the mode anchor or fallback state used to build the archive | Discard the archive and restart derived-ID allocation from the second export |
| IDENTITY_RESOLUTION | A required SettingValueId cannot be resolved safely | Request the exact SettingValueId without exposing internal allocator values |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before retrying a duplicate or invalid country save | The affected country selection and the required correction |
| When a SettingValueId cannot be resolved | Request the exact SettingValueId. Do not show internal seed IDs, derived IDs, allocation formulas, or internal anchor state. |
| Before any automation or API validation | The source states that no supported customer API is documented and the internal-only endpoint must not be used |
| After a successful GLOBAL or LIST_OF_REGIONS configuration | Inform the user: Make sure the Recruiting Notification Library for Double Opt In Confirmation is configured. This is a follow-up reminder, not a task dependency or completion blocker. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A supported external API is not documented | Do not use recruitingUISettings or infer another internal endpoint as a customer integration contract |
| Notification prerequisite enforcement is not confirmed | Do not present notification content as a verified task-level gate |
| A Global or regional configuration succeeds | Do not block the successful configuration, modify notification content, or imply that the notification library was validated; show only the documented follow-up reminder |

## Open Undocumented Items

| TBD ID | Missing Fact | Owner | Blocker | Next Action |
|---|---|---|---|---|
| DOI-TBD-01 | Resolved text for IRC_CSP_CONTEXT_UNIQUEVALUES | Recruiting Engineering or localization owner | User-facing error copy | Inspect the message-bundle entry. |
| DOI-TBD-02 | Exact required-field and invalid LOV error behavior | Recruiting Engineering | Error-handling detail | Inspect runtime validation or additional source. |
| DOI-TBD-03 | Supported external read or validation API | Product/API owner | Automation | Confirm a public API contract; do not use the internal-only endpoint. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOI.INFORM_NOTIFICATION_LIBRARY | step | 55 | execution_gate | informed->DOI.RETURN_SUCCESS | DOI.APPLY_MODE_DEFAULT | continue | A GLOBAL or LIST_OF_REGIONS configuration commits successfully |
| DOI.HANDLE_ACCESS_ISSUE | step | 60 | error_handler | disclosed->RETURN_ISSUES | DOI.CHECK_READINESS | stop | FSM task access is unavailable |
| DOI.HANDLE_INPUT_ISSUES | step | 70 | error_handler | disclosed->RETURN_ISSUES | DOI.VALIDATE_INPUT | stop | A required country selection is blank or invalid |
| DOI.HANDLE_DESIGN_ISSUE | step | 80 | error_handler | disclosed->RETURN_ISSUES | DOI.ENFORCE_REGION_DESIGN | stop | A regional design rule blocks Save and Close |
| RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A task gate fails |
| DOI.RETURN_NO_OPT_IN | terminal | 115 | terminal | none | DOI.APPLY_MODE_DEFAULT | stop | Save and Close completes with no Double Opt In |
| DOI.RETURN_SUCCESS | terminal | 120 | terminal | none | DOI.INFORM_NOTIFICATION_LIBRARY | stop | Save and Close commits, shows the notification-library reminder for GLOBAL or LIST_OF_REGIONS, and returns to Setup Manager |
