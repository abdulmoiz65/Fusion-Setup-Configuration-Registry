# Manage Opportunity Profile Options Input Validation

Exact-code Review requires live Apps Common GETs and read privileges only;
no export attempt, export approval, ZIP, or write privilege is required.
Use exact live Apps Common reads for configured values. Successful same-target
export membership selects FSM or omission fallback. A classified failed export
continues to live lookup and permits REST Update only for an existing exact
child. FSM package and REST preview checks apply to their selected route.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Candidate scope and source inputs | Optional OpportunityOptionIdentityEvidence and InventoryScope=all_options or explicit_candidates with SelectedCodes | Default unspecified Inventory scope to all_options; a supplied exact code may enter definition-only lookup without source evidence at intake. Resolve ownership and coverage through LOOKUP before final review or mutation readiness | Validate supplied field shapes; the named resolver later generates CandidateReceipt and design checks its coverage. Never require lookup outputs as initial user inputs | Intake; source resolution occurs at LOOKUP | resolve_opportunity_option_candidates |
| Product creation support evidence shape | Optional ProductCreationSupportEvidence with OracleSource, ApplicableRelease, Resource, SupportedOperation, Restrictions, and RequiredPrivilege | Product creation policy remains blocked; this input is unnecessary for legacy reads and existing-row updates | Supply verifiable source evidence for the owning design gate; approval is a separate input | New REST Product child only | |
| Requested operation | Inventory, Review, Set, or BulkSet | Block validation | Normalize list/current requests to Inventory or Review and requested value changes to Set or BulkSet | Every request | |
| Target environment | EnvironmentUrl, canonical EnvironmentIdentity, FusionRelease, and ProjectId | Block external access | Resolve the selected implementation environment and project | Every request | |
| Export attempt evidence | Classified outcome; on success ExportMode=data, no-filter evidence, ProcessId, ZIP path/SHA-256, exact task, environment, release, timestamp, complete members, headers, and row counts | Require attempted-call evidence; a recorded failure continues to live reads and existing-value REST update checks | Attempt the populated exact-task export with --data and no export criteria | Inventory, Set, or BulkSet; not exact-code Review | resolve_profile_option_export_baseline |
| Exact profile-option identity | Exact case-sensitive ProfileOptionCode, one unique exact display name, or one unambiguous immediate-context code | Block Review or mutation | Resolve one exact live Opportunity definition; supplied code and display name must agree | Review, Set, or BulkSet | resolve_live_profile_option |
| Requested value target | Code, ProfileLevel, ProposedValue; UserName for User; ProductApplicationShortName for REST Product; optional ExpectedCurrentValue | Block mutation readiness | Resolve the exact scope and live current state; bind that state or explicit not configured and compare any supplied expected value | Set or BulkSet | resolve_live_profile_option |
| Route-selection evidence | Successful complete export and per-code definition count, or classified exact-task export failure; MutationRoute and FallbackReason | Block preview or handoff | Present definition selects FSM; zero definitions permits REST Create/Update; failed export permits REST Update only with existing exact live value; ambiguity blocks | Set or BulkSet | resolve_profile_option_export_baseline |
| FSM package and task context | Existing exported Site/User row, final target/release/task binding, ASM identity, member/header receipt, reviewed value delta, state locks, preservation evidence, final ZIP path/reopened SHA-256, validation result, persisted TaskContextPath and positive TaskSequence | Block Data Loader handoff | Build and reopen the package from the fresh baseline; resolve persisted context to this exact skill, TaskCode, TaskName, offering, and functional area | FSM Set/BulkSet | verify_profile_option_final_package |
| REST target and current state | Exact live Site/Product/User key, enabled/updatable live level flags, one existing row or explicit absence for confirmed omission only, validated stored value, and privilege | Block REST preview | Resolve exact live state and conditional dependencies through Apps Common | REST Set/BulkSet | resolve_live_profile_option |
| REST preview and approval | Canonical environment/task, FallbackReason and omission or failure evidence, method, endpoint, code/level/key, expected state, proposed stored value, minimal body, dependencies, verification plan, PreviewSha256; later standalone approval bound to that preview | Return preview without writing; block stale or mismatched execution approval | Complete the REST design gate, persist preview, and wait for approval; refresh evidence on approved resume | REST preview/execution | |
| Bulk changes | Unique ordered code/level/scope-key/value rows, state locks, and route per row | Block ambiguous or duplicate rows; split mixed routes before execution | Preflight all rows and submit separate FSM and REST batches with their own previews and approvals | BulkSet | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Display-name-only input has no unique exact-code mapping | Return missing code/source identity; do not pass a display label as ProfileOptionName | Review or mutation | resolve_opportunity_option_candidates |
| Supplied InventoryScope is not all_options or explicit_candidates, or explicit_candidates has no exact SelectedCodes | Return invalid or missing scope fields; do not silently narrow an all-options request | Inventory intake | |
| ProductCreationSupportEvidence is supplied without required source/release/resource/operation fields | Return missing evidence fields before the owning design gate; preserve all other routes | New REST Product child | |
| Operation is unsupported or ambiguous, including Delete/Remove | Reject before export or lookup | Every request | |
| Current/latest/configured request is classified as documentation-only | Normalize to Inventory or Review and use live configured-value reads | Inventory or Review | |
| Short follow-up has zero or multiple prior exact codes | Request one exact code; do not inherit ambiguous context | Review | |
| Code is malformed, unknown, misspelled, belongs to another product area, or conflicts with display name | Return exact identity failure; never substitute a similar code, default, or another package row | Review or mutation | resolve_live_profile_option |
| Exact-code Review has no export attempt or export approval | Continue direct live GETs; record ExportStatus=not_requested_for_review, never failed; no separate mutation approval or write privilege required | Review | resolve_live_profile_option |
| Export POST approval is absent | Stop the export step as approval blocker; do not call POST or reinterpret lack of approval as export failure | Inventory, Set, BulkSet, or explicit export request | |
| An artifact offered as a successful export is template/spec or filtered, or task, environment, release, completion, full member/header receipt, or hash is invalid | Exclude it; block mutation and disclose reconciliation gap; failed-export fallback does not require successful-artifact fields | Every request | resolve_profile_option_export_baseline |
| Exact-task export attempt fails or times out | Record failure and unknown membership; continue exact Apps Common reads; an existing live child may select PATCH, absent child blocks update | Set or BulkSet | resolve_profile_option_export_baseline |
| Complete export contains zero exact option definitions | Record confirmed omission and select Apps Common REST only if exact live definition exists | Set or BulkSet | resolve_profile_option_export_baseline |
| Complete export contains the exact definition but lacks its requested value or capability row | Block FSM readiness; do not reinterpret missing child/level rows as option omission | FSM Set/BulkSet | resolve_profile_option_export_baseline |
| Complete export contains duplicate or conflicting definitions | Block both mutation routes as an identity mismatch | Set or BulkSet | resolve_profile_option_export_baseline |
| Live definition or complete configured child evidence is missing without a classified attempted-call result | Do not complete Inventory/Review or mutation readiness | Every request | resolve_live_profile_option |
| ProfileLevel, proposed value, or required User/Product key is blank | Request the missing field without changing scope | Mutation | |
| FSM request targets Product or a nonexisting exported Site/User row | Reject package readiness; no REST fallback for a present option | FSM Set/BulkSet | resolve_profile_option_export_baseline |
| Selected level is disabled or not updatable | Block; FSM additionally requires matching exported capability | Mutation | resolve_live_profile_option |
| Supplied expected value differs from exact live state | Invalidate readiness and any approval; use a fresh preview or package | Mutation | resolve_live_profile_option |
| REST child is absent after confirmed successful-export omission | Select POST and bind explicit not configured state | REST Set/BulkSet | resolve_live_profile_option |
| REST child is absent after export failure | Block update; do not issue POST, upsert, or synthesize omission evidence | REST Set/BulkSet | resolve_live_profile_option |
| REST child exists once | Select PATCH to the exact item and lock its current value | REST Set/BulkSet | resolve_live_profile_option |
| REST Create body has fields beyond required LevelValue and ProfileOptionValue, PATCH changes anything except ProfileOptionValue, or Upsert-Mode is used | Reject and rebuild the minimal deterministic request | REST Set/BulkSet | |
| Proposed value cannot be deterministically validated using current SqlValidation and supported stored-value resolvers | Block before package or preview; never execute validation SQL or guess a stored code/ID | Mutation | resolve_live_profile_option |
| FSM value row lacks matching parent definition or package changes metadata, headers, keys, dependencies, audit fields, or unrelated values | Reject package readiness | FSM package validation | resolve_profile_option_export_baseline |
| Latest live state differs from immutable package evidence | Invalidate handoff and refresh live/export evidence | Before FSM handoff | resolve_live_profile_option |
| Persisted task context or final ASM/member/header/hash/preservation receipt is missing or inconsistent | Block FSM handoff; never synthesize context solely to satisfy Data Loader | FSM handoff | verify_profile_option_final_package |
| REST route, environment, method, endpoint, body, dependency, capability, scope identity, or expected state changed after preview | Invalidate approval; refresh recorded export outcome/live evidence and build a new preview | Before each REST write | resolve_live_profile_option |
| BulkSet contains both FSM and REST rows | Return route-specific batch plan; no handoff, preview approval, or write occurs | BulkSet | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.PROFILE_OPTIONS.VALIDATE | step | 1 | validate_input | valid->OPP.PROFILE_OPTIONS.DEPENDENCIES;missing->OPP.PROFILE_OPTIONS.RETURN_MISSING;invalid->OPP.PROFILE_OPTIONS.RETURN_FAILED | none | stop | Normalize Inventory/Review/Set/BulkSet; exact-code Review needs no export or mutation approval; validate exact identities and route-conditional inputs and reject unsupported operations |
