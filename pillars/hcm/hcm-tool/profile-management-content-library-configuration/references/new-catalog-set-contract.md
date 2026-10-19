# Complete new Item Catalog set

Use through the parent skill and Item Catalogs task for one new catalog and all
supplied portable children. This separate capability is certification-only;
merge-quality implementation does not imply runtime verification or general-use
promotion. Existing catalog-only, anchored-one-child and candidate-only modes
are unchanged. Do not split a complete request or discard unsupported rows.

## Scope and evidence

The registry is item-catalogs/references/catalog-new-set-fsm-provider.json.
It permits controlled certification in an authenticated non-production target,
classified by the owning workflow or the bound user confirmation below,
for one of the existing nine contexts. None is live-certified for this new shape.
Keep the existing exact headers, metadata, grouping keys, parent aliases, supplier
C, explicit applicable dates, blank generated IDs and all code/Name collision
checks. Rating descriptions, dynamic fields, translations and relationships are
not enabled. Quarterly or technical release matching is not a gate.

Use the [optional-export policy](../item-catalogs/references/optional-export-policy.md)
to skip pre-import export without attempting it, reuse validated package templates and
perform post-import REST fallback. Current-state absence and indirect Profile V2 checks
remain explicitly unverified without evidence. Preserve supported Content Type
checks, synthetic/approved-seed-only storage and provider-row approval.
The existing narrow registry supplies portable field constraints,
not new-set certification. Its provider_use must be controlled-certification.

Source: ItemCatalogMigrationService imports the root graph; ContentItemVOImpl
resolveAttributes obtains ContentValueSetId from its parent logical row in phase
two. Do not invent physical IDs or claim transaction-wide atomicity. This source
supports controlled testing, not a claim that a particular target load succeeded.

## Additional package-input contract

Only explicit new-set preview/preparation modes accept an additional top-level
catalog_set_contract in the existing package-input JSON. It has the following
required fields and only the one optional field listed:

| Field | Required value |
|---|---|
| capability_id | item-catalog-new-set-v1 |
| registry_sha256 | SHA-256 of the separate new-set registry |
| use | controlled-certification |
| target_classification | non-production, established by the owning workflow or the scoped user confirmation below |
| target_evidence_reference | Sanitized reference to Core-authenticated target identity evidence, never a user assertion |
| source | input_method (direct, template or existing-file), reference and sha256 |
| mappings | One entry per parent/child row: member, zero-based row_index, source_reference and status confirmed |
| group_counts | All 14 canonical groups; item_catalogs=1, item_catalog_content_items=N; every other group=0 |
| target_classification_confirmation | Optional exact user-confirmation object defined below; omit for workflow-established classification |

Preserve full source-to-field mappings in the original approved proposal linked
by proposal_fingerprint. The additional row ledger proves complete row coverage;
it does not replace field mapping or authorize declaring supplied groups omitted.
Normalize a behavior catalog into item_catalogs for this task-specific package
without losing its original source identity. A supplied competency relationship
keeps the complete request blocked; it must not be omitted to enter this mode.

The local helper compares routed evidence assertions; it cannot authenticate an
environment or establish their authority. The owning workflow must verify Core
target identity, the selected classification source, source provenance and
declared omissions before invoking it.

## Scoped user confirmation of non-production classification

For this certification-only capability, accept the user's explicit confirmation
that the already authenticated target is a test/non-production environment.
Record it as user-confirmed classification, not machine-verified classification.
No separate environment inventory, screenshot or release proof is required.
This policy is an explicitly user-approved local workflow change, not a claim
about Oracle provider behavior or a general environment-authentication exception.

The owning workflow must retain the actual sanitized user statement/decision,
resolve the same target through Core, and bind the following optional object
before the complete-set preview. Do not fabricate a Core receipt or a user's
confirmation. All six fields are required; additional fields are rejected.

| Field | Required value |
|---|---|
| policy_id | new-catalog-set-user-nonproduction-v1 |
| confirmed_non_production | Boolean true, not a string or number |
| target_environment | Exact Core-resolved alias matching the proposal target_environment |
| proposal_fingerprint | Exact reviewed proposal_fingerprint, 64 lowercase hexadecimal characters |
| authenticated_target_evidence_reference | Exact match to target_evidence_reference; the referenced Core evidence must identify that target |
| confirmation_reference | Nonblank sanitized reference to the actual user statement/decision, distinct from the Core evidence reference |

Recheck authenticated target identity at the declared execution gates. A target
change or conflicting authoritative production classification blocks use of this
confirmation. Missing authentication cannot be replaced by user testimony.
Material changes to the bound proposal or confirmation require a fresh complete-set
preview and preparation approval. The confirmation is not standing authority for
another target or request; same-target token renewal alone does not require asking
the user again if the classification and bindings remain valid.

This exception establishes classification only. It does not establish access,
privileges, synthetic/approved-seed-only export contents, permission to retain
customer data, duplicate clearance, provider readiness, or upload/import approval.
The full-export data-handling gate and all Core Task Hook/approval checks remain
unchanged. Never fill missing authenticated evidence from this confirmation.

