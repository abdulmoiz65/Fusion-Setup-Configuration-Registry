# Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any REST request | Error | resolve_duplicate_management_lookup | Exact inventory membership or Standard category is not proven | Reconcile current exact GET | Yes |
| Mutation | Error | resolve_duplicate_management_lookup | Configuration level, code origin, current describe, immutable preview, or approval is missing | Complete exact GET, describe, preview, and approval | Yes |
| System mutation | Error | resolve_duplicate_management_lookup | Operation is not an existing-code Meaning update | Restrict the request to writable Meaning | No |
| Extensible mutation | Error | resolve_duplicate_management_lookup | Target is not one of the two Extensible members or operation exceeds permitted wording/display and proven custom-code lifecycle fields | Restrict the request to the level-specific contract | Yes |
| Seeded or unknown code | Error | resolve_duplicate_management_lookup | Delete, identity change, state/date change, or custom-code treatment is requested | Select a proven custom code or permitted non-destructive field | Yes |
| Unsupported mutation | Error | resolve_duplicate_management_lookup | Request renames a code or changes parent, module, security, level, or Tag | Refuse; use a supported setup route if appropriate | No |
| FSM ZIP | Error |  | Metadata/hash/envelope is unsafe or wrong task | Rebuild Core Data Loader preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_duplicate_management_lookup | Before any REST read or mutation preview | Exact task membership, Standard category, customization level, current type/code values, seed evidence, links, and describe metadata | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DML.ENFORCE | decision | 40 | design_enforcement | pass->DML.READY;fail->DML.ERROR | DML.DEPENDENCIES | stop | Before REST or setup-data execution readiness. |
