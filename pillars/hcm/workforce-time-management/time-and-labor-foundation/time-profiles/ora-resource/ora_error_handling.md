# Time Profiles Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and
stop-before-retry behavior. It does not authorize a Fusion write or replace the
provider skill that owns CRUD execution.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required profile, effective date, or core setup input is missing | Stop and request only the missing business value |
| A new or changed Profile Name is not business-oriented, or includes DEV, TEST, UAT, or PROD as a standalone token | Stop and request a meaningful business-purpose name without an environment label. Match environment labels case-insensitively and do not reject an ordinary business word merely because it contains the same letters. |
| A name search matches multiple Time Profiles | Display all matching profile business records and ask the user to select one; do not select a match automatically. |
| Effective-dated history cannot be retrieved for an update or correction | State that the history could not be retrieved, show the verified current profile state and current group assignments, and continue to the normal update summary and approval flow. |
| A create request has suitable similar profiles | Show suitable and unsuitable Time Profile candidates with business comparison reasons. A differently named profile is still suitable when its description, effective-date applicability, and configuration meet the derived requirement. Ask: “A similar Time Profile already exists. Would you like to use an existing profile or create a new profile?” Do not create, link, or select a profile until the user answers. |
| Enable Time Profile is unavailable, inactive, disabled, or neither effective as Enabled for the current user nor verified as Y at the exact site level when the effective value is unavailable | Stop before profile search, validation, preview, approval, or provider handoff. Show: “Time Profiles can’t continue because Enable Time Profile isn’t enabled for your user or at the site level. Ask your Time and Labor administrator to enable it, then start a new session. This task doesn’t change profile options.” |
| A LOV or selector contains search returns one or more eligible choices without a unique user-selected result | Show the bounded business choices and request one selection; never choose a sample or first result |
| A Time Consumer Set lookup has no exact result | Keep the selected repeating period, use q=Name LIKE '%{search text}%' with only RepeatingTimePeriodId in finder, then, if needed, rerun the same finder without q and show up to five similar Name choices for user selection; do not select a similar consumer automatically. |
| A Payroll Time Type lookup has no normalized exact result | Rerun the same Payroll Time Type finder context without SearchTerm, show up to five similar DisplayValue choices, and require the user to select or refine; do not construct a payroll element from the requested text. |
| Another LOV or selector contains search returns no eligible choices | Show up to five bounded closest business choices from the same eligible domain; if no closest choices are available, ask for a refined search term |
| Existing-profile name search or item read returns zero matches, multiple matches without a user selection, or a mismatched result | Stop and request a refined name, a selection from the displayed case-insensitive contains matches, or a verified TimeProfileId; never choose a sample or first result. |
| Consumer Set becomes invalid after Time Card Period changes | Clear the stale value and require reselection |
| Assignment validation returns messages | Show the affected assignment and sanitized message, then stop |
| Live describe, lookup, or current-state read is unavailable | Stop at the failed read stage; do not guess fields, mappings, keys, or current values |
| Authentication remains invalid after one workflow-permitted refresh | Stop and require reauthentication |
| Required REST privilege is denied | Stop and report the missing access without changing routes |
| Target environment cannot be reached | Stop and report the environment and failed stage |
| Data Loader DAT generation, DAT validation, or ZIP validation fails | Stop in core.data-loader, preserve the provider result, and correct the artifact before approval |
| Required Time Profiles task guidance or fresh live Data Loader metadata/sample evidence was not reviewed before DAT creation | Stop before DAT creation; review the selected task SKILL.md, applicable ora_* rules, and fresh timeProfiles sample headers and attribute details, then rebuild the DAT from the reviewed contract |
| An existing-profile parent context row uses UPDATE because the profile exists | Stop before validation or preview; rebuild the parent timeProfiles context row with RestAction PATCH and regenerate the immutable archive |
| A DAT contains blank placeholder fields or a metadata-only section | Stop before validation or preview; remove every field without a verified value and every section without a populated MERGE row, then regenerate the immutable archive |
| A group assignment DateFrom or DateTo uses a non-ISO date string | Stop before provider preview; correct the date to YYYY-MM-DD, rebuild the immutable archive, validate it, and obtain fresh approval before submission |
| Data Loader upload or initiation fails | Stop in core.data-loader, preserve sanitized provider evidence, and do not substitute direct timeProfiles CRUD |
| Data Loader processing reports failure, partial completion, or uncertain outcome | Preserve the request identifier and provider diagnostics, reconcile through the provider status workflow, and stop before retry |
| Approved asynchronous submission is accepted | Immediately start the task-authorized provider status flow; do not report final success until the provider returns terminal success and the Time Profile read-back verifies the approved supported values |
| Terminal success does not produce exactly one approved-profile collection match or its item read cannot be verified | Stop before final success; do not infer a profile identity or treat acceptance or terminal processing status as verified configuration |
| A terminal-success read-back does not persist every selected feature in its documented business representation | Classify as a verification mismatch, preserve the confirmed and unverified settings, do not report final success, and do not resubmit automatically |
| A terminal-success read-back does not persist selected Web Clock edit access, mobile-only access, geofencing enablement, or conditional geofencing settings | Classify as a verification mismatch, preserve the confirmed and unverified Web Clock settings, do not report final success, and do not resubmit automatically |
| Exactly one active documented parent workflow establishes Time Profiles as a prerequisite | Retain its identity, relevant pending inputs, and safe resume stage; after prerequisite verification, state that it is ready to resume and ask: Would you like to resume {parent workflow}? |
| No active documented parent workflow establishes Time Profiles as a prerequisite | End with the verified standalone Time Profiles result only; do not show a resume prompt or dependent-workflow message |
| Parent contexts are multiple, conflicting, stale, incomplete, or undocumented | Stop and ask the user to identify the intended workflow; do not infer a handoff |
| A prerequisite fails, times out, is partial or uncertain, or fails verification | Preserve the last known result, provide one safe investigation or resume action, and do not offer parent-workflow continuation |
| Data Loader rejects a date-effective profileProperties update | Refresh the exact REST child and fresh live Data Loader metadata; rebuild the DAT with SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, EffectiveEndDate, and effectiveOf as RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD}; populate TimeProfileId with the same value as SetupProfileId, serialize both effective-date fields as YYYY-MM-DD, revalidate the immutable archive, and require fresh approval before retry |
| Data Loader rejects a calendarEventPayrollElements update | Refresh the exact REST child and fresh live Data Loader metadata; rebuild the DAT with SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate, serialize both effective-date fields as YYYY-MM-DD, revalidate the immutable archive, and require fresh approval before retry |
| Data Loader rejects a date-effective create context | Rebuild the create DAT with effectiveOf as RangeStartDate={YYYY-MM-DD}; do not add RangeMode, revalidate the immutable archive, and require fresh approval before retry |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, reference resolution, or defaulting; do not enter the provider-owned approval process and do not place a warning, diagnostic, or technical note in the summary |
| Provider rejects a mutation | Preserve sanitized response evidence and stop before retry |
| A write times out or its outcome is unknown | Do not replay it; reconcile the exact profile and children first |
| Delete Changes lacks an eligible history row or returned profileProperties links | Stop; do not substitute parent DELETE or construct keys |
| Page or source evidence conflicts with live provider metadata | Stop as a catalog mismatch and require authoring review |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required values, ranges, conditional fields, identity, dates, or assignments are invalid | Correct the input and restart validation |
| Catalog mismatch | Describe, source mapping, endpoint contract, or provider metadata is missing or inconsistent | Correct the authoring/provider contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Reauthenticate through the authorized owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment or service cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects a read, validation action, Data Loader request, or provider operation | Preserve sanitized diagnostics and correct the declared issue |
| Process failed | Data Loader or provider execution reaches failure, partial failure, or uncertain completion | Reconcile through the provider-owned status and verification workflow and stop before retry |
| Process timeout | Provider execution does not reach a verifiable outcome within its allowed wait | Stop and retain identifiers for a later status or state check |
| Artifact persistence | The provider cannot preserve the reviewed preview or immutable execution artifact | Correct artifact persistence before approval |
| Approval blocker | Exact environment, operation, preview, or current approval is missing or stale | Regenerate the preview and obtain explicit approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Target environment, operation, stage, failure category, sanitized message, and one safe next action |
| Lookup failure | Business field, supplied display value, match count, and reason without exposing protected identifiers |
| Conditional validation failure | Parent option or value, affected dependent field, rule, and required correction |
| Assignment validation failure | Affected assignment and sanitized provider messages |
| Data Loader or write failure | Operation, safe request identifier when available, confirmed parts, failed parts, unverified parts, and provider-owned reconciliation path |
| Partial or uncertain result | Before state, confirmed after state, unresolved state, and why automatic retry is prohibited |
| Final verified standalone configuration | Submission accepted, terminal request status, verified Time Profiles configuration, user-supplied values without a Default label, actually applied values labeled Default, and no dependent workflow or resume prompt |
| Verified prerequisite with one active parent | Submission accepted, terminal request status, verified Time Profiles configuration, user-supplied values without a Default label, actually applied values labeled Default, parent identity, and the exact resume question; state that the parent workflow has not started or been resubmitted |
| Awaiting or requested resume | Whether the resume prompt is awaiting confirmation or resume_requested; retain the parent identity and safe resume stage without starting the parent |

