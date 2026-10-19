# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Resolution Policy

Resolve codes, names, meanings, descriptions, translations, and ordinary user wording in any language to one authoritative member. Canonical output values are resolution targets, not restrictions on input language or phrasing. Reject no-match only after complete supported authority establishes absence; actual ambiguity or known incompatibility requires correction. Preserve authored names and translated text.

Assigned sets use the field-specific input contract below instead of the broad cross-field resolution policy: name input searches SetName only; explicit code input searches SetCode only. Other resolvers retain their own documented matching rules.

Missing optional reference authority or unverified UI/import eligibility parity is REFERENCE_UNRESOLVED, Warning, blocking=false. Required consumer-impact evidence for an existing identity and required translation-name collision evidence are separate gates: absence or an invalid evidence contract is blocking and cannot use that warning outcome. Preserve supplied values in their proven CSV representation, disclose the skipped check and next evidence needed, and continue every remaining supported check and preview without a waiver only when required gates are satisfied. Do not invent a code or ID from unresolved prose; ask only if actual ambiguity or a missing representation prevents construction. Failed supported reads, incomplete pagination, malformed packages and proven invalid values remain errors. Developer SQLcl, CodeSearch and undeclared exports are never runtime fallbacks.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_work_type_transfer_type | Transfer Price Amount Type supplied or source-confirmed defaulted | Candidate mappings below plus supported current target package/template evidence; static completeness unverified | Resolve code, meaning, translation, or unambiguous natural-language intent; emit a mapped code only when its serialization is evidenced | PJF_PROJECT_WORK_TYPE.csv.TpAmtTypeCode = evidenced code, never display Meaning; otherwise preserve only proven supplied representation and disclose the unverified check | Actual ambiguity or missing payload representation needs clarification; absence from the candidate list alone is not proof of invalidity; no additional live lookup declared |
| resolve_work_type_boolean | Billable or Utilizable supplied or source-confirmed defaulted | Independent checkbox semantics and candidate serialization mappings below, confirmed by current target contract evidence | Resolve boolean, code, translated meaning, or ordinary affirmation/negation independently; require evidence for serialized Y/N mapping | PJF_PROJECT_WORK_TYPE.csv.BillableCapitalizableFlag or UtilizableFlag = evidenced value for the intended column; no interchange | Block ambiguous intent; unverified serialization mapping must not become a guessed value; preserve proven supplied representation and disclose unverified checks |
| find_work_type | Create/update/import | Fresh joined base/set/translation FSM export | Resolve supplied identity or evidenced alternate wording to one canonical work-type identity; stable ID when available; preserve a new requested name on create | Exists, baseline, dates, flags, children; canonical parent Name for child references | Verified absence permits create only; one=update; ambiguity or incomplete evidence blocks |
| resolve_work_type_children | Create or translation/DFF change | Current child baseline, complete fresh target translation baseline retained from the selected same-task FSM export, prepared child diffs, confirmed target name-comparison evidence, resolve_work_type_dff_context evidence result and applicable resolve_work_type_languages output | Resolve supplied translation rows to the parent and language; preserve omitted children on update. Apply Translation Name Collision Check below before returning resolved. Carry unavailable DFF/translation eligibility checks as warnings while completing all supported checks | Resolved translation identities, explicit child diffs and name-collision check evidence with baseline/change references; retain optional unresolved warnings without claiming complete DFF validation | Duplicate parent/language rows or translated-name collisions require correction. Missing, stale or incomplete required collision evidence returns failure, never REFERENCE_UNRESOLVED. Missing optional DFF/eligibility authority alone remains Warning, blocking=false |
| resolve_work_type_dff_context | Create or DFF change | Flexfield Support below; requested operation and changed CSV fields | Updates preserving DFFs require no DFF lookup. No verified Work Types deployed context/segment metadata acquisition route is currently declared; membership, requiredness and context/segment mapping remain unverified | Preserve supplied AttributeCategory and Attribute1 through Attribute15 in their proven serialized representation; emit REFERENCE_UNRESOLVED, Warning, blocking=false with skipped checks; no validated segment output | Continue supported checks/preview without waiver or manual metadata requirement. Ask only for ambiguity or missing representation; never infer a code or CSV mapping from unresolved prose |
| resolve_work_type_languages | Translation Language or SourceLang supplied | Current-run acquire_work_type_languages output | Resolve each field independently across the complete unfiltered catalog by Fusion code, description, evidenced language tag or unambiguous multilingual intent; retain installation/activation status as evidence only | Canonical Language and SourceLang, separately; uniqueness by parent Work Type and Language. Missing Work Type import-eligibility parity is REFERENCE_UNRESOLVED, Warning, blocking=false | Complete catalog with zero identities is missing; multiple identities ambiguous; inaccessible catalog is an operational error. InstalledFlag/ActivationStatus alone do not prove incompatibility. Never equate SourceLang with Language or infer an ISO mapping |
| resolve_work_type_use | Existing identity with an actual billable/utilizable/transfer, availability-date or set-assignment diff | Local caller handoff work_type_use_evidence, captured from a completed operation selected by the active workflow; Consumer Impact Evidence Contract below | Validate the handoff against the resolved identity, target, current run and proposed diff using the contract below; no acquisition operation is declared by this resolver | satisfied with validated coverage, counts, transaction ranges, profile state and impact facts; not_applicable only for no relevant diff or a new identity proven absent from the complete fresh baseline | Missing evidence/source route returns missing; invalid, stale, mismatched or incomplete evidence returns failure; both block. Never emit REFERENCE_UNRESOLVED for this dependency or infer zero consumers. Proven unsafe impact is retained for dependency/design conflict handling |
| verify_work_type_scope | Before validation | Catalog codes and target | Exact task/target | Verified scope | Block mismatch |
| verify_work_type_package | Import preparation before preview | Current template/export, final immutable archive, verified Data Loader preflight and retained preparation context | Exact conditional members, headers and counts; require the preflight SHA-256 to match the prepared archive; preserve original input/evidence provenance | Verified prepared-package contract for Task Hook preview; integrity values remain internal | Block unproven/mixed package or archive/preflight mismatch; repeat preparation and validation before preview. Later submission uses the intact approved archive, not the original source; changed approved artifact or target/context requires fresh validation and approval |

