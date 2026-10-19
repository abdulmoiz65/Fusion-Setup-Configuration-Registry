# Manage Ledger Sets Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| UI route requested or attempted by a delegate | Return input_validation with reason ui_execution_prohibited and stop that route. Do not navigate, inspect or operate Fusion UI for discovery, validation, writes or verification. Use the declared FSCR route only for a supported operation. |
| Required fact missing from framework sources | Return catalog_or_metadata_mismatch with reason missing_framework_evidence and the exact fact/contract missing from the declared endpoint/export/adapter. Stop the affected operation. Do not close the gap through UI inspection, screenshots, ad hoc SQL or an invented API. |
| Requested or packaged deletion of an existing ledger set | Return input_validation with reason ledger_set_deletion_prohibited, the requested set identity and preserved-state disposition. Stop before deletion-related acquisition, package preparation, upload or execution. This is FSCR policy, not missing Oracle metadata; do not obtain a delete contract, request delete approval or propose another route. |
| Missing required header, classified currency or all assignments | Stop before Data Loader upload/submission. Treat a no-assignment rejection such as GL-780364 as input_validation; supply at least one valid assignment. |
| Generic required-value error on an FSM header | A message such as FND_CMN_ENTR_VLUE does not identify the missing attribute. Retrieve ProcessLog, ProcessResultsReport and ProcessResultsSummaryReport through the selected core diagnostic route when available; the detailed result report can contain nested JBO errors absent from ProcessLog. Inspect the reported parent file, actual row and current technical create profile. Distinguish confirmed missing value from candidate fields; do not assert that ShortName, currency or a flag caused the error without attribute-specific or controlled-test evidence. Reconcile persisted state before a corrected submission. |
| Detailed row report contains JBO-25026, JBO-27027 or JBO-27014 | Trace the nested error to the ledger-set entity and retain each completely named mandatory attribute. Match those names to the actual candidate header and the packaged field contract. Missing initialization values such as ledger type codes, legacy currency/first-period placeholders and accounting flags belong to that profile; a member-ledger export does not automatically supply valid set values. A truncated final attribute name or status message means the list may be incomplete. Do not claim a minimal sufficient field set from a truncated report or successful multi-field correction. |
| Detailed row report contains JBO-27024 or invalid-attribute messages after primary-export values were supplied | Enumerate every complete nested message, not only the first ProcessLog attribute. Separate ledger-set category/type, legacy currency/first-period, segment-option and future-period initialization from shared structure evidence. Compare with the packaged set contract, retaining unresolved or truncated diagnostics. Reconcile persisted state before any corrected candidate; the previous archive approval never covers changed bytes. |
| Duplicate identity or conflicting lookup facts | Disclose distinct business identities and resolve create versus update; do not choose the first result. |
| New project has no external initialization or structure profile | Use packaged MLS_FSM_CREATE_V1, fresh lookups and the primary-ledger-scoped structural export. Missing historical profiles or a separate COA export are not ordinary creation blockers. Report actual package/type, scope/identity, access or required-field failures; conditional COA acquisition must name its required gap. |
| Fresh duplicate queries return zero | Record no_conflict_observed with the queried scope and read/paging results, then continue normal preparation. Do not demand a global inventory certificate unless the stricter policy was explicitly selected; known access restrictions still require correction. |
| Base-profile omission rejected by Fusion | Treat the completely named field as a server-confirmed requirement for that contract. Inspect all row diagnostics, reconcile state, establish an exact mapping, rebuild and obtain approval for changed bytes. Do not guess a descriptor, inherit primary-ledger settings or silently retry. |
| Incompatible member or GAAP/currency restriction | Identify the exact member and conflicting property before approval. |
| Nested set rejected for classification mismatch (for example, GL-782640) | Compare the parent and assigned set classifications, not only their leaf currencies. Treat the parent and child object failures as one relationship error when the detailed result shows the child failed because the parent failed. Correct the classification or choose a compatible nested set, reconcile persisted state, then validate new package bytes before an approved import. |
| Unsupported assignment removal, clearing, structural change or DFF mapping | Return missing supported contract; do not treat CSV omission as member deletion or blank as an implicit clear. Existing parent-set deletion is prohibited separately, even if a delete contract exists. |
| Business inputs change after references or package validation | Re-resolve affected declared endpoint facts, rebuild the intended delta and revalidate immutable bytes before approval/submission; do not inspect dependent UI controls. |
| External lookup/import failure | Classify and retain sanitized stage, task/environment, status and exact known process/request ID; preserve partial successes and do not replay an uncertain mutation. |
| Accepted export but local download/path failure | Classify the local failure separately from the Fusion process result. Reconcile the recorded process and retry its read/download through the declared helper into a valid destination; do not submit a duplicate export merely to shorten its local path. |
| Negative test blocked before import | Record rejected_before_import, the assisted or automated evaluation method, owning rule/node, exact conflicting facts and that no import was submitted. Do not describe this as an Oracle import failure or proof that Oracle prohibits the action. |
| Several violations in one request | Retain all observed blockers and identify which facts conflict. Do not infer isolated GAAP, calendar or COA coverage from a case that fails several checks together. |

