# Sparse basic CAP updates through Data Loader

This contract governs the loader route. For an explicitly selected basic-attribute
item update, use [shared REST batch update](batch-update-contract.md) instead.
That route has separate evidence and approval; it never bypasses or satisfies
this route's loader gates. Do not switch routes after an uncertain submission.

Scope: one existing profile, explicit nonempty replacement of description, name
and/or visibility. No identity, status, child, content-default, certificate or
reconciliation edits. No direct REST write; unchanged core owns authentication,
template validation, ZIP packaging, Task Hook, approval, UCM and submission.
Description is the first live acceptance case. Name/visibility use the same
validated path; a multi-update executor waits for successful single-update
acceptance as sequenced in the approved implementation plan.

## Field and source interpretation

| Field | Supported basic-update interpretation |
|---|---|
| description | Explicit nonempty string, source maximum 4000 and tighter verified target maximum |
| name | Explicit nonempty string, source maximum 250; complete exact-name duplicate scan, excluding the same stable number |
| visibility | Verified lookup ORA_EVERYONE or ORA_CONTRIBUTORS, source maximum 30; verified non-system-default profile for an actual change |
| learningCatalogProfileNumber | Immutable lookup/staging identity, never a requested edit |
| status/destinationProfileId | Separate lifecycle operations, unavailable |
| processing/audit/system flags | Observations, not update inputs |
| priority/start/end and child/default/certificate fields | Not established basic-update contracts; unavailable here |

Live `updatable=true` alone is insufficient: require string type, `allowChanges=always`
and a verified maximum for each changed field. The number may advertise
updatable while retaining inCreate semantics. An old APEX all-Updatable=No
display is not more authoritative than typed current product metadata.
Omission means unchanged; null, blank, whitespace-only and DAT null markers are
not implemented clearing contracts. Reject pipes, control characters and
overlength values instead of rewriting user text. Preserve supplied Unicode.
Seeded default visibility is protected. Everyone permits catalog-manager
visibility, not contributor management access or learner enrollment.

Saved jkaribee_v2 evidence already contains a number-finder override removing
SysEffectiveDateBindVar; a wiki statement that it is absent conflicts with that
saved source. Do not prescribe adding it again or assume deployment parity.
Date-plus-number canonical URLs, EffectiveDated=Y and Effective-Of handling are
separate facts. A number-only GET is a useful check, never proof of loader PATCH
mapping. Never embed a date in the profile-number input as a workaround.

## Read-only evidence and preparation

1. Resolve one complete accessible baseline using the supported read route.
   `cap_workflow.py inspect-update-contract --request-stdin` performs local
   readiness only; authorized `--execute-read` selects root describe, complete
   number equality lookup and bounded canonical/number-only item GET comparison.
   Use exact-number request shape and confirmed configured host/environment.
   This route does not grant write readiness. Known/unknown access remains explicit.
2. Establish current registration, downloaded live UCM template, mapped root
   attributes, explicit RestAction PATCH, omitted-field preservation and immutable
   number handling from attributable deployment/source evidence. Use the supported
   shared `load_business_object_schema` and read-only preflight, never an alternate
   downloader or private client. Require one verified registered mapping:
   `number_only`, or `registered_composite` with its exact relative PatchUrl,
   template-declared staging date field, type/format and payload exclusion,
   fixed ISO date, and canonical date-plus-number identity. Keep the actual
   profile number unchanged. A canonical GET alone is not loader-mapping proof.
   Missing PostUrl/PatchUrl in a resolver that does not expose those fields is
   unknown, not proof of an empty override. Use current registration-export or
   attributable deployment evidence; request external correction only when needed.
3. Retain core baseline number/name/description/status/visibility/system-default,
   plus other observable settings when available. Record unknowns, actual observed
   effective date and language. A rename needs complete accessible duplicates;
   absence is not tenant-global uniqueness. Privileges must assess update, not
   copy create or GET access. Shared enforcement assessment with no known denial
   is permitted; no separate administrator certificate or permission-probe write.
4. Use `cap_update_validation.validate_changes` to derive the exact sparse diff.
   No change returns no_op: no archive, approval or network request is needed.
   The evidence format is [cap-update-evidence.schema.json](../schemas/cap-update-evidence.schema.json).
   Every check has an attributed target-bound file reference/hash. A status flag
   or synthetic fixture is not proof. At preparation, validate freshness and the
   actual source fingerprint; do not synthesize facts to pass.
   Inspection retains raw `field_metadata` and supplies `typed_field_metadata`:
   only unambiguous positive decimal maxLength text becomes an integer;
   writable permissions are never coerced. Invalid lengths remain unavailable.