## Translation Name Collision Check

These mechanics belong to resolve_work_type_children and run at
WTYPE.RESOLVE_CHILDREN before preview whenever translation rows are supplied.
Reuse only the selected workflow's retained export and prepared-package context;
this check declares no new acquisition route or original-source reread.

| Situation | What Happens |
|---|---|
| Required baseline and change scope | Require the complete fresh target translation baseline across all work types and languages, joined to canonical base identities, plus the exact prepared child diffs. A baseline filtered to one work type, reference set, active date or language is not enough to establish absence. Verify target/run and baseline/change binding; missing, stale, mismatched or incomplete evidence returns failure |
| Parent and language identity | Resolve each child parent to its canonical base identity and Language to its Fusion identity first. Reject duplicate proposed rows for the same parent plus Language before overlaying changes; never let the last row silently win. SourceLang is not part of the uniqueness key |
| Resulting rows | Preserve every omitted baseline translation. Replace each explicitly changed parent/Language row with its proposed row and add explicitly new rows. Compare the resulting Name/Language pairs across distinct work-type identities, including other proposed rows and preserved baseline rows. Exclude only the previous version of the same changed row; never exclude all rows of a changed work type or all proposed identities |
| Same identity and different languages | An unchanged translation for its own parent/Language is not a self-conflict. The same Name in different resolved languages is not a collision under this key. Renaming one row does not remove a different work type's retained row or reserve the old name forever |
| Comparison semantics | Preserve authored Name exactly. Use confirmed target uniqueness-comparison semantics and record their evidence reference; do not borrow assigned-set trimming/case-folding, strip accents, normalize Unicode or infer database collation. If missing comparison authority prevents establishing the result, return failure with the missing check; never report unverified uniqueness as passed |
| Collision or incomplete check | Different work-type identities sharing a Name/Language under the confirmed comparison produce WTYPE_TRANSLATION_NAME_CONFLICT, blocking=true, and WTYPE.RESOLVE_CHILDREN failure to WTYPE.RETURN_ISSUES. Identify affected rows, language and conflicting work types using sanitized display evidence. Incomplete required evidence produces WTYPE_TRANSLATION_NAME_CHECK_INCOMPLETE on the same failure path; neither is waived by optional reference warnings or upload approval |
| Collision-free result | Record baseline/change and comparison evidence, resolved parent/language keys, checked candidate counts and the collision-free result for every proposed row. Continue remaining supported child checks and retain optional DFF/eligibility warnings; this result does not prove a live import or authorize submission |

