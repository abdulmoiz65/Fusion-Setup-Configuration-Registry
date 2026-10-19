# Root create: source evidence versus target acceptance

Reviewed source snapshot 2026-09-18. These are product implementation facts,
not proof of the configured environment's exact build or the account's grants.
Backend paths are relative to fusionapps/hcm/components/hcmLearn/common/model/src/
oracle/apps/hcm/learn/common/model/ unless stated otherwise.

| Input or effect | Source-backed behavior | Source |
|---|---|---|
| name | Nonempty; maps to title | catalogadminprofiles/view/LearningCatalogAdminProfilesVOImpl.java:124 |
| number omitted | Maps optional profile number to organization number; entity generates OLC plus WLF_LEARNING_ITEM_NUMBER_SQ sequence | same VO:134; items/entity/LearningItemDEOImpl.java:697; util/ILAConstants.java:1023 |
| status omitted | ORA_ACTIVE | learningorganizations/persistence/DefaultLearningOrgHelper.java:83 |
| visibility | ORA_EVERYONE; defaulted when omitted | CAP VO:138; util/ILAConstants.java:2103 |
| system default | N; REST read-only | learningorganizations/entity/LearningOrganizationEO.xml:292 |
| reconcile priority | ORA_P2; no inferred start date | DefaultLearningOrgHelper.java:98 |
| processing | ORA_NEEDS_PROCESSING; post-create attempts ESS; caught job error is not completion | learningorganizations/persistence/DefaultLearningOrgPersistenceHelper.java:273; CAP VO:147 |
| defaults | Profile defaults, six content-default rows and disabled completion-certificate row are seeded without optional input | catalogadminprofiles/persistence/CatalogAdminProfilesPersistenceHelper.java:63; CatalogAdminProfilesHelper.java:271 |

The six content types are SCORM1.2, web link, video, PDF, assessment and observation
checklist. Certificate default is ORA_ELEARNING/ORA_COMPLETION_CERTIFICATE with
certificateEnabled=N. Omitting content/certificate configuration does not prevent
these server-seeded rows. Include them in expected effects; do not write them.

Redwood learning-administration-ui extension1/sources/ui/self/applications/
learning-setup/flows/main/pages/catalog-administration-profile-details-page.js:6
adds contributorCriteria only for a nonempty contributor array. Backend creation
does not require person rows; its default-manager call is commented out
(DefaultLearningOrgPersistenceHelper.java:57). Creating a contributor relation
is not creating a person membership. Everyone is catalog-manager visibility,
not an ordinary noncontributor management grant or learner enrollment access.
Central all-items/REST overrides remain separate from functional permissions and
membership. Do not infer creator-only access. CAP VO:304 and :345 enforce ordinary
manage privilege plus active contributor membership, with separate overrides.

CAP functional privilege: WLF_MANAGE_CATALOG_ADMINISTRATION_PROFILE_PRIV.
fusionapps/hcm/components/hcmLearn/src/META-INF/jazn-data.xml:20150 maps it to
ManageCatalogAdministrationProfileByAdmin/invoke, learningCatalogProfiles create
and other resource actions, and ReconcileCatalogProfilesJob execute/read.
This mapping does not establish the current account's grant. UCM upload into
hcm$/dataloader$/import$ and loader initiation are separate. The shared
role-access-check manifest supplies no executable effective-grant verifier.
Do not invent one, demand a separate administrator certificate, or use a write
as a permission probe. Review available account/operation evidence and known
denials, then use the unchanged shared loader's authenticated read-only preflight.

### Privilege assessment, not grant certification

The shared loader requires authenticated target/metadata access, source/schema
validation and exact approval; it has no effective-role certificate input.
Certifying Agencies and Units of Measure route to this same service without a
separate pillar grant-proof gate. Its actual upload/initiation requests enforce
Fusion authorization. This is a genuine approved load, never a permission probe.

Keep checks.privileges with source and the existing target-bound evidenceRef.
Use status=verified only for actual supported grant evidence. Alternatively use
status=assessed, enforcement=core.data-loader, grantsVerified=false and
knownDenial=false after reviewing available evidence. This explicitly retains
unproven write access. Missing assessment, a known denial, fabricated evidence,
or any shared preflight failure blocks; no readiness override is used.
Only after successful shared preflight may preparation issue an unapproved
preview, with the authorization uncertainty retained as a warning. Never infer
write grants from that preview or a successful GET. Review every required
operation: CAP create, template/metadata read, UCM upload, loader initiation and
status/readback access. State which evidence exists and which is server-enforced.

The exact-load approval still applies. Shared UCM403 handling stops before
initiation without refreshing/retrying the denied upload. Other failures follow
the shared policy; the pillar never retries an uncertain or failed attempt.
References: core/data-loader/SKILL.md (Execute a data-loading request; Present
every result clearly), upload_and_initiate.py (upload_and_initiate,
post_ucm_multipart), and the two reference skills' REST Data Loader workflows.

Source VO IsNotNull markers coexist with explicit number/status defaulting.
The shared loader validates supplied headers against current template/attributes;
it does not universally reject omission of every metadata-mandatory field.
That validates schema shape, not target-side default execution.

Effective-date omission is supported by the inherited framework, rather than a
CAP-specific setter. Under hcm/components/hcmCoreSetup/common/core/publicModel/src/
oracle/apps/hcm/common/core/, HcmEntityImpl.java:397–479 computes validation dates
and populates absent start/end values for normal date-effective new rows.
HcmDeHelper.java:1575–1589 uses the effective-date context and minimum applicable
parent/current/maximum end. HcmConstants.java:88 sets the maximum to 4712-12-31;
that is not proof of every row's physical end date. LearningOrgLearningItemDEO
inherits LearningItemDEO and EffectiveDated metadata; PerEntityImpl and
HcmSecurityEntityImpl delegate to this framework. Omit date columns/helpers for
root POST; do not fabricate Effective-Of headers. A target create that omits
dates corroborates omission support; its canonical key date does not establish
the physical row bounds. Exact unexposed bounds are a readback limitation, not
an additional mandatory user input or a reason to invent dates.

Evaluate user-supplied execution evidence narrowly: an explicit ORA_ACTIVE input
does not test status omission, a null processingStatus is unverified, no child
input does not prove empty effective membership, and business REST creation
does not prove UCM or Data Loader permissions. Omitted status remains supported
by DefaultLearningOrgHelper.java:83; verify the actual default after creation.
No required field is invented, no readiness rule waived, and no live load is
approved solely because source/default metadata or an offline fixture passes.
