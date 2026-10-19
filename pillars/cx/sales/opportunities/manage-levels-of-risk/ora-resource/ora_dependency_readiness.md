# Manage Levels of Risk Dependency Readiness

Treat reference-set assignment as a read-only prerequisite. This task does not
create or update record-set assignments.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Reference data set | For SingleLookup, resolve one exact SetId and SetCode; Package Export has no set selector, while Package mutation or Import validates the set on every changed MOO_SETID_RISK_LEVEL row |
| 2 | Record-set assignment | For SingleLookup or a changed package row with a business unit, confirm the assignment under the parent-returned ReferenceGroupName; Package Export has no assignment prerequisite |
| 3 | Lookup state | Resolve SingleLookup state directly; defer package-row state locks to atomic package verification and require no code state for full-task Export |

## Dependency Rules

For a SingleLookup request, require the exact parent-returned ReferenceGroupName,
one set, and any explicitly requested business-unit assignment. For Package
mode, validate those same conditions independently for every changed row in the
immutable ZIP; do not force the package to one set or one code.

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| manage_levels_of_risk_record_set | ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES | Yes | RequestMode=SingleLookup | Lookup | Read-only Apps Common set and business-unit assignment responses | resolve_risk_reference_set | Level of Risk codes are set enabled and must remain scoped to one resolved reference data set | Ask whether Common Set should be used; otherwise require one exact set selector. When selecting by business unit, complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES first if its assignment is absent | SetSelectionDecision, SetId, SetCode, BUOrgId when supplied, and prerequisite status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | SingleLookup resolves one exact set and any requested assignment | Yes |
| Not applicable | RequestMode is Package; full-task Export has no selector, while package mutation or Import defers per-row set and assignment checks to package verification | Yes |
| Lookup | The read-only resolver must determine the exact set or requested assignment | Yes |
| Blocked | The set is ambiguous or the requested assignment is absent or incorrect | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.RISK.DEPENDENCY | step | 4 | resolve_dependency | satisfied->OPP.RISK.RESOLVE_STATE;not_applicable->OPP.RISK.RESOLVE_STATE;missing->OPP.RISK.RETURN_MISSING;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.RESOLVE_SET | stop | Verify the explicit Common-versus-different decision, returned reference group, exact set, and any BU assignment for SingleLookup; never infer Common Set. Package mode defers the same checks for every changed row to package verification |