Source reviewed on 2026-10-12: [PJF_WORK_TYPES_TL, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypestl-25298.html),
Indexes, PJF_WORK_TYPES_TL_U2 is unique on NAME and LANGUAGE, independently of
the parent/language key. This establishes the collision constraint; it does
not establish target collation, FSM row ordering or atomic rename behavior.
A collision-free resulting state does not authorize reordering rows, splitting
loads or assuming a multi-row name swap imports atomically. Unverified importer
behavior remains subject to the existing supported package contract.

## Consumer Impact Evidence Contract

This is the caller handoff contract approved for the task's consumer-impact gate. It validates evidence already captured by the active workflow; it does not acquire evidence, designate a new Fusion endpoint, or make an unsupported source authoritative. No consumer/profile acquisition adapter is currently declared by this task. Without a completed, workflow-selected source satisfying this contract, affected existing-identity changes stop with a workflow gap.

| Situation | What Happens |
|---|---|
| Handoff source | Accept work_type_use_evidence only from the active caller's captured context. Require source_skill_or_adapter, workflow_step_ref, operation, evidence_ref and successful acquisition_status, all traceable to a completed supported operation explicitly selected by that workflow. A user assertion, manually assembled snapshot or arbitrary file is not sufficient authority; do not request one as a workaround |
| Target and identity | Require TargetEnvironment, task_code=PJF_MANAGE_WORK_TYPES and canonical work_type_identity matching the fresh joined baseline and current request. Match a stable ID when the baseline exposes it; otherwise require the uniquely resolved base identity. Cross-target, ambiguous or mismatched evidence is invalid |
| Run and change binding | Require run_ref, collected_at and proposed_change_ref matching the current run and exact diff. Acquisition must complete after the current baseline and proposed diff are established, before the gate is evaluated. Future timestamps, previous-run evidence, changed target/identity/diff, or reported intervening consumer/profile changes invalidate the handoff. Do not reuse it across preparation runs |
| Coverage | Require coverage entries for project types/templates/projects/tasks, assignments, expenditures, billing, cross-charge and utilization, plus the relevant profile state. Each entry names its selected source operation, scope, acquisition time and successful complete status. Pagination must be complete where applicable; absent categories, partial reads, truncated extracts, unknown completeness or unsupported exclusions return failure. A not-applicable category requires a reason evidenced by the selected workflow; it cannot replace unknown coverage |
| Consumer facts | Every applicable category supplies a nonnegative integer consumer_count and, for dated consumers, transaction_date_min and transaction_date_max with confirmed date semantics and min no later than max. Missing/null counts are unknown. A verified zero count needs explicit complete-scope evidence; null date bounds are allowed only for verified zero consumers or an evidenced undated category |
| Profile and impact facts | Require the profile values governing billability and the evidence needed to assess each changed flag/type, availability boundary or assignment. Positive consumer counts do not prove a conflict by themselves; expose affected consumers and dates to the owning design rule. Missing profile state or impact facts return failure; do not label an unchecked change safe |
| Output and graph outcome | Return satisfied only after all applicable contract checks pass; return missing for an absent handoff or undeclared source operation, and failure for a supplied invalid handoff. At WTYPE.FIND_WORK_TYPE, missing/failure maps to its failure transition to WTYPE.RETURN_ISSUES. If a gap is detected later, WTYPE.RESOLVE_DEPENDENCIES uses missing to WTYPE.RETURN_ISSUES; WTYPE.ENFORCE_DESIGN uses blocked to WTYPE.RETURN_REFUSAL. No warning or approval transition can replace these outcomes |
| No relevant impact diff | A Description-only update, translation/DFF-only update, or resubmission preserving flags/dates/sets records not_applicable with the compared baseline/diff. A new unique identity records absence evidence from the complete fresh target baseline; no historical-use lookup is required. Omission alone does not establish that an existing identity has no relevant diff |
| Diagnostics and storage | Return sanitized source references and missing checks through the caller's normal task-rule result. Record a workflow gap with stage, failure_class, recommended_action, target and safe evidence references in the caller's authorized durable record. Keep raw consumer data, protected runtime identifiers, hashes, approval objects and source payloads internal; this handoff does not authorize an extra export, original-source reread or task-local copy of loader artifacts. Preserve Task Hook's prescribed validation-result evidence |

## Transfer Price Amount Type
CSV columns: PJF_PROJECT_WORK_TYPE.csv.TpAmtTypeCode

| Lookup Code | Meaning |
|---|---|
| COST_TRANSFER | Cost transfer |
| REVENUE_TRANSFER | Revenue transfer |

