# Manage Resource Roles Execution Contract

Every Fusion REST request in this execution contract must include
`REST-Framework-Version: 9`.

## Runtime Sources

| Source | Purpose |
|---|---|
| Task catalog metadata | Confirms FSM/CSV export-import support for Manage Resource Roles |
| Supplied Oracle Manage Resource Roles documentation | Define UI steps and identify the missing REST contract for direct create/update/delete actions |
| Supplied Oracle Resource Roles REST endpoints documentation | Define read-only collection and item retrieval endpoints |

## Execution Contract

| Situation | What Happens |
|---|---|
| A collection read is requested | Use the documented read-only Resource Roles collection GET endpoint |
| An item read is requested | Require RoleCode and use the documented read-only Resource Roles item GET endpoint |
| Create or update by FSM CSV import is requested | Route to `shared.setup-import.task-level-import` using Customer Data Management, Resources, Manage Resource Roles, and task code HZ_MANAGE_RESOURCE_ROLES. Validate the import artifact and reference data before submission. |
| REST create, update, or delete is requested | Block because no writable REST contract is supplied |
| FSM delete is requested | Block because the import object's delete semantics are not documented in this skill |
| Manual setup is performed | Navigate to Setup and Maintenance, open Users and Security, select Manage Resource Roles, create the role, enter documented fields, and save and close |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Get all resource roles | GET | /crmRestApi/resources/11.13.18.05/resourceRoles |
| Get a resource role | GET | /crmRestApi/resources/11.13.18.05/resourceRoles/{RoleCode} |
| Create or update resource role | FSM CSV import | Route to shared.setup-import.task-level-import; no direct REST endpoint is used |
| Create, update, or delete resource role by REST | TBD | No writable REST endpoint is supplied |
| Delete resource role by FSM | TBD | No documented import-object delete semantics are supplied |

## Preview Pattern

| Step | Requirement |
|---|---|
| Review read request | Confirm whether collection or item retrieval is requested and require RoleCode for an item read |
| Review FSM import request | Confirm the CSV artifact, explicit create/update operation, task identity, reference-data validation, and import routing before submission |

## Live Pattern

| Step | Requirement |
|---|---|
| Execute collection read | Send GET to the collection endpoint and return the Fusion response |
| Execute item read | Send GET to the item endpoint with an exact RoleCode and return the Fusion response |
| Execute FSM create/update import | Delegate the validated artifact to `shared.setup-import.task-level-import`; the shared import workflow owns upload, submission, polling, and result handling |
| Execute REST write or FSM delete | Not available until an approved REST contract or documented FSM delete semantics is supplied |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.ROLE_LOOKUP | step | 7 | rest_get | found->MRR.DONE_READ;not-found->MRR.BLOCKED | MRR.ENFORCE | stop | A read-only resource-role collection or item lookup is requested |
| MRR.DONE_READ | terminal | 8 | terminal | none | MRR.ROLE_LOOKUP | stop | The Resource Roles GET request completed successfully |
| MRR.FSM_IMPORT_ROUTE | step | 10 | execution_gate | routed->MRR.DONE_FSM_IMPORT_ROUTE;blocked->MRR.BLOCKED | MRR.ENFORCE | stop | A validated create or update FSM CSV import is requested |
| MRR.DONE_FSM_IMPORT_ROUTE | terminal | 11 | terminal | none | MRR.FSM_IMPORT_ROUTE | stop | The create/update import is routed to shared.setup-import.task-level-import |
