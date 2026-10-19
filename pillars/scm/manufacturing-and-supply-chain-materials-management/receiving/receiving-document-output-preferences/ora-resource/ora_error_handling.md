# Receiving Document Output Preferences Error Handling

Sources: provided Redwood document-output-preferences flow, task-level FSM CSV import architecture, and registered Data Loader business object.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A LOV resolver has no match, multiple matches, or conflicting code and display inputs | Stop preparation, identify the field and resolver, and require an unambiguous corrected value. |
| A parent value changes after a dependent LOV value was selected | Clear the stale dependent value and resolve it again in the new context. |
| FSM template, metadata, or validation fails | Stop that FSM attempt; preserve its diagnostic. The user may separately select the registered Data Loader route. |
| Data Loader metadata or load validation fails | Stop that Data Loader attempt and follow its diagnostic; do not use direct Fusion REST. |
| A write or import is requested | Complete the selected route's ZIP or Data Loader validation and approval workflow before execution. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required task context or compatible LOV values are missing | Correct the supplied values and validate again. |
| Reference lookup failure | A documented resolver is unavailable, has no match, or has multiple matches | Correct the reference value; do not infer a replacement. |
| FSM blocker | Template metadata or immutable ZIP validation fails | Follow the returned FSM diagnostic and restart validation after correction. |
| Data Loader blocker | Data Loader metadata preflight or load validation fails | Follow the returned Data Loader diagnostic; do not bypass it with direct REST. |
| Approval blocker | A state-changing FSM import or Data Loader load lacks its route-specific approval | Obtain approval through the selected workflow. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup is unresolved | Do not create a payload, select an arbitrary result, or bypass the resolver. |
| FSM validation rejects metadata or source validation | Do not use direct Fusion REST; preserve the diagnostic and allow only an independently approved Data Loader operation. |
| Data Loader validation rejects the registered business object or payload | Do not use direct Fusion REST; correct the Data Loader input or select FSM through its separate approval path. |
| A load is unapproved | Do not upload or initiate it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCDOP.DATA_LOADER_GATE | decision | 30 | execution_gate | ready->RCDOP.DONE;blocked->RCDOP.RETURN_ISSUES | RCDOP.RESOLVE_LOVS | stop | Validated task input is handed to the selected FSM import or Data Loader workflow |
| RCDOP.RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | Any input, lookup, FSM, Data Loader, or approval issue exists |
| RCDOP.DONE | terminal | 50 | terminal | none | RCDOP.DATA_LOADER_GATE | stop | Task input is ready for the selected governed FSM or Data Loader workflow |
