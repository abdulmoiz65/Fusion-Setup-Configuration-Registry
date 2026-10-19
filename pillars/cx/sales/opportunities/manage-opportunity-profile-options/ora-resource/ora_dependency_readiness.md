# Manage Opportunity Profile Options Dependency Readiness

For exact-code Review, resolve environment and read privileges and continue to
LOOKUP with ExportStatus=not_requested_for_review; skip export dependencies.
Resolve the environment, recorded export outcome for Inventory/mutation, and exact live target before
selecting mutation readiness. Export failure continues to Apps Common lookup;
an existing exact child permits REST Update without a ZIP or omission proof.
The export subskill's failed or timeout result is intermediate for this child.
When canonical environment and Apps Common read readiness pass, classify the
dependency node as satisfied and continue to LOOKUP. Do not map export status
directly to the child node's failed transition. Ignore partial export files;
failed-export membership remains unknown and live lookup establishes value
existence. Invalid identity or an actual Apps Common failure still stops.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and conditional export | Resolve canonical target/read route; Review skips export, while Inventory/Set/BulkSet attempt populated exact-task export with --data/no criteria after required export approval |
| 2 | Live configured state | Read exact definitions, live level capability rows, and complete Site/User/Product children |
| 3 | Mutation route | Select FSM for present exported definitions, REST Create/Update for confirmed omission, or REST Update for failed export plus existing live child; classify every bulk row |
| 4 | Route-specific readiness | FSM requires existing export closure and package/task context; REST requires exact scope, current state, privilege, stored-value dependencies, and immutable preview |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| opportunity_option_candidates | Source-backed code/name/ownership and discovery coverage | Yes | Every request; partial coverage is permitted for Inventory only | Lookup | Checked-in documented seeds, validated task-export identities, and verified Oracle identity evidence | resolve_opportunity_option_candidates | Prevent invented codes, cross-domain selection, and false all-options completion | Resolve exact identity sources; incomplete Inventory discovery preserves partial live results and its next action without changing Review export requirements | CandidateReceipt, exact identity/provenance, CoverageScope, SourceCoverage, counts, per-code statuses, UnresolvedCandidates, CoverageGaps, AllOptionsComplete |
| target_environment | Canonical target and declared Apps Common route | Yes | Every request | Verify | Project/environment context | resolve_live_profile_option | Prevent cross-target reads or writes | Resolve the selected environment and REST host | EnvironmentUrl, EnvironmentIdentity, FusionRelease, ProjectId, attempted-call evidence |
| export_attempt | Exact task export and classified outcome | Yes | Inventory, Set, or BulkSet; not Review | Lookup | shared.setup-export.task-level-export | resolve_profile_option_export_baseline | Establish scope and mutation-route membership | For applicable modes, approve export POST then attempt it; on failure record diagnostics and continue live reads/update checks; unapproved export is approval blocker, not failure | Attempted task/target/time, classified outcome and available ProcessId/status; on success ExportMode=data/no-filter/member/header/count/path/hash receipt; on failure sanitized diagnostics and unknown membership |
| live_profile_option_reads | Exact definition and configured child state | Yes | Every request | Lookup | core.fusion-api.apps-common.profile-options | resolve_live_profile_option | Establish authoritative current state | Read exact definition, profileOptionLevels LevelName/EnabledFlag/UpdateableFlag rows, and complete value children | Definition/status, live level flags, configured rows or explicit absence, timestamps |
| mutation_route | Successful definition membership or classified exact-task export failure | Yes | Set or BulkSet | Lookup | Recorded export outcome and exact live identity | resolve_profile_option_export_baseline | Distinguish omission from missing values or export failure | Present exported definition selects FSM; confirmed omission selects REST Create/Update; failed export plus existing live child selects REST Update | Known match count or unknown membership, MutationRoute, FallbackReason, omission or failure evidence |
| fresh_profile_option_export | Existing Site/User export closure and validation contract | Yes | FSM Set/BulkSet | Lookup | Fresh exact-target task export | resolve_profile_option_export_baseline | Preserve imported identity and package structure | Require matching parent, level, and existing value; no synthetic rows | ApplicationId, SqlValidation, level/key, flags, current value, dependency closure, ASM/member/header receipt |
| rest_target_identity | Site key, Product application short name, or exact UserName and conditional UserGuid | Yes | REST Set/BulkSet | Lookup | Apps Common live identity and selected scope | resolve_live_profile_option | Build the correct child-item key and create body | Site uses SITE; Product uses application short name; User item uses UserName and Create LevelValue uses UserGuid | Scope key, exact user/GUID or product identity, child present/absent state; export failure requires present state |
| stored_value_dependency | Exact active stored code/ID or other supported current value contract | Yes | Every mutation | Lookup | Live SqlValidation and documented safe resolver | resolve_live_profile_option | Avoid storing display labels or invalid values | Resolve the exact supported dependency; stop when no safe resolver exists | Proposed stored value, meaning, dependency evidence and timestamps |
| rest_privilege | FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV | Yes | Before REST preview/execution | Verify | Apps Common privilege evidence | resolve_live_profile_option | Authorize configured-value mutation | Verify the required privilege before preview | Privilege evidence and selected scope capability |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Environment and applicable route prerequisites are resolved | No |
| Lookup | Declared live reads or complete export joins remain to run | Yes, read-only lookups only |
| Blocked | Environment, export identity, live identity, scope, privilege, or stored-value contract is unresolved | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.PROFILE_OPTIONS.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->OPP.PROFILE_OPTIONS.LOOKUP;missing->OPP.PROFILE_OPTIONS.RETURN_MISSING;failed->OPP.PROFILE_OPTIONS.RETURN_FAILED | OPP.PROFILE_OPTIONS.VALIDATE | stop | Resolve environment/read readiness; Review skips export and continues satisfied to LOOKUP; Inventory/mutation require approved recorded export attempt, with classified failure intermediate rather than child failure |
