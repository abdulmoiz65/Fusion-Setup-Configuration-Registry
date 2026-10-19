# Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | The Site-level FUSION_APPS_SEARCH_ENABLED record is absent, ambiguous, or not Y or N | Stop and request a valid approved Site-level value; do not infer or update the profile value |
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | Global Search is not visible after the profile value is enabled | Ask the user to sign out and sign back in before validating visibility again |
| ORA_SVC_MANAGE_STANDARD_TEXT_PROFILE_OPTS | Manage Standard Text Profile Options | The SVC_ENABLE_STD_TEXT_IN_SR value, target scope, or write contract is incomplete | Stop and request the missing required input or approved implementation source |
| ORA_SVC_MANAGE_SERVICE_REQUEST_DYNAMIC_LINKS | Manage Service Request Dynamic Links | A Dynamic Link collection GET fails or a requested write is not covered by the separate approved workflow | Stop, preserve sanitized error evidence, and do not retry a write or infer a write payload |
| ORA_SVC_MANAGE_TAGS | Manage Tags | The Tag identity or request contract is incomplete, the exact-name preflight finds a match, or Fusion rejects the request | Stop, preserve sanitized diagnostics, do not retry a POST, and do not create a duplicate tag |
| ORA_CONFIGURE_ACTION_BAR_PARAMETERS | Configure Action Bar Parameters | An Action Bar configuration collection GET fails or a requested write is not covered by the separate approved workflow | Stop, preserve sanitized error evidence, and do not retry a write or infer update fields |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | A Note Types collection GET or exact-match preflight fails, the target is not unique, or Fusion rejects an update | Stop, preserve sanitized error evidence, do not retry a PATCH, and do not infer an alternate target or payload |
| ORA_MANAGE_SERVICE_REQUEST_MESSAGE_TYPES_AND_SUBTYPES | Manage Service Request Message Types and Subtypes | The Message Type or Subtype lookup-value contract is incomplete | Stop and request the missing implementation source |
| ORA_SVC_MANAGE_PASSIVE_BEACON_CONFIGURATION | Manage Passive Beacon Configuration | A passive Beacon provider-status collection GET fails or a requested write is not covered by the separate approved workflow | Stop, preserve sanitized error evidence, and do not retry a write or infer a write payload |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | The Site-level FUSION_APPS_SEARCH_ENABLED value is not exactly Y or N, or approval is missing | Do not update the profile value |
| ORA_SVC_MANAGE_STANDARD_TEXT_PROFILE_OPTS | Manage Standard Text Profile Options | The SVC_ENABLE_STD_TEXT_IN_SR value, target scope, or approved write contract is incomplete | Do not update a profile value |
| ORA_SVC_MANAGE_SERVICE_REQUEST_DYNAMIC_LINKS | Manage Service Request Dynamic Links | The supported REST request contract is TBD | Do not create, update, or delete a Dynamic Link |
| ORA_SVC_MANAGE_TAGS | Manage Tags | The create preflight is not clear or explicit approval of the exact payload is missing | Do not POST a Tag; do not use upsert or retry a POST |
| ORA_CONFIGURE_ACTION_BAR_PARAMETERS | Configure Action Bar Parameters | The requested operation is a write or its supported update-field contract is incomplete | Do not create or update an Action Bar configuration |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | The update preflight is not clear or explicit approval of the exact payload is missing | Do not PATCH a Note Type or retry a PATCH |
| ORA_MANAGE_SERVICE_REQUEST_MESSAGE_TYPES_AND_SUBTYPES | Manage Service Request Message Types and Subtypes | The supported lookup-code contract is TBD | Do not change a Message Type or Subtype |
| ORA_SVC_MANAGE_PASSIVE_BEACON_CONFIGURATION | Manage Passive Beacon Configuration | The requested operation is a write or the supported write contract is incomplete | Do not change passive Beacon configuration |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | GSEARCH.DONE | terminal | 90 | terminal | none | GSEARCH.DESIGN | stop | Global Search guidance is ready for preview handoff |
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Global Search gate produces issues |
| ORA_SVC_MANAGE_STANDARD_TEXT_PROFILE_OPTS | Manage Standard Text Profile Options | STDTEXT.DONE | terminal | 90 | terminal | none | STDTEXT.VALIDATE | stop | Standard Text profile option guidance is ready for preview handoff |
| ORA_SVC_MANAGE_STANDARD_TEXT_PROFILE_OPTS | Manage Standard Text Profile Options | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Standard Text profile option gate produces issues |
| ORA_SVC_MANAGE_SERVICE_REQUEST_DYNAMIC_LINKS | Manage Service Request Dynamic Links | DYNLINK.DONE | terminal | 90 | terminal | none | DYNLINK.LOOKUP | stop | Dynamic Link guidance is ready for preview handoff |
| ORA_SVC_MANAGE_SERVICE_REQUEST_DYNAMIC_LINKS | Manage Service Request Dynamic Links | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Dynamic Link gate produces issues |
| ORA_SVC_MANAGE_TAGS | Manage Tags | TAG.DONE | terminal | 90 | terminal | none | TAG.LOOKUP | stop | Tag guidance is ready for preview handoff |
| ORA_SVC_MANAGE_TAGS | Manage Tags | TAG.CREATE_APPROVAL_GATE | decision | 30 | execution_gate | approved->TAG.CREATE_READY;denied->TAG.CREATE_REFUSED | TAG.CREATE_PREFLIGHT | stop | Exact-name preflight found no match and the exact create payload is ready for user approval |
| ORA_SVC_MANAGE_TAGS | Manage Tags | TAG.CREATE_READY | terminal | 31 | terminal | none | TAG.CREATE_APPROVAL_GATE | stop | Explicit approval permits one POST to the documented Tags collection endpoint |
| ORA_SVC_MANAGE_TAGS | Manage Tags | TAG.DUPLICATE | terminal | 32 | terminal | none | TAG.CREATE_PREFLIGHT | stop | An exact-name match exists; creation is blocked |
| ORA_SVC_MANAGE_TAGS | Manage Tags | TAG.CREATE_REFUSED | terminal | 33 | terminal | none | TAG.CREATE_APPROVAL_GATE | stop | The create preview was denied or approval was not granted |
| ORA_SVC_MANAGE_TAGS | Manage Tags | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Tag gate produces issues |
| ORA_CONFIGURE_ACTION_BAR_PARAMETERS | Configure Action Bar Parameters | ACTIONBAR.DONE | terminal | 90 | terminal | none | ACTIONBAR.LOOKUP | stop | Action Bar guidance is ready for preview handoff |
| ORA_CONFIGURE_ACTION_BAR_PARAMETERS | Configure Action Bar Parameters | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Action Bar gate produces issues |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | NOTETYPE.DONE | terminal | 90 | terminal | none | NOTETYPE.LOOKUP | stop | Note Type guidance is ready for preview handoff |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | NOTETYPE.UPDATE_APPROVAL_GATE | decision | 30 | execution_gate | approved->NOTETYPE.UPDATE_READY;denied->NOTETYPE.UPDATE_REFUSED | NOTETYPE.UPDATE_PREFLIGHT | stop | Exact-match preflight found one target and the exact Meaning update payload is ready for user approval |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | NOTETYPE.UPDATE_READY | terminal | 31 | terminal | none | NOTETYPE.UPDATE_APPROVAL_GATE | stop | Explicit approval permits one PATCH to the documented Note Type lookup-code endpoint |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | NOTETYPE.UPDATE_REFUSED | terminal | 32 | terminal | none | NOTETYPE.UPDATE_APPROVAL_GATE | stop | The update preview was denied or approval was not granted |
| ORA_SVC_MANAGE_NOTE_TYPES | Manage Note Types | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Note Type gate produces issues |
| ORA_MANAGE_SERVICE_REQUEST_MESSAGE_TYPES_AND_SUBTYPES | Manage Service Request Message Types and Subtypes | MSGTYPE.DONE | terminal | 90 | terminal | none | MSGTYPE.LOOKUP | stop | Message Type or Subtype guidance is ready for preview handoff |
| ORA_MANAGE_SERVICE_REQUEST_MESSAGE_TYPES_AND_SUBTYPES | Manage Service Request Message Types and Subtypes | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Message Type or Subtype gate produces issues |
| ORA_SVC_MANAGE_PASSIVE_BEACON_CONFIGURATION | Manage Passive Beacon Configuration | BEACON.DONE | terminal | 90 | terminal | none | BEACON.LOOKUP | stop | Passive Beacon guidance is ready for preview handoff |
| ORA_SVC_MANAGE_PASSIVE_BEACON_CONFIGURATION | Manage Passive Beacon Configuration | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any Passive Beacon gate produces issues |
