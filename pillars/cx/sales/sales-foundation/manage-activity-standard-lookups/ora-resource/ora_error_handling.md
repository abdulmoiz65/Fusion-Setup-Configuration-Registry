# Activity Standard Lookup Error Handling and Execution Gate

Stop safely on missing task scope, ambiguous identity, protected lookup data,
stale approval, incomplete sibling-order evidence, invalid setup packages, or
uncertain mutation outcomes. These task nodes authorize a route; Apps Common
transport belongs to `core.fusion-api.apps-common` and its shared REST client.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup type and code CRUD boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Protected operations, translations, effective dates, deletion, and session refresh |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Sales lookup configuration-level restrictions |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-template-exports.html | Task CSV template export boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task CSV import and result boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Role, task-code, ZIP, and package requirements |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html | Activity Type function membership and tag requirement |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitytypelookupslov-get.html | Function-specific Activity Type verification |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, parent type, code, meaning, update field, translation, environment, package, or approval is missing | Stop and request only the missing business value or gate. |
| Parent type is absent or is not verified in this setup task | Stop; do not create a new lookup type or use generic Standard Lookups REST presence as task-scope proof. |
| Exact code already exists for Create | Return the current row and require an explicit Update request; do not enable upsert. |
| Exact code is absent for Update, Deactivate, Delete, Translate, or Review | Stop and request a corrected identity or explicit Create request. |
| Parent or row configuration prevents the requested field change | Stop and disclose the configuration level, predefined-data evidence, requested fields, and permitted alternative. |
| A tag is requested for a non-ZMM_ACTIVITY_TYPE lookup | Reject the tag without changing other fields. |
| A ZMM_ACTIVITY_TYPE Create lacks exact functions, enablement, start date, or the canonical derived Tag | Stop before REST or package preview and request only the missing or conflicting value. |
| A completed task export is supplied as loose files | Build and validate a separate ZIP that preserves the exact root files and headers; never edit or import the original export in place. |
| Status or Activity-search sequence impact is incomplete | Stop until the full sibling list is read and the resulting default is accepted. |
| A read returns 401 or 403 | Classify as authorization or privilege failure; do not search another lookup category. |
| A read fails or returns ambiguous evidence | Report the sanitized method, endpoint identity, status, and request ID or ECID; stop before mutation. |
| Approval does not match the current state, endpoint, method, body, or environment | Invalidate approval, re-read the target, and present a new immutable preview. |
| A direct translation write is requested | Use the documented task UI or current task CSV workflow because the FSCR Standard Lookups reference documents translation reads but no translation mutation contract. |
| A POST, PATCH, or DELETE has an uncertain transport outcome | Do not replay it. Reconcile once with the exact code GET and report success, unchanged state, or uncertainty. |
| Post-write verification differs from the approved body | Report the mismatch and stop; do not issue a compensating write automatically. |
| A new Activity Type passes Standard Lookup verification but is absent from any selected function LOV | Report incomplete Activity-function visibility and stop; do not claim completion or retry the mutation automatically. |
| The CSV template or export is stale, for another task, or has altered files or headers | Stop and obtain a current package for ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS. |
| Import approval does not match the exact package preview | Stop and revalidate the changed package before new approval. |
| Import completes with errors or uncertain status | Retrieve the documented result or process log once, disclose it safely, and stop before retry. |
| A lookup-code Create, Update, Deactivate, or Delete does not select a route | Use the Apps Common code-CRUD contract; do not require an export package or initialize browser control. |
| The requester explicitly selects manual UI, Export, Import, or a supported translation workflow | Use only the explicitly selected documented route; do not substitute it for normal Apps Common code CRUD. |

## Apps Common Standard Lookup Code Route

| Operation | Method and Endpoint | Body Boundary | Required Precondition |
|---|---|---|---|
| Create | POST `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes` | Include only approved supported fields: LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, and permitted Tag; for ZMM_ACTIVITY_TYPE include the canonical function-derived Tag; omit absent optional fields and never set Upsert-Mode=true | Exact parent exists, exact code is absent, matrix and Activity rules pass, Activity functions are resolved when applicable, and immutable preview is approved |
| Update | PATCH the canonical CodeItemLink, or `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode}` with both keys encoded as path segments | Include only fields whose values change and are permitted; never include LookupCode | Exact code exists, current state and editability are known, impact passes, and immutable preview is approved |
| Deactivate | PATCH the canonical code item | Include only approved EnabledFlag=N, EndDateActive, or both | Exact code exists and the configuration matrix permits the selected controls |
| Delete | DELETE the canonical CodeItemLink | No body | Exact code exists, deletion is permitted, impact is accepted, and deletion approval is explicit |

