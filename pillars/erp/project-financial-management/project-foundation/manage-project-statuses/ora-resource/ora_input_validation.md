# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | read, create, update, validate, export, import, end_date; recognize rename, clear, delete, remove_lifecycle and replace_lifecycle as unsupported intents | Block malformed input; refuse known unsupported intent | Normalize show/inspect to read and explicit removal/rename/clear intents to the scope guard; do not request create fields for a refused operation | Every request | check_project_status_operation_scope |
| Normalized changes | changes object, optional clear_fields list, optional LifecycleTargets list of resolved code strings and lifecycle_intent append/replace | Block malformed shape | Keep source StatusType/ProjectStatusName as identity. Put explicit update values in changes; omit unchanged blank intake cells before normalization. Explicit empty/null values in changes represent a clear request | Scope guard input | check_project_status_operation_scope |
| Identity | StatusType (status object), ProjectStatusName, and ProjectSystemStatusCode (classification) for create | Block write | Resolve object and name; resolve classification from the existing baseline for an update | Writes | find_project_status |
| Named status read | StatusType plus ProjectStatusName, or a verified ProjectStatusCode | Block only the named read if unresolved | Resolve current object/name/code through the declared identity lookup; do not assume a seed's display name is unchanged | Named reads | find_project_status |
| From Date | StartDateActive; FromDate is a conversational alias | Block create | Ask for an explicit start date; preserve existing start date on update | Create/update |  |
| Behavior | StartingStatusFlag, NextAllowableStatusFlag and targets, EnableBpFlag and outcomes, controls | Apply documented create defaults or preserve update omissions | Normalize the explicit user request before reading or constructing CSV; distinguish absent, blank, false and clear | Create/update |  |
| PROJECT create controls policy | prefer-current-else-standard or exact-inheritance | Default to prefer-current-else-standard | Exact current UI defaults, inherit exactly, or equivalent explicit wording selects exact-inheritance; disclose any standard-source configuration in the preview | PROJECT create only | resolve_status_controls |
| Target/artifacts | TargetEnvironment, current_export, package_template; use evidence when affected fields require it | Block affected write | Obtain task-scoped current evidence and native template through the selected workflow | Writes | verify_project_status_package |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ProjectStatusName is nonempty, at most 80 characters | Accept; otherwise identify the invalid field | Create/update |  |
| Description is at most 255 characters | Accept; otherwise reject | Supplied |  |
| StatusType and ProjectSystemStatusCode are at most 30 characters and resolve as a catalog pair | Accept; otherwise reject without substitution | Writes | resolve_status_capabilities |
| Dates parse as calendar dates | Normalize to the target template's format; do not use a locale-dependent ambiguous date | Dates supplied |  |
| StartingStatusFlag and EnableBpFlag use Y or N | Normalize Yes/No, true/false and boolean values; false means N, not omission | Supplied |  |
| Requested NextAllowableStatusFlag uses A, N, U, or S | Normalize All, None, Status, or Status Classification; never use UI option indexes as codes. An existing opaque legacy value such as Y is preserved when this field is not requested, not rejected or silently converted | Requested change or create default |  |
| Control EnabledFlag, AllowOverridesFlag, and CopyToUserStatusFlag use Y or N | Normalize an Allow request expressed as Yes/No, tick/untick or true/false to AllowOverridesFlag Y/N. Reject malformed raw values; authority for EnabledFlag and CopyToUserStatusFlag is checked by design enforcement | Controls supplied |  |
| ProjectStatusWeight is an integer with at most 18 digits | Reject fractional or malformed data; inherited weight is resolved separately | Progress weight supplied |  |
| Exact native package members and headers | Reject changed, mixed, or unproven package structure | Import | verify_project_status_package |

For read, require only a resolvable named identity and target; do not apply create defaults, require a start date, or build an import package. Return available current fields and identify unavailable details. Do not require per-status fields for a whole-task export or template lookup. Business restrictions, uniqueness, date ordering, graph policies, and editability belong to design enforcement. Missing downstream graph evidence is disclosed as deferred; missing identity or required payload data is not a deferred check.

## Consultant Field Normalization

| Accepted Input | Canonical Meaning | What Happens |
|---|---|---|
| Status object, Status_Type, StatusType | StatusType | Resolve Project to PROJECT; do not confuse it with the classification |
| System status, System_Status, Status classification | ProjectSystemStatusCode | Resolve within the selected object; Pending close becomes PENDING_CLOSE |
| Status, status name | ProjectStatusName | Preserve exact name after object/name matching |
| Starting_Status, Initial Status | StartingStatusFlag | Normalize explicit booleans to Y/N |
| Enable_Workflow, Enable Workflow | EnableBpFlag | Normalize explicit booleans to Y/N |
| Status_After_Change_Accepted / Status_After_Change_Rejected | Outcome target names | Resolve to status codes before assigning BpSuccessStatusCode / BpFailureStatusCode |
| Next Allowable Status Type | NextAllowableStatusFlag | A=All, N=None, U=Status, S=Status Classification |
| Status Lifecycle / Next Allowable Status | Requested target collection | Interpret names as statuses in U and classifications in S; record whether the intent is append or replace |
| Action label or ActionCode plus Allow; all action controls Yes/No | Requested action-control changes | Resolve the object-scoped labels/codes; materialize every requested existing action, including explicit N values |
| Blank cell in a create table | Omitted optional input | Apply documented defaults; never invent a mandatory start date |
| Absent or blank optional field on update | No change unless user explicitly requests clear | Carry forward current values; a clear is a separate operation with verified semantics |
| Assigned_Sets_Code | No assigned-set instruction | This native task package has no assigned-set member; a nonblank request requires a separately declared supported route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSTATUS.VALIDATE_INPUT | step | 1 | validate_input | valid->PSTATUS.LOOKUP_IDENTITIES;invalid->PSTATUS.RETURN_ISSUES;unsupported->PSTATUS.RETURN_REFUSAL | none | stop | Every request: run the local operation scope guard first; unsupported refuses before external lookups, malformed input returns issues, and needs_baseline may proceed only to declared identity/baseline resolution |
| PSTATUS.ROUTE_OPERATION | decision | 6 | evaluate_result | supported->PSTATUS.RESOLVE_DEPENDENCIES;unsupported->PSTATUS.RETURN_REFUSAL;invalid->PSTATUS.RETURN_ISSUES | PSTATUS.RESOLVE_GRAPH | stop | After capability and graph resolution |
