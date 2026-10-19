# Manage Collective Agreements Design Enforcement

## Purpose

Defines the mandatory Collective Agreement design gates evaluated before
preview or routing. It does not perform lookups, apply defaults, or create
missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm operation and target | Require one supported operation and the exact applicable agreement or create-availability evidence |
| 2 | Confirm effective and EFF evidence | Require one effective row and current EFF metadata and values when applicable |
| 3 | Validate source scope | Keep the parent and requested EFF rows together with complete row identity |
| 4 | Confirm route safety | Require the Core Data Loader route and safe user-facing output |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| OPERATION | Every request | Blocking |  | Operation is missing, mixed, or unsupported by the registered Data Loader object | Select one supported operation | Input fix |
| TARGET_CARDINALITY | Read, edit, delete, or create uniqueness check | Blocking | find_manage_collective_agreements | The target, effective row, or uniqueness result has invalid cardinality | Supply one exact target and effective date, or a unique create identity | Lookup fix |
| EFF_METADATA | An EFF context or segment is requested | Blocking | resolve_collective_agreement_eff_metadata | Current context, segment, target attribute, type, cardinality, or category metadata is unavailable | Resolve the current EFF contract before authoring the row | Lookup fix |
| EFF_VALUE | A supplied EFF segment declares an LOV | Blocking | resolve_collective_agreement_eff_value_set | The value does not resolve to one compatible metadata-declared typed stored value | Supply one exact compatible EFF value | Lookup fix |
| EFF_ROW_IDENTITY | An EFF row is authored | Blocking | resolve_collective_agreement_eff_metadata | Parent and requested EFF rows are split, EFF_CATEGORY_CODE is absent, or required sequence or unique values are blank or repeated | Rebuild one parent-scoped source with complete distinct EFF row identity | Source rebuild |
| SENSITIVE_OUTPUT | A preview or user-facing result is produced | Blocking |  | Credentials, runtime links, raw payloads, or surrogate IDs are exposed | Regenerate the output with sensitive and transient values removed | Re-preview |
| ROUTE | A mutation is requested | Blocking |  | Fusion REST, FSM CSV, ZAP, permanent deletion, deactivation, or an unapproved retry is proposed instead of Core Data Loader | Use only the declared Core Data Loader route | No |

| AGREEMENT_PLANNING | Create or edit | Warning |  | Planned change lacks a future effective date or review, or bulk import was not explicitly requested | Use a future date for planned changes, review the change, and use bulk import only when requested | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_collective_agreements | Read, edit, delete, or create uniqueness check | Exact identity, effective row, current values, or create-availability evidence | ora_reference_lookups.md |
| resolve_collective_agreement_eff_metadata | An EFF context, segment, or row is requested | Context, segment, category, target attribute, type, cardinality, and row-identity contract | ora_reference_lookups.md |
| resolve_collective_agreement_eff_value_set | A supplied EFF segment declares an LOV | One compatible metadata-declared typed stored value | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CA.ENFORCE | decision | 6 | design_enforcement | passed->CA.ROUTE;not_required->CA.ROUTE;blocked->CA.ERROR | CA.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |

## Date-effective Split Delete Gate

Block deletion unless all effective-dated splits were fetched and displayed through hcmDateEffectiveObjectChanges, a non-first displayed split is selected, and the source is a bounded HDL/Data Loader MERGE. Block REST or HDL DELETE, a missing `SET PURGE_FUTURE_CHANGES Y` directive, non-`YYYY/MM/DD` DAT dates, a source without the retained predecessor MERGE, or a range that deletes more than the selected contiguous splits.

## Strict Data Loader Route

The only permitted deletion implementation is hcmDateEffectiveObjectChanges for history resolution plus Core Data Loader/HDL MERGE for mutation. The source must contain `SET PURGE_FUTURE_CHANGES Y` and the retained predecessor MERGE bounded through the final selected split end date; it must contain no HDL DELETE instruction. For multiple noncontiguous selections, require newest-to-oldest separate preflight, preview, approval, merge submission, and timeline verification.

## Mutation Transport Enforcement

Block the request if hcmDateEffectiveObjectChanges is proposed as the mutation transport. It is read-only; HDL/Core Data Loader MERGE is the exclusive transport for deletion and effective-date updates.


## Corrected HDL Split-Deletion Contract (Supersedes Earlier Examples)

Use exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one retained-predecessor `MERGE` row, with DAT dates in `YYYY/MM/DD`. The retained predecessor start and final selected end bound the contiguous removal. Reject HDL DELETE, mixed instructions, ISO DAT dates, first/only split deletion, and any REST mutation.