Invoke these routes only through `core.fusion-api.apps-common`, which owns the
shared OAuth-backed REST client. Submit a mutating request once. After the
response, verify with an exact GET and record the method, endpoint, safe HTTP
outcome, returned request ID or ECID when available, and final row state.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| BLOCKED | Input, task scope, editability, impact, package, environment, preview, approval, or supported route is missing | Resolve the named gate; do not perform a mutation |
| FAILED | A live read, validation, mutation, verification, or import result is invalid, ambiguous, or unsuccessful | Disclose sanitized evidence and wait for corrected input or explicit retry instruction |
| APPS_COMMON_READY | An exact approved create, update, deactivate, or delete is ready for the core Apps Common executor | Hand off once; do not execute from a task resource node |
| UI_GUIDANCE_READY | The requester explicitly selected manual UI and the reviewed plan is ready for an authorized setup user | Follow the documented task UI; no Fusion side effect has yet occurred |
| IMPORT_HANDOFF_READY | A current task package has passed validation and exact approval | Hand off to core.data-loader |
| REVIEW_COMPLETE | Review, validation, or export planning completed without a Fusion mutation | Return current evidence and any session-refresh or impact follow-up |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Apps Common mutation preview | Task code, target environment, operation, LookupType, LookupCode, current state or confirmed absence, configuration level, predefined-data status, exact method, endpoint, JSON body or no-body delete, Upsert-Mode=false for create, impact result, verification GET, and approval fingerprint |
| UI plan | Task code, operation, LookupType, LookupCode, changed fields, editability, impact, and sign-out and sign-in verification guidance |
| Import handoff | Exact package identity, task code, metadata status, root files, header validation, unchanged parent row, unique row delta, blank new-row audit fields, derived function Tag, package fingerprint, preview, approval state, and authorized executor |
| Failure | Safe resolver or endpoint identity, response or process status, sanitized request ID or ECID, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Parent type or task ownership is unknown | Do not create a lookup type, guess a parent, or mutate a code. |
| Duplicate create | Do not set Upsert-Mode=true or reinterpret Create as Update. |
| Protected or disallowed field | Do not bypass configuration-level or predefined-data restrictions. |
| LookupCode rename | Do not PATCH the identifier; require a separately reviewed replacement plan. |
| Direct translation request | Do not invent a translation POST or PATCH contract. |
| Missing or stale approval | Do not invoke POST, PATCH, or DELETE. |
| Failed or uncertain mutation | Do not retry automatically, issue a compensating write, or claim success. |
| Missing current task package or schema | Do not hand-build CSV files or submit an import. |
| Activity Type Tag does not match the supplied function set | Do not import or POST the row, and do not infer or add a function. |
| Secret-bearing diagnostics | Do not print credentials, bearer tokens, authorization headers, client secrets, or token-cache content. |

## Documented Guided Setup — Explicit Manual UI Only

1. In Setup and Maintenance, open the Sales offering, Sales Foundation
   functional area, and `Manage Activity Standard Lookups` task.
2. Select the exact existing Activity lookup type.
3. For Create, add a lookup-code row and enter the stable code, meaning, and
   reviewed optional values. For Update, Deactivate, or Delete, select the exact
   current row and change only fields permitted by its configuration level and
   predefined-data status.
4. For a new `ZMM_ACTIVITY_TYPE`, select the exact Activity functions and use
   the matching canonical colon-wrapped function Tag. Treat calendar-color
   changes as a separate guided operation until current evidence proves a
   representation that preserves the function Tag. Do not use Tag for other
   Activity lookup types.
5. For `ZMM_ACTIVITY_STATUS_CD` or `ORA_ZMM_ACTIVITY_FILTER_TYPE`, review the
   resulting order and default before saving.
6. Save and Close. Have affected users sign out and sign back in before
   validating a user-visible lookup change.

## Documented CSV Automation Route — Explicit Requests Only

| Sequence | Required Gate | What Must Happen |
|---|---|---|
| 1 | Task package | Export the current template or setup data for ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS. |
| 2 | Package preparation | Copy the current package, preserve ASM_SETUP_CSV_METADATA.xml, FND_APP_STANDARD_LOOKUP.csv, and ORA_FND_APP_STANDARD_LOOKUP_CODE.csv at the ZIP root, keep the existing parent row unchanged, and add only the reviewed child row with blank system audit fields. |
| 3 | Validation | Validate metadata task identity and completion, exact headers, unique row delta, configuration restriction, date, canonical function Tag, and sequence-impact rules. |
| 4 | Immutable preview | Build a preview for the exact normalized ZIP and target environment. |
| 5 | Approval | Obtain approval bound to the exact package fingerprint, preview, and authorized executor. |
| 6 | Import handoff | Route the approved package to core.data-loader using task code ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS. |
| 7 | Verification | Retrieve the result or process log once, verify the exact Standard Lookup code, verify a new Activity Type through every selected function LOV, and refresh the affected user session. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_STD.EXECUTION_GATE | decision | 8 | execution_gate | apps_common_ready->ACTIVITY_STD.APPS_COMMON_READY;ui_guidance_ready->ACTIVITY_STD.UI_READY;explicit_import_ready->ACTIVITY_STD.IMPORT_READY;review_or_export_complete->ACTIVITY_STD.REVIEW_COMPLETE;missing_or_unsupported_gate->ACTIVITY_STD.BLOCKED | ACTIVITY_STD.DESIGN | stop | Route lookup-code Create, Update, Deactivate, or safe Delete to Apps Common; use manual UI or package import only when explicitly selected. |
| ACTIVITY_STD.APPS_COMMON_READY | terminal | 9 | terminal | none | ACTIVITY_STD.EXECUTION_GATE | stop | An exact approved create, update, deactivate, or delete is ready for core.fusion-api.apps-common |
| ACTIVITY_STD.UI_READY | terminal | 10 | terminal | none | ACTIVITY_STD.EXECUTION_GATE | stop | The requester explicitly selected manual UI and the reviewed task plan is ready for an authorized setup user; no Fusion side effect has occurred |
| ACTIVITY_STD.IMPORT_READY | terminal | 11 | terminal | none | ACTIVITY_STD.EXECUTION_GATE | stop | An explicitly requested Import package is validated and ready for core.data-loader handoff |
| ACTIVITY_STD.REVIEW_COMPLETE | terminal | 12 | terminal | none | ACTIVITY_STD.EXECUTION_GATE | stop | Review, validation, or export planning completed without mutation |
| ACTIVITY_STD.BLOCKED | terminal | 13 | terminal | none | none | stop | A required input, task-scope, editability, impact, route, package, preview, or approval gate is missing |
| ACTIVITY_STD.FAILED | terminal | 14 | terminal | none | none | stop | A validation, live read, mutation, verification, or import result is invalid, ambiguous, or unsuccessful |
