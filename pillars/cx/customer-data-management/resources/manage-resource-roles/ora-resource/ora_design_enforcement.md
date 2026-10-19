# Manage Resource Roles Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish roles and types | Create and associate needed resource roles and resource types before adding users |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| MRR-ROLE-TYPE-ASSOCIATION | Before adding users | Blocker | Manual UI verification | A required role or resource type is not created and associated | Complete role and type associations first | Yes |
| MRR-ROLE-TYPE-LOOKUP | Before creating, importing, or updating a resource role | Blocker | Exact `JTF_RS_ROLE_TYPE` `LookupCode` validation through Manage Resource Role Lookups | The supplied Role Type or RoleTypeCode is not an existing exact lookup code | Set up or activate the code in Manage Resource Role Lookups, then revalidate the role | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.ENFORCE | decision | 6 | design_enforcement | read->MRR.ROLE_LOOKUP;fsm-import-create-update->MRR.FSM_IMPORT_ROUTE;unsupported-write-or-delete->MRR.BLOCKED;blocked->MRR.BLOCKED | MRR.ADVISORY | stop | Resource-role design is reviewed and the requested operation is classified |
