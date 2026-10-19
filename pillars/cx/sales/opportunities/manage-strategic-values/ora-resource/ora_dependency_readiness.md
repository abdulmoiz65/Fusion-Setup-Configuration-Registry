# Manage Strategic Values Dependency Readiness

Treat reference-set assignment as a read-only prerequisite. This task does not
create or update record-set assignments.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Reference data set | For SingleLookup or every Package REST_FALLBACK row, resolve the exact SetId and SetCode; Package Export has no selector and native FSM Package validates per-row sets during package verification |
| 2 | Record-set assignment | For SingleLookup or every changed row with a business unit, confirm the assignment under the parent-returned ReferenceGroupName; REST_FALLBACK resolves each applicable assignment live and Export has no assignment prerequisite |
| 3 | Lookup state | Resolve SingleLookup or every distinct Package REST_FALLBACK code/set pair directly; native FSM Package defers row state locks to atomic package verification and full-task Export requires no code state |

## Dependency Rules

For a SingleLookup request, require the exact parent-returned ReferenceGroupName,
one set, and any explicitly requested business-unit assignment. For Package
mode, validate those same conditions independently for every changed row in the
immutable ZIP or reviewed REST_FALLBACK row list; do not force it to one set or
one code. Final fallback never repairs a missing assignment or changes a set.

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| manage_strategic_values_record_set | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES | Yes | RequestMode=SingleLookup or Package REST_FALLBACK | Lookup | Read-only Apps Common set and business-unit assignment responses | resolve_strategic_value_reference_set | Strategic Value codes are set enabled and each reviewed code must retain its confirmed reference data set | Ask whether Common Set should be used; otherwise require one exact set selector per row. When selecting by business unit, complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES first if its assignment is absent | SetSelectionDecision, SetId, SetCode, BUOrgId when supplied, and prerequisite status per row |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | SingleLookup or every Package REST_FALLBACK row resolves its exact set and requested assignment | Yes |
| Not applicable | Native FSM Package only; full-task Export has no selector and FSM package mutation or Import defers per-row set/assignment checks to package verification | Yes |
| Lookup | The read-only resolver must determine the exact set or requested assignment | Yes |
| Blocked | The set is ambiguous or the requested assignment is absent or incorrect | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.STRATEGIC.DEPENDENCY | step | 4 | resolve_dependency | satisfied->OPP.STRATEGIC.RESOLVE_STATE;not_applicable->OPP.STRATEGIC.RESOLVE_STATE;missing->OPP.STRATEGIC.RETURN_MISSING;failed->OPP.STRATEGIC.RETURN_FAILED | OPP.STRATEGIC.RESOLVE_SET | stop | Verify explicit set decisions, returned reference group, exact sets and requested assignments for SingleLookup or every Package REST_FALLBACK row; never infer Common Set. Only native FSM Package defers per-row checks to package verification |
