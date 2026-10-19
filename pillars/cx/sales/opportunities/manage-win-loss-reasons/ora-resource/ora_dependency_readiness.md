# Manage Win/Loss Reasons Dependency Readiness

Treat reference-set assignment as a read-only prerequisite. This task does not
create or update record-set assignments.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Route eligibility and task identities | Keep MOO_MANAGE_WIN/LOSS_REASONS as catalog identity and FND_MANAGE_SET_ENABLED_LOOKUPS as FSM export/import identity. A classified failed, timed-out, or unusable exact-target export routes the existing Create, Update, or Disable intent to direct Apps Common REST before any upload/import/mutation; retain its receipt and never use the slash-containing catalog code for transport |
| 2 | Reference data set | For SingleLookup, resolve one exact SetId and SetCode; Package Export has no set selector, while Package mutation or Import validates the set on every changed MOO_SETID_WIN_LOSS_REASON row |
| 3 | Record-set assignment | For SingleLookup or a changed package row with a business unit, confirm the assignment under the parent-returned ReferenceGroupName; Package Export has no assignment prerequisite |
| 4 | Lookup state and REST readiness | Resolve SingleLookup state directly and defer FSM package-row state locks to package verification. Direct REST fallback reads every exact requested row afresh; only completed lookup omission also requires complete nonempty existing inventory. No registered loader lookup or capability check is required |

## Dependency Rules

For a SingleLookup request, require the exact parent-returned ReferenceGroupName,
one set, and any explicitly requested business-unit assignment. For Package
mode, validate those same conditions independently for every changed row in the
immutable ZIP; do not force the package to one set or one code.

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| manage_win_loss_reasons_fsm_transport | FND_MANAGE_SET_ENABLED_LOOKUPS export/import route | Yes | Package Export, Import, or ExecutionRoute=FSM for Create, Update, or Disable | Verify | Exact setup-task identity and either a usable same-target baseline or classified export-unavailability receipt; final package/context only for native FSM handoff | verify_win_loss_reason_fsm_package | MOO_MANAGE_WIN/LOSS_REASONS contains `/` and is not used as transport identity; native package changes remain scoped to the fixed lookup | Attempt the complete FND data export. For Create/Update/Disable, an unavailable/unusable exact-target receipt continues as fallback_candidate without final ZIP or Data Loader context; usable native packages retain exact context and unrelated-row preservation. Export/Import stay FSM-only | CatalogTaskCode, CatalogTaskName, ExecutionTaskCode, ExecutionTaskName, LookupType, usable-baseline identity/preservation or classified unavailability receipt |
| manage_win_loss_reasons_rest_fallback | Same-target FND export failure, timeout, or unusable baseline | Yes | ExecutionRoute=REST_FALLBACK for Create, Update, or Disable | Verify | Sanitized exact-target export-attempt receipt with classified reason and defect; fresh REST reads as defined by the verifier | verify_win_loss_reason_fsm_package | The unusable FSM baseline selects direct Apps Common REST; native FSM Data Loader task context and approval do not apply | Continue once with unchanged intent, rows and confirmed sets. Validate the receipt and then fresh parent, set and requested-row state; completed omission also requires complete nonempty selected-set inventory. Show and separately approve the exact REST preview | RestFallbackEligible, FsmExportUnavailableReason, request fingerprint, ProcessId/requestId when available, actual last status, environment, release, timestamp, defect and fresh-read evidence references |
| manage_win_loss_reasons_record_set | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES | Yes | RequestMode=SingleLookup or ExecutionRoute=REST_FALLBACK | Lookup | Read-only Apps Common set and business-unit assignment responses | resolve_win_loss_reason_reference_set | Win/Loss Reason codes are set enabled and every direct REST row must remain scoped to one resolved reference data set | Ask whether Common Set should be used; otherwise require one exact set selector per distinct REST row. When selecting by business unit, complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES first if its assignment is absent | Per-row SetSelectionDecision, SetId, SetCode, BUOrgId when supplied, and prerequisite status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verified | Catalog and execution task identities are fixed, the package is a fresh complete FND_MANAGE_SET_ENABLED_LOOKUPS export, and only reviewed MOO_SETID_WIN_LOSS_REASON rows change | Yes |
| REST fallback candidate | An exact-target export receipt for EXPORT_REQUEST_FAILED, PROCESS_FAILED, PROCESS_TIMEOUT, COMPLETED_LOOKUP_OMISSION, or COMPLETED_UNUSABLE_EXPORT validates, but required fresh REST reads have not completed | Lookup only; no mutation preview or write |
| REST fallback eligible | The classified same-target unavailability receipt and all applicable fresh REST reads validate | Yes, subject to direct REST editability, privilege, impact, and exact-preview approval gates |
| Satisfied | SingleLookup resolves one exact set and any requested assignment | Yes |
| Not applicable | FSM Package mode; full-task Export has no selector, while FSM package mutation or Import defers per-row set and assignment checks to package verification | Yes |
| Lookup | The read-only resolver must determine the exact set or requested assignment | Yes |
| Blocked | The set is ambiguous or the requested assignment is absent or incorrect | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.WIN_LOSS.DEPENDENCY | step | 4 | resolve_dependency | satisfied->OPP.WIN_LOSS.RESOLVE_STATE;fallback_eligible->OPP.WIN_LOSS.RESOLVE_STATE;fallback_candidate->OPP.WIN_LOSS.RESOLVE_STATE;not_applicable->OPP.WIN_LOSS.RESOLVE_STATE;missing->OPP.WIN_LOSS.RETURN_MISSING;failed->OPP.WIN_LOSS.RETURN_FAILED | OPP.WIN_LOSS.RESOLVE_SET | stop | Preserve the exact catalog/FND identities. For FSM mutation preparation, a classified export-unavailability receipt may continue as fallback_candidate without a final ZIP or Data Loader context. REST_FALLBACK receipts remain candidates until fresh requested-row reads and, for completed lookup omission, nonempty inventory confirmation. Verify exact explicit sets and returned reference group/BU assignments; never infer Common Set or query loader capability |