The table retains candidate serialization mappings from prior authoring; its provenance as a complete fixed PJF_TP_AMT_TYPE_CODE seed list is unverified. Oracle 26D documents Cost and Revenue business classifications, but the consulted sources do not enumerate these exact stored codes or prove that the list is exhaustive. Confirm mappings through the selected workflow's supported target package/template evidence before deriving a code from intent. No additional lookup or database route is declared; absence from this table alone cannot establish invalidity.

## Billable and Utilizable
CSV columns: PJF_PROJECT_WORK_TYPE.csv.BillableCapitalizableFlag; PJF_PROJECT_WORK_TYPE.csv.UtilizableFlag

| Lookup Code | Meaning |
|---|---|
| Y | Yes |
| N | No |

Yes and No describe the independent checkbox intents. Y and N are retained candidate CSV serialization mappings; the prior claim of database YES_NO corroboration has no traceable research record in this package. Confirm the current target serialization contract before deriving a stored value from intent. Preserve explicit, proven serialized values and the independent business intent of each flag; do not claim that the public table documentation establishes these literals.

## Flexfield Support

CSV columns: PJF_PROJECT_WORK_TYPE.csv.AttributeCategory; PJF_PROJECT_WORK_TYPE.csv.Attribute1 through PJF_PROJECT_WORK_TYPE.csv.Attribute15

This task currently has no supported runtime route to acquire deployed Work
Types context and segment metadata. Report missing membership, requiredness,
and segment-mapping authority as REFERENCE_UNRESOLVED, Warning, blocking=false
for create or DFF changes; continue supported validation and preview with these
checks explicitly unverified. Preserve supplied values only in their proven
serialized CSV fields; unresolved prose must not become a guessed code or
segment assignment. Updates preserving existing DFFs do not run this check.
A blank context does not prove the absence of global segments. Do not request
manually assembled metadata, invent segment labels, or substitute deployment
status for context/segment validation. Enforce known constraints when supported
evidence exists; this warning does not excuse proven invalid values. No static
context/segment values or speculative REST route are prescribed.

## Translation Fields Without a Task-Page LOV

CSV columns: PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.Language; PJF_PROJECT_WORK_TYPE_TRANSLATION.csv.SourceLang

Language and SourceLang are required stored Fusion language codes, not task-page LOV controls. Acquire their current identity catalog through acquire_work_type_languages. Installation and activation state do not establish Work Type import eligibility; retain that unverified check as a nonblocking warning. Retain explicit SourceLang semantics and the current translation baseline; do not manufacture source relationships. Translated Name and Description are authored text, not lookup values. The parent reference remains the base work type Name and is distinct from translated Name.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_work_type_sets | Set supplied or explicitly changed; create with omitted assignments needs no set lookup | Original user value and explicit name/code label, authenticated target, and current work-type assignment baseline; an agent-derived SetCode retains its original name-resolution evidence | /fscmRestApi/resources/11.13.18.05/setIdSetsLOV?onlyData=true&fields=SetCode,SetName,Description&limit=500&offset=0&orderBy=SetCode | SetCode, SetName, Description | Complete Set Acquisition once per run/source context, then apply Assigned Set Input and Matching below. Name input compares SetName only; explicitly labeled code input compares SetCode only. No description, fuzzy or cross-field fallback. No active-date, business-unit, project-unit, Common-set or Enterprise-set exclusion is evidenced | PJF_PROJECT_WORK_TYPE_ST.csv.SetCode = returned SetCode; retain input type, matched field, candidate count and display evidence internally. Derive assignment count from the separate work-type baseline and proposed diff | Unique name: derive code and continue without code clarification. Multiple name matches: show returned candidates for selection. Zero name matches: request a corrected name only when needed to construct the code, never reinterpret as code. Actual ambiguity, conflicting duplicate codes, failed/incomplete retrieval or missing identity fields are errors. Unverified task/security parity remains REFERENCE_UNRESOLVED, Warning, blocking=false; preserve only proven representation, never insert SetName or numeric SetId into CSV |
| acquire_work_type_languages | Translation rows supplied and no complete same-run catalog exists | Target, authenticated identity and application language | GET /fscmRestApi/resources/11.13.18.05/languagesLOV?onlyData=true&fields=LanguageCode,Description,LanguageTag,InstalledFlag,ActivationStatus&limit=500&offset=0&orderBy=LanguageCode | LanguageCode, Description, LanguageTag, InstalledFlag, ActivationStatus | Complete Language Acquisition and Resolution below before resolving either language field; no installed/active filter | Scoped language catalog for resolve_work_type_languages | Separate inaccessible/incomplete acquisition from missing/ambiguous identities; no fabricated CSV output |

