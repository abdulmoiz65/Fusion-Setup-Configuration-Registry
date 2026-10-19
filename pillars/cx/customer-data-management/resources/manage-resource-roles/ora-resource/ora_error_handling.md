# Manage Resource Roles Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required role inputs are incomplete or invalid | Stop and request corrected values |
| Supplied Role Type or RoleTypeCode is absent from `JTF_RS_ROLE_TYPE` | Stop the role operation. Direct the user to Manage Resource Role Lookups to set up or activate the exact lookup code, then repeat validation. |
| Required role and type association is not verified | Stop before adding users or assigning work |
| Resource role GET returns no matching item | Report the not-found response and do not create a role |
| REST create, update, or delete is requested | Stop and request approved writable REST guidance |
| FSM CSV create/update import is requested | Route to shared.setup-import.task-level-import after artifact and reference-data validation; do not classify it as a REST write |
| FSM delete is requested | Stop and state that Manage Resource Roles does not yet document delete semantics for its FSM import object |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Role input is incomplete or invalid | Correct inputs |
| fusion_api_error | Resource Roles GET fails | Report the HTTP outcome and Fusion response |
| rest_write_blocker | A REST write contract is absent | Supply approved REST contract |
| fsm_delete_blocker | FSM delete semantics are not documented | Supply the documented import-object delete contract |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| REST write execution blocker | State that no writable REST endpoint or request contract was supplied |
| FSM delete blocker | State that FSM create/update import is supported, but delete semantics are not documented |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No writable REST contract is supplied | Do not invent a REST endpoint, payload, or REST execution behavior |
| No FSM delete semantics are supplied | Do not infer that a create/update import file or route can delete a resource role |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.BLOCKED | terminal | 12 | terminal | none | none | stop | Any validation, dependency, design, lookup, REST-write, or FSM-delete blocker occurs |
