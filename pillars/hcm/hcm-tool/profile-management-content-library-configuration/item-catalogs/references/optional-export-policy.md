# Optional exports for Item Catalog imports

This policy applies only to ORA_MANAGE_PROFILE_ITEM_CATALOG, including catalog-only,
anchored-child and explicit new-set packages. It is a workflow choice, not an
Oracle requirement to export before importing. Other tasks keep their contracts.

## Before import

Skip pre-import export. Do not invoke shared.setup-export.task-level-export to
acquire current state or a new baseline before importing, and do not ask whether
to attempt it. Record status skipped and continue package validation and the
normal Core Data Loader workflow using a supplied or reusable reviewed template.

If no valid template is available, do not fabricate one or silently initiate an
export. Offer the separately requested and approved
[filtered schema recovery route](filtered-schema-recovery.md), or ask for a
supplied template. The skip policy applies to the import workflow; it does not
prohibit an explicitly selected standalone export investigation. Such an export
may establish schema, not complete current-state or duplicate-absence evidence.

When using a supplied export, validate its target, task, schema, completeness,
freshness and hash; known duplicates or conflicting parent values still block
create. Do not silently discard contradictory evidence. A failed acquisition
must not be represented as an empty export or a successful duplicate check.

Without current-state export, omit --current-state-zip and set the proposal's
current_state_receipt to exactly:

```json
{
  "status": "skipped",
  "task_code": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
  "target_environment": "TEST_TARGET",
  "diagnostic_reference": null
}
```

For compatibility with an already-failed attempt, accept status failed and a nonblank sanitized diagnostic
artifact alias, such as item-catalog-export-attempt-1. The owning workflow retains
the actual failure class, request/process IDs when available and safe diagnostic
details under that alias. Bind this receipt in provider_rows_fingerprint and the
Core preview. No live call is made by the package builder.

The builder still requires --baseline-zip for valid metadata/member/header shape.
This may be a supplied or reusable reviewed package/template; it need not be
newly exported or contain current target data. For that option use exactly:

```json
{
  "kind": "reviewed-template",
  "task_code": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
  "target_environment": "TEST_TARGET",
  "sha256": "ACTUAL_SHA256_OF_REVIEWED_TEMPLATE"
}
```

Do not fabricate metadata or submit baseline business rows. Rewrite all CSVs
from the approved rows and preserve validated metadata bytes. Existing
template-only and complete-export receipts remain supported with their freshness
checks. A reviewed template establishes package format, not current target state.

Exact Content Type, supported field/provider, source mapping, target/access,
package integrity, task context and Core approval checks remain. Without the
export, profile_v2_evidence_sha256 may be null; do not fabricate its fingerprint.
Export-based duplicate checks, existing-parent no-drift comparison and indirect
Profile V2 preflight are reported as not performed in unverified_checks. An
anchored child still requires the exact intended parent values; their current
target equality is unverified. A new parent is intended-new, not verified absent.
Local duplicate rows and known observed collisions remain errors.

## After import

Keep import process status separate from verification status. Retain status and
ProcessLog when available. Never replay an import because export or readback
failed, and never convert a failed/partial/timed-out import into success.

Attempt a fresh task export for post-import verification. If it fails, report
that failure and try the registered read-only alternative below. An unavailable export must not erase a
successful import result. A successful export with mismatching values remains a
mismatch; do not hide it with a more limited read.

For supported enhanced-profile children, route through the Content Items owner:
content-items/scripts/talent_content_item_catalog_adapter.py capability, then
check --context CONTEXT --content-item-code EXACT_CODE, using authenticated Core
configuration. Use the registered selector and Fusion-returned child links from
content-items/references/content-item-rest-provider-registry.json. Exhaust pages
and all owning catalogs; bind the target, exact parent/catalog/context/code,
fresh post-completion capture and evidence hash. These are GETs, never alternate
import writes. Do not use an undocumented endpoint or historical HDL create route.

Try this read for every supplied child. Report the observed fields, differences,
missing/ambiguous matches, and failures. The current REST surface can verify
catalog identity and registered child fields, but does not prove full parent
description/no-drift, scoped row counts, rating rows or every child field. Use
partially_verified for matching limited coverage and verification_incomplete
when no reliable comparison is available. Reserve verified/runtime_verified for
complete supported evidence. For catalog-only scope or fields without a registered
read, report the gap and the next supported verification step; do not invent one.

The new-set lifecycle verifier accepts readback null or a same-operation
fsm-export record with status skipped/failed. Failed records must reference the
retained diagnostic file using evidence.path and evidence.sha256. child_evidence
contains the existing registered per-child REST receipts. The verifier compares
these when export is unavailable and reports partial coverage; it never fetches
evidence, mutates Fusion, or promotes a provider. Both partial and incomplete
verification return exit 2; process_failed retains exit 4.

Provider-promotion evidence and the explicit one-child certification batch keep
their stronger complete-readback criteria. If those criteria cannot be met,
report that certification/batch verification is incomplete; an ordinary authorized
import does not depend on promotion or completion of that optional batch mode.
