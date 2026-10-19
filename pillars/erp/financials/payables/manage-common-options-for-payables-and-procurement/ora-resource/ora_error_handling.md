# Manage Common Options for Payables and Procurement Error Handling

For inaccessible additional REST validation, follow the availability policy
in ora_reference_lookups.md: retain the sanitized failure class and status,
preserve values, emit UNVERIFIED_API_UNAVAILABLE and continue preparation and
preview. This is a non-blocking warning, not a passed lookup or automatic
approval. The missing-evidence and auth failure stops below still apply to
BU/ledger identity, SOAP account validation and checks without this exception.
Completed negative or ambiguous reference results still require correction.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Template, header, node, or row-field-count mismatch | Stop, retain a sanitized package-shape finding, and recreate the candidate from the exact same-task template |
| A product-validated field lacks its required resolver evidence | Stop before preview unless the supplemental REST availability policy applies; record the specific attribute and missing resolver category |
| A transport-sanity-only field lacks a business-domain validator | Do not block a structurally valid candidate. Record the limitation so Fusion import/reconciliation remains the final acceptance check. |
| A direct LOV resolver has no exact eligible match, or a target/context resolver is ambiguous | Stop the local candidate and ask for corrected input or evidence. Do not fuzzy-match, select the first value, or reuse an export value. Report `AP:::AP_ATTR_NOT_EXISTS_TARGET_INS` only if the Fusion import actually returns it. |
| EnterpriseId is unresolved after applying the defaulting precedence | Ask for the affected row's EnterpriseId. Explicit input is allowed even when the export is empty, all blank, or has multiple distinct IDs. A singleton nonblank export value needs no confirmation. |
| The ERP Financials BU or ledger receipt does not prove one exact BU and its matching primary ledger | Stop before candidate construction. A user-entered EnterpriseId is allowed but does not replace BU/ledger evidence. Do not substitute a cross-pillar endpoint, user-entered SOBName, first returned row, or unrelated ledger. |
| HCM bill-to name resolution returns an authentication, authorization, transport, service, or endpoint-access error | Stop name resolution and ask for InternalLocationCode only if missing; never guess it or treat the error as no match. With an explicitly supplied code, use the declared FSCM fallback. Inaccessible supplemental checks may continue with a warning under the availability policy. |
| `SOBName` cannot resolve to exactly one ledger | Reject the row because `SetOfBooksId` is mandatory in the underlying entity |
| An account-segment field reaches governed import execution | If GL returns an invalid-combination result, preserve the redacted error and stop without retry. If it returns a newly created CCID, treat it as a verified side effect of the approved artifact and reconcile it through the Data Loader route |
| An approved direct account-combination SOAP creation receives a timeout, transport failure, HTTP 401, HTTP 403, or SOAP fault | Do not replay the mutating request. Preserve sanitized request identity and failure evidence, then run read-only `DynamicInsertion=No` reconciliation for the exact ledger and full string before considering any further action |
| An approved direct account-combination SOAP creation returns `Invalid` | Preserve the sanitized receipt and returned GL error; do not create segment values, modify the request, or retry. Correct the underlying ledger, segment-value, cross-validation, or dynamic-insertion condition before requesting new approval |
| An approved direct account-combination SOAP creation returns `Valid` but the no-create follow-up does not return the same valid enabled CCID | Classify as uncertain write, preserve both receipts, and stop. Do not repeat creation; resolve through a read-only GL investigation |
| Data Loader validation, Task Hook, preview, or approval is missing/stale | Stop before mutation; changed input requires a new validation and approval cycle |
| Fusion process, authentication, transport, or verification fails in a later governed execution | Preserve redacted process/status evidence and do not replay an import automatically |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Package contract gap | Header, row count, metadata node, or archive contract differs | Refresh/rebuild the exact package |
| Product-validation evidence gap | A changed field with an import-hook/entity/GL resolver lacks its required evidence | Obtain the named task-specific evidence |
| Transport-sanity disclosure | A changed field has no source-backed business domain beyond CSV shape | Preserve the type/length/precision/date result and disclose that field-level semantic acceptance is deferred to Fusion |
| Technical lookup gap | A required resolver outside the supplemental REST availability exception is unavailable, returns null, has no exact eligible match, or yields an ambiguous target/context | Stop the local candidate; correct the input or obtain the named evidence. Keep any later Fusion error separate from this local classification. |
| UNVERIFIED_API_UNAVAILABLE | A supplemental REST read reports a bound API availability failure | Preserve supplied values and continue with a warning under ora_reference_lookups.md; never report the check as passed. |
| Target-context default gap | No explicit EnterpriseId or usable export-derived value, or the two ERP responses are not exact/matching | Ask for missing EnterpriseId; separately obtain valid ERP BU/ledger receipts. The ERP endpoint does not validate EnterpriseId. |
| Approval blocker | Immutable preview or current contextual approval is absent/stale | Revalidate and obtain a later approval through Data Loader |
| Auth or authz | Required privilege is unavailable | Use core's permitted read-only authentication handling; supplemental REST failures continue with a warning, while required identity and execution failures stop. |
| HCM location-route access gap | HCM name resolution remains unavailable after the permitted read-only authentication handling | Ask for InternalLocationCode only if missing; with supplied CSV inputs, follow the declared fallback and supplemental availability policy. |
| Transport or environment | Network or target service fails before side effects | Retry only bounded idempotent reads in the selected workflow |
| Fusion API or process failed | Later governed submission/process fails | Persist redacted log/status and do not replay |
| Process timeout | Status remains nonterminal | Do not resubmit; preserve the process identity and provide the next-check path |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Static blocker | Exact task code, resource rule, missing evidence, and safe next action |
| Future preview | Exact target, immutable artifact identity, package-shape receipt, unresolved blockers, and current approval state |
| Future failure | Failure class, environment, stage, redacted evidence, external IDs when available, and recommended action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unknown business behavior | Do not invent a default, requiredness rule, accepted value, lookup, or update behavior; apply only the declared transport sanity when no product-backed field contract exists |
| Incomplete resolver | Do not call an undocumented service, fuzzy-match, or select the first candidate |
| Missing Data Loader gate | Do not upload, invoke a task adapter, import, or otherwise change Fusion |
| Uncertain write | Do not replay until read-only reconciliation establishes side effects |
| Direct SOAP creation is requested without exact current approval | Do not set `DynamicInsertion=Yes`; obtain a new approval bound to the ledger, full segment string, endpoint, operation, and side effect |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APCO.HANDLE_ERROR | step | 60 | error_handler | handled->APCO.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, or enforcement failure |
| APCO.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| APCO.DONE | terminal | 80 | terminal | none | APCO.ENFORCE_DESIGN | stop | Required checks passed and unavailable additional REST checks are disclosed as unverified |