For controlled trials, report one testcase per submitted immutable package, with request ID, Data Loader terminal status, loaded/failed counts, FSM ProcessLog processed/succeeded/failed/warning counts, detailed error cause where applicable, and a separate persisted-state result. Count a corrected submission as a new attempt; do not hide the failed attempt or infer success from a zero-error initiation response.

For a test suite, count live creates/updates, read-only reviews and pre-import rejections separately. FSM business-object counts are not a count of assigned ledgers or proof of saved member names. Include exact direct-membership comparison, requested field comparison and update preservation results; label recursive effective membership as derived unless independently reported. Report missing fixtures, unsupported operation contracts and unavailable DFF sources as remaining coverage gaps, not passed tests.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Missing, malformed, too-long or invalid-enum input; prohibited UI route or existing-set deletion | Correct the identified input; for ui_execution_prohibited use the declared FSCR route, and for ledger_set_deletion_prohibited preserve the set and select only create, review or a supported update. |
| catalog_or_metadata_mismatch | Wrong task/package/release, unsupported representation, unproved import operation or missing required framework evidence | Obtain the exact required facts through current declared FSCR metadata/endpoints/exports; no UI fallback. |
| auth_expired_or_invalid | Authorized cached-token read rejected | Core auth may refresh once, then retry the identical GET once. |
| authorization_or_privilege | Missing privileges or 403 after allowed refresh | Use role/access diagnostics; stop. |
| transport_or_environment | Environment unavailable or bounded read retry exhausted | Resolve connection and resume safe read only. |
| fusion_api_error | Valid server error response | Preserve safe message/status/path and concrete correction. |
| process_timeout | Core process wait limit reached | Report last status and process/request ID; check existing process before resubmission. |
| process_failed | Import/load reports failure or partial errors | Review every row diagnostic and reconcile resulting state. |
| artifact_persistence | Invalid path, failed write or digest mismatch | Preserve safe diagnostics and rebuild only in permitted workspace. |
| approval_blocker | Mutation/retry lacks approval for the exact operation/artifact | Use the selected core executor's approval workflow after all validation passes. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Task validation complete | Exact task code/name, operation, target environment, validated header/member deltas, evidence and candidate digest, remaining limitations; this is not write completion. |
| Base-profile create preview | Packaged profile ID, explicit initialization/omissions, exact primary-scoped structural source, negative duplicate-precheck scope and any untested field handling. Disclose any named gap and conditional COA acquisition separately. No claim of universal server acceptance or global uniqueness. |
| Before loader execution | Existing Data Loader preview and immutable-artifact approval; do not require this validation graph to receive a second approval. |
| After change verification | Persisted Name, Classification, Currency, structure/calendar, default, supplied DFF values, direct and effective membership, evidence source and actual unverified fields. |
| Failure | Failure class, current node/stage, safe message, known process/request ID, partial state and next safe action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing endpoint facts, manual fallback or requested UI execution | Do not use browser automation, screen/DOM/network inspection, UI controls, screenshots or grid extracts for task evidence or actions. Core.auth may hand login to the user without agent UI access; it does not authorize task-page access. |
| Existing ledger-set deletion or deletion-equivalent cleanup | Do not delete through UI, REST, FSM or another adapter; do not delete and recreate, remove all members as a workaround, or delete test data for cleanup/rollback. Metadata, privileges and general test/import approval do not waive the rule. Preserve the set and return the policy blocker. |
| Missing dependent ledger/calendar/COA/currency | Do not create another setup object implicitly. |
| Missing write endpoint | Do not invent one or mutate a LOV. FSM writes belong to core.data-loader. |
| Failed or uncertain mutation | Do not automatically retry upload or initiation, or bypass the framework through a direct mutation. Reconcile state through declared reads/exports and follow core retry approval. |
| Outdated or sample-only baseline | Do not claim current duplicates, membership, privileges or successful import from a sample or stale export. |
| Candidate validated | Do not report a ledger set created/updated until persisted-state verification passes. |
| Creation from the packaged contract | Do not require previous runs, a full ledger-set export, an external qualification receipt or a tenant-wide inventory solely to start ordinary creation. Current template incompatibility, failed reads, observed conflicts, invalid role joins and conditional state requirements remain blockers. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MLS.EXECUTION_GATE | decision | 60 | execution_gate | ready->MLS.DONE;blocked->MLS.HANDLE_ERROR;failure->MLS.HANDLE_ERROR | MLS.ENFORCE_DESIGN | stop | Validate handoff readiness, artifact identity and passed framework-only/existing-set preservation gates only. UI execution, deletion or missing required framework evidence blocks handoff; never use another executor as a bypass. Pre-upload Task Hook must pass before core.data-loader renders approval; it does not require approval or import completion to validate. Review requires complete requested evidence. |
| MLS.HANDLE_ERROR | step | 70 | error_handler | disclosed->MLS.FAILED | none | stop | Any applicable validation, lookup, dependency, default or design gate blocks. |
| MLS.DONE | terminal | 80 | terminal | none | MLS.EXECUTION_GATE | continue | Return task validation passed or verified read-only review. A write request is ready for the core loader's approval/execution step; no write success is asserted. |
| MLS.FAILED | terminal | 90 | terminal | none | MLS.HANDLE_ERROR | continue | Return a classified blocker, sanitized evidence and safe next action. |

