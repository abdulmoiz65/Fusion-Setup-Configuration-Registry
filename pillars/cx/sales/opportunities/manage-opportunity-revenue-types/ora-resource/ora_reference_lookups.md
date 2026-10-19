# Manage Opportunity Revenue Types Reference Lookups

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

Resolve the exact MOO_SETID_REVENUE_TYPE parent before resolving sets or child codes.
Lookup resolution never authorizes a mutation, and the returned
ReferenceGroupName is the only value allowed for a business-unit assignment
query; never substitute LookupType for ReferenceGroupName.

Before reference-set resolution, require `SetSelectionDecision`. Ask whether
Common Set should be used or a different set should be specified. Resolve a
confirmed Common Set from its actual SetCode/SetId; never infer Common Set or
hard-code its numeric SetId.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_manage_opportunity_revenue_types_parent | Input validation succeeds | Catalog-fixed mapping of Manage Opportunity Revenue Types (MOO_MANAGE_REVENUE_TYPES) to LookupType MOO_SETID_REVENUE_TYPE | GET /fscmRestApi/resources/11.13.18.05/setEnabledLookups/MOO_SETID_REVENUE_TYPE?fields=LookupType,Meaning,Description,ModuleId,CustomizationLevel,RestAccessSecured,ReferenceGroupName&links=self,canonical; do not use onlyData=true because canonical links are required | LookupType, Meaning, Description, ModuleId, CustomizationLevel, RestAccessSecured, ReferenceGroupName, and returned self/canonical links | Require exactly one response whose LookupType is exactly MOO_SETID_REVENUE_TYPE and whose ReferenceGroupName is nonblank; task ownership comes from this adapter's exact catalog mapping, not REST presence alone | LookupParent, ReferenceGroupName, CustomizationLevel, RestAccessSecured, ParentItemLink, CatalogTaskScopeEvidence | A healthy exact 404 is not found and blocks this adapter; blank ReferenceGroupName, mismatched type, many results, 401/403, malformed data, or a catalog mapping mismatch fails closed |
| resolve_revenue_type_reference_set | The exact parent and returned ReferenceGroupName resolve for SingleLookup or every Package REST_FALLBACK row | SetId, SetCode, BUOrgId, or OrganizationCode plus returned ReferenceGroupName | For SetId, GET /fscmRestApi/resources/11.13.18.05/setIdSets with finder=PrimaryKey;SetId={SetId}; for SetCode use finder=SetCodeFinder;SetCode={SetCode}. For BUOrgId, GET /fscmRestApi/resources/11.13.18.05/setIdAssignmentsBusinessUnit with finder=AssignmentFinder;DeterminantValue={BUOrgId},ReferenceGroupName={returned ReferenceGroupName}; for OrganizationCode use finder=DeterminantFinder;bindBusinessUnitCode={OrganizationCode}, then validate the exact returned ReferenceGroupName. Pass each finder as one URL-encoded query value, request only the listed fields plus self/canonical links, and advance offset until hasMore=false | SetId, SetCode, SetName, OrganizationId, OrganizationCode, ReferenceGroupName, self/canonical links, and hasMore | Require one exact set per distinct requested row identity and, when BU-scoped, one exact assignment whose ReferenceGroupName equals the parent-returned value; multiple selectors must resolve to the same set, and absence cannot be inferred from an incomplete page | SetId, SetCode, SetName, BUOrgId when supplied, returned ReferenceGroupName, RecordSetAssignmentVerified, canonical links, pagination completion | Stop on no set, incomplete pagination, conflicting selectors, more than one exact set, or a missing/mismatched BU assignment; return the adapter's record-set prerequisite without mutating it |
| resolve_revenue_type_lookup_state | The parent, reference set, and applicable assignment resolve for SingleLookup or every Package REST_FALLBACK row | Resolved SetId and optional LookupCode | For a code, GET /fscmRestApi/resources/11.13.18.05/setEnabledLookups/MOO_SETID_REVENUE_TYPE/child/lookupCodes with finder=PrimaryKey;LookupCode={LookupCode},SetId={SetId}, passed as one URL-encoded query value, plus fields=LookupCode,SetId,SetCode,Meaning,Description,EnabledFlag,StartDateActive,EndDateActive,DisplaySequence,Tag and links=self,canonical. For Inventory, use q=SetId={SetId}, the same fields/links, a bounded limit, and advance offset until hasMore=false | LookupCode, SetId, SetCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, self/canonical links, and hasMore | For Inventory, return every exact-SetId code only after pagination completes; otherwise require zero or one exact case-sensitive LookupCode and SetId match for every distinct requested row | Sanitized current code state, current-state fingerprint and timestamp, pagination evidence, and returned child item identifier or item link | An empty completed Inventory is valid; not found is valid only for Create; stop on many exact matches, incomplete pagination, identity mismatch, or lookup failure |
| verify_revenue_type_fsm_package | Package Export/Import or Create, Update, Disable after route-aware state resolution | FSM: fresh exact-target/release/task data baseline, separate immutable final ZIP and reviewed rows, unchanged parent linkage, metadata-derived members/headers, PackagePath/PackageSha256, exact TaskName and persisted TaskContextPath/positive TaskSequence for handoff. Final CSV exhaustion: same-target CsvFailureReceipt, applicable recovery outcomes, unchanged business intent/rows/sets and complete prior-submission reconciliation. REST_FALLBACK: the retained receipt plus fresh parent/set/code resolver outputs | Read-only ZIP/metadata/CSV/hash/context validation for native FSM; read-only comparison of caller-owned project failure/recovery/reconciliation evidence for route selection; no Fusion mutation | Exact task/environment/release, export status/timestamp/scope, members/headers/hash, reviewed per-row set/code/pre-state/delta/impact, unchanged parent linkage and handoff context; or classified same-target CSV failure, recovery outcomes, actual process statuses/IDs and complete reconciliation | Export validates the unmodified full-task data baseline, including valid header-only CSVs, without requiring set/code/delta/context. FSM mutations validate one reviewed SingleLookup code plus unchanged support parent or every Package row atomically; preserve metadata, unrelated rows/members, minimal deltas, live state locks, impact and immutable bytes, with exact persisted context before Data Loader handoff. Keep valid/repairable CSV on FSM. Only Create/Update/Disable satisfying the task skill final-fallback conditions and same-target exhaustion receipt returns fallback_required; missing inputs/context/approval, stale scope, auth/set gaps, pending/uncertain/partial writes cannot produce that outcome. REST_FALLBACK returns fallback_candidate for verify_revenue_type_rest_fallback without requiring an FSM ZIP/context. Export/Import never return fallback outcomes; Inventory/Read/REST_DELETE return not_applicable | Native FSM baseline receipt or FsmPackageReady with reviewed rows, parent linkage, context and PackageSha256; fallback_required with unchanged intent and RestFallbackEligible=false; or fallback_candidate for dedicated verification, never direct REST approval | Missing/stale/cross-environment/malformed/changed package evidence blocks native FSM; a documented unusable exact-target export attempt may qualify only under final CSV exhaustion. Never synthesize context/schema/receipt, parse unsafe ZIP members, alter source exports, substitute FND_MANAGE_SET_ENABLED_LOOKUPS, reroute repairable/pending/uncertain/partial work, or reuse export/Data Loader approval |
| verify_revenue_type_rest_fallback | REST_FALLBACK Create, Update, or Disable after fresh parent, set/assignment, and requested-code resolution | Caller-owned project CsvFailureReceipt, CsvRecoveryExhausted evidence, complete prior-submission status/errors/ProcessLog reconciliation when submitted, unchanged reviewed row list, and fresh outputs of the three exact live resolvers above | Read-only comparison of retained project failure/recovery/process evidence and fresh live resolver outputs; no new external call or mutation in this verifier. Submitted-import diagnostics are obtained only through the declared Core Data Loader status workflow on a later explicit results request | Exact environment/release/task/lookup/operation/row/set identity, request fingerprint, failed stage and permitted reason, actual process statuses/IDs, timestamps, elapsed timeout when applicable, artifact refs/hashes, recovery outcomes, submission certainty, terminal status for all related import jobs, complete diagnostics, reviewed pre-state/proposed state, live per-row state and pagination | Require same-target EXPORT_FAILED, EXPORT_TIMEOUT, UNUSABLE_EXPORT, CSV_IMPORT_FAILED, or CSV_IMPORT_NO_EFFECT plus documented exhaustion of applicable CSV recovery. A valid header-only export or repairable missing parent does not qualify. Reject input/catalog/set/assignment/auth/approval/context gaps, FSM-only scope, stale/cross-target evidence, unknown submissions, running import jobs, incomplete diagnostics, partial application, or concurrent state changes. If every requested row matches the intended state, return already_applied without a write. Otherwise every requested row must still match its reviewed pre-state, including complete absence for Create; submitted imports additionally require terminal jobs and prescribed status/errors/ProcessLog evidence. Verify fresh exact parent, sets, assignments, unique code/set identities, and unchanged intent before eligibility | RestFallbackEligible=true only for an exhausted and reconciled unchanged request; reconciled per-row state locks and failure receipt. Otherwise verified already-applied result or an exact blocker; no Data Loader session, final ZIP/context, inherited approval, or loader capability lookup | Missing or unsafe evidence blocks fallback and does not authorize a write. Never label timeout as failure, infer write privilege from GET, silently drop applied rows, reroute partial/uncertain work, or retry an import to establish exhaustion |

