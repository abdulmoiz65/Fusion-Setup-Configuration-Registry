# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Hierarchy scope | One hierarchy name, status, and intended node tree | Stop package preparation | Obtain the approved hierarchy scope | Every request | |
| Node evidence | Exact geography elements, master-geography identifiers, and immediate parent evidence for each node | Stop package preparation | Obtain authoritative source evidence | Every node | |
| Node correlation | Unique nonblank GeoNodeCode and immediate ParentGeoNodeCode for each child | Stop validation | Correct the package-local node links | Every node package | |
| Identifier coverage | One identifier row per imported node with matching hierarchy name, node code, name, and status | Stop validation | Add or correct identifier rows | Every node package | |
| Task-native artifact | Matching FSM export or template and final ZIP candidate | Stop validation | Export the task or obtain its approved template | Every package request | |
| Import target | Exact target environment | Stop import preview | Obtain the target environment | Import request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|
| CSV width | Require three hierarchy fields, 25 node fields, and six identifier fields | Every package | |
| Source values | Reject guessed geography codes, names, accent variants, master identifiers, or parent relations | Every node | |
| Archive integrity | Require the matching task-native archive structure before approval | Every package | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHH.VALIDATE | decision | 10 | validate_input | valid->GHH.READINESS;issues->GHH.INPUT_ISSUES | none | stop | A Geography Hierarchies package is prepared or reviewed |
