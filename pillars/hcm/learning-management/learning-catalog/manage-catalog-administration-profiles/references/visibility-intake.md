# Visibility for create and update

| Requester's choice | Exact value | Meaning |
|---|---|---|
| Everyone / all catalog administrators | ORA_EVERYONE | Other catalog administrators can view the profile's content, subject to privileges. Viewing does not grant management access. |
| Contributors only / only contributors | ORA_CONTRIBUTORS | Contributor-restricted viewing; functional privileges and central override access still apply. |

Source checked 2026-09-21: `jkaribee_v2/fusionapps/hcm/components/hcmLearn/common/model/src/oracle/apps/hcm/learn/common/model/`:
`catalogadminprofiles/view/LearningCatalogAdminProfilesVO.xml:115-127,369-380,1329`
binds visibility to lookup `ORA_WLF_CAP_ADMIN_VISIBILITY`;
`util/ILAConstants.java:1696,2103,2152` identifies the two codes and lookup.
Redwood `learning-administration-ui/extension1/sources/ui/self/applications/learning-setup/flows/main/pages/manage-catalog-administration-profiles-page.json:365`
uses the same lookup. `catalog-administration-profile-details-page.js:6-37,43-61`
passes basic fields in create and sparse batch update respectively.
These sources identify the contract, not the current target's enabled lookup values.
Use current target metadata/evidence before execution; never manufacture an enum.
The Oracle-authored functional reference distinguishes viewing from contributor
management and central override access; learner enrollment is a separate concept.

## Intake and review

Use `cap_proposal.py draft/revise` for both creation and update proposals. Its
visibility input accepts the labels above, canonical codes (case-insensitive),
and `all catalog admins`, `all catalog managers`, or `contributors`.
`cap_visibility.normalize` matches complete choices, not substrings of arbitrary
prose. The agent may interpret a clear sentence, but must preserve its source and
show the interpretation. “Private”, “public”, “HR only”, “all employees”, conflicting
choices, or learner access requests require clarification; do not map ORA_OPEN or
ORA_PRIVATE from other object types. Ask: “Who should be able to view this catalog's
content: all catalog administrators, or contributors only?” Do not guess a choice.

Missing create visibility stays unknown in the proposal and blocks preparation
until selected. Missing update visibility means unchanged and is not added to the
payload. An explicit choice equal to the current value is a no-op, not a write.
Do not infer visibility from the contributor count or vice versa. With no
contributors, show that no ordinary contributor membership is being added;
do not promise creator-only access or bypasses of central override privileges.

Present original wording, label, canonical code, access explanation, contributor
count state, and (for updates) current versus proposed visibility. Proposal edits
invalidate earlier approval. For creates, prepare canonical codes in the DAT
before shared validation and immutable ZIP approval; never normalize frozen bytes.
For shared REST updates, `cap_batch_update.py` accepts the same choices and retains
the input plus `visibilityReview` in the exact-hashed preview. Only canonical codes
enter the sparse payload. Current writable metadata/verified enum, non-default
protection, privilege assessment, exact approval and independent readback remain
mandatory. Readback checks the exact code; it does not prove every user's access.
Status, contributors and other unrequested fields remain unchanged.

When root metadata has no inline enum, the batch observation resolves its
`LearnCatalogProfilesVisibilityLOVVA` association using the unchanged shared GET
client: `/fscmRestApi/resources/11.13.18.05/commonLookupsLOV`, finder
`LookupTypeFinder;LookupType=ORA_WLF_CAP_ADMIN_VISIBILITY`. This is the Redwood
service catalog's fscmRest route. Require one complete page (limit 100), unique
supported codes and no explicitly disabled entries. Partial, unexpected or
unavailable results block preparation. Retain lookup path, finder, codes and
observation time in hashed field metadata; this read is not privilege proof.