## Route-Aware CSV Verification

The native ZIP checks above apply to FSM and Export/Import. For FSM Create,
Update, or Disable, first keep a usable or repairable package on the CSV route.
If the task skill's final-fallback receipt proves the applicable CSV path is
exhausted, return `fallback_required` with `RestFallbackEligible=false` before
requiring a final ZIP. This is a router handoff, not execution permission.
Missing input, task context, approval, or unresolved prior submissions are
blockers and cannot produce that outcome.

For `REST_FALLBACK`, `verify_revenue_type_fsm_package` returns
`fallback_candidate` to the dedicated fallback verifier instead of requiring
an FSM ZIP or Data Loader context. That verifier alone may return `eligible`
after failure/recovery evidence, fresh reads, and reconciliation pass. Export
and Import cannot use either fallback outcome. An accepted import still ends
its request; after-submission failure evidence requires the later explicit
status/results workflow. Existing FSM validation failures remain blockers
until the documented final-fallback conditions are proven.

## Header-Only Baseline and Parent Validation

Use the task skill's **Header-Only FSM Baselines and Parent Linkage** procedure
when a successful same-target exact-task data export omits seeded rows. The
export is still the authority for task metadata, CSV members, and headers;
fresh read-only parent, set, and code responses supply the existing identity
and Create absence evidence. Do not infer those values from an empty file.

