# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Business event type | EventTypeCode or EventType meaning | Stop before Data Loader handoff | Provide one event type code or meaning that resolves exactly through resolve_inventory_business_event_type | A configuration row is supplied | resolve_inventory_business_event_type |
| Business event name | EventCode or EventName meaning | Stop before Data Loader handoff | Provide one event code or meaning that resolves exactly through resolve_inventory_business_event_name | A configuration row is supplied | resolve_inventory_business_event_name |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Event type input | Accept a code, a meaning, or both. When both are supplied, require both to resolve to the same LookupCode. For REST/Data Loader, fill EventTypeCode with that code. For FSM CSV, fill EventType with that code; do not send the display meaning in the FSM EventType column. | EventTypeCode or EventType is supplied | resolve_inventory_business_event_type |
| Event name input | Accept a code, a meaning, or both. When both are supplied, require both to resolve to the same LookupCode within the resolved event-type prefix. For REST/Data Loader, fill EventCode with that code. For FSM CSV, fill EventName with that code; do not send the display meaning in the FSM EventName column. | EventCode or EventName is supplied after EventTypeCode resolves | resolve_inventory_business_event_name |
| Publish Event normalization | Map the Redwood checkbox state selected to PublishEventCode Y and clear to PublishEventCode N. Preserve an explicit Y or N code unchanged. | Publish Event is supplied in the Redwood control representation or as its backend code | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IBEC.VALIDATE_INPUT | step | 10 | validate_input | valid->IBEC.RESOLVE_EVENT_TYPE;invalid->RETURN_ISSUES | none | stop | An Inventory Business Event Configurations row is supplied for validation |
