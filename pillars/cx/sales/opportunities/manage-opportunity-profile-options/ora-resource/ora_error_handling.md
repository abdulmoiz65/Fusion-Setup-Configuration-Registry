# Manage Opportunity Profile Options Error Handling

FSM and REST have separate gates and approval ownership. Preserve the selected
route and sanitized evidence; never switch routes to recover a failed write.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Inventory discovery is incomplete after export failure/omission or an unresolved documented identity | Continue known source-backed exact-code reads, preserve provenance/counts/statuses/gaps, and return PARTIAL at RETURN_PARTIAL_INVENTORY; never claim all options were found or silently narrow scope |
| Display name has no exact code mapping or supplied code has no source-backed Opportunity ownership | Return missing identity/source evidence; exact-code Review still does not require export |
| New Product value lacks current Oracle creation-support evidence | Stop before preview/write under the owning design policy; preserve legacy Product reads and eligible existing-row PATCH |
| Current-value request is answered from defaults, documentation, or export alone | Resume exact live definition and configured child reads |
| Exact identity is absent, wrong product area, ambiguous, or conflicts across sources | Classify input/identity validation and stop without substituting a similar code or level |
| Exact-code Review asks approval for required export before reading | Resume direct declared Apps Common GETs; no export job is required and no separate mutation approval applies |
| Required export POST lacks approval | Stop that export as approval blocker; do not perform POST or relabel it as export failure to authorize REST mutation |
| Parent omits SiteLevelEnabled/SiteLevelUpdatable or corresponding Product/User aliases | Resolve the advertised profileOptionLevels child row using LevelName, EnabledFlag, and UpdateableFlag; absence of parent aliases is not disabled/read-only capability |
| Apps Common read fails | Report actual auth/authz/transport/Fusion API/pagination/shape failure; 401/403 is never not configured |
| Exact-task export fails or times out | Record classified failure/unknown membership and continue exact Apps Common lookup; an existing exact child permits REST PATCH preview, absence blocks update |
| Artifact offered as a successful export is incomplete/invalid/is template-only/is filtered or has duplicate definitions | Exclude invalid successful-baseline evidence and block mutation; ignore partial files from a recorded failed export and continue its exact live lookup |
| Successful complete export omits option and exact live definition resolves | Select declared Apps Common branch; do not demand an exported value row, import ZIP, or Data Loader context |
| Export contains option but lacks existing Site/User value or capability row | Block default FSM mutation; do not route to REST merely to bypass a missing value |
| FSM final package/task identity, receipt, state lock, path/hash, or persisted context is missing | Stop handoff and correct exact evidence; never hand-author context solely for Data Loader |
| FSM package/import/submission result is failed or uncertain | Preserve status/IDs/partial success and reconcile before a new package and Data Loader-owned preview/approval; do not retry |
| Data Loader returns accepted initiation | End request; later explicit status/results request is required for polling, ProcessLog, results, or verification |
| REST dependency, capability, exact key, privilege, or stored-value contract is unresolved | Stop before preview or write and return exact missing evidence |
| REST approval is missing | Persist/return immutable preview at RETURN_APPS_COMMON_READY; no POST/PATCH occurs |
| REST preview/approval differs from current route, environment, method, endpoint, body, dependencies, capability, scope, or current child state | Invalidate approval and return a fresh preview; do not transfer FSM approval to REST |
| REST POST/PATCH returns an error or an uncertain result | Preserve sanitized method/path/status/request ID/ECID and report possible change; read exact child to reconcile before considering a new preview; no replay |
| Exact REST post-write read disagrees | Report verification_mismatch and stop without retry or compensation |
| REST BulkSet fails after earlier verified rows | Stop immediately; report verified/failed/unattempted rows and require a new preview for remaining rows |
| BulkSet contains both routes | Return per-row route and separate-batch plan at RETURN_SPLIT before any approval, handoff, or write |

## REST Preview, Execution, and Verification

APPS_COMMON_GATE first returns a persisted immutable preview without a write.
The preview includes canonical environment/task, FallbackReason and successful
omission or classified failed-export receipt, exact code/level/key, current
value or explicit not configured for confirmed omission only,
validated proposed value/meaning, method/relative endpoint/minimal body,
dependencies, privilege, verification plan, ordered bulk rows, and SHA-256 over
all canonical preview fields. Ask for a later standalone approval of that
preview. No Data Loader preview or task context participates in this route.