provider_rows_fingerprint uses the original material plus catalog_set_contract.
For old proposals without that field, the fingerprint algorithm is unchanged.
The full catalog_set_fingerprint hashes the entire package-input JSON, including
the skipped-export/template receipts (or validated supplied-evidence receipts)
and all rows, after normal validation. JSON arrays stay
arrays in the displayed preview. Material changes require a new preview.

## Local preview and package

SKILL is enabled in this independent new-set registry for a new custom catalog
and its portable children only. Read the [Skill creation contract](../item-catalogs/references/skill-catalog-creation.md).
It remains certification-only: the verified narrow existing-parent registry and
historical HDL status are unchanged. Predefined/managed Skill catalog codes are
excluded even when pre-import export is skipped.

Use all normal arguments to scripts/prepare_profile_content_library_fsm_package.py
and add --preview-new-catalog-set. Omit --current-state-zip for the skipped
pre-import export. It validates the full request, skipped-export receipt and
reviewed baseline, displays every provider row plus provenance and 14-group counts, and
writes no ZIP or readiness file. Safe unused output paths are still required.

After review, the exact statement PREPARE CATALOG SET <catalog_set_fingerprint>
authorizes local preparation only. Run the same inputs with
--prepare-new-catalog-set --new-catalog-set-approval followed by that statement
as one quoted argument. Do not combine either mode with --validate-new-catalog-set.
The latter retains its non-executable candidate report and accepts its original
input contract only.

The builder writes one deterministic ZIP and a sanitized readiness receipt,
reopens the ZIP, checks every row and preserves metadata/header/member shape.
The receipt and Core Task Hook finalData bind the new capability, registry and
complete-set fingerprint as well as the original archive/task/row fingerprints.
Package readiness means eligible for a separate Core preview, not authorization
to upload or a successful import. Reopen and compare the exact archive and the
bound proposal at Task Hook; a receipt alone is not payload validation.

## Submission and complete readback

Use the unchanged Core Data Loader Task Hook, exact task context, immutable
preview and its own approval/qualifying same-request auto-approval contract.
Do not introduce another transport, waive task validation or reuse a standing
session approval. The existing one-child composite batch runner/receipt is not
a new-set execution route; use the ordinary declared loader/status workflow.

After accepted initiation, retain IDs and obtain terminal state and ProcessLog
through the declared status workflow. On failure, partial success or timeout,
retain the result and stop; do not replay, clean up or automatically correct.

After a successful process, attempt post-import export. Report export failures
and try supported registered REST reads as the read-only alternative;
limited coverage is partially_verified, not full runtime verification.
For complete export evidence, the local verify_item_catalog_set_readback function in
scripts/profile_content_library_fsm_evidence.py compares the parent, every child,
scoped row counts and supplied/omitted fields, rejecting missing/extra/changed
children and scoped rating rows. It is a comparison primitive, not a process or
approval verifier. Its caller must independently bind the approved proposal,
package SHA-256, target, accepted process, successful status and fresh evidence.

The task's local lifecycle caller is now
`scripts/verify_new_catalog_set_lifecycle.py`, described below. Do not use the
comparison primitive alone as complete lifecycle evidence.

If export omits ContentItemCode or another required value, the result is not
verified. Obtain the registered child readback through the Content Items owning
workflow, retaining the exact parent and child identity; never fill readback from
the approved input. Full verification requires complete supported evidence. REST-only
readback reports which fields it proves and the remaining gaps. A sample of one
child or an initiation receipt is insufficient for whole-set verification.

Promotion requires separate reviewed complete-set evidence for the tested
context(s). No automatic promotion, PM acceptance or project closure follows
from a local test, generated package, successful process or this contract alone.

## Local lifecycle verification

This is a later, explicitly requested status/readback phase, not a pre-import
rule and not a new execution adapter. Obtain original evidence only through the
declared Core initiation/status, task-level export and registered Content Items
read workflows with their existing prerequisites. The owning workflow retains
the sanitized source responses and projects their fields into the lifecycle
document below. Do not manufacture accepted IDs, success, target classification,
approval or readback assertions. Hashes establish file consistency, not source
authenticity; the local helper cannot authenticate an arbitrary supplied receipt.

Use Python 3.11 (minimum 3.10):

```bash
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/verify_new_catalog_set_lifecycle.py \
  --project-root project/SELECTED_PROJECT \
  --proposal artifacts/TEST_RUN/package-input.json \
  --readiness artifacts/TEST_RUN/package-readiness.json \
  --archive artifacts/TEST_RUN/new-set.zip \
  --baseline baselines/TEST_RUN/item-catalog.zip \
  --task-envelope artifacts/TEST_RUN/core-approved-envelope.json \
  --task-context artifacts/shared/runbook/current/task-context.json --sequence 1 \
  --lifecycle artifacts/TEST_RUN/lifecycle.json \
  --as-of ACTUAL_CURRENT_RFC3339_TIME
```

