# Categories Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A Category create request lacks a user-provided title | Ask for the title, return MISSING, and perform no write |
| An applicable profile option cannot be read or its trigger is unclear | Stop the dependent proposal, identify the exact option/trigger, and preserve unrelated validation work |
| An applicable profile option is already correctly populated | Record it as satisfied and omit it from the user dialog; do not propose a redundant change |
| A profile-option change lacks exact approval or readback | Stop before Category execution; do not treat request acceptance or a stale value as completion |
| Unified listing/CAP administration applies but applicable CAPs are not validated | Block only that dependency path and route CAP work to its separate excluded scope; do not create or update CAPs here |
| A search-mode change lacks an authoritative exact value or representative search results | Preserve the current value and block only the proposed search-mode change |
| Category or Topic identity is missing, ambiguous, inaccessible, or wrong subtype | Stop only the affected parent or child row and request a technical identifier or explicit selection |
| A Topic, membership, group, asset, DFF, or Data Loader write route is unregistered or unproven | Preserve the requested operation, name the exact missing route/field/registration, and block only its affected rows |
| A parent is valid but one or more child rows are blocked | Preserve the valid parent and independent siblings in the versioned proposal; never hide, coerce, or silently drop blocked rows |
| A branding upload or processing step fails after the Category parent succeeds | Report the verified parent success and the separate asset failure; do not roll back or misstate the parent |
| Criteria/group processing is asynchronous or has mixed row outcomes | Return process and row-level states, active-member counts when available, elapsed time, and one safe next-check path |
| A manager removal would leave no active manager | Stop that membership row before mutation and require another active manager |
| Category, manager set, Topic relationship, access, field value, or capability changes after preview | Invalidate only affected approval, preserve evidence, and issue a refreshed proposal version and fingerprint |
| A write outcome is uncertain | Do not retry; reconcile through returned parent/child read links before considering a new approved attempt |
| Readback differs from the approved preview | Report partial or failed verification with parent/child scope and do not claim success |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, identity, access, applicable profile option/trigger, CAP prerequisite, search decision/test, live value, route contract, membership state, approval, or readback is unavailable | Supply or resolve the named blocker |
| UNSUPPORTED | Direct learning, skills, qualifications, contributions, self-service conversations, Draft, deactivate, reactivate, object delete, generic upsert, or another excluded operation is requested | Route Topic-only work to a Topic or select a supported Category operation |
| FAILED | Validation, execution, polling, persistence, or verification fails | Review sanitized parent/child diagnostics and verified effects before another attempt |
| ALL_GOOD | Every selected approved Category parent and eligible child operation is verified | Return stable row-specific results and the completed task-local run record |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before proposal | Exact environment, operation, applicable profile-option triggers/current values, satisfied options omitted from dialog, decisions/changes still needed, stable parent/child row IDs, missing or corrected values, blocked/excluded rows, generated/defaulted values, and warnings |
| Before mutation | Every exact proposed profile-option code/level/current/proposed value and prerequisite, Category identity or create key, exact selected rows, Active behavior, visibility, summary provenance, parent and association dates, relationship effects, manager result, async behavior, verified routes, proposal version/fingerprint, and approval status |
| After profile-option change | Exact option code and level, sanitized readback evidence, dependent privilege/data-role or administrator access check, and representative search results when search mode changed |
| On asynchronous work | Process identity suitable for safe follow-up, last status, row counts/outcomes, elapsed time, and next-check guidance |
| On failure | Failure class, affected stable row and parent, current rule, sanitized evidence, verified side effects, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent, stale, or not bound to the exact proposal fingerprint | Do not call any POST, PATCH, DELETE, upsert, asset, association, membership, group, DFF, or Data Loader write route |
| A profile option's v7 trigger does not apply | Do not display it for decision or propose a change |
| An applicable profile option is already correctly populated | Do not ask the user to approve a redundant change; record it as satisfied |
| A profile-option change is absent from exact approval or lacks readback | Do not apply or depend on it for Category execution |
| Applicable Catalog Administration Profiles are missing or unverified | Do not set ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD or create/update CAPs in this excluded task scope |
| Search-mode intent or exact current mapping is unresolved | Do not translate broad/balanced/tight intent into an invented code or replace the current value |
| A child route or payload is not registered and target-confirmed | Do not infer one from a generic collection method, UI behavior, or similarly named resource |
| A Category subtype or live field value is unresolved | Do not infer a code from a label, endpoint, baseline mapping, or another environment |
| A Topic or person match is ambiguous | Do not choose the first result or copy a display label as a technical identifier |
| Manager safety is unresolved | Do not remove the last active manager or treat a pending/criteria row as an active replacement |
| A Topic-only or excluded lifecycle operation is requested | Do not expose, redirect silently, or invoke a generic DELETE/upsert method |
| A fingerprint exists | Do not describe it as ETag, If-Match, or atomic concurrency protection; the supplied Describe provides no such evidence |
| A write result is uncertain | Do not automatically replay the write or roll back unrelated verified successes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAT.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->CAT.EVALUATE_RESULT;blocked->CAT.HANDLE_ERROR | CAT.ENFORCE_DESIGN | stop | A validation-only result or exact approved profile-option, parent, and child row set has current evidence, prerequisite readbacks, and verified operation routes |
| CAT.HANDLE_ERROR | step | 8 | error_handler | disclosed->CAT.RETURN_ISSUES | none | stop | A Category profile dependency, parent, or child row is blocked by input, dependency, lookup, design, approval, execution, timeout, persistence, or verification |
| CAT.RETURN_SUCCESS | terminal | 9 | terminal | none | CAT.EVALUATE_RESULT | stop | Every selected valid profile dependency, Category parent, and eligible child row is verified with row-specific results |
| CAT.RETURN_ISSUES | terminal | 10 | terminal | none | CAT.HANDLE_ERROR | stop | One or more Category profile dependencies, parent rows, or child rows cannot safely complete |
