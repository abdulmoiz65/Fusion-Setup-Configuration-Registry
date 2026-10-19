# Profile Types and Content Section Configuration Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Competing business answers materially change behavior, scope, timing, reuse, or downstream impact | Ask one concise business-language question and stop at review; do not request technical field names |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Evidence, technical identity, exact match, provider contract, preview, approval, persistence, or readback fails | Stop without a substitute route; retain sanitized evidence and request the exact correction or confirmation |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | The target isn't an exact Profiles V2 seeded type, the seeded ID/key pair is mismatched, a custom parent profile type is requested, or type-and-operation support is unconfirmed | Classify as input validation or catalog mismatch and stop before immutable preview or FSM import handoff; preserve the source unchanged and identify the unsupported target or operation |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | An FSM ZIP is structurally valid but its parent, child, or translation rows don't exactly match the approved business scope | Classify as input validation and stop before upload; report the mismatched scope without treating the archive example as a business default |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A supplied subscriber has no exact content-source relationship, subscriber-property rows are orphaned, or a subscriber-property translation has no single base row | Classify as input validation and stop before immutable preview or upload; report the exact profile type, content context, section context, and source code, and require a newly validated archive |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A non-Person section has blank or mismatched parent business keys, populated parent surrogate IDs, no active source template, multiple Person matches, incomplete Person-section pagination, or rewritten ASM_SETUP_CSV_METADATA.xml content | Classify as input validation or catalog mismatch and stop before immutable preview; preserve the source and rejected candidate, disclose the target profile type, failing section and fields, and build a new candidate only through FSM processing from exact resolved parent evidence and source metadata bytes |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A non-Person property response is missing, incompletely paginated, contains an unexpected SourceProfileTypeCode or nonnull Person SourceCode, or produces duplicate or unsupported property metadata | Classify as catalog mismatch and stop before candidate ZIP preparation; identify whether the selected-Person B response or template M response failed, then refresh only the read-only evidence and run a new dry-run |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | The corresponding active Person content section is not found for a non-Person target | Disclose the missing Person prerequisite and ask for explicit approval to include it in the implementation scope. After approval pass the parent-and-target intent to FSM processing; do not construct, order, or import the Person section in this skill, and do not treat scope approval as Core Data Loader execution approval |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Exact seeded ProfileTypeId or SectionContext is unavailable, or no documented exact GET applies | Record duplicate checking as unavailable and stop; do not guess an endpoint, infer parent existence from profileTypeSectionsLOV, or submit |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A read-only verification request includes POST, PUT, PATCH, DELETE, a request body, an action endpoint, setup export/import, or browser fallback | Classify as input validation and reject the request before the Fusion business-resource call; do not split the instruction and execute its read portion as implied approval for a later write |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A verification GET is unavailable, unauthorized, structurally unexpected, or incompletely paginated | Return blocked for the affected verification; do not report not_found, guess a route, reuse the browser HAR's opaque runtime URL, or generalize Person/Job evidence to another seeded type |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Exact duplicate GETs across the candidate sections return zero, one, or multiple rows | Zero exact rows for every candidate clears only the duplicate gate. One exact row for any candidate rejects the entire ZIP, including otherwise-new sections; disclose all duplicates and require a new ZIP excluding them. Multiple exact rows for any candidate are ambiguous and also reject the entire ZIP |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Structured Fusion environment preflight is unavailable | Block preflight and report the missing structured check; do not request screenshots, copied URLs, browser address-bar images, exact reply text, or user attestations |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Quarterly release is absent from trusted metadata | Continue without recording a release; do not ask the user or infer one from API version, hostname, documentation, or date |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | XLSX worksheet prefix collision | Use the valid FSM route when available; otherwise block until the user explicitly requests DAT preparation |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Export task is ambiguous, CSV export isn't supported, source identity or privilege is missing, or filtered criteria aren't confirmed | Classify as input validation, catalog mismatch, or authorization and stop before creating an export process; do not broaden a filtered request |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Export polling times out or the process fails | Persist TaskCode, ProcessId, last status, elapsed wait, and ProcessLog/status reference; do not submit another export or resume polling without user direction |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Export succeeds but the ZIP can't be persisted or fails integrity validation | Classify as artifact persistence, preserve safe diagnostics, and do not report a successful downloadable artifact |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Proposal review | What will be enabled, for whom or process, effective date, resolved defaults or associations, material assumptions, exclusions, and assumption-ledger status |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Immutable preview | Exact environment, operation, complete preview revision, exact-reuse outcome, and separate executor approval requirement |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Completion | Readback comparison, discrepancies, and unperformed downstream actions |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Export approval | Exact source environment, task name/code, data versus template mode, full or filtered scope, criteria when present, and output directory |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Export completion | Task name/code, source environment, ProcessId, terminal status, ZIP or log path, SHA-256 for a valid ZIP, retrieved enclosure type, elapsed wait, and safe next action |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | FSM import approval | Exact target environment, HRT_MANAGE_PROFILE_TYPES, immutable ZIP name and SHA-256, complete parent/child/translation scope, duplicate result, Task Hook readiness, operation, and whether approval is explicit or a same-prompt zero-match condition |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Read-only verification completion | Source environment alias, exact target, methods_used=[GET], writes_performed=false, existence status, pagination completeness, requested component results, differences, unverifiable values, and the fact that the route ended without export, import, or configuration |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Proposal is confirmed | Do not treat confirmation as execution approval or import authorization |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Synchronization is requested | Do not enable or run synchronization; do not hide its possible add, update, or delete effect on synced position items |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Provider contract is TBD or write route is unsupported | Do not write through undocumented REST, HDL, FSM, UI automation, migration, or browser routes |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Environment preflight evidence is needed | Do not use visual or user-attested environment evidence unless the requested verification is inherently visual |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | One or more exact existing sections are found anywhere in the candidate ZIP | Do not submit any part of the ZIP and do not update, merge, overwrite, resubmit, add child rows, or offer a fresh-approval exception. Disclose all duplicates and require a newly prepared ZIP that excludes them and completes a fresh validation and approval cycle |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A required Person content section is absent | Do not silently create it, hand-build its FSM rows, or continue target-property customization; obtain explicit scope approval and use only the confirmed FSM processing contract |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | A custom parent profile type is supplied for Profiles V2 | Do not create or import the parent, and do not rewrite ProfileTypeCode or ProfileUsageCode as a seeded type key |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Current data is requested | Do not return a template/spec ZIP in place of current setup values |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Filtered scope can't be proven | Do not infer criteria from the seeded ID/key mapping and do not silently export the full task |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Export timeout, failed process, or ambiguous submission response | Do not automatically create a second export process; retry polling for the known ProcessId only after user direction |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | Current-state verification is requested | Do not use POST, PUT, PATCH, DELETE, request bodies, action endpoints, setup export/import, Core Data Loader, browser automation, or any mutation-capable fallback; GET evidence never grants permission for a later write |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.IMMUTABLE_PREVIEW | decision | 12 | execution_gate | immutable_preview_approved->PTCS.HANDOFF;approval_pending->PTCS.PREVIEW_READY;blocked->PTCS.ERROR | PTCS.EXECUTION_CONTRACT | stop | Executor contract, parent-anchor validation, model-property resolution, and subscriber-closure validation are confirmed and immutable preview is requested |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.PREVIEW_READY | terminal | 90 | terminal | none | PTCS.IMMUTABLE_PREVIEW | stop | Proposal and technical review are complete; executor approval is pending |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.HANDOFF | terminal | 91 | terminal | none | PTCS.IMMUTABLE_PREVIEW | stop | Immutable preview has separate executor approval; execution and readback remain executor-owned |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.DUPLICATE_STOP | terminal | 97 | terminal | none | none | stop | One or more candidate sections are exact duplicates; the entire ZIP is rejected and only a newly prepared ZIP excluding all duplicates may begin a fresh validation cycle |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.CLARIFY | terminal | 98 | terminal | none | none | stop | One material business clarification is required before technical normalization |
| HRT_MANAGE_PROFILE_TYPES | Profile Types | PTCS.ERROR | terminal | 99 | terminal | none | none | stop | Any technical, provider, approval, or readback gate blocks or fails |
