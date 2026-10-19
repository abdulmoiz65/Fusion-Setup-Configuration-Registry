# Pending CAP operation contracts — source audit

Source audit 2026-09-18; bounded gap review refreshed 2026-09-20. FSCR baseline:
`874de5c7edeb7ada57d2980da6121535cab475ae`.
No Fusion request, job, registration edit or write was made for this audit.
ADE and Redwood source prove implementation intent, not that DL_ENV deploys the
same build. Historical target results remain explicitly historical. Unavailable
contracts must not be replaced with a direct REST write or a private client.

## Capability ledger

The dated source audit below is historical. Current basic-update execution is
defined by [update-contract.md](update-contract.md) and the separately selected
[batch-update-contract.md](batch-update-contract.md). Project receipts and readback,
not this historical audit, establish live acceptance for a particular run.

| Capability | Established evidence | Remaining executable prerequisite / disposition |
|---|---|---|
| Root create | Existing exact-approved shared-loader canary loaded one row and read back its generated number; name/description/Everyone matched, Active/nondefault defaulted. | Preserve the proven route. New rows require new target-bound validation, duplicate baseline, exact immutable approval and per-row readback. Processing was pending, not complete. |
| Multiple root creates | cap_create_batch implements1..20 independent root handoffs, prevalidates all exact artifacts before the first submission and stops on uncertainty. | Fresh target-bound preparation, aggregate/member exact approval and live batch acceptance remain. Separate datasets, not atomic multi-row or mixed-write execution; XLSX is not required. |
| Basic update | Redwood uses date-plus-number item key and RangeMode=UPDATE; backend loader preserves PATCH. Current pillar routes support sparse name/description/visibility updates. | Loader requires verified deployed key/template mapping. Separately selected shared REST basic updates use current metadata, canonical identity, privilege assessment and exact payload approval; no loader fallback or implied lifecycle support. Live acceptance is project/run-specific. |
| Activation/deactivation | Redwood uses separate status actions and eligibility hints. | Unavailable until current transition, default/provider/usage eligibility, grants and a lifecycle execution/readback contract are implemented and verified. Basic-update evidence cannot satisfy this gap. |
| Contributor criteria add/edit/remove | Product has criteria children and UI create/update/delete semantics. Later saved target template has contributorCriteria, unlike the earlier APEX excluded hierarchy. | Verify current child registration, parent/criterion keys, people resolution, supported input modes, source type, writable fields and reconciliation. Template inclusion alone does not establish a usable child write. |
| Contributor person-list input | UI creates attachment metadata for person-number/email-list uploads; effective person list is read-only. | A raw CSV parser is not the product attachment uploader. Async tracker/attachment route and corresponding loader mapping are unverified. Do not create membership by writing a read-only derived list. |
| Content defaults | Product seeds six content-type rows; normal child POST is rejected; existing row update delegates typed validation. | Need current child metadata/registration and row identity, exact field/type and null/reset/inheritance contract, then supported PATCH and readback. Never submit `defaultedRow=Y` to bypass the ordinary POST prohibition. |
| Certificates | Product seeds one disabled row. Y requires a filename; N/null requires a null filename. | Need current template/child mapping and row key, permitted certificate-template lookup, supported clearing representation, inheritance and rendering verification. Source filename validation is not proof a template exists. |
| Deletion | Product UI implements logical deletion by PATCH `status=ORA_DELETED`, adding destinationProfileId for in-use content; system default cannot be deleted. | Requires update contract plus usage/provider/destination eligibility and migration readback. Do not translate declared MERGE_DELETE into physical CAP DELETE. |
| Reconciliation execution | Product action commits reconciliation-ready flag and submits ESS; ordinary loader batch operations are POST/PATCH/DELETE. | No supported Data Loader action mapping for CAP reconcile established. `RestAction=RECONCILE` is explicitly unsupported in inspected backend. Keep action unavailable; a separately approved supported shared action route would be a new declared route, not a fallback. |
| Processing observation | Root processingStatus comes from processing-details row for ReconcileCatalogProfilesJob; source sets ORA_NEEDS_PROCESSING. | Read-only observation can be expanded through declared shared GET. Unknown/null statuses remain unverified. Root state alone does not prove a correlated job or effective contributor membership completed. |

## Shared-loader boundary: exact source findings

Repository source references below are relative to the FSCR repository root:

