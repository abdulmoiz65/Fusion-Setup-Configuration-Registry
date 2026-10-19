# Design Enforcement

| Condition | Severity | Required action |
|---|---|---|
| A supplied data CSV is parsed, compared with a sample/template, or checked for columns, fields, rows, lookups, identities, parents, row-level operation semantics, or volume | Error | Stop local data validation and restart the supplied-CSV pass-through route. Job-level `ImportMode` must still be selected separately. |
| A supplied data CSV is normalized, repaired, or rewritten | Error | Restore the exact supplied bytes and rebuild the immutable preview. |
| A supplied CSV has more, fewer, reordered, or unfamiliar columns | Allowed | Preserve it unchanged; Fusion Import Management evaluates the content. |
| A `PartyUsageCode` check or waiver is requested for a supplied CSV | Error | Remove the check; no data-validation waiver is required. |
| Exact object routing remains ambiguous | Error | Ask only for the CX Business Object code; do not inspect data to infer it. |
| Job-level `ImportMode` is missing, ambiguous, inferred from CSV content, or left to Oracle's default | Error | Stop before approval and require exactly one of `CREATE_ONLY`, `CREATE_RECORD`, or `DELETE_RECORD`. |
| Exact code is absent from live Import Management metadata or `ImportSupport` is not `Y` | Error | Stop before upload; do not substitute another code. |
| UCM account is caller-supplied or stale | Error | Resolve it from current exact-object metadata. |
| Ordered sources or any source bytes change after preview | Error | Invalidate approval and build a new CSV-group preview. |
| Approval digest is a source-file or ZIP digest, or a reconstructed group digest | Error | Complete Core source review, reconcile its ZIP with the protected CX manifest using the skill-local helper, then bind only the adapter-returned group digest. |
| The pre-approval Core Data Loader preview includes `--task-routed` but has no approved Task Hook envelope | Error | Remove `--task-routed` from the non-mutating preview invocation. Reconcile Core source review with the protected CX preview before building the Task Hook preview from the adapter group digest. |
| A supplied direct CSV is renamed, rewritten, or reported under a synthetic `direct-cx-import.csv` name | Error | Preserve the exact supplied basename and bytes. For one data CSV, use its basename as the Data Set Name; for multiple data CSVs, retain every upload basename and use an object-based aggregate Data Set Name. |
| Direct-CX Task Hook requires physical-archive verification of a CSV group | Error | Keep Core Data Loader's review ZIP and digest as separate source-review evidence; reconcile it with the protected CX preview and use the adapter group digest without physical-archive verification. |
| The unchanged target and canonical digest are presented for a second routine execution approval | Error | Use the user's single approval to create the matching Task Hook envelope and protected Core adapter approval, then execute it once; a consumed approval cannot authorize a rerun. |
| Task Hook preview omits `ImportMode`, activity name, or the mode-aware execution adapter | Error | Rebuild the preview; a descriptive word such as `delete` does not bind `DELETE_RECORD`. |
| This skill executes generic Core Data Loader `initiateDataLoad`, or the CX adapter omits/mismatches `--import-mode` | Error | Stop before the first POST. Use Core Data Loader only for governing preflight/authorization and the CX Import Management adapter for exact-mode execution. |
| The approved group needs multiple data files or a mapping CSV but the mode-aware adapter cannot bind the complete group | Error | Record the workflow gap and stop; do not fall back to a generic import. |
| Live submission bypasses Core Data Loader preflight/Task Hook authorization or retries a POST automatically | Error | Stop and rebuild the governed preview with fresh exact-group approval. |
| A live upload bypasses the supported Core CX adapter | Error | Use `core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py execute-approved-import` with the approved local CSV group, exact settings, and protected `--approval-id`; do not create a pillar transport wrapper. |
| An uncertain Core upload/import outcome causes the source file to be uploaded again | Error | Stop and use the Core adapter's read-only status route; obtain explicit recovery authorization before any new write. |
| An unchanged supplied Hierarchy or Hierarchy Member delete lacks locally verified identifiers, an exact pre-delete match, or row-level delete capability evidence | Allowed | Preserve the CSV unchanged, bind DELETE_RECORD and the destructive effect into the immutable approval, and let Fusion Import Management accept or reject the rows. |
| A generated or explicitly validated Hierarchy or Hierarchy Member delete lacks its documented exact identity, identifier-only shape, exact pre-delete match, destructive approval, or target-specific DELETE_RECORD evidence | Error | Stop before upload and correct the generated or explicitly validated request. |
| An Additional Identifier live delete lacks one exact parent-scoped `PartyIdentifierId` match, an identifier-only row, or destructive approval | Error | Stop before upload. Resolve the exact child under the selected party; do not use a source-system pair or descriptive fields as delete identity. |

Template, profile, field, parent, row-level operation semantics, volume, lookup,
and destructive-data rules apply only when generating a CSV or when the user
explicitly requests data validation. Exact job-level `ImportMode` selection and
binding always apply.
In that optional branch, completion cannot be claimed until the verification
ledger covers every requested parent instance. Linked Party target-value
validation must use the exact `fusion-runtime` `--target-values-json` contract.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCA.DESIGN_GATE | decision | 5 | design_enforcement | pass->TCA.APPROVAL;fail->TCA.RETURN_ISSUES | TCA.METADATA | stop | Preserve supplied CSV bytes and enforce routing, group-integrity, approval, and executor boundaries. |
