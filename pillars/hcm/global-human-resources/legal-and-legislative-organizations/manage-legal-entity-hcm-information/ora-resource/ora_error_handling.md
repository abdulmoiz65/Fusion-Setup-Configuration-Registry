# Legal Entity HCM Information Error Handling

## Purpose

Own synchronization and mutation-route handoffs, sanitized failure classification, disclosure, refusal, reconciliation, and retry safety.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| LE-01 | Identity is missing or ambiguous | Input validation | Stop before synchronization and request one exact business identifier |
| LE-02 | ManageLegalEntity synchronization has not run or has no reusable verified outcome | Input validation | Reuse only a successful terminal same-session, same-identity, same-environment outcome no more than 24 hours old. Otherwise, for an explicit HCM Information detail read, prepare and approve the synchronization-only loader handoff, poll that load to terminal status, then refresh search and resume; otherwise return LE.SYNC_LOADER_READY |
| LE-03 | Synchronization fails or is uncertain | Input validation | Reconcile through fresh search and root reads; do not invoke the action again automatically |
| LE-04 | Applicable root, CategoryCode, EFF link, context definition, value set, or history is absent or ambiguous | Catalog mismatch | Stop with the owning resolver and exact safe next action; a valid zero-row View context is not an absent context |
| LE-05 | Describe-backed context collection is empty during View | Catalog mismatch | Treat it as valid empty configuration and show supported segments as Not configured |
| LE-06 | Loader object is unregistered | Catalog mismatch | Classify as catalog mismatch and make no loader handoff |
| LE-07 | UCM template, component metadata, or requested action contract is unavailable | Catalog mismatch | Stop before preview; do not infer parity from another object and do not use direct REST mutation |
| LE-08 | An EFF root locator is missing; the FLEX value is the literal flexfield identifier instead of the row's resolved context code; a child uses the wrong PATCH/POST or `effectiveOf` contract; an existing child changes or omits its current OrgInformationId, EffectiveStartDate, or EffectiveEndDate; or a correction/update action does not match the affected top-level organization's current EffectiveStartDate | Input validation | Stop before preview and rebuild every affected DAT member with exact live EFF controls and root locators. An existing child requires PATCH and its current OrgInformationId, EffectiveStartDate, and EffectiveEndDate. A new POST child leaves all three child fields blank and, in a dated-update branch, requires `RangeStartDate=YYYY-MM-DD` without RangeMode. For correction, require `RangeMode=CORRECTION;RangeStartDate=YYYY-MM-DD`, blank action dummyId and OrgInformationId, `RestAction=invoke`, ISO StartDate, and resolved OrganizationId. For split, re-read the current template and supply every required action field, including ISO effectiveStartDate and organizationId when required |
| LE-09 | Parent-delete source uses an EFF object, omits a required DeleteOrganizationUnitForDTDelete field, contains EFF/root locator fields or action sections, or duplicates the same organization/history-start pair | Catalog mismatch | Stop before preview and rebuild one DeleteOrganizationUnitForDTDelete row from the synchronized OrganizationId and selected complete-history start |
| LE-10 | Source or immutable artifact changes | Artifact persistence | Invalidate validation and approval and restart the Core Data Loader cycle |
| LE-11 | Authentication returns 401 or 403 | Authentication | Refresh cached authentication once when eligible, repeat only the safe read, and stop after a second auth response |
| LE-12 | Transport fails during a read | Transport/environment | Retry only when the failure is known recoverable and no mutation was attempted |
| LE-13 | Upload or initiation fails | Input validation | Report completed side effects and identifiers needed for status/recovery; do not retry or delete uploaded content automatically |
| LE-14 | Loader processing times out | Process timeout | Report environment, operation, request/process identifier, last status, elapsed wait, and next status-check path |
| LE-15 | Loader process fails or partially succeeds | Process failed | Preserve every verified effect and error; never label partial work complete or replay automatically |
| LE-16 | Loader outcome is uncertain | Input validation | Reconcile through safe reads/status, remain blocked, and require a rebuilt artifact plus renewed approval for any retry |
| LE-17 | Post-load verification fails | Process failed | Return FAILED with the changed and unverified business effects; do not fall back to REST |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required identity, operation, branch, date, context, value, or row selection is missing or invalid | Correct the named input and resume the preserved stage |
| Catalog mismatch | Configured object, live registration, template, section, or action contract does not match | Refresh the loader contract and source before retrying validation |
| Auth/authz | Authentication or required REST/Data Loader privilege fails | Correct access; retry only the failed read unless a new mutation request and approval are required |
| Transport/environment | Host, callback, network, timeout, or environment identity fails | Correct the environment and repeat only safe preflight work |
| Fusion API | A declared read returns a business/API failure | Preserve sanitized evidence and retry only when eligible |
| Process failed or timeout | The ManageLegalEntity synchronization load fails, partially succeeds, times out, or is uncertain | Preserve loader diagnostics and reconcile through fresh reads; do not resubmit automatically |
| Approval blocker | Core Data Loader's current immutable preview is not approved or is stale | Obtain approval through Core Data Loader after revalidation |
| Process timeout | The automatic detail-read synchronization poll does not reach a terminal result within the polling contract | Use the recorded request identifier for a later explicit status check; do not resubmit automatically |
| Process failed | Loader validation, import, or load reports failure or partial results | Review diagnostics; do not replay automatically |
| Artifact persistence | A required project artifact cannot be safely registered or saved | Preserve external state and retry persistence only after resolving the path/conflict |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Synchronization loader handoff | Business identity, safe environment alias, ManageLegalEntity, and that this synchronization-only approval does not authorize another mutation |
| Loader handoff | Selected business objects, business-facing requested changes, effective boundary, and unresolved contract blockers |
| Failure | Failure class, stage, safe environment alias, sanitized server/process message, completed side effects, retry safety, and one recommended action |
| Timeout | Request/process identifier, last status, elapsed wait, and next-check path |
| Partial or uncertain result | Every verified effect, every failed or unknown effect, and explicit no-replay guidance |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous business identity | Do not synchronize, resolve roots, or prepare a loader mutation |
| Unsupported parent/classification request | Do not reinterpret it as an EFF change |
| Missing loader contract | Do not copy ModifyOrganizationUnitForChildCorrect, SplitOrganizationUnitForEFFUpdate, or any action layout from another object |
| Mutation requested | Do not use REST batch, PATCH, PUT, DELETE, splitOrganizationUnitForEFFUpdate, or invoke deleteOrganizationUnitForDTDelete directly; its registered loader business object is permitted only for eligible parent deletion |
| Loader approval is absent or stale | Do not upload or initiate |
| Loader failure or uncertainty | Do not retry, switch transport, or claim success |
| Physical or complete deletion | Do not route through this task |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.SYNC_GATE | decision | 3 | execution_gate | required->LE.SYNC_LOADER_READY;completed->LE.ROOTS;failed->LE.ERROR;uncertain->LE.ERROR | LE.SEARCH | stop | One exact Legal Entity is selected and current synchronization readiness must be resolved |
| LE.SYNC_LOADER_READY | terminal | 4 | terminal | none | LE.SYNC_GATE | continue | A synchronization-only ManageLegalEntity archive is ready for Core Data Loader; after successful completion, refresh search and resume the original request |
| LE.ROUTE | decision | 13 | execution_gate | read->LE.DONE;mutation->LE.LOADER_READY;import->LE.LOADER_READY;unsupported->LE.BLOCKED;failed->LE.ERROR | LE.DESIGN | stop | Select a terminal read result or Core Data Loader handoff without executing a business-data mutation here |
| LE.ERROR | step | 14 | error_handler | reconciled->LE.BLOCKED;failed->LE.BLOCKED | none | stop | A validation, lookup, synchronization, metadata, loader-readiness, process, persistence, approval, or verification gate fails |
| LE.DONE | terminal | 15 | terminal | none | LE.ROUTE | continue | The requested read completed and verification passed |
| LE.EXPORT_DONE | terminal | 16 | terminal | none | LE.VALIDATE | continue | Explicit task-level export routing is selected |
| LE.LOADER_READY | terminal | 17 | terminal | none | LE.ROUTE | continue | A supported mutation or import is fully mapped to legalEmployersEFF, payrollStatutoryUnitsEFF, both EFF objects, or DeleteOrganizationUnitForDTDelete as appropriate and is ready for Core Data Loader |
| LE.BLOCKED | terminal | 18 | terminal | none | none | stop | The request is blocked with sanitized diagnostics and one resume action |
