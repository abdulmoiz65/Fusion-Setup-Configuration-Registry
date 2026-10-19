# Official Communities Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Parent subtype/status, tenant summary rule, privilege evidence, or required DFF contract is unresolved | Stop the parent before mutation and name the exact missing runtime authority |
| An applicable profile option cannot be read or its trigger cannot be evaluated | Stop the dependent proposal or operation; preserve the current value and identify the Application Profile Option Foundation evidence needed |
| Unified listing applies but Catalog Administration Profile readiness is missing | Return the precise external CAP prerequisite; do not create, validate, or modify CAPs and do not invent a CAP skill ID |
| ORA_WLF_COMMUNITIES_REDWOOD_ENABLED is absent | Do not propose a value; request evidence for the current release's supported control and community-management surface |
| Search-mode tuning lacks a decision or supported stored value | Preserve the current ORA_WLF_SS_CATALOG_SEARCH_MODE value and ask for broader recall, balanced matching, or tighter precision only when the trigger applies |
| A profile change is absent from exact approval or its readback differs | Do not submit it or continue dependent community work; refresh values, rebuild the proposal, and obtain new approval |
| Person, learning selector, membership, group, assignment, skills/qualifications, contribution, or moderation contract is unavailable | Block only dependent rows, preserve unrelated valid rows, and do not substitute another route |
| Optional asset, forum, related-material, translation, or DFF child is unsupported or invalid | Exclude or fail only that child unless the user made it mandatory; keep parent outcome separate |
| A removal, reconciliation, required-membership change, assignment cancellation, or moderation action has learner impact | Show the exact impact and require a revised exact approval before mutation |
| Parent, manager set, capability, or selected relationship changes after preview | Skip the affected action, invalidate approval, and rebuild the proposal |
| A write outcome is uncertain | Stop later submissions; do not retry; reconcile through confirmed read routes first |
| An asynchronous group, assignment, upload, or processing action times out | Return the operation, sanitized process identity, last status, elapsed time, and safe next-check guidance |
| Parent or child readback differs from the approved preview | Report partial, failed, or indeterminate verification without hiding independently verified success |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, approval, applicable profile/CAP/access evidence, exact identity, resolver, capability, or runtime value is unavailable | Supply or resolve the named blocker and issue a new proposal |
| UNSUPPORTED | Generic upsert, Draft, deactivate, reactivate, delete-object, or an unregistered child operation is requested | Select a supported operation or defer only the affected row |
| FAILED | Validation, execution, polling, or verification fails | Review sanitized row-specific diagnostics before another attempt |
| PARTIAL | A parent or independent child verified while another approved child failed or remains indeterminate | Preserve verified results and reconcile only unresolved rows |
| ALL_GOOD | Every selected approved parent and child row is verified | Return row-specific results and the completed run record |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before proposal | Exact target, operation, parent/child rows, applicable profile triggers and effective values, satisfied options omitted from the dialog, external CAP blockers, generated/defaulted values, and excluded optional rows |
| Before mutation | Exact environment, Official Community identity or create key, subtype/status evidence, manager count, relationship and learner impact, every proposed profile option name/level/old/new value, row selection, proposal version/fingerprint, and approval status |
| After profile mutation | Configured and effective value readback, intended-administrator access result when applicable, representative search result when search mode changed, verified side effect, and safe next action |
| On capability block | Requested operation, missing registered method/schema/readback authority, affected rows, and one concrete next action |
| On failure or timeout | Failure class, affected parent/child row, current rule, sanitized evidence, verified side effects, process status when applicable, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent, stale, or bound to a different proposal | Do not call parent or child mutation routes |
| An already-correct profile option is found | Do not ask the user to reconfirm it or submit a no-op profile write |
| Applicable CAP readiness is absent | Do not implement CAP setup or set ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD to Site Y |
| ORA_WLF_COMMUNITIES_REDWOOD_ENABLED is absent from the current tenant/release | Do not hard-code it, propose a value, or manufacture another option as its replacement |
| A profile change is not bound to exact approval or readback is incomplete | Do not submit the change, retry it automatically, or execute its dependent community operation |
| Official Community subtype, Active status code, profile/access evidence, summary rule, or required field is unresolved | Do not infer a code/property or create the parent |
| Person, learning, group, assignment, skill, qualification, or moderation authority is absent | Do not convert a label or unrelated child into a write identifier or route |
| A manager or membership action leaves zero active managers or mixes selection methods/states | Do not stage or submit it |
| Generic upsert, Draft, deactivate, reactivate, or delete-object is requested | Do not expose or invoke it under this story |
| A child requires parent identity | Do not call it before verified parent readback |
| A fingerprint exists | Do not describe it as ETag, If-Match, or atomic concurrency protection |
| A write result is uncertain | Do not automatically replay the write or continue dependent submissions |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OCM.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->OCM.EVALUATE_RESULT;blocked->OCM.HANDLE_ERROR | OCM.ENFORCE_DESIGN | stop | A validation-only result or exact approved profile-change, parent, and child row set is ready for evaluation |
| OCM.HANDLE_ERROR | step | 8 | error_handler | disclosed->OCM.RETURN_ISSUES | none | stop | An applicable profile dependency/change or Official Community parent or child row is blocked by validation, dependency, lookup, design, approval, execution, timeout, or verification |
| OCM.RETURN_SUCCESS | terminal | 9 | terminal | none | OCM.EVALUATE_RESULT | stop | Every selected profile change and valid parent and child row is verified and row-specific results are available |
| OCM.RETURN_ISSUES | terminal | 10 | terminal | none | OCM.HANDLE_ERROR | stop | One or more profile dependencies/changes or Official Community parent or child rows cannot safely complete |