## Assigned Set Input and Matching

These rules are owned by resolve_work_type_sets. Apply them independently to each supplied assignment before constructing its CSV SetCode. A value that looks like a code is still a name unless the user explicitly identifies it as a code.

| Situation | What Happens |
|---|---|
| Unqualified assigned-set value, set name wording, or user-authored SetName/assigned_set_name field | Search SetName only. Compare the complete name after trimming surrounding whitespace and case folding; preserve the returned literals. Do not match SetCode, Description, substrings, prefixes, translations inferred outside the returned SetName, or fuzzy intent |
| Explicit set code wording, such as set code is XYZ or code is XYZ in the assigned-set context, or user-authored SetCode/assigned_set_code field | Search SetCode only using exact equality after trimming surrounding whitespace. Do not switch to SetName or Description if the code has no match |
| Both name and code explicitly supplied for the same assignment | Match each field according to its own rule and require the same returned identity; conflicting input needs correction |
| One distinct SetCode matches the supplied name | Derive the returned SetCode automatically. Do not ask the user to supply, confirm or relabel the code; retain any separate eligibility warning |
| Multiple distinct SetCodes match the supplied name | Show the returned SetName, SetCode and Description as disambiguators and ask which set is intended; do not require the user to know a code beforehand |
| No name match after complete acquisition | Never fall back to a matching code or description. If no canonical code can be constructed, request a corrected set name. Retain unverified task/security parity as a warning instead of claiming proven task invalidity |
| No explicit-code match after complete acquisition | Never fall back to a matching name. If no proven code representation is available, request a corrected explicit code; retain any parity warning |
| Agent-generated SetCode field from original name input | Preserve the original name input type and name-to-code evidence. The output column is not evidence that the user supplied a code. During Task Hook validation use the prepared package and retained preparation context; do not reread the original source or guess the original label. Missing preparation evidence needs clarification of the original set name, not reinterpretation as a code |
| Failed or incomplete collection | Report the supported lookup failure; do not substitute a code question for completing or restoring the declared read |

## Set Acquisition

Use the shared REST client for one complete collection acquisition, reused by
all supplied set assignments in the run. Complete-fetch selection supports
name-only matching or explicitly selected code-only matching; Description is
display evidence, not a matching field. Do not exclude candidates through an
assumed filter. Research on 2026-09-18 found a moderate
database population, but API-visible size/security scope remains unknown;
that observation is neither an API count nor a permanent cap. Reassess page
metadata during the selected read. No per-row HTTP calls are prescribed.

Start at offset=0 and advance by the actual returned item count until
hasMore=false. Use stable SetCode ordering; detect repeated/conflicting codes,
missing identity fields, failed later pages and empty/nonprogressing pages with
hasMore=true as incomplete acquisition. Cache by run, target, read identity,
application language, resource/version, requested fields, ordering and filter
scope; key resolved matches by input type as well as normalized value, so a
name and a code with identical text cannot share a resolution. Share compatible
results across repeated same-type set inputs only
within that context. No cross-target or stale reuse. The documented collection
establishes returned set identities; precise task UI/security population parity
remains unverified and must not be claimed as a successful eligibility check.

## Language Acquisition and Resolution

Use the existing core.fusion-api.rest-api-client GET workflow for
acquire_work_type_languages. Confirm the target, read identity and application
language, then fetch the complete catalog with offset=0, limit=500 and
orderBy=LanguageCode. Advance by actual returned count until hasMore=false.
Validate required fields, count, offset and items; reject failed, duplicate or
nonprogressing pages. A failed read is inaccessible, never proof of absence.
Scope the result to target, identity, language, resource/version, requested
fields, unfiltered ordering and this run; do not reuse a prior run's collection.
Execute the lookup only for supplied translation rows and share it across both
language fields and repeated normalized intents. The language catalog is
expected to be small; the research DB population is not an API-visible size
or permanent limit. Always complete the documented paging contract.

Match Language and SourceLang independently using returned codes, descriptions
or evidenced language tags and unambiguous multilingual intent. No candidates
after complete identity acquisition is missing; multiple codes is ambiguous.
Retain installed/active state as evidence, not an unsupported exclusion. Never force English,
equate the two fields, or infer a code from an ISO abbreviation. Successful
resolution establishes catalog identity only. Missing Work Type import-eligibility
parity is REFERENCE_UNRESOLVED, Warning, blocking=false; continue other checks.