## Final Completion Result Format

Use this business-facing format only after the task-authorized provider status
flow reaches a terminal result. Do not label a result as successful until both
terminal success and the documented read-back comparison have passed. Populate
the Verified Configuration table only with supported persisted business values:
required values, explicitly selected optional values, and actual defaults.

```md
## Final Result

| Business Outcome | Result |
|---|---|
| Submission | Accepted |
| Final Status | {terminal business status} |

## Verified Configuration

| Business Setting | Verified Value |
|---|---|
| {user-supplied business label} | {verified business display value} |

## Defaults Applied

| Business Setting | Verified Value |
|---|---|
| {defaulted business label} | {verified business display value} Default |
```

For a verified standalone result, end after these sections and state that no
dependent workflow is active. For one verified documented parent prerequisite,
state that the parent is ready but has not started or been resubmitted, then
ask exactly: `Would you like to resume {parent workflow}?` For failure,
timeout, partial success, uncertain outcome, unavailable status, or verification
mismatch, show the last known business result, do not show a verified
configuration, and give one safe investigation or resume action.

## User-Requested Status Result

When a user asks for status for an accepted Time Profiles load, use the
provider-owned status route and respond according to the returned state:

| Provider state | Required response |
|---|---|
| In progress or not yet available | Return the provider status result only. Do not present a final result or verified configuration. |
| Failed, partial, timed out, uncertain, or unavailable | Return the provider status and actionable diagnostics only. Do not present a final result or retry automatically. |
| Terminal success | Immediately run `verify_submitted_time_profile`. When the read-back comparison passes, return the Final Result and Verified Configuration in the same response. Do not require a separate request to show a summary. |
| Terminal success with a verification mismatch | Return the provider status and the verified mismatch. Do not present a successful final result or retry automatically. |

