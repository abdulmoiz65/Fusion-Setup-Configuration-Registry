# Topics Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Title or existing Topic identity is missing | Ask only for the missing identity and perform no write |
| Profile, access, subtype, value, DFF, or parent contract is unresolved | Stop the affected operation before proposal or mutation and identify the exact gate |
| An applicable profile option is unread, wrong-scope, stale, or not at its required approved value | Block the affected dependency; show the exact code and trigger, and do not substitute a cached or similarly named option |
| A Single Catalog Listing change lacks applicable CAP readiness | Block that conditional dependency and direct CAP creation or validation to its separate excluded task scope; do not invent a CAP skill ID or perform CAP setup here |
| A child route is unregistered or unsupported | Block only that child operation; never invent a route or payload from a similar resource |
| Category, learning, person, skill, qualification, rating, asset, or related-material reference fails | Report the child row separately and preserve valid independent rows |
| A membership action would leave no manager | Refuse the action and show the current and proposed manager counts |
| A row creates self-reference, duplicate association, or graph cycle | Mark the edge blocked and require a corrected proposal |
| A Topic, manager set, capability, or relationship changes after proposal | Skip the stale action, invalidate its approval, refresh evidence, and re-propose |
| A write outcome is uncertain | Do not retry; reconcile through confirmed read routes before offering another mutation |
| An asynchronous group, criteria, media, or child process is incomplete | Return sanitized process identity, status, last check, elapsed time, and safe next-check path |
| Parent succeeds and an optional child fails | Report partial configuration and every verified result; do not claim full success or roll back unrelated work |
| Readback differs from the approved proposal | Return failed verification with the exact affected parent or child row |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required identity, approval, lookup, privilege, DFF, route, or reference is unavailable | Supply or resolve the named blocker and issue a new proposal when required |
| UNSUPPORTED | Lifecycle/delete, Category-as-learning, self-reference, cycle, or operation without a registered capability is requested | Select a supported operation or exclude the affected child row |
| FAILED | Validation, execution, polling, persistence, or readback fails | Review sanitized diagnostics and reconcile before another attempt |
| PARTIAL | Parent or independent rows succeeded while one or more optional child rows failed or remain in process | Preserve verified successes and address only the unresolved rows |
| ALL_GOOD | Every selected approved parent and child result is verified | Return persisted IDs, row-level outcomes, and completed run record |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before proposal approval | Exact environment, operation, Topic create key or persisted identity, subtype, Active behavior, visibility, applicable profile-option decisions or changes and prerequisite evidence, generated and defaulted values, standalone or relationship behavior, selected rows, impacts, execution order, exclusions, and fingerprint |
| Before mutation | Fresh applicable profile-option reads and change readbacks, conditional CAP readiness, access and HCM data-role result, capability, current-state and manager evidence, exact proposal version, and approval status |
| On failure | Failure class, affected parent or child row, current rule, sanitized evidence, verified side effects, and one safe next action |
| On partial result | Persisted parent identity, every attempted child outcome, asynchronous status, excluded rows, and remaining configuration |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent, stale, or bound to another proposal | Do not call POST, PATCH, DELETE, upload, group, contribution, moderation, or Data Loader write routes |
| A profile-option change is absent from exact approval or lacks foundation-provider readback | Do not change the option or continue into dependent Topic execution |
| Catalog Administration Profile readiness is missing | Do not create CAPs, invent a CAP dependency skill ID, or bypass the external prerequisite |
| Topic subtype or lookup value is unresolved | Do not infer a code from generic Learning Topics labels, another object, or a display meaning |
| Category relationship capability is absent | Do not substitute communityLearningCatalogItems or a Product UI action |
| Person, skill, qualification, or optional-child selector is unavailable | Do not persist a display label or manufacture a technical ID |
| Last manager would be removed | Do not execute the individual or bulk membership change |
| Draft, deactivate, reactivate, or Topic delete is requested | Do not expose or invoke root DELETE or an unsupported status transition |
| A fingerprint exists | Do not describe it as ETag, If-Match, or atomic concurrency protection |
| A write result is uncertain | Do not automatically replay the write |
| Diagnostics are returned | Do not expose credentials, bearer tokens, opaque identifiers, or full request and response bodies |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TOP.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->TOP.EVALUATE_RESULT;blocked->TOP.HANDLE_ERROR | TOP.ENFORCE_DESIGN | stop | A validation-only result or exact approved Topic parent and child row set is ready for evaluation |
| TOP.HANDLE_ERROR | step | 8 | error_handler | disclosed->TOP.RETURN_ISSUES | none | stop | A Topic parent or child row is blocked by validation, dependency, lookup, design, approval, execution, timeout, or verification |
| TOP.RETURN_SUCCESS | terminal | 9 | terminal | none | TOP.EVALUATE_RESULT | stop | Every selected valid Topic parent and child row is verified and row-specific results are available |
| TOP.RETURN_ISSUES | terminal | 10 | terminal | none | TOP.HANDLE_ERROR | stop | One or more Topic parent or child rows cannot safely complete |
