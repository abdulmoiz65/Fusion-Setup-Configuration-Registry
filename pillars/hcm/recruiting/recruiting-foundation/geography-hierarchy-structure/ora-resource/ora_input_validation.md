# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Target scope | One target country and an approved country code | Stop package preparation | Obtain the approved country scope | Every request | |
| Level mapping | Approved country-level mapping with level two populated before level three | Stop package preparation | Obtain the approved mapping evidence | Every package request | |
| Configured-level read | Exact target environment and country; current task-native structure export with exactly one matching CountryCode row and GeoLevel2ColumnName and GeoLevel3ColumnName columns | Stop the read and report missing or ambiguous configuration evidence | Obtain the current setup-data export through shared.setup-export.task-level-export; no final import ZIP or import approval is required for a read | A request to explain existing country levels | |
| Task-native artifact | Matching FSM export or template and final ZIP candidate | Stop validation | Export the task or obtain its approved template | Every package request | |
| Import target | Exact nonproduction or approved target environment | Stop import preview | Obtain the target environment | Import request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|
| Country isolation | Reject a package that contains more than one intended country | Every package | |
| Supported levels | Reject Postal Code and a level-three mapping without level two | Every package | |
| Archive integrity | Require the task-native archive structure and validated CSV rows before approval | Every package | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHS.VALIDATE | decision | 10 | validate_input | valid->GHS.READINESS;read->GHS.LABELS;issues->GHS.INPUT_ISSUES | none | stop | For a configured-level read, validate the read inputs and choose read; for package preparation or review choose valid only after package checks; missing or ambiguous inputs choose issues |