For Product, also include ProductLevelSupportResult: legacy_existing_update or
documented_creation_exception, source/release/resource/operation/restrictions,
and source-evidence fingerprint. On approved resume revalidate the applicable
support evidence; changed or withdrawn evidence invalidates the preview and
approval. Missing Product children remain blocked without the documented
creation exception, and export failure never permits POST.

On approved resume, refresh live definition/capability/scope/child/dependency
state through resolve_live_profile_option and re-enter APPS_COMMON_GATE after
the preceding gates. Missing approval returns the preview; drift blocks
execution and requires a new preview. Once exact approval and immediate state
checks pass, hand the approved request to core.fusion-api.apps-common.profile-options,
which owns OAuth and shared HTTP transport. After export failure, require the
exact child still exists and send one PATCH only. For confirmed omission, send
one POST for explicit absence or one PATCH for an existing child. Do not change parent metadata, use
Upsert-Mode, issue DELETE, use direct HTTP/browser fallback, or retry a write.

After a successful response, perform a fresh exact child read in the same run.
Return verified only if the exact item exists and its stored value equals the
approved proposal. Optional profileValues reads report effective-session state
separately. For REST BulkSet, preflight and preview all ordered rows, approve
once, then re-read/write/verify sequentially and stop on the first drift,
write, or verification failure; report earlier verified successes without
rollback. Follow the core skill's next-session notification after success.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation or catalog mismatch | Identity, export, scope, row, dependency, or package contract is invalid | Correct exact inputs/evidence and rerun applicable preflight |
| Auth/authz, transport/environment, or Fusion API | Declared read or external call fails | Report actual attempted-call evidence and one safe recovery path |
| Process timeout or process failed | Export/import processing did not complete | Preserve task/environment/ProcessId/last status/elapsed wait; export failure may continue to exact live existing-value REST checks without polling/retry; accepted or uncertain imports still require a later explicit next-check |
| Approval blocker or stale state | Approval is absent/mismatched or target changed | Return a fresh route-specific preview; require new approval before mutation |
| Verification mismatch or uncertain write | REST result is not confirmed | Reconcile exact child state before a new preview; do not retry or compensate |
| Partial bulk completion | Earlier REST rows succeeded before a failure | Report successes and unattempted rows; request a new batch preview |
| Artifact persistence | Required evidence/preview/package cannot be saved | Block handoff/write and report intended path and safe recovery |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Inventory coverage | Requested scope, CandidateReceipt source/provenance, SourceCoverage, candidate/read counts, per-code statuses, UnresolvedCandidates, CoverageGaps, AllOptionsComplete, and complete or PARTIAL status; distinguish complete explicit-candidate reads from exhaustive all-options discovery |
| Inventory or Review | Canonical environment, exact code/candidate, definition status, live level flags, complete Site/User/Product values/absence, timestamps, export outcome or not_requested_for_review, separately labeled delivered/effective/export evidence |
| FSM failure | Environment/task/name, operation/route/stage/classification, immutable package path/hash, code/level, sanitized error, external IDs/status/partial successes, whether configuration may have changed, and one safe next action |
| REST preview/result/failure | Environment/task/route, FallbackReason and omission/failure evidence, exact code/level/key, method/path, current/proposed stored value and meaning, dependencies, minimal body, preview digest/approval state, HTTP result, exact verification/partial success, and one safe next action |
| Split required | Ordered rows, per-row FSM or REST route, separate-batch plan, and confirmation that no handoff or write occurred |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Incomplete Inventory discovery | Do not invent codes, use prefix-only ownership, return an empty complete inventory, treat a bounded seed set as exhaustive, or transfer partial discovery to mutation readiness |
| Product support evidence missing or changed | Do not treat enabled flags, generic POST availability, old service documentation, or user approval as a current new-value exception; do not replace missing legacy rows through POST |
| Missing exact live evidence or identity | Do not return defaults/export-only state as current or choose similar identities |
| Export failure | Do not fabricate omission or synthesize FSM rows; REST fallback requires an existing exact live child, PATCH, and separate preview/approval |
| Missing value for a successfully exported option | Do not fabricate omission, synthetic FSM rows, or REST fallback |
| FSM preview/approval before handoff | Child must not own or reuse approval; follow Data Loader session preview and approval lifecycle |
| REST preview/approval absent or stale | Do not write, import, invoke Data Loader, or transfer approval between routes |
| Uncertain mutation or failed verification | Do not automatically retry, compensate, poll FSM, or claim unchanged configuration |

