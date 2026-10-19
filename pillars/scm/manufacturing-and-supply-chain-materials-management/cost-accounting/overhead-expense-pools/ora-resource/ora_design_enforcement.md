# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | Resolve reference values | For Create, obtain the LookupCode and SetId. For DELETE, resolve any supplied SetName or ExpensePoolTypeCode only as a target qualifier, then resolve one exact target from the approved task-export baseline. For PATCH, resolve only a supplied ExpensePoolTypeCode; the set is immutable after Create. |
| 2 | Construct payload | For Create, construct the payload with validated ExpensePoolCode, resolved LookupCode, derived SetId, and normalized InactiveFlag only when supplied. For DELETE, use only the verified ExpensePoolCode and generated RestAction=DELETE. For PATCH, construct a delta containing only supplied, validated, normalized, or resolved fields. |
| 3 | Bind operation action | Add `RestAction=POST`, `RestAction=PATCH`, or `RestAction=DELETE` to the prepared JSON and generated source for Create, PATCH, or DELETE respectively. Verify the row action before immutable preview creation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An expense pool type meaning is supplied | Error | resolve_expense_pool_type | The fixed lookup type returns zero or multiple exact normalized Meaning matches | Do not construct a Create payload, or include this PATCH field, until the resolver returns one LookupCode. | Yes; provide a valid or more precise meaning. |
| A SetName is supplied for Create or DELETE | Error | resolve_reference_set | The verified SetName candidate query returns zero or multiple candidates, or its result fails local normalized verification | Do not construct a Create payload or qualify a DELETE target until the resolver returns one SetId. | Yes; provide a valid or more precise set name. |
| A Create payload is proposed | Error | | A required Create field is omitted; a supplied InactiveFlag is not uppercase `Y` or `N`; ExpensePoolTypeCode is not the LookupCode returned from the Meaning search; SetId or SetCode was supplied by the user; or SetId is not the SetName resolver output | When supplied, normalize the inactive term to `Y` or `N`; otherwise preserve its omission, then construct the documented payload using resolved values. | Yes; reconstruct from validated facts. |
| A PATCH payload is proposed | Error | | An omitted field is resolved or included; SetName, SetId, or SetCode is supplied; a supplied field is null or invalid; or a supplied InactiveFlag is not uppercase `Y` or `N` | Reject a set change because the set is immutable after Create. Otherwise normalize the inactive term to `Y` or `N`, then construct a delta containing only supplied, validated, normalized, or resolved mutable fields. | Yes; reconstruct the delta from supplied values. |
| A DELETE source is proposed | Error | resolve_delete_target | No exact target was resolved; ExpensePoolCode is absent; a mutable attribute or qualifier is included; or a user-supplied internal ID is present | Use only the verified ExpensePoolCode. SetName and ExpensePoolTypeCode qualify target identity only and never appear in the delete payload. | Yes; correct the supplied source. |
| An operation source is proposed | Error | | Its `RestAction` is missing, blank, or does not exactly match `POST` for Create, `PATCH` for PATCH, or `DELETE` for DELETE | Rebuild the JSON and generated row with the intent-derived action, then validate again. | Yes; reconstruct the source. |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_expense_pool_type | Before Create payload construction or when PATCH changes ExpensePoolTypeCode | LookupCode from one exact normalized Meaning match, or complete allowed Meaning values after no match | ora_reference_lookups.md |
| resolve_reference_set | Before Create payload construction or when DELETE supplies SetName as a target qualifier | SetId from one verified SetName candidate after local normalized verification | ora_reference_lookups.md |
| resolve_delete_target | Before DELETE payload validation | One exact target selected from ExpensePoolCode and any resolved optional qualifiers | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OEP.ENFORCE_PAYLOAD | decision | 7 | design_enforcement | enforced->OEP.DONE_OPERATION;blocked->OEP.HANDLE_ISSUE | OEP.RESOLVE_DELETE_TARGET | stop | Create, DELETE, or supplied PATCH changes are validated |
