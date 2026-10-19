# Shared REST basic-attribute batch update

Explicit item-update route, not an import or fallback for failed loader
validation. Creation/import and loader-update retain their own contracts.
Name, description and visibility can be replaced individually or together.
Status is a separate lifecycle operation and remains unavailable pending current
eligibility/hint/provider contracts. No child or deletion writes are enabled.

Use `scripts/cap_batch_update.py`, Python3.11+. Shared OAuth and
`core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` own HTTP.
No pillar transport, browser calls or core modifications.

## Evidence and readiness

Performance Library Goals declares shared-client ADF batch scalar updates.
CAP Redwood constructProfilesBatchPayload and supplied UI evidence establish
one part: `/learningCatalogProfiles/<ISO-date>,<number>`, operation update,
effectiveOf RangeMode=UPDATE and description payload. Use the standard versioned
HCM root `/hcmRestApi/resources/11.13.18.05/` with framework9, matching the
shared CAP resource version and standard ADF batch-root protocol. No browser
UUIDs/cookies or captured identities/dates. Source/UI evidence is not completed
shared-client CAP acceptance. Determine live acceptance from the selected project's
submission receipts and independent readback, scoped to target, operation and run;
do not declare it globally pending or complete from this reusable reference.

Current root metadata must advertise PATCH and each requested field as string/updatable/
allowChanges/maxLength. Resolve exactly one current number, fresh key/self identity
and matching canonical GET. Bound reads120seconds. No number-only probe, loader
registration, template, DAT, ZIP or UCM prerequisite on this route.

Require an attributed current update-privilege assessment; GET/create success is
not update grants. Assessed shared enforcement may retain unverified grants with
a warning; known denial blocks. No new certificate or permission-probe write.
Preserve an active initial Run Book when required by project policy, but do not
update its Data Loader task or claim its completion for this REST operation.

## Commands and input

Request JSON: mode exact, number, optional expected_name/expected_id, environment,
host, confirmed_host, allowed read headers, changes with only a nonempty
replacement for name, description and/or visibility. Caller URLs, parts and
operation overrides are refused. Empty/clearing/null edits are not supported.

- `inspect --request-stdin --execute-read`: bounded read-only observation.
- `prepare --request-stdin --execute-read --project-root <project> --output-dir <new-directory> --privilege-assessment <project-file>`: observe and retain unapproved preview/payload.
- `submit --preview <preview.json> --project-root <project> --approved-preview-sha256 <reviewed-digest> --approve`: only after later exact-payload consent.
- `verify --preview <preview.json> --project-root <project> --execute-read`: independent readback, never a write.

The privilege assessment has environment {name,host}, operation
update_description for description-only input, otherwise update_basics;
enforcement core.fusion-api.rest-api-client, status
assessed/verified, knownDenial false, boolean grantsVerified and an attributable
source explanation. Never fabricate grants or promote read readiness to writes.
The assessment is an attributed judgment, not a server-issued privilege proof or
an authenticated-user binding. Reassess after account changes; the shared client's
current authenticated user and Fusion authorization determine actual access.
Preparation expiry bounds profile evidence, not the age of privilege evidence.

CAP-BATCH nodes are distinct from read and loader gates. No-op creates no payload.
Preparation freezes environment, profile/date, baseline, changes, headers,
implementation/project hashes and semantic JSON payload hash. One details part
only: update, fresh canonical key, effectiveOf and actually changed basic attributes. No status,
provider list, other identity/body fields, null clearing or children. Show old/new
values for every changed field, target, payload/hash and fixed-date/concurrency/privilege limits.
Obtain exact approval immediately before POST. Preview expires30minutes;
reprepare rather than modifying approved dates, metadata or bytes.

## Execution and result discipline

Submission checks approval/expiry/frozen integrity/configuration without rebuilding
or live revalidation. Implementation/project changes invalidate the preview.
A durable exclusive target/payload marker prevents automatic replay through a
copied preview. Shared auth-rejection refresh is unchanged; no pillar retry on
timeout or uncertain result. Standard configured-host redirects remain enforced,
not a reject-all-redirects guarantee.

Verify part count/id/path/operation/errors and every changed attribute, not merely
HTTP200. Never emit raw responses/auth errors. Response confirmation still needs
independent readback against requested and captured unchanged settings. Missing
coverage remains unknown. ORA_NEEDS_PROCESSING is pending; no loader job exists.
Receipt failure after a confirmed response is not a no-effects claim. Reconcile
uncertain writes using supported reads, never automatic replay or cleanup.
Readback alone proves observed state, not that this route caused it; retain and
inspect the submission receipt before attributing execution to this workflow.

## Rename and visibility rules

An actual rename requires current name queryability and a complete bounded
exact-name shared GET search. Exclude only the same stable profile number;
another accessible matching number blocks. Incomplete results never clear
duplicates. Preserve case/whitespace; do not silently normalize a proposed name.
This is account-visible, not a tenant-global uniqueness guarantee. Fusion may
still reject a conflict. Recheck for each preparation; approval expires30minutes.

Visibility intake accepts [plain-language choices](visibility-intake.md), preserving
them in the reviewed request and mapping before payload construction. The payload
accepts only ORA_EVERYONE or ORA_CONTRIBUTORS when included in the
current field metadata's verified enum. Missing target enum blocks visibility
preparation; do not infer values from labels or inject source constants as live
metadata. An actual visibility change requires isSystemDefault=N. Everyone is
catalog-manager visibility, not learner enrollment or contributor-management access.

Unchanged supplied fields are validated but omitted from the transmitted part.
After rename, verify the stable number and expected new name, not the old name.
Route cap-shared-rest-basic-batch-v2 is isolated from old approvals. Historical
description-v1 previews remain readable for verification but cannot submit.
Multi-profile execution remains separate one-profile previews/approvals; this
extension does not add an automatic batch executor or atomic multi-profile write.

## Status readiness gap

Reviewed Redwood catalog-administration-profile-details-page.js
constructStatusPayload: one update part, composite key, RangeMode=UPDATE, status
alone. profilesSecondaryActionChain handles ORA_ACTIVE and ORA_INACTIVE separately.
checkIfUserCanDeactivateCAP requires CAN_DEACTIVATE in the first returned
userActionHints.canManageLearningItem list. initCatalogAdministrationProfileChain
warns that provider-used profiles cannot be deactivated/deleted. These are source
facts, not proof of current target eligibility or a generic status-edit contract.

Before enabling status, add and verify a declared read contract for action hints
(schema, exact parent, complete row handling, permissions and missing/denied data),
target transition/default/provider restrictions and status requiredness/writability.
Then implement separate lifecycle evidence/approval/readback tests. Never accept
ORA_DELETED as activation/deactivation or mix a lifecycle transition silently into
a basic-field update. Current status requests stop before HTTP with this gap.
