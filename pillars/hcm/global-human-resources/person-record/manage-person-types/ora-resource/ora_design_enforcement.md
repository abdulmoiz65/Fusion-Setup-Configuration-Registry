# Manage Person Types Design Enforcement

## Purpose

Defines the mandatory paired-key, System Person Type, source, route, and
preview design gates evaluated before routing. It does not perform lookups,
apply defaults, or redefine fixed System Person Types.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm paired identity | Resolve one enabled System/User Person Type pair |
| 2 | Protect fixed setup | Restrict mutations to supported User Person Type changes |
| 3 | Validate source | Keep the current scoped PersonType source; use one ordered DAT source for a document-specified mutation batch |
| 4 | Confirm mutation control | Require the declared Data Loader route and approved immutable preview |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Create, edit, delete, or exact read | Blocking | find_manage_person_types | The paired System/User business key is incomplete or ambiguous | Correct the complete pair and evaluate all required pages | Lookup fix |
| SYSTEM | Every change | Blocking | find_manage_person_types | A fixed System Person Type is redefined or deleted | Prepare only a supported User Person Type change | No |
| REFERENCE | A System Person Type is supplied | Blocking | resolve_system_person_type | The System Person Type is missing, disabled, or ambiguous | Resolve one enabled current System Person Type | Lookup fix |
| ACTIVE | Active is supplied | Blocking | resolve_person_type_active | Active does not resolve to one enabled current stored code | Resolve one exact enabled Active value | Lookup fix |
| SOURCE | Create, edit, delete, or document-specified mutation batch | Blocking |  | Source is stale, incomplete, unsafe, cannot represent every row, or contains unrelated changes | Rebuild the scoped source and revalidate it | Source rebuild |
| MUTATION_ROUTE | Create, edit, or delete | Blocking |  | REST, FSM, CSV, or another mutation route is proposed | Use only Core Data Loader with business object PersonType | No |
| APPROVAL | Create, edit, or delete | Blocking |  | Preview or approval is absent, stale, or bound to changed source bytes | Regenerate and approve the exact immutable preview | Re-preview |
| VERIFY | After load | Blocking | find_manage_person_types | Reconciliation does not prove the requested state | Report failed or unknown; do not replay automatically | No |

For a `PersonType` delete, the scoped loader source is an explicit DAT record
with the first field `DELETE`, not `MERGE`, and the second field `PersonType`.
Use the exact resolved `SystemPersonType` and `UserPersonType` business key;
do not substitute a `RestAction` column.

For a document-specified mutation batch, the scoped loader source is exactly one
ordered DAT file with one `METADATA|PersonType|...` header. The source may
contain supported `MERGE|PersonType|...` and `DELETE|PersonType|...` rows in
document order only when every row's current identity is resolved before the
file is built. Reject a row that needs an ID or state created earlier in the
same batch unless a current loader contract supplies a stable pre-resolved key;
do not use a stale ID or split the batch into separate uploads.

| PERSON_TYPE_DEFAULT | Create, edit, or inactivate | Warning |  | System type, default User Person Type, or replacement default is not confirmed | Maintain User Person Types within the correct System Person Type and preserve a valid default | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_system_person_type | A System Person Type is supplied | One enabled current code and meaning | ora_reference_lookups.md |
| find_manage_person_types | Identity, System Person Type, fixed-setup, or reconciliation evaluation | Exact paired business key, enabled state, current values, and current-run identity | ora_reference_lookups.md |
| resolve_person_type_active | Active is supplied | One enabled current stored code | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.ENFORCE | decision | 5 | design_enforcement | passed->PT.ROUTE;not_required->PT.ROUTE;blocked->PT.ERROR | PT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
