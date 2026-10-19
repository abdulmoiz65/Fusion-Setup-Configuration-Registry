# Manage Resource Roles Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Interactive role definition | Role Name, Role Code, Role Type, and Orientation | Each resource role to create or validate |
| FSM CSV import | Import CSV artifact and an explicit create or update operation | Resource-role creation or update through supported FSM import |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| Role Name | Yes | Identify the resource role | No | Not documented |
| Role Code | Yes | Supply the organization role code | No | Not documented |
| Role Type or RoleTypeCode | Yes | Classify the role | No | Must exactly match a `JTF_RS_ROLE_TYPE` `LookupCode`; validate through Manage Resource Role Lookups |
| Orientation | Yes | Classify responsibility | No | Use Member, Manager, or Administrator |
| Role Code for lookup | Conditional | Retrieve one existing resource role | No | Required only for the item GET endpoint |
| Requested operation | Yes | Select read, FSM CSV import for create/update, REST write, or FSM delete | No | FSM import is supported only for create/update; REST writes and FSM delete are blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.COLLECT | step | 1 | collect_input | valid->MRR.VALIDATE;missing->MRR.BLOCKED | none | stop | A resource role is requested |
