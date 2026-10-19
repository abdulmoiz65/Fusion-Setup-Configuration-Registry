# Costing of Elements HDL Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identity | Complete shared Search without changing requested_operation. |
| 2 | Operation scope | Evaluate complete history/detail using the bounded contracts below. |
| 3 | Account design | For Create/Update/Correct apply the relevant subtype, representation and value rules. End Date changes only dates, preserving accounts and CostInfo options from the baseline. |
| 4 | Prepare | Resolve applicable values/templates and render source. The explicit artifact-only branch returns its locally checked ZIP; submission requires full validation and Task Hook. |
| 5 | Handoff | core.data-loader owns the single approval and submission; do not replay the HAR batch. |

## Operation Contracts

| Operation | Supported behavior | Boundary |
|---|---|---|
| Create | New EL allocation, EL CostInfo and selected LIV CostInfo rows, plus requested COST/BAL/OVRRIDE accounts. Require Search CostingExists=N, empty complete allocation history and empty detail at the requested start. | A future or historical allocation blocks Create too; no overwrite or automatic Update. Search proves eligibility at the requested as-of date. Require end on/after start; do not infer the semantic owner of numbered Search date fields. Enforce additional eligibility bounds only when current metadata identifies them. |
| Update | New dated snapshot within the latest existing allocation interval: its start must be strictly after that interval's start and no later than its end. Carry forward all existing accounts and EL/LIV values; apply only explicit changes. Use the observed end, not a new open-ended default, for the allocation and each aligned CostInfo row. | Require complete history and baseline, with touched EL/LIV intervals aligned to that parent. No insertion before a later interval, account removal, new input identity, eligibility change, or clearing that invalidates baseline identity. Adding a COST/BAL role is allowed only when that subtype is proven absent. Existing priority rows require an explicit stable selection/order; response order is not priority. |
| Correct | In-place changes to selected existing EL CostableType,TransferToGlFlag,DistributionSetName or existing LIV CostedFlag. Resolve each CostInfoId and preserve its exact start/end. MERGE with the unchanged date interval corrects it instead of creating an Update split. | Restricted to the latest aligned interval. Do not move dates, add/remove input records or correct accounts. Account deltas are mapped/readable but their HDL in-place correction contract is not established by these HARs. Report unsupported scope before preview. |
| End Date | Always close the complete eligibility costing: CostAllocationV3 EL, CostInfoV3 EL and all existing CostInfoV3 LIV records for the selected interval, to the same requested inclusive end. Set end_date_scope=complete_costing; the target set includes all three component types without requiring the user to name them separately. | Apply the End Date Scope rules below. Account, flag, type, group and input changes are unsupported in this operation. New allocation-only, CostInfo-only or selected-LIV-only scopes are unsupported; do not silently narrow the closure. |
| Zap | Delete the selected logical costing allocation's complete history, all historical accounts and every associated EL/LIV CostInfo through explicit HDL DELETE rows. The start date selects the record; it does not limit deletion to one interval. | Apply Zap Scope and Handoff below. Preserve the element, eligibility, LDG and unrelated costing. No Delete (ED Split), account-only or CostInfo-only deletion is introduced. |