The [documented language collection (26D)](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-languageslov-get.html)
supplies the identity and state fields. If this endpoint is inaccessible in the selected target, report
that failure; do not substitute another access method.

## Assigned Sets

CSV columns: PJF_PROJECT_WORK_TYPE_ST.csv.SetCode

Reference data sets are editable setup data, not an immutable seeded list. Resolve against the current target collection; do not hardcode Common or any tenant-specific set. Use the documented set-ID-set lookup as the identity authority. No enabled flag or effective-date predicate is evidenced for this collection. Assignment-preservation and consumer-impact rules are separate from set membership.

The shared GET-all contract is documented in [Oracle Get all set ID sets (26D)](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-setidsetslov-get.html). Refresh identities at runtime and retain the UI/security parity warning rather than treating API visibility as complete task eligibility.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| Base/child group omitted | Preserve current values/rows |
| Set collection hasMore=true | Advance offset by the actual returned item count, not the requested limit; complete all pages before assessing uniqueness or absence. Failed, repeated or nonadvancing pages are operational errors |
| Set removal requested | Compute remaining assignments from the work-type baseline and proposed diff; evaluate BU/set consumers separately. Do not invent active dates for reference sets |
| Billable flag changes | Disclose profile-dependent scheduled/actual billing behavior; do not backdate silently |
| Transfer type changes | Disclose cost-versus-revenue cross-charge pricing impact |
| workTypesLOV is readable | Use for discovery only; do not treat as write authority |
| DFF metadata or task eligibility authority unavailable | Emit REFERENCE_UNRESOLVED, Warning, blocking=false; preserve proven representation and continue all supported checks/preview without waiver; disclose skipped checks |
| Package/template malformed or supported acquisition failed | Keep the operational/contract error distinct from an unresolved-authority warning; do not claim complete validation or use an undeclared fallback |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WTYPE.FIND_WORK_TYPE | step | 3 | reference_lookup | resolved->WTYPE.RESOLVE_CHILDREN;warning->WTYPE.RESOLVE_CHILDREN;failure->WTYPE.RETURN_ISSUES | WTYPE.APPLY_DEFAULTS | stop | Resolve work type and sets; validate required consumer-impact handoff for existing-identity impact diffs; missing/invalid handoff uses failure, never warning |
| WTYPE.RESOLVE_CHILDREN | step | 4 | reference_lookup | resolved->WTYPE.ROUTE_OPERATION;warning->WTYPE.ROUTE_OPERATION;failure->WTYPE.RETURN_ISSUES | WTYPE.FIND_WORK_TYPE | stop | Resolve translations, check translated-name collisions, DFFs, and semantic impact; complete required collision evidence and supported reads before returning warnings |

## Source Evidence and Static Mapping Limits

Reviewed on 2026-10-08 against the latest published release 26D.

| Claim | Source and locator | Confirmed scope |
|---|---|---|
| Work types support billing and cost/revenue cross-charge classification | [Work Types for Billing, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oapfm/work-types-for-billing.html), Billable Project Work and Cross-Charge Classification | Business semantics, including the profile-dependent billability effect; no exact transfer lookup code list or checkbox CSV literals |
| Separate billable and utilizable fields; transfer classification storage | [PJF_WORK_TYPES_B, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypesb-25294.html), BILLABLE_CAPITALIZABLE_FLAG, UTILIZABLE_FLAG, TP_AMT_TYPE_CODE | Separate stored fields, lengths and descriptions; no UI defaults or exhaustive lookup members |
| Work Types LOV discovery | [Get all work types, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/fapap/op-worktypeslov-get.html) | Read-only discovery contract; does not authorize setup writes or establish all task CSV mappings |
| COST_TRANSFER / REVENUE_TRANSFER and Y / N serialization; fixed-list completeness | Prior authoring assertions; no source-reviewed seed extract or target template supplied with this reusable package | Unverified. Retain candidates for review, require supported representation evidence before mapping intent, and disclose unresolved membership/serialization checks |

Current target evidence must come from the selected workflow's declared artifact acquisition. A populated export can corroborate a represented value; it cannot prove the complete allowed domain or an omitted-value default. Record the exact evidence reference and checked mapping, without copying customer values into this package. If serialization is proven but complete membership authority remains unavailable, retain REFERENCE_UNRESOLVED, Warning, blocking=false and continue supported checks. If representation cannot be constructed, request the missing value or representation rather than inventing a code. This authoring source review adds no runtime acquisition route. Use only the selected workflow's declared clients and artifacts.
