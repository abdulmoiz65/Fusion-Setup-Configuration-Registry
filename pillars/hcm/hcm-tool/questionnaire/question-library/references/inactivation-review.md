# Comparing Question inactivation reviews

Use only for the existing status-only Question Library inactivation route. The
live resolver and Data Loader remain responsible for target verification and
submission. This offline comparator does not make REST requests, generate DAT
files, establish that a user approved an action, or authorize an upload.

## Workflow

1. Collect current identity, live HDL contract and complete visible-usage evidence
   using the task's declared resolvers. Populate the normalized snapshot below;
   keep raw evidence hashes, timestamps and scanned totals in the audit record.
2. Run the comparator with `--current` to obtain the material approval fingerprint.
   Show the business effect, zero matching usages and partial-coverage limitation
   for approval. Record the actual user approval against this fingerprint.
3. After approval, refresh the live checks and run with `--approved` pointing to the
   immutable snapshot that was actually approved and `--current` to the new one.
   Compare semantic scope rather than hashes of whole JSON response files.
4. If the result is `rescan_required`, perform one fresh complete read-only scan
   and pass it with `--confirmation`. Reuse neither the first response nor its scan
   ID. If the same question-specific evidence is confirmed, preserve the original
   approval and report count drift as a warning. Do not request approval again
   just because unrelated counts still differ. If the repeat fails or material
   evidence differs, stop for diagnosis rather than looping.
5. Only `approval_retained` can resume the existing route after recorded approval.
   Map the business intent `inactivate` to the existing serializer's `intent:
   update`, `operation: MERGE`, with a complete `update_contract`; its sole changed
   field is Status and it emits no child data rows. Continue the normal separate
   unchanged-hash Data Loader preview and approval. This comparison never relaxes
   DAT/ZIP byte integrity or other flows' approval rules.

Run from the Question Library skill directory:

```bash
python3 scripts/compare_inactivation_review.py --current current-review.json
python3 scripts/compare_inactivation_review.py --approved approved-review.json --current current-review.json
python3 scripts/compare_inactivation_review.py --approved approved-review.json --current current-review.json --confirmation confirmation-review.json
```

The script emits JSON to stdout and writes nothing. Exit 0 means
`approval_retained`; exit 2 means review, rescan or diagnosis is needed. Persist
its output through the existing project artifact workflow. `upload_authorized`
is always false.

## Normalized review snapshot

All fields below are required. SHA values are lowercase hex SHA-256 strings, not
the placeholders below. Evidence must come from the current live checks, while
unresolvable optional provenance must be recorded explicitly as unavailable.
Keep `Question.dat` content and the operation/component contract hash separate
from the functional questionnaire-template scan. Application-release and
principal provenance are explicitly nullable: unavailable evidence is recorded,
never invented, and does not by itself block the partial-evidence impact review.

```json
{
  "review_schema": 2,
  "task": "question-library",
  "requested_operation": "inactivate",
  "environment": "<resolved target identity>",
  "release_evidence": {"status": "unavailable", "value": null},
  "principal_evidence": {
    "status": "unavailable",
    "fingerprint_sha256": null
  },
  "scan_id": "<unique live scan ID>",
  "checked_at": "<timestamp>",
  "question_key": {
    "SubscriberName": "Recruiting",
    "QuestionCode": "<exact question code>",
    "QstnVersionNum": 1
  },
  "current_state": {"Status": "A", "LatestVersion": "Y", "UpdateAllowedFlag": true},
  "lifecycle_conflicts": [],
  "change": {"Status": {"from": "A", "to": "I"}},
  "changed_fields": ["Status"],
  "child_rows": 0,
  "preserved_values_sha256": "<canonical unchanged emitted root values hash>",
  "template": {
    "file": "Question.dat",
    "sha256": "<exact live DAT template bytes hash>",
    "contract_sha256": "<canonical discriminator, keys, components, attributes and MERGE contract hash>",
    "supported_operation": "MERGE"
  },
  "checks": {
    "identity_exact": true,
    "fresh": true,
    "hdl_contract_validated": true,
    "inactive_status_validated": true,
    "preserved_values_verified": true,
    "lifecycle_state_checked": true
  },
  "visible_usage": {
    "coverage": "partial",
    "endpoints": {
      "questionnaireQuestionsLOV": {
        "request_scope_sha256": "<canonical request scope hash>",
        "success": true,
        "pagination_complete": true,
        "child_pagination_complete": true,
        "scope_verified": true,
        "matching_placements": []
      },
      "questionnaireTemplates": {
        "request_scope_sha256": "<canonical request scope hash>",
        "success": true,
        "pagination_complete": true,
        "child_pagination_complete": true,
        "scope_verified": true,
        "matching_placements": []
      }
    }
  },
  "scan_diagnostics": {
    "templates_checked": 3,
    "placements_checked": 14,
    "template_set_sha256": "<sorted distinct functional template business-key set hash>"
  }
}
```

The caller records actual current lifecycle conflicts (seeded, locked, in-use,
or other non-editable evidence). Empty means no conflict was returned by the
declared checks; it does not prove hidden dependencies absent. Retain any extra
material lifecycle state in `current_state`, including unknown state, so changes
are detectable. Never populate success/freshness/coverage booleans from an old
summary merely to satisfy the comparator. Use true child completion for the flat
placement LOV only after verifying no child traversal is needed; template
sections and questions require their own traversal proof.

Use canonical JSON with sorted keys and stable value types for content hashes.
Canonicalize business-key sets before hashing: order, duplicate page entries and
pagination offsets are not business identity. When a current application release
is independently verified, set `release_evidence.status` to `verified` and record
the returned non-empty value. Otherwise retain `unavailable` and `null`; never
infer a quarterly release from the date, hostname, REST resource version, or HDL
template timestamp. The live template and contract hashes remain mandatory and
bind the executable target contract.

When the authentication layer supplies a stable, verified, non-secret principal
identifier, hash only that identifier and set `principal_evidence.status` to
`verified`. Otherwise retain `unavailable` and a null fingerprint. Never hash an
access token, refresh token, client secret, Authorization header, or an assumed
Fusion data-security scope. Successful authenticated endpoint requests prove only
those exact reads; they do not prove complete data visibility. The mandatory
`visible_usage.coverage: partial` warning carries this limitation into approval.
The request-scope hash rules and exact matching procedure belong to
`ora_reference_lookups.md`.

## Decisions

| Outcome | Meaning |
|---|---|
| approval_required | Initial review, missing comparable old snapshot, or material target/key/version/state/preserved-value/contract/access/query scope changed. Show the concrete changed business evidence. |
| rescan_required | Only catalog scan diagnostics changed. Perform one fresh confirmation scan without asking for approval again. |
| approval_retained | Fresh complete checks retain the same eligible question-specific scope; any diagnostic drift has been confirmed. Continue under the recorded business approval. |
| blocked | Visible usage, failed/incomplete traversal, stale or unverified evidence, unsafe state, changed child scope, or inconsistent confirmation. Diagnose rather than seek approval to bypass. |

Schema-1 reviews and old reviews that contain only totals plus
`pagination_complete: true` cannot be upgraded by inference. Collect missing
scope and nested coverage once and obtain one schema-2 review. Subsequent
timestamp, evidence-ID or unrelated total changes follow this contract and do
not create a recurring approval loop.
