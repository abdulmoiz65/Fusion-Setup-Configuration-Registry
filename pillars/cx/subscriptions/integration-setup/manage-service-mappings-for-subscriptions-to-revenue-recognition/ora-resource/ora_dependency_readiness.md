# Subscription to RMCS Service Mapping Dependency Readiness

## Scope

Checks phase-specific evidence dependencies for the assisted checkpoint. Lookup mechanics remain in [reference lookups](ora_reference_lookups.md). This is not cross-task sequencing and does not require Subscription activation, Financials setup or integration testing before supported local source analysis.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current request and input contract | Resolve the exact current pair and applicable phase |
| 2 | Source-analysis evidence | Check question, source records and evidence states for analysis or handoff |
| 3 | Handoff contribution | Check structured result and applicable source-owned final-row contribution |
| 4 | Status boundary | Keep local evidence, source choice, proposed exposure and publication claims separate |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RMCSSM.DEP.CONTRACT | Current-pair preflight and checkpoint identity | Yes | Every phase | Verify | Current-request local evidence from the canonical lookup | resolve_rmcs_service_mapping_contract | An unrelated or stale export cannot support this checkpoint | Supply current inputs and correct the reported preflight gap | Preflight result and current input references |
| RMCSSM.DEP.BINDINGS | Source question and available binding evidence | Conditional | phase analysis or handoff | Verify | Current source records and local evidence from the canonical lookup | resolve_rmcs_mapping_bindings | Source meaning, provider/access and decision states must be represented accurately | Preserve pending choices and missing exposure as specific outcomes | Source records, evidence states and remaining questions |
| RMCSSM.DEP.HANDOFF | Structured mapping result | Conditional | phase handoff | Verify | Current handoff and primary-supplied rows from the canonical lookup | verify_rmcs_mapping_handoff | Caller needs complete source facts or exact unresolved items | Return canonical outcome and source-owned contribution without invented algorithm facts | Handoff findings and unresolved items |
| RMCSSM.DEP.CONFIGURATION | Evidence for claimed completed new source exposure | Conditional | A result claims a previously proposed source is now exposed | Verify | Refreshed source evidence in the local binding record | resolve_rmcs_mapping_bindings | Proposal acceptance alone does not create exposure | Supply refreshed evidence or retain the proposed-state prerequisite | Current versus proposed exposure/access status |
| RMCSSM.DEP.PUBLICATION | Evidence for a publication claim | Conditional | phase handoff and result claims published or deployed configuration | Verify | Explicit publication evidence in the handoff record | verify_rmcs_mapping_handoff | Local analysis authority is not Fusion publication proof | Keep publication unverified unless supported; no new live read is selected here | Proven or unverified publication status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Checkpoint inputs satisfied | Applicable phase input and evidence records exist | Applicable documented local lookups only; never a create |
| Decision pending | Newly recommended source awaits acceptance | Return needs_decision; no automatic selection |
| Prerequisite pending | Chosen source lacks required exposure/access or a claim lacks evidence | Return affected prerequisite; unrelated supported local analysis may continue |
| Handoff complete with unresolved outcome | Record accurately supplies pending, blocked or declined status and next action | Return that outcome; record completeness is not configuration readiness |
| Unsupported future operation | Mutation, publication, setup verification or result acquisition lacks its separate contract | No substitute route; retain [unsupported live contracts](ora_reference_lookups.md#unsupported-live-contracts) |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSSM.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | ready->RMCSSM.ENFORCE_DESIGN;blocked->RMCSSM.REPORT_ISSUES | RMCSSM.RESOLVE_EVIDENCE | stop | Check current-phase record dependencies after local resolution or optional describe; pending business decisions are structured outcomes, not publication success. |
