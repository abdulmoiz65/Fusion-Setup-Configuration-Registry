# Manage Levels of Risk Reference Lookups

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

Resolve the exact MOO_SETID_RISK_LEVEL parent before resolving sets or child codes.
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
| resolve_manage_levels_of_risk_parent | Input validation succeeds | Catalog-fixed mapping of Manage Levels of Risk (MOO_MANAGE_LEVELS_OF_RISK) to LookupType MOO_SETID_RISK_LEVEL | GET /fscmRestApi/resources/11.13.18.05/setEnabledLookups/MOO_SETID_RISK_LEVEL?fields=LookupType,Meaning,Description,ModuleId,CustomizationLevel,RestAccessSecured,ReferenceGroupName&links=self,canonical; do not use onlyData=true because canonical links are required | LookupType, Meaning, Description, ModuleId, CustomizationLevel, RestAccessSecured, ReferenceGroupName, and returned self/canonical links | Require exactly one response whose LookupType is exactly MOO_SETID_RISK_LEVEL and whose ReferenceGroupName is nonblank; task ownership comes from this adapter's exact catalog mapping, not REST presence alone | LookupParent, ReferenceGroupName, CustomizationLevel, RestAccessSecured, ParentItemLink, CatalogTaskScopeEvidence | A healthy exact 404 is not found and blocks this adapter; blank ReferenceGroupName, mismatched type, many results, 401/403, malformed data, or a catalog mapping mismatch fails closed |
| resolve_risk_reference_set | The exact parent and returned ReferenceGroupName resolve for a SingleLookup request | SetId, SetCode, BUOrgId, or OrganizationCode plus returned ReferenceGroupName | For SetId, GET /fscmRestApi/resources/11.13.18.05/setIdSets with finder=PrimaryKey;SetId={SetId}; for SetCode use finder=SetCodeFinder;SetCode={SetCode}. For BUOrgId, GET /fscmRestApi/resources/11.13.18.05/setIdAssignmentsBusinessUnit with finder=AssignmentFinder;DeterminantValue={BUOrgId},ReferenceGroupName={returned ReferenceGroupName}; for OrganizationCode use finder=DeterminantFinder;bindBusinessUnitCode={OrganizationCode}, then validate the exact returned ReferenceGroupName. Pass each finder as one URL-encoded query value, request only the listed fields plus self/canonical links, and advance offset until hasMore=false | SetId, SetCode, SetName, OrganizationId, OrganizationCode, ReferenceGroupName, self/canonical links, and hasMore | Require one exact set and, when BU-scoped, one exact assignment whose ReferenceGroupName equals the parent-returned value; multiple selectors must resolve to the same set, and absence cannot be inferred from an incomplete page | SetId, SetCode, SetName, BUOrgId when supplied, returned ReferenceGroupName, RecordSetAssignmentVerified, canonical links, pagination completion | Stop on no set, incomplete pagination, conflicting selectors, more than one exact set, or a missing/mismatched BU assignment; return the adapter's record-set prerequisite without mutating it |
| resolve_risk_lookup_state | The parent, reference set, and applicable assignment resolve | Resolved SetId and optional LookupCode | For a code, GET /fscmRestApi/resources/11.13.18.05/setEnabledLookups/MOO_SETID_RISK_LEVEL/child/lookupCodes with finder=PrimaryKey;LookupCode={LookupCode},SetId={SetId}, passed as one URL-encoded query value, plus fields=LookupCode,SetId,SetCode,Meaning,Description,EnabledFlag,StartDateActive,EndDateActive,DisplaySequence,Tag and links=self,canonical. For Inventory, use q=SetId={SetId}, the same fields/links, a bounded limit, and advance offset until hasMore=false | LookupCode, SetId, SetCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, self/canonical links, and hasMore | For Inventory, return every exact-SetId code only after pagination completes; otherwise require zero or one exact case-sensitive LookupCode and SetId match | Sanitized current code state, current-state fingerprint and timestamp, pagination evidence, and returned child item identifier or item link | An empty completed Inventory is valid; not found is valid only for Create; stop on many exact matches, incomplete pagination, identity mismatch, or lookup failure |
| verify_risk_fsm_package | Package Export; SingleLookup Create, Update, or Disable; or Package Create, Update, Disable, or Import after route-aware state resolution | For Export: exact target/release/task identity and a fresh completed MOO_MANAGE_LEVELS_OF_RISK baseline ZIP. For SingleLookup mutation: that baseline plus a separate immutable final ZIP and exactly one reviewed row matching the resolved set/code/state. For Package mutation or Import: the baseline plus a separate immutable final ZIP and every reviewed changed row. Every final ZIP supplies ASM_SETUP_CSV_METADATA.xml, metadata-derived members and headers, PackagePath, PackageSha256, and exact TaskName; every mutation or import handoff also supplies persisted `TaskContextPath` plus positive `TaskSequence`, resolved to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area | Local read-only ZIP, metadata, CSV, persisted Data Loader task context, and SHA-256 validation; no Fusion mutation | For Export: TaskCode, environment, release, completed status, export timestamp, baseline members, headers, path, and SHA-256. For SingleLookup mutation: also the one changed row identity, set, state lock, delta, impact, and final package identity. For Package mutation or Import: those same values for every changed row | Export validates the unmodified full-task baseline without requiring a set selector, code, changed row, state lock, or impact. SingleLookup Create/Update/Disable requires exactly one changed MOO_SETID_RISK_LEVEL row matching the previously resolved set, code, and state. Package Create/Update/Disable/Import atomically validates every changed row and may span multiple codes and sets. Both mutation modes preserve exact task identity, metadata-derived members and headers, minimal reviewed deltas, fresh state locks, impact evidence, and unchanged bytes. Every mutation or import handoff requires persisted Data Loader task context. Data Loader binds finalData.archiveSha256 only after handoff | For Export: validated baseline receipt. For mutation or Import: FsmPackageReady, validated package summary, per-row identities, sets, state locks, impacts, task context and its resolved identities, and PackageSha256 | Missing, stale, cross-environment, malformed, scope-expanded, or changed evidence is not ready; never synthesize missing context or files/headers, mutate the source export in place, or substitute FND_MANAGE_SET_ENABLED_LOOKUPS |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The reference set cannot be resolved exactly | Stop before reading codes or creating a preview |
| SetSelectionDecision is absent or Common Set was inferred | Stop and ask whether Common Set should be used or a different exact SetId, SetCode, BUOrgId, or OrganizationCode should be supplied |
| SetId is malformed/nonpositive, SetCode is blank, or the selected-environment set does not exist | Stop before code lookup or preview; do not substitute Common Set, another environment's set, or a close match |
| SetId/SetCode disagree, confirmed Common Set resolves elsewhere, or the set conflicts with the BU/organization assignment, confirmed request, export, or package row | Stop as a set-scope conflict, disclose sanitized returned identities, and require one corrected explicit set decision |
| The parent is absent, mismatched, has no ReferenceGroupName, or lacks task-scope evidence | Stop before set or code lookup; do not substitute a generic set-enabled type |
| A requested business-unit assignment for the parent-returned ReferenceGroupName is absent | Return ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES as the prerequisite gap and do not change the assignment here |
| A single-code lookup returns one exact item | Preserve current state and the returned child identifier or item link for design validation and preview |
| No exact single code is found | Continue only as a Create candidate; Read, Update, Disable, and Delete remain blocked |
| Fusion returns 401 or 403 | Stop as authentication or privilege failure; do not treat the lookup or code as absent |
| A mutation is requested through a reference lookup | Refuse and pass only validated evidence to the adapter's execution gate |
| A collection reports hasMore=true or pagination is incomplete | Continue the read; never report absence or a complete inventory until hasMore=false |
| FSM package verification is not applicable to Inventory, Read, or Delete | Continue to the execution gate with not_applicable; Delete must satisfy its separate REST-only contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.RISK.RESOLVE_PARENT | step | 2 | reference_lookup | resolved->OPP.RISK.RESOLVE_SET;missing->OPP.RISK.RETURN_MISSING;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.VALIDATE | stop | Resolve the exact MOO_SETID_RISK_LEVEL parent, task scope, editability metadata, canonical link, and nonblank ReferenceGroupName |
| OPP.RISK.RESOLVE_SET | step | 3 | reference_lookup | resolved->OPP.RISK.DEPENDENCY;not_applicable->OPP.RISK.DEPENDENCY;missing->OPP.RISK.RETURN_MISSING;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.RESOLVE_PARENT | stop | Require the explicit Common-versus-different set decision, then resolve one exact set and any requested BU assignment; reject malformed, unknown, cross-environment, Common-choice, selector, assignment, export, or row-identity conflicts without substitution; Package mode defers per-row validation to verify_risk_fsm_package, and Export has no set selector |
| OPP.RISK.RESOLVE_STATE | step | 5 | reference_lookup | resolved->OPP.RISK.VERIFY_PACKAGE;not_found->OPP.RISK.VERIFY_PACKAGE;empty->OPP.RISK.VERIFY_PACKAGE;not_applicable->OPP.RISK.VERIFY_PACKAGE;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.DEPENDENCY | stop | Resolve current state for SingleLookup; Package mode and full-task Export continue as not_applicable |
| OPP.RISK.VERIFY_PACKAGE | step | 6 | reference_lookup | ready->OPP.RISK.DESIGN;not_applicable->OPP.RISK.DESIGN;missing->OPP.RISK.RETURN_MISSING;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.RESOLVE_STATE | stop | Validate a set-less full-task Export baseline, exactly one resolved row for SingleLookup Create, Update, or Disable, or every changed row in a Package mutation or Import; Inventory, Read, and REST Delete are not_applicable |