## Mandatory Log Review Before Outcome Reporting

| Reporting Gate | Required Evidence or Action |
|---|---|
| Before reporting a submitted creation or update import as succeeded or failed, including a status-check reply | Through core.data-loader's declared status/diagnostic workflow, retrieve, persist and inspect the actual FSM ProcessLog matching the target environment and recorded request/process. Reconcile terminal status with business-object and row results, failed counts, warnings and error details. |
| Failed rows, partial results or generic/truncated errors | Inspect ProcessResultsReport and ProcessResultsSummaryReport when available through the declared core diagnostic route. Retain all complete nested errors and distinguish a child failure caused by its parent from an independent business error. Disclose diagnostic retrieval limits. |
| Matching log unavailable, incomplete or inconsistent with the status response | Report the API status as provisional and the import outcome as unconfirmed pending log review/reconciliation. Preserve known request/process IDs, retrieval error and next safe read. Do not declare success/failure, advance dependent work or resubmit solely because log evidence is missing. |
| Log-confirmed processing outcome | Cite the reviewed log, exact request/process identity and counts actually exposed. Disclose warnings, failed objects/rows and partial successes. Do not invent missing row counts or interpret successful business-object counts as saved member names or membership cardinality. |
| Before claiming the ledger set was created or updated as requested | Complete the entrypoint's applicable persisted-state checks in addition to log review. Processing success does not alone prove header values, supplied DFFs, exact direct/effective membership or preservation of unrequested fields. Report each remaining verification limit separately. |
| Rejection or failure before import submission | Inspect and cite the actual validation/client diagnostic and state that no import was submitted. No FSM ProcessLog exists for an unsubmitted request; do not describe this as a failed Oracle import. |
| Read-only review or an identical-state no-op | Cite the current framework evidence or comparison; do not present it as a successful import or invent a process log. |

A loader summary, HTTP response, terminal API status, validated candidate or absence of a visible error is insufficient to quote import success or failure. This reporting gate applies after submission; it is not a pre-upload Task Hook prerequisite, an additional approval or a reason to bypass the core executor. Preserve completed and partial results, reconcile uncertain outcomes through declared reads and never use deletion or automatic mutation retry to obtain cleaner logs.


## All Result Reporting and UI Refusal

The mandatory log-review gate applies before quoting any submitted import result, including status-check replies and failure analysis. Persist and read the actual matching log; do not substitute a loader summary, initiation receipt or UI observation. Missing or contradictory logs leave the outcome unconfirmed, with request/process identity and the retrieval gap disclosed.

For lookup, duplicate-check, review and no-op results, inspect the actual declared endpoint responses and available core diagnostics first, complete paging, and state visibility/unexposed-field limits. For native REST creation inspect its matching core diagnostic/audit record, response receipt and exact re-lookup. For pre-submission rejection inspect the actual rule/client diagnostic and say no import was submitted. These routes do not have FSM import logs; never invent one or require a dummy import to obtain it.

Refuse UI navigation or inspection by this skill or any delegate, including manual screenshots supplied as a verification workaround. Missing required evidence remains a reported endpoint/contract gap. Authentication is only the user-completed core.auth handoff; it grants no task UI access. Existing qualified preparation profiles and their bounded verification limits remain unchanged.
