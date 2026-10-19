# Manage Business Event Trigger Points Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EventEnabledFlag | true | The user intent is activate | No | |
| EventEnabledFlag | false | The user intent is inactivate | No | |
| EventCriteriaId | -1 | The row is the explicit `ORDER_ATTRIBUTE_UPDATE` event row | Yes | |
| EventEnabledFlag | true or false | The row is the explicit `ORDER_ATTRIBUTE_UPDATE` event row and the user supplied activate or inactivate; never default it from attribute activity | No | |
| ConfigurationAction | create | No configured `ORDER_ATTRIBUTE_UPDATE` attribute row has the requested EventCriteriaId | Yes | resolve_existing_order_attribute_update_attributes |
| EventEnabledFlag | true | The row is a new `ORDER_ATTRIBUTE_UPDATE` attribute row requested for add, or no configured row has the requested EventCriteriaId | Yes | resolve_order_attribute_update_event_criteria |
| EventEnabledFlag | false | A matched `ORDER_ATTRIBUTE_UPDATE` attribute row is requested for removal | Yes | resolve_existing_order_attribute_update_attributes |
| EventEnabledFlag | true | A re-add request matches a disabled `ORDER_ATTRIBUTE_UPDATE` attribute row; do not prepare a row already enabled | Yes | resolve_existing_order_attribute_update_attributes |
| ConfigurationAction | create | An activation lookup returns EventDetailId -1 | No | resolve_existing_business_event_detail_for_activation |
| ConfigurationAction | update | An activation lookup returns an EventDetailId other than -1 | No | resolve_existing_business_event_detail_for_activation |
| EventDetailId | blank | ConfigurationAction is create | Yes | |
| EventCriteriaId | -1 | EventCode is `CANCEL_BACKORDERS`, `CHANGE_COMP_COMPLETE`, `FULFILL_LINE_CLOSE`, `FLINE_STATUS_UPDATE`, `HOLD`, `RELEASE_HOLD`, or `SPLIT` | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUSINESS_EVENT_TRIGGER_POINTS.APPLY_CONFIGURATION_ACTION | step | 39 | apply_default | default-applied->BUSINESS_EVENT_TRIGGER_POINTS.APPLY_EVENT_CRITERIA_ID;invalid-event-detail->RETURN_ISSUES | BUSINESS_EVENT_TRIGGER_POINTS.RESOLVE_EXISTING_EVENT_DETAIL | stop | An explicit event-enable request has resolved EventDetailId; retain it for update, or leave the explicit parent-event source EventDetailId blank for create. |
| BUSINESS_EVENT_TRIGGER_POINTS.APPLY_EVENT_CRITERIA_ID | step | 40 | apply_default | default-applied->BUSINESS_EVENT_TRIGGER_POINTS.APPLY_EVENT_ENABLED_FLAG;not-applicable->BUSINESS_EVENT_TRIGGER_POINTS.APPLY_EVENT_ENABLED_FLAG | BUSINESS_EVENT_TRIGGER_POINTS.RESOLVE_EVENT_CODE | stop | EventCode is `CANCEL_BACKORDERS`, `CHANGE_COMP_COMPLETE`, `FULFILL_LINE_CLOSE`, `FLINE_STATUS_UPDATE`, `HOLD`, `RELEASE_HOLD`, or `SPLIT`. |
| BUSINESS_EVENT_TRIGGER_POINTS.APPLY_EVENT_ENABLED_FLAG | step | 41 | apply_default | default-applied->BUSINESS_EVENT_TRIGGER_POINTS.ENFORCE_CONTRACT;invalid-intent->RETURN_ISSUES | BUSINESS_EVENT_TRIGGER_POINTS.RESOLVE_EVENT_CODE | stop | Set the `ORDER_ATTRIBUTE_UPDATE` parent-event row only from a supplied explicit activate or inactivate intent. Create a separate attribute row with EventEnabledFlag true when no configured row has the requested EventCriteriaId. Set every re-added disabled attribute row to true. For a removal request, retain every matched attribute row and set EventEnabledFlag false. Report each already-enabled re-add row as a duplicate and do not prepare it. |