- `core/data-loader/scripts/upload_and_initiate.py:1568–1617` validates a
  supplied DAT's sections without converting its action values. `:683` owns
  immutable ZIP preparation; `:2372` is the approved-preflight uploader.
  `core/data-loader/SKILL.md:164–170` requires source/schema and Task Hook
  validation, immutable preparation and later exact-artifact approval. Its
  multi-DAT support is not permission to skip per-profile CAP validation.
- `core/data-loader/scripts/generate_sample_dat.py:267–298` chooses PATCH for
  enriched update *samples*, otherwise POST. This sample fallback is **not**
  an update limitation on the prepared-DAT route. Do not silently convert an
  unresolved intended update into create.
- `core/data-loader/scripts/get_data_load_info.py:24–26,573` owns data-set
  status/errors/failed-lines/all-object errors. A submitted request is not load
  completion; load completion is not CAP processing completion.

Fusion backend source base (`DL`):
`<fusion-source-root>/hcm/components/hcmCoreSetup/common/dataLoader/model/src/oracle/apps/hcm/common/dataLoader/`

`DL/core/model/applicationModule/DataLoaderAMImpl.java`:

- `:9367–9392`: an explicit PATCH is preserved; an absent surrogate must resolve
  through configured user keys or fails. `:9587–9595` makes the resolved
  surrogate the LOCAL key.
- `:8706–8738`: absent configured URL override, item operations append the LOCAL
  key to the top-resource path. `:10664–10704` and `:10722–10740` recursively use
  parent item keys for child operations. A parent CAP key problem therefore also
  affects operations on existing CAP children.
- `:10596–10608`: effectiveOf is forwarded only for an EFFECTIVE_DATED object and
  a nonblank stage value. This header handling does not construct the composite
  item identifier.
- `:11806–11865`: PostUrl/PatchUrl templates can override paths with registered
  stage-value placeholders. A null PatchUrl supplies no override. No custom URL
  is proposed here: required placeholders, registration/template exposure and
  deployment must first be verified by the service owner.
- `:8859–8879`: ordinary batch action mapping accepts POST, PATCH and DELETE,
  otherwise throws Unsupported RestAction. This does not support inventing an
  arbitrary action name for reconcile.
- No `If-Match` or `ETag` reference was found in this bounded class inspection.
  Conditional-write support is **unverified**, not a claim that no Oracle API
  supports concurrency. Approval-bound bytes protect the requested change, not
  against another actor changing the same profile before execution.

No mandatory FSCR-core patch has been established for prepared multi-create.
Existing-profile updates may need deployed product key behavior or registration
correction, **not necessarily a Python shared-core change**. Product service
owners must resolve the missing target contract. Do not reintroduce the
unconditional shared-loader transport blocker or claim project risk acceptance fixed TLS,
redirect or target-host behavior.

## Product and UI source evidence

Product source base (`CAP`):
`<fusion-source-root>/hcm/components/hcmLearn/common/model/src/oracle/apps/hcm/learn/common/model/`

UI source base (`UI`):
`<learning-administration-ui-root>/extension1/sources/ui/self/applications/learning-setup/flows/main/pages/`

- `UI/catalog-administration-profile-details-page.js:6–32`: contributorCriteria
  omitted for an empty contributor array. Individual entries use sourceType and
  sourceId. ORA_PERSON_LIST / ORA_PERSON_EMAIL_LIST require personListAttachment
  entries containing AsyncTrackerId, FileName and DatatypeCode FILE.
- Same file `:42–73,107–181`: root and contributor parts have separate identities
  and update/create/delete semantics. Removing a proposal row is not this
  product deletion operation.
- `UI/catalog-administration-profile-details-page-chains/profilesSecondaryActionChain.js:25–42,62–102`
  and `deleteProfileChain.js:33–45`: source uses UTC-date plus number, effective
  range update, Active/Inactive transitions and logical deletion. Destination
  migration is a separate effect, not ordinary removal.
- `CAP/catalogadminprofiles/persistence/CatalogAdminProfilesHelper.java:187–240`:
  rejects deletion of system default; destination required when related
  e-learning exists; supplied destination must exist. Do not infer that these
  checks exhaust all provider/access/eligibility rules.
- Same helper `:246–260`: create cannot start deleted, and configured default-rule
  attributes are prohibited during initial root POST. `:271–302` seeds SCORM1.2,
  web-link, video, PDF, assessment and observation-checklist defaults and disabled
  ORA_ELEARNING / ORA_COMPLETION_CERTIFICATE row.
