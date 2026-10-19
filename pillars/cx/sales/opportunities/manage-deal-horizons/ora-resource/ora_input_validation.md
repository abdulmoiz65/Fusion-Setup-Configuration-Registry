# Manage Deal Horizons Input Validation

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

Validate the exact MOO_SETID_DEAL_HORIZION request before any lookup, preview, export review,
or import handoff. The enclosing task skill fixes the FSM task code to
MOO_MANAGE_DEAL_HORIZONS.

Set `RequestMode` explicitly before applying selector rules. Use
`SingleLookup` for Inventory, Read, Delete, or one-code Create, Update, or
Disable. Use `Package` for full-task Export, Import, or package-scoped Create,
Update, or Disable. Package REST_FALLBACK uses the unchanged reviewed ordered
row list; its per-row set and state checks are live, not deferred to a ZIP.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request envelope | Operation and RequestMode; ExecutionRoute for a mutation | Block lookup, export, package review, or preview | Select SingleLookup or Package and a compatible operation before continuing | Every request |  |
| SingleLookup request identity | SetSelectionDecision plus either confirmed Common Set or one of SetId, SetCode, BUOrgId, or OrganizationCode for a different set | Block lookup and preview | Ask whether Common Set should be used; otherwise require one exact reference-set or business-unit identifier | SingleLookup | resolve_deal_horizon_reference_set |
| SingleLookup code identity | LookupCode | Block lookup and preview | Provide the exact code | SingleLookup Read, Create, Update, Disable, or Delete |  |
| SingleLookup create definition | Meaning; optional Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, and Tag | Block preview | Provide a display meaning for the new code | SingleLookup Create |  |
| SingleLookup update definition | At least one of Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, or Tag | Block preview | Provide at least one intended mutable field | SingleLookup Update |  |
| Target environment | EnvironmentUrl, EnvironmentIdentity, FusionRelease, and ProjectId | Block live reads, export, or handoff | Select and verify one target Fusion environment and durable project workspace | Every request |  |
| SingleLookup expected state and impact | Exact current-state fields or confirmed absence, live-read timestamp, owner, purpose, affected Opportunity or revenue field, historical-use assessment, and downstream consumers | Block mutation preparation | Complete the read-before-write and business-impact review | SingleLookup Create, Update, Disable, or Delete |  |
| Export request | Target environment and release with TaskCode fixed to MOO_MANAGE_DEAL_HORIZONS | Block export | Run the automatic full-task export for this exact target and task; do not supply a set selector or LookupCode | Package Export |  |
| FSM baseline, final package, exact task identity, and persisted Data Loader task context | TaskCode fixed to MOO_MANAGE_DEAL_HORIZONS; fresh completed same-target baseline; separate immutable final PackagePath and PackageSha256; exact metadata-derived members and headers; reviewed row delta; TaskName fixed to Manage Deal Horizons; require persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area | Block FSM handoff | Validate the exact task and unchanged archive, require persisted Data Loader task context, and hand it to Data Loader without requiring Data Loader-owned preview or approval evidence | ExecutionRoute=FSM for SingleLookup Create, Update, or Disable; Package Create, Update, Disable, or Import | verify_deal_horizon_fsm_package |
| Native FSM package changed rows | For every changed row: RowOperation, fixed LookupType, LookupCode, exact SetId, proposed fields, current-state lock, and business-impact evidence | Block package review or FSM handoff | Resolve and validate every changed row independently; the package may contain multiple codes and sets | ExecutionRoute=FSM for Package Create, Update, Disable, or Import | verify_deal_horizon_fsm_package |
| Direct REST delete authorization | ExecutionRoute=REST_DELETE, canonical returned child item link, current-state fingerprint, editability and delivered/custom evidence, downstream and historical impact acceptance, no-body DELETE preview, disclosed exact verification GET, and approval bound to the exact environment, method, endpoint, identity, state, and fingerprint | Block REST readiness | Explicitly select REST delete and approve its immutable preview immediately before one DELETE and its disclosed exact GET | SingleLookup Delete |  |
| Final Apps Common fallback evidence | ExecutionRoute=REST_FALLBACK; same-target CsvFailureReceipt with EXPORT_FAILED, EXPORT_TIMEOUT, UNUSABLE_EXPORT, CSV_IMPORT_FAILED, or CSV_IMPORT_NO_EFFECT; CsvRecoveryExhausted with applicable recovery outcomes; complete prior-submission reconciliation; unchanged reviewed rows and confirmed sets | Block fallback; retain FSM or the original blocker | Apply CSV recovery first. For a submitted import, require a later explicit results request, terminal jobs, prescribed status/errors/ProcessLog, and fresh proof that every requested row is unchanged or Create-absent | SingleLookup or Package Create, Update, or Disable using REST_FALLBACK | verify_deal_horizon_rest_fallback |
| Direct REST fallback authorization | RestFallbackEligible=true; per-row fresh state, write privileges, editability and impact evidence; immutable ordered preview with exact target, methods, endpoints, writable bodies, verification GETs, fingerprint and separate immediate approval | Block REST submission; preview preparation does not require approval | Load Apps Common then Lookups; obtain approval of the exact REST preview immediately before one submission per row. Export/Data Loader approval cannot be reused | ExecutionRoute=REST_FALLBACK |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| RequestMode is SingleLookup for Export or Import, or Package for Inventory, Read, or Delete | Reject the incompatible mode; do not apply one-code selector rules to package work | Every request |  |
| A supplied LookupType is not MOO_SETID_DEAL_HORIZION | Reject before lookup; do not infer or substitute a lookup type | Every request |  |
| Operation is outside Inventory, Read, Create, Update, Disable, Delete, Export, or Import | Reject before lookup or package validation | Every request |  |
| A SingleLookup request supplies more than one set selector and the selectors have not been proven equivalent | Reject the conflicting identity before lookup | SingleLookup with multiple selectors | resolve_deal_horizon_reference_set |
| SetSelectionDecision is missing, or Common Set was inferred rather than explicitly confirmed | Block before lookup or preview; ask whether Common Set should be used or a different exact SetId, SetCode, BUOrgId, or OrganizationCode should be supplied | Every set-scoped request | resolve_deal_horizon_reference_set |
| SetId is not an integer, SetCode is blank after trimming, or no exact set exists in the selected environment | Reject before code lookup, package readiness, or preview; request one valid exact set identity and do not substitute Common Set or a close match. Do not reject an integer solely because it is zero; require explicit set selection and exact selected-environment resolution | Every set-scoped request | resolve_deal_horizon_reference_set |
| SetId and SetCode resolve to different sets, confirmed Common Set resolves to a non-Common set, or the resolved set differs from the BU/organization assignment, confirmed request, fresh export, or package row | Reject the conflicting set scope; show sanitized supplied and returned identities and require one corrected explicit set decision | Every set-scoped request | resolve_deal_horizon_reference_set |
| LookupCode is blank | Reject before lookup or package readiness | SingleLookup Read, Create, Update, Disable, or Delete; every changed package row |  |
| Meaning is blank | Reject before lookup or package readiness | SingleLookup Create or a package Create row |  |
| No mutable field is supplied | Reject before lookup or package readiness | SingleLookup Update or a package Update row |  |
| EnabledFlag is supplied with a value other than Y or N | Reject the field before lookup | Create or Update |  |
| EndDateActive precedes StartDateActive | Reject the date range before lookup | Both dates are supplied |  |
| LookupCode is longer than 30 characters or contains whitespace; Meaning is longer than 80 characters; Description is longer than 240 characters; or Tag is longer than 150 characters | Reject the invalid field and show its exact limit | Create or Update |  |
| StartDateActive or EndDateActive is not ISO YYYY-MM-DD, or DisplaySequence is not an integer | Reject before lookup or package preparation | A supplied date or display sequence |  |
| Update or Disable attempts to change LookupType, LookupCode, SetId, or SetCode | Reject immutable identity changes | SingleLookup Update or Disable; every package Update or Disable row |  |
| Disable supplies anything other than EnabledFlag=N as its mutable delta | Reject the compound or contradictory disablement | SingleLookup Disable or a package Disable row |  |
| ExecutionRoute is incompatible with Operation or RequestMode | Accept FSM for native CSV work, REST_FALLBACK only for Create, Update, or Disable after the final fallback verifier, and REST_DELETE only for SingleLookup Delete; reject other routes and REST Export/Import | Every request |  |
| REST_FALLBACK lacks valid exhaustion/reconciliation evidence or requests a different environment, task, lookup, set, operation, or row scope | Reject before REST preview; it cannot bypass missing input, workflow/context, catalog, auth/authz, set/assignment, approval, explicit FSM-only scope, pending jobs, uncertain submissions, partial changes, or a repairable CSV package | REST_FALLBACK | verify_deal_horizon_rest_fallback |
| A fallback Create body sends SetCode or audit/parent fields, an Update changes identity, a returned item link points outside the exact target/lookup, or a batch repeats a LookupCode/SetId pair | Reject the REST preview; use resolved integer SetId only for Create, canonical returned child links for PATCH, minimal mutable deltas, and unique ordered row identities | REST_FALLBACK |  |
| Delete does not use the canonical returned child link, includes a body, lacks editability or impact evidence, omits the exact verification GET, or lacks approval bound to the exact preview | Reject REST readiness | SingleLookup Delete |  |
| An FSM package uses a task code other than MOO_MANAGE_DEAL_HORIZONS, has stale or cross-environment export evidence, changes metadata-derived members or headers, includes an unreviewed type/set/code row, or changes after validation | Reject package readiness; for SingleLookup require exactly the reviewed lookup-code change plus its unchanged support parent, and for Package validate every changed code and parent linkage without forcing one set | ExecutionRoute=FSM for SingleLookup Create, Update, or Disable; Package Create, Update, Disable, or Import | verify_deal_horizon_fsm_package |
| A completed exact-task data export has header-only CSVs | Validate successful process evidence, metadata, members and headers; zero rows alone are not a failure. For Create, apply the task skill's Header-Only FSM Baselines and Parent Linkage procedure with fresh live parent, set and absent-code evidence | Package Export; SingleLookup Create; Package Create | verify_deal_horizon_fsm_package |
| A changed code has no matching in-package parent row, its parent fields differ from the fresh live parent, or its SetCode differs from the resolved set | Block package preparation and handoff; retain the exact exported parent or add its unchanged support row from fresh read-only parent evidence, and validate the child join and set | Every FSM mutation or Import | verify_deal_horizon_fsm_package |
| The persisted Data Loader task context is inconsistent or has a different task name/code, or the persisted project context has blank TaskContextPath or nonpositive TaskSequence, or the archive changes after PackageSha256 is calculated | Reject Data Loader handoff and restart package validation; missing or inconsistent task context blocks handoff and cannot trigger fallback; never hand-author or synthesize task context, and Data Loader later binds finalData.archiveSha256 to this unchanged PackageSha256 after it creates its own preview | ExecutionRoute=FSM for SingleLookup Create, Update, or Disable; Package Create, Update, Disable, or Import | verify_deal_horizon_fsm_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.DEAL_HORIZON.VALIDATE | step | 1 | validate_input | valid->OPP.DEAL_HORIZON.RESOLVE_PARENT;missing->OPP.DEAL_HORIZON.RETURN_MISSING;invalid->OPP.DEAL_HORIZON.RETURN_MISSING;failed->OPP.DEAL_HORIZON.RETURN_FAILED | none | stop | Every Manage Deal Horizons request; set-scoped requests require an explicit Common-versus-different decision and reject malformed, unknown, cross-environment, or conflicting set identity |
