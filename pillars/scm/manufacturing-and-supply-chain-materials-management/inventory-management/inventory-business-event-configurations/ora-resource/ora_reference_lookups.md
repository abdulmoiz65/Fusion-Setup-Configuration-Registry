# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_inventory_business_event_type | EventTypeCode or EventType meaning is supplied | Supplied EventTypeCode and or EventType | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?onlyData=true&fields=Meaning,LookupCode&q=LookupType='ORA_INV_BUS_EVENT_TYPES' | Meaning and LookupCode | Compare supplied code and meaning with trim plus case-insensitive exact matching. When both are supplied, require the same one returned row. Never fuzzy-match or select the first result. | REST/Data Loader EventTypeCode: LookupCode; FSM EventType: LookupCode | Zero or multiple matches, or conflicting supplied code and meaning: stop and request one exact event type. Read failure: stop and report a sanitized diagnostic. |
| resolve_inventory_business_event_name | EventCode or EventName meaning is supplied after event type resolution | Resolved EventTypeCode; supplied EventCode and or EventName | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?onlyData=true&fields=Meaning,LookupCode&q=LookupType='ORA_INV_BUS_EVENT_NAMES' and LookupCode like '{EventTypeCode}%' | Meaning and LookupCode | Compare supplied code and meaning with trim plus case-insensitive exact matching within the returned EventTypeCode prefix. When both are supplied, require the same one returned row. Never fuzzy-match or select the first result. | REST/Data Loader EventCode: LookupCode; FSM EventName: LookupCode | Zero or multiple matches, an event code outside the event-type prefix, or conflicting supplied code and meaning: stop and request one exact event name for the resolved event type. Read failure: stop and report a sanitized diagnostic. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Event type lookup succeeds | For REST/Data Loader, use the returned LookupCode as EventTypeCode. For FSM CSV, use it as EventType. |
| Event name lookup succeeds | For REST/Data Loader, use the returned LookupCode as EventCode. For FSM CSV, use it as EventName. |
| Either lookup is zero-match, ambiguous, conflicting, or unreadable | Stop before Data Loader metadata preflight or handoff. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IBEC.RESOLVE_EVENT_TYPE | step | 20 | reference_lookup | resolved->IBEC.RESOLVE_EVENT_NAME;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | IBEC.VALIDATE_INPUT | stop | EventTypeCode or EventType meaning is supplied |
| IBEC.RESOLVE_EVENT_NAME | step | 30 | reference_lookup | resolved->IBEC.CONFIRM_FUSION_DATA_FOUNDATION;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | IBEC.RESOLVE_EVENT_TYPE | stop | EventCode or EventName meaning is supplied after event type resolution |