- `CAP/catalogadminprofiles/view/LearningContentDefaultRulesVOImpl.java:41–59`:
  ordinary POST rejected unless internal creation context defaultedRow=Y.
  `CatalogAdminProfilesHelper.java:499` delegates typed content-default rules.
- `CAP/catalogadminprofiles/persistence/CatalogAdminProfilesHelper.java:418–422`
  calls `CAP/items/digitallearning/util/DigitalLearningValidationUtil.java:925–942`:
  certificateEnabled allows Y/N; enabled requires filename, disabled/null forbids
  a nonnull filename. This is not a certificate upload or rendering contract.
- `CAP/learningorganizations/view/LearnOrgLearningItemVORowImpl.java:1799–1810`
  commits the flag before invoking ESS. CAP override
  `catalogadminprofiles/view/LearningCatalogAdminProfilesVORowImpl.java:1477–1516`
  sets ORA_NEEDS_PROCESSING and submits reconciliation. A call can therefore be
  uncertain/partially effective; never automatically retry a failed action.
- `CAP/catalogadminprofiles/view/LearningCatalogAdminProfilesVO.xml:60` selects
  processingStatus from ReconcileCatalogProfilesJob processing details. This
  audit did not establish an authoritative complete terminal-state enumeration.

REST resource definition:
`<fusion-source-root>/hcm/components/hcmLearn/common/restModel/hcmLearnRestModel/adfmsrc/oracle/apps/hcm/learn/common/restModel/learner/applicationModule/rest/r13/LearnerRestAM_LearningCatalogAdminProfilesVOResources.xml:13–103`
declares root children, number RowFinder key, read-only effective person-list,
messages/hints/metrics, and disabled DELETE for defaults/certificates. Its number
RowFinder declaration can represent later source behavior; it does not invalidate
the observed historical DL_ENV date-plus-number key. Resolve source/deployment
differences before allowing PATCH. Child visibility is not loader registration.

## Saved target evidence and unresolved deployment facts

- Project `current/CAP-CREATE-READBACK-20260918.md` records the canary request, one
  loaded/zero failed, exact-name/number readback and pending processing.
  It did not inspect contributors, content-default or certificate rows.
- `current/CAP-CREATE-EXECUTION-READINESS-20260918.md:83` cites earlier ART-107
  template retrieval (root39 / contributorCriteria26 attributes). This supersedes
  an assumption that all historical APEX exclusions are still deployed, but does
  not prove attachments, effective membership or child writes.
- Historical wiki/APEX evidence: number-only PATCH failed, canonical date-plus-
  number GET worked; EffectiveDated=Y and PatchUrl=null. No successful corrected
  CAP update was established by that historical wiki/APEX evidence. Treat source fixes, target metadata and actual
  operation acceptance as distinct evidence layers.
- FDD examples remain illustrative. The inaccessible requirements attachment is
  still a bounded completeness gap; it neither supplies missing runtime contracts
  nor invalidates independently verified root-only creation.

Final enabling rule: preserve all capabilities in the ledger, but graduate an
operation only after its declared shared route, exact target fields/keys,
privilege assessment, executable validation, immutable approval and observable
success criteria are established. Local test fixtures cannot certify deployment.

## Gap-review disposition

The prepared-DAT route preserves PATCH. Available template evidence includes
EffectiveStartDate, EffectiveEndDate and effectiveOf, not SysEffectiveDate.
These helper columns do not establish item-URL construction. Ask the Learning/
Data Loader service owner for the supported current CAP update DAT, exact key
and date/header mappings, deployed URL-resolution evidence and concurrency
semantics. No central FSCR Python patch or guessed PatchUrl is prescribed.

The criterion-count read contract now uses criteriaId, backed by
UI/catalog-administration-profile-details-page.js constructDeletePayload and
constructUpdatePayload (returned row.criteriaId in item URLs) plus typed current
schema. This closes criterion-row identity only. The separate effective
contributorPersonList ServiceDataProvider in learning-catalog-item-details-page
declares no keyAttributes. The personID key in criteria/personList belongs to a
different child and cannot establish contributorPersonList uniqueness. Fresh
ADE contributor VO access was denied during this review; no new Java identity
evidence is claimed. Request its documented unique key and compatible schema
from the Learning REST owner before enabling effective person counts.

For defaults/certificates the saved current root describe and loader template do
not expose the setting rows; request their supported resources, mappings and
semantics from Learning/registration owners. For reconcile, request a declared
shared action workflow and correlation contract. A generic POST-capable client
does not supply those missing contracts. These operations remain unavailable;
unknown evidence is not proof that the product cannot support them.
