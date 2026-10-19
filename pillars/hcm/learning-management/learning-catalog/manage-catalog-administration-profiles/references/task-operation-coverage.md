

# Manage Catalog Administration Profiles

## Setup Task Metadata

- Task name: `Manage Catalog Administration Profiles`
- Task code: `CUSTOM_MANAGE_CATALOG_ADMINISTRATION_PROFILES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `learningCatalogProfiles`

## Operation contract

The nested task now supports attributed offline proposals and a declared
shared read-only root describe/exact/list workflow. The compiled graph represents
draft/read, create-preparation and raw-write refusal branches. Read readiness
never authorizes Data Loader submission. An evidence-validated root create has
a separate exact-approved continuation through cap_create_submission.
Use cap_workflow for routed reads and cap_proposal for local revision processing.
The table below retains every wider capability and its contract gaps; root
collection retrieval does not require a PATCH item key. See the runtime contract
and FDD mapping for verified local behavior versus pending target acceptance.
Known source behavior and prior target reads are distinguished below. Source
accessor existence, APEX authoring, deployed registration, template columns and
business acceptance are different evidence levels. Do not ask for secrets or
repeat requirements already in the project record.

| Track | Expected behavior and proposed route | Evidence and blocking prerequisite |
| --- | --- | --- |
| CAP-01 Identify | Resolve exact profile number, preserve text precision, cross-check any supplied ID; use actual canonical self identity, page all matches. Zero accessible matches is not proof of absence. | Root number surrogate/finder observed in Stage 1. Canonical date-plus-number key/deployment remains G-02; full metadata G-01. |
| CAP-02 Create/basic attributes | One new root POST via cap_create_handoff preparation and cap_create_submission after exact approval; reviewed name/description/visibility, supplied/generated number policy, current template/grants/duplicates/defaults and independent processing verification. | Shared Task Hook and immutable ZIP approval plus pillar input/evidence/target binding. No central CAP plugin or transport patch. User-supplied root success is not a Data Loader success; current runtime facts must pass. Basic updates use the separate verified-evidence update handoff. |
| CAP-03 Update basics | Dedicated cap_update_handoff/submission supports sparse description/name/visibility through Data Loader. Separately selected cap_batch_update supports basic-attribute shared REST ADF batch updates. Immutable number; clearing/lifecycle/children unavailable. | Loader requires verified mapping/template/omission evidence under update-contract.md. Basic-attribute batch uses current root metadata, unique canonical identity/baseline, privilege assessment, frozen one-part payload and separate immediate exact approval under batch-update-contract.md; no loader mapping inference or automatic route switch. |
| CAP-04 Contributors | Add/change/remove criteria; individual person or person-number resolution, person-number CSV or email CSV. Read actual criterion and attachment identities; verify resolved membership after processing. | Historical APEX hierarchy excluded contributors; a newer saved template includes contributorCriteria. Current child/file contract is unverified, not presumed excluded. sourceType create-only and sourceNumber read-only; G-03/G-08 block all three write methods. |
| CAP-05 Activate | Candidate PATCH status ORA_ACTIVE, only valid transitions, exact identity and authorized grant; already-active is a no-op after readback. | Redwood/source behavior, not load acceptance. Deleted records cannot be presumed restorable; G-02/G-07. |
| CAP-06 Deactivate | Candidate PATCH status ORA_INACTIVE; verify CAN_DEACTIVATE/provider usage and concurrent state, disclose warning/visibility effects. | UI restrictions are not exhaustive server enforcement; G-02/G-07. |
| CAP-07 Delete | Logical status PATCH ORA_DELETED, eligible replacement when used, then verify association migration and source disposition. | Protect system default/providers; missing/nonexistent destination rejected in source. Generic REST DELETE/MERGE_DELETE does not establish this route; G-02/G-07. |
| CAP-08 Content defaults | Update existing seeded type-specific rows and applicable root defaults; separate observer-person replacement diff. No ordinary child POST, DELETE or internal flag bypass. | Six seeded types, allowlists and coupling in source; target exposure/keys/registration/inheritance/reset G-04. |
| CAP-09 Certificates | Update existing CAP certificate setting row; enabled Y requires a permitted nonnull template filename, N/null requires null filename. Verify agreed inheritance/override effects. | Source only; child DELETE disabled. CAP template lookup, live null clearing, registration and rendering G-05; global certificate docs are not the CAP contract. |
| CAP-10 Reconciliation/monitoring | Correlate loader and CAP processing independently; exact membership/migration readback. Requested on-demand reconcile remains blocked until action arguments, privileges and shared route are defined. | Reconcile action advertised, not executable mapping. Needs-processing is not completion; G-06. |

## Governed REST Data Loader route

This is REST import, not FSM CSV export/import (catalog flags remain N). CSV
contributor files are domain input, not an override of the task's CSV flags.
There is no private HTTP client in this pillar. The separate basic-update route
uses the unchanged shared REST client; it is not a Data Loader fallback. The steps below
describe central services reused by the bounded root-create continuation.
Creation and sparse basic updates have separate evidence/approval-gated continuations; other write routes remain unavailable.

1. Resolve project/task/environment identity and operation-specific grants through
   the selected workflow. Confirm deployed BO, components, attributes, live
   template and HCM describe parity. ORA_HRC_DL_ENABLE_FSCR=Y is a technical
   prerequisite, not permission to change the profile option. Keep
   businessObject/BusObjTopDiscriminator=learningCatalogProfiles and
   learningCatalogProfiles.dat; never substitute the display name.
2. The approved canary source is prepared DAT, validated against the target's
   actual shared schema and packaged through shared Data Loader. Offline synthetic
   schema tests prove byte preservation only, not target acceptance. XLSX generation
   is not this route; do not invoke removed HCM sampling flags or replace the
   spreadsheet runtime. Its broader HCM enrichment gap remains G-08.
3. Populate only verified writable columns/sections. Keep big IDs as text. Use
   explicit RestAction POST for the supported single-create route. PATCH uses
   the separate evidence-gated update contract; absent mapping evidence blocks it.
   Generic DELETE produces a DAT delete instruction but is not a certified CAP
   lifecycle operation. Do not invent RECONCILE. effectiveOf is a control helper
   carried to ADF batch Effective-Of, not a business attribute or composite-key
   substitute. Use effectiveOfRangeMode=UPDATE only when the operation's target
   contract agrees with the source UI evidence. YYYY/MM/DD conversion applies
   only to verified Date fields, not arbitrary timestamps. Never invent a
   SysEffectiveDate DAT column, clearing token, custom PatchUrl or date default.
4. Validate and convert through shared core to DAT/immutable ZIP. Keep files,
   sections, parent/child identifiers, selected operation and final ZIP/hash
   consistent. The task-hook data-load validation runs the compiled rule plan;
   a local file check is not a substitute. Incomplete readiness stops here or
   earlier; no waiver is implied by this skill or its implementation approval.
5. Core.data-loader presents the exact task/target/operation and immutable ZIP,
   applies its validation and approval rules, then executes only that approved
   action. Changed ZIP, environment, identity or operation invalidates approval.
   Do not add a second approval for the same core.data-loader task action.
6. Its UCM path uses raw ZIP multipart to /documents/files/data with
   metadataValues and primaryFile, account hcm$/dataloader$/import$ and
   FAFusionImportExport. Not Base64. Use returned dDocName as contentId for
   initiateDataLoad with fileAction=IMPORT_AND_LOAD and core-owned options.
   No invented content ID or alternate uploader. Fusion REST framework version
   9 and supported resource version are core-owned, not silently substituted.
7. Status SUCCESS plus RequestId means submitted only. The shared helper stops
   after initiation: explicitly use the declared monitoring step, correlate
   readDataSetRequestId, paginate dataSetErrors/failedLines/dataSetAllObjects,
   inspect terminal counts and exact business readback. Reconciliation or
   migration is another phase; caught/logged job/event failures are not success.

The root authoring metadata is ADF_REST/ORA_HCM_REST/ORA_FSCR with number
surrogate, EffectiveDated=Y, empty user/foreign keys and null PostUrl/PatchUrl
in the inspected review. Source table metadata is not permission for database
writes. Registration/attribute refresh/template jobs require separate approval.

## Field families and restrictions

Known basics: name max 250 and nonempty; description max 4000; number display30
is not a maximum. Use current maxLength when available and source precision2000
as a local bound; number is create-only. Profile ID big-integer text, resolved
or generated. visibility uses ORA_EVERYONE/ORA_CONTRIBUTORS in prior live lookup,
not old APEX ORA_PRIVATE/ORA_OPEN. Status lookup values are not blanket transition
permission. destinationProfileId is only for the approved replacement intent.
Audit, meanings, processing outputs, isSystemDefault and providerNamesList are
readback fields. Reject unknown/readonly input, precision loss or silent truncation.

Contributor types are ORA_PERSON, ORA_PERSON_LIST and ORA_PERSON_EMAIL_LIST.
Resolve PersonId as sourceId via a documented authorized resolver. Do not PATCH
create-only sourceType, write target read-only sourceNumber, use a person ID as
criterion key or mutate the derived person list. Source attachment hints
attachmentAsyncTrackerId, FileName and DatatypeCode=FILE do not define a complete
file contract. Exact CSV header/encoding/size/duplicate/empty/error semantics and
criterion/attachment removal remain TBD. Observer persons are distinct objects.

Content-default candidate fields (not a target loader column list):

- Attempts/review: learnerAttemptRule, learnerMaximumAttempts,
  learnerAttemptReview, learnerAttemptReviewCondition, disableAttemptsOverride.
- Completion/playback: completionRule, allowBrowseCondition,
  scoredContentCompletionRule, scoreViewRule, allowFwdScrub, completionThreshold,
  showFeedbackToLearner, disableCompletionOverride, effortCalculationRule.
- Observers: obsType, obsManagerType, obsRepType, obsManagerLevel, routingType,
  obsAttemptRule, obsMaximumAttempts, obsAttemptReviewByLearner,
  obsAttemptReviewConditionByLearner, obsAllowBrowseCondition,
  obsAllowReassignment, obsShowFeedbackToLearner,
  disableAttemptsOverrideObserver, disableCompletionOverrideObserver, obsPersonDetails.
- Root defaults: notification/business driver/coordinator/level/publisher,
  enrollment and withdrawal ESS/MSS approvals, learning-content visibility,
  learning-path/community overrides, and post-completion override control.

ORA_SCORM_12, ORA_WEBLINK, ORA_VIDEO, ORA_PDF, ORA_ASSESSMENT and
ORA_OBSERVATION_CHECKLIST are separately seeded types. Source normalizes
SCORM2004/HACP/unknown to SCORM12 lookup, not permission for arbitrary types.
Apply type-specific allowlists, not their union. Limited attempts require a
positive count; single/unlimited defaults 1/-1 apply only in specified branches;
web/video/PDF follow the unlimited branch. Resolve contentDefaultId from readback.
Changing to non-individual observer type can remove observer rows: require an
explicit replacement diff. RoutingType versus routingType, exact type/field and
enum map, nulls, root field applicability and inheritance/reset remain TBD.
Never expose defaultedRow=Y to bypass the ordinary POST rejection.

CAP certificate source seeds ORA_ELEARNING/ORA_COMPLETION_CERTIFICATE with
certificateEnabled=N. certificateId and learningItemId identify row/parent;
certificateTitle is derived. Enable/disable and certificateFileName are candidate
settings, not an attachment upload. An arbitrary filename/URL is not a permitted
template identity. Existing template publication is a separate prerequisite.
Verify empty string versus null, DAT clearing, template grants and CAP new/existing
content inheritance/override/rendering. No inferred global-course behavior.

## Remaining readiness gates and owners

| Gap | Required evidence or prerequisite | Proposed owner, not assigned |
| --- | --- | --- |
| G-01 | Typed root attributes/requiredness/keys; explain empty attribute rows and APEX all-Updatable=No discrepancy. Current target values outrank stale display text. | Registration and Learning REST owners |
| G-02 | Actual canonical item identity, finder/key deployment parity, safe verified composite mapping if needed; separately approved PATCH/readback test. EffectiveDated alone is not a fix. | Learning REST and loader owners |
| G-03 | Verify current contributor criteria/attachment hierarchy; exact parent/criterion/person keys, file contract and add/replace/remove semantics; current target template. Propose registration changes only for confirmed omissions. No assumed root payload workaround. | Learning, registration and core owners |
| G-04 | Target contentDefaults/obsPersonDetails and root default exposure; per-type schema/keys/lookups, update-only registration, observer order, inheritance/reset. | Learning SME/REST owner |
| G-05 | CAP certificates child and template resolver, row key/privileges/null clearing, supported registration, downstream inheritance and render acceptance. | Learning/certificate owner |
| G-06 | Reconcile arguments, response, authorized route/grants, terminal states and correlation, repeat-call/timeout behavior. | Learning processing and core owners |
| G-07 | Operation/data grants, provider/default protections, active nonself replacement, concurrent-change and complete association migration checks. | Security and Learning owners |
| G-08 | HCM sample enrichment and explicit PATCH guarantee; supported file packaging and shared monitoring/error route. No pillar-local fix. | Core owner |
| G-09 | Target release, root-default breadth, certificate inheritance expectations, monitoring wait/interval and scale/performance acceptance. Local delivery approval is not full runtime acceptance. | PM/user and reviewers |

Monitor resources (messages, metrics, userActionHints and resolved person lists)
stay outside writable registration sections. Reconcile is not a DAT RestAction.
Direct GETs are allowed only when a workflow has selected and passed the declared
lookup step. Missing route is a blocker, not grounds for browser or OAuth fallback.

## Source basis and evidence limits

Product-source evidence date: 2026-09-16; migration/FDD review: 2026-09-18.
Reverify deployment/release through an authorized
workflow before runtime. The skill contains generalized source findings; pod IDs,
actual people, browser sessions, test request IDs and historical response bodies
belong only in sanitized project evidence, not reusable instructions.

- [Oracle CAP functional reference](https://docs.oracle.com/en/cloud/saas/talent-management/fatul/catalog-administration-profiles.html).
- [FSCR Learning REST Data Load wiki](https://confluence.oraclecorp.com/confluence/display/VS/REST+Based+Data+Load+for+FSCR+Learning): historical successful create, failed number-only update, effective-date/key distinction. Not tests rerun by this skill.
- [Completion template customization](https://docs.oracle.com/en/cloud/saas/talent-management/fatul/configure-completion-certificate-templates-for-oracle-learning.html) and [global certificate behavior](https://docs.oracle.com/en/cloud/saas/talent-management/fatul/completion-certificates-for-oracle-learning-courses-specializations-and-legacy-items.html): not CAP API proof.
- Fusion source base hcm/components/hcmLearn/common/model/src/oracle/apps/hcm/learn/common/model/: catalogadminprofiles/persistence/CatalogAdminProfilesHelper.java (106–305,418–852); CatalogAdminProfilesPersistenceHelper.java (63–73); catalogadminprofiles/view/LearningContentDefaultRulesVOImpl.java (42–69,110–130); CapDefaultCertificatesVO.xml (24–236); catalogadminprofiles/util/LearningCatalogProfilesEnums.java (15–111); items/digitallearning/util/DigitalLearningValidationUtil.java (925–944). Line ranges refer to reviewed snapshots, not universal release locations.
- Local restModel LearnerRestAM_LearningCatalogAdminProfilesVOResources.xml (13–110): child hierarchy and disabled DELETE. Redwood CAP action chains: logical status updates, effectiveOfRangeMode UPDATE and lifecycle safeguards. Their presence is not target behavior certification.
- Local shared core/data-loader source reviewed in Stage 1: HCM/FSCM enrichment mismatch and unverified-update POST fallback. Request a core-owner remedy separately; do not change core here.

## Local verification and resume

Use the unchanged shared compiler and planner without operation extensions.
The ready task graph exposes draft/read/preparation and raw-write refusal branches.
Authorized retrieve/list use shared GET. Exact-approved root creation uses the
dedicated shared submission continuations for create and sparse basic updates; lifecycle and child writes remain unavailable.
Read [runtime limits](runtime-contract.md) and [FDD reconciliation](fdd-traceability.md).
Offline algorithms and one-row create-preparation checks remain available in the
pillar scripts. No shared readiness override or alternate HTTP client is allowed.
An implemented route is not evidence of a completed load. On resume read project INDEX/CHECKPOINT first; preserve
the existing Run Book and distinguish historical live evidence from offline tests.