`verify_revenue_type_fsm_package` validates one reviewed child-code change
for SingleLookup, plus a matching unchanged parent support row. Match the
child's `FND_APP_SET_ENABLED_LOOKUP.LookupType` to the parent's `LookupType`
and its `SetCode` to the resolved set. Every changed child needs this join;
the live parent's existence does not make a child-only import valid. Keep all
unrelated rows and archive members. An added support parent must match the
fresh exact parent fields and is disclosed separately from business changes.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The reference set cannot be resolved exactly | Stop before reading codes or creating a preview |
| SetSelectionDecision is absent or Common Set was inferred | Stop and ask whether Common Set should be used or a different exact SetId, SetCode, BUOrgId, or OrganizationCode should be supplied |
| SetId is not an integer, SetCode is blank, or the selected-environment set does not exist | Stop before code lookup or preview; do not substitute Common Set, another environment's set, or a close match. Zero is valid only with explicit selection and exact live set resolution; do not infer its set identity |
| SetId/SetCode disagree, confirmed Common Set resolves elsewhere, or the set conflicts with the BU/organization assignment, confirmed request, export, or package row | Stop as a set-scope conflict, disclose sanitized returned identities, and require one corrected explicit set decision |
| The parent is absent, mismatched, has no ReferenceGroupName, or lacks task-scope evidence | Stop before set or code lookup; do not substitute a generic set-enabled type |
| A requested business-unit assignment for the parent-returned ReferenceGroupName is absent | Return ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES as the prerequisite gap and do not change the assignment here |
| A single-code lookup returns one exact item | Preserve current state and the returned child identifier or item link for design validation and preview |
| No exact single code is found | Continue only as a Create candidate; Read, Update, Disable, and Delete remain blocked |
| Fusion returns 401 or 403 | Stop as authentication or privilege failure; do not treat the lookup or code as absent |
| A mutation is requested through a reference lookup | Refuse and pass only validated evidence to the adapter's execution gate |
| A collection reports hasMore=true or pagination is incomplete | Continue the read; never report absence or a complete inventory until hasMore=false |
| FSM package verification is not applicable to Inventory, Read, or Delete | Continue to the execution gate with not_applicable; Delete must satisfy its separate REST-only contract |
| The applicable exact-task CSV path is exhausted for Create, Update, or Disable | Return fallback_required with the classified same-target receipt and RestFallbackEligible=false; the router may resume once as REST_FALLBACK with fresh parent/set/per-row reads and the dedicated verifier |
| REST_FALLBACK has an eligible receipt and complete fresh resolution/reconciliation | Return eligible only through verify_revenue_type_rest_fallback; prepare a separate Apps Common preview and approval. No FSM ZIP, loader task context, or inherited approval is required |
| Fresh reconciliation finds every requested value already applied | Return already_applied and a verified result without any new mutation |
| A prior import is pending, uncertain, incompletely diagnosed, or partially applied | Block fallback; reconcile through the declared explicit results workflow and review a new remaining-change request if necessary |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.REVENUE_TYPE.RESOLVE_PARENT | step | 2 | reference_lookup | resolved->OPP.REVENUE_TYPE.RESOLVE_SET;missing->OPP.REVENUE_TYPE.RETURN_MISSING;failed->OPP.REVENUE_TYPE.RETURN_FAILED | OPP.REVENUE_TYPE.VALIDATE | stop | Resolve the exact MOO_SETID_REVENUE_TYPE parent, task scope, editability metadata, canonical link, and nonblank ReferenceGroupName |
| OPP.REVENUE_TYPE.RESOLVE_SET | step | 3 | reference_lookup | resolved->OPP.REVENUE_TYPE.DEPENDENCY;not_applicable->OPP.REVENUE_TYPE.DEPENDENCY;missing->OPP.REVENUE_TYPE.RETURN_MISSING;failed->OPP.REVENUE_TYPE.RETURN_FAILED | OPP.REVENUE_TYPE.RESOLVE_PARENT | stop | Resolve the explicit set decision, exact set, and requested assignment for SingleLookup or every Package REST_FALLBACK row without substitution. FSM Package defers per-row validation to package verification; full-task Export has no selector |
| OPP.REVENUE_TYPE.RESOLVE_STATE | step | 5 | reference_lookup | resolved->OPP.REVENUE_TYPE.VERIFY_PACKAGE;not_found->OPP.REVENUE_TYPE.VERIFY_PACKAGE;empty->OPP.REVENUE_TYPE.VERIFY_PACKAGE;not_applicable->OPP.REVENUE_TYPE.VERIFY_PACKAGE;failed->OPP.REVENUE_TYPE.RETURN_FAILED | OPP.REVENUE_TYPE.DEPENDENCY | stop | Resolve exact current state for SingleLookup or every distinct Package REST_FALLBACK row; native FSM Package and full-task Export continue as not_applicable |
| OPP.REVENUE_TYPE.VERIFY_PACKAGE | step | 6 | reference_lookup | ready->OPP.REVENUE_TYPE.DESIGN;not_applicable->OPP.REVENUE_TYPE.DESIGN;fallback_required->OPP.REVENUE_TYPE.RETURN_FALLBACK_REQUIRED;fallback_candidate->OPP.REVENUE_TYPE.VERIFY_FALLBACK;missing->OPP.REVENUE_TYPE.RETURN_MISSING;failed->OPP.REVENUE_TYPE.RETURN_FAILED | OPP.REVENUE_TYPE.RESOLVE_STATE | stop | Validate native exact-task CSVs, including header-only recovery and unchanged parent linkage; usable or repairable CSV stays on FSM. Only documented exhausted Create/Update/Disable returns fallback_required to the router. REST_FALLBACK returns fallback_candidate for dedicated verification; Export/Import stay FSM-only and Inventory/Read/REST Delete are not_applicable |
| OPP.REVENUE_TYPE.VERIFY_FALLBACK | step | 7 | reference_lookup | eligible->OPP.REVENUE_TYPE.DESIGN;already_applied->OPP.REVENUE_TYPE.RETURN_VERIFIED;missing->OPP.REVENUE_TYPE.RETURN_MISSING;blocked->OPP.REVENUE_TYPE.RETURN_MISSING;failed->OPP.REVENUE_TYPE.RETURN_FAILED | OPP.REVENUE_TYPE.VERIFY_PACKAGE | stop | REST_FALLBACK only: verify final CSV exhaustion, same-target receipt, fresh exact parent/set/per-row reads, and complete prior-submission reconciliation. Pending/uncertain/partial work or repairable CSV blocks; all-applied returns without writing |
