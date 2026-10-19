# Profile Rating Models Error Handling

## Error Situations

| Task Code | Task Name | Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-01 | Requirements or workbook mapping are missing, invalid, conflicting or ambiguous | Input validation | Return source, sheet, row, field, cell, impact and correction; stop before lookup |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-02 | Multiple candidates remain or a candidate cannot be fully classified | Input validation | Require specialist selection or complete read coverage; never infer reuse |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-03 | Read path, task/package, HDL hierarchy or attributes are missing or mismatched | Catalog or metadata mismatch | Preserve the blueprint and stop; do not substitute REST/browser/direct loader calls |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-04 | Cached authentication remains invalid after one allowed refresh | Authentication | Stop and require reauthentication through the owning skill |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-05 | Required read, Profile Rating Model or Data Loader privilege is denied | Authorization | Report required route-specific access; do not change routes |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-06 | Declared Fusion environment cannot be reached | Transport/environment | Stop and report environment and failed stage |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-07 | Read fails or returns incomplete component/paging coverage | Fusion API | Preserve sanitized diagnostics and stop |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-08 | Required workbook, mapping, blueprint, preview or digest cannot be persisted | Artifact persistence | Stop before approval/import and restore the artifact |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-09 | Immutable preview or approval is missing, stale or for another environment/artifact | Approval blocker | Regenerate preview and use core.data-loader approval |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-10 | Data Loader reports failed, partial, completed-with-errors or uncertain result | Process failed | Persist logs/errors, reconcile current state and do not replay automatically |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-11 | Polling times out | Process timeout | Report environment, task code, ProcessId/requestId, last status and elapsed wait |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-12 | Fresh read-back differs or is incomplete | Verification failed | Return expected/observed differences and do not report success |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-13 | Initial business request omits technical model fields but supports one safe review-only proposal | Review required | Discover patterns, populate the assumption ledger, and present one complete business proposal; do not turn the omission into a technical questionnaire |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-14 | Multiple consumer interpretations or scale patterns remain equally supported and materially different | Input validation | Explain the competing business outcomes and ask one plain-language question; do not ask the user to choose a Fusion consumer or object |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-15 | Proposal assumptions are unreviewed or proposal confirmation is treated as live-import approval | Approval blocker | Keep the proposal review-only; after confirmation build and validate the immutable creation artifact, then use only core.data-loader approval |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-16 | A screenshot, browser or manual UI navigation, address-bar image, exact user reply or user attestation is proposed as required or sufficient environment, access or completion proof | Workflow contract | Do not request or persist the UI evidence. Return to the declared authenticated environment, supported read and structured read-back route; if that route is unavailable, stop as blocked, incomplete or failed without inventing a manual proof step |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-17 | Performance calculation method, decimal places, decimal rounding rule, mapping metric, mapping method, or Target Ratings Distribution is treated as rating-model-owned setup or omitted from the downstream handoff | Design contract | Keep only model-owned levels and applicable review points and ranges in the rating-model blueprint; complete the Performance section handoff and stop before preview until ownership is corrected |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-18 | A model selected for a Talent Review X or Y axis lacks rating categories for applicable levels | Design contract | Block the Talent Review handoff and complete the model's rating categories; do not claim the box-chart matrix is ready |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-19 | A Skills Center model uses incompatible level identifiers or the handoff omits the post-association model lock | Design contract | Correct the scale to unique increasing integer identifiers from 1 through 9 and disclose the association constraint before skills are added to the content section |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM-20 | Quarterly release metadata is unavailable during read-only preflight and the flow proposes asking the user, requiring manual UI navigation, or blocking before an otherwise source-backed capability probe | Workflow contract | Keep the quarterly label unknown, do not ask the user, and continue with the exact authenticated environment plus the source-backed REST API version, path and bounded request. Block only when that machine-verifiable capability contract is missing or fails |

## Retry and Disclosure Rules

| Task Code | Task Name | Situation | Required Behavior |
|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | 401 or 403 with cache-managed token | Refresh once; a second failure stops |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Bounded read-only transport failure | Retry only when the active core client declares it recoverable |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | POST, upload, import, loader or uncertain creation | Never automatically retry |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Initial technical values are absent but one supported proposal can be produced | Continue to discovery and a review-only proposal; do not stop or request every technical field |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Before proposal review | Show the business outcome, workforce or process, effective date, proposed scale, important exclusions, material assumptions, and Review assumptions option |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Proposal is confirmed before an immutable artifact exists | Treat confirmation only as design input; never upload, import, or claim live authorization |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Before approval | Show environment, operation, source version, consumers, exact-search result, every value/exclusion, handoffs, artifact digest and read-back assertions |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Environment, access or completion evidence | Do not request a screenshot, browser navigation or exact user reply. Use only the declared core context and structured read results; UI evidence supplied without request remains supplemental and cannot pass a gate |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Quarterly release metadata | Record the value and source only when trusted core context or supported target metadata already provides them. Do not ask the user or infer the quarterly release from a REST API version, hostname, documentation URL or calendar date; its absence alone does not block the bounded capability probe |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | Diagnostics | Redact credentials, tokens, opaque URLs, raw sensitive payloads, internal IDs and ETags |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.ROUTE | decision | 9 | execution_gate | reuse_complete->PRM.DONE_REUSE;loader_ready->PRM.DONE_LOADER;blocked->PRM.ERROR | PRM.DESIGN | stop | Complete exact reuse or enter only the declared core.data-loader stage for one immutable creation source |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.ERROR | step | 10 | error_handler | stopped->PRM.BLOCKED | none | stop | Any prior node returns invalid, missing, ambiguous, incomplete, blocked, failed, stale, partial, timed-out, uncertain or unverified; return a business-language question when business input is the only blocker |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.DONE_REUSE | terminal | 11 | terminal | none | PRM.ROUTE | continue | One exact model is proven and structured handoffs are ready |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.DONE_LOADER | terminal | 12 | terminal | none | PRM.ROUTE | continue | One creation source is ready for core.data-loader or a later approved run completed with full read-back verification |
| HRT_MANAGE_PROFILE_RATING_MODELS | Profile Rating Models | PRM.BLOCKED | terminal | 13 | terminal | none | none | stop | One business clarification or corrected requirements, mapping, access, metadata, source, approval or reconciliation is required |