The example skips pre-import export. Supply --current-state only when revalidating
an older package that used retained current-state evidence; never acquire a new
pre-import export for this workflow. Replace the example paths with the exact retained files. Every file argument
except project-root is project-relative. Only verified synthetic or approved seed
setup evidence may be stored here; do not acquire customer-bearing full exports
without an approved Core data-handling contract. Hidden paths, traversal,
symlinks, unsupported extensions, oversized and recognizable sensitive content
are rejected. Nothing is written by this command; persist its sanitized stdout
through project artifact registration. No network access is used.

The lifecycle JSON has exactly five root fields:

| Field | Contract |
|---|---|
| schema_version | 1.0 as a string |
| submission | Accepted Core submission record described below |
| process | Latest retained normalized process state described below |
| readback | Complete export record, null when unavailable, or same-operation fsm-export record with status skipped/failed; failed requires a diagnostic evidence reference |
| child_evidence | Registered child JSON paths; used as a REST fallback when export is unavailable, or to supplement complete export |

Every submission, process and populated readback record contains task_code,
target_environment, package_sha256, catalog_set_fingerprint, request_id and
process_id. They must all bind the same accepted operation; IDs are positive
decimal strings. Its evidence field is exactly path and sha256, referencing the
original sanitized owning-workflow response (submission/process) or export ZIP
(readback). The normalization is a task-owned projection, not a claim that Core
emits this document schema. Preserve the source response alongside it for review.

| Record | Additional required fields |
|---|---|
| submission | route core.data-loader; status accepted; submitted_at; task_envelope_sha256; task_context_sha256 |
| process | status succeeded, failed, pending or timeout; captured_at; terminal states also completed_at and process_log (path and sha256) |
| readback | Successful export: origin fsm-export, unfiltered_task_export true, captured_at and valid_through. Optional export: origin fsm-export and status skipped/failed, with diagnostic evidence for failed. |

The approved Core envelope contains its unchanged preview and approval objects;
task-context and sequence select the exact retained task. The verifier reuses
Core's archive approval check and revalidates ordered task rule results, exact
finalData and task identity. It reopens the entire archive against the complete
proposal and original baseline/current evidence at submitted_at, not against new
duplicates created by the load. Metadata/member shape and every provider row
must match. Approval must precede submission. Terminal completion must follow
submission and precede status capture; readback must follow completion and be
fresh at as-of. Reusing the package, baseline or pre-import export as readback
does not pass.

When child codes are blank in the full export, obtain one complete, independently
captured evidence document per supplied child from the registered Content Items
exact-code read workflow. These are the existing catalog adapter's complete
CATALOG_REST / read-only-exact-code-check documents, with their evidence_sha256,
exact_provider_key, catalogs, matches, captured_at and valid_through. The verifier
requires complete same-target/context coverage, exactly one global code match,
the exact owning catalog and registered template, and fresh post-completion
observations for every child. It joins by context, catalog and exact observed Name,
never array order. It supplements only missing export ContentItemCode values
with independently observed codes. Full-export descriptions, dates, counts,
supplied and omitted values still have to match; no approved value is copied
into readback. Missing descriptions or other required values are not repaired
from the input or this limited REST surface.

| Exit | Status and meaning |
|---|---|
| 0 | verified: retained successful process and complete bound readback agree |
| 2 | blocked, readback_mismatch, partially_verified or verification_incomplete: invalid evidence, differences, limited REST coverage or missing verification; import status is reported separately |
| 3 | readback_pending: pending or timeout; keep IDs and use the existing status-only next-check route |
| 4 | process_failed: terminal import failure retained, with partial observations and evidence gaps when available |

A missing or corrupt log blocks a success claim but does not erase an already
bound failed process. Invalid partial readback likewise appends an error to the
failed result. Even matching readback cannot convert a failed process into a
success. Every result has submission_authorized false and retry_performed false;
no upload, correction, cleanup or replay is authorized. A verified result means
the retained evidence agrees; synthetic fixture results are local test proof,
not live evidence. This command neither promotes the certification-only registry
nor verifies unrelated tasks in a mixed-task canonical request.

## Strict-verifier limitations

The comparison currently treats an omitted optional foreign-ID column and an
exported literal `#null` as different values. Do not ignore CountryId,
RatingModelId or StateProvinceId wholesale: that would also hide an unapproved
reference. Retain the mismatch until authoritative provider null semantics and
a narrowly scoped comparison rule have been reviewed. Matching business fields
and a successful import remain separate evidence, not a strict verification pass.

For a package that used supplied current-state evidence, the lifecycle helper
revalidates that receipt at submitted_at. Skipped-export receipts have no
freshness claim. It does not consume a Core-approved freshness waiver. If Core
accepted such a waiver, preserve its exact approved evidence and the helper's
blocked result; do not backdate submission, extend the receipt, or describe the
load as unapproved solely because this stricter local verifier cannot accept it.
Supporting that case requires a reviewed waiver-aware verification contract,
not a generic bypass. Neither limitation authorizes a retry or provider promotion.
