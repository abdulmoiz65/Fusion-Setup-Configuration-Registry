# Design Enforcement

## Design Rules
| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any REST request | Error | resolve_data_cleansing_lookup | Exact member or Standard category not proven | Reconcile current GET | Yes |
| Update | Error | resolve_data_cleansing_lookup | System level, code, writable Meaning, preview, or approval missing | Complete preflight | Yes |
| Mutation | Error | resolve_data_cleansing_lookup | Operation changes anything except existing-code Meaning | Refuse | No |
| FSM ZIP | Error |  | Metadata/hash/envelope unsafe or wrong task | Rebuild preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_data_cleansing_lookup | Before any REST read or update preview | Exact task membership, Standard category, customization level, current type/code values, seed evidence, links, and describe metadata | ora_reference_lookups.md |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCL.ENFORCE | decision | 40 | design_enforcement | pass->DCL.READY;fail->DCL.ERROR | DCL.DEPENDENCIES | stop | Before REST or setup-data readiness. |