The Update/Correct date rules apply Oracle's
[date-effective maintenance contract](https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/overview-of-loading-date-effective-objects.html)
and [same-start correction behavior](https://docs.oracle.com/en/cloud/saas/tutorial-hdl-date-effective-updates/).
The HARs demonstrate Create and reads, not an executed HDL Update/Correct;
these bounded contracts still require current loader schema validation.

The End Date allocation mapping follows the developer-selected
[costing-of-departments contract](../../costing-of-departments/ora-resource/ora_input_validation.md)
and its [schema boundary](../../costing-of-departments/ora-resource/ora_design_enforcement.md).
Adapt ORG/DepartmentName to EL/ElementEligibilityName/ElementCode using this
task's existing identity mapping. The EL/LIV mapping combines the existing
identity mappings with the CostInfo end-date pattern in
[costing-of-payment-sources](../../costing-of-payment-sources/ora-resource/ora_input_validation.md)
and Oracle's [special date attribute contract](https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/examples-of-changing-first-effective-start-date-and-last.html).
The developer's manual-load tests verified the allocation and EL/LIV closures
separately. The requested contract now includes all three; no cascade is assumed.
Those results do not bypass current component/schema or shared-loader validation.

## End Date Scope

| Situation | What Happens |
|---|---|
| Target interval | The explicit start must match exactly one latest allocation history row. Require start <= requested end <= current allocation end; reject later splits or extension. Resolve one EL CostInfo and at least one existing LIV CostInfo from the complete baseline. Every targeted CostInfo must retain the supplied start and the same physical identity at the requested end, with an end of 4712/12/31 or the requested date. Other independent intervals are outside this bounded contract; stop rather than omit them or change their starts. |
| Complete target set | Include every existing LIV CostInfo in the selected interval, regardless of CostedFlag. Missing EL/LIV, duplicate names/keys or incomplete child evidence blocks preparation. Preserve all accounts, flags, type, group, input names and earlier intervals. Existing detail supplies the values; End Date never creates a missing component. |
| Change set and no-op | Compare each target's end separately. Include only targets whose ends exceed the requested date in the change set; retain targets already at that date in the expected result. A closed allocation alone is not a no-op. Return unchanged only when the complete target set already ends at the requested date. Fresh evidence of a partial prior closure may produce a smaller archive, but the final verification still covers all three component types. |
| Recovery boundary | An earlier failed or uncertain load is reconciled through the status/verification branch first. Do not automatically replay or repair it. A new explicit End Date request uses fresh evidence and its own archive validation and approval, or the explicit artifact-only handoff. |

## Zap Scope and Handoff

The user-selected [department](../../costing-of-departments/ora-resource/ora_input_validation.md)
and [payroll](../../costing-of-payrolls/ora-resource/ora_input_validation.md)
contracts supply full-history allocation and physical-account deletion.
[Payment sources](../../costing-of-payment-sources/ora-resource/ora_input_validation.md)
adds explicit CostInfo deletion and component-level verification. Adapt their
identities to this task's canonical EL/LIV mappings. The element DELETE key
forms are extrapolated contracts requiring current loader validation; a
successful PM load is not an executed EL/LIV Zap test.

| Situation | What Happens |
|---|---|
| Logical scope | Require one exact history start selecting one CostAllocationId, then include all that ID's earlier, selected and later intervals, including already end-dated records. Require the allocation user-key/date DELETE to address only that logical allocation. Multiple logical matches, a conflicting selector or a request to delete only one split is unsupported; never broaden it into another eligibility or unrelated allocation. |
| Component coverage | Require complete historical allocation, account and EL/LIV evidence using Zap History and Detail. Explicitly delete the allocation, every EL/LIV CostInfo ID and every physical account. A proven empty account set permits omitting only that member; an empty LIV set in a complete historical expansion adds no invented input. No cascade is assumed between business objects. Missing, misaligned, shared or ambiguous targets block the whole operation. |
| Identity-only scope | Zap skips costing-type, distribution-group, input-value LOV, KFF and segment validation. Existing input names and physical identities come from detail. Account-value validation failures must not be imported from Create/Update rules into deletion. Do not delete element or eligibility setup objects. |
| Runtime DELETE contract | Require current core.data-loader validation of all included components, EL/LIV key forms and cross-object dependency processing. A listed attribute or a PM-specific successful key does not prove element DELETE support. Do not infer processing order or atomicity from ZIP member order. Rejected keys or missing capability evidence block before upload; no trial live keys, REST writes or component omission. |
| Preparation and preview | For execution, finish the immutable ZIP, source/schema checks, persisted loader preflight, task-specific Task Hook preview and preapproval freshness before the single core.data-loader approval. Show the target environment, eligibility/LDG, full date span, interval count and per-component DELETE counts. The approval must cover the whole history and every account/EL/LIV target; no separate pillar confirmation. |
| Validation-only | An explicit prepare/validate-only request finishes with validated deliverables and no upload or approval prompt. It still requires the full DELETE contract; it cannot use the End Date special-attribute artifact-only exception. Later execution requires current preparation, loader preflight and its own exact-artifact approval. |
| Approval resume | A contextual approval restores COE.ZAP.GATE with saved completed preparation and freshness evidence. Use the loader's Task Hook approval and approved-archive verification against exact bytes and bound environment/Run Book; preserve its returned taskValidationEnvelope. Do not rediscover identities or rebuild the archive on intact approval. Changed or missing control artifacts invalidate approval and require new preparation. |
| Accepted submission | Submit once through core.data-loader, bind the actual accepted identifiers to the archive/baseline and return pending without polling. Explicit status/verification enters the dedicated Zap result branch. An earlier Create/End Date approval or job cannot authorize or prove a Zap. |
| Partial result | Successful parent deletion with failed CostInfo or accounts is partial failure. Preserve outcomes and stop for supported reconciliation; do not automatically replay the archive, reuse old approval or transplant payment-source orphan-recovery calls into this task. |

## Account and Change Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| End Date schema boundary | Blocker | | ReplaceLastEffectiveEndDate is removed because ordinary metadata omits it, or a wrapper rejection is treated as validation success. | Keep the special attribute; the department source identifies Component Details, Date Effectivity as the capability authority. Ordinary omission alone is not evidence of unsupported capability. Any explicit capability conflict blocks preparation; wrapper rejection blocks upload. Do not patch the shared validator or substitute SET. | No |
| Create/Update Cost Account | Blocker | | More than one COST row or any Proportion other than 1. | Use one partial segment account when requested. | Yes |
| Create/Update Offset Account | Blocker | | More than one BAL row or any Proportion other than 1. | Use one partial segment account when requested. | Yes |
| Create/Update Priority Cost Accounts | Blocker | resolve_element_priority_account | Sum of normalized OVRRIDE fractions exceeds 1, full account is unresolved, or Segment columns are populated. | Allow a total below or equal to 1; use ConcatenatedSegment only. COST/BAL are not included in this total. | Yes |
| Create/Update/Correct Distributed costing | Blocker | resolve_element_distribution_group | Effective type is D without a valid distribution group. | Resolve the required group in this LDG. Do not apply a captured group as a default. | Yes |
| Create/Update/Correct other costing types | Blocker | | An incompatible distribution group would be introduced or left after changing away from D. | Require an explicit compatible change/clear; do not silently discard data. | Yes |
| Create/Update supplied accounts | Blocker | resolve_element_costing_kff | Account labels, structure, values or date validity are unproven. | Use the declared runtime resolvers for the effective date. Optional COST/BAL segments may remain absent. | Yes |
| Update preservation | Blocker | read_element_costing_record | A requested delta lacks a unique baseline target, an unrequested value is dropped, or retained account data is incomplete. | COST/BAL select by unique subtype; OVRRIDE requires stable row identity/old full account and unambiguous priority order. Preserve unedited values. | No |
| Input replacement | Blocker | | Request implicitly disables other costed inputs or creates a new LIV during Update/Correct. | Treat named changes independently; require an explicit supported change for each existing input. New inputs are supported in Create only. | No |
| Source route | Blocker | | Batch/REST costing writes, arbitrary actions or an import outside core.data-loader. | Use declared lookups and the immutable HDL workflow. | No |
| Progress | Blocker | | Lookup, defaults, rendering or validation success is treated as an intermediate approval pause except for the explicitly requested End Date artifact-only terminal. | Continue to exact-archive preview, stopping only for missing input, actual failure or the loader approval gate. | Yes |
| Approval integrity | Blocker | | Context, evidence or archive differs from its retained preflight. | Reprepare before requesting approval. Later approval verifies retained bytes; it does not rerender or repeat identity discovery. End Date also follows its declared read-only state recheck; unchanged facts preserve approval, changed facts invalidate it. | Yes |

## Verification Contract

| Situation | What Happens |
|---|---|
| Accepted initiation | Report pending with saved loader identifiers. It is not completed costing. Follow core.data-loader's status workflow only when requested; do not automatically poll after initiation. |
| Terminal successful load and requested verification | Reuse history/detail resolvers to compare all submitted objects. Compare cost type, flags, selected LIV names/flags, accounts, subtype counts and normalized fractions against the immutable expected result. |
| Update verification | New interval starts at requested date; prior interval ends the day before; previous accounts/options and unrelated history remain unchanged. |
| End Date verification | The dedicated result branch must first establish terminal success for the bound archive and retain end_date_scope, complete target set and submitted change set. COE.END_DATE.VERIFY applies End Date Read Comparisons in ora_reference_lookups.md. Complete costing closure requires explicit end-date evidence for the allocation, EL and every baseline LIV, including targets omitted from the archive because already closed. |
| Zap verification | COE.ZAP.RESULT requires terminal successful DELETE outcomes for every submitted target before COE.ZAP.VERIFY applies Zap Verification in ora_reference_lookups.md. Confirm complete historical removal, preserved eligibility and unrelated data. Disclose the independent CostInfo read-back limit; an absent parent alone is insufficient. |
| Correct verification | Same intervals and IDs, only requested EL/LIV attributes changed; accounts and other inputs remain unchanged. |
| Mismatch/partial success | Report unverified or partial result and stop. Do not replay a load to repair it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COE.SEARCH.ENFORCE_ROUTE | decision | 7 | design_enforcement | ready->COE.SEARCH.FETCH;blocked->COE.HDL.HANDLE_ERROR | COE.SEARCH.CHECK_DEPENDENCIES | stop | Shared Search uses its two public GET contracts; LDG-text branch must have resolved its LDG. |
| COE.IDENTITY.CHECK_OPERATION | decision | 12 | design_enforcement | supported->COE.HDL.VALIDATE_INPUT;zap->COE.ZAP.VALIDATE_INPUT;unsupported->COE.OPERATION.UNSUPPORTED;blocked->COE.HDL.HANDLE_ERROR | COE.IDENTITY.SELECT | stop | Create requires explicit N; Update/Correct/End Date explicit Y. Explicit Zap uses the dedicated branch after unique source selection; Search's costing flag cannot replace complete historical scope or prove absence. State checks remain provisional until history/detail. |
| COE.HDL.CHECK_SCOPE | decision | 17 | design_enforcement | ready->COE.HDL.RESOLVE_VALUES;unchanged->COE.END_DATE.UNCHANGED;unsupported->COE.OPERATION.UNSUPPORTED;blocked->COE.HDL.HANDLE_ERROR | COE.HDL.RESOLVE_CONTEXT | stop | Apply Operation Contracts before value resolution. Build Update's preserved snapshot and uniquely selected deltas. End Date applies End Date Scope to build its complete target set, expected result and change set; unchanged requires every target already at the requested end. A narrowed End Date scope is unsupported; missing or conflicting component evidence is blocked. Unsupported Correct account/new-input scope has no write. |
| COE.HDL.ENFORCE_ROUTE | decision | 30 | design_enforcement | ready_create->COE.HDL.GATE_CREATE;ready_update->COE.HDL.GATE_UPDATE;ready_correct->COE.HDL.GATE_CORRECT;ready_end_date->COE.HDL.GATE_END_DATE;blocked->COE.HDL.HANDLE_ERROR | COE.HDL.VALIDATE_SOURCE | stop | Enforce final account/change rules and project prerequisites against the loader-validated immutable archive before the single approval. |
| COE.ZAP.CHECK_SCOPE | decision | 31 | design_enforcement | ready->COE.ZAP.CHECK_DEPENDENCIES;unsupported->COE.OPERATION.UNSUPPORTED;blocked->COE.HDL.HANDLE_ERROR | COE.ZAP.DETAILS | stop | Apply Zap Scope and Handoff to complete history/detail. Require full logical history, target exclusivity and explicit coverage of allocation, accounts and all existing EL/LIV; reject split-only or partial-object deletion. |
| COE.ZAP.ENFORCE | decision | 36 | design_enforcement | ready->COE.ZAP.REFRESH;blocked->COE.HDL.HANDLE_ERROR | COE.ZAP.VALIDATE_SOURCE | stop | Enforce Zap component coverage, source preservation and validated loader dependency handling. Require persisted preflight and Task Hook preview for execution; validation-only retains its distinct no-upload intent. Continue to freshness before requesting approval. |