This status behavior applies only when the active Time Profiles workflow can
associate the provider request with one approved profile. It does not alter
generic Data Loader status behavior or create a new submission route.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup, provider contract, identity, key, current state, or effective context is unresolved | Do not infer or invent it |
| A value-source provider is inactive, design-time only, or absent | Do not present it as active runtime behavior |
| Parent DELETE is visible in describe | Do not present it as the active Delete Changes behavior |
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A planned operation, target, preview, or source bytes change | Do not reuse earlier approval |
| Fusion rejects a date-effective profileProperties update | Do not retry the same archive; refresh the exact REST child and fresh live metadata, then rebuild with SetupOptionValId, TimeProfileId, SetupProfileId, EffectiveStartDate, EffectiveEndDate, and effectiveOf as RangeMode=UPDATE;RangeStartDate={YYYY-MM-DD}, populating TimeProfileId with the same value as SetupProfileId and serializing both effective-date fields as YYYY-MM-DD, before seeking fresh approval |
| Fusion rejects a calendarEventPayrollElements update | Do not retry the same archive; refresh the exact REST child and fresh live metadata, then rebuild with SetupProfileExtraInformationId, EffectiveStartDate, and EffectiveEndDate serialized as YYYY-MM-DD before seeking fresh approval |
| A DAT is created without the required task-guidance and live Data Loader metadata preflight | Do not validate, preview, upload, initiate, or retry it; discard the unreviewed artifact, complete the preflight, rebuild the DAT from the reviewed fields and formats, and obtain fresh approval |
| An existing-profile parent context row uses UPDATE because the profile exists | Do not validate, preview, upload, initiate, or retry it; rebuild the parent context with RestAction PATCH after confirming the live Data Loader mapping |
| A DAT contains blank placeholder fields or metadata-only sections | Do not validate, preview, upload, initiate, or retry it; remove the blank fields and empty sections, regenerate the archive, revalidate it, and obtain fresh approval |
| This consuming skill reaches provider handoff | Do not clone or bypass provider CRUD and execution ownership |
| A Time Profiles CRUD mutation is requested | Do not call direct timeProfiles POST, PATCH, or DELETE; use core.data-loader with businessObject timeProfiles |
| A DAT or ZIP artifact is needed | Do not hand-build or submit it in this consuming skill; let core.data-loader generate, validate, preview, and submit it |
| core.data-loader reaches its approval gate | Do not request a duplicate consuming-task approval for the same immutable archive |
| Source data, payload, archive, selected configuration, or any approval-relevant value changes | Do not retain the prior approval; rebuild the immutable preview and obtain new current explicit approval before submission |
| Final completion fails, times out, is partial, uncertain, unavailable, or mismatched | Do not upload, initiate, import, load, create, update, or retry automatically; preserve the last known status and offer one safe investigation or resume action |
| A parent workflow is identified | Do not start, preview, approve, submit, create, update, import, or load it from this task; return resume_requested only after the user confirms the exact resume prompt |
| Diagnostics or evidence are returned | Do not expose credentials, tokens, complete protected payloads, tenant-specific sample IDs, or opaque URLs |
| A Complete Summary is presented | Do not expose identifiers, codes, keys, internal values, opaque links, request details, fingerprints, service or payload terms, field or column names, resolver or rule names, task-node names, technical file names, raw boolean values, diagnostics, or warnings |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TP.ROUTE | decision | 25 | execution_gate | read_complete->TP.DONE_READ;mutation_ready->TP.PROVIDER_SUBMISSION;mutation_blocked->TP.ERROR | TP.DATALOADER_METADATA | stop | Select read-only completion or the provider-owned approved mutation handoff after the required Data Loader metadata preflight passes |
| TP.PROVIDER_SUBMISSION | decision | 28 | execution_gate | accepted->TP.FINAL_STATUS;not_accepted->TP.ERROR;approval_invalidated->TP.ERROR | TP.ROUTE | stop | Route normalized verified fields to core.data-loader for DAT generation, immutable archive validation, preview, approval, and one submission; proceed only when the provider reports that the approved asynchronous request was accepted |
| TP.RESUME_PROMPT | decision | 32 | execution_gate | awaiting_confirmation->TP.AWAITING_RESUME_CONFIRMATION;confirmed->TP.RESUME_REQUESTED;approval_invalidated->TP.ERROR | TP.PARENT_CONTEXT | stop | Present exactly: Would you like to resume {parent workflow}? On confirmation, return resume_requested with the retained parent identity and safe resume stage; never start the parent here |
| TP.ERROR | step | 36 | error_handler | stopped->TP.BLOCKED | none | stop | Any prior node returns missing, invalid, unsupported, unresolved, selection_required, ambiguous, blocked, failed, partial, timed-out, stale, mismatched, uncertain, unavailable, or provider_gap |
| TP.DONE_READ | terminal | 27 | terminal | none | TP.ROUTE | continue | Requested read, history, or validation completed without a configuration change |
| TP.DONE_MUTATION | terminal | 33 | terminal | none | TP.PARENT_CONTEXT | continue | Verified standalone configuration: submission accepted, terminal success status, and persisted supported approved values verified; no dependent workflow exists |
| TP.AWAITING_RESUME_CONFIRMATION | terminal | 34 | terminal | none | TP.RESUME_PROMPT | continue | Prerequisite verified and ready to resume one documented parent workflow; the resume prompt is awaiting user confirmation and the parent has not started or been resubmitted |
| TP.RESUME_REQUESTED | terminal | 35 | terminal | none | TP.RESUME_PROMPT | continue | Return resume_requested with retained parent identity and safe resume stage; the parent workflow has not started or been resubmitted |
| TP.BLOCKED | terminal | 37 | terminal | none | none | stop | The request cannot safely continue without correction, provider reconciliation, or documented read-back verification |