5. For a real change, prepare one explicit DAT under the project:
   `MERGE` root row with `RestAction=PATCH`, immutable number and only changed
   fields. `effectiveOf=RangeMode=UPDATE` is optional only when its exact helper
   mapping is verified; do not infer it from EffectiveDated alone. Headers must
   match the real template. A verified registered_composite row also includes
   exactly its approved staging date, excluded from the business payload.
   `dateValue` and the canonical URL date stay ISO `yyyy-MM-dd`.
   `dateFieldFormat` describes DAT bytes: verified String helpers require
   `yyyy-MM-dd`; verified Date helpers require `yyyy/MM/dd`. Date values are
   derived deterministically from the same ISO key date. Verify the registered
   SQL DATE formatter converts the staged value back to ISO for the URL;
   a public DataType label alone does not establish deployed conversion.
   Changing helper type/format requires new evidence and preparation, never
   conversion or metadata refresh after approval. Legacy Date+ISO evidence is
   refused; number-only and verified String behavior are unchanged.
   No guessed executable examples are supplied here.
6. Run from this pillar:

   From the repository root: `python3.11 pillars/hcm/learning-management/learning-catalog/manage-catalog-administration-profiles/scripts/cap_update_handoff.py --source <learningCatalogProfiles.dat> --evidence <verified-update-evidence.json> --task-context <selected-task-context.json> --project-root <project> --output-dir <new-project-directory>`

   The helper checks all local evidence/bytes first, performs unchanged shared
   read-only preflight, validates the actual immutable ZIP, evaluates the dedicated
   CAP-UPDATE graph, then builds the unapproved shared Task Hook preview.
   Create/read rule results cannot substitute. Missing evidence means no preview,
   not an approval question. Existing source/approval artifacts are never replaced.

## Exact approval and submission

Disclose old/new values, immutable identity, target, operation, unchanged settings,
mapping-specific date policy, access limits and processing expectations through the
shared approval workflow. Sparse PATCH is last-writer-wins: unrelated fields are
omitted, but a concurrent edit to the same field can be overwritten. No ETag or
transactional as-of guarantee is claimed. Number-only retains server_current;
registered_composite binds a fixed_key_date, not a date recomputed at submission.
This URL key date is separate from effectiveOf processing directives. Revisions
require a fresh preparation. Registration updates are not authorized by a local
mapping implementation or by approval of a profile-data load.

After actual approval of this exact retained load only:

From the repository root: `python3.11 pillars/hcm/learning-management/learning-catalog/manage-catalog-administration-profiles/scripts/cap_update_submission.py --preview <retained-cap-update-preview.json> --project-root <project> --approved-preview-sha256 <reviewed-preview-digest> --approve-upload`

The update continuation verifies frozen ZIP-to-input/identity consistency and
preview/evidence/context integrity; invokes the unchanged public Task Hook
approval/archive verifier; and calls `upload_approved_preflight`. It never
reopens original DAT/evidence, refreshes metadata or expiry, recompiles rules,
or repeats live checks after later approval. Shared target/Run Book integrity
checks still apply. The exclusive target/ZIP/operation attempt marker prevents
automatic retry on authorization rejection or uncertainty. Preserve receipts and
known external identifiers; do not report no effects after accepted submission.
No separate generic consent gate duplicates the shared approval.

## Verification and regression requirements

On an authorized request to verify results, use shared `get_data_load_info`
for terminal status/counts and all prescribed error resources. Then complete an
exact-number read and `cap_update_validation.verify_readback`: exactly one
matching identity, changed values equal the approved input, other captured fields
unchanged. Missing observed coverage must remain explicit. Loader completion,
field readback and CAP processing completion are distinct. ORA_NEEDS_PROCESSING
is pending; unknown/null state is unverified, not success. Do not trigger reconcile
or cleanup. Never automatically retry an uncertain write.

Offline tests cover field lengths/nulls, no-op, duplicate rename, seed protection,
typed evidence, key mismatch, child/lifecycle refusal, immutable archive approval,
coherent preview tampering, altered target/Run Book, uncertain replay, and the
actual unchanged shared validation boundary. Retain existing read/list/create
regressions. Live update acceptance and clean-model reviews are separately
reported; offline tests cannot certify deployed PATCH routing.
