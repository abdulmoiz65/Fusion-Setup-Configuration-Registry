# Manage Resource Role Descriptive Flexfields Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Target flexfield | JTF_RS_ROLES_B | Stop | Use the task's fixed Resource Role DFF code | Every request |  |
| Configuration intent | Global segment change, context segment change, context change, context-sensitive segment change, segment validation change, or deployment/test request | Stop | State the intended DFF configuration outcome | Every request |  |
| Segment definition | Segment identity, display properties, and validation design | Stop | Provide the attributes to configure for each requested segment | Adding or updating a segment |  |
| Context definition | Context code, name, description, and context-sensitive segment definition | Stop | Provide the complete context definition | Adding or updating a context |  |
| Sandbox test plan | Sandbox identity and test evidence plan | Stop | Provide the sandbox and the intended validation scenario | Publishing a descriptive-flexfield change |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Segment sequence is unique | Block a sequence number already used by another global segment or by another context-sensitive segment within the same context | Adding or updating a segment |  |
| Context value set is compatible | Require an independent or table-validated Character value set whose maximum value length does not exceed the context column length | Assigning a context value set |  |
| Table-validated context value set uses permitted binds | Block a WHERE clause using VALUESET.value_set_code or SEGMENT.segment_code | Assigning a table-validated context value set |  |
| Initial-value SQL is safe | Require a statement that returns one row and a value of the correct type | Defining a SQL initial value |  |
| Existing context is preserved | Block deletion of an existing context; require disabling its associated context value with an end date in the past instead | Retiring a context |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRRDFF.VALIDATE_INPUT | decision | 1 | validate_input | valid->MRRDFF.APPLY_DEFAULTS;invalid->MRRDFF.BLOCKED | none | stop | Every request |