## Source Basis

- 03-authoring-guardrails.md
- 05-crud-lifecycle-behavior.md
- 06-rest-describe-evidence.md
- Repository workflow error-handling and approval discipline
- Developer-provided authoring directive: Time Profile identity lookup uses GET {BASE}/timeProfiles?q=ProfileName='{exact Profile Name}'; do not use LIKE, contains matching, or Advanced Search
- Developer-provided authoring directive: use core.data-loader with businessObject timeProfiles for CRUD mutations
- Developer-provided authoring directive: serialize every populated EffectiveStartDate and EffectiveEndDate as YYYY-MM-DD; reject every other representation before validation or preview
- Developer-provided authoring directive: serialize group assignment DateFrom and DateTo as ISO YYYY-MM-DD and fail closed before preview when either date is non-ISO
- Developer-provided authoring directive: require a business-only Complete Summary before the provider-owned approval process
- Developer-provided authoring directive: task-authorized post-submission status monitoring, persisted-state verification, and documented parent-workflow resume semantics
- Developer-provided authoring directive: all Time Profiles LOV and selector searches use bounded contains or LIKE matching, present eligible choices, and offer bounded closest choices when the contains search returns none
- Developer-provided authoring directive: before creating every Time Profiles DAT, review the selected task guidance and fresh live Data Loader metadata/sample headers and attribute details; use the reviewed field set, key form, and value formats without inference
- Developer-provided authoring directive: when an existing-profile DAT requires a timeProfiles parent context row, set RestAction to PATCH; never infer UPDATE from the profile's existence or lifecycle label
- Developer-provided authoring directive: emit only DAT fields with verified values and only sections with a populated MERGE row; reject blank placeholder columns and metadata-only sections before validation or preview
