# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect identity/dates | One exact work type and valid availability |
| 2 | Validate semantics | Billable/utilizable/transfer behavior supplied or documented-defaulted and resolved |
| 3 | Validate sets/children | Validate supplied or explicitly changed assignments only; complete supported checks and disclose unresolved DFF/eligibility checks |
| 4 | Protect profile/use | Downstream and transaction-date impact safe |
| 5 | Protect package/approval | Exact FSM diff bound to the final immutable archive; complete Task Hook validation before preview; Data Loader requires approval and matching envelopes before submission |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create/update | Blocker | find_work_type | Duplicate/ambiguous identity or bad dates | Correct identity/dates | Yes |
| Existing identity with billable/utilizable/transfer, availability-date or set-assignment changes | Blocker | resolve_work_type_use | Required impact handoff is not satisfied, or validated facts show unsafe backdated, consumer, transaction-date or profile impact | Resolve the workflow gap and obtain valid impact evidence before import; correct the unsafe change; missing evidence cannot become a warning or be cleared by execution approval | Yes |
| Sets | Blocker | resolve_work_type_sets | Duplicate assignment or unsafe consumer impact in the proposed diff; membership comes from the set resolver, with no invented set-active-date filter | Omission on create is not a blocker; validate explicit assignment changes; evaluate consumers through resolve_work_type_use | Yes |
| Translations/DFF | Blocker | resolve_work_type_children | Proven invalid language, known unwritable/incompatible segment, actual ambiguity or missing representation preventing construction; absent metadata alone is not a blocker | Correct proven errors; preserve supplied proven representation | Yes |
| Translation rows supplied | Blocker | resolve_work_type_children | Child resolver reports a translated-name collision or incomplete required name-collision check | Correct the conflicting name or restore required collision evidence through the selected workflow before preview; optional reference warnings and upload approval cannot clear this gate | Yes |
| Missing supported DFF/reference membership authority or unverified UI/import parity | Warning |  | None for these reference checks; blocking=false; required consumer-impact handoff and translation-name collision evidence are excluded from this warning policy | Disclose skipped reference checks and next evidence; continue remaining supported checks only when required dependencies are satisfied | No |
| Delete/direct REST | Blocker |  | No supported setup contract | Use end-date/FSM | No |
| Import preparation | Blocker | verify_work_type_package | Prepared package contract invalid or inconsistent with the verified Data Loader preflight | Correct the package and repeat preflight/task validation before preview; Data Loader checks approval only at its later submission gate | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_work_type | Create/update | Stable identity/baseline | ora_reference_lookups.md |
| resolve_work_type_sets | Set supplied or explicitly changed | Canonical set codes and display evidence; assignment count from baseline and proposed diff | ora_reference_lookups.md |
| resolve_work_type_children | Translation/DFF | Language/segment results and completed translated-name collision result when translation rows are supplied | ora_reference_lookups.md |
| resolve_work_type_use | Existing identity with an actual flag/transfer, availability-date or set-assignment diff | satisfied handoff and validated impact facts | ora_reference_lookups.md |
| verify_work_type_package | Import | Exact prepared package contract and internal archive/preflight integrity binding | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WTYPE.ENFORCE_DESIGN | decision | 7 | design_enforcement | pass->WTYPE.EXECUTION_GATE;warning->WTYPE.EXECUTION_GATE;blocked->WTYPE.RETURN_REFUSAL;failure->WTYPE.RETURN_ISSUES | WTYPE.RESOLVE_DEPENDENCIES | stop | Before import approval; block unsatisfied required consumer-impact evidence and unsafe impact; optional reference warnings never waive this gate |
