# Manage Levels of Risk Error Handling

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Stop before undocumented writes, automatic mutation retries, stale approvals,
or substitution of another lookup type or FSM task code.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity or mutable data is missing or invalid | Show the exact field or conflict and stop before lookup or preview |
| The reference set, requested assignment, or code state is missing or ambiguous | Show sanitized identity and match evidence; request a corrected exact value or return ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| SetId/SetCode is malformed, absent in the selected environment, conflicts with another selector or package row, confirmed Common Set resolves elsewhere, or a BU/organization assignment resolves to another reference group/set | Classify as input, lookup, or catalog/scope mismatch; disclose sanitized supplied and returned identities and stop before code lookup, package review, or preview |
| Fusion returns 401 or 403 | Refresh a cache-managed token at most once, then stop as authentication or privilege failure |
| A read-only call fails | Preserve sanitized endpoint and request evidence; retry only within the bounded core read policy |
| A core.data-loader FSM import fails or is uncertain | Do not replay; reconcile once by exact read and require a new package, preview, and later standalone approve |
| A direct REST mutation fails or is uncertain | Do not retry or switch routes; reconcile once by exact read and require a new REST preview and approval |
| Delete is requested through FSM | Stop before package preparation; offer Disable or the documented direct REST exception |
| Create, Update, or Disable requests direct REST | Stop before preview; these operations use the exact MOO_MANAGE_LEVELS_OF_RISK FSM package |
| An accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, or live lookup verification | Stop; accepted initiation is terminal and those reads require a later explicit status or results request |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required field, operation, set selector, date, or mutable value is invalid | Correct the request and rerun validation |
| Catalog mismatch | LookupType is not MOO_SETID_RISK_LEVEL or the package task code is not MOO_MANAGE_LEVELS_OF_RISK | Use this adapter's fixed identities |
| Record-set prerequisite | A requested assignment is absent or incorrect | Complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES, then rerun read-only resolution |
| Authentication or privilege | Fusion rejects access after the permitted token refresh | Reauthenticate or obtain required privileges |
| Transport or Fusion API | Connectivity or Fusion response prevents deterministic resolution | Correct the environment or request before a new preview |
| Approval blocker | A REST Delete lacks its separate immediate preview approval, or a post-handoff Data Loader preview/approval lifecycle is incomplete | For REST, approve the exact Delete preview before submission. For FSM pre-preview handoff, approval is not yet required; Data Loader creates its preview and requests the later standalone approve |
| Process timeout or failure | An FSM process times out or fails | Preserve process evidence, reconcile target state, and do not retry automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| FSM handoff | Environment, MOO_MANAGE_LEVELS_OF_RISK, operation, MOO_SETID_RISK_LEVEL, SingleLookup set/state or every package row's set/state lock, immutable package path, SHA-256, member summary, proposed rows, impact, and verification plan |
| REST preview | Environment, MOO_MANAGE_LEVELS_OF_RISK, operation, MOO_SETID_RISK_LEVEL, resolved set, current state, method, endpoint, body or no-body delete, impact, verification GET, and preview fingerprint |
| Failure or uncertainty | Failed stage, classification, sanitized status and identifiers, last known state, possible side effects, what was not retried, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Exact SingleLookup or per-row package evidence is missing, or a REST Delete lacks its exact preview and approval | Do not submit REST or hand an incomplete FSM package to Data Loader; absence of Data Loader approval before its preview is expected and must not block the handoff |
| The approved operation, identity, endpoint, body, package, or fingerprint changed | Do not reuse approval |
| A mutation or import failed or is uncertain | Do not retry automatically or claim Fusion is unchanged |
| Delete is selected with FSM | Do not prepare or submit an FSM delete row |
| Another lookup type or task code is supplied | Do not substitute it into this adapter |
| Set identity is wrong, conflicting, or cross-environment | Do not substitute Common Set, choose a close match, rewrite a package row, or continue under a different set scope |
| Credentials, bearer tokens, or protected values are supplied | Do not print or persist them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.RISK.GATE | decision | 8 | execution_gate | read_only->OPP.RISK.RETURN_READ;rest_approved->OPP.RISK.RETURN_REST_READY;fsm_handoff_ready->OPP.RISK.RETURN_FSM_READY;accepted_initiation->OPP.RISK.RETURN_ACCEPTED;export_ready->OPP.RISK.RETURN_EXPORT_READY;missing->OPP.RISK.RETURN_MISSING;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.DESIGN | stop | Return Inventory or Read without mutation; return a validated full-task Export baseline; route Delete only through one explicitly selected and approved no-body DELETE plus its disclosed exact GET; hand only fully validated Create, Update, Disable, or Import packages to core.data-loader; terminate when Data Loader returns accepted initiation |
| OPP.RISK.RETURN_READ | terminal | 9 | terminal | none | OPP.RISK.GATE | continue | Inventory or Read completed with exact parent, reference-group, pagination, set, assignment when requested, and lookup evidence |
| OPP.RISK.RETURN_REST_READY | terminal | 10 | terminal | none | OPP.RISK.GATE | continue | One exact separately approved REST Delete is ready for Apps Common, followed by its disclosed exact GET verification |
| OPP.RISK.RETURN_FSM_READY | terminal | 11 | terminal | none | OPP.RISK.GATE | continue | One unchanged MOO_MANAGE_LEVELS_OF_RISK Create, Update, Disable, or Import ZIP and exact task identity, plus persisted Data Loader task context, are ready for core.data-loader Task Hook validation and preview; no upload approval or execution has occurred |
| OPP.RISK.RETURN_ACCEPTED | terminal | 12 | terminal | none | OPP.RISK.GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog retrieval, result retrieval, or live verification until a later explicit request |
| OPP.RISK.RETURN_EXPORT_READY | terminal | 13 | terminal | none | OPP.RISK.GATE | continue | The fresh MOO_MANAGE_LEVELS_OF_RISK export baseline is validated for review or package preparation; no mutation package or upload approval is implied |
| OPP.RISK.RETURN_MISSING | terminal | 14 | terminal | none | none | continue | Required input, parent or lookup evidence, prerequisite, impact review, package evidence, exact task identity, persisted Data Loader task context, or REST-specific approval is missing; persisted task context is required for Data Loader handoff, and Data Loader approval is not required before FSM handoff |
| OPP.RISK.RETURN_FAILED | terminal | 15 | terminal | none | none | continue | Validation, parent/set/code lookup, package verification, handoff, execution, import, or later explicit verification failed |
