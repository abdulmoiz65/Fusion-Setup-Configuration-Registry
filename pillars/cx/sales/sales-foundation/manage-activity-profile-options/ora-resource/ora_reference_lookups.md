# Activity Profile Options Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| inventory_activity_profile_options_from_reference_export | After fresh export validation | FND_APP_PROFILE_OPTION.csv, FND_APP_PROFILE_VALUE.csv, ORA_FND_APP_PROFILE_OPTION_LEVEL.csv, and ASM_SETUP_CSV_METADATA.xml | Join by exact ProfileOptionName and ApplicationId; require unique definitions, no orphan values or levels, and one unambiguous capability row per code and level | Exported inventory, configured values by scope, level flags, SQL validation, descriptions, row counts, export hash, environment, release, and timestamp | Return failure for duplicate keys, orphan rows, missing metadata, or changed export evidence |
| resolve_documented_activity_profile_option_identity | Inventory or exact option input | Current Oracle Activity guidance and the documented coverage baseline | Accept an exact case-sensitive code or one exact unique documented display-name match | Documented code, display name, source URL, feature, documentation retrieval date | Return invalid for fuzzy or ambiguous names; documentation failure does not invalidate an exact exported code |
| reconcile_documented_and_exported_activity_options | After documentation refresh and export attempt | Documented and exported exact codes | Classify each code as documented-and-exported, documented-live-only candidate, export-only, or unavailable after live probing | Reconciliation counts, code lists, export status, and live status | Never infer live absence or mutation ineligibility from export omission |

## Documented Coverage Baseline

Refresh current Oracle pages when documentation access is available. This
baseline prevents an export-only inventory from silently dropping documented
options and is not a substitute for exact live resolution. Calculate the
candidate count from the rows plus successfully refreshed additions on every
run.

| Activity Area | Profile Option Code |
|---|---|
| Activity search | ZMM_ACTIVITY_ENABLE_ALL_RECORDS |
| External task notifications | ZMM_ACTIVITY_TASKS_EXTERNAL_NOTIFICATION |
| External appointment notifications | ZMM_ACTIVITY_EXTERNAL_NOTIFICATION |
| Company-wide appointment email notifications | ZMM_ACTIVITY_DISABLE_EMAIL_APPT_NOTIF |
| Company-wide task email notifications | ZMM_ACTIVITY_DISABLE_EMAIL_TASK_NOTIF |
| Company-wide appointment notification list | ZMM_ACTIVITY_DISABLE_LIST_APPT_NOTIF |
| Company-wide task notification list | ZMM_ACTIVITY_DISABLE_LIST_TASK_NOTIF |
| Appointment delegation | ZMM_ACTIVITY_APPT_DELEGATION |
| Task delegation | ZMM_ACTIVITY_TASK_DELEGATION |
| Task notification-list reminders | ORA_ZMM_TASK_NOTIF_LIST_REMINDER |
| Task email reminders | ORA_ZMM_TASK_EMAIL_REMINDER |
| Default task reminder period | ORA_ZMM_TASK_DEFAULT_REMINDER |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| ACTIVITY_PROFILE.LOOKUP_PROFILE | resolve_exact_activity_profile_option_and_dependencies | Inventory, Review, Set, Remove, or BulkSet after identity and dependency preflight | Documented or exported ProfileOptionCode, ProfileLevel, UserName or ProductApplicationShortName, ExpectedCurrentValue, proposed display or stored value, and applicable reminder dependency | GET /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}; GET child/profileOptionLevels; GET child/siteProfileOptionValues; GET child/userProfileOptionValues; GET child/productProfileOptionValues; conditionally GET /fscmRestApi/resources/11.13.18.05/profileUsers/{UserName}; conditionally read the related task email or notification-list disable profile through the same profileOptions children; conditionally resolve validation-backed lookup values through an existing Apps Common resolver | Definition fields and SqlValidation; Site, Product, and User enabled/updatable flags; complete configured child rows; UserGuid; related notification channel state; stored code and meaning; timestamps | Require one exact case-sensitive definition, one unambiguous level capability per scope, complete paginated child collections, and one exact selected child row or explicit absence; require one exact user and related channel state when applicable; Inventory probes the documented and exported union; Review and mutation probe the exact selected code and scope key | Environment identity, definition, SqlValidation, level capabilities, configured Site/Product/User rows or absence, exact item key, UserGuid, related channel evidence, stored code and meaning, lookup timestamps, per-code status, source classification, export reconciliation, and deterministic Create, Update, or Delete selection | Return not_found when the definition or required dependency is absent; return many for ambiguous definition, user, application, child, channel, or lookup matches; return failure for systemic auth, authorization, transport, environment, pagination, or response-shape errors; export omission is never a CRUD failure |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exact current-session profileValues match | Return the effective value as optional comparison evidence only; never treat it as the configured child row. |
| No profileValues match | Do not infer Site, Product, or User configuration because security categories can restrict the collection. |
| Inventory candidate | Read the exact definition, level capabilities, and all paginated Site, Product, and User child collections; record explicit absence. |
| Review candidate | Perform the same complete reads for the one exact selected code. |
| Site scope | Use the literal item key SITE. An absent item selects Create; one exact item selects Update or Delete. |
| Product scope | Require one exact application short name and use it as both create LevelValue and item key. Never use an application display name. |
| User scope | Resolve profileUsers/{UserName} exactly. Use UserName as the item key and UserGuid only as create-body LevelValue. Treat zero User rows as explicit absence, not export evidence. |
| Reminder enablement | Read the related task email or notification-list disable profile at Site scope and block when the channel is disabled. |
| Mutation method | Select POST only for an absent Set target, PATCH only for an existing Set target, DELETE only for an existing Remove target, and no write for an absent Remove target. |
| Code omitted from FSM export | Continue exact Apps Common reads. Omission does not block or authorize CRUD and never causes CSV materialization. |
| Lookup-backed value | Accept an exact active stored code or resolve one exact active meaning to its code; show both and send only the stored code. |
| 401 or 403 | Classify as authentication or privilege failure, never not found. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_PROFILE.LOOKUP_PROFILE | step | 3 | reference_lookup | found->ACTIVITY_PROFILE.ROUTE;not_found->ACTIVITY_PROFILE.ROUTE;many->ACTIVITY_PROFILE.RETURN_ISSUES;failure->ACTIVITY_PROFILE.RETURN_ISSUES | ACTIVITY_PROFILE.DEPENDENCIES | stop | Resolve documented and exported candidates against exact live profile, level, configured-value, user, application, notification-channel, and stored-value evidence |
| ACTIVITY_PROFILE.ROUTE | decision | 4 | evaluate_result | proceed->ACTIVITY_PROFILE.DESIGN;blocked->ACTIVITY_PROFILE.RETURN_ISSUES | ACTIVITY_PROFILE.LOOKUP_PROFILE | stop | Proceed for Inventory only with a result or status and complete configured-value evidence for every candidate, Review only with exact definition and complete child reads, or Set, Remove, and BulkSet with deterministic method, exact scope key, current-state lock, Activity dependency closure, and stored-value resolution; block documentation-only results, ambiguous rows, unsupported scope, or unresolved dependencies |