Redact credentials, bearer tokens, headers, OAuth state, cookies, token-cache
contents, private keys, unnecessary user GUIDs, and sensitive values. Persist
only sanitized evidence and governed external identifiers.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.PROFILE_OPTIONS.GATE | decision | 6 | execution_gate | review_ready->OPP.PROFILE_OPTIONS.RETURN_REVIEW;inventory_partial->OPP.PROFILE_OPTIONS.RETURN_PARTIAL_INVENTORY;handoff_ready->OPP.PROFILE_OPTIONS.RETURN_READY;accepted_initiation->OPP.PROFILE_OPTIONS.RETURN_ACCEPTED;missing->OPP.PROFILE_OPTIONS.RETURN_MISSING;failed->OPP.PROFILE_OPTIONS.RETURN_FAILED | OPP.PROFILE_OPTIONS.DESIGN | stop | Return complete exact-code Review without export/mutation approval; Inventory returns review_ready only for completed explicit user-candidate scope or proven AllOptionsComplete, otherwise inventory_partial with known live results and discovery gaps. Preserve validated FSM handoff and Data Loader approval ownership; accepted initiation remains terminal |
| OPP.PROFILE_OPTIONS.APPS_COMMON_GATE | step | 8 | execution_gate | preview_ready->OPP.PROFILE_OPTIONS.RETURN_APPS_COMMON_READY;verified->OPP.PROFILE_OPTIONS.RETURN_APPS_COMMON_VERIFIED;missing->OPP.PROFILE_OPTIONS.RETURN_MISSING;failed->OPP.PROFILE_OPTIONS.RETURN_FAILED | OPP.PROFILE_OPTIONS.APPS_COMMON_DESIGN | stop | Preserve immutable REST preview, later exact approval, immediate live-state checks, one core POST/PATCH, same-run verification and bulk failure stop. Bind Product support evidence/restrictions to preview and revalidate on resume; failure fallback stays PATCH-only |
| OPP.PROFILE_OPTIONS.RETURN_REVIEW | terminal | 9 | terminal | none | OPP.PROFILE_OPTIONS.GATE | continue | Exact-code Review, complete explicit user-candidate Inventory, or Inventory with proven AllOptionsComplete is complete; disclose its exact source coverage and authorize no mutation |
| OPP.PROFILE_OPTIONS.RETURN_READY | terminal | 10 | terminal | none | OPP.PROFILE_OPTIONS.GATE | continue | Unchanged validated FSM package has exact task/target/context/ASM/member/header/delta/state/preservation/path/hash evidence and is ready for Data Loader-owned preview/approval; no import occurred |
| OPP.PROFILE_OPTIONS.RETURN_ACCEPTED | terminal | 11 | terminal | none | OPP.PROFILE_OPTIONS.GATE | continue | Data Loader returned accepted initiation; end without automatic polling, ProcessLog, results, or verification |
| OPP.PROFILE_OPTIONS.RETURN_APPS_COMMON_READY | terminal | 12 | terminal | none | OPP.PROFILE_OPTIONS.APPS_COMMON_GATE | continue | Exact REST fallback preview including confirmed omission or classified export failure and existing live value is persisted and ready for later standalone approval; no write occurred |
| OPP.PROFILE_OPTIONS.RETURN_APPS_COMMON_VERIFIED | terminal | 13 | terminal | none | OPP.PROFILE_OPTIONS.APPS_COMMON_GATE | continue | Approved Apps Common Set/BulkSet writes and exact same-run child verification succeeded |
| OPP.PROFILE_OPTIONS.RETURN_SPLIT | terminal | 14 | terminal | none | OPP.PROFILE_OPTIONS.ROUTE | continue | Mixed FSM/REST BulkSet requires separate route-specific batches/previews/approvals; no handoff or write occurred |
| OPP.PROFILE_OPTIONS.RETURN_MISSING | terminal | 15 | terminal | none | none | continue | Required request/live/export/route/dependency/package/preview/approval evidence is missing or stale |
| OPP.PROFILE_OPTIONS.RETURN_FAILED | terminal | 16 | terminal | none | none | continue | Input, identity, environment, export, design, package/import, REST write/verification, or persistence failed; preserve sanitized partial-success evidence |
| OPP.PROFILE_OPTIONS.RETURN_PARTIAL_INVENTORY | terminal | 17 | terminal | none | OPP.PROFILE_OPTIONS.GATE | continue | Inventory only: return PARTIAL with known-candidate live results, exact source coverage, unresolved identities/gaps and one safe next action; AllOptionsComplete is false and no mutation is authorized |
