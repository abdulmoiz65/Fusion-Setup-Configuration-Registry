# Job Requisition Descriptive Flexfields Input Validation

Validate only task-scoped requests for Job Requisition Descriptive Flexfields under Recruiting Configuration. Do not substitute a generic Common descriptive-flexfields task.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Exact FSM task identity | task_code = ORA_IRC_MANAGE_JOB_REQUISITION_DESCRIPTIVE_FLEXFIELDS; task_name = Job Requisition Descriptive Flexfields | Block as unsupported scope | Supply the exact task identity from the generated task skill and effective catalog | Any request | |
| Explicit requested operation | operation = Inspect, Plan, Export, Validate, or approved Import or Change | Block and request the exact operation | Normalize read, list, retrieve, or show segments to Inspect; otherwise obtain the explicit operation from the request | Any supported request | |
| Exact DFF and scope identity | Exact exported DFF root and Global or named context scope; segment identity only for a single-segment or change request | Block the ambiguous target | For Inspect, resolve one exact DFF root and the requested scope from a fresh exact-task export; for changes, use the approved change request | Any supported request | |
| Fresh read-only export artifact | Newly downloaded and extracted exact-task CSV export from the selected environment | Stop until a fresh artifact is available and valid | Use shared.setup-export.task-level-export with the exact task code and Recruiting Configuration context | Inspect or list current segments | |
| Requested business-change scope | setup_task_scope containing only the requested DFF attributes and values | Block unrelated or incomplete changes | Obtain the exact approved change scope | Any configuration request | |
| Immutable import artifact | setup_data_artifacts containing the exact immutable FSM CSV ZIP | Stop until the artifact and its source are confirmed | Use the Core Data Loader lifecycle selected by the task route | Import or approved change submission | |
| LOV or value-set reference | Value-set identity; DFF segment association; authoritative source; match rule; requested fields; output mapping | Stop before change preview, import, activation, or mutation | Obtain the authoritative reference contract and resolve it through resolve_dff_reference_authority | A configuration change specifies an LOV or value set | resolve_dff_reference_authority |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Another FSM page or generic Common DFF task is requested | UNSUPPORTED | Stop and route to the correct task | |
| The requested operation or scope is missing or ambiguous | MISSING | Request only the exact missing detail and stop | |
| Inspect or list is requested without a fresh exact-task export | BLOCKED | Run shared.setup-export.task-level-export and validate the downloaded FileContent archive | |
| The fresh export contains no DFF root or more than one DFF root for the exact task | MISSING or AMBIGUOUS | Report the exact match count and stop; do not substitute another DFF task | |
| A Global result contains context-sensitive rows | INVALID | Discard contextual rows and retain only the Global Data Elements segment rows from the exported DFF | |
| An import lacks the exact immutable task-scoped artifact | BLOCKED | Stop until the artifact and its source are confirmed | |
| An LOV or value-set contract is undocumented or incomplete | BLOCKED | Obtain the authoritative contract before change preview, import, activation, or mutation | resolve_dff_reference_authority |
| A mutation lacks an exact preview and current approval | APPROVAL_REQUIRED | Return to the Core Data Loader approval lifecycle | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task equality | Require exact task code ORA_IRC_MANAGE_JOB_REQUISITION_DESCRIPTIVE_FLEXFIELDS and task name Job Requisition Descriptive Flexfields | Any request | |
| Operation enumeration | Accept Inspect, Plan, Export, Validate, or approved Import or Change; normalize read, list, retrieve, or show segments to Inspect | Any supported request | |
| Inspect target completeness | Require only the requested scope for a list; resolve the exact DFF root from the fresh exact-task export and do not require a segment identity for a list-all request | Inspect or list | |
| DFF target completeness | Require the exact DFF code, Global or named context scope, and segment or attribute identity applicable to a single-segment or change request | Plan, Validate, Import, or Change | |
| Fresh export identity | Require the exact task code, selected environment, retrieved FileContent, valid ZIP extraction, and exactly one exported DFF root | Inspect or list | |
| Global row isolation | Select only rows whose exported context is Global Data Elements; exclude every context-sensitive segment row | Inspect with scope Global | |
| Segment list presentation | Sort by SequenceNumber and render exactly Seq., Name, Code, API Name, Column, Type, Value Set, Required; map RequiredFlag Y or N to Yes or No and use an em dash only for a blank supported value | Inspect or list | |
| Change-scope isolation | Accept only requested DFF attributes and values; reject unrelated attributes, inferred contexts, or inferred segments | Any configuration request | |
| Artifact identity | Require a fresh task-level CSV export for Inspect evidence or an immutable FSM CSV ZIP for import | Inspect or import | |
| LOV or value-set authority | Require the supplied value-set identity and DFF segment association to resolve through the approved reference contract | A configuration change specifies an LOV or value set | resolve_dff_reference_authority |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB_REQ_DFF.VALIDATE_INPUT | step | 10 | validate_input | valid->JOB_REQ_DFF.RESOLVE_REFERENCES;missing->JOB_REQ_DFF.RETURN_ISSUES;invalid->JOB_REQ_DFF.RETURN_ISSUES;ambiguous->JOB_REQ_DFF.RETURN_ISSUES;unsupported->JOB_REQ_DFF.RETURN_ISSUES | none | stop | Every supported Job Requisition Descriptive Flexfields request |
